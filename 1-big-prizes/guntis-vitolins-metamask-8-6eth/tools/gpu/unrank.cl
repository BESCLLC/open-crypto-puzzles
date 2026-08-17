/*
 * Index to candidate, on device.
 *
 * Each work item gets one integer and must produce one 12-word candidate with
 * no shared state. The mapping has to be the same bijection tools/gpu_reference.py
 * implements, candidate for candidate, or a sweep silently searches something
 * other than what was priced and its negative is worthless.
 *
 *     idx = ((psub * n_vsub) + vsub) * 362880 + perm
 *
 * The 9 non-anchor words are sorted ascending by wordlist index before the
 * permutation is applied. That matters: the reference sorts them alphabetically,
 * and the BIP39 English list is stored in alphabetical order, so sorting by
 * index here is the same ordering. If that ever stops being true the two
 * implementations diverge, which is why the reference asserts it.
 */

#define PERM9 362880UL
#define SLOT_WATER 4
#define SLOT_LAST 11

/* binomial(n, k) for the small n and k this search uses */
static ulong binom(uint n, uint k) {
  if (k > n) return 0;
  if (k > n - k) k = n - k;
  ulong r = 1;
  for (uint i = 0; i < k; i++) {
    r = r * (ulong)(n - i) / (ulong)(i + 1);
  }
  return r;
}

/* the rank-th k-subset of [0, n), lexicographic, written into out */
static void unrank_comb(ulong rank, uint n, uint k, uint *out) {
  uint x = 0, at = 0;
  while (k > 0) {
    ulong c = binom(n - x - 1, k - 1);
    if (rank < c) {
      out[at++] = x;
      k--;
    } else {
      rank -= c;
    }
    x++;
  }
}

/* the rank-th permutation of the 9 values in pool, lexicographic (Lehmer) */
static void unrank_perm9(ulong rank, const ushort *pool, ushort *out) {
  ushort work[9];
  uint left = 9;
  for (int i = 0; i < 9; i++) work[i] = pool[i];
  ulong f[9] = {40320UL, 5040UL, 720UL, 120UL, 24UL, 6UL, 2UL, 1UL, 1UL};
  for (int i = 0; i < 9; i++) {
    ulong fact = f[i];
    uint j = (uint)(rank / fact);
    rank = rank % fact;
    out[i] = work[j];
    for (uint m = j; m + 1 < left; m++) work[m] = work[m + 1];
    left--;
  }
}

/*
 * Produce the 12 wordlist indices for one candidate.
 *
 * post_forced holds 3 entries and its first is the word anchored at position 1.
 * video_forced holds 2, the last-position word and the water word, in that
 * order. The free arrays hold the pool words the forced ones exclude, ascending.
 */
static void candidate_for_index(
    ulong idx,
    __global const ushort *post_free, uint n_post_free,
    __global const ushort *video_free, uint n_video_free,
    __global const ushort *post_forced,
    __global const ushort *video_forced,
    ushort *out12) {

  ulong n_vsub = binom(n_video_free, 4);
  ulong perm = idx % PERM9;
  ulong rest = idx / PERM9;
  ulong vsub = rest % n_vsub;
  ulong psub = rest / n_vsub;

  uint pc[3], vc[4];
  unrank_comb(psub, n_post_free, 3, pc);
  unrank_comb(vsub, n_video_free, 4, vc);

  /* the 9 that are not anchored: post_forced[1..2], the 3 chosen post words,
     and the 4 chosen video words */
  ushort free9[9];
  uint at = 0;
  free9[at++] = post_forced[1];
  free9[at++] = post_forced[2];
  for (int i = 0; i < 3; i++) free9[at++] = post_free[pc[i]];
  for (int i = 0; i < 4; i++) free9[at++] = video_free[vc[i]];

  /* insertion sort, 9 elements, ascending by wordlist index */
  for (uint i = 1; i < 9; i++) {
    ushort v = free9[i];
    int j = (int)i - 1;
    while (j >= 0 && free9[j] > v) {
      free9[j + 1] = free9[j];
      j--;
    }
    free9[j + 1] = v;
  }

  ushort placed[9];
  unrank_perm9(perm, free9, placed);

  const uint slots[9] = {1, 2, 3, 5, 6, 7, 8, 9, 10};
  out12[0] = post_forced[0];
  out12[SLOT_WATER] = video_forced[1];
  out12[SLOT_LAST] = video_forced[0];
  for (int i = 0; i < 9; i++) out12[slots[i]] = placed[i];
}


/*
 * SHA-256 of exactly 16 bytes, for the BIP39 checksum.
 *
 * Written here rather than pulled from a general SHA-2 implementation because
 * the input is one fixed-size block: 16 bytes of message, the 0x80 pad byte,
 * zeros, and a 64-bit length of 128 bits. No message schedule across blocks,
 * no length branching. Only the first byte of the digest is ever read.
 */

__constant uint SHA256_K[64] = {
  0x428a2f98u,0x71374491u,0xb5c0fbcfu,0xe9b5dba5u,0x3956c25bu,0x59f111f1u,
  0x923f82a4u,0xab1c5ed5u,0xd807aa98u,0x12835b01u,0x243185beu,0x550c7dc3u,
  0x72be5d74u,0x80deb1feu,0x9bdc06a7u,0xc19bf174u,0xe49b69c1u,0xefbe4786u,
  0x0fc19dc6u,0x240ca1ccu,0x2de92c6fu,0x4a7484aau,0x5cb0a9dcu,0x76f988dau,
  0x983e5152u,0xa831c66du,0xb00327c8u,0xbf597fc7u,0xc6e00bf3u,0xd5a79147u,
  0x06ca6351u,0x14292967u,0x27b70a85u,0x2e1b2138u,0x4d2c6dfcu,0x53380d13u,
  0x650a7354u,0x766a0abbu,0x81c2c92eu,0x92722c85u,0xa2bfe8a1u,0xa81a664bu,
  0xc24b8b70u,0xc76c51a3u,0xd192e819u,0xd6990624u,0xf40e3585u,0x106aa070u,
  0x19a4c116u,0x1e376c08u,0x2748774cu,0x34b0bcb5u,0x391c0cb3u,0x4ed8aa4au,
  0x5b9cca4fu,0x682e6ff3u,0x748f82eeu,0x78a5636fu,0x84c87814u,0x8cc70208u,
  0x90befffau,0xa4506cebu,0xbef9a3f7u,0xc67178f2u
};

#define ROTR32(x,n) (((x) >> (n)) | ((x) << (32 - (n))))

static uint sha256_first_byte_of_16(const uchar *msg) {
  uint w[64];
  uchar blk[64];
  for (int i = 0; i < 64; i++) blk[i] = 0;
  for (int i = 0; i < 16; i++) blk[i] = msg[i];
  blk[16] = 0x80;
  blk[62] = 0x00; blk[63] = 128;          /* length in bits, big-endian */

  for (int i = 0; i < 16; i++)
    w[i] = ((uint)blk[i*4] << 24) | ((uint)blk[i*4+1] << 16)
         | ((uint)blk[i*4+2] << 8) | (uint)blk[i*4+3];
  for (int i = 16; i < 64; i++) {
    uint s0 = ROTR32(w[i-15],7) ^ ROTR32(w[i-15],18) ^ (w[i-15] >> 3);
    uint s1 = ROTR32(w[i-2],17) ^ ROTR32(w[i-2],19) ^ (w[i-2] >> 10);
    w[i] = w[i-16] + s0 + w[i-7] + s1;
  }

  uint a=0x6a09e667u,b=0xbb67ae85u,c=0x3c6ef372u,d=0xa54ff53au,
       e=0x510e527fu,f=0x9b05688cu,g=0x1f83d9abu,h=0x5be0cd19u;
  for (int i = 0; i < 64; i++) {
    uint S1 = ROTR32(e,6) ^ ROTR32(e,11) ^ ROTR32(e,25);
    uint ch = (e & f) ^ ((~e) & g);
    uint t1 = h + S1 + ch + SHA256_K[i] + w[i];
    uint S0 = ROTR32(a,2) ^ ROTR32(a,13) ^ ROTR32(a,22);
    uint mj = (a & b) ^ (a & c) ^ (b & c);
    uint t2 = S0 + mj;
    h=g; g=f; f=e; e=d+t1; d=c; c=b; b=a; a=t1+t2;
  }
  return (0x6a09e667u + a) >> 24;         /* the first digest byte */
}

/*
 * BIP39 checksum over 12 word indices: 132 bits split as 128 entropy plus a
 * 4-bit checksum, which must equal the top 4 bits of sha256(entropy). Pure
 * SHA256, and it rejects 15 of every 16 candidates before the expensive part.
 */
static bool checksum_ok(const ushort *w12) {
  /*
   * 132 bits, written most-significant first into 17 bytes: the first 16 are
   * the entropy, and bits 128 to 131 land in the high nibble of byte 16.
   *
   * Done bit by bit rather than through 64-bit accumulators on purpose. Six
   * words is 66 bits, which does not fit a ulong, and an earlier version of
   * this function silently dropped the top 2 bits that way.
   */
  uchar buf[17];
  for (int i = 0; i < 17; i++) buf[i] = 0;

  uint bit = 0;
  for (int i = 0; i < 12; i++) {
    ushort v = w12[i];
    for (int b = 10; b >= 0; b--) {
      if ((v >> b) & 1) buf[bit >> 3] |= (uchar)(0x80u >> (bit & 7));
      bit++;
    }
  }

  uchar checksum = (uchar)(buf[16] >> 4);
  uint first = sha256_first_byte_of_16(buf);
  return (uchar)((first >> 4) & 0x0F) == checksum;
}
