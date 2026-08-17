# Tested: Bitaps Shamir secret-sharing challenge

Full negatives ledger. The README shows the summary table.

## 1. Wrong code base (rounds 1 and 2, superseded)

I first analyzed `pybtc`, a Python reimplementation of the same scheme, and found a
time-based coefficient bias in its `(a * i) % 255` construction, computing a residual of
119, 98, then 82 bits under 3 successive refinements. This turned out to be the wrong
target: `pybtc`'s Shamir index space is `x` in 1 to 5, and the real published share 2 has
index `x = 15`, which `pybtc` cannot produce. `pybtc` also only gained the embedded-index
feature it would need on 2020-07-11, three weeks after the challenge address was funded.
I dropped this line of analysis once the index mismatch was confirmed; it is kept in the
project history as a recorded wrong turn, not as a result.

## 2. Establishing the real code base

`bitaps-com/mnemonic-offline-tool`, commit `5b6dd995` (2020-06-19, the funding date),
bundles `jsbtc`, not `pybtc`. 3 checks confirm this: the trailing 4 bits of each share are
a data field (an index), not a checksum, since both published shares fail the BIP39
checksum in a way consistent with an embedded index rather than corruption; the observed
index values (3 and 15) fall inside `jsbtc`'s 4-bit index range (1 to 15) and outside
`pybtc`'s 3-bit range (1 to 5) as it existed on the funding date; and re-deriving from
both candidate implementations against the 2 published shares, only the `jsbtc` reading
produces internally consistent output. Method: source comparison plus the index-range
argument above. Witness: the public BIP84 test vector reproduces via `tools/oracle.py
--selftest`. Result: `jsbtc` established as the code of record. Date: 2026-08-03.

## 3. Residual entropy of the secret

See `data/entropy_measurements.csv` for the 3 measurements and their method. Summary: the
theoretical 128 bits narrows to 127.73 bits under the duplicate-value coefficient
rejection rule common to both `jsbtc` and `pybtc`, and to about 125 bits (124.90 to
125.19 across 3 independent measurements) once I added the effect of a real defect in the
deployed 2020 generator: its randomness self-check calls an undefined function
(`igam`, called from `igamc`), which throws and is silently caught, discarding a
disproportionate share of otherwise-valid random draws. None of this is small enough to
search; the point of measuring it is to state the true entropy accurately rather than by
assumption. Witness: the multiplication and interpolation tables underneath the
measurement were checked against an independent reference (65,536 GF(256) products, 0
discrepancies; 32,553 Lagrange evaluations, 0 discrepancies). Date: 2026-08-03.

## 4. Third-share search in the archives

14 archived captures of the challenge page and its regional mirrors (`bitaps.com`, plus
`ltc`, `tltc`, `tbtc`, `btc` subdomains), spanning 2020-07-04 to 2024-02-25 (Wayback CDX
and Common Crawl), all show the same 2 shares. Method: fetch every capture, extract any
12-word phrase, compare against the 2 known shares. Witness: the detector recovers both
known-good shares from every capture it reads, so an empty result is not a detector
failure. Result: 0 additional shares found across 14 captures. The interval between
2020-06-19 (funding) and 2020-07-04 (earliest capture), 15 days, is not covered by either
archive. Date: 2026-08-03.

## 5. Coefficient PRNG check

`bip39_mnemonic.js` in the bundled `jsbtc` uses `crypto.getRandomValues` or Node's
`randomBytes` for share coefficients, with no `Math.random` fallback path in the code I
read. Method: source review of the exact bundled file. Result: no exploitable seed bias
found in the coefficient generator itself (the bias found in section 1 was specific to
`pybtc`, the wrong code base). Date: 2026-08-03.

## 6. Degenerate coefficient case

The scheme's second coefficient can, with probability 1/255 per byte, be zero, which
would drop the polynomial's effective degree. This is not identifiable from only 2
shares; I enumerated the 16-byte space of this specific degenerate case and found no way
to test it without a 3rd share. Not pursued further as a standalone lead. Date:
2026-08-03.

## 7. Independent recomputation of the 127.73-bit figure, against the 2 published shares

Section 3 measures the duplicate-value rejection by enumerating the per-byte coefficient
space in the abstract. I have now redone that measurement the other way round, directly
against the 2 shares the author actually published, with an implementation written from
the deployed source rather than from my earlier notes, and the two agree exactly.

The rule, read off `__split_secret` in the bundled `jsbtc`: the coefficient list starts as
`q = [secret[b]]`, and each newly drawn byte is rejected while `q.includes(w)`. At
threshold 3 that forbids three equalities, `c1 = s`, `c2 = s` and `c1 = c2`, where `s` is
the secret byte. Because the 2 published shares sit at distinct nonzero indexes (3 and
15), every candidate `s` implies exactly one `(c1, c2)` pair by solving the 2 equations in
2 unknowns over GF(256). So the rule is directly testable per byte: solve for the pair,
discard `s` when the pair violates it.

Method: for each of the 16 byte positions, all 256 candidate values of `s`, each solved
and then re-substituted into both share equations before the rejection rule was applied.
Result: exactly 253 of 256 candidates survive at every one of the 16 positions, the 3
eliminated values being one per forbidden equality. Residual entropy
16 x log2(253) = 127.73 bits, narrowed by 0.27 bits from the uniform 128. This reproduces
section 3's first measurement to 2 decimal places by an independent route.

Witness: the same code re-derives both published shares from a synthetic secret and
recovers that secret from 3 shares, so the field arithmetic and the index decoding are
certified before the count is taken.

This also settles the outside claim recorded in `data/related_disclosures.csv`, that the
biased coefficient generation "enables practical statistical attacks using fewer shares
than the declared threshold". It does not. The bias is real and it is worth a quarter of
one bit across the entire secret. At the full 125-bit figure from section 3, a search is
not merely expensive, it is unreachable by any margin that further optimisation could
close. Nothing in the coefficient rejection rule is a way in.

Date: 2026-08-17.
