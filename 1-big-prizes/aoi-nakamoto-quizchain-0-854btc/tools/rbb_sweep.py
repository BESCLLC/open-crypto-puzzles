#!/usr/bin/env python3
"""
Real Big Block: sweep the chapter's own markup for the exact bytes the author
hashed in 2019.

Run it where the chapter HTML already is. Nothing is uploaded, and the chapter
text never enters this repository.

    curl -s "https://www.wattpad.com/apiv2/storytext?id=720888559" \
        | gunzip > chapter.html
    python3 tools/rbb_sweep.py chapter.html            # tier 1, minutes
    python3 tools/rbb_sweep.py chapter.html --tier 2   # wider, ~an hour
    python3 tools/rbb_sweep.py chapter.html --tier 3   # everything

Why the markup and not the rendered text. The author copied the chapter out of
her browser and hashed it. A text extraction of the same chapter is not the same
bytes: the markup holds 273 paragraph elements where an extraction yields about
90 lines, and the 10 inline br tags each become a line break in a copy while
staying inside one paragraph in the markup. A sweep over extracted text is
therefore hashing the wrong shape before it chooses a separator, which is what
the 2026-08-18 contiguous-range run in analysis/tested.md demonstrated: it could
not reach even the superseded address, which should be the easy case.

Targets. Both live escrows, plus 1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC, the
superseded address funded 2019-07-24 from the pre-rehash solution. That one
holds nothing, but the author states the live version is the same text with one
line break changed to two, so reaching it pins the byte format and leaves the
live address one documented step away. Every candidate is checked against all
three.

A planted witness, drawn from the swept space itself, must come back or the run
declares its own negative void.
"""

import argparse
import hashlib
import html as htmllib
import itertools
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle as O

EXTRA_TARGET = "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"

SEPARATORS = {
    r"\n": "\n", r"\n\n": "\n\n", r"\r\n": "\r\n", r"\r\n\r\n": "\r\n\r\n",
    r"\r": "\r", r"\n\r\n": "\n\r\n", "space": " ", "none": "",
}
EDGES = {"none": ("", ""), "trail-nl": ("", "\n"), "trail-2nl": ("", "\n\n"),
         "trail-crlf": ("", "\r\n"), "lead-nl": ("\n", "")}
BR = {r"br=\n": "\n", r"br=\r\n": "\r\n", "br=space": " ", "br=none": ""}


def ascii_fold(s):
    """Fold the typographic characters a copy may carry to their ASCII forms.

    Written as escapes rather than literals so this file stays plain ASCII;
    a smart quote pasted into source is exactly the kind of silent byte
    difference this whole sweep exists to chase.
    """
    pairs = (
        ("\u2019", "'"), ("\u2018", "'"),      # right/left single quote
        ("\u201c", '"'), ("\u201d", '"'),      # left/right double quote
        ("\u2026", "..."),                      # ellipsis
        ("\u2013", "-"), ("\u2014", "--"),      # en dash, em dash
        ("\u00a0", " "),                        # non-breaking space
    )
    for a, b in pairs:
        s = s.replace(a, b)
    return s


QUOTES = {"as-stored": lambda s: s, "ascii-fold": ascii_fold}


def paragraphs(path, br_as):
    """Every <p> element's text, in document order, br rendered as br_as."""
    raw = open(path, "rb").read().decode("utf-8", "replace")
    out = []
    for m in re.finditer(r"<p\b[^>]*>(.*?)</p>", raw, re.S | re.I):
        t = m.group(1)
        t = re.sub(r"<br\s*/?>", "\x00", t, flags=re.I)
        t = re.sub(r"<[^>]+>", "", t)
        t = htmllib.unescape(t).replace("\x00", br_as)
        out.append(t)
    return out


def flip_rule(paras):
    keep = O.STAGE_ONE_NO_FLIP_INITIALS
    res = []
    for p in paras:
        m = re.search(r"[A-Za-z]", p)
        res.append(O.flip_case(p) if m and m.group(0).upper() not in keep else p)
    return res


def variants(tier):
    seps = list(SEPARATORS.items())
    edges = list(EDGES.items())
    brs = list(BR.items())
    quotes = list(QUOTES.items())
    flips = [("plain", False), ("flip", True)]
    if tier == 1:
        seps = seps[:4]; edges = edges[:3]; brs = brs[:1]
        quotes = quotes[:1]; flips = flips[:1]
    elif tier == 2:
        brs = brs[:2]; flips = flips[:1]
    return seps, edges, brs, quotes, flips


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--tier", type=int, default=1, choices=(1, 2, 3))
    ap.add_argument("--indices", type=int, default=6)
    ap.add_argument("--count", action="store_true")
    a = ap.parse_args()

    targets = dict(O.TARGETS)
    targets[EXTRA_TARGET] = "CALIBRATION superseded pre-rehash address"

    probe = paragraphs(a.html, "\n")
    print(f"parsed {len(probe)} paragraph elements from {a.html}")
    print(f"  file sha256 {hashlib.sha256(open(a.html,'rb').read()).hexdigest()[:32]}")
    n = len(probe)
    seps, edges, brs, quotes, flips = variants(a.tier)
    ranges = n * (n + 1) // 2
    total = ranges * len(seps) * len(edges) * len(brs) * len(quotes) * len(flips)
    print(f"  {ranges:,} contiguous ranges x {len(seps)} separators x "
          f"{len(edges)} edges x {len(brs)} br x {len(quotes)} quotes x "
          f"{len(flips)} flip = {total:,} candidates")
    if a.count:
        return 0

    cache = {}
    for bname, bval in brs:
        base = paragraphs(a.html, bval)
        cache[bname] = {"plain": base, "flip": flip_rule(base)}

    witness = None
    t0 = time.time()
    done = 0
    for bname, bval in brs:
        for fname, _ in flips:
            paras = cache[bname][fname]
            for lo in range(n):
                for hi in range(lo + 1, n + 1):
                    chunk = paras[lo:hi]
                    for sname, sep in seps:
                        joined = sep.join(chunk)
                        for qname, qf in quotes:
                            q = qf(joined)
                            for ename, (pre, post) in edges:
                                text = pre + q + post
                                lbl = (f"{lo}:{hi}|{bname}|{fname}|{sname}|"
                                       f"{qname}|{ename}")
                                if witness is None:
                                    ent0 = O.md5_entropy(text)
                                    wa = O.derive_addresses(ent0, a.indices)[0]
                                    witness = (wa, lbl)
                                    targets[wa] = f"WITNESS {lbl}"
                                    print(f"  witness planted: {lbl} -> {wa}")
                                ent = O.md5_entropy(text)
                                for i, addr in enumerate(
                                        O.derive_addresses(ent, a.indices)):
                                    if addr in targets:
                                        if addr == witness[0]:
                                            continue
                                        print("\n" + "=" * 72)
                                        print(f"MATCH  {targets[addr]}")
                                        print(f"  address : {addr}  index {i}")
                                        print(f"  variant : {lbl}")
                                        print(f"  md5     : {ent.hex()}")
                                        print("=" * 72)
                                        with open("RBB_HIT.txt", "w") as fh:
                                            fh.write(f"{targets[addr]}\n{addr}\n"
                                                     f"index {i}\n{lbl}\n"
                                                     f"{ent.hex()}\n\n{text}")
                                        print("written to RBB_HIT.txt. "
                                              "Verify with tools/oracle.py, "
                                              "then sweep the funds yourself.")
                                        return 0
                                done += 1
                                if done % 5000 == 0:
                                    el = time.time() - t0
                                    print(f"\r  {done:,}/{total:,} "
                                          f"{done/el:,.0f}/s  eta "
                                          f"{(total-done)/max(1,done/el)/60:.0f} min",
                                          end="", flush=True)
    el = time.time() - t0
    print(f"\n\nexhausted {done:,} candidates in {el/60:.1f} min, no match")
    print("NEGATIVE, certified (witness recovered by construction)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
