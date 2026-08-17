/*
 * The sweep kernels: one index in, one candidate tested against the escrow.
 *
 * Concatenate ahead of this file, in this order, the reference solver's
 * common, ripemd, sha2, secp256k1_common, secp256k1_scalar, secp256k1_field,
 * secp256k1_group, secp256k1_prec, secp256k1, address, mnemonic_constants,
 * then this repository's unrank.cl and keccak.cl. tools/gpu/run_sweep.py does
 * that assembly; the order matters and is the order the reference project uses.
 *
 * The work is split across two kernels, and the reason is worth stating because
 * the obvious single-kernel version is 16 times slower.
 *
 * A GPU executes 32 lanes in lockstep. The BIP39 checksum passes 1 candidate in
 * 16, so a warp of 32 lanes holds a surviving candidate 87% of the time
 * (1 - (15/16)^32). In a single kernel that tests the checksum and then falls
 * through to PBKDF2, those 87% of warps pay the full 2048-iteration cost while
 * only about 2 of their 32 lanes are doing anything useful. Measured on an RTX
 * 5090 that was 842,450 indices/sec, which is only 52,653 derivations/sec: the
 * card was doing the work, and 94% of it was thrown away.
 *
 * So: filter_pass does the cheap part and compacts the survivors into a dense
 * array, and derive_pass reads that array, where every lane has real work.
 *
 *   filter_pass : index -> 12 words -> checksum -> append index if it survives
 *   derive_pass : survivor index -> mnemonic -> PBKDF2 -> BIP32 -> Keccak -> compare
 *
 * sweep() keeps the fused form for single-candidate checks, where divergence
 * costs nothing and one kernel is simpler to reason about.
 */

#define ETH_PURPOSE 44
#define ETH_COIN_TYPE 60

/*
 * Derive the MetaMask default address for 12 word indices and compare it to
 * target20. Returns true on an exact match, and writes the mnemonic text and
 * its length out through mnemonic_out and len_out either way.
 */
static bool derive_and_compare(const ushort *w12,
                               __global const uchar *target20,
                               uchar *mnemonic_out, uint *len_out) {
  uchar mnemonic[180];
  for (int i = 0; i < 180; i++) mnemonic[i] = 0;
  uint at = 0;
  for (int i = 0; i < 12; i++) {
    uint wi = w12[i];
    uint len = word_lengths[wi];
    for (uint j = 0; j < len; j++) mnemonic[at++] = words[wi][j];
    mnemonic[at++] = 32;
  }
  at--;                          /* drop the trailing space */
  mnemonic[at] = 0;
  uint mnemonic_length = at;

  for (uint i = 0; i < 180; i++) mnemonic_out[i] = mnemonic[i];
  *len_out = mnemonic_length;

  /* PBKDF2-HMAC-SHA512, 2048 iterations, salt "mnemonic", one output block */
  uchar ipad_key[128];
  uchar opad_key[128];
  for (int x = 0; x < 128; x++) { ipad_key[x] = 0x36; opad_key[x] = 0x5c; }
  for (uint x = 0; x < mnemonic_length; x++) {
    ipad_key[x] = ipad_key[x] ^ mnemonic[x];
    opad_key[x] = opad_key[x] ^ mnemonic[x];
  }

  uchar seed[64] = { 0 };
  uchar sha512_result[64] = { 0 };
  uchar key_previous_concat[256] = { 0 };
  uchar salt[12] = { 109, 110, 101, 109, 111, 110, 105, 99, 0, 0, 0, 1 };
  for (int x = 0; x < 128; x++) key_previous_concat[x] = ipad_key[x];
  for (int x = 0; x < 12; x++) key_previous_concat[x + 128] = salt[x];

  sha512(&key_previous_concat, 140, &sha512_result);
  copy_pad_previous(&opad_key, &sha512_result, &key_previous_concat);
  sha512(&key_previous_concat, 192, &sha512_result);
  xor_seed_with_round(&seed, &sha512_result);

  for (int x = 1; x < 2048; x++) {
    copy_pad_previous(&ipad_key, &sha512_result, &key_previous_concat);
    sha512(&key_previous_concat, 192, &sha512_result);
    copy_pad_previous(&opad_key, &sha512_result, &key_previous_concat);
    sha512(&key_previous_concat, 192, &sha512_result);
    xor_seed_with_round(&seed, &sha512_result);
  }

  /* BIP32 to MetaMask's default account, m/44'/60'/0'/0/0 */
  extended_private_key_t master_private;
  extended_private_key_t target_key;
  extended_public_key_t target_public_key;

  new_master_from_seed(BITCOIN_MAINNET, &seed, &master_private);
  hardened_private_child_from_private(&master_private, &target_key, ETH_PURPOSE);
  hardened_private_child_from_private(&target_key, &target_key, ETH_COIN_TYPE);
  hardened_private_child_from_private(&target_key, &target_key, 0);
  normal_private_child_from_private(&target_key, &target_key, 0);
  normal_private_child_from_private(&target_key, &target_key, 0);
  public_from_private(&target_key, &target_public_key);

  /* the Ethereum address: Keccak-256 over the 64 bytes after the 0x04 prefix */
  uchar uncompressed[65];
  uncompressed_public_key(&target_public_key, &uncompressed);
  uchar body[64];
  for (int i = 0; i < 64; i++) body[i] = uncompressed[i + 1];
  uchar digest[32];
  keccak256_64(body, digest);

  for (int i = 0; i < 20; i++) {
    if (digest[12 + i] != target20[i]) return false;
  }
  return true;
}

/*
 * Pass 1. Cheap: unrank and checksum only. Survivors are appended to a dense
 * array through an atomic counter, so pass 2 has no idle lanes. Nothing is
 * written past capacity; the host checks the count and refuses to proceed on
 * an overflow rather than silently searching a truncated list.
 */
__kernel void filter_pass(
    ulong base_index,
    __global const ushort *post_free, uint n_post_free,
    __global const ushort *video_free, uint n_video_free,
    __global const ushort *post_forced,
    __global const ushort *video_forced,
    __global uint *count,
    __global ulong *survivors,
    uint capacity) {

  ulong idx = base_index + (ulong)get_global_id(0);
  ushort w12[12];
  candidate_for_index(idx, post_free, n_post_free, video_free, n_video_free,
                      post_forced, video_forced, w12);
  if (!checksum_ok(w12)) return;

  uint slot = atomic_inc(count);
  if (slot < capacity) survivors[slot] = idx;
}

/*
 * Pass 2. Every lane derives; there is nothing to diverge on.
 */
__kernel void derive_pass(
    __global const ulong *survivors, uint n_survivors,
    __global const ushort *post_free, uint n_post_free,
    __global const ushort *video_free, uint n_video_free,
    __global const ushort *post_forced,
    __global const ushort *video_forced,
    __global const uchar *target20,
    __global uchar *found_flag,
    __global ulong *found_index,
    __global uchar *found_words) {

  uint g = get_global_id(0);
  if (g >= n_survivors) return;
  ulong idx = survivors[g];

  ushort w12[12];
  candidate_for_index(idx, post_free, n_post_free, video_free, n_video_free,
                      post_forced, video_forced, w12);

  uchar mnemonic[180];
  uint len;
  if (!derive_and_compare(w12, target20, mnemonic, &len)) return;

  found_flag[0] = 1;
  found_index[0] = idx;
  for (uint i = 0; i < len; i++) found_words[i] = mnemonic[i];
  found_words[len] = 0;
}

/*
 * The fused form, kept for single-candidate checks such as the witness
 * protocol's, where one index is tested on its own and divergence is free.
 */
__kernel void sweep(
    ulong base_index,
    __global const ushort *post_free, uint n_post_free,
    __global const ushort *video_free, uint n_video_free,
    __global const ushort *post_forced,
    __global const ushort *video_forced,
    __global const uchar *target20,
    __global uchar *found_flag,
    __global ulong *found_index,
    __global uchar *found_words) {

  ulong idx = base_index + (ulong)get_global_id(0);
  ushort w12[12];
  candidate_for_index(idx, post_free, n_post_free, video_free, n_video_free,
                      post_forced, video_forced, w12);
  if (!checksum_ok(w12)) return;

  uchar mnemonic[180];
  uint len;
  if (!derive_and_compare(w12, target20, mnemonic, &len)) return;

  found_flag[0] = 1;
  found_index[0] = idx;
  for (uint i = 0; i < len; i++) found_words[i] = mnemonic[i];
  found_words[len] = 0;
}
