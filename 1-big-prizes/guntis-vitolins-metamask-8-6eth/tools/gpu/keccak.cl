/*
 * Keccak-256 as Ethereum uses it, specialised to a single 64-byte input.
 *
 * Ethereum's address hash is Keccak-256 (the original padding, 0x01, not
 * SHA3-256's 0x06) over the 64-byte uncompressed public key with its 0x04
 * prefix stripped. The address is the low 20 bytes of the digest.
 *
 * The input is always exactly 64 bytes, which is below the 136-byte rate, so
 * the sponge absorbs one padded block and squeezes once. No loop, no length
 * handling, nothing to get wrong at a block boundary.
 */

__constant ulong KECCAK_RC[24] = {
  0x0000000000000001UL, 0x0000000000008082UL, 0x800000000000808aUL,
  0x8000000080008000UL, 0x000000000000808bUL, 0x0000000080000001UL,
  0x8000000080008081UL, 0x8000000000008009UL, 0x000000000000008aUL,
  0x0000000000000088UL, 0x0000000080008009UL, 0x000000008000000aUL,
  0x000000008000808bUL, 0x800000000000008bUL, 0x8000000000008089UL,
  0x8000000000008003UL, 0x8000000000008002UL, 0x8000000000000080UL,
  0x000000000000800aUL, 0x800000008000000aUL, 0x8000000080008081UL,
  0x8000000000008080UL, 0x0000000080000001UL, 0x8000000080008008UL
};

__constant int KECCAK_ROT[25] = {
   0,  1, 62, 28, 27,
  36, 44,  6, 55, 20,
   3, 10, 43, 25, 39,
  41, 45, 15, 21,  8,
  18,  2, 61, 56, 14
};

#define ROTL64(x, n) (((n) == 0) ? (x) : (((x) << (n)) | ((x) >> (64 - (n)))))

static void keccak_f1600(ulong *A) {
  for (int round = 0; round < 24; round++) {
    ulong C[5], D[5], B[25];

    for (int x = 0; x < 5; x++)
      C[x] = A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20];

    for (int x = 0; x < 5; x++)
      D[x] = C[(x + 4) % 5] ^ ROTL64(C[(x + 1) % 5], 1);

    for (int x = 0; x < 5; x++)
      for (int y = 0; y < 5; y++)
        A[x + 5 * y] ^= D[x];

    /* rho then pi, in one pass: B[y][2x+3y] <- rot(A[x][y]) */
    for (int x = 0; x < 5; x++) {
      for (int y = 0; y < 5; y++) {
        int r = KECCAK_ROT[x + 5 * y];
        B[y + 5 * ((2 * x + 3 * y) % 5)] = ROTL64(A[x + 5 * y], r);
      }
    }

    for (int x = 0; x < 5; x++)
      for (int y = 0; y < 5; y++)
        A[x + 5 * y] = B[x + 5 * y]
                     ^ ((~B[((x + 1) % 5) + 5 * y]) & B[((x + 2) % 5) + 5 * y]);

    A[0] ^= KECCAK_RC[round];
  }
}

/*
 * in  : 64 bytes, the uncompressed public key without its 0x04 prefix
 * out : 32 bytes, the Keccak-256 digest. The Ethereum address is out[12..31].
 */
static void keccak256_64(const uchar *in, uchar *out) {
  ulong A[25];
  for (int i = 0; i < 25; i++) A[i] = 0;

  /* absorb: 64 bytes little-endian into the first 8 lanes */
  for (int i = 0; i < 8; i++) {
    ulong lane = 0;
    for (int b = 0; b < 8; b++)
      lane |= ((ulong)in[i * 8 + b]) << (8 * b);
    A[i] = lane;
  }

  /* pad10*1 over the 136-byte rate: 0x01 at offset 64, 0x80 at offset 135 */
  A[8] ^= 0x0000000000000001UL;          /* byte 64, lane 8, position 0 */
  A[16] ^= 0x8000000000000000UL;         /* byte 135, lane 16, position 7 */

  keccak_f1600(A);

  /* squeeze the first 32 bytes */
  for (int i = 0; i < 4; i++)
    for (int b = 0; b < 8; b++)
      out[i * 8 + b] = (uchar)((A[i] >> (8 * b)) & 0xFF);
}
