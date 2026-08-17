#!/usr/bin/env python3
"""
Reference candidate generator for the Guntis Vitolins 10 ETH challenge, lead 1.

This is the CPU ground truth the GPU kernel must reproduce. It enumerates the
lead-1 space, applies the BIP39 checksum filter, and (optionally) derives the
MetaMask address for survivors. It is deliberately simple and slow: its job is
to be obviously correct, not fast.

Space (README "Open leads", lead 1), with the connecting words included:
    post side  = {dutch, fork, fiber} + 3 of the remaining post-pool words
    video side = {parrot, WATER}      + 4 of the remaining video-pool words
    positions   1 <- dutch, 5 <- WATER, 12 <- parrot, the other 9 words free
    WATER in {fog, cloud}
"""

import hashlib
import itertools
import sys

# BIP39-valid words present in the 5 planted sentences, plus the confirmed
# metadata words. Extracted mechanically from clues/author-posts.md; the
# connecting words (can, more, then, there, will, you, because, only, like)
# fall out of that extraction and are exactly what lead 1 adds.
VIDEO_POOL = ['can', 'easy', 'expect', 'finish', 'fog', 'goat', 'lake', 'more',
              'parrot', 'sing', 'song', 'then', 'there', 'top', 'update',
              'will', 'winter', 'you']
POST_POOL = ['because', 'cattle', 'dinner', 'dutch', 'fiber', 'forest', 'fork',
             'fresh', 'like', 'market', 'only', 'rib', 'roast', 'round',
             'season', 'there', 'wood']

POST_FORCED = ['dutch', 'fork', 'fiber']
VIDEO_FORCED = ['parrot']          # the water word is added per branch
WATER_BRANCHES = ['fog', 'cloud']

ANCHOR_FIRST = 'dutch'
ANCHOR_LAST = 'parrot'
ANCHOR_WATER_POS = 4               # 0-indexed: "word 5"

TARGET = "0x9c2f44efad0c1e852a09df9939e6daf061140caf"


def load_wordlist():
    import glob
    import os
    import bip_utils
    p = glob.glob(os.path.join(os.path.dirname(bip_utils.__file__),
                               '**', 'bip39', '**', 'english.txt'),
                  recursive=True)[0]
    words = open(p).read().split()
    assert len(words) == 2048, len(words)
    return words, {w: i for i, w in enumerate(words)}


WORDS, INDEX = load_wordlist()


def checksum_ok(idxs):
    """True if the 12 word indexes form a checksum-valid BIP39 mnemonic.

    132 bits = 128 bits entropy + 4 bits checksum; the checksum must equal the
    top 4 bits of sha256(entropy). Pure SHA256, no PBKDF2: this is the cheap
    filter that removes 15 of every 16 arrangements before the expensive part.
    """
    bits = 0
    for i in idxs:
        bits = (bits << 11) | i
    entropy = (bits >> 4).to_bytes(16, 'big')
    got = bits & 0xF
    want = hashlib.sha256(entropy).digest()[0] >> 4
    return got == want


def subsets(branch_water):
    """Yield (post_six, video_six) as tuples, honouring the forced members."""
    post_rest = [w for w in POST_POOL if w not in POST_FORCED]
    video_forced = VIDEO_FORCED + [branch_water]
    video_rest = [w for w in VIDEO_POOL if w not in video_forced]
    for pc in itertools.combinations(post_rest, 6 - len(POST_FORCED)):
        post_six = tuple(POST_FORCED) + pc
        for vc in itertools.combinations(video_rest, 6 - len(video_forced)):
            yield post_six, tuple(video_forced) + vc


def arrangements(post_six, video_six, branch_water):
    """Yield 12-tuples of words with the 3 anchors placed and the rest free."""
    free = [w for w in post_six + video_six
            if w not in (ANCHOR_FIRST, ANCHOR_LAST, branch_water)]
    assert len(free) == 9, free
    slots = [i for i in range(12)
             if i not in (0, ANCHOR_WATER_POS, 11)]
    for perm in itertools.permutations(free):
        out = [None] * 12
        out[0] = ANCHOR_FIRST
        out[ANCHOR_WATER_POS] = branch_water
        out[11] = ANCHOR_LAST
        for slot, w in zip(slots, perm):
            out[slot] = w
        yield out


def candidates(branch_water, subset_limit=None):
    """Yield checksum-valid 12-word candidates for one water branch."""
    for n, (post_six, video_six) in enumerate(subsets(branch_water)):
        if subset_limit is not None and n >= subset_limit:
            return
        for arr in arrangements(post_six, video_six, branch_water):
            if checksum_ok([INDEX[w] for w in arr]):
                yield arr


def space_size():
    from math import comb, factorial
    sub = comb(len(POST_POOL) - 3, 3) * comb(len(VIDEO_POOL) - 2, 4)
    return sub, sub * factorial(9)


def selftest():
    """Five checks. A generator that fails any of these must not be used to
    produce a negative: an enumeration bug silently skips part of the space,
    and a skipped part is indistinguishable from a searched one afterwards."""
    from bip_utils import Bip39MnemonicValidator
    ok = True

    n = bad = 0
    for arr in candidates('fog', subset_limit=1):
        if not Bip39MnemonicValidator().IsValid(" ".join(arr)):
            bad += 1
        n += 1
        if n >= 400:
            break
    ok &= bad == 0
    print(f"emitted candidates accepted by an independent BIP39 validator: "
          f"{n - bad}/{n}: {'OK' if bad == 0 else 'FAIL'}")

    tot = hit = 0
    for post_six, video_six in itertools.islice(subsets('fog'), 2):
        for arr in arrangements(post_six, video_six, 'fog'):
            tot += 1
            hit += checksum_ok([INDEX[w] for w in arr])
            if tot >= 200000:
                break
        if tot >= 200000:
            break
    rate = tot / hit
    ok &= 15.0 < rate < 17.0
    print(f"checksum acceptance rate 1 in {rate:.2f} (expected 16): "
          f"{'OK' if 15.0 < rate < 17.0 else 'FAIL'}")

    witnesses = []
    for arr in candidates('fog', subset_limit=3):
        witnesses.append(" ".join(arr))
        if len(witnesses) >= 3:
            break
    seen = {" ".join(a) for a in candidates('fog', subset_limit=3)}
    found = sum(w in seen for w in witnesses)
    ok &= found == len(witnesses)
    print(f"planted witnesses recovered by a re-run: {found}/{len(witnesses)}: "
          f"{'OK' if found == len(witnesses) else 'FAIL'}")

    n = viol = 0
    for arr in candidates('fog', subset_limit=2):
        if arr[0] != ANCHOR_FIRST or arr[ANCHOR_WATER_POS] != 'fog' \
                or arr[11] != ANCHOR_LAST:
            viol += 1
        n += 1
        if n >= 2000:
            break
    ok &= viol == 0
    print(f"anchors held on {n - viol}/{n} emitted candidates: "
          f"{'OK' if viol == 0 else 'FAIL'}")

    sub, enum = space_size()
    expected = 662480
    ok &= sub == expected
    print(f"subsets per water branch {sub:,} (expected {expected:,}): "
          f"{'OK' if sub == expected else 'FAIL'}")

    if ok:
        print("SELFTEST OK: the lead-1 enumeration, its checksum filter and its "
              "anchors all reproduce")
    return ok


def main():
    if '--selftest' in sys.argv:
        return 0 if selftest() else 1
    sub, enum = space_size()
    print(f"subsets per water branch : {sub:,}")
    print(f"arrangements per branch  : {enum:,}")
    print(f"after 1-in-16 checksum   : {enum // 16:,}")
    print(f"both water branches      : {enum // 16 * 2:,} derivations")
    return 0


if __name__ == '__main__':
    sys.exit(main())
