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
