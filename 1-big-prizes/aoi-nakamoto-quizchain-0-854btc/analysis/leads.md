# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. Reconstruct the 2019 browser-copy rendering of the Wattpad chapter

The author states she typed the chapter with a blank line between paragraphs
("two line breaks... one 13 and one 10 for each"), but the chapter's current
storage (fetched through Wattpad's API, `modifyDate` 2019-07-23, matching the
2019-07-30 funding of the current escrow) contains no blank paragraphs at all:
Wattpad's storage format normalizes them away. What she actually hashed was most
likely whatever her browser produced when she selected and copied the rendered
page in 2019, not the raw API storage read today. A first attempt at simulating
this (Chromium's `selection.toString` and `innerText` rendering rules) is
included in the "simulated browser copy" row of `analysis/tested.md`, but it
used only one rendering assumption; the actual 2019 Wattpad reader page layout
(paragraph spacing, non-breaking spaces around punctuation, title block) has not
been reconstructed and tested as its own base text.

What would confirm it: rendering `data/chapitre_second_page.html` the way a 2019
browser would have displayed it, extracting the resulting paragraph text, and
running it (with the certified case-flip rule applied to the same candidate
paragraph groups already tested) through `tools/oracle.py`.
What would kill it: a faithful reconstruction still not matching after the
already-tested paragraph-selection hypotheses are re-applied to it.
Cost: hours, mostly in getting the 2019 rendering right; the derivation itself is
seconds per candidate.

## 2. Read the 27 posts and comments between the rehash and the shutdown

The author rehashed and refunded the Real Big Block on 2019-07-30, then stopped
posting shortly after. The 27 posts and comments she made between 2019-07-30 and
2019-08-04 have been read once for an explicit "twist" statement, but not
re-read systematically against the current, narrower list of untested paragraph
combinations.

What would confirm it: a stated detail (an extra modification, a further
paragraph, a corrected count) that, applied to the certified rule and re-tested,
matches the address.
What would kill it: a full re-read producing no new candidate paragraph or rule
variant beyond what `analysis/tested.md` already covers.
Cost: an hour of reading.

## 3. Two-character edits on the strongest base texts

The single-character-edit sweep (266,038,400 candidates, `analysis/tested.md`)
covers every one-character difference from 40 base texts and is exhaustive for
that distance. It does not cover 2-character differences, which would catch a
base text that is off by, for example, one inserted invisible character AND one
capitalization slip. A 2-character sweep restricted to the small set of NBSP and
line-ending pairs (rather than all positions) is a bounded space, not a full
40-base x 2-character search.

What would confirm it: a match within the bounded 2-character space.
What would kill it: exhausting that bounded space with 0 match; the full,
unbounded 2-character space is not proposed here, since its cost is
disproportionate without a narrower reason to expect the answer lives there.
Cost: on the order of an hour on a rented GPU for the bounded version described
above; the private research folder priced this at roughly 45 minutes per base
text for a similarly scoped variant.

## 4. Identify what "76" indexes for Block 76

A method confirmed on 3 other blocks in the same series (56, 57, 58) uses the
block's own number as a position index into a specific corpus (a numbered post
by Satoshi Nakamoto or Hal Finney on bitcointalk, read in a specific order). The
same method, tried against every corpus and ordering available (Satoshi's and
Hal Finney's bitcointalk posts, Hal Finney's tweets), does not produce a post
containing "change" or "from" at position 76. The corpus this method should
index for block 76 has not been identified; candidates not yet tried include the
complete list of Hal Finney's tweets (only 58 were recovered through the
official API; a fuller archive may exist), Satoshi's SourceForge posts, the
Bitcoin whitepaper or v0.1 source code read as a sequence of numbered units, and
the author's own r/Grycoin posts read as their own numbered sequence.

What would confirm it: a position-76 item in the right corpus containing "change
to" or "from change to", tested through `tools/oracle.py --block76-filter` and
then a full derivation.
What would kill it: exhausting the remaining candidate corpora with no match at
position 76.
Cost: minutes per corpus once a candidate corpus is assembled.

## 5. A short, human-reasoned answer to "change to" / "from change to"

The author's own hint structure (a short, freeform-text question plus a short
TOMI expansion, confirmed on more than a dozen other blocks) argues for a short,
punchy answer rather than a long dictionary phrase. The scripted sweep in
`analysis/tested.md` covers dictionary and corpus vocabulary exhaustively within
its stated bounds, but a human-reasoned short answer with unusual capitalization
or punctuation (the author's own confirmed style on other blocks, for example
"NGD" for "net zero" or "JD6" for "QWERTY") is a different kind of hypothesis
than a word-list sweep can reach.

What would confirm it: any short candidate, tested through
`tools/oracle.py --block76-filter` first (a near-instant filter) and then
through a full derivation.
What would kill it, in the useful sense: nothing kills this lead outright; it
stays open as a standing invitation, same as any human-reasoned wordplay block
in the series.
Cost: minutes per candidate; no sweep implied.

## 0. Grycoin Block 2 as a second certification vector (2026-08-18)

Two statements recovered from the author's 2019 activity reorder everything
above.

**She removed a twist rather than adding one.** Moving the prize from
`1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC` to the live escrow on 2019-07-30, she said
she "wanted to remove one of the twists". The live target is therefore a simpler
transform than the superseded one, not a variant of equal difficulty. The
2026-08-18 sweep in `analysis/tested.md` treated the dead address as the easy
calibration case, on the reasoning that it predates the modification; that
reasoning is backwards. The dead address carries an extra complication that the
live one does not.

**She published a worked example, after the rehash, on purpose.** Grycoin Block
2, posted 2019-08-02, is described as deliberately written to demonstrate the
exact format used in both stages of block 77, case-flip and copy-paste rules
together. Every block in the series except this folder's two was solved and
swept, so Block 2 is a solved question-and-address pair produced by the same
transform, and produced *after* the author had settled on the format the live
escrow uses.

That makes it a second certification vector, and a better one than Block 77
Stage One in two respects: it needs no third-party text, since the question is
her own writing, and it encodes the post-rehash format rather than the
pre-rehash one.

What would confirm it: reproducing Block 2's escrow address from its published
question text. The serialization that does so is then the author's actual
copy-paste convention, measured rather than guessed, and applying it to the
Wattpad chapter is a single derivation rather than a sweep.
What would kill it: no serialization of Block 2's question reaching its address,
which would mean the transform is not uniform across the series after all.
Cost: minutes, once the question text and escrow address are in hand.

The author also stated, in the Real Big Block discussion thread, that "once
someone figures out the format for the first stage, they will also have a big
hint for the format of this second stage", which is consistent with one
transform across both.
