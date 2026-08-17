/*
 * The sweep kernel: one index in, one candidate tested against the escrow.
 *
 * Concatenate ahead of this file, in this order, the reference solver's
 * common, ripemd, sha2, secp256k1_common, secp256k1_scalar, secp256k1_field,
 * secp256k1_group, secp256k1_prec, secp256k1, address, mnemonic_constants,
 * then this repository's unrank.cl and keccak.cl. tools/gpu/run_sweep.py does
 * that assembly; the order matters and is the order the reference project uses.
 *
 * Per work item:
 *   1. index to 12 wordlist indices        (unrank.cl, checked against the reference)
 *   2. BIP39 checksum, and stop if it fails (unrank.cl; discards 15 in 16)
 *   3. mnemonic string, then PBKDF2-HMAC-SHA512 x2048 to a 64-byte seed
 *   4. BIP32 to m/44'/60'/0'/0/0
 *   5. Keccak-256 of the uncompressed public key, low 20 bytes
 *   6. compare to the target, and report the index if it matches
 *
 * Step 3 is essentially all of the cost. Steps 1 and 2 exist to keep 15 of
 * every 16 candidates from reaching it.
 */

#define ETH_PURPOSE 44
#define ETH_COIN_TYPE 60

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

  /* the mnemonic as a space-separated string, no trailing space */
  uchar mnemonic[180];
  for (int i = 0; i < 180; i++) mnemonic[i] = 0;
  uint at = 0;
  for (int i = 0; i < 12; i++) {
    uint wi = w12[i];
    uint len = word_lengths[wi];
    for (uint j = 0; j < len; j++) mnemonic[at++] = words[wi][j];
    mnemonic[at++] = 32;
  }
  at--;                      /* drop the trailing space */
  mnemonic[at] = 0;
  uint mnemonic_length = at;

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
    if (digest[12 + i] != target20[i]) return;
  }

  /* a match: record the index and the words, and let the host confirm it */
  found_flag[0] = 1;
  found_index[0] = idx;
  for (uint i = 0; i < mnemonic_length; i++) found_words[i] = mnemonic[i];
  found_words[mnemonic_length] = 0;
}
