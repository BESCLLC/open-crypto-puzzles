#!/usr/bin/env python3
"""
The corrected sweep: CRLF CRLF separator, derivation index 0.

Two things the Real Big Block Discussion thread settles, both of which earlier
sweeps had wrong for this block:

  Separator.  Asked directly whether "two line breaks" means one Enter or two,
  she answers "the second one. Hit enter twice. This displays in Ascii as
  13 10 13 10". That is CR LF CR LF. Stage One and Block 2 measured LF LF, but
  those are different sources; the Real Big Block is the Wattpad chapter where
  she added the extra breaks, and she states its separator outright.

  Index.  Discussion point 4: the 7th private key has three 7s, "but the first
  one also has some amazing properties" -- she sent the funds to the first
  address. Index 0.

The exhaustive small marked-set sweep was previously run only with LF LF and LF.
This reruns it with CR LF CR LF primary, at index 0, and also tries the full
rule (every marked paragraph flipped) which "a couple of letters" does not
describe but the big block may still use.

    pip install coincurve
    pip install coincurve pycryptodome
    python3 tools/chapter_sweep.py            # full rule, k=1,2, then k=3
    python3 tools/chapter_sweep.py --k3-only
"""
import glob, hashlib, hmac, html, itertools, os, re, sys, time
import multiprocessing as mp

SRC = os.environ.get("AOI_SOURCES", os.path.expanduser("~/aoi-sources"))
LIVE = {
    "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "LIVE Real Big Block 0.777 BTC",
    "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC": "SUPERSEDED pre-rehash RBB",
    "13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd": "LIVE Block 76 0.077 BTC",
}
CURVE_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

import coincurve
try:
    from Crypto.Hash import RIPEMD160
    def ripemd160(b):
        return RIPEMD160.new(b).digest()
except ImportError:
    def ripemd160(b):
        return hashlib.new("ripemd160", b).digest()

import bip_utils
WORDS = open(glob.glob(os.path.join(os.path.dirname(bip_utils.__file__),
             "**", "bip39", "**", "english.txt"), recursive=True)[0]).read().split()


def mnemonic(ent):
    bits = int.from_bytes(ent, "big") << 4 | (hashlib.sha256(ent).digest()[0] >> 4)
    return " ".join(WORDS[(bits >> (11 * (11 - i))) & 0x7FF] for i in range(12))


def _ckd(k, c, i):
    if i >= 0x80000000:
        data = b"\x00" + k.to_bytes(32, "big") + i.to_bytes(4, "big")
    else:
        data = coincurve.PublicKey.from_valid_secret(
            k.to_bytes(32, "big")).format(True) + i.to_bytes(4, "big")
    I = hmac.new(c, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + k) % CURVE_N, I[32:]


def account_node(text):
    ent = hashlib.md5(text.encode("utf-8")).digest()
    seed = hashlib.pbkdf2_hmac("sha512", mnemonic(ent).encode(), b"mnemonic",
                               2048, 64)
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32], "big"), I[32:]
    for i in (44 + 0x80000000, 0x80000000, 0x80000000, 0):
        k, c = _ckd(k, c, i)
    return k, c


def addrs(text, n):
    k0, c0 = account_node(text)
    out = []
    for i in range(n):
        k, _ = _ckd(k0, c0, i)
        pub = coincurve.PublicKey.from_valid_secret(k.to_bytes(32, "big")).format(True)
        payload = b"\x00" + ripemd160(hashlib.sha256(pub).digest())
        full = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        v, s = int.from_bytes(full, "big"), ""
        while v:
            v, r = divmod(v, 58)
            s = B58[r] + s
        out.append("1" * (len(full) - len(full.lstrip(b"\x00"))) + s)
    return out


def selftest():
    from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44,
                           Bip44Coins, Bip44Changes)
    for t in range(8):
        raw = os.urandom(20).hex()
        ent = hashlib.md5(raw.encode()).digest()
        mn = Bip39MnemonicGenerator().FromEntropy(ent)
        want = (Bip44.FromSeed(Bip39SeedGenerator(mn).Generate(), Bip44Coins.BITCOIN)
                .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
                .AddressIndex(t % 5).PublicKey().ToAddress())
        if addrs(raw, 5)[t % 5] != want:
            print("deriver FAIL"); return False
    print("deriver agrees with bip_utils: OK")
    return True


TAG = re.compile(r"<[^>]+>")


def load(br="newline", nbsp="keep", title=True):
    paras, n = [], 1
    while os.path.exists(os.path.join(SRC, "storytext-p%d.html" % n)):
        page = open(os.path.join(SRC, "storytext-p%d.html" % n),
                    encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"<p[^>]*>(.*?)</p>", page, re.S | re.I):
            body = re.sub(r"<br\s*/?>", "\n" if br == "newline" else " ",
                          m.group(1), flags=re.I)
            p = html.unescape(TAG.sub("", body))
            if nbsp == "space":
                p = p.replace("\xa0", " ")
            paras.append(p)
        n += 1
    return paras if title else paras[1:]


def fl(p):
    return next((c.upper() for c in p if c.isalpha()), None)


def flip(p):
    L = [j for j, c in enumerate(p) if c.isalpha()]
    if not L:
        return p
    ch = list(p)
    ch[L[0]] = ch[L[0]].lower()
    ch[L[-1]] = ch[L[-1]].upper()
    return "".join(ch)


# CR LF CR LF primary, per her explicit statement; LF LF kept as a check.
SEPS = (("CRLFCRLF", "\r\n\r\n"), ("LFLF", "\n\n"))
G = {}


def _init(b):
    G.update(b)


def probe(text, tag, nidx):
    for i, a in enumerate(addrs(text, nidx)):
        if a in LIVE:
            return (LIVE[a], tag + " idx=%d" % i, hashlib.md5(text.encode()).hexdigest())
    return None


def job_small(args):
    bname, k = args
    ps = G[bname]
    n = len(ps)
    for combo in itertools.combinations(range(n), k):
        for modes in itertools.product(("flip", "first", "last"), repeat=max(k, 1)) if k else ((),):
            out = list(ps)
            for j, i in enumerate(combo):
                p = ps[i]; L = [x for x, c in enumerate(p) if c.isalpha()]
                if L:
                    ch = list(p); m = modes[j]
                    if m in ("flip", "first"): ch[L[0]] = ch[L[0]].lower()
                    if m in ("flip", "last"):  ch[L[-1]] = ch[L[-1]].upper()
                    out[i] = "".join(ch)
            for sepn, sep in SEPS:
                for trail in ("", "\n", "\r\n"):
                    h = probe(sep.join(out) + trail,
                              "k=%d %s %s | %s | %s trail%r"
                              % (k, list(combo), list(modes), bname, sepn, trail),
                              5)
                    if h:
                        return h
    return None


def job_full(bname):
    """Every marked paragraph flipped, under each selector, CRLFCRLF and LFLF."""
    ps = G[bname]
    for name, keep in (("ITASM", set("ITASM")),
                       ("SATOSHINAKAMOTO", set("SATOSHINAKAMOTO")),
                       ("SATOSHI", set("SATOSHI"))):
        out = [flip(p) if fl(p) and fl(p) not in keep else p for p in ps]
        for sepn, sep in SEPS:
            for trail in ("", "\n", "\r\n"):
                h = probe(sep.join(out) + trail,
                          "FULL %s | %s | %s trail%r" % (name, bname, sepn, trail), 5)
                if h:
                    return h
    return None


def job_k3(args):
    bname, first = args
    ps = G[bname]
    n = len(ps)
    fld = [flip(p) for p in ps]
    for b in range(first + 1, n):
        for c in range(b + 1, n):
            out = list(ps)
            out[first], out[b], out[c] = fld[first], fld[b], fld[c]
            text = "\r\n\r\n".join(out)
            for a in addrs(text, 1):
                if a in LIVE:
                    return (LIVE[a], "k=3 %s | %s | CRLFCRLF idx=0" % ([first, b, c], bname),
                            hashlib.md5(text.encode()).hexdigest())
    return None


def show(h):
    who, tag, md5 = h
    print("\n" + "=" * 72)
    print("*** MATCH  %s" % who)
    print("    %s" % tag)
    print("    md5 %s" % md5)
    print("=" * 72)
    return 0


def main():
    if not selftest():
        return 2
    bases = {"title": load(title=True),
             "no-title": load(title=False),
             "nbsp=space": load(nbsp="space", title=True),
             "br=space": load(br="space", title=True)}
    n = len(bases["title"])
    print("%d paragraphs; separator CR LF CR LF; index 0 (plus 0-4 margin for k<=2)" % n)
    nproc = os.cpu_count() or 4
    with mp.Pool(nproc, _init, (bases,)) as pool:
        if "--k3-only" not in sys.argv:
            print("\nfull rule (all marked), CRLFCRLF and LFLF", flush=True)
            for h in pool.imap_unordered(job_full, list(bases)):
                if h:
                    pool.terminate(); return show(h)
            print("  no match")

            jobs = [(b, k) for k in (0, 1, 2) for b in bases]
            t0 = time.time()
            print("\nk = 0,1,2 crossed: %d units" % len(jobs), flush=True)
            for j, h in enumerate(pool.imap_unordered(job_small, jobs), 1):
                if h:
                    pool.terminate(); return show(h)
                print("\r  %d/%d, %.0fs" % (j, len(jobs), time.time()-t0), end="", flush=True)
            print("\n  no match")

        jobs = [("title", f) for f in range(n)]
        total = n * (n - 1) * (n - 2) // 6
        t0 = time.time()
        print("\nk = 3, flip, CRLFCRLF, index 0: %d candidates" % total, flush=True)
        for j, h in enumerate(pool.imap_unordered(job_k3, jobs), 1):
            if h:
                pool.terminate(); return show(h)
            el = time.time() - t0
            print("\r  %d/%d units, %.0fs, ~%.0f min left"
                  % (j, len(jobs), el, el/j*(len(jobs)-j)/60), end="", flush=True)
        print("\n  no match")
    return 1


if __name__ == "__main__":
    sys.exit(main())
