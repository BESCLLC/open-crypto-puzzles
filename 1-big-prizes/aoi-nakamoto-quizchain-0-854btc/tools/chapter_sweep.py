#!/usr/bin/env python3
"""
Exhaustive small marked sets over the Real Big Block chapter.

Needs the chapter's own bytes, which this repository does not redistribute:
fetch them with `tools/fetch_sources.py` and set AOI_SOURCES to the directory,
or leave them in ~/aoi-sources. They are Wattpad's paginated storytext for part
720888559, one file per page.

The text is confirmed whole: the part metadata reports length 45451 and 12
pages, and the 273 paragraphs joined with a blank line come to 45450 characters
plus a trailing newline. So the serialization is not the problem and the marked
set is.

Every structured guess at that set has now failed -- the letter-set selectors,
the four FFWW groups whole, all 2^16 subsets of their paragraphs, the extra
candidates around them. What has never been done is the direct thing: take her
own description of the format, "change only a couple of letters in their
capitalization", at face value. Flipping one paragraph changes two letters. So
one, two or three flipped paragraphs is "a couple", and all of those together
are only 3.4 million candidates.

Derivation is the whole cost, so this ships its own: hashlib's C PBKDF2 and
libsecp256k1 through coincurve, checked against bip_utils on random entropies
before the sweep starts. About 540 candidates per second per core.

    pip install coincurve
    python3 tools/chapter_sweep.py              # k = 0,1,2 crossed, then k = 3
    python3 tools/chapter_sweep.py --k3-only    # straight to the long stage
"""
import glob, hashlib, hmac, html, itertools, os, re, sys, time
import multiprocessing as mp

SRC = os.environ.get("AOI_SOURCES", os.path.expanduser("~/aoi-sources"))
LIVE = {
    "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W": "LIVE Real Big Block 0.777 BTC",
    "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC": "superseded pre-rehash RBB",
    "13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd": "LIVE Block 76 0.077 BTC",
}
CURVE_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

import coincurve
import bip_utils
WORDS = open(glob.glob(os.path.join(os.path.dirname(bip_utils.__file__),
             "**", "bip39", "**", "english.txt"), recursive=True)[0]).read().split()
assert len(WORDS) == 2048


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


def address(text, index=0):
    ent = hashlib.md5(text.encode("utf-8")).digest()
    seed = hashlib.pbkdf2_hmac("sha512", mnemonic(ent).encode(), b"mnemonic",
                               2048, 64)
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32], "big"), I[32:]
    for i in (44 + 0x80000000, 0x80000000, 0x80000000, 0, index):
        k, c = _ckd(k, c, i)
    pub = coincurve.PublicKey.from_valid_secret(k.to_bytes(32, "big")).format(True)
    payload = b"\x00" + hashlib.new(
        "ripemd160", hashlib.sha256(pub).digest()).digest()
    full = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n, out = int.from_bytes(full, "big"), ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    return "1" * (len(full) - len(full.lstrip(b"\x00"))) + out


def selftest():
    from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44,
                           Bip44Coins, Bip44Changes)
    bad = 0
    for t in range(12):
        raw = os.urandom(24).hex()
        ent = hashlib.md5(raw.encode()).digest()
        mn = Bip39MnemonicGenerator().FromEntropy(ent)
        want = (Bip44.FromSeed(Bip39SeedGenerator(mn).Generate(),
                               Bip44Coins.BITCOIN)
                .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
                .AddressIndex(t % 4).PublicKey().ToAddress())
        if address(raw, t % 4) != want:
            bad += 1
    print("deriver agrees with bip_utils on 12 random texts: %s"
          % ("OK" if not bad else "FAIL"))
    return bad == 0


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


def variant(p, mode):
    L = [j for j, c in enumerate(p) if c.isalpha()]
    if not L:
        return p
    ch = list(p)
    if mode in ("flip", "first"):
        ch[L[0]] = ch[L[0]].lower()
    if mode in ("flip", "last"):
        ch[L[-1]] = ch[L[-1]].upper()
    return "".join(ch)


G = {}


def _init(paras_by_base):
    G.update(paras_by_base)


def probe(text, tag, indices):
    for i in indices:
        a = address(text, i)
        if a in LIVE:
            return (LIVE[a], tag, i, hashlib.md5(text.encode()).hexdigest())
    return None


def job_small(args):
    """k = 0, 1, 2 fully crossed: every base, mode, separator and index."""
    bname, k = args
    ps = G[bname]
    n = len(ps)
    for combo in itertools.combinations(range(n), k):
        for modes in itertools.product(("flip", "first", "last"), repeat=k):
            out = list(ps)
            for j, i in enumerate(combo):
                out[i] = variant(ps[i], modes[j])
            for sepn, sep in (("LFLF", "\n\n"), ("LF", "\n")):
                for trail in ("", "\n"):
                    h = probe(sep.join(out) + trail,
                              "k=%d %s %s | %s | %s | trail %r"
                              % (k, list(combo), list(modes), bname, sepn, trail),
                              range(5))
                    if h:
                        return h
    return None


def job_k3(args):
    """k = 3, flip only, the measured separator and index."""
    bname, first = args
    ps = G[bname]
    n = len(ps)
    flipped = [variant(p, "flip") for p in ps]
    for b in range(first + 1, n):
        for c in range(b + 1, n):
            out = list(ps)
            out[first] = flipped[first]
            out[b] = flipped[b]
            out[c] = flipped[c]
            text = "\n\n".join(out)
            if address(text, 0) in LIVE:
                a = address(text, 0)
                return (LIVE[a], "k=3 %s | %s | LFLF" % ([first, b, c], bname),
                        0, hashlib.md5(text.encode()).hexdigest())
    return None


def show(h):
    who, tag, i, md5 = h
    print("\n" + "=" * 72)
    print("*** MATCH  %s" % who)
    print("    %s" % tag)
    print("    derivation index %d, md5 %s" % (i, md5))
    print("=" * 72)
    return 0


def main():
    if not selftest():
        return 2
    bases = {
        "title": load(title=True),
        "no-title": load(title=False),
        "title nbsp=space": load(nbsp="space", title=True),
        "br=space title": load(br="space", title=True),
    }
    n = len(bases["title"])
    print("%d paragraphs" % n)
    nproc = os.cpu_count() or 4
    print("%d cores, about %d candidates/sec" % (nproc, 540 * nproc))

    with mp.Pool(nproc, _init, (bases,)) as pool:
        if "--k3-only" not in sys.argv:
            jobs = [(b, k) for k in (0, 1, 2) for b in bases]
            t0 = time.time()
            print("\nk = 0, 1, 2 fully crossed: %d units" % len(jobs), flush=True)
            for j, h in enumerate(pool.imap_unordered(job_small, jobs), 1):
                if h:
                    pool.terminate(); return show(h)
                print("\r  %d/%d, %.0fs" % (j, len(jobs), time.time() - t0),
                      end="", flush=True)
            print("\n  no match")

        jobs = [("title", f) for f in range(n)]
        total = n * (n - 1) * (n - 2) // 6
        t0 = time.time()
        print("\nk = 3, flip, LFLF, index 0: %d candidates in %d units"
              % (total, len(jobs)), flush=True)
        done = 0
        for j, h in enumerate(pool.imap_unordered(job_k3, jobs), 1):
            if h:
                pool.terminate(); return show(h)
            el = time.time() - t0
            print("\r  %d/%d units, %.0fs elapsed, ~%.0f min left"
                  % (j, len(jobs), el, (el / j * (len(jobs) - j)) / 60),
                  end="", flush=True)
        print("\n  no match")
    return 1


if __name__ == "__main__":
    sys.exit(main())
