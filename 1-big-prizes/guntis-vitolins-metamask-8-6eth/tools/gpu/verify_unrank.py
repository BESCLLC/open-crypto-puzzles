#!/usr/bin/env python3
"""
Check unrank.cl against tools/gpu_reference.py on any OpenCL device.

No GPU needed: a CPU runtime (pocl) compiles and runs the same source a card
would. Two things are compared, both of which fail silently on real hardware if
they are wrong.

  1. Index to candidate. Every index must produce the same 12 words the
     reference produces. A divergence means the sweep searches something other
     than what was priced, and its negative is worthless.
  2. The BIP39 checksum filter. It discards 15 of every 16 candidates before
     the expensive derivation, so a wrong one either throws away the answer or
     wastes the run.

    pip install pyopencl pocl-binary-distribution
    python3 tools/gpu/verify_unrank.py
"""

import glob
import os
import random
import sys

import numpy as np
import pyopencl as cl

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)

from gpu_reference import Space, TIER1_POST_POOL, TIER1_VIDEO_POOL  # noqa: E402
import lead1_generator as ref                                       # noqa: E402

POST_FORCED = ['dutch', 'fork', 'fiber']
VIDEO_FORCED = ['parrot', 'fog']          # last-position word first, then water


def wordlist():
    import bip_utils
    p = glob.glob(os.path.join(os.path.dirname(bip_utils.__file__),
                              '**', 'bip39', '**', 'english.txt'),
                  recursive=True)[0]
    return open(p).read().split()


def main():
    wl = wordlist()
    idx = {w: i for i, w in enumerate(wl)}
    post, video = TIER1_POST_POOL, TIER1_VIDEO_POOL
    sp = Space(post, video, POST_FORCED, VIDEO_FORCED, 'dutch', 'fog', 'parrot')

    post_free = [idx[w] for w in sp.post_free]
    video_free = [idx[w] for w in sp.video_free]
    assert post_free == sorted(post_free), "post_free must be ascending by index"
    assert video_free == sorted(video_free), "video_free must be ascending by index"

    src = open(os.path.join(HERE, 'unrank.cl')).read() + """
__kernel void k_cand(__global const ushort *pf, uint npf,
                     __global const ushort *vf, uint nvf,
                     __global const ushort *pforced,
                     __global const ushort *vforced,
                     __global const ulong *idxs, __global ushort *out) {
  uint g = get_global_id(0);
  ushort w[12];
  candidate_for_index(idxs[g], pf, npf, vf, nvf, pforced, vforced, w);
  for (int i = 0; i < 12; i++) out[g*12+i] = w[i];
}
__kernel void k_cs(__global const ushort *w12s, __global uchar *ok) {
  uint g = get_global_id(0);
  ushort w[12];
  for (int i = 0; i < 12; i++) w[i] = w12s[g*12+i];
  ok[g] = checksum_ok(w) ? 1 : 0;
}
"""
    ctx = cl.create_some_context(interactive=False)
    q = cl.CommandQueue(ctx)
    prg = cl.Program(ctx, src).build()
    mf = cl.mem_flags

    def rbuf(a, dt):
        return cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR,
                         hostbuf=np.array(a, dtype=dt))

    print(f"device: {ctx.devices[0].name}")
    print(f"space : {sp.n_psub} x {sp.n_vsub} x {sp.n_perm:,} = {sp.total:,}")

    rng = random.Random(5)
    edges = [0, 1, 2, sp.n_perm - 1, sp.n_perm, sp.total - 1]
    idxs = edges + rng.sample(range(sp.total), 4000 - len(edges))

    outb = cl.Buffer(ctx, mf.WRITE_ONLY, len(idxs) * 12 * 2)
    prg.k_cand(q, (len(idxs),), None,
               rbuf(post_free, np.uint16), np.uint32(len(post_free)),
               rbuf(video_free, np.uint16), np.uint32(len(video_free)),
               rbuf([idx[w] for w in POST_FORCED], np.uint16),
               rbuf([idx[w] for w in VIDEO_FORCED], np.uint16),
               rbuf(idxs, np.uint64), outb)
    got = np.empty(len(idxs) * 12, dtype=np.uint16)
    cl.enqueue_copy(q, got, outb)
    q.finish()

    bad = 0
    for n, i in enumerate(idxs):
        if [wl[x] for x in got[n*12:(n+1)*12]] != sp.candidate(i):
            bad += 1
    ok1 = bad == 0
    print(f"index to candidate, {len(idxs):,} indices including the boundaries: "
          f"{'OK' if ok1 else f'FAIL, {bad} mismatches'}")

    cands = [sp.candidate(i) for i in rng.sample(range(sp.total), 6000)]
    flat = np.array([idx[w] for c in cands for w in c], dtype=np.uint16)
    okb = cl.Buffer(ctx, mf.WRITE_ONLY, len(cands))
    prg.k_cs(q, (len(cands),), None,
             cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=flat), okb)
    kres = np.empty(len(cands), dtype=np.uint8)
    cl.enqueue_copy(q, kres, okb)
    q.finish()

    want = [ref.checksum_ok([idx[w] for w in c]) for c in cands]
    agree = sum(1 for a, b in zip(kres, want) if bool(a) == b)
    ok2 = agree == len(cands)
    rate = len(cands) / max(1, int(kres.sum()))
    print(f"checksum filter, {len(cands):,} candidates: "
          f"{'OK' if ok2 else f'FAIL, {len(cands)-agree} disagreements'}")
    print(f"  accept rate 1 in {rate:.2f}, expected 1 in 16")

    if ok1 and ok2:
        print("SELFTEST OK: unrank.cl matches the reference on both stages")
    return 0 if (ok1 and ok2) else 1


if __name__ == '__main__':
    sys.exit(main())
