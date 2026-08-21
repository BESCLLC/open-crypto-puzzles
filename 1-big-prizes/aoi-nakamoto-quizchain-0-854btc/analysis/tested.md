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
