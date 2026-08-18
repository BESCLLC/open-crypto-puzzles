#!/usr/bin/env python3
"""
Reverse Grycoin Block 2 to measure the author's transform exactly.

Block 2, posted 2019-08-02, is the worked example she wrote to demonstrate the
format used on block 77. Its escrow `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi` is
spent, so it was solved, and everything she fixed is now known:

    start       the first "I"
    stop        the period after "method"
    edges       "no spaces or line breaks before or after that included"
    separator   "the ASCII codes 13 and 10, for 13 10 13 10 meaning two line
                 breaks, or \\r\\n \\r\\n as another way of saying the same thing"
    MD5 prefix  3c6              "First three digits of MD5 hash are 3c6"
    rule        a flipped paragraph gets its first letter lowered and its last
                raised: "I" -> "i" and "himself" -> "himselF"
    format      [solution]       no TOMI field

Solving it measures every convention her tool used -- the separator bytes, the
encoding, the derivation index, the exact shape of the case rule -- instead of
leaving them to be guessed on the Real Big Block, where there is no free filter
and no known answer to check against.

    python3 tools/block2_reverse.py question.txt

question.txt holds the Question section only, one paragraph per line, from the
first "I" through the period after "method". The post's own text is not shipped
here; `tools/fetch_sources.py` downloads it as the author typed it.

What is searched, and why each dimension is free:

  Lost paragraph breaks.  Her example changes "I" to "i" and "himself" to
  "himselF" in a single step, which is one rule over one paragraph only if that
  paragraph ends at "himself." A paste can merge two paragraphs but cannot
  invent one, so every sentence boundary inside every supplied paragraph is
  searched as a break that may have been lost in transcription. Pass a text
  fetched rather than transcribed and this dimension costs nothing extra: the
  true configuration is simply among those searched.

  Flip subsets.  Which paragraphs carry "the signs" is the puzzle itself.

  Case rule.  Force (first lowered, last raised) and toggle differ only where a
  paragraph already ends in a capital, which two of hers do.

  Quotes, apostrophes, ellipsis, separator, encoding.  What a copy out of a
  browser, and a hashing tool of unknown vintage, can each change.

The 3c6 prefix rejects 4,095 of every 4,096 candidates for the cost of one MD5,
so the whole grid costs seconds and only the survivors reach key derivation.
"""

import argparse
import hashlib
import multiprocessing as mp
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle as O

BLOCK2_ADDRESS = "1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi"
MD5_PREFIX = "3c6"

SEPS = {r"\r\n\r\n": "\r\n\r\n", r"\n\n": "\n\n", r"\r\n": "\r\n", r"\n": "\n"}
ENCODINGS = ["utf-8", "cp1252"]

# Escapes, not literals: these are the characters a transcription loses, so the
# file that hunts for them must not carry them itself.
CURLY_APOS, CURLY_OPEN, CURLY_CLOSE, ELLIPSIS = (
    "\u2019", "\u201c", "\u201d", "\u2026")

# A sentence ends at . ! or ? followed by a space and a capital or a quote.
# Abbreviations would break this; her prose has none.
SENTENCE_END = re.compile('(?<=[.!?])\\s+(?=["\u201c]?[A-Z])')


def curly_quotes(s):
    """Straight double quotes to a matched curly pair, as a browser copy has."""
    out, opening = [], True
    for c in s:
        if c == '"':
            out.append(CURLY_OPEN if opening else CURLY_CLOSE)
            opening = not opening
        else:
            out.append(c)
    return "".join(out)


TEXTOPS = {
    "straight":   lambda s: s,
    "cq":         curly_quotes,
    "ca":         lambda s: s.replace("'", CURLY_APOS),
    "cq+ca":      lambda s: curly_quotes(s).replace("'", CURLY_APOS),
    "ell":        lambda s: s.replace("...", ELLIPSIS),
    "cq+ell":     lambda s: curly_quotes(s).replace("...", ELLIPSIS),
    "cq+ca+ell":  lambda s: (curly_quotes(s).replace("'", CURLY_APOS)
                             .replace("...", ELLIPSIS)),
}


def force(p):
    """The rule her example demonstrates: first letter down, last letter up."""
    ch = list(p)
    letters = [i for i, c in enumerate(ch) if c.isalpha()]
    if not letters:
        return p
    ch[letters[0]] = ch[letters[0]].lower()
    ch[letters[-1]] = ch[letters[-1]].upper()
    return "".join(ch)


def toggle(p):
    """The same two positions, inverted rather than forced."""
    ch = list(p)
    letters = [i for i, c in enumerate(ch) if c.isalpha()]
    if not letters:
        return p
    for k in (letters[0], letters[-1]):
        ch[k] = ch[k].lower() if ch[k].isupper() else ch[k].upper()
    return "".join(ch)


FLIPS = {"force": force, "toggle": toggle}


def read_paragraphs(path):
    return [l.rstrip("\r\n") for l in open(path, encoding="utf-8") if l.strip()]


def split_config(sentences, mask):
    """Rebuild paragraphs, breaking at the boundaries `mask` selects."""
    out, at = [], 0
    for sents in sentences:
        cur = [sents[0]]
        for s in sents[1:]:
            if mask >> at & 1:
                out.append(" ".join(cur))
                cur = [s]
            else:
                cur.append(s)
            at += 1
        out.append(" ".join(cur))
    return out


def work(job):
    sentences, n_bounds, opname, sepname, enc = job
    op, sep = TEXTOPS[opname], SEPS[sepname]
    tried, hits = 0, []
    for mask in range(1 << n_bounds):
        paras = [op(p) for p in split_config(sentences, mask)]
        n = len(paras)
        for fname, fn in FLIPS.items():
            flipped = [fn(p) for p in paras]
            for bits in range(1 << n):
                text = sep.join(flipped[i] if bits >> i & 1 else paras[i]
                                for i in range(n))
                try:
                    raw = text.encode(enc)
                except UnicodeEncodeError:
                    break
                tried += 1
                digest = hashlib.md5(raw).hexdigest()
                if digest.startswith(MD5_PREFIX):
                    hits.append((opname, sepname, enc, mask, fname, bits, n,
                                 digest))
    return tried, hits


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("question", help="the Question section, one paragraph per line")
    ap.add_argument("--indices", type=int, default=10,
                    help="BIP44 address indices to check per survivor")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--no-splits", action="store_true",
                    help="trust the supplied paragraph breaks exactly")
    args = ap.parse_args()

    paras = read_paragraphs(args.question)
    sentences = [[p] if args.no_splits else SENTENCE_END.split(p) for p in paras]
    n_bounds = sum(len(s) - 1 for s in sentences)
    print(f"{len(paras)} paragraphs, {n_bounds} free sentence boundaries")
    print(f"  starts: {paras[0][:56]!r}")
    print(f"  ends  : {paras[-1][-40:]!r}")

    jobs = [(sentences, n_bounds, o, s, e)
            for o in TEXTOPS for s in SEPS for e in ENCODINGS]
    t0, tried, hits = time.time(), 0, []
    with mp.Pool(min(args.jobs, len(jobs))) as pool:
        for done, (t, h) in enumerate(pool.imap_unordered(work, jobs), 1):
            tried += t
            hits += h
            print(f"\r  {done}/{len(jobs)} units, {tried:,} texts, "
                  f"{len(hits)} past the {MD5_PREFIX} filter, "
                  f"{time.time()-t0:.0f}s", end="", flush=True)
    print(f"\n\n{tried:,} texts, {len(hits)} matched {MD5_PREFIX} "
          f"(chance expectation {tried/4096:.0f})")

    print(f"deriving {len(hits) * args.indices:,} addresses...", flush=True)
    for opname, sepname, enc, mask, fname, bits, n, digest in hits:
        for idx, addr in enumerate(
                O.derive_addresses(bytes.fromhex(digest), args.indices)):
            if addr != BLOCK2_ADDRESS:
                continue
            flipped = [i for i in range(n) if bits >> i & 1]
            print("\n" + "=" * 72)
            print("SOLVED BLOCK 2 -- the transform is measured, not guessed")
            print(f"  separator          : {sepname}")
            print(f"  encoding           : {enc}")
            print(f"  quotes             : {opname}")
            print(f"  case rule          : {fname}")
            print(f"  paragraphs         : {n} "
                  f"(split mask {mask:0{max(n_bounds,1)}b})")
            print(f"  flipped paragraphs : {flipped}")
            print(f"  md5                : {digest}")
            print(f"  derivation index   : {idx}")
            print("=" * 72)
            print("\nApply these same conventions to the Real Big Block chapter.")
            return 0

    print("\nNo candidate reaches the escrow.")
    print("The supplied text differs from what the author posted by something")
    print("none of these dimensions varies: a word, a comma, a capital letter.")
    print("Fetch the post rather than transcribing it: tools/fetch_sources.py")
    return 1


if __name__ == "__main__":
    sys.exit(main())
