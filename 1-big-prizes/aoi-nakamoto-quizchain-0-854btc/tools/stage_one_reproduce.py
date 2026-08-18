#!/usr/bin/env python3
"""
Reproduce Block 77 Stage One from Hal Finney's post, then apply what that
measures to the Real Big Block chapter.

Stage One is solved: escrow 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN, swept
2019-08-03. Its source is Finney's "Bitcoin and me". So the rule, the separator
bytes and the derivation index are all recoverable by search against a known
answer, in the same block and the same format as the live 0.777 BTC lot.

Run it where ~/aoi-sources already holds what fetch pulled:

    python3 solve.py

Prints a short report. Nothing large needs to travel back.
"""
import hashlib, html, itertools, os, re, sys, time
import multiprocessing as mp

SRC = os.environ.get("AOI_SOURCES", os.path.expanduser("~/aoi-sources"))
STAGE_ONE = "19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN"
LIVE = {
    "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "LIVE Real Big Block 0.777 BTC",
    "13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd": "LIVE Block 76 0.077 BTC",
    "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC": "superseded pre-rehash RBB",
}
SEPS = {"LFLF": "\n\n", "LF": "\n", "CRLFCRLF": "\r\n\r\n", "CRLF": "\r\n",
        "LFLFLF": "\n\n\n"}

try:
    from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44,
                           Bip44Coins, Bip44Changes)
except ImportError:
    print("installing bip_utils...")
    os.system(sys.executable + " -m pip install --quiet bip_utils")
    from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44,
                           Bip44Coins, Bip44Changes)


def addresses(text, n=10):
    ent = hashlib.md5(text.encode("utf-8")).digest()
    mn = Bip39MnemonicGenerator().FromEntropy(ent)
    acct = (Bip44.FromSeed(Bip39SeedGenerator(mn).Generate(), Bip44Coins.BITCOIN)
            .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT))
    return [acct.AddressIndex(i).PublicKey().ToAddress() for i in range(n)]


TAG = re.compile(r"<[^>]+>")


def strip_tags(s):
    return html.unescape(TAG.sub("", s)).replace("\xa0", " ").strip()


def finney_paragraphs(path):
    """Bitcointalk renders one post as a div with <br /> pairs for paragraphs."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'<div class="post"[^>]*>(.*?)</div>', raw, re.S)
    body = m.group(1) if m else raw
    body = re.sub(r"<br\s*/?>", "\n", body, flags=re.I)
    body = re.sub(r"</?(div|blockquote|cite)[^>]*>", "\n", body, flags=re.I)
    text = strip_tags(body)
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def wattpad_paragraphs(path):
    """Wattpad's storytext wraps each paragraph in its own <p>."""
    raw = open(path, encoding="utf-8", errors="replace").read()
    ps = re.findall(r"<p[^>]*>(.*?)</p>", raw, re.S | re.I)
    if not ps:
        ps = re.split(r"<br\s*/?>", raw, flags=re.I)
    out = [strip_tags(p) for p in ps]
    return [p for p in out if p.strip()]


def first_letter(p):
    return next((c.upper() for c in p if c.isalpha()), None)


def last_letter(p):
    return next((c for c in reversed(p) if c.isalpha()), None)


def apply_rule(paras, marked, mode):
    out = []
    for i, p in enumerate(paras):
        L = [j for j, c in enumerate(p) if c.isalpha()]
        if i not in marked or not L:
            out.append(p); continue
        ch = list(p)
        if mode in ("flip", "first"):
            ch[L[0]] = ch[L[0]].lower()
        if mode in ("flip", "last"):
            ch[L[-1]] = ch[L[-1]].upper()
        out.append("".join(ch))
    return out


def census(paras, label):
    text = "\n\n".join(paras)
    # Escapes rather than literals: these are exactly the characters a
    # transcription loses, so the file that counts them must not carry them.
    special = {"curly-apos": "\u2019", "curly-open": "\u201c",
               "curly-close": "\u201d", "ellipsis": "\u2026",
               "en-dash": "\u2013", "em-dash": "\u2014",
               "nbsp": "\u00a0"}
    got = {k: text.count(v) for k, v in special.items()}
    print(f"\n{label}: {len(paras)} paragraphs, {len(text)} chars")
    print("  initials: " + "".join(first_letter(p) or "?" for p in paras))
    print("  finals  : " + "".join(last_letter(p) or "?" for p in paras))
    print("  special : " + (str({k: v for k, v in got.items() if v}) or "none"))
    for name, keep in (("SATOHI", set("SATOHI")), ("ITASM", set("ITASM"))):
        marked = [i for i, p in enumerate(paras) if first_letter(p) not in keep]
        sig = "".join(last_letter(paras[i]) or "?" for i in marked)
        print(f"  {name}: {len(marked)} marked, last letters {sig[:24]!r}")


def check(paras, targets, label, exhaustive=False):
    """Rule-based selections first; optionally every subset if that is small."""
    n = len(paras)
    sels = {}
    for name, keep in (("SATOHI", set("SATOHI")), ("ITASM", set("ITASM")),
                       ("SATOSHINAKAMOT", set("SATOSHINAKAMOT"))):
        sels[name] = frozenset(i for i, p in enumerate(paras)
                               if first_letter(p) not in keep)
    sels["none"] = frozenset()
    sels["all"] = frozenset(range(n))
    tried = 0
    for sname, marked in sels.items():
        for mode in ("flip", "first", "last"):
            base = apply_rule(paras, marked, mode)
            for sepn, sep in SEPS.items():
                for i, a in enumerate(addresses(sep.join(base), 20)):
                    tried += 1
                    if a in targets:
                        print(f"\n*** MATCH {targets[a]}")
                        print(f"    {label} | select {sname} | rule {mode} | "
                              f"sep {sepn} | index {i}")
                        return (sname, mode, sepn, i)
    print(f"  {label}: {tried} addresses from rule-based selections, no match")
    if exhaustive and n <= 20:
        print(f"  {label}: sweeping all 2^{n} subsets x {len(SEPS)} separators...")
        t0 = time.time()
        # Only the integer travels to the workers; re-pickling the paragraphs
        # 65,536 times costs more than the search does.
        with mp.Pool(os.cpu_count() or 4, _init, (paras, tuple(targets))) as pool:
            for k, hit in enumerate(
                    pool.imap_unordered(_subset, range(1 << n), 64), 1):
                if hit:
                    pool.terminate()
                    bits, sepn, i, addr = hit
                    print(f"\n*** MATCH {targets[addr]}")
                    print(f"    {label} | paragraphs "
                          f"{[j for j in range(n) if bits >> j & 1]} | "
                          f"sep {sepn} | index {i}")
                    return ("subset", bits, sepn, i)
                if k % 4096 == 0:
                    print(f"\r    {k:,}/{1<<n} subsets, {time.time()-t0:.0f}s",
                          end="", flush=True)
        print(f"\n  {label}: all 2^{n} subsets, no match")
    return None


_W = {}


def _init(paras, targets):
    _W["paras"] = paras
    _W["targets"] = targets


def _subset(bits):
    paras, targets = _W["paras"], _W["targets"]
    marked = frozenset(j for j in range(len(paras)) if bits >> j & 1)
    base = apply_rule(paras, marked, "flip")
    for sepn, sep in SEPS.items():
        for i, a in enumerate(addresses(sep.join(base), 10)):
            if a in targets:
                return (bits, sepn, i, a)
    return None


def main():
    fin = os.path.join(SRC, "finney-155054.html")
    wat = os.path.join(SRC, "wattpad-720888559.html")

    measured = None
    if os.path.exists(fin):
        paras = finney_paragraphs(fin)
        census(paras, "Finney post (Block 77 Stage One source)")
        measured = check(paras, {STAGE_ONE: "BLOCK 77 STAGE ONE"},
                         "stage one", exhaustive=True)
    else:
        print("missing", fin)

    if os.path.exists(wat):
        paras = wattpad_paragraphs(wat)
        census(paras, "Wattpad chapter (Real Big Block source)")
        check(paras, LIVE, "chapter")
        if measured:
            print("\nmeasured conventions from stage one:", measured)
    else:
        print("missing", wat)

    print("\nmeta:")
    j = os.path.join(SRC, "wattpad-720888559.json")
    if os.path.exists(j):
        print(" ", open(j, encoding="utf-8", errors="replace").read()[:400])


if __name__ == "__main__":
    main()
