#!/usr/bin/env python3
"""
Compile keccak.cl on any OpenCL device and check it against the canonical vector.

A GPU is not required. A CPU OpenCL runtime (pocl) compiles and runs the same
kernel source, which is enough to prove the arithmetic before renting anything:
the canonical BIP-0039 mnemonic must come out as the address this folder
already certifies its oracle against.

    pip install pyopencl pocl-binary-distribution
    python3 tools/gpu/verify_keccak.py
"""
import numpy as np, pyopencl as cl, os, sys
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keccak.cl')).read()
src += """
__kernel void test_keccak(__global const uchar *in, __global uchar *out) {
  uchar buf[64], digest[32];
  for (int i=0;i<64;i++) buf[i]=in[i];
  keccak256_64(buf, digest);
  for (int i=0;i<32;i++) out[i]=digest[i];
}
"""
ctx = cl.create_some_context(interactive=False)
q = cl.CommandQueue(ctx)
prg = cl.Program(ctx, src).build()
mf = cl.mem_flags

# the canonical vector's uncompressed pubkey, prefix stripped
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
m = "abandon "*11+"about"
node = (Bip44.FromSeed(Bip39SeedGenerator(m).Generate(), Bip44Coins.ETHEREUM)
        .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0))
pub = node.PublicKey().RawUncompressed().ToBytes()[1:]
assert len(pub)==64

inb = cl.Buffer(ctx, mf.READ_ONLY|mf.COPY_HOST_PTR, hostbuf=np.frombuffer(pub,dtype=np.uint8))
outb = cl.Buffer(ctx, mf.WRITE_ONLY, 32)
prg.test_keccak(q, (1,), None, inb, outb)
res = np.empty(32, dtype=np.uint8)
cl.enqueue_copy(q, res, outb); q.finish()
digest = bytes(res)
addr = "0x"+digest[12:].hex()
print("OpenCL kernel compiled and ran on:", ctx.devices[0].name)
print("keccak digest :", digest.hex())
print("eth address   :", addr)
print("expected      : 0x9858effd232b4033e47d90003d41ec34ecaeda94")
ok = addr == "0x9858effd232b4033e47d90003d41ec34ecaeda94"
print("SELFTEST OK: keccak.cl reproduces the canonical vector" if ok else "FAIL")
sys.exit(0 if ok else 1)
