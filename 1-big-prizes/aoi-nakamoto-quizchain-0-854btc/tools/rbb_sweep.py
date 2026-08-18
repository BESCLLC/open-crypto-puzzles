#!/usr/bin/env python3
"""
Real Big Block: sweep the chapter's own markup for the exact bytes the author
hashed in 2019.

Run it where the chapter HTML already is. Nothing is uploaded, and the chapter
text never enters this repository.

    curl -s "https://www.wattpad.com/apiv2/storytext?id=720888559" \
        | gunzip > chapter.html
    python3 tools/rbb_sweep.py chapter.html --count
    python3 tools/rbb_sweep.py chapter.html --jobs 32
    python3 tools/rbb_sweep.py chapter.html --tier 2 --blocks --jobs 32

Why the markup and not the rendered text. The author copied the chapter out of
her browser and hashed it. A text extraction is not the same bytes: the markup
holds 273 paragraph elements where an extraction yields about 90 lines, and each
inline br becomes a line break in a copy while staying inside one paragraph in
the source. A sweep over extracted text hashes the wrong shape before it has
chosen a separator, which is exactly what the 2026-08-18 run in
analysis/tested.md showed: it could not reach even the superseded address.

Targets. Both live escrows, plus 1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC, the
superseded address funded 2019-07-24 from the pre-rehash solution. It holds
nothing, but the author states the live version is the same text with one line
break changed to two, so reaching it pins the byte format and leaves the live
address one documented step away.

A witness drawn from the swept space itself must come back, or the run declares
its own negative void.
"""

import argparse
import hashlib
import html as htmllib
import multiprocessing as mp
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle as O

EXTRA_TARGET = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"

SEPARATORS = [
    (r"\n", "\n"), (r"\n\n", "\n\n"), (r"\r\n", "\r\n"),
    (r"\r\n\r\n", "\r\n\r\n"), (r"\r", "\r"), (r"\n\r\n", "\n\r\n"),
    ("space", " "), ("none", ""),
]
EDGES = [("none", ("", "")), ("trail-nl", ("", "\n")),
         ("trail-2nl", ("", "\n\n")), ("trail-crlf", ("", "\r\n")),
         ("lead-nl", ("\n", ""))]
BR = [(r"br=\n", "\n"), (r"br=\r\n", "\r\n"), ("br=space", " "), ("br=none", "")]

# Typographic characters a 2019 copy may carry, and their ASCII folds. Written
# as escapes so this file stays plain ASCII: a smart quote pasted into source is
# exactly the kind of silent byte difference this sweep exists to chase.
FOLDS = (
    ("\u2019", "'"), ("\u2018", "'"),      # right and left single quote
    ("\u201c", '"'), ("\u201d", '"'),      # left and right double quote
    ("\u2026", "..."),                      # ellipsis
    ("\u2013", "-"), ("\u2014", "--"),      # en dash, em dash
    ("\u00a0", " "),                        # non-breaking space
)


def ascii_fold(s):
    for a, b in FOLDS:
        s = s.replace(a, b)
    return s


QUOTES = [("as-stored", lambda s: s), ("ascii-fold", ascii_fold)]


def paragraphs(path, br_as, blocks=False):
    """Every block element's text, in document order, br rendered as br_as.

    With blocks=False only p elements are read. With blocks=True headings and
    divs are read too. That distinction matters: a browser selection takes what
    is on the page, so if the section headings live in h2 rather than p, a
    p-only reading drops them and every contiguous range is measured against the
    wrong sequence.
    """
    raw = open(path, "rb").read().decode("utf-8", "replace")
    tags = "p|h1|h2|h3|h4|h5|h6|div|li|blockquote" if blocks else "p"
    out = []
    for m in re.finditer(r"<(" + tags + r")\b[^>]*>(.*?)</\1>", raw, re.S | re.I):
        t = m.group(2)
        if re.search(r"<(" + tags + r")\b", t, re.I):
            continue                      # a wrapper; keep only the innermost
        t = re.sub(r"<br\s*/?>", "\x00", t, flags=re.I)
        t = re.sub(r"<[^>]+>", "", t)
        t = htmllib.unescape(t).replace("\x00", br_as)
        if t.strip() or not blocks:
            out.append(t)
    return out


def flip_rule(paras):
    """The Block 77 Stage One rule: a paragraph whose first letter is not in
    ITASM gets its first letter lowered and its last raised."""
    keep = O.STAGE_ONE_NO_FLIP_INITIALS
    res = []
    for p in paras:
        m = re.search(r"[A-Za-z]", p)
        res.append(O.flip_case(p) if m and m.group(0).upper() not in keep else p)
    return res


def axes(tier):
    if tier == 1:
        return SEPARATORS[:4], EDGES[:3], BR[:1], QUOTES[:1], [("plain", 0)]
    if tier == 2:
        return SEPARATORS, EDGES, BR[:2], QUOTES, [("plain", 0)]
    return SEPARATORS, EDGES, BR, QUOTES, [("plain", 0), ("flip", 1)]


def enumerate_texts(args):
    """Yield (label, text) for every candidate, in a stable order."""
    seps, edges, brs, quotes, flips = axes(args.tier)
    for bname, bval in brs:
        base = paragraphs(args.html, bval, args.blocks)
        variants = {"plain": base, "flip": flip_rule(base)}
        n = len(base)
        for fname, _ in flips:
            paras = variants[fname]
            for lo in range(n):
                for hi in range(lo + 1, n + 1):
                    chunk = paras[lo:hi]
                    for sname, sep in seps:
                        joined = sep.join(chunk)
                        for qname, qf in quotes:
                            q = qf(joined)
                            for ename, (pre, post) in edges:
                                yield (f"{lo}:{hi}|{bname}|{fname}|{sname}|"
                                       f"{qname}|{ename}", pre + q + post)


def count_space(args):
    seps, edges, brs, quotes, flips = axes(args.tier)
    n = len(paragraphs(args.html, "\n", args.blocks))
    return (n * (n + 1) // 2) * len(seps) * len(edges) * len(brs) \
        * len(quotes) * len(flips), n


_S = {}


def _init(args, targets):
    _S["args"], _S["targets"] = args, targets


def _work(bounds):
    lo, hi = bounds
    args, targets = _S["args"], _S["targets"]
    hits = []
    for i, (lbl, text) in enumerate(enumerate_texts(args)):
        if i < lo:
            continue
        if i >= hi:
            break
        ent = O.md5_entropy(text)
        for k, addr in enumerate(O.derive_addresses(ent, args.indices)):
            if addr in targets:
                hits.append((addr, k, lbl, ent.hex(), text))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--tier", type=int, default=1, choices=(1, 2, 3))
    ap.add_argument("--indices", type=int, default=6)
    ap.add_argument("--blocks", action="store_true",
                    help="read headings and divs too, not only p elements")
    ap.add_argument("--jobs", type=int, default=1,
                    help="worker processes; tiers 2 and 3 need this")
    ap.add_argument("--count", action="store_true")
    args = ap.parse_args()

    targets = dict(O.TARGETS)
    targets[EXTRA_TARGET] = "CALIBRATION superseded pre-rehash address"

    total, n = count_space(args)
    digest = hashlib.sha256(open(args.html, "rb").read()).hexdigest()
    print(f"parsed {n} block elements from {args.html}")
    print(f"  file sha256 {digest[:32]}")
    print(f"  tier {args.tier}, {n*(n+1)//2:,} contiguous ranges "
          f"-> {total:,} candidates")
    if args.count:
        return 0

    wlbl, wtxt = next(enumerate_texts(args))
    wit = O.derive_addresses(O.md5_entropy(wtxt), args.indices)[0]
    targets[wit] = f"WITNESS {wlbl}"
    print(f"  witness planted: {wlbl} -> {wit}")

    t0 = time.time()
    jobs = max(1, args.jobs)
    step = (total + jobs - 1) // jobs
    bounds = [(i * step, min(total, (i + 1) * step)) for i in range(jobs)]
    if jobs == 1:
        _init(args, targets)
        results = [_work(bounds[0])]
    else:
        with mp.Pool(jobs, initializer=_init, initargs=(args, targets)) as pool:
            results = pool.map(_work, bounds)
    el = max(time.time() - t0, 1e-9)

    hits = [h for r in results for h in r]
    got_witness = any(h[0] == wit for h in hits)
    real = [h for h in hits if h[0] != wit]

    print(f"\n  swept {total:,} in {el/60:.1f} min "
          f"({total/el:,.0f}/s across {jobs} job(s))")
    print(f"  witness recovered: {got_witness}")

    for addr, k, lbl, md5, text in real:
        print("\n" + "=" * 72)
        print(f"MATCH  {targets[addr]}")
        print(f"  address : {addr}  index {k}")
        print(f"  variant : {lbl}")
        print(f"  md5     : {md5}")
        print("=" * 72)
        with open("RBB_HIT.txt", "w") as fh:
            fh.write(f"{targets[addr]}\n{addr}\nindex {k}\n{lbl}\n{md5}\n\n{text}")
        print("written to RBB_HIT.txt. Verify with tools/oracle.py, then sweep "
              "the funds yourself. Nothing has been broadcast.")
        return 0

    if not got_witness:
        print("  NEGATIVE IS VOID: the run did not recover its own witness")
        return 1
    print("  NEGATIVE, certified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
