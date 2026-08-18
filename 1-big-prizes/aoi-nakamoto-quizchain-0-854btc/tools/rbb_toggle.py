#!/usr/bin/env python3
"""
Real Big Block: keep the whole text, toggle the case of a few letters.

This is the transform the author described in the Grycoin Block 2 post, which
she wrote on 2019-08-02 specifically to demonstrate the format used on block 77:

    "copypaste everything in the Question from this Reddit post. Start with the
     first I and stop with the period after method, with no spaces or line
     breaks before or after that included in the hash."

    "I am saying copy paste and do not change anything with the line breaks,
     change only the capitalization of letters in solution."

    "people are supposed to keep the whole long text and change only a couple of
     letters in their capitalization. For example, if the letter n at the end of
     the last paragraph was part of the solution, you would be expected to
     change it to N and write capitalizatioN."

That rules out the two dimensions every earlier sweep spent itself on. The
paragraphs are not selected: the whole text is kept. The separator is not
chosen: the line breaks are left exactly as the copy produced them. What varies
is which letters have their case flipped, and there are only a couple of them.

    python3 tools/rbb_toggle.py chapter.txt --toggles 1
    python3 tools/rbb_toggle.py chapter.txt --toggles 2 --jobs 32
    python3 tools/rbb_toggle.py chapter.txt --list-bases

The base text still has to be right, so a small set of them is swept: where the
copy starts, and whether paragraphs are separated by one line break or two. The
author says the live escrow's text has two; the superseded one had one.
"""

import argparse
import hashlib
import itertools
import multiprocessing as mp
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle as O

EXTRA_TARGET = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"


def read_paragraphs(path):
    raw = open(path, "rb").read().decode("utf-8", "replace")
    if "<" in raw and ">" in raw:                      # looks like markup
        import html as htmllib
        out = []
        for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", raw, re.S | re.I):
            t = re.sub(r"<br\s*/?>", "\n", m.group(1), flags=re.I)
            t = re.sub(r"<[^>]+>", "", t)
            out.append(htmllib.unescape(t))
        return out
    return raw.rstrip("\n").split("\n")


def bases(paras):
    """Candidate base texts: where the copy starts, and the line-break style.

    The author's own instruction for the worked example was to start at a named
    character and stop at a named one, with no whitespace either side. The
    starts below are the plausible readings of that for this chapter, and the
    separators are the one and two line breaks she describes for the superseded
    and live escrows respectively.
    """
    starts = {}
    starts["full"] = 0
    for i, p in enumerate(paras):
        if re.match(r"\s*I\b", p):
            starts.setdefault("first-I", i)
        if re.match(r"\s*I thought", p):
            starts.setdefault("first-prose", i)
    seps = {r"\n": "\n", r"\n\n": "\n\n", r"\r\n": "\r\n", r"\r\n\r\n": "\r\n\r\n"}
    out = {}
    for sname, start in starts.items():
        for pname, sep in seps.items():
            text = sep.join(paras[start:]).strip("\r\n \t")
            out[f"{sname}|{pname}"] = text
    return out


_S = {}


def _init(text, targets, k, indices):
    _S.update(text=text, targets=targets, k=k, indices=indices,
              letters=[i for i, c in enumerate(text) if c.isalpha()])


def _flip(text, positions):
    b = list(text)
    for p in positions:
        c = b[p]
        b[p] = c.lower() if c.isupper() else c.upper()
    return "".join(b)


def _work(bounds):
    lo, hi = bounds
    text, targets = _S["text"], _S["targets"]
    letters, k, indices = _S["letters"], _S["k"], _S["indices"]
    hits = []
    for n, combo in enumerate(itertools.combinations(letters, k)):
        if n < lo:
            continue
        if n >= hi:
            break
        cand = _flip(text, combo)
        ent = O.md5_entropy(cand)
        for i, addr in enumerate(O.derive_addresses(ent, indices)):
            if addr in targets:
                hits.append((addr, i, combo, ent.hex(), cand))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter")
    ap.add_argument("--toggles", type=int, default=1)
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--indices", type=int, default=6)
    ap.add_argument("--base", default=None, help="sweep only this base text")
    ap.add_argument("--list-bases", action="store_true")
    a = ap.parse_args()

    paras = read_paragraphs(a.chapter)
    allbases = bases(paras)
    print(f"{len(paras)} paragraphs from {a.chapter}")
    if a.list_bases:
        for name, t in allbases.items():
            print(f"  {name:24} {len(t):>7,} chars  "
                  f"md5 {hashlib.md5(t.encode()).hexdigest()[:16]}  {t[:40]!r}")
        return 0

    targets = dict(O.TARGETS)
    targets[EXTRA_TARGET] = "CALIBRATION superseded pre-rehash"
    todo = {a.base: allbases[a.base]} if a.base else allbases

    from math import comb
    for name, text in todo.items():
        letters = [i for i, c in enumerate(text) if c.isalpha()]
        total = comb(len(letters), a.toggles)
        print(f"\nbase {name}: {len(text):,} chars, {len(letters):,} letters, "
              f"{a.toggles} toggle(s) -> {total:,} candidates")

        # witness: a real toggle of this base, planted with its own address
        wcombo = tuple(letters[:a.toggles])
        wit = O.derive_addresses(O.md5_entropy(_flip(text, wcombo)),
                                 a.indices)[0]
        tg = dict(targets)
        tg[wit] = f"WITNESS toggle{wcombo}"

        t0 = time.time()
        jobs = max(1, a.jobs)
        step = (total + jobs - 1) // jobs
        bounds = [(i * step, min(total, (i + 1) * step)) for i in range(jobs)]
        if jobs == 1:
            _init(text, tg, a.toggles, a.indices)
            res = [_work(bounds[0])]
        else:
            with mp.Pool(jobs, initializer=_init,
                         initargs=(text, tg, a.toggles, a.indices)) as pool:
                res = pool.map(_work, bounds)
        el = max(time.time() - t0, 1e-9)
        hits = [h for r in res for h in r]
        got_wit = any(h[0] == wit for h in hits)
        real = [h for h in hits if h[0] != wit]
        print(f"  swept {total:,} in {el/60:.1f} min ({total/el:,.0f}/s), "
              f"witness {'OK' if got_wit else 'MISSING'}")
        for addr, i, combo, md5, cand in real:
            print("\n" + "=" * 72)
            print(f"MATCH  {tg[addr]}")
            print(f"  address   : {addr}  index {i}")
            print(f"  base      : {name}")
            print(f"  toggled   : positions {combo}")
            print(f"  md5       : {md5}")
            print("=" * 72)
            with open("RBB_HIT.txt", "w") as fh:
                fh.write(f"{tg[addr]}\n{addr}\nindex {i}\nbase {name}\n"
                         f"toggled {combo}\n{md5}\n\n{cand}")
            print("written to RBB_HIT.txt. Verify with tools/oracle.py, then "
                  "sweep the funds yourself. Nothing has been broadcast.")
            return 0
        if not got_wit:
            print("  NEGATIVE IS VOID for this base: witness not recovered")
    print("\nno match on any base swept")
    return 0


if __name__ == "__main__":
    sys.exit(main())
