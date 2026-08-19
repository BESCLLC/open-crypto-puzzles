# Session findings: exact bytes, an edited chapter version, and the 2-hop chain (2026-08-19)

Independent re-derivation that converges with `tested.md`/`leads.md` and pins
three things those files left open. All derivations use the certified
MD5 -> BIP39 -> BIP44 `m/44'/0'/0'/0/i` pipeline (verified against Block 77
Stage One -> `19TbyN5...` and Grycoin Block 2 below).

## 1. The 6 "invisible items" are NBSP+space (`\xa0\x20`), pinned

`tested.md` lists "the 6 non-breaking spaces kept, spaced or dropped" as an open
byte question. Fetched byte-for-byte from the storytext API, the 6 spots are
**`\xa0\x20`** (a non-breaking space *followed by* a regular space), not a
double regular space and not `\x20\xa0`. Locations (0-indexed `<p>` from the
"Second" title): paragraphs 89, 124, 125, 195, 256. The chapter is otherwise
straight-quote ASCII, 273 `<p>` paragraphs, 10 `<br>`, 13 paragraphs carrying a
trailing space.

## 2. A second, edited version of the chapter exists (different p-ids)

The storytext currently served has `"2020."`, `"...ten years..."`,
`"A popular name for Japanese girls."`, `"third rate quiz questions"`, and no
`<br>` before `"Good morning, Tom."`. A separately-circulated version replaces
those paragraphs (with *new* `data-p-id`s, so they are distinct objects):

| p-id (served) | served text | edited version |
|---|---|---|
| 386883cd... | `"2020."` | `"Still 21st Century".` (d1607e3b...) |
| d9e26324... | `...Not even ten years...` | `...Not even one hundred years...` (158f37ff...) |
| 7b809e65... | `A popular name for Japanese girls.` | `Third most popular name for Japanese girls right now.` (e689f538...) |
| 165d0210... | `third rate quiz questions ... for the next ten years` | `second rate quiz questions ... over the next ten years` (2a4b1682...) |
| ae28710b... | `"Good morning, Tom."` | `<br>"Good morning, Tom."` (leading `<br>` added) |

Which version the live escrow (`14zMkTga...`) hashes is unresolved; both were
tested (section 4). The edited set matches the author's "21st century" phrasing
recorded elsewhere and is the more likely 2019-07-30 rehash text.

## 3. The 2-hop self-chain is real (Grycoin "Big Block 2")

Grycoin Block 2's escrow `13qUHVzMYAneyyBGYvEey4SHy2iMSz3Jzh` is reached from the
published solution string `"BaSCifCatfAaa1i"Metamon` (leading quote literal) by a
**two-hop chain**, not a direct derivation:

    solution -> MD5 (2941774a...) -> BIP39 -> index 1 WIF (L5Z66q...)
    -> MD5(that WIF) (7b44cc...) -> BIP39 -> index 0 -> 13qUHVz...  [reproduced]

This is the class of "tricky bits" puzzleponky referenced and the author said she
did not know. It is the concrete candidate mechanism for the Real Big Block's
"how to claim" step, distinct from chaining the *stage-1* key (which is ruled
out).

## 4. What still returns 0 (both escrows, indices 0-7)

On both chapter versions, both separators (CRLFCRLF, LFLF), and `<br>` as
{LF, CRLF, empty, space}: nothing changed / cluster-1 / 3 clean FFWW clusters /
4 FFWW groups / all-non-ITASM, each tested **direct** and through the 2-hop chain
(intermediate index 0-7 -> MD5(WIF) -> final index 0-3). 3,200 derivations, 0.

Block 2 (Grycoin format demo, escrow `1tzieU...`, free `3c6` filter) calibrated
byte-exact: unmodified text -> `7759227d7406...` under **LF LF** (matches the
author's stated "7759227, three 7s"). Its solved version is not reproduced by
capitalizing any <=3 lowercase letters anywhere (268M candidates, 65k passed
`3c6`, 0 at the escrow) nor by any first-lower/last-upper subset of its 5
non-ITASM paragraphs (0 even at the `3c6` filter). Consistent with `tested.md`:
the marked letters are mid-word and method-chosen, not brute-forceable.

## Conclusion (unchanged from the ledger, now with the bytes and chain pinned)

The transform is per-letter capitalization; the specific letters are the gating
information and were **never published** (puzzleponky solved Stage One but wrote
"I will wait before revealing the full solution" and did not; the author states
she does not know them). Remaining exhaustive step for a GPU: 2-letter
capitalizations of the edited chapter under CRLFCRLF at index 0, direct and via
the 2-hop chain, with the "7th key has three 7s" cross-check as a secondary
witness.
