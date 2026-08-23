# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row.
All figures are re-read from the private research's own dated result logs before
being written here.

## Real Big Block (0.777 BTC)

The mechanism is certified (the case-flip rule reproduces the solved sibling lot
Block 77 Stage One exactly). What is not established is exactly which paragraphs
of the "Second" chapter the author modified on 2019-07-30, and the precise text
she copied. Every row below tests a specific hypothesis about that, against both
the current escrow (`14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`) and its superseded
predecessor (`1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC`).

| Hypothesis family | Candidates | Result |
|---|---|---|
| Chapter unmodified, every plausible serialization (line-break style, encoding) | approximately 150,000 | 0 match |
| Certified case-flip rule applied to the 3 planted paragraph groups plus the Finney quote, 16 combinations, both letter-position modes | approximately 200,000 | 0 match |
| Every subset of the 17 candidate paragraphs (2^17), 18 serialization variants | 2,360,000 | 0 match |
| Paragraphs selected by a name or word ("Satoshi", "Aoi Nakamoto", "Hal Finney", "Grycoin", and 7 more), by first letter or first character | approximately 10,000 | 0 match |
| Every paragraph starting with F or W (and F, W, H) | approximately 1,000 | 0 match |
| The certified groups plus one arbitrary extra paragraph | 13,000 | 0 match |
| The certified groups plus two arbitrary extra paragraphs | approximately 600,000 | 0 match |
| The single-word planted correction from block 29 ("voice" to "vOIce"), alone and combined with the groups | 6,000 | 0 match |
| Block-29-style link suffixes appended to the text | 8,000 | 0 match |
| Chapter subsections read alone | 3,000 | 0 match |
| Page-level prefixes (duplicated title, author byline) | 2,000 | 0 match |
| A simulated Chromium browser copy (selection/innerText rendering rules) | 1,000 | 0 match |
| Alternate text encodings (Latin-1, UTF-16, cp1252, NBSP normalization) | 3,000 | 0 match |
| Simulated-browser-copy base combined with the name/word selectors, then with all 2^17 paragraph subsets | approximately 800,000 | 0 match |
| A single invisible character (BOM, zero-width space, tab, and 6 more) inserted at the start or end | 5,000 | 0 match |
| Paragraphs selected by the letters of "Satoshi Nakamoto" specifically (a refinement of the name-selector row above, after finding the Finney post has a paragraph starting with M) | 60 | 0 match |
| Last-letter-only or first-letter-only variants of the case-flip rule, on the certified groups | 456 texts (2,736 address checks across derivation indices) | 0 match |
| All of the above serialization families repeated under CRLF line endings | 2,448 texts (14,688 address checks) | 0 match |
| 1 to 3 single-letter case toggles across all sign positions, and 1 to 2 across all paragraph boundaries | 1,450,000 | 0 match |
| Every single-character edit (insert, delete, replace, case toggle) at every position, across 40 base texts (5 paragraph-set choices x 2 NBSP conventions x 2 line-ending conventions x 2 separator conventions) | 266,038,400 | 0 match |

Witness status: every row above used the oracle certified against Block 77 Stage
One (see README, "Certified against"); the single-character-edit row additionally
planted 3 synthetic witnesses per base text (head, middle, tail) and recovered
all of them on all 40 bases, plus recovered the real Stage One text and address
when run as a 41st base. Dates: all rows 2026-08-15.

Cumulative for Real Big Block: approximately 272 million candidates tested, 0
match. The single-character-edit sweep accounts for the large majority of this
total and is the only row certified as a complete sweep of its stated space (all
40 bases, every single edit); every other row is a targeted, not exhaustive,
test of one specific hypothesis about which paragraphs were modified.

## Quizchain2 Block 76 (0.077 BTC)

The chain a community player found in 2019 (`solution = "format"`,
`TOMI = "before TOMI"`) satisfies both of the author's published MD5-prefix
hints, but no standard BIP44/49/84 derivation, derivation path, or passphrase
variant of it produces the escrow address. Two later calibration checks (blocks
73 and 74, both already solved and swept, not part of the live prize) confirm
the derivation code itself is correct, and a later cross-check on 2019-07-29
comment timing suggests the "format" chain was itself a false positive found by
searching for strings that pass the 2 published prefixes, rather than the
author's real answer, since the author never corrected the block after seeing it
posted publicly (see README).

Standard-derivation sweep on the `format`/`before TOMI` chain:

| Hypothesis family | Candidates | Result |
|---|---|---|
| BIP44, BIP49, BIP84, accounts 0 to 4, external and internal chains, index 0 to 199 (BIP44 external: 0 to 1999) | standard derivation space | 0 match |
| Non-standard derivation paths (Coleman-style m/0'/0/i, m/0/i, m/0', root key) | small, enumerated | 0 match |
| Passphrase variants ("TOMI", "format", "before TOMI", bracket and whitespace forms) | small, enumerated | 0 match |
| Alternate entropy functions (SHA-256 as a 24-word mnemonic, SHA-1, RIPEMD-160, truncated SHA-512, double MD5) | small, enumerated | 0 match |
| Off-by-one word at BIP39 import (12 positions x 2,047 alternate words each) | 24,564 | 0 match |
| Word order reversed | 1 | 0 match |

Word-transform "salves" on the question "change to" / "from change to" (each
family's candidate solution strings tested through the same 2 MD5-prefix filters
before any derivation; only pairs passing both filters were derivation-tested):

| Salve | Candidate solutions | Passed prefix 1d | Passed both filters (derivation-tested) |
|---|---|---|---|
| Single-letter edits, anagrams, Atbash/ROT/foldover, translations of "change" | 7,730 | 32 | 3,506 TOMI pairs, 0 match |
| WordNet synsets and hyper/hyponyms of change/alter | 20,199 | 74 | 8,806 TOMI pairs, 0 match |
| Wikipedia article titles containing "change" | 14,666 | 44 | 4,949 TOMI pairs, 0 match |
| Sentences from Satoshi/Hal Finney bitcointalk posts and emails containing "change to" | 46 | 0 | n/a |
| Sentences from bitcointalk posts numbered 60 to 94 (2 orderings) | 1,992 | 11 (noise) | n/a |
| Strings built from the number 76 (years, technical constants, ordinals) | 3,779 | 23 (noise) | n/a |
| Encodings of "change" (hex, base64, NATO alphabet, Morse, keyboard shift) | approximately 130 | 1 (noise) | n/a |
| "changeto" (no space) combined with TOMI variants | 1 | 1 | 1,701 TOMI pairs, 0 match |
| Every address and txid from the author's 158 other funding transactions | approximately 1,500 | 4 (case noise) | n/a |
| Renaming candidates ("wealth", "legacy", and similar) | 45 | 0 | n/a |
| An Easter/resurrection word family, echoing the same block number in round 1 | 2,752 | 17 (noise) | 5,857 TOMI pairs, 0 match |
| Halving-related terms | 45 | 1 (noise) | n/a |
| Grycoin/burn-address/second-layer terms from the chapter | 60 | 0 | n/a |
| Literal strings and typos from the block's own post | 45 | 0 | n/a |

A separate "post-number-as-index" method, confirmed on 3 other blocks in the
series (numbers 56, 57 and 58 each index a specific post or tweet by Satoshi or
Hal Finney, by position), does not carry over to block 76: post number 76 in
every corpus and ordering tried (Satoshi's bitcointalk posts newest-first and
chronological, Hal Finney's posts, Hal Finney's tweets) contains neither "change"
nor "from".

A large dictionary-times-corpus sweep tested every 1-to-4-word phrase built from
the author's own writing (Reddit posts, comments, and Wattpad chapters) as a
candidate TOMI value, against a dictionary-and-WordNet-derived candidate solution
list: 189,565 candidate solutions passing the first filter, times 656,845 to
1,250,000 candidate TOMI phrases depending on the pass, for a combined total of
approximately 3.2x10^11 MD5 computations and approximately 78 million full
address derivations on the pairs that passed both filters. 0 match. The
derivation code was re-confirmed correct on both calibration blocks (73 and 74)
at the head, middle and tail of this run.

Cumulative for Block 76: approximately 78 million address derivations from the
scripted dictionary sweep, plus approximately 53,000 smaller thematic candidates
across the 14 salves above, plus the full standard-derivation sweep on the one
chain found by search. 0 match anywhere. This is reported as a targeted, not
exhaustive, negative: the true solution may use vocabulary outside the corpora
swept (the author's own writing and 2 general-purpose dictionaries), and the
block may simply be misconfigured (see README).

## Contiguous-range serialisation sweep, with the superseded address as a
## calibration target (2026-08-18)

Every earlier row selects paragraphs as an arbitrary subset, up to 2^17 of them.
A browser selection is not arbitrary: it is a drag, and a drag is contiguous.
The realistic space is therefore every contiguous range of the chapter's lines,
not every subset, and that space is small enough to exhaust outright.

Set: all 4,095 contiguous ranges of the chapter's 90 lines as returned by the
Wattpad API, crossed with 8 paragraph separators (LF, LF LF, CRLF, CRLF CRLF,
CR, LF CR LF, space, non-breaking space), 2 quotation conventions (the smart
quotes as stored, and an ASCII fold of them), 5 edge conventions (none, trailing
LF, trailing CRLF, leading LF, leading BOM), and 2 readings of the certified
case-flip rule (applied to the range, or not). 655,200 candidate texts,
6 derivation indices each.

Targets: both live escrows, and `1EFojcAo2vbhRGCGCa7q8Wwvzss28mhQYC`, the
superseded address funded 2019-07-24 from the pre-rehash solution. That third
address is the useful one. It holds nothing, so hitting it wins no money, but
the author states the live version is the same text with one line break changed
to two, so pinning the byte format that produces it would leave the live
address one documented step away.

Result: 0 match on all three. Witness: a candidate drawn from the swept space
itself, planted with its own derived address and recovered by the run.
Duration: 6.8 minutes at 1,609 candidates/second on 4 CPU cores.

What this rules out is worth stating precisely, because it points somewhere. The
failure to reach the superseded address is the informative half. That address
should be the easy case: the chapter as published, one line break between
paragraphs, no modification of any kind. If the API's text were byte-faithful to
what the author copied in 2019, some contiguous range of it under some ordinary
separator should reproduce it. None does. So the remaining discrepancy is not in
which paragraphs were selected, nor in how they were joined; it is in the source
bytes themselves. Something the author hashed is absent from the text the API
returns today, which is consistent with her own statement that she added extra
line breaks and with the API storing none.

The next test is therefore the chapter's raw HTML rather than its extracted
text: empty paragraph elements, `&nbsp;` entities and `<br>` tags all survive in
the markup and all vanish from a text extraction, and any of the three would
change the hash while leaving the visible chapter identical.

## Grycoin Block 2 as a worked example, and why the reversal could not run yet
## (2026-08-18)

Block 2's escrow is `1tzieUfbeQghz2zjDeGHcAEfzCRgX6eLi`, funded with 700,000
sats on 2019-08-01 in transaction
`f11eca9925c7809210796a3c8d95677dfaf0becb4f6df4c74e7261c3011a2e3c`, and it is
spent. The block was solved, so the transform demonstrably produces claimable
keys, and reversing that solved pair would measure the author's conventions
rather than leaving them to be guessed: how many letters get toggled, what her
line breaks were byte for byte, which derivation index she used, and where her
copy started.

The reversal cannot run yet because the question text is not recovered. Reddit
is refusing both the JSON endpoint and the old interface to scrapes, and the
best reconstruction available from surviving snippets is provably incomplete:
the author's instruction is to "stop with the period after method", and the only
occurrence of that word in the reconstruction sits inside the instruction
itself, followed by a quotation mark and a comma rather than a period. The
question body that ends in "method." is absent.

Tested anyway, in case the reconstruction was closer than it looked: 10 base
readings of it, crossed with 0, 1 and 2 letter case toggles, 14.3 minutes, 0
match against the Block 2 escrow. That is the expected result for a text missing
its ending, and it is recorded here only so the same partial reconstruction is
not swept again.

What would unblock it: any pristine copy of the Block 2 post. A Wayback capture
of the Reddit thread is the most likely source and has not been checked. The
repository's fact 6 records that no archive of the Wattpad chapter exists, but
that check covered the chapter, not the author's Reddit posts, which are on a
far more heavily crawled host.

## Block 2's question text, pinned exactly (2026-08-18)

A player asked her, in the Block 2 thread, for the hash of the full Question
text *without* the letter changes, so that he could check his own transcription
before starting -- he was not on Windows and his copy gave him LF line breaks.
She answered:

> Thank you for asking. I really like the answer, turns out that the first seven
> digits of that MD5 hash are 7759227, with three numbers 7 turning up there.

That is 28 bits over the unmodified text, with no flip subset and no key
derivation in the way: a direct check on a transcription. Running the recovered
post through it lands on

    md5 7759227d7406d8230d7e3a8f7b9846d7

which measures the text and its serialization outright, and settles two things
that had been assumed:

| | Measured |
|---|---|
| Separator | LF LF. Not CR LF CR LF, though the post says "13 10 13 10" |
| Paragraph 5 | one paragraph: "...outing himself. Even after I explained..." |
| Quotes and apostrophes | straight; the text is plain ASCII throughout |
| The transcription | correct, character for character |

The separator is the useful correction. She describes typing CR LF CR LF, and
her instruction is to copypaste from the rendered post -- and what a copy of a
rendered Reddit post produces is LF LF. What she typed and what her tool hashed
are not the same thing. The same distinction is the open question on the Real
Big Block, where the argument has been about what her browser produced from the
Wattpad page rather than what she typed into it.

It also kills the reading that her worked example implies: "I" to "i" and
"himself" to "himselF" in one step only pairs a paragraph's first and last
letter if that paragraph ends at "himself." The hash says it does not.

Two more published solutions check out on the same front of the pipeline, and
are now part of `tools/oracle.py --selftest`:

| Block | Solution, exactly as she gave it | Announced prefix | MD5 |
|---|---|---|---|
| Quizchain2 Block 67 | `Thomas TOMI Harold Thomas Finney II` | f47 | f4738a... |
| Grycoin chain Block 1 | `Still 21st Century` | 4c4 | 4c4148... |

## Block 2 case changes, on the pinned text (2026-08-18)

With the base text pinned, the only unknown left on Block 2 is which letters
change case, and her published 3c6 prefix filters that for free.

| Family | Candidates | Result |
|---|---|---|
| Every subset of the 10 paragraph-initial and 10 paragraph-final letters (2^20) | 1,048,576 | 0 match |
| Paragraph initials alone, all subsets | 1,024 | 0 match |
| Paragraph finals alone, all subsets | 1,024 | 0 match |
| Every 1 or 2 letter case change anywhere in the text | 717,004 | 0 match |

The first row is the important one: it is exhaustive over the entire
first-letter-down, last-letter-up family at paragraph granularity, in both the
forced and the toggled reading, since forcing is a subset of toggling here. So
Block 2's answer changes at least one letter that is neither a paragraph's first
nor its last -- which is consistent with her own example, where "himself" ends a
sentence in the middle of a paragraph rather than the paragraph itself.

## The selection rule, measured on the solved lot (2026-08-18)

Defending the puzzle in the Block 77 thread, she states the mechanism:

> There is no way to dispute that if you take all the paragraphs not starting
> with a letter in "Satoshi" and look at the last letters of these you get STNM.
>
> I assume you understand that STNM would be a reasonable way to sign as
> "Satoshi Nakamoto".

Her description is loose, and the post she is describing settles it. Hal
Finney's "Bitcoin and me" was fetched from bitcointalk rather than transcribed
and run against Block 77 Stage One's own escrow,
`19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`, which is solved and spent. It reproduces:

| | Measured |
|---|---|
| Paragraphs | 16, initials `IFFWIWTATSMATIAT` |
| Selector | keep I, T, A, S, M; mark the other 4 |
| Marked paragraphs' last letters | `s`, `t`, `n`, `m` -- STNM |
| Rule | first letter lowered, last letter raised |
| Separator | LF LF |
| Derivation index | 0 |

S, A, T, O, H, I taken literally from her sentence marks 5 paragraphs instead of
4 and reads STNMT, and does not reproduce the address. The full letter set of
"Satoshi Nakamoto", which adds N and K, marks the same 4 as I, T, A, S, M here,
so this post cannot separate those two readings. It does rule out hers as
written. A text with more distinct paragraph initials will separate them, and
the "Second" chapter has 90 paragraphs, so it will.

This is the calibration the folder had been asserting from the private research
without a reproduction in the repository. It now has one, and it was measured
from the source's own bytes.

## Block 2 reversal, from the full post text (2026-08-18)

The Block 2 post was recovered in full, so the reversal that the section above
records as blocked could finally run. It does not solve the block.

The question body is the 10 paragraphs from "I thought I would write a bit about
the format for block 77" through "it should be faster to solve by the thinking
only method." -- her stated start, the first "I", and her stated stop, the period
after "method". Everything her post fixes was taken as fixed: the separator she
spells out as ASCII 13 10 13 10, no whitespace at either edge, and the free
12-bit filter "First three digits of MD5 hash are 3c6", which rejects candidates
before any key derivation and makes the whole sweep cost nothing.

What was left free is what a copy out of a browser can change, plus the one
thing the recovered text cannot settle by itself. Her worked example changes
"I" to "i" and "himself" to "himselF" in the same step, which only makes sense
as one rule over one paragraph if that paragraph ends at "himself." -- yet in
the recovered text the sentence continues. A paste can merge two paragraphs but
cannot invent one, so every sentence boundary inside every recovered paragraph
was searched as a possible lost break.

| Dimension | Values |
|---|---|
| Lost paragraph breaks | all 2^5 subsets of the 5 internal sentence boundaries |
| Flip subsets | every subset of the resulting 10 to 15 paragraphs |
| Case rule | force (first lowered, last raised) and toggle |
| Quotes and apostrophes | straight, curly, and each independently |
| Ellipsis | 3 periods and the single character |
| Separator | CRLFCRLF, LFLF, CRLF, LF |
| Encoding | UTF-8 and cp1252 |
| Derivation index | 0 to 9 |

27,869,184 texts, 63 seconds on 4 cores. 6,998 passed the 3c6 filter against a
chance expectation of 6,804, which is the first result worth reading: the prefix
hits land exactly where random texts would put them, with no excess anywhere in
the grid. 0 of the 69,980 derived addresses is the escrow.

Witness: a point of the grid was picked (split mask 10110, curly quotes and
apostrophes, CRLFCRLF, cp1252, toggle, a specific flip subset), its own address
derived at index 3, the searcher retargeted at that address, and the searcher
recovered exactly that point. A negative from a searcher that cannot find a
planted positive is worthless; this one can.

A single correct point inside that grid would have been found, so the grid does
not contain it. The recovered text differs from what the author posted by
something none of these dimensions varies -- a word, a comma, a capital letter.
The transcription came through screenshots, which is exactly where that kind of
difference survives unnoticed.

What would unblock it: `tools/fetch_sources.py`, run anywhere with open outbound
HTTPS. Reddit's JSON endpoint returns `selftext`, the raw markdown the author
typed, character for character, which removes the transcription from the loop
entirely. The same fetch collects the Block 77 Stage One post, whose reversal is
already reproduced and would then be re-derivable from pristine bytes as a
witness, and both forms of the Wattpad chapter.

## The chapter, at its real length (2026-08-18)

Every Real Big Block row above this section was run against a 90-paragraph,
9.5 KB rendering of the "Second" chapter. The chapter is 273 paragraphs and
45,450 characters. The ledger was searching roughly a fifth of the text.

The mistake is easy to make and hard to notice. Wattpad serves a part's text
from a paginated endpoint, `apiv2/?m=storytext&id=720888559&page=N`, and a fetch
that omits the page parameter, or stops early, returns a prefix that looks like
a complete chapter: it starts at the title and ends mid-sentence only if you
check. Completeness is checkable outright -- the part metadata reports
`length` 45451, `pages` 12, `wordCount` 9091, and the 273 paragraphs joined with
a blank line come to 45450 characters, which is that length less one trailing
newline. Page 13 returns nothing.

### The signs, located

The chapter documents its own mechanism. Paragraph 228 reads

> All paragraphs except for four, which start with F F and W W.

describing the Finney post it goes on to quote, and paragraph 236 is the bare
string `STNM`, paragraph 238 `I STNM.`. So the marked paragraphs are the ones
whose initial breaks the pattern, and their last letters carry the signature.

That pattern occurs exactly 4 times in 273 paragraphs, and every one of them
spells `stnm` in its final letters. They are also the only `stnm` runs anywhere
in the text:

| Paragraphs | Initials | Finals |
|---|---|---|
| 4 to 7 | `FFWW` | `stnm` |
| 92 to 95 | `FFWW` | `stnm` |
| 167 to 170 | `FFWW` | `stnm` |
| 230 to 234 | `FFWIW` | `stngm`, marked 230 231 232 234 |

The fourth is Hal Finney's post quoted verbatim, carrying its own `IFFWIW`
shape, which is why its marked four skip a paragraph. This folder already
recorded "the 3 planted paragraph groups plus the Finney quote" as tested; that
test ran on the 90-paragraph text, where 3 of the 4 groups lie past the end.

### What that structure does not do

| Hypothesis | Candidates | Result |
|---|---|---|
| Letter-set selectors (ITASM, SATOSHI, NAKAMOTO, AOINAKAMOTO, HALFINNEY, combined) x 3 rule modes x 4 separators x 4 trailers x 36 text variants | 48,384 | 0 match |
| The chapter with nothing changed, every variant and separator | 864 | 0 match |
| First or last k of the letter-set-marked paragraphs, k = 1 to 118 | approximately 57,000 | 0 match |
| Prefix and suffix truncations at every paragraph, with and without the rule | approximately 26,000 | 0 match |
| The rule applied inside every contiguous run of paragraphs | approximately 297,000 | 0 match |
| Every subset of the 4 FFWW groups, 3 rule modes, 4 separators, 2 trailers, 36 variants, indices 0 to 19 | approximately 14,000 | 0 match |
| Every subset of the 16 individual FFWW paragraphs, 8 variants, 2 separators | 1,048,576 | 0 match |
| FFWW group subsets crossed with every subset of the 10 extra sign candidates (the paragraph Finney's shape skips, `STNM`, `I STNM.`, and the 7 paragraphs that already end in a capital) | approximately 262,000 | 0 match |
| The same crossed with truncations | approximately 140,000 | 0 match |

The text variants cover what a browser copy of that page can change: `<br>`
inside a `<p>` as a newline, a paragraph break or a space; the 6 non-breaking
spaces kept, spaced or dropped; per-paragraph whitespace kept or stripped; the
title paragraph in or out. The chapter contains no curly quotes, dashes or
ellipsis characters at all, so those dimensions collapse.

The FFWW structure is not a coincidence -- 4 occurrences in 273 paragraphs, all
spelling the signature, in a text that names the rule in prose. But flipping
some subset of exactly those paragraphs is now exhausted. Either the marked set
includes paragraphs outside them, or the bytes her 2019 browser produced differ
from the API's HTML in a way this parse does not reproduce.

### What is running

Her own description of the format is "keep the whole long text and change only a
couple of letters in their capitalization". Flipping one paragraph changes two
letters, so one to three flipped paragraphs anywhere in the chapter is the
literal reading, and it is only 3.4 million candidates. There is no free filter
on this block -- no published MD5 prefix -- so every candidate costs a full
PBKDF2-HMAC-SHA512 at 2048 iterations, about 1.9 ms, which is the floor on a
CPU. k up to 3 is roughly an hour on a small machine and is exhaustive for that
reading. k = 4 is 224 million and needs a GPU.

## Two conventions the author states outright for the Real Big Block (2026-08-18)

The "Real Big Block Discussion" thread settles two things that earlier work had
inferred from sibling blocks rather than from this one.

Separator. A player asks whether "two line breaks" means one Enter or two. She
answers: "the second one. Hit enter twice. This displays in Ascii as 13 10 13
10, according to asciivalue.com." That is CR LF CR LF, not LF LF. Stage One and
Grycoin Block 2 were measured at LF LF, but they are different sources; the Real
Big Block is the Wattpad chapter, where she added the extra breaks, and she
states its separator directly. Earlier chapter sweeps tried CR LF CR LF only on
whole-group subsets, never on the exhaustive small marked-set search, which had
used LF LF and LF alone.

Index. Discussion point 4: "I just noticed that the 7th private key in the list
for this wallet contains the number 7 three times ... Maybe should have sent the
funds to that address. But the first one also has some amazing properties." She
sent the funds to the first address, so the derivation index is 0. This closes
the block-number-as-index idea (from Quizchain2 Block 2, "the second private key
because this was block 2") for the Real Big Block specifically.

`tools/chapter_sweep.py` was rerun with CR LF CR LF and index 0 across the full
rule and every 1, 2 and 3 paragraph marked set. [result pending]

## The chapter read in full, and the marking model narrowed (2026-08-19)

The chapter was fetched at full length and read. It documents its own mechanism,
and that reading eliminates the marking rule the whole search had assumed.

Paragraph 240, in the author's own words: "the FF and WW has meaning as well, as
a dedication message. WW obviously is UUUU or 'four U, for you'. I leave it as an
exercise for the reader to figure out who FF is." The FFWW paragraph groups --
at 4-7, 92-95, 167-170, each spelling stnm in their final letters -- are a
planted dedication, not the solution signs. That is why every FFWW-subset sweep
failed: they are a decoy.

The letter rule that solved Block 77 Stage One does not transfer either. On the
Finney post, the paragraphs whose initial is not in I,T,A,S,M number exactly 4
and their last letters spell STNM. On the chapter, that same rule marks 119
paragraphs whose last letters spell garbage (stnmnm?dsrsgerhmm...), and no
keep-set of initials isolates a 3-to-8 paragraph set with a clean signature.

So the marked paragraphs are chosen by meaning, not by any letter or position
rule. That was tested directly: every 2-to-5 paragraph subset of the 20
paragraphs that actually make the identity claim or are named as the code
source (5, 167, 188, 193, 198, 199, 210, 227, 229, 230, 231, 232, 234, 235, 236,
238, 244, 245, 265, 272), in both the flip and the last-letter-only operation,
both separators, indices 0-9 -- 21,679 subsets, 0 match.

| Model | Coverage | Result |
|---|---|---|
| Whole-paragraph flip, FFWW groups | every subset of the 16 | 0 (decoy, per para 240) |
| Whole-paragraph flip, full ITASM | 119 paragraphs | 0 (finals are garbage) |
| Whole-paragraph flip/last, 1-3 paragraphs anywhere | exhaustive | 0 |
| Whole-paragraph flip/last, 2-5 of the 20 identity paragraphs | 21,679 sets | 0 |
| Whole-paragraph flip/last, every 4 paragraphs anywhere | 216,540,318 x 2 modes x 2 seps | in progress |

What the negatives point at: her Block 2 worked example changes individual
letters mid-paragraph -- "I" to "i" and "capitalization" to "capitalizatioN".
That last change capitalises the final letter of a word in the middle of a
paragraph, not a paragraph boundary. If the Real Big Block's "change only a
couple of letters" is the same kind of per-letter edit at positions the prose
points to, no paragraph-level sweep can reach it, and the exhaustive k=4 run is
the last test of the paragraph model before that conclusion is forced.

What would break it open: the exact winning string of any block this author
solved in the same era -- Block 77 Stage One, or Quizchain2 Block 76, which was
solved and swept 2026-08-17. A single worked per-letter example fixes the model.

## Per-letter model confirmed, paragraph model exhausted (2026-08-19)

Her own documentation settles the operation. Complete Quizchain, block 29:
"just change the o and i in 'voice' in the second sentence to 'O' and 'I', same
method as in Block 2. Only two letters changed." Block 2 first round: "One of
the letters in the family name of the author is changed from lower to upper
case. Change the other letters in his name in the same way." The solution
capitalises a few specific letters inside words -- not paragraph boundaries.

That retires the whole-paragraph model, which is now exhausted anyway:

| Search | Coverage | Result |
|---|---|---|
| Per-letter: capitalize each name occurrence, and each signature (STNM, SATOSHI, NAKAMOTO, ...) as an in-order subsequence within paragraph/sentence/whole | ~27,000 | 0 |
| Contiguous slice of the chapter + plain/ITASM/FFWW flip, every range, both separators, indices 0-9 | 36,856 ranges | 0 |
| Every 4-paragraph flip/last set, both separators (k=4 backstop) | 216M x 4 | in progress |

The block-77 material in the Wattpad "Complete" chapters is all first-run
(the genesis address: "eight items in two sets of four, 44 read from left and
from right"). The live second-run Stage Two is marked "stay tuned" -- its
specific letter pointer is not in the story. It is in the Reddit threads:
Stage One (`ca6jxv`, solved) whose winning comment shows the exact per-letter
operation on a bounded text, and the discussion thread (`chn8un`). Both are the
gating information; brute force cannot substitute for them, since the marked
letters are 2-to-4 positions among ~37,000 with no filter.

## The chapter pinned, the separator measured, four models eliminated (2026-08-20)

The "Second" chapter was recovered in full as served markup and pinned before
any candidate was tested. It parses to 273 paragraphs and 44,906 characters of
prose; joined with LF LF that is 45,450 bytes, which is the part length the
2026-08-18 metadata reports. Its first-letter and last-letter streams reproduce
the ones recorded in that entry character for character. The chapter this entry
tests is therefore the chapter, not a rendering of it.

Paragraph 240 was read from those bytes and says what the 2026-08-19 entry
reports, in her words: "And by the way, the FF and WW has meaning as well, as a
dedication message. WW obviously is UUUU or 'four U, for you'. I leave it as an
exercise for the reader to figure out who FF is." The three stnm runs sit at
paragraphs 4-7, 92-95 and 167-170, and each is an FFWW group. A shuffle of the
same last letters produces 0.07 such runs on average against the 3 observed, so
they are planted; paragraph 240 says what they are planted as.

### The separator, settled on her own published hash

Block 2 is the only lot where she published the hash of an unmodified question
text, and it decides the separator outright:

| Separator | MD5 of the Block 2 question |
|---|---|
| LF LF (`\n\n`) | `7759227d7406d8230d7e3a8f7b9846d7` -- her announced 7759227 |
| CRLF CRLF (`\r\n\r\n`) | `e997007971f6f17c8775d83f30edb4c6` |
| CRLF (`\r\n`) | `fc3c7a6634dcb02eb33e341b47ef1a83` |
| LF (`\n`) | `7d6f7387fedec29ebbfea54045cf0820` |

Seven hex digits is 28 bits, so this is not a coincidence: what her tool hashed
was LF LF, and her own description of typing "13 10 13 10" describes her
keystrokes, not her bytes. No reading of which sentence of hers is controlling
can override this, and the single-CRLF reading in particular is ruled out.

### Derivation re-certified without bip_utils

The sweeps below use a pure-python MD5-entropy to BIP39 to BIP44
`m/44'/0'/0'/0/i` to P2PKH implementation, certified before use against both
legs of her own published chain: `2941774a2abec9f30c7d6777d1d53d91` at index 1
gives `L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex`, and
`7b44cc11c866ab85b7078c43ad6795e1` at index 0 gives
`KzFB7hBGmLBqm8nqVCVLBmgyd1NxnoJXZUhE377QL4T2iy5rw4Wz`. A negative from an
uncertified deriver is worthless; this one reproduces her numbers exactly.

### Eliminated on the chapter

Each set below is swept over every subset, in 4 operations (first-down-last-up,
toggle, last-up only, last-down only), both separators, against both the live
escrow and the superseded one.

| Mark set | Why it was a candidate | Coverage | Result |
|---|---|---|---|
| The 9 paragraphs whose last letter is already uppercase: 188, 189, 193, 206, 210, 228, 236, 238, 258 | the only paragraphs in 273 where force and toggle differ, so the only ones carrying evidence of which rule she used | 512 subsets, 16,384 addresses | 0 |
| The 12 paragraphs containing "recognize the signs": 19, 41, 219, 221, 222, 224, 225, 229, 235, 243, 245, 272 | the most literal reading of her Block 2 instruction, "for all the paragraphs where you recognize the signs" | 4,096 subsets, 327,680 addresses | 0 |
| The 5 malformed-capitalization words: `VIrgin` (127), `BItcoin` (135), `ppM` (72), and the stray capital L in both alphabet strings (125) | "change only a couple of letters in their capitalization" plus "two and only two changes"; a proofreader notices these, a script does not | 1,440 texts, 14,400 addresses | 0 |

The casing scan that produced the third row is exhaustive over the chapter: of
every word carrying a non-initial capital, all others are acronyms (ALS, OPEC,
PGP, RPOW, IBM, STNM, PETM, UTXO, CPU, HAL, THOMAS, TOM, GRY, BIT, AH, FF, WW,
UUUU, II, III, NOT, ST) or her own deliberate constructs
(`WorldWideAbsoluteCarbonBudget`, `AHScoin`, `BITcoin`, `oXXX`,
`FUCKFuckFUCK...`). The five above are the complete set of malformed ordinary
words.

### The three planted instances are not the Finney shape

Her three FFWW instances open the three major sections and are preceded, not
interrupted, by their I paragraphs:

    I. Second Life        3:I   4:F 5:F 6:W 7:W
    II. Second Layer     91:I  92:F 93:F 94:W 95:W
    III. Second Identity 164:I 165:I 166:I  167:F 168:F 169:W 170:W

The post they imitate has the I *inside* the run. In the chapter's own
quotation of it, paragraphs 230-234 read F F W I W, with "I was more positive."
sitting between the two W paragraphs. So no instance reproduces the source
shape, and the count of leading I paragraphs -- three for Second Identity
against one each for Second Life and Second Layer -- is the only asymmetry
separating the three.

### Her alterations to the Finney post, audited

Hal Finney's post was diffed against every place the chapter quotes it. The
long block quotation at paragraphs 230-234 is verbatim with exactly one change,
`facinating` to `fascinating`. Paragraph 221 quotes "Today, Satoshi's true
identity has become a mystery" verbatim, keeping "true". Her looser quote at
paragraph 216 carries four alterations: `correspond with both` to `correspond
both with`, `create` to `make`, `proof of work` to `proof-of-work`, and a
truncation.

One alteration sits at a marked position. Having quoted "true identity"
correctly at 221, paragraph 242 gives the *extraction* as `"Today, Satoshi's
real identity"`, and 245 repeats "real identity" twice. Recorded because it is
an author-created substitution at the step she labels "the first four words",
and because the live block is called the Real Big Block. Weighted low: "real"
appears 10 times in the chapter against 4 for "true", so it is her habitual
word, and the phrase 245 is building is "Satoshi's real identity, recognize the
signs". The FFWW groups are the standing warning here -- deliberate, planted,
statistically impossible by chance, and documented by her as a decoy.

### A transcription warning

A copy of the Finney post taken from a rendered forum page reproduces the
structure exactly -- 16 paragraphs, initials `IFFWIWTATSMATIAT`, the 4
non-ITASM paragraphs at 1, 2, 3, 5 with last letters STNM -- but does not
reproduce Stage One's escrow under any of 108 serializations (3 keep-sets x 3
case rules x 3 quote styles x 4 separators, indices 0-9, 1,080 addresses). The
derivation is certified, so the difference is in the bytes. Fetch that post,
never transcribe it; the same caution applies to any source used here.

## Stage One's solution hash, and four certified negatives (2026-08-20)

### A free filter on Stage One nobody had recorded

In the Block 77 Stage One thread, the winning solver posted, on solving it:

> Okay. I think solving 77 deserves a celebration of sorts. Here you are:
> 9dd (copypasted).

That is the first three digits of the MD5 of Stage One's winning solution, in
the same form the author uses for every other block. It is a free 12-bit filter
on a *solved* lot whose carrier text (Hal Finney's "Bitcoin and me", bitcointalk
topic 155054) is public, and it was not recorded here before. Anyone holding a
fetched copy of that post can now check a candidate serialization for `9dd`
before deriving a single key, which is 4,096 candidates rejected per MD5.

The author's own Hint 2 in that thread also settles a wording question: she
writes "Satoshi's true identity" there, matching Hal. The chapter's "Satoshi's
real identity" (paragraph 242) is therefore a later drift in her own prose, not
a reading she carried from the start.

### The separator, settled by measurement rather than by her description

A player told her he was not on Windows, so his copy of the Block 2 question
gave him LF line breaks, and asked for the hash of the unmodified text so he
could check his transcription. She answered with `7759227`, and separately told
him "copy paste and do not change anything with the line breaks". Testing every
separator against that published anchor:

| Separator | MD5 of the unmodified Block 2 question |
|---|---|
| LF LF `\n\n` | `7759227d7406d8230d7e3a8f7b9846d7` **matches** |
| CRLF CRLF `\r\n\r\n` | `e997007971f6f17c8775d83f30edb4c6` |
| CRLF `\r\n` | `fc3c7a6634dcb02eb33e341b47ef1a83` |
| LF `\n` | `7d6f7387fedec29ebbfea54045cf0820` |

LF LF, at 28 bits. Her post says she typed "13 10 13 10"; her tool hashed
`\n\n`. Her account of her own byte format is wrong, so no reading of which
sentence is "controlling" can settle a byte question -- only a published hash
can, and there is exactly one.

### The chapter, verified independently

The Wattpad chapter was reconstructed from its HTML and checked three ways: 273
paragraphs, the paragraph-initial and paragraph-final letter streams matching
character for character, and 44,906 characters of prose + 272 LF LF separators
= 45,450, the length recorded in fact 5. Paragraph 240's dedication statement
was read in the author's own words, confirming the FFWW decoy from the source.

### Derivation certified before any negative was recorded

`derive.py`, a standalone implementation used for these sweeps, reproduces both
legs of her published chain exactly: `2941774a2abec9f30c7d6777d1d53d91` at index
1 gives `L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex`, and
`7b44cc11c866ab85b7078c43ad6795e1` at index 0 gives
`KzFB7hBGmLBqm8nqVCVLBmgyd1NxnoJXZUhE377QL4T2iy5rw4Wz`, plus the BIP39 all-zero
vector. The negatives below are measured, not asserted.

### Block 2: the answer changes four or more letters

| Search | Coverage | Result |
|---|---|---|
| Sentence-scoped flip, no inserted break | 32,768 subsets x 2 rules | 0 |
| Every 1, 2 or 3 letter case change anywhere | 285,129,390 | 0 |

The sentence-scoped model matters because it reproduces her worked example
byte-perfectly -- marking paragraph 5's first sentence yields exactly
`i expected otherwise...` and `...outing himselF` -- and it edits nothing but
the marked span, where `block2_reverse.py`'s split grid inserts separator bytes
and so never tested this model. Every subset of the 15 sentences fails.

The 3-letter sweep is exhaustive over every triple of positions in the text,
with no structural assumption at all: 69,424 candidates passed her `3c6` prefix
against a chance expectation of 69,612 -- dead on chance, no excess anywhere --
and none of the 347,120 derived addresses is the escrow. Combined with the
earlier exhaustion of all 1 and 2 letter changes, **Block 2's answer changes at
least 4 letters**. That is the first quantitative bound on her "change only a
couple of letters".

### Real Big Block: four more paragraph-selection models eliminated

| Marked set | Coverage | Result |
|---|---|---|
| The 9 paragraphs whose last letter is already uppercase (188, 189, 193, 206, 210, 228, 236, 238, 258) | 512 subsets x 4 ops x 2 seps | 0 |
| The 12 paragraphs containing "recognize the signs" (19, 41, 219, 221, 222, 224, 225, 229, 235, 243, 245, 272) | 4,096 subsets x 4 ops x 2 seps x idx 0-9 | 0 |
| The 12 FFWW paragraphs (4-7, 92-95, 167-170) | 4,096 subsets x 4 ops x 2 seps x idx 0-9 | 0 |
| The 5 malformed-capital words, every casing variant | 1,440 texts x idx 0-9 | 0 |

The 9 uppercase-final paragraphs are the only ones in 273 where "force" and
"toggle" differ, so that row closes the rule-variant question at paragraph
granularity. The FFWW row now rests on a measurement here rather than on the
private research it was quoted from.

An inventory of every word in the chapter carrying a non-initial capital, with
acronyms and her deliberate constructs removed, leaves exactly five: `VIrgin`
(127), `BItcoin` (135), `ppM` (72), and two alphabet strings in paragraph 125
each carrying a stray capital L. The Bitcoin-address example there,
`3abcdefghijkLmnopqruvwxyz`, is also missing `s` and `t` where the Grycoin one
`7abcdefghijkLmnopqrstuvwxyz` is complete -- worth noting in a chapter about the
signature STNM, though restoring letters is a content change her rule forbids.

### What is still open on Block 2

Four or more changed letters, in combinations `words.py` cannot reach because it
forces *both* edits of a marked word. The bounded next layer is every case
change at up to 4 of the 296 word-boundary positions that carry a case effect:
317,735,946 candidates, the same scale as the 3-letter run, filtered by `3c6`.

## A published plaintext hash, solved (2026-08-20)

The genesis-block chapter closes its hint series with two 28-bit anchors for the
first-run block 77:

> After the above hints it should be fairly obvious what the cleartext items
> are. But to celebrate the French national holiday [...] I now release partial
> MD5 hashes for the plaintext items, just so everyone can make sure they got
> that part right.
>
> For the two plaintext items read from the left, the first 7 digits are
> cc9485a. For the two plaintext items read from the left, they are d78c92f.

The second "from the left" is a slip for "from the right"; the chapter reads the
address in both directions. The first anchor falls to a plain string:

    "Hal Finney"  ->  cc9485a095f30ddc861118b8e7449e2d

matching her published `cc9485a` at 28 bits. The counterpart `d78c92f` does not
match `Nakamoto Satoshi`, `Satoshi Nakamoto`, `Nm ST`, `N7 S5`, or any of
1,854,816 candidates built from every substring and reversed substring of the
genesis address crossed with the name forms and six joiners.

What the solved half is worth is calibration on the *shape* of her answers. The
chapter's machinery around this address is enormous -- Atbash, two foldovers,
Fibonacci, Roman numerals, the Voldemort anagram, HAL as IBM -- and the answer
string it all produces is a person's name, ordinarily capitalized, with a single
space. That matches every other solution of hers on record: `Still 21st Century`,
`Thomas TOMI Harold Thomas Finney II`. Her narrative is elaborate; her answer
strings are plain. A Stage Two hypothesis that requires an elaborate constructed
string is out of character for the author, on her own published evidence.

The same chapter list also settles the `true`/`real` question raised by paragraph
242. Her Wattpad table of contents carries a chapter titled **"Satoshi's Real
Identity", dated 2019-04-24** -- three months before the Real Big Block existed.
"Satoshi's real identity" is her house phrase, not a pointer planted for this
block.

### Paragraph-initial recognition does not transfer to the chapter

Sixteen candidate recognition keys were tested as paragraph-initial keep-sets
over the 273-paragraph chapter, on the model that reproduces Stage One:

| Key | Paragraphs marked | Finals |
|---|---|---|
| HAROLDTHOMASFINNEY | 56 | `nmm?dsrsmmtseents...` |
| SATOSHI | 95 | `stnmnm?dsrsgerhmm...` |
| AOINAKAMOTO | 117 | `dgstnmm?dsrsgehhm...` |
| ITASM | 119 | `stnmnm?dsrsgerhmm...` |
| THOMAS | 140 | `enstnmnnmsd?dsrss...` |
| HALFINNEY | 147 | `dgnmm?dsrswhmlmts...` |
| AOI | 175 | `dgstnmnm?dsrsgewh...` |
| SECOND | 224 | `enstnmnmesd?dsrss...` |

None yields a small marked set with a readable signature, and none can: a
keep-set of k letters marks about (26-k)/26 of all paragraphs, which is 4 of 16
on Hal's post and dozens to hundreds of 273 here. The mechanism is not
scale-invariant, so no choice of name rescues it. What must be revised is the
assumption that Stage Two recognises signs at paragraph initials at all.

### The chapter's one markup anomaly

A scan of all 273 paragraphs for irregular markup finds only `<br>` tags
everywhere except one: paragraph 181, the heading `b) THOMAS and Satoshi`, whose
final `i` sits in a bold tag of its own (`<b>b) THOMAS and Satosh</b><b>i</b>`).
It is the only split-tag paragraph in the document, and it falls on the heading
about the extra `I` that distinguishes "Satoshi" from "THOMAS". Being invisible
in rendered text it cannot be a hash-affecting edit, only a pointer. The edit it
points at was tested: capitalising it to `SatoshI`, in every combination with the
five malformed-capital words, 1,536 texts x 10 indices, 0 reach either escrow.

## Block 77 Stage One, reproduced end to end (2026-08-20)

Stage One is solved, and its exact serialization is now measured rather than
described. The missing byte was invisible in every rendered copy of Hal Finney's
post: bitcointalk's stored markup joins the post's trailer to the final
paragraph with a **single** `<br />`, not the double that separates paragraphs.

    <p>...I'm comfortable with my legacy.<br />[edited slightly]</p>

So the last paragraph is `That's my story. ... I'm comfortable with my
legacy.\n[edited slightly]` -- one line feed, inside the paragraph. Every
transcription from the rendered page either drops the trailer or promotes it to
a paragraph of its own, and both are wrong.

With that one character in place:

| | |
|---|---|
| Source | Hal Finney, "Bitcoin and me", bitcointalk topic 155054, 16 paragraphs |
| Trailer | `[edited slightly]` joined to paragraph 16 by a single LF |
| Keep-set | I, T, A, S, M (the letters of "Satoshi Nakamoto" pick the same 4 here) |
| Marked | paragraphs 1, 2, 3, 5 (0-based) -- initials F, F, W, W -- finals spell **STNM** |
| Rule | marked paragraph's first letter lowered, last letter raised |
| Separator | LF LF |
| MD5 | `9dd2efb9bc976c2095bd534d7b8d431c` |
| Derivation index | 0 |
| Address | `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` = the Stage One escrow |

Two independent oracles agree: the escrow address, and the `9dd` the winning
solver published in the Stage One thread ("Okay. I think solving 77 deserves a
celebration of sorts. Here you are: 9dd (copypasted)."). The MD5 begins 9dd.

This is the calibration the folder has been asserting from private research
without a reproduction. It now has one, and every convention in it is measured:
separator LF LF (again, against her own "13 10 13 10"), index 0, force rather
than toggle (they coincide here), and the trailer's single line feed.

### What it says about the Real Big Block

Applying the identical rule to the 273-paragraph chapter does not reach either
escrow at any keep-set:

| Keep-set | Paragraphs marked | md5 | index 0 |
|---|---|---|---|
| ITASM | 118 | `7a167cc62420...` | `1JUq82YNEwiKZ1mEdhPgcQFQcwGFdShSjT` |
| SATOSHI | 94 | `82dc13338ffe...` | `15kEcnyrY7giQSWqVpzz5vPxcG3qo5aF3F` |
| SATOSHINAKAMOTO | 86 | `3bca3b6eb417...` | `1CMSBRMbofkXQpnsQbhjmKz9qn47UXXJke` |

as expected: a keep-set cannot select a small set out of 273 paragraphs. But
Stage One shows that the keep-set was never what made the marked set
*recognisable* -- the **signature** was. The four marked paragraphs are the ones
whose last letters spell STNM.

That transfers without a scale problem, and it is a small search. Every
increasing set of chapter paragraphs whose final letters spell a candidate
signature:

| Signature | Candidate paragraph sets |
|---|---|
| stnm | 79,021 |
| nmst | 34,014 |
| tomi | 392 |
| ims | 254 |
| tom | 126 |
| hal, aoi, iam, second, thomas, finney, satoshi, nakamoto, satommi, grycoin, bitcoin | 0 (no such subsequence exists) |

113,807 sets in total, each one MD5 and one derivation under the certified rule.
`tools/sig.py` in the research scratch runs it; the result is recorded below when
it lands.

## The signature model, closed on both streams (2026-08-20)

Stage One's marked set is recognisable by its **signature**, not by its keep-set:
the four marked paragraphs are the ones whose last letters spell STNM. That
transfers to the chapter without a scale problem, and it is a small search.
Every increasing set of chapter paragraphs whose letters spell a candidate
signature was enumerated and run through the certified Stage One rule (first
letter lowered, last raised, LF LF, both escrows):

| Stream | Signatures with any subsequence | Sets | Result |
|---|---|---|---|
| Paragraph finals | stnm 79,021; nmst 34,014; tomi 392; ims 254; tom 126 | 113,807 | 0 |
| Paragraph initials | stnm 46; nmst 685; tom 367; ims 348; iam 969; aoi 3,045; tomi 3,998; ffww 3,462; nakamoto 8,120; thomas 9,945; satommi 15,840 | 46,825 | 0 |

160,632 paragraph sets, 0 reaching either escrow. The finals row is exhaustive in
a strong sense: `hal`, `aoi`, `iam`, `second`, `thomas`, `finney`, `satoshi`,
`nakamoto`, `halfinney`, `satommi`, `grycoin` and `bitcoin` have **zero**
subsequences in the chapter's final letters, so no paragraph set can spell them
there at all. Every signature the chapter's finals can physically support has
been tested.

## Block 2 inside the FFWW paragraphs, exhausted to six changes (2026-08-20)

Her selector marks Block 2's paragraphs {2,3,6,7} (initials F F W W, from the
literal letters of SATOSHI), and her rule keeps everything outside the marked
paragraphs unchanged, so every changed letter must lie inside those four. They
contain 96 word-boundary positions carrying a case effect. Every subset up to
size 6 -- 991,641,864 candidates -- was swept under her free 3c6 prefix:

| Half | Texts | Past 3c6 | Addresses derived (idx 0-1) | Result |
|---|---|---|---|---|
| anchors 0-7 | 408,089,334 | 100,003 | 200,006 | 0 |
| anchors 8-95 | 583,552,530 | 142,974 | 285,948 | 0 |

Prefix hits land at chance in both halves. So within the FFWW paragraphs, no
combination of up to six word-boundary case changes reaches the escrow at index
0 or 1. Block 2's answer therefore either changes a letter that is not at a word
boundary, or marks paragraphs other than the FFWW four, or uses a derivation
index above 1.

## The chapter, certified character by character (2026-08-20)

Wattpad's `data-p-id` attribute on each `<p>` element is the **MD5 of that
paragraph's canonical text**. It is published in the page source, one per
paragraph, and it converts the carrier from "probably right" to verified.

The discovery came from the genesis-block chapter, which prints a solution
string as its own paragraph:

    <p data-p-id="4241d2d0e352e5090381c69e408ca80d">1A1zP1eP5QGefi2DMPTfTL5SLmv <b>7</b> DivfNa</p>

and `md5("1A1zP1eP5QGefi2DMPTfTL5SLmv 7 DivfNa")` = `4241d2d0e352e509...`.

Checked against all 273 ids of the Real Big Block chapter, this settles two
serialization questions that no amount of reading could, and both had been
answered wrongly here:

| | Assumed | Measured |
|---|---|---|
| `<br>` inside a paragraph | one line feed | **no character at all** |
| A run of two spaces | two spaces (0x20 0x20) | **NBSP + space (0xa0 0x20)** |

Six paragraphs contain a `<br>` and five contain a doubled space, so eleven of
the 273 paragraphs were wrong in every sweep this folder has ever run against
the chapter, this session's included. The `<br>` error was invisible because no
`<br>` sits at a paragraph edge, so the paragraph-initial and paragraph-final
letter streams matched perfectly, and the 45,450-character figure recorded in
fact 5 was itself computed under the same wrong assumption -- two
independent-looking confirmations both inheriting one mistake.

With `<br>` dropped and doubled spaces stored as NBSP + space:

    272 of 273 paragraphs reproduce their published data-p-id exactly
    chapter text: 44,896 characters, 6 NBSP

The single exception is paragraph 77, `"What?"`, whose text is identical to
paragraph 33; Wattpad assigns distinct ids to duplicate paragraphs, so this is
an id-uniqueness artifact, not a content difference. **Every character of the
carrier is now confirmed against the platform's own hashes.**

Any future work on this block should start from that check. It costs one MD5 per
paragraph and it is the only way to know the bytes are right; the letter streams
and the total length both pass while the text is still wrong.

### Re-run on the certified carrier

The certified Stage One rule applied directly, all keep-sets, both separators,
indices 0-9, plus the unmodified chapter: no candidate reaches either escrow.
The signature searches of the previous section are being re-run against the
corrected bytes, since their earlier negatives were computed on the wrong text.

## Stage One's structure, transferred at Stage One's scale (2026-08-20)

Her rule marks 4 of Hal's 16 paragraphs. It cannot mark a small set out of 273,
which is why every keep-set fails on the whole chapter. But the chapter is not
one flat text: 28 bold headings divide it, and several of its sections are
Hal-post sized. Applying the keep-set inside each section gives, for each
section, a marked set of the right order.

One section reproduces Stage One's structure exactly:

| Section | Paragraphs | Keep-set | Marked | Their last letters |
|---|---|---|---|---|
| **1. My Identity** | 10 | SATOSHI | **4** (167, 168, 169, 170) | **stnm** |
| 3. Reverse Turing Test | 16 | SATOSHI | 4 (77, 80, 81, 86) | tntn |
| 2. Bitcoin With Two Changes | 14 | SATOSHI | 4 (115, 119, 127, 128) | seln |
| d) Outing himself as Satoshi | 31 | SATOSHI | 6 (225, 230-232, 234, 235) | estnmh |

A ten-paragraph section, the literal letters of SATOSHI as the keep-set, four
exceptions, and their final letters spelling the signature -- the same shape as
the Finney post, in the section that makes the identity claim. It is the
strongest structural echo the chapter contains.

It does not reach either escrow. Nor does any of the others, nor the chapter's
own verbatim quotation of Stage One's four marked paragraphs (230, 231, 232,
234), nor any of the three FFWW groups, alone or together.

### A carrier ambiguity this raised, and it is not settled

`data-p-id` proves what Wattpad *stores*. What she hashed was a copy out of the
*rendered* page, and a browser renders `<br>` as a line break. So there are two
live carriers, not one:

| | `<br>` | doubled space |
|---|---|---|
| Wattpad canonical (proven by the ids) | no character | NBSP + space |
| Browser copy (what she describes doing) | line feed | NBSP + space, or two spaces |

Four conventions in total. Everything in this section was run against all four,
plus both separators and three case operations, and the per-section sweep also
tried each section as a carrier in its own right, with and without its heading:

| Sweep | Candidates | Addresses | Result |
|---|---|---|---|
| Named structural sets (My Identity, Outing, FFWW groups, quoted Stage One block, and combinations) | 240 | 2,400 | 0 |
| Every section x 4 keep-sets x 4 carriers x 2 separators x 3 scopes | 1,488 | 8,928 | 0 |

Anyone running the exhaustive search should carry all four carrier conventions,
not one: `C(273,4)` x 4 conventions is 928 million derivations rather than 232
million.

## Second Life against Second, diffed by paragraph hash (2026-08-20)

The standalone "Second Life" part and the Real Big Block chapter share a long
passage, and because Wattpad publishes a `data-p-id` per paragraph the diff can
be done at hash level rather than by eye. Of the 17 overlapping paragraphs, 13
carry identical ids -- byte-identical text -- and 4 differ, plus one paragraph
present only in the chapter:

| Chapter | Second Life (earlier) | Chapter (later) |
|---|---|---|
| 14 | `"Still 21st Century".` | `"2020."` |
| 15 | `...Not even one hundred years have passed.` | `...Not even ten years have passed.` |
| 18 | `Third most popular name for Japanese girls right now."` | `A popular name for Japanese girls."` |
| 19 | *absent* | `I recognize the signs.` **inserted** |
| 24 | `...bore you with second rate quiz questions...` | `...third rate quiz questions...` |

Every edit is certified: the quoted Second Life text reproduces its own
published id exactly in all four cases, and the unchanged paragraphs match the
chapter's ids exactly.

`Still 21st Century` is the published solution of Grycoin chain Block 1 --
`md5` = `4c414876be9043da...`, matching the `4c4` she announced. So the earlier
version of this passage contained one of her own block answers verbatim, and she
replaced it with `"2020."` when the passage was folded into the chapter. She also
said of Block 1, "It is for 77, but you will not see it if you let a script solve
the block", which is consistent: a script that finds the hash never asks why that
phrase, and so never finds the version difference.

The standalone part also gives a third independent confirmation of the `<br>`
rule: its first paragraph is `<br>"Good morning, Tom."` and carries the same id
as the chapter's plain `"Good morning, Tom."`. A leading `<br>` changes nothing.

### What the edits are not

The five changed paragraphs are not the marked set. Every subset of
{14, 15, 18, 19, 24}, under all four carrier conventions, both separators and
three case operations -- 744 candidates, 7,440 derived addresses -- reaches
neither escrow. (This had been asserted earlier in discussion without being run;
it is now measured.)

Nor do the edit tokens themselves hash to any of her published prefixes. Every
old-side and new-side phrase, every pair of them across six joiners, and the
ordered concatenations of each side were checked against `d78c92f`, `f8e`, `1d`,
`3c6` and `4c4`: the only match is `Still 21st Century` to `4c4`, already known.
Ten candidates matched `1d`, which is 8 bits and expects nine by chance out of
that many.

What the edits do establish is provenance: the chapter is a revision of an
earlier published text, she edited it deliberately in five places, and one of
those places held a block answer she had already published. That is a strong
pointer that the two documents are meant to be compared. It is not yet a
selector.

## The second-letter reading, and what it does and does not explain (2026-08-20)

Of the chapter's malformed ordinary-word capitals, two share a construction the
third does not:

    V I rgin      anomalous capital at the SECOND letter, and it is I
    B I tcoin     anomalous capital at the SECOND letter, and it is I
    p p M         anomalous capital at the THIRD letter

Both second-letter cases sit inside part II, "Second Layer", and both fall after
the passage that says Grycoin is built "with two and only two changes", in a
section titled "2. Bitcoin With Two Changes" whose text then separates "One
change is that..." from "The other change is replay protection". Two changes,
announced twice, followed by exactly two conspicuous capitalization violations,
each at a second letter, each an I -- which is also the Roman numeral of the
part they sit in.

Read as an edit, this is dead: every casing variant of those two words, alone
and in combination with the other anomalies, was tested earlier (15,360
addresses, 0). Read as a *demonstration of an operation*, it survives that, and
it is the first clue in this folder that names an operation rather than a
position.

Tested as an operation:

| Marked set | Operation | Candidates | Addresses | Result |
|---|---|---|---|---|
| FFWW groups, My Identity, the quoted Stage One block, the Second Life edits, the two anomaly paragraphs, the whole Grycoin section, part II entire, all 273 | 2nd letter up; 1st down + 2nd up; 2nd letter toggled | 248 | 1,488 | 0 |
| Every word's second letter capitalized, whole chapter | global | 8 | 48 | 0 |
| Signature subsequence sets (stnm, nmst, tom, ims, ii in initials; tomi, ims, tom, ii in finals) | 2nd up; 1st down + 2nd up | 26,472 | 52,944 | 0 |

All across both `<br>` conventions and both separators.

So the second-letter operation is eliminated on every mark set this folder has
reason to prefer. What it leaves standing is the observation itself: if she
demonstrates an operation twice, in the part whose own numeral is II, right
after saying "two and only two changes", the demonstration is probably about
*something*. The unresolved question is what object the operation applies to,
and that is not the chapter's paragraphs under any selector tried here.

## Carrier bytes certified, and the Stage-One predicate exhausted on Second (2026-08-23)

The Wattpad page source was recovered with its `data-p-id` attributes intact.
Each `data-p-id` is Wattpad's own MD5 of that paragraph's canonical text. The
273-paragraph carrier used throughout this folder reproduces **272 of 273**
exactly; the one exception is `p77 = "What?"`, byte-identical to `p33 = "What?"`
-- MD5 of that text equals p33's stored id, and p77's differs only because
Wattpad salts the id of a duplicate paragraph. So the per-paragraph carrier
bytes are not in question: they are Wattpad's canonical bytes. The only open
byte variable is the inter-paragraph separator, and the "get the 2019 rendered
copy" lead (leads.md #1) is closed -- the rendered source matches what is
already hashed.

The author's live-rehash statement ("two line breaks between each", recorded as
"13 10 13 10") makes **CRLF CRLF** the candidate separator for the funded
escrow. Every Stage-Two negative in this folder had used LF LF only. Re-run
under CRLF and CRLF CRLF:

| Test | Separators | Result |
|---|---|---|
| Full contiguous-span sweep, ITASM-exception edge rule, idx0 | CRLF, CRLF CRLF | 0 (each 37,401 spans) |
| Corrected sweep with **`swapcase`** first-letter op (fixes lowercase `a)`-`f)` headings), all spans | LF LF and CRLF CRLF x {br=nothing, br=LF} | 0 (all 4 passes, 37,401 spans each) |
| Keepset sweep -- ITASM, STNM, ISTNM, NMST, SATOSHI, THOMAS, HALFINNEY, AOI, SECOND, IAMSATOSHI, IM, MII, and 9 more | LF LF, CRLF CRLF, idx 0-59 | 0 |

The keepset diagnostic is the point: on Hal's 16-paragraph post ITASM marks
exactly 4 paragraphs (FFWW). On the 273-paragraph chapter every candidate
keepset marks **118-223** paragraphs. The paragraph-initial mechanism is not
scale-invariant, so no keepset reproduces the Stage-One shape on whole-Second,
and none reaches either escrow.

The pre-existing capitalization anomalies (ppM idx72, VIrgin idx127, BItcoin
idx135 -- reading **M I I**, which Section III defines as Satoshi's "extra I,
missing M" and the "II" of Harold Thomas Finney II) were tested both as payload
and as selector:

| Reading | Configs | Result |
|---|---|---|
| Normalize ppM/VIrgin/BItcoin (5 subsets A-E) | 20 x {2 br, 2 sep} x idx 0-7,76 x both escrows | 0 |
| Anomaly paragraphs {72,127,135}, idx95, quartet as marked, edge-op | 28 | 0 |

The "I am" reading (unique `IM` initial adjacency at idx162-163, "III. Second
Identity"/"1. My Identity", followed by literal "I am" at 164/166, mirroring
bcflick's `In/Basically/Mike/I'm` = I B M then "I'm"): recasing "I am" at the
opening/in-section/chapter-wide occurrences, plus combined "I am STNM" on the
Identity section, 64 configs across both serializations and both escrows -- 0.

The Satoshi-Mystery chapter (its own published per-paragraph MD5 oracle
reproduced byte-for-byte; `cc9485a` = MD5("Hal Finney") = its answer) is a
Hal-post-shaped carrier with a single non-ITASM initial (Y). Exhaustive over
all 2^11 whole-paragraph exception subsets x 4 joins x trailing-strip, idx0,
plus the justified single-Y reading at idx 0-29 -- 0.

### The derivation was reopened and largely closed

Grycoin Block 2's "change only the capitalization" is stated to bind **both**
stages of block 77 (the "copy paste" in the comments means *preserve the
carrier verbatim*, not remove words; para 266's "remove a couple of words" is
semantic interpretation of Hal's prose, not the serialization rule). So the
operation is capitalization-only. That leaves the solution-text -> key
derivation as the assumption to test independently, since the author separated
"which capitalization changes" (which she knew) from "how to claim the prize"
(which she said she did not).

`data/pipeline-stages.json` and `tools/oracle.py --selftest` certify
MD5 -> BIP39 -> BIP44 `m/44'/0'/0'/0/i` against the author's **own** published
vector (entropy `2941774a...` -> WIF at idx1), and blocks-structure records the
whole ~90-block series using it. Tested anyway, on the 8-9 strongest
capitalization candidates:

| Derivation family | Coverage | Result |
|---|---|---|
| 19 text->key methods: BIP44 idx0-5, raw-MD5-key (comp/uncomp), MD5x2, SHA256 brainwallet (comp/uncomp), SHA256(md5hex), SHA256->BIP39, double-SHA | 9 candidates x 2 encodings x both escrows | 0 |
| BIP44 index scan | 8 candidates x 2 encodings x idx **0-5000** x both escrows | 0 |

If any of these candidate texts were correct, one of ~40,000 (text x method x
index) checks should have hit. The derivation is therefore not the (sole)
broken link -- consistent with it being the most-certified assumption we have.
The remaining open variable is the marking rule / carrier scope, and the
highest-value missing input is a primary-source statement of the Stage-Two
scope within "Second" (a start/end, a single section) -- the r/Grycoin threads
are the source and were not reachable from this environment.

## No Stage-2 prefix, the p77 stale-id anomaly, and cleczc's un-pinnable filter (2026-08-23, cont.)

**No MD5 prefix exists for either RBB stage.** Stage 1: "no first digits of MD5
hash, nothing." Stage 2: none published (this file, above). Every prefix on
record -- `f8e`/`1d` (Block 76), `3c6`/`7759227` (Grycoin Block 2 / cleczc),
`9dd` (Stage One's *already-solved* solution) -- belongs to another block.
There is no free filter for the live escrow, which is why 2-to-4 marked letters
among ~37,000 positions cannot be brute-forced.

**p77 is a stale pre-edit id, not a dedup salt.** "What?" is the only duplicated
text in all 273 paragraphs, so the salt theory had one data point and is now
retracted. `8b71bade` is not MD5 of "What?" nor of ~30,000 counter/salt forms
(`"What?"+n`, char salts, nested hashes, HTML-element forms) nor of ~19
plausible short originals. Since `data-p-id` is provably content-derived (exact
MD5 for 272/273), the most consistent reading is that Wattpad assigns the id at
paragraph creation and it persists across edits: `8b71bade` is the MD5 of an
*original* line later replaced with "What?", sitting between p76 ("two ways...
reverse Turing test") and p78 ("Of course you know what a Turing test is"). That
original is a candidate marked paragraph, recoverable only from a pre-edit
snapshot (Wayback/Wattpad revision), all egress-blocked from this environment.
Any candidate can be verified instantly: MD5 must equal `8b71bade9685...`.

**cleczc cannot be pinned by its own filter.** The 10-paragraph Grycoin Block 2
example (base `7759227`, solved form `3c6`) was attacked as a calibration
problem, since the author says its marks follow from the Stage-One solution:

| Operation | Coverage | Hits 3c6 |
|---|---|---|
| Paragraph edge-flip (swapcase first + upper last), all marked-sets | 2^10 x 2 ops | 0 |
| ITASM-complement marked paragraphs {2,3,5,6,7}, edge-flip | (in the above) | 0 |
| Sentence edge-flip (both / first-only), all subsets | 2^15 x 2 | ~8 each = chance rate |
| Sentence raise-last-only, all subsets | 2^15 | 0 |
| Aoi's literal in-text example: "I"->"i" + "himself"->"himselF" | 1 | 0 |

The in-text "I"/"himself" changes are framed hypothetically ("if you thought the
I was one of them") and do not hit the filter -- they teach the mechanism, not
the marks. A 12-bit prefix over 32,768 candidates yields chance-rate hits with
no way to distinguish the intended set, matching the earlier large 3c6 sweeps.
cleczc's true marked set is therefore not recoverable from the text plus filter;
it needs the published winning solution from its Reddit thread. That solved
capitalization -- 10 paragraphs, answer known -- is the cleanest available
Rosetta stone for the Stage-Two marking rule, and remains the gating input.

## Bounded deterministic marked-set search, exhausted to subset size 6 (2026-08-23, cont.)

The "deliberate anomaly" features (capital-final endings [9], trailing spaces
[13], internal `<br>` [10], question endings [13], Hal block [230-234]) were
run as a bounded, ordered search rather than one feature at a time:

| Step | Candidate sets | Transforms | Result |
|---|---|---|---|
| Feature intersections k=2,3 | 3 non-empty | 6 variants x 2 seps x idx0-5 | 0 |
| Neighbor expansions of the 9 (i-1, i+1, both) | ~28 sets | same | 0 |
| Capital-final 9 as marked set | 1 | lower-last / swap-first / edge x 3 enc x idx0-20 | 0 |
| **Pool brute**: all size 4-6 subsets of the 18-index pool {127,138,188,189,193,206,208,210,212,228,230-234,236,238,258} | 30,192 subsets | 6 transform variants (last-token-upper/title, last-letter-lower, first-alpha-upper/lower, first+last-token-upper), CRLF CRLF, both escrows, idx0 | **0 (181,152 tested)** |

The capital-final 9 were verified to be content-incidental: every one ends on an
all-caps acronym or single-letter answer (TOM, II, IBM, II, S, WW, STNM, STNM,
C), all inside Part III's "2. The Satoshi Code" explanation, and their finals
spell `MIMISWMMC` (no signature). They are not an applied transform and cannot
be "raised" (already capital).

This closes the small-deterministic-marked-set search over the chapter's
computable anomalies. Combined with every prior structural elimination, the
conclusion is firm and matches the 2026-08-19 finding: the Stage-Two marks are
not singled out by any feature of the carrier. The next input must be external
-- the solved cleczc capitalization or the ca6jxv winning comment -- not another
structural sweep.
