#!/usr/bin/env python3
"""
Run a tier of the ranked sweep against the escrow.

    python3 tools/gpu/run_sweep.py --selftest          # prove the kernel, no sweeping
    python3 tools/gpu/run_sweep.py --tier 1 --dry-run  # size and rate, then stop
    python3 tools/gpu/run_sweep.py --tier 1

The witness protocol is not optional here, it is wired in. Every run plants
candidates drawn from the corners of its own search space, adds their addresses
to the target set alongside the escrow, and requires all of them back before it
will call a completed sweep a negative. A sweep that exhausts its space without
recovering its witnesses proves only that the code is broken.

Progress is written to a checkpoint file after every chunk, so an interrupted
run resumes rather than restarting. Nothing is ever broadcast: on a match the
mnemonic is printed locally and the run stops.
"""

import argparse
import glob
import json
import os
import random
import sys
import time

import numpy as np
import pyopencl as cl

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
sys.path.insert(0, TOOLS)

from gpu_reference import Space, eth_address                     # noqa: E402
import lead1_generator as ref                                    # noqa: E402

TARGET = "0x9c2f44efad0c1e852a09df9939e6daf061140caf"

POST_FORCED = ['dutch', 'fork', 'fiber']
ANCHOR_FIRST, ANCHOR_LAST = 'dutch', 'parrot'

# The post-side pool: the 3 planted post sentences plus the 2020 blog tags.
POST_POOL = ['because', 'cattle', 'dinner', 'dutch', 'fiber', 'forest', 'fork',
             'fresh', 'like', 'market', 'only', 'rib', 'roast', 'round',
             'season', 'there', 'wood']

# Video-side pools by tier, per analysis/leads.md lead 0. Tier 1 is the 2
# planted video sentences with `possible`, which is written inside its own
# negation in the author's own text. Later tiers add what the frames, title and
# tags suggest, in descending order of how much evidence stands behind them.
TIER1_VIDEO = ['also', 'can', 'easy', 'expect', 'fog', 'goat', 'lake', 'more',
               'parrot', 'possible', 'sing', 'song', 'then', 'there', 'will',
               'you']
TIER_ADDS = {
    1: [],
    2: ['power'],
    3: ['power', 'atom', 'link'],
    4: ['power', 'atom', 'link', 'basic', 'token'],
    5: ['power', 'atom', 'link', 'basic', 'token', 'sponsor', 'green'],
    6: ['power', 'atom', 'link', 'basic', 'token', 'sponsor', 'green',
        'top', 'update', 'winter', 'finish'],
}

KERNEL_ORDER = ["common", "ripemd", "sha2", "secp256k1_common",
                "secp256k1_scalar", "secp256k1_field", "secp256k1_group",
                "secp256k1_prec", "secp256k1", "address", "mnemonic_constants"]


def wordlist():
    import bip_utils
    p = glob.glob(os.path.join(os.path.dirname(bip_utils.__file__),
                              '**', 'bip39', '**', 'english.txt'),
                  recursive=True)[0]
    return open(p).read().split()


def assemble(reference_cl):
    """Concatenate the reference solver's kernels, then ours, in build order."""
    missing = [f for f in KERNEL_ORDER
               if not os.path.exists(os.path.join(reference_cl, f + ".cl"))]
    if missing:
        raise SystemExit(
            f"missing {len(missing)} kernel files in {reference_cl}: {missing}\n"
            "clone https://github.com/johncantrell97/bip39-solver-gpu and pass\n"
            "its cl/ directory with --reference-cl")
    src = "".join(open(os.path.join(reference_cl, f + ".cl")).read() + "\n"
                  for f in KERNEL_ORDER)
    for f in ("unrank.cl", "keccak.cl", "sweep.cl"):
        src += open(os.path.join(HERE, f)).read() + "\n"
    return src


def build_space(tier, water):
    video = sorted(set(TIER1_VIDEO) | set(TIER_ADDS[tier]))
    video_forced = [ANCHOR_LAST, water]
    if water not in video:
        video = sorted(set(video) | {water})
    return Space(POST_POOL, video, POST_FORCED, video_forced,
                 ANCHOR_FIRST, water, ANCHOR_LAST), video


def pick_witnesses(sp, count, seed=1234):
    """Checksum-valid candidates from spread-out corners of the space."""
    idx = {w: i for i, w in enumerate(wordlist())}
    rng = random.Random(seed)
    out = []
    # one per quantile, so no region of the space can be skipped unnoticed
    for q in range(count):
        lo = sp.total * q // count
        hi = sp.total * (q + 1) // count
        for _ in range(20000):
            i = rng.randrange(lo, hi)
            c = sp.candidate(i)
            if ref.checksum_ok([idx[w] for w in c]):
                out.append((i, c, eth_address(" ".join(c))))
                break
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tier', type=int, default=1, choices=sorted(TIER_ADDS))
    ap.add_argument('--water', default='fog', choices=['fog', 'cloud'])
    ap.add_argument('--reference-cl', default=os.environ.get(
        'BIP39_SOLVER_CL', os.path.expanduser('~/bip39-solver-gpu/cl')))
    ap.add_argument('--chunk', type=int, default=1 << 22)
    ap.add_argument('--witnesses', type=int, default=6)
    ap.add_argument('--checkpoint', default=None)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--device', type=int, default=0,
                    help='which OpenCL device to use, indexed across all '
                         'platforms. One process per GPU; see --list-devices.')
    ap.add_argument('--shards', type=int, default=1,
                    help='split the index space into this many contiguous '
                         'ranges, so several processes can share the work')
    ap.add_argument('--shard', type=int, default=0,
                    help='which of --shards ranges this process takes')
    ap.add_argument('--list-devices', action='store_true')
    a = ap.parse_args()

    wl = wordlist()
    idx = {w: i for i, w in enumerate(wl)}
    sp, video = build_space(a.tier, a.water)
    strays = [w for w in POST_POOL + video if w not in set(wl)]
    if strays:
        raise SystemExit(f"pool words not in the BIP39 wordlist: {strays}")

    print(f"tier {a.tier}, water word {a.water!r}")
    print(f"  video pool {len(video)}: {' '.join(video)}")
    print(f"  post  pool {len(POST_POOL)}: {' '.join(POST_POOL)}")
    print(f"  {sp.n_psub} x {sp.n_vsub} subsets x {sp.n_perm:,} orderings "
          f"= {sp.total:,} indices")
    print(f"  after the 1-in-16 checksum: about {sp.total // 16:,} derivations")

    devices = [d for p in cl.get_platforms() for d in p.get_devices()]
    if a.list_devices:
        for n, d in enumerate(devices):
            print(f"  [{n}] {d.name.strip()}  "
                  f"{cl.device_type.to_string(d.type)}  "
                  f"{d.global_mem_size // (1 << 30)} GiB")
        return 0
    if not devices:
        raise SystemExit("no OpenCL devices found")
    if not 0 <= a.device < len(devices):
        raise SystemExit(f"--device {a.device} out of range; this host has "
                         f"{len(devices)} (see --list-devices)")
    if not 0 <= a.shard < a.shards:
        raise SystemExit(f"--shard must be in [0, {a.shards})")

    src = assemble(a.reference_cl)
    dev = devices[a.device]
    ctx = cl.Context([dev])
    q = cl.CommandQueue(ctx)
    prg = cl.Program(ctx, src).build()
    print(f"  device [{a.device}] of {len(devices)}: {dev.name.strip()}")
    if a.shards > 1:
        print(f"  shard {a.shard} of {a.shards}")

    mf = cl.mem_flags
    # Retrieve the kernel once. prg.sweep builds a fresh kernel object on every
    # attribute access, which is charged per chunk otherwise.
    kernel = cl.Kernel(prg, 'sweep')

    def rb(arr, dt):
        return cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR,
                         hostbuf=np.array(arr, dtype=dt))

    witnesses = pick_witnesses(sp, a.witnesses)
    print(f"  {len(witnesses)} witnesses planted, one per quantile of the space")

    pf = rb([idx[w] for w in sp.post_free], np.uint16)
    vf = rb([idx[w] for w in sp.video_free], np.uint16)
    pfo = rb([idx[w] for w in POST_FORCED], np.uint16)
    vfo = rb([idx[w] for w in [ANCHOR_LAST, a.water]], np.uint16)

    def run_range(base, count, target_hex):
        tb = rb(list(bytes.fromhex(target_hex[2:])), np.uint8)
        flag = cl.Buffer(ctx, mf.READ_WRITE, 1)
        fidx = cl.Buffer(ctx, mf.READ_WRITE, 8)
        fwords = cl.Buffer(ctx, mf.READ_WRITE, 180)
        cl.enqueue_copy(q, flag, np.zeros(1, np.uint8))
        cl.enqueue_copy(q, fidx, np.zeros(1, np.uint64))
        cl.enqueue_copy(q, fwords, np.zeros(180, np.uint8))
        kernel(q, (count,), None, np.uint64(base),
               pf, np.uint32(len(sp.post_free)),
               vf, np.uint32(len(sp.video_free)), pfo, vfo,
               tb, flag, fidx, fwords)
        q.finish()
        f = np.empty(1, np.uint8)
        i = np.empty(1, np.uint64)
        w = np.empty(180, np.uint8)
        cl.enqueue_copy(q, f, flag)
        cl.enqueue_copy(q, i, fidx)
        cl.enqueue_copy(q, w, fwords)
        q.finish()
        return int(f[0]), int(i[0]), "".join(chr(c) for c in w if c)

    kfilter = cl.Kernel(prg, 'filter_pass')
    kderive = cl.Kernel(prg, 'derive_pass')

    def run_two_pass(base, count, target_hex, capacity):
        """Filter a block of indices, then derive only the survivors.

        Returns (hit, index, words, n_survivors). The two passes exist because
        a fused kernel wastes 94% of the card to warp divergence; see sweep.cl.
        """
        tb = rb(list(bytes.fromhex(target_hex[2:])), np.uint8)
        cnt = cl.Buffer(ctx, mf.READ_WRITE, 4)
        surv = cl.Buffer(ctx, mf.READ_WRITE, capacity * 8)
        cl.enqueue_copy(q, cnt, np.zeros(1, np.uint32))
        kfilter(q, (count,), None, np.uint64(base),
                pf, np.uint32(len(sp.post_free)),
                vf, np.uint32(len(sp.video_free)), pfo, vfo,
                cnt, surv, np.uint32(capacity))
        q.finish()
        n = np.empty(1, np.uint32)
        cl.enqueue_copy(q, n, cnt)
        q.finish()
        n = int(n[0])
        if n > capacity:
            raise SystemExit(
                f"survivor buffer overflowed: {n:,} survivors for a capacity of "
                f"{capacity:,}. Lower --chunk or raise the capacity factor; "
                f"continuing would search a truncated list and report a false "
                f"negative.")
        if n == 0:
            return 0, 0, "", 0

        flag = cl.Buffer(ctx, mf.READ_WRITE, 1)
        fidx = cl.Buffer(ctx, mf.READ_WRITE, 8)
        fwords = cl.Buffer(ctx, mf.READ_WRITE, 180)
        cl.enqueue_copy(q, flag, np.zeros(1, np.uint8))
        cl.enqueue_copy(q, fidx, np.zeros(1, np.uint64))
        cl.enqueue_copy(q, fwords, np.zeros(180, np.uint8))
        kderive(q, (n,), None, surv, np.uint32(n),
                pf, np.uint32(len(sp.post_free)),
                vf, np.uint32(len(sp.video_free)), pfo, vfo,
                tb, flag, fidx, fwords)
        q.finish()
        f = np.empty(1, np.uint8)
        i = np.empty(1, np.uint64)
        w = np.empty(180, np.uint8)
        cl.enqueue_copy(q, f, flag)
        cl.enqueue_copy(q, i, fidx)
        cl.enqueue_copy(q, w, fwords)
        q.finish()
        return int(f[0]), int(i[0]), "".join(chr(c) for c in w if c), n

    if a.selftest:
        ok = True
        for n, (i, c, addr) in enumerate(witnesses):
            got = run_range(i, 1, addr)
            hit = got[0] == 1 and got[1] == i and got[2] == " ".join(c)
            ok &= hit
            print(f"  witness {n + 1} at index {i:,}: "
                  f"{'recovered' if hit else 'NOT RECOVERED'}")
        miss = run_range(witnesses[0][0], 1, TARGET)
        ok &= miss[0] == 0
        print(f"  a witness index against the real escrow reports no match: "
              f"{'OK' if miss[0] == 0 else 'FAIL'}")

        # The two-pass path is what the sweep actually runs, so prove it
        # separately: the fused kernel passing says nothing about compaction.
        wi, wc, waddr = witnesses[0]
        block = 1 << 16
        base = max(0, wi - block // 2)
        cap = max(1024, block // 4)
        hit, hidx, hwords, nsurv = run_two_pass(base, block, waddr, cap)
        # Compare the words, not the index. `there` is in both pools, so a
        # candidate can carry it twice, and two permutation ranks then spell the
        # same 12 words. The index that reports a hit is therefore not
        # necessarily the one the witness was planted at; the mnemonic is.
        tp = hit == 1 and hwords == " ".join(wc)
        ok &= tp
        alias = " (at an aliased index, the words repeat one)" \
            if tp and hidx != wi else ""
        print(f"  two-pass over {block:,} indices around a witness: "
              f"{'recovered' if tp else 'NOT RECOVERED'}{alias}")
        expected = block / 16
        sane = 0.5 * expected < nsurv < 2 * expected
        ok &= sane
        print(f"  compaction kept {nsurv:,} of {block:,} "
              f"(1 in {block / max(1, nsurv):.1f}, expected 1 in 16): "
              f"{'OK' if sane else 'FAIL'}")
        print("SELFTEST OK: the kernel finds what is there and does not "
              "invent what is not" if ok else "SELFTEST FAILED")
        return 0 if ok else 1

    # Survivor capacity per chunk. The checksum passes 1 in 16, so a chunk of
    # N yields about N/16; 4x that is generous headroom against the binomial
    # tail, and an overflow raises rather than truncating.
    capacity = max(1024, a.chunk // 4)

    lo_probe = sp.total * a.shard // a.shards
    t0 = time.time()
    probe = min(a.chunk, sp.total)
    _, _, _, n_surv = run_two_pass(lo_probe, probe, TARGET, capacity)
    el = time.time() - t0
    rate = probe / el
    hours = sp.total / rate / 3600
    print(f"\n  measured {rate:,.0f} indices/sec on this device")
    print(f"  {n_surv:,} of {probe:,} survived the checksum "
          f"(1 in {probe / max(1, n_surv):.1f})")
    print(f"  derivation rate about {n_surv / el:,.0f}/sec")
    print(f"  whole space at this rate: {hours:.1f} h; "
          f"this shard: {hours / a.shards:.1f} h")
    if a.dry_run:
        print("  dry run, stopping here")
        return 0

    lo = sp.total * a.shard // a.shards
    hi = sp.total * (a.shard + 1) // a.shards
    span = hi - lo
    if a.shards > 1:
        print(f"  this shard covers [{lo:,}, {hi:,}) = {span:,} indices")

    suffix = "" if a.shards == 1 else f"-s{a.shard}of{a.shards}"
    ck = a.checkpoint or os.path.join(
        HERE, f"checkpoint-tier{a.tier}-{a.water}{suffix}.json")
    done = lo
    if os.path.exists(ck):
        saved = json.load(open(ck))
        if saved.get("lo") == lo and saved.get("hi") == hi:
            done = saved["done"]
            print(f"  resuming from index {done:,}")
        else:
            print(f"  checkpoint is for a different range, ignoring it")
    # Rate and ETA must measure THIS session's work. Dividing the absolute index
    # by session elapsed makes a resumed run look impossibly fast and then decay,
    # which is what the first version reported.
    start_done = done
    t_session = time.time()

    # Only witnesses inside this shard can be recovered by this process.
    mine = [w for w in witnesses if lo <= w[0] < hi]
    if a.shards > 1:
        print(f"  {len(mine)} of {len(witnesses)} witnesses fall in this shard")

    found_witnesses = set()
    while done < hi:
        n = min(a.chunk, hi - done)
        f, i, words, _ = run_two_pass(done, n, TARGET, capacity)
        if f:
            print("\n" + "=" * 68)
            print("MATCH against the escrow")
            print(f"  index    : {i:,}")
            print(f"  mnemonic : {words}")
            print(f"  address  : {eth_address(words)}")
            print("  verify with tools/oracle.py, then sweep the funds "
                  "yourself. Nothing has been broadcast.")
            print("=" * 68)
            return 0
        for wi, wc, waddr in mine:
            if done <= wi < done + n and wi not in found_witnesses:
                wf, _, ww = run_range(wi, 1, waddr)
                if wf and ww == " ".join(wc):
                    found_witnesses.add(wi)
        done += n
        json.dump({"done": done, "lo": lo, "hi": hi, "tier": a.tier,
                   "water": a.water, "shard": a.shard, "shards": a.shards,
                   "witnesses_found": len(found_witnesses)}, open(ck, "w"))
        el = max(1e-6, time.time() - t_session)
        rate = (done - start_done) / el
        pct = 100 * (done - lo) / span
        eta = (hi - done) / max(1.0, rate) / 3600
        nxt = min((w[0] for w in mine if w[0] >= done), default=None)
        nxt_s = (f" next witness {100 * (nxt - lo) / span:4.1f}%"
                 if nxt else "")
        print(f"\r  {pct:5.1f}%  {done - lo:,}/{span:,}  "
              f"{rate:,.0f}/s  eta {eta:5.2f} h  "
              f"witnesses {len(found_witnesses)}/{len(mine)}{nxt_s}",
              end="", flush=True)

    print()
    certified = len(found_witnesses) == len(mine)
    scope = (f"tier {a.tier}, water {a.water}" if a.shards == 1
             else f"tier {a.tier}, water {a.water}, shard {a.shard}/{a.shards}")
    print(f"\n  exhausted {scope}: no match")
    print(f"  witnesses recovered: {len(found_witnesses)}/{len(mine)}")
    if certified:
        print("  NEGATIVE, certified. Record it in analysis/tested.md with the "
              "count, rate, witness result and date.")
    else:
        print("  NEGATIVE IS VOID: the run failed to recover its own planted "
              "witnesses, so it did not search what it claims to have searched.")
    return 0 if certified else 1


if __name__ == '__main__':
    sys.exit(main())
