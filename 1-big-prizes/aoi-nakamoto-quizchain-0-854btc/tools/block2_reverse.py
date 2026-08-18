#!/usr/bin/env python3
"""
Reverse Grycoin Block 2 to measure the author's transform exactly.

Block 2, posted 2019-08-02, is the worked example she wrote to demonstrate the
format used on block 77. Its escrow is spent, so it was solved, and every
constraint she stated is now known:

    separator   \r\n\r\n         "the ASCII codes 13 and 10, for 13 10 13 10
                                  meaning two line breaks, or \r\n \r\n"
    start       the first "I"
    stop        the period after "method"
    edges       "no spaces or line breaks before or after that included"
    MD5 prefix  3c6              "First three digits of MD5 hash are 3c6"
    rule        a flipped paragraph gets its first letter lowered and its last
                raised: "I" -> "i" and "himself" -> "himselF"
    format      [solution]       no TOMI field

The only unknown is which paragraphs are flipped, which is one bit per
paragraph. The MD5 prefix filters that space for free, before any key
derivation, so the whole reversal is milliseconds.

    python3 tools/block2_reverse.py question.txt

question.txt holds the Question section only, one paragraph per line, from the
first "I" through the period after "method".

Whatever this measures, the same conventions then apply to the Real Big Block
chapter, which is the point: they stop being guesses.
"""

import hashlib
import itertools
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle as O

BLOCK2_ADDRESS = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
MD5_PREFIX = "3c6"
SEP = "\r\n\r\n"


def flip_paragraph(p):
    """First letter lowered, last letter raised, as her example shows."""
    chars = list(p)
    first = next((i for i, c in enumerate(chars) if c.isalpha()), None)
    last = next((i for i in range(len(chars) - 1, -1, -1) if chars[i].isalpha()),
                None)
    if first is None or last is None:
        return p
    chars[first] = chars[first].lower()
    chars[last] = chars[last].upper()
    return "".join(chars)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    paras = [l.rstrip("\r\n") for l in open(sys.argv[1], encoding="utf-8")
             if l.strip()]
    n = len(paras)
    print(f"{n} paragraphs, {2**n:,} flip subsets")
    print(f"  first paragraph starts: {paras[0][:44]!r}")
    print(f"  last paragraph ends   : {paras[-1][-34:]!r}")

    prefix_hits, addr_hit = [], None
    for bits in range(2 ** n):
        chosen = [i for i in range(n) if bits >> i & 1]
        text = SEP.join(flip_paragraph(p) if i in chosen else p
                        for i, p in enumerate(paras))
        d = hashlib.md5(text.encode("utf-8")).hexdigest()
        if not d.startswith(MD5_PREFIX):
            continue
        prefix_hits.append((chosen, d))
        for idx, addr in enumerate(O.derive_addresses(bytes.fromhex(d), 6)):
            if addr == BLOCK2_ADDRESS:
                addr_hit = (chosen, d, idx, text)
                break
        if addr_hit:
            break

    print(f"\n  {len(prefix_hits)} subsets matched the 3c6 prefix "
          f"(expected about {2**n/4096:.1f} by chance)")
    for chosen, d in prefix_hits[:12]:
        print(f"    flip {chosen}  md5 {d}")

    if addr_hit:
        chosen, d, idx, text = addr_hit
        print("\n" + "=" * 70)
        print("SOLVED Block 2 -- the transform is now measured, not guessed")
        print(f"  flipped paragraphs : {chosen}")
        print(f"  md5                : {d}")
        print(f"  derivation index   : {idx}")
        print(f"  address            : {BLOCK2_ADDRESS}")
        print("=" * 70)
        print("\nApply the same conventions to the Real Big Block chapter:")
        print(f"  separator {SEP!r}, no edge whitespace, index {idx},")
        print(f"  {len(chosen)} of {n} paragraphs flipped by first-lower/last-upper.")
        with open("BLOCK2_SOLVED.txt", "w") as fh:
            fh.write(f"{chosen}\n{d}\nindex {idx}\n\n{text}")
        return 0

    print("\n  no subset reaches the escrow. Either a paragraph is transcribed")
    print("  wrongly, or the flip rule differs from the Stage One reading.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
