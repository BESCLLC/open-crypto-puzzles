#!/usr/bin/env python3
"""
search_missing_word.py -- exhaust one unknown BIP39 word against a passphrase list.

Motivation:
    A 12-word mnemonic with exactly one unknown slot is a bounded search: 2048 candidates
    for the gap, of which only those whose BIP39 checksum closes are derivable (~1 in 16,
    so ~128). Crossed with a passphrase candidate list this is minutes of compute, not the
    unbounded guess the three insight locks are. This tool exists so that any future
    partial reconstruction of the seed can be exhausted mechanically before anyone spends
    time on it by hand.

Usage:
    # template: 12 space-separated slots, exactly one of them "?"
    python3 tools/search_missing_word.py "word1 word2 ... ? ... word12" passphrases.txt
    python3 tools/search_missing_word.py "<template>" --empty-passphrase

    Passphrase file: one candidate per line, blank line = empty passphrase.

Output:
    "MATCH <mnemonic> :: <detail>" per hit, then a summary line. Exit 0 on a hit, 1 if none.

Dependencies:
    stdlib; `ecdsa` optional (speed only); `mnemonic` for the English wordlist, with a
    fallback to the wordlist bundled next to this file if the package is absent.
"""

from __future__ import annotations

import hashlib
import itertools
import os
import sys
import time
from multiprocessing import Pool, cpu_count

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle_pure as O  # noqa: E402


def load_wordlist() -> list[str]:
    try:
        from mnemonic import Mnemonic
        return list(Mnemonic("english").wordlist)
    except ImportError:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "english.txt")
        with open(path) as fh:
            return [w.strip() for w in fh if w.strip()]


def checksum_ok(words: list[str], wl: list[str]) -> bool:
    """A 12-word BIP39 mnemonic is 128 entropy bits + a 4-bit SHA-256 checksum."""
    bits = "".join(format(wl.index(w), "011b") for w in words)
    entropy, chk = bits[:128], bits[128:]
    digest = hashlib.sha256(int(entropy, 2).to_bytes(16, "big")).digest()
    return format(digest[0], "08b")[:4] == chk


_TEMPLATE: list[str] = []


def _job(pair):
    word, passphrase = pair
    slots = list(_TEMPLATE)
    slots[slots.index("?")] = word
    mnemonic = " ".join(slots)
    matched, detail = O.check(mnemonic, passphrase)
    return (mnemonic, passphrase, detail) if matched else None


def _init(template):
    global _TEMPLATE
    _TEMPLATE = template


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 1

    template = argv[0].split()
    if len(template) != 12 or template.count("?") != 1:
        print("template must be 12 slots with exactly one '?'", file=sys.stderr)
        return 1

    if len(argv) > 1 and argv[1] != "--empty-passphrase":
        with open(argv[1]) as fh:
            passphrases = [line.rstrip("\n") for line in fh]
    else:
        passphrases = [""]

    wl = load_wordlist()
    known = [w for w in template if w != "?"]
    unknown = [w for w in known if w not in wl]
    if unknown:
        print(f"not BIP39 words: {unknown}", file=sys.stderr)
        return 1

    gap = template.index("?")
    candidates = []
    for word in wl:
        trial = list(template)
        trial[gap] = word
        if checksum_ok(trial, wl):
            candidates.append(word)
    print(f"{len(candidates)}/2048 candidates for slot {gap + 1} close the BIP39 checksum")

    work = list(itertools.product(candidates, passphrases))
    print(f"{len(work)} (word, passphrase) pairs to check")

    start = time.time()
    hits = []
    with Pool(cpu_count(), initializer=_init, initargs=(template,)) as pool:
        for i, result in enumerate(pool.imap_unordered(_job, work, chunksize=32)):
            if result:
                hits.append(result)
                print(f"MATCH {result[0]} :: passphrase={result[1]!r} :: {result[2]}", flush=True)
            if i and i % 10000 == 0:
                print(f"  {i}/{len(work)} {time.time() - start:.0f}s", file=sys.stderr, flush=True)

    print(f"done: {len(work)} pairs in {time.time() - start:.0f}s, {len(hits)} hit(s)")
    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
