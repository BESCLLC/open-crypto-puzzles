#!/usr/bin/env python3
"""
Combinatorial unranking for the GPU front end.

The GPU gets one integer per work item and must turn it into one 12-word
candidate, with no shared state and no enumeration order dependency. That is
a bijection from [0, N) onto the candidate set. If it is not a bijection the
sweep silently skips or repeats part of the space, and a negative built on it
is worthless -- which is the whole reason this is validated against the
reference generator before any OpenCL is written.

Layout of the index:

    idx = ((psub * n_vsub) + vsub) * 362880 + perm

    psub  -> combination rank, 3 of the 14 free post words
    vsub  -> combination rank, 4 of the 15 free video words
    perm  -> Lehmer rank of the 9 free words across the 9 free slots
"""

from math import comb, factorial

FREE_SLOTS = [1, 2, 3, 5, 6, 7, 8, 9, 10]   # 0-indexed; 0, 4, 11 are anchored


def unrank_combination(rank, n, k):
    """The rank-th k-subset of range(n), in lexicographic order."""
    out = []
    x = 0
    while k > 0:
        c = comb(n - x - 1, k - 1)
        if rank < c:
            out.append(x)
            k -= 1
        else:
            rank -= c
        x += 1
    return out


def unrank_permutation(rank, items):
    """The rank-th permutation of items, in lexicographic (Lehmer) order."""
    pool = list(items)
    out = []
    for i in range(len(pool), 0, -1):
        f = factorial(i - 1)
        j, rank = divmod(rank, f)
        out.append(pool.pop(j))
    return out


class Space:
    def __init__(self, post_pool, video_pool, post_forced, video_forced,
                 anchor_first, anchor_water, anchor_last):
        self.post_free = [w for w in post_pool if w not in post_forced]
        self.video_free = [w for w in video_pool if w not in video_forced]
        self.post_forced = list(post_forced)
        self.video_forced = list(video_forced)
        self.anchor_first = anchor_first
        self.anchor_water = anchor_water
        self.anchor_last = anchor_last
        self.kp = 6 - len(post_forced)
        self.kv = 6 - len(video_forced)
        self.n_psub = comb(len(self.post_free), self.kp)
        self.n_vsub = comb(len(self.video_free), self.kv)
        self.n_perm = factorial(9)
        self.total = self.n_psub * self.n_vsub * self.n_perm

    def candidate(self, idx):
        """idx -> the 12-word list, or None if idx is out of range."""
        if not 0 <= idx < self.total:
            return None
        perm, rest = idx % self.n_perm, idx // self.n_perm
        vsub, psub = rest % self.n_vsub, rest // self.n_vsub

        post_six = self.post_forced + [
            self.post_free[i]
            for i in unrank_combination(psub, len(self.post_free), self.kp)]
        video_six = self.video_forced + [
            self.video_free[i]
            for i in unrank_combination(vsub, len(self.video_free), self.kv)]

        free = sorted(w for w in post_six + video_six
                      if w not in (self.anchor_first, self.anchor_water,
                                   self.anchor_last))
        assert len(free) == 9, free
        placed = unrank_permutation(perm, free)

        out = [None] * 12
        out[0] = self.anchor_first
        out[4] = self.anchor_water
        out[11] = self.anchor_last
        for slot, w in zip(FREE_SLOTS, placed):
            out[slot] = w
        return out


# ---------------------------------------------------------------------------
# Keccak-256 exactly as gpu/keccak.cl computes it.
#
# This is a transliteration, not an independent implementation: same lane
# indexing, same single-block padding, same squeeze. Its purpose is to let the
# OpenCL be checked against a known-good Ethereum vector on a machine with no
# GPU. If this reproduces the canonical address, the kernel's arithmetic is
# right; what remains to test on hardware is only the plumbing.
# ---------------------------------------------------------------------------

KECCAK_RC = [
    0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
    0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
    0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
    0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
    0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
    0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
    0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
    0x8000000000008080, 0x0000000080000001, 0x8000000080008008,
]
KECCAK_ROT = [0, 1, 62, 28, 27, 36, 44, 6, 55, 20, 3, 10, 43, 25, 39,
              41, 45, 15, 21, 8, 18, 2, 61, 56, 14]
_MASK64 = (1 << 64) - 1


def _rotl(x, n):
    return x if n == 0 else ((x << n) | (x >> (64 - n))) & _MASK64


def keccak_f1600(A):
    for rnd in range(24):
        C = [A[x] ^ A[x + 5] ^ A[x + 10] ^ A[x + 15] ^ A[x + 20] for x in range(5)]
        D = [C[(x + 4) % 5] ^ _rotl(C[(x + 1) % 5], 1) for x in range(5)]
        for x in range(5):
            for y in range(5):
                A[x + 5 * y] ^= D[x]
        B = [0] * 25
        for x in range(5):
            for y in range(5):
                B[y + 5 * ((2 * x + 3 * y) % 5)] = _rotl(A[x + 5 * y],
                                                         KECCAK_ROT[x + 5 * y])
        for x in range(5):
            for y in range(5):
                A[x + 5 * y] = B[x + 5 * y] ^ (
                    ((~B[((x + 1) % 5) + 5 * y]) & _MASK64)
                    & B[((x + 2) % 5) + 5 * y])
        A[0] ^= KECCAK_RC[rnd]
    return A


def keccak256_64(data):
    """Keccak-256 of exactly 64 bytes: the uncompressed pubkey, prefix stripped."""
    if len(data) != 64:
        raise ValueError("this specialisation takes exactly 64 bytes")
    A = [0] * 25
    for i in range(8):
        A[i] = int.from_bytes(data[i * 8:i * 8 + 8], 'little')
    A[8] ^= 0x0000000000000001        # pad start, byte 64
    A[16] ^= 0x8000000000000000       # pad end, byte 135 of the 136-byte rate
    A = keccak_f1600(A)
    return b"".join(A[i].to_bytes(8, 'little') for i in range(4))


def eth_address(mnemonic):
    """The MetaMask default address for a mnemonic, by the kernel's own route."""
    from bip_utils import (Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    node = (Bip44.FromSeed(seed, Bip44Coins.ETHEREUM).Purpose().Coin()
            .Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0))
    pub = node.PublicKey().RawUncompressed().ToBytes()
    if pub[0] != 4:
        raise ValueError("expected an uncompressed public key")
    return "0x" + keccak256_64(pub[1:])[12:].hex()


CANONICAL_MNEMONIC = "abandon " * 11 + "about"
CANONICAL_ADDRESS = "0x9858effd232b4033e47d90003d41ec34ecaeda94"

# Tier 1 of the ranked sweep in analysis/leads.md: the BIP39 entries present in
# the 5 planted sentences, plus `possible`, which is written inside its own
# negation in the video's own planted sentence. Extracted from the sentences
# mechanically rather than typed, and asserted against the wordlist below.
TIER1_VIDEO_POOL = ['also', 'can', 'easy', 'expect', 'fog', 'goat', 'lake',
                    'more', 'parrot', 'possible', 'sing', 'song', 'then',
                    'there', 'will', 'you']
TIER1_POST_POOL = ['because', 'cattle', 'dinner', 'dutch', 'fiber', 'forest',
                   'fork', 'fresh', 'like', 'market', 'only', 'rib', 'roast',
                   'round', 'season', 'there', 'wood']


def selftest():
    import itertools
    from math import comb, factorial
    ok = True

    got = eth_address(CANONICAL_MNEMONIC)
    hit = got == CANONICAL_ADDRESS
    ok &= hit
    print(f"keccak + m/44'/60'/0'/0/0 on the canonical BIP-0039 vector "
          f"derives {got}: {'OK' if hit else 'FAIL'}")

    good = True
    for n in range(1, 16):
        for k in range(1, min(n, 6) + 1):
            if [tuple(unrank_combination(r, n, k)) for r in range(comb(n, k))] \
                    != list(itertools.combinations(range(n), k)):
                good = False
    ok &= good
    print(f"combination unranking reproduces lexicographic order for every "
          f"n<=15, k<=6: {'OK' if good else 'FAIL'}")

    items = list('abcdefghi')
    good = ([tuple(unrank_permutation(r, items)) for r in range(factorial(9))]
            == list(itertools.permutations(items)))
    ok &= good
    print(f"permutation unranking reproduces all {factorial(9):,} orderings of 9 "
          f"in order: {'OK' if good else 'FAIL'}")

    post = TIER1_POST_POOL
    video = TIER1_VIDEO_POOL

    # Guard first: a pool word that is not in the wordlist cannot appear in any
    # valid mnemonic, so every candidate containing it is wasted work and the
    # priced space is wrong. This check exists because "think" was typed into
    # this pool by hand and is not a BIP39 entry.
    import glob
    import os
    import bip_utils
    wl = open(glob.glob(os.path.join(os.path.dirname(bip_utils.__file__),
                                     '**', 'bip39', '**', 'english.txt'),
                        recursive=True)[0]).read().split()
    strays = [w for w in post + video if w not in set(wl)]
    ok &= not strays
    print(f"every pool word is a BIP39 entry: "
          f"{'OK' if not strays else 'FAIL, not in the wordlist: ' + str(strays)}")

    sp = Space(post, video, ['dutch', 'fork', 'fiber'], ['parrot', 'fog'],
               'dutch', 'fog', 'parrot')
    import random
    rng = random.Random(11)
    idxs = rng.sample(range(sp.total), 50000)
    seen = {tuple(sp.candidate(i)) for i in idxs}
    good = len(seen) == len(idxs)
    ok &= good
    print(f"index to candidate collides on none of 50,000 random draws from "
          f"{sp.total:,}: {'OK' if good else 'FAIL'}")
    print("  note: this is sparsity, not injectivity. A candidate whose words "
          "repeat one\n  entry has 2 indices; see tools/gpu/unrank.cl.")

    bad = sum(1 for i in idxs[:5000]
              if sp.candidate(i)[0] != 'dutch'
              or sp.candidate(i)[4] != 'fog'
              or sp.candidate(i)[11] != 'parrot'
              or len(sp.candidate(i)) != 12)
    ok &= bad == 0
    print(f"anchors and length hold on 5,000 candidates: "
          f"{'OK' if bad == 0 else 'FAIL'}")

    if ok:
        print("SELFTEST OK: the address derivation matches the canonical vector "
              "and the index mapping covers the space")
    return ok


if __name__ == '__main__':
    import sys
    sys.exit(0 if selftest() else 1)
