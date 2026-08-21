#!/usr/bin/env python3
"""Exhaustive search for the Real Big Block's marked paragraph set.

Everything about this block except one thing is now measured rather than
guessed, and this tool encodes exactly that state.

MEASURED, from Block 77 Stage One reproduced end to end
-------------------------------------------------------
Stage One's escrow 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN is reached by taking Hal
Finney's "Bitcoin and me" (bitcointalk topic 155054), keeping the letters
I,T,A,S,M as paragraph initials, and on the four paragraphs that fails --
whose last letters spell STNM -- lowering the first letter and raising the
last; paragraphs joined with LF LF; BIP39 from the MD5; BIP44
m/44'/0'/0'/0/0. Its md5 is 9dd2efb9bc976c2095bd534d7b8d431c, whose first
three digits are the "9dd (copypasted)" the winning solver published in 2019.

So for the Real Big Block the operation, the separator and the index are all
fixed. The only unknown is WHICH paragraphs of the "Second" chapter are marked.

WHY THIS COULD NOT BE BRUTE FORCED BEFORE
-----------------------------------------
1. The carrier bytes were wrong. Wattpad's data-p-id attribute is the MD5 of
   each paragraph's text, and checking against it shows that a <br> inside a
   paragraph contributes NO character (not a line feed) and a run of two
   spaces is stored as NBSP + space. Eleven of the 273 paragraphs are wrong
   under the obvious extraction, and nothing else catches it: the
   paragraph-initial and paragraph-final letter streams still match, and so
   does the published character count. A perfect search over wrong bytes
   returns nothing and tells you nothing.
2. The rule was not pinned, so each candidate had to be tried across 4 case
   operations x 2 separators x 10 indices = 80 derivations. It is now 1.
3. This block has no published MD5 prefix -- she gave one for every other
   block but not this one -- so there is no free filter. Every candidate costs
   a full BIP39 + BIP44 derivation.

Together those made the search 80x more expensive than it needs to be, over a
text that was quietly wrong. This tool fixes all three.

    python3 rbb_search.py --html chapter.html --verify
    python3 rbb_search.py --html chapter.html --k 4 --jobs 8

--verify is not optional in spirit: run it first. It rebuilds the paragraphs
from the page source and checks all 273 against the data-p-ids published in
that same source. 272 must match; paragraph 77 is textually identical to
paragraph 33 and Wattpad gives duplicates distinct ids.

SIZES, and what they cost
-------------------------
    C(273,3) =            2,738,376
    C(273,4) =          231,917,400
    C(273,5) =       12,398,230,000
Stage One marked 4 paragraphs of 16, so small k is where she works. At the
~600 derivations/sec of pure Python on four cores, k=4 is about 100 hours; with
bip_utils installed it is several times faster, and on a GPU implementation of
PBKDF2-HMAC-SHA512 it is minutes. Install bip_utils before running anything
large: pip install bip_utils
"""
from __future__ import annotations
import argparse, hashlib, html as _html, itertools, json, os, pickle, re, sys, time
import multiprocessing as mp

LIVE      = "14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W"   # 0.777 BTC, unspent
SUPERSEDED= "1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC"   # the pre-rehash address
TARGETS   = {LIVE: "REAL BIG BLOCK (live, 0.777 BTC)", SUPERSEDED: "superseded address"}

# ---------------------------------------------------------------- derivation
try:
    from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44,
                           Bip44Changes, Bip44Coins)
    def address0(entropy: bytes) -> str:
        m = Bip39MnemonicGenerator().FromEntropy(entropy)
        seed = Bip39SeedGenerator(m).Generate()
        acct = (Bip44.FromSeed(seed, Bip44Coins.BITCOIN).Purpose().Coin()
                .Account(0).Change(Bip44Changes.CHAIN_EXT))
        return acct.AddressIndex(0).PublicKey().ToAddress()
    BACKEND = "bip_utils"
except ImportError:                                    # pure-python fallback
    import hmac
    P  = 2**256 - 2**32 - 977
    N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    def _add(p, q):
        if p is None: return q
        if q is None: return p
        if p[0] == q[0] and (p[1] + q[1]) % P == 0: return None
        if p == q: l = 3 * p[0] * p[0] * pow(2 * p[1], P - 2, P)
        else:      l = (q[1] - p[1]) * pow(q[0] - p[0], P - 2, P)
        x = (l * l - p[0] - q[0]) % P
        return (x, (l * (p[0] - x) - p[1]) % P)
    def _mul(k, p=(Gx, Gy)):
        r = None
        while k:
            if k & 1: r = _add(r, p)
            p = _add(p, p); k >>= 1
        return r
    def _ser(pt):
        return (b"\x02" if pt[1] % 2 == 0 else b"\x03") + pt[0].to_bytes(32, "big")
    _B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    def _b58c(payload: bytes) -> str:
        raw = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        n = int.from_bytes(raw, "big"); out = ""
        while n: n, r = divmod(n, 58); out = _B58[r] + out
        return "1" * (len(raw) - len(raw.lstrip(b"\0"))) + out
    _WL = None
    def _words():
        global _WL
        if _WL is None:
            import bip_utils  # noqa - only to locate a wordlist if present
        return _WL
    def _mnemonic(ent: bytes) -> str:
        # BIP39 English wordlist must be available; ship it next to this file
        wl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               "english.txt")).read().split()
        bits = "".join(f"{b:08b}" for b in ent)
        bits += f"{hashlib.sha256(ent).digest()[0]:08b}"[: len(ent) * 8 // 32]
        return " ".join(wl[int(bits[i:i+11], 2)] for i in range(0, len(bits), 11))
    def address0(entropy: bytes) -> str:
        seed = hashlib.pbkdf2_hmac("sha512", _mnemonic(entropy).encode(),
                                   b"mnemonic", 2048, 64)
        k = int.from_bytes(seed[:32], "big"); c = seed[32:]
        for idx in (0x8000002C, 0x80000000, 0x80000000, 0, 0):
            data = (b"\x00" + k.to_bytes(32, "big") if idx >= 0x80000000
                    else _ser(_mul(k))) + idx.to_bytes(4, "big")
            I = hmac.new(c, data, hashlib.sha512).digest()
            k = (int.from_bytes(I[:32], "big") + k) % N; c = I[32:]
        h = hashlib.new("ripemd160", hashlib.sha256(_ser(_mul(k))).digest()).digest()
        return _b58c(b"\x00" + h)
    BACKEND = "pure-python (slow; pip install bip_utils)"

# ------------------------------------------------------------------- carrier
def paragraphs_from_html(path: str) -> tuple[list[str], list[str]]:
    """Rebuild the canonical paragraph texts, and collect the published ids.

    Two conventions, both proven against the ids themselves:
      <br> contributes no character at all
      a run of two spaces is stored as NBSP + space
    """
    raw = open(path, encoding="utf-8").read()
    paras, pids = [], []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', raw, re.S):
        attrs, inner = m.group(1), m.group(2)
        pid = re.search(r'data-p-id="([0-9a-f]{32})"', attrs)
        pids.append(pid.group(1) if pid else "")
        t = re.sub(r"<br\s*/?>", "", inner)
        t = re.sub(r"<[^>]+>", "", t)
        t = _html.unescape(t)
        t = re.sub(r"  ", "  ", t)
        paras.append(t)
    return paras, pids

def verify(paras, pids) -> int:
    ok = 0
    for i, (p, pid) in enumerate(zip(paras, pids)):
        if not pid:
            print(f"  [{i:3}] no data-p-id in source"); continue
        if hashlib.md5(p.encode()).hexdigest() == pid:
            ok += 1
        else:
            dup = [j for j, q in enumerate(paras) if q == p and j != i]
            note = f"duplicate of paragraph {dup}" if dup else "TEXT MISMATCH"
            print(f"  [{i:3}] {note}")
    return ok

def force(p: str) -> str:
    """Her rule, measured on Stage One: first letter down, last letter up."""
    c = list(p); L = [i for i, x in enumerate(c) if x.isalpha()]
    if not L: return p
    c[L[0]] = c[L[0]].lower(); c[L[-1]] = c[L[-1]].upper()
    return "".join(c)

# -------------------------------------------------------------------- search
PARAS: list[str] = []
FORCED: list[str] = []

def _init(paras):
    global PARAS, FORCED
    PARAS = paras; FORCED = [force(p) for p in paras]

def _chunk(combos):
    hits = []
    for combo in combos:
        s = set(combo)
        text = "\n\n".join(FORCED[i] if i in s else PARAS[i] for i in range(len(PARAS)))
        a = address0(hashlib.md5(text.encode()).digest())
        if a in TARGETS: hits.append((combo, a))
    return len(combos), hits

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--html", required=True, help="the chapter's page source")
    ap.add_argument("--verify", action="store_true", help="check the carrier and stop")
    ap.add_argument("--k", type=int, default=4, help="number of marked paragraphs")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 4)
    ap.add_argument("--state", default="rbb_state.pkl", help="resume file")
    ap.add_argument("--batch", type=int, default=2000)
    a = ap.parse_args()

    paras, pids = paragraphs_from_html(a.html)
    print(f"{len(paras)} paragraphs, {sum(len(p) for p in paras):,} characters")
    ok = verify(paras, pids)
    print(f"verified {ok}/{len(paras)} against the published data-p-id hashes")
    if ok < len(paras) - 1:
        print("STOP: the carrier does not reproduce its own hashes. Fix the "
              "extraction before searching -- a search over wrong bytes cannot "
              "find anything and cannot tell you why.")
        return 1
    if a.verify: return 0

    from math import comb
    total = comb(len(paras), a.k)
    print(f"\nbackend: {BACKEND}")
    print(f"searching every {a.k}-paragraph marked set: {total:,} candidates")
    done = 0
    if os.path.exists(a.state):
        done = pickle.load(open(a.state, "rb"))
        print(f"resuming after {done:,}")

    gen = itertools.combinations(range(len(paras)), a.k)
    for _ in range(done): next(gen, None)
    t0 = time.time(); n = done
    with mp.Pool(a.jobs, initializer=_init, initargs=(paras,)) as pool:
        while True:
            batches = []
            for _ in range(a.jobs * 4):
                b = list(itertools.islice(gen, a.batch))
                if not b: break
                batches.append(b)
            if not batches: break
            for cnt, hits in pool.imap_unordered(_chunk, batches):
                n += cnt
                for combo, addr in hits:
                    print("\n" + "=" * 70)
                    print("*** SOLVED -- " + TARGETS[addr])
                    print(f"  marked paragraphs : {list(combo)}")
                    s = set(combo)
                    text = "\n\n".join(force(paras[i]) if i in s else paras[i]
                                       for i in range(len(paras)))
                    print(f"  md5               : {hashlib.md5(text.encode()).hexdigest()}")
                    open("SOLVED.txt", "w", encoding="utf-8").write(text)
                    print("  solution text written to SOLVED.txt")
                    print("  SWEEP THE FUNDS FIRST, ANNOUNCE AFTERWARDS.")
                    print("=" * 70)
                    return 0
            pickle.dump(n, open(a.state, "wb"))
            el = time.time() - t0
            rate = (n - done) / el if el else 0
            eta = (total - n) / rate / 3600 if rate else 0
            print(f"  {n:,}/{total:,}  {rate:,.0f}/s  eta {eta:.1f}h", flush=True)
    print(f"\nno {a.k}-paragraph marked set reaches either escrow")
    return 1

if __name__ == "__main__":
    sys.exit(main())
