#!/usr/bin/env python3
"""
oracle_pure.py -- dependency-light re-implementation of tools/oracle.py.

Why this exists:
    tools/oracle.py needs bip_utils, which pulls in crcmod and fails to build wheels on a
    machine without Python development headers. This file reproduces the same check using
    only the standard library, with an optional `ecdsa` fast path for the curve arithmetic
    (pure-Python fallback is used automatically when ecdsa is absent, ~60x slower but
    identical in output).

What it certifies (strictly more than tools/oracle.py):
    1. xpub -> address leg: the published account xpub's m/0/0 in P2WPKH form equals the
       escrow. Same check tools/oracle.py makes.
    2. mnemonic -> seed leg: the BIP39 English test vector "abandon x11 about" with
       passphrase "TREZOR" reproduces the published reference seed (c55257c3...7463b04).
       tools/oracle.py documents this leg as uncertified for want of a known-good vector;
       the public BIP39 vector supplies one.
    3. Whole pipeline: the same mnemonic with an empty passphrase derives
       bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu at m/84'/0'/0'/0/0, the official BIP84
       test vector address. That is the exact derivation path this puzzle uses, so
       mnemonic-in to address-out now has a positive control end to end.
    4. Negative control: that same mnemonic does not match the puzzle escrow.

    A NO MATCH from this tool is therefore trustworthy as derivation math, end to end. It
    still says nothing about whether the candidate words are the right words.

Usage:
    python3 tools/oracle_pure.py --selftest
    python3 tools/oracle_pure.py "w1 ... w12" ["passphrase"]
    python3 tools/oracle_pure.py --stdin          # "mnemonic[:passphrase]" per line

Dependencies:
    stdlib; `ecdsa` optional (speed only).
"""
import hashlib, hmac, unicodedata

P  = 2**256 - 2**32 - 977
N  = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

def inv(a): return pow(a, P-2, P)
def add(p, q):
    if p is None: return q
    if q is None: return p
    (x1,y1),(x2,y2) = p,q
    if x1 == x2 and (y1+y2) % P == 0: return None
    if p == q: l = (3*x1*x1) * inv(2*y1) % P
    else:      l = (y2-y1) * inv(x2-x1) % P
    x3 = (l*l - x1 - x2) % P
    return (x3, (l*(x1-x3) - y1) % P)
def mul(k, p=(Gx,Gy)):
    r = None
    while k:
        if k & 1: r = add(r, p)
        p = add(p, p); k >>= 1
    return r

try:
    from ecdsa.ecdsa import generator_secp256k1 as _G
    from ecdsa.ellipticcurve import Point as _Pt, INFINITY as _INF
    _CURVE = _G.curve()
    def _to(p): return _INF if p is None else _Pt(_CURVE, p[0], p[1])
    def _fr(p): return None if p == _INF else (p.x(), p.y())
    def mul(k, p=(Gx, Gy)):
        return _fr((k * _G) if p == (Gx, Gy) else (k * _to(p)))
    def add(p, q):
        return _fr(_to(p) + _to(q))
except ImportError:
    pass

def ser_p(pt): return bytes([2 + (pt[1] & 1)]) + pt[0].to_bytes(32, 'big')
def parse_p(b):
    x = int.from_bytes(b[1:], 'big')
    y = pow((x*x*x + 7) % P, (P+1)//4, P)
    if (y & 1) != (b[0] & 1): y = P - y
    return (x, y)

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58d(s):
    n = 0
    for c in s: n = n*58 + B58.index(c)
    raw = n.to_bytes((n.bit_length()+7)//8, 'big')
    raw = b'\x00' * (len(s) - len(s.lstrip('1'))) + raw
    assert hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:], "b58 checksum"
    return raw[:-4]
def b58e(raw):
    raw += hashlib.sha256(hashlib.sha256(raw).digest()).digest()[:4]
    n = int.from_bytes(raw, 'big'); out = ''
    while n: n, r = divmod(n, 58); out = B58[r] + out
    return '1' * (len(raw) - len(raw.lstrip(b'\x00'))) + out

def h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()

CS = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def bech32(hrp, wit, prog):
    def pm(v):
        g = [0x3b6a57b2,0x26508e6d,0x1ea119fa,0x3d4233dd,0x2a1462b3]; c = 1
        for d in v:
            b = c >> 25; c = ((c & 0x1ffffff) << 5) ^ d
            for i in range(5):
                if (b >> i) & 1: c ^= g[i]
        return c
    def conv(data):
        acc = bits = 0; out = []
        for b in data:
            acc = (acc << 8) | b; bits += 8
            while bits >= 5: bits -= 5; out.append((acc >> bits) & 31)
        if bits: out.append((acc << (5-bits)) & 31)
        return out
    data = [wit] + conv(prog)
    exp = [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]
    chk = pm(exp + data + [0,0,0,0,0,0]) ^ 1
    return hrp + '1' + ''.join(CS[d] for d in data + [(chk >> 5*(5-i)) & 31 for i in range(6)])

class Node:
    def __init__(self, key, cc, priv, depth=0, fpr=b'\0'*4, idx=0):
        self.key, self.cc, self.priv, self.depth, self.fpr, self.idx = key, cc, priv, depth, fpr, idx
    @classmethod
    def from_seed(cls, seed):
        I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
        return cls(int.from_bytes(I[:32], 'big'), I[32:], True)
    @classmethod
    def from_xpub(cls, xpub):
        raw = b58d(xpub)
        return cls(raw[45:78], raw[13:45], False, raw[4], raw[5:9], int.from_bytes(raw[9:13], 'big'))
    def pub(self): return ser_p(mul(self.key)) if self.priv else self.key
    def ckd(self, i):
        if self.priv:
            data = (b'\x00' + self.key.to_bytes(32,'big') + i.to_bytes(4,'big')) if i >= 2**31 \
                   else (self.pub() + i.to_bytes(4,'big'))
            I = hmac.new(self.cc, data, hashlib.sha512).digest()
            return Node((int.from_bytes(I[:32],'big') + self.key) % N, I[32:], True,
                        self.depth+1, h160(self.pub())[:4], i)
        assert i < 2**31, "hardened from xpub"
        I = hmac.new(self.cc, self.key + i.to_bytes(4,'big'), hashlib.sha512).digest()
        pt = add(mul(int.from_bytes(I[:32],'big')), parse_p(self.key))
        return Node(ser_p(pt), I[32:], False, self.depth+1, h160(self.key)[:4], i)
    def path(self, p):
        n = self
        for part in p.split('/'):
            if part in ('m', ''): continue
            n = n.ckd(int(part.rstrip("'h")) + (2**31 if part[-1] in "'h" else 0))
        return n
    def xpub(self):
        raw = bytes.fromhex('0488b21e') + bytes([self.depth]) + self.fpr + \
              self.idx.to_bytes(4,'big') + self.cc + self.pub()
        return b58e(raw)
    def addr(self): return bech32('bc', 0, h160(self.pub()))
    def wif(self):
        return b58e(b'\x80' + self.key.to_bytes(32,'big') + b'\x01')

XPUB = ("xpub6CpNc58zqQvNGPHDGGTr68wgrmtfFDBWRuSDAxoDdrCE1iRAaZtyAD5T9uCJ3ELUYKCkx8Jkind2"
        "kwoR3Uxmg1ycQ6DWyGxZBMFvQqhNqVC")
ESCROW = "bc1q0akdjvrc2csau2n3gyxa3xcq0fss852x997m9y"
PATHS = ["m/84'/0'/0'", "m/49'/0'/0'", "m/44'/0'/0'", "m/0'", "m/0", "m", "m/84'/0'/0'/0"]

def seed_of(mnemonic, passphrase=""):
    m = unicodedata.normalize('NFKD', ' '.join(mnemonic.split()))
    s = unicodedata.normalize('NFKD', 'mnemonic' + passphrase)
    return hashlib.pbkdf2_hmac('sha512', m.encode(), s.encode(), 2048)

def check(mnemonic, passphrase=""):
    master = Node.from_seed(seed_of(mnemonic, passphrase))
    for p in PATHS:
        acct = master.path(p)
        if acct.xpub() == XPUB:
            leaf = acct.path("0/0")
            return True, f"account xpub == published xpub via {p}; addr={leaf.addr()} WIF={leaf.wif()}"
        leaf = acct.path("0/0")
        if leaf.addr() == ESCROW:
            return True, f"{p}/0/0 == escrow; WIF={leaf.wif()}"
    return False, "no path matches"

BIP39_VECTOR_SEED = (
    "c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e53495531f09a6987599d182"
    "64c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04"
)


BIP84_VECTOR_ADDR = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"


def run_selftest() -> int:
    ok = True

    addr = Node.from_xpub(XPUB).path("0/0").addr()
    hit = addr == ESCROW
    ok &= hit
    print(f"[selftest] published xpub, m/0/0, P2WPKH == escrow: {'yes' if hit else 'no'} ({addr})")

    ctrl = " ".join(["abandon"] * 11 + ["about"])
    hit = seed_of(ctrl, "TREZOR").hex() == BIP39_VECTOR_SEED
    ok &= hit
    print(f"[selftest] BIP39 English test vector seed (passphrase 'TREZOR') reproduces: "
          f"{'yes' if hit else 'no'}")

    bip84_addr = Node.from_seed(seed_of(ctrl, "")).path("m/84'/0'/0'/0/0").addr()
    hit = bip84_addr == BIP84_VECTOR_ADDR
    ok &= hit
    print(f"[selftest] official BIP84 vector, mnemonic to m/84'/0'/0'/0/0 address: "
          f"{'yes' if hit else 'no'} ({bip84_addr})")

    matched, detail = check(ctrl)
    ok &= not matched
    print(f"[selftest] known-wrong mnemonic rejected: {'yes' if not matched else 'NO'} ({detail})")

    if not ok:
        print("SELFTEST FAILED")
        return 1
    print("[selftest] scope: the full pipeline is certified end to end. BIP39 mnemonic-to-seed "
          "against the public BIP39 test vector; mnemonic to BIP84 m/84'/0'/0'/0/0 P2WPKH "
          "address against the official BIP84 test vector, which is the exact path this "
          "puzzle uses; and BIP32-to-P2WPKH against the published xpub-to-escrow identity.")
    print("SELFTEST OK")
    return 0


def main():
    import sys
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(run_selftest())
    if "--stdin" in argv:
        any_match = False
        for line in sys.stdin:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            mn, _, pp = line.partition(":")
            matched, detail = check(mn, pp)
            if matched:
                any_match = True
                print(f"MATCH '{mn}' :: {detail}", flush=True)
        sys.exit(0 if any_match else 1)
    if not argv:
        print(__doc__)
        sys.exit(1)
    matched, detail = check(argv[0], argv[1] if len(argv) > 1 else "")
    print(("MATCH " if matched else "NO MATCH (") + detail + ("" if matched else ")"))
    sys.exit(0 if matched else 1)


if __name__ == "__main__":
    main()
