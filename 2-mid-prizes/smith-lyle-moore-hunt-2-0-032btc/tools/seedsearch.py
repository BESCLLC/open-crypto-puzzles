#!/usr/bin/env python3
"""
seedsearch.py -- bounded seed search for the Smith, Lyle & Moore "Glimmer" hunt.

Purpose:
    oracle.py verifies one candidate mnemonic. This script sweeps a small, explicitly
    bounded family of candidates around a partially known word list: it takes a set of
    known words in a fixed order, inserts one unknown BIP39 word at every position, keeps
    only the mnemonics whose BIP39 checksum is valid, and tests each survivor against a
    list of candidate passphrases.

    It is deliberately self-contained: BIP39, BIP32, BIP84 and bech32 are implemented here
    in pure Python with no third-party packages, so a negative from this script does not
    depend on an install that may differ from the one used to certify oracle.py. The only
    external input is the BIP39 English wordlist, read from the `mnemonic` package if it is
    installed or from a file given with --wordlist.

Usage:
    python3 tools/seedsearch.py --selftest
    python3 tools/seedsearch.py --words "when you depart find mystery hunt gather whale blood virtual moon" \
                                --passphrases tools/passphrases.txt

Self-test (must print SELFTEST OK before any result is trusted):
    1. The published account xpub's m/0/0 key, encoded as P2WPKH, equals the escrow address.
    2. The BIP39 test vector "abandon x11 about" produces the documented seed for the
       empty passphrase, which certifies the mnemonic-to-seed leg that oracle.py cannot
       certify from puzzle material alone.
    3. That same test-vector mnemonic reports NO MATCH against the escrow.

    Cross-checked once, outside the self-test, against bip_utils (the library oracle.py
    uses): 25 random 12-word mnemonics under 3 passphrases derive the same BIP84 address in
    both implementations.

Output:
    "MATCH mnemonic=<...> passphrase=<...> path=<...> address=<...>" on a hit, and a
    one-line summary of the space searched otherwise. Exit 0 on a match, 1 on none.
"""

import argparse
import hashlib
import hmac
import itertools
import sys
import time
import unicodedata

# --- puzzle constants, from the puzzle site and the escrow -------------------------------

ESCROW = "bc1q0akdjvrc2csau2n3gyxa3xcq0fss852x997m9y"
ACCOUNT_XPUB = ("xpub6CpNc58zqQvNGPHDGGTr68wgrmtfFDBWRuSDAxoDdrCE1iRAaZtyAD5T9uCJ3E"
                "LUYKCkx8Jkind2kwoR3Uxmg1ycQ6DWyGxZBMFvQqhNqVC")

# --- secp256k1 ---------------------------------------------------------------------------

P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8


def _add(p, q):
    if p is None:
        return q
    if q is None:
        return p
    if p[0] == q[0] and (p[1] + q[1]) % P == 0:
        return None
    if p == q:
        lam = 3 * p[0] * p[0] % P * pow(2 * p[1] % P, P - 2, P) % P
    else:
        lam = (q[1] - p[1]) % P * pow((q[0] - p[0]) % P, P - 2, P) % P
    x = (lam * lam - p[0] - q[0]) % P
    return (x, (lam * (p[0] - x) - p[1]) % P)


def _mul(k, p=(GX, GY)):
    r = None
    while k:
        if k & 1:
            r = _add(r, p)
        p = _add(p, p)
        k >>= 1
    return r


def ser_p(point):
    x, y = point
    return (b"\x03" if y & 1 else b"\x02") + x.to_bytes(32, "big")


# A windowed table of multiples of G, so that a scalar multiplication of the generator
# costs 31 mixed Jacobian additions and a single field inversion instead of 256 affine
# doublings, each of which would need its own inversion. This is the whole cost of the
# search: without it the sweep below runs at about 3 candidates a second.

_TABLE = []


def _build_table():
    base = (GX, GY)
    for _ in range(32):
        row = [None]
        acc = None
        for _ in range(255):
            acc = _add(acc, base)
            row.append(acc)
        _TABLE.append(row)
        for _ in range(8):
            base = _add(base, base)


def _mul_g(k):
    """k * G, via the window table."""
    if not _TABLE:
        _build_table()
    X = Y = Z = 0
    for i in range(32):
        d = (k >> (8 * i)) & 0xFF
        if not d:
            continue
        x2, y2 = _TABLE[i][d]
        if Z == 0:
            X, Y, Z = x2, y2, 1
            continue
        zz = Z * Z % P
        u2 = x2 * zz % P
        s2 = y2 * Z % P * zz % P
        h = (u2 - X) % P
        r = (s2 - Y) % P
        if h == 0:
            if r == 0:                     # point doubling, not reachable for distinct
                lam = 3 * X * X % P * pow(2 * Y % P, P - 2, P) % P
                nx = (lam * lam - 2 * X) % P
                X, Y, Z = nx, (lam * (X - nx) - Y) % P, Z
                continue
            X = Y = Z = 0                  # sum is the point at infinity
            continue
        hh = h * h % P
        hhh = h * hh % P
        v = X * hh % P
        nx = (r * r - hhh - 2 * v) % P
        X, Y, Z = nx, (r * (v - nx) - Y * hhh) % P, Z * h % P
    if Z == 0:
        return None
    zi = pow(Z, P - 2, P)
    zi2 = zi * zi % P
    return (X * zi2 % P, Y * zi2 % P * zi % P)


# --- base58check -------------------------------------------------------------------------

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58decode_check(s):
    n = 0
    for c in s:
        n = n * 58 + B58.index(c)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    raw = b"\x00" * (len(s) - len(s.lstrip("1"))) + raw
    body, chk = raw[:-4], raw[-4:]
    if hashlib.sha256(hashlib.sha256(body).digest()).digest()[:4] != chk:
        raise ValueError("bad base58 checksum")
    return body


# --- bech32 (BIP173) ---------------------------------------------------------------------

CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    gen = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1FFFFFF) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if ((top >> i) & 1) else 0
    return chk


def _hrp_expand(hrp):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _convertbits(data, frm, to, pad=True):
    acc = bits = 0
    ret = []
    maxv = (1 << to) - 1
    for b in data:
        acc = (acc << frm) | b
        bits += frm
        while bits >= to:
            bits -= to
            ret.append((acc >> bits) & maxv)
    if pad and bits:
        ret.append((acc << (to - bits)) & maxv)
    return ret


def p2wpkh(pubkey, hrp="bc"):
    h160 = hashlib.new("ripemd160", hashlib.sha256(pubkey).digest()).digest()
    data = [0] + _convertbits(h160, 8, 5)
    chk = _polymod(_hrp_expand(hrp) + data + [0] * 6) ^ 1
    return hrp + "1" + "".join(CHARSET[d] for d in data + [(chk >> 5 * (5 - i)) & 31 for i in range(6)])


# --- BIP32 -------------------------------------------------------------------------------

def master_from_seed(seed):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    return int.from_bytes(I[:32], "big"), I[32:]


def ckd_priv(k, c, index):
    if index >= 0x80000000:
        data = b"\x00" + k.to_bytes(32, "big") + index.to_bytes(4, "big")
    else:
        data = ser_p(_mul_g(k)) + index.to_bytes(4, "big")
    I = hmac.new(c, data, hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + k) % N, I[32:]


def ckd_pub(point, c, index):
    if index >= 0x80000000:
        raise ValueError("cannot derive a hardened child from a public key")
    I = hmac.new(c, ser_p(point) + index.to_bytes(4, "big"), hashlib.sha512).digest()
    return _add(_mul_g(int.from_bytes(I[:32], "big")), point), I[32:]


def derive_priv(seed, path):
    k, c = master_from_seed(seed)
    for index in path:
        k, c = ckd_priv(k, c, index)
    return k, c


# --- BIP39 -------------------------------------------------------------------------------

def load_wordlist(path=None):
    if path:
        with open(path, encoding="utf-8") as fh:
            words = [w.strip() for w in fh if w.strip()]
    else:
        try:
            from mnemonic import Mnemonic
        except ImportError:
            sys.exit("no wordlist: pip install mnemonic, or pass --wordlist <file>")
        words = list(Mnemonic("english").wordlist)
    if len(words) != 2048:
        sys.exit(f"wordlist has {len(words)} entries, expected 2048")
    return words


def checksum_ok(words, index_of):
    bits = "".join(format(index_of[w], "011b") for w in words)
    ent_len = len(bits) * 32 // 33
    ent = int(bits[:ent_len], 2).to_bytes(ent_len // 8, "big")
    want = format(hashlib.sha256(ent).digest()[0], "08b")[: len(bits) - ent_len]
    return bits[ent_len:] == want


def to_seed(mnemonic, passphrase=""):
    m = unicodedata.normalize("NFKD", mnemonic).encode("utf-8")
    s = unicodedata.normalize("NFKD", "mnemonic" + passphrase).encode("utf-8")
    return hashlib.pbkdf2_hmac("sha512", m, s, 2048, 64)


# --- the check ---------------------------------------------------------------------------

PATHS = {
    "bip84 m/84'/0'/0'/0/0": [84 + 0x80000000, 0x80000000, 0x80000000, 0, 0],
    "bip44 m/44'/0'/0'/0/0": [44 + 0x80000000, 0x80000000, 0x80000000, 0, 0],
}


def addresses_for(seed):
    for name, path in PATHS.items():
        k, _ = derive_priv(seed, path)
        yield name, p2wpkh(ser_p(_mul_g(k)))


def check(mnemonic, passphrase):
    seed = to_seed(mnemonic, passphrase)
    for name, addr in addresses_for(seed):
        if addr == ESCROW:
            return name, addr
    return None


# --- self-test ---------------------------------------------------------------------------

def selftest():
    body = b58decode_check(ACCOUNT_XPUB)
    chain, keydata = body[13:45], body[45:78]
    x = int.from_bytes(keydata[1:], "big")
    y = pow(pow(x, 3, P) + 7, (P + 1) // 4, P)
    if (y & 1) != (keydata[0] & 1):
        y = P - y
    point, c = (x, y), chain
    for index in (0, 0):
        point, c = ckd_pub(point, c, index)
    got = p2wpkh(ser_p(point))
    assert got == ESCROW, f"xpub m/0/0 gave {got}, expected {ESCROW}"

    vector = "abandon " * 11 + "about"
    want = ("c55257c360c07c72029aebc1b53c05ed0362ada38ead3e3e9efa3708e5349553"
            "1f09a6987599d18264c1e1c92f2cf141630c7a3c4ab7c81b2f001698e7463b04")
    assert to_seed(vector, "TREZOR").hex() == want, "BIP39 test vector seed mismatch"

    k, _ = derive_priv(to_seed(vector, ""), PATHS["bip84 m/84\'/0\'/0\'/0/0"])
    got = p2wpkh(ser_p(_mul_g(k)))
    want_addr = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"
    assert got == want_addr, f"BIP84 test vector gave {got}, expected {want_addr}"

    assert check(vector, "") is None, "known-wrong mnemonic must not match"
    print("SELFTEST OK")


# --- search ------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--words", help="known words, in order, with one slot unknown")
    ap.add_argument("--passphrases", help="file of candidate passphrases, one per line")
    ap.add_argument("--wordlist", help="BIP39 English wordlist file")
    ap.add_argument("--insert", type=int, default=None,
                    help="only try the unknown word at this 1-based position")
    ap.add_argument("--exact", action="store_true",
                    help="treat --words as a complete mnemonic, insert nothing")
    args = ap.parse_args()

    if args.selftest:
        selftest()
        return 0

    if not args.words:
        ap.error("--words is required unless --selftest")
    selftest()

    wordlist = load_wordlist(args.wordlist)
    index_of = {w: i for i, w in enumerate(wordlist)}
    known = args.words.split()
    unknown = [w for w in known if w not in index_of]
    if unknown:
        sys.exit(f"not BIP39 words: {', '.join(unknown)}")

    phrases = [""]
    if args.passphrases:
        with open(args.passphrases, encoding="utf-8") as fh:
            phrases = [ln.rstrip("\n") for ln in fh]

    if args.exact:
        candidates = [known] if checksum_ok(known, index_of) else []
        positions = [len(known)]
    else:
        positions = [args.insert - 1] if args.insert else range(len(known) + 1)
        candidates = []
        for pos in positions:
            for w in wordlist:
                trial = known[:pos] + [w] + known[pos:]
                if checksum_ok(trial, index_of):
                    candidates.append(trial)

    total = len(candidates) * len(phrases)
    print(f"checksum-valid mnemonics: {len(candidates)}  passphrases: {len(phrases)}  "
          f"derivations: {total}")
    start = time.time()
    for trial, passphrase in itertools.product(candidates, phrases):
        hit = check(" ".join(trial), passphrase)
        if hit:
            name, addr = hit
            print(f"MATCH mnemonic={' '.join(trial)} passphrase={passphrase!r} "
                  f"path={name} address={addr}")
            return 0
    rate = total / max(time.time() - start, 1e-9)
    print(f"NO MATCH over {total} derivations at {rate:.0f}/s")
    return 1


if __name__ == "__main__":
    sys.exit(main())
