# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row.
Every sweep below used a witness protocol: candidate lists known in advance to
belong to the swept set (one per corner of the search space, so no quarter of
the space could be silently skipped) were added to the target set before the
run, and their addresses had to be recovered for the negative to count.

## P1 -- full words from the 5 planted sentences (2026-08-15)

Set: full words from the 5 planted sentences only, 6-words-from-video /
6-words-from-post partition, anchors `dutch` at position 1, `parrot` at the
last position, position 5 in {`fog`, `cloud`}, both possible positions of
`fork`, free order otherwise.

2,413,152,000 candidate lists enumerated, 150,822,000 passing the BIP39
checksum (6.25%, matching the expected 1-in-16 rate), derived and compared on
a rented 43-core server. Witness: 4 planted candidates, one per corner of the
space (both `fog`/`cloud` branches crossed with both `fork` positions), all 4
recovered. Rate: 11,807 derivations/second sustained across 40 processes.
Cost: $0.56. Result: 0 match.

## G1 -- same words, `fork` not required as a literal match (2026-08-15)

Set: the P1 word pool without treating `fork` as a required literal word (a
paraphrase reading), 3,500 candidate subsets, 79,391,851 derivations, run on
one rented GPU. Witness: 4 planted candidates, one per corner, all 4
recovered. Rate: 654,436 derivations/second. Duration: 121 seconds. Result: 0
match. This closes the paraphrase reading of `fork` under these anchors: since
`fork` is spoken and spelled letter by letter in the source video, a literal
match is the better-supported reading regardless.

## R1 -- word pool extended with page and video metadata (2026-08-15)

Set: the 5-sentence word pool plus metadata words recovered from the blog
post's own tags (`season`, `market`, `fork`, `round`, from the archived 2020
HTML footer "Tagged... ethereum fork, round") and from the challenge video's
title and hook line ("top", "update", "winter", "finish"), 6/6 partition,
anchors as above, `fork` required, both `fog`/`cloud` branches. 158,670
candidate subsets, 3,384,362,972 derivations, one rented GPU. Witness: 6
planted candidates, all 6 recovered. Rate: 648,936 derivations/second.
Duration: 87 minutes. Result: 0 match.

## R2 minus R1 -- same pools, the 6/6 partition constraint dropped (2026-08-15)

Set: R1's word pools without the 6-words-per-source partition, restricted to
the candidate subsets not already covered by R1 (54,030 of R2's 193,800
total). 1,225,433,776 derivations. Witness: 6 planted candidates, all 6
recovered. Rate: 757,684 derivations/second. Duration: 27 minutes. Result: 0
match. Combined with R1, this makes the full R2 set (metadata-extended pool,
`fork` required, any split between the 2 sources) entirely negative.

## S1 -- blog contributes exactly A1 plus A2, wide video-side pool (2026-08-15)

Set: the post side fixed to exactly the 6 words of sentences A1 and A2 plus
`fiber` (the reading that the post alone supplies exactly 6 words), the video
side drawn from a pool of 56 candidate words (sentences, metadata, natural
inflections, and template text), `parrot` and `fork` anchored, both
`fog`/`cloud` branches. 51,039 candidate subsets, 1,157,541,475 derivations.
Witness: 6 planted candidates, all 6 recovered. Rate: 758,383
derivations/second. Duration: 25 minutes. Result: 0 match.

## R1b -- R1 extended with natural word inflections (2026-08-15)

Set: R1's word pool plus grammatical inflections of already-included words
(for example "hunt" and "health" alongside "hunter" and "healthy"), 6/6
partition, `fork` on the post side, same anchors. 490,776 candidate subsets,
10,752,000,393 derivations, one rented GPU (shared part of the time with
another job). Witness: 6 planted candidates, all 6 recovered. Rate: 668,827
derivations/second. Duration: 4 hours 28 minutes. Result: 0 match.

## Cumulative, metadata-extended era (G1 through R1b, plus P1)

16,749,552,467 candidate derivations across the 6 sweeps above, all negative,
every sweep individually witnessed. This covers: the 5 planted sentences'
words, confirmed metadata words from the blog post's tags and the video's
title and hook line, natural grammatical inflections of those words, both
partition and no-partition readings of the 6-and-6 split, and every free
ordering under the confirmed anchors. It does not cover connecting words
(prepositions, articles), substrings of longer words, or metadata beyond the
tags, title and hook line already identified.

## Earlier, smaller sweeps (pre-metadata, dates not individually re-timestamped
in the source record, all prior to 2026-08-15)

- Text reading order (in-source order, contiguous halves, on a strict then a
  widened word pool): 99,335 lists across 36 reading paths. Result: 0 match.
- Every interleaving of the 2 source word sets on the strict pool: 5.4 million
  candidates, only 3 possible reading paths tested. Result: 0 match.
- All 5 candidate word sets with every internal ordering allowed: tested,
  result 0 match, count not separately recorded.
- A posteriori likelihood-ordered search: started, interrupted before
  completion (not a negative, an abandoned run).
- Closing the 6-plus-6 budget by a likelihood-ratio rule, 4 candidate sets:
  91,865 lists, 0 match. This method's 2 strongest supporting words
  ("whisper", "impose") were later found to come from an unconfirmed prefix
  rule, not a validated one, so this negative's supporting logic is weaker
  than it looked at the time.
- A uniformity test of whether the hint words are unusually common in the
  BIP39 dictionary: statistical power 0.023, too low to support any
  conclusion.
- A test for planted list words hidden in the ordinary, non-absurd prose of
  the 2 texts: z = +0.52, p = 0.34, no signal detected.

## What none of this has tested

Every sweep above assumes the 12 elements come from the 2 published texts
(including their metadata). None of it tests the possibility that an element
is a substring of a longer written word (the author's own comment about
"possible" as a substring of its own negation, formed with the prefix "im-",
is acknowledged but not confirmed as a real mechanism; see README), or that a
word exists in material outside these
2 texts and their direct metadata.

## Metadata surfaces, read to exhaustion (2026-08-17)

Every surface either text names is now read, and the word pool is closed unless
the video's own frames yield something.

| surface | BIP39 entries it carries | in the pool |
|---|---|---|
| blog post body, full text | 89 | yes |
| blog post tags, 2020 archived capture | `season`, `market`, `fork`, `round` | yes |
| video title and description | 37 | yes |
| video tags, 10 of them | `top`; `season`, `hard`, `coin` as substrings | yes |
| blog post tags, current live page | `home`, `guide`, `profit`, `main`, `ability` | no, see below |

The live page's tags are excluded deliberately, not overlooked. They are
"Crypto, Bitcoin mining, Crypto mining, ASIC miners, Bitmain Antminers, Avalon
ASICs, Mining profitability, Mining guides, Mining ROI, home asic miner,
asicminervalue, mini bitcoin miner, hiveos", none of which appears on the 2020
archived capture. They arrived with a site redesign years after the wallet was
funded on 2020-02-12, so they cannot hold words that were fixed on that date.
Reading the live page also confirms independently what fact 5 in the README
states: the original tags are gone from it, which is why `fork` sat unfound.

What this leaves untested is the one surface the author names and no one has
looked at: text written on screen in the video itself, and the thumbnail. No
sweep can reach it, and if 2 of the 6 video words live there, every sweep
priced in `analysis/leads.md` is void.
