# Mechanism, in full

## The site

The puzzle lives on an approximately 70-page Wix site, almost all of it password-protected
page by page. The entry page (`/treasure-hunt`) carries an image whose EXIF metadata encodes
GPS coordinates; entering the latitude and then the longitude as consecutive page passwords
opens a compass page, which displays four branch passwords in clear text: `north64`,
`south64`, `east64`, and `west64`. From there the site forks into four branches.

The entry chain, as re-walked on the live site on 2026-09-03:

| Step | Page asks | Password |
|---|---|---|
| 1 | the EXIF latitude | `27756932` |
| 2 | the EXIF longitude | `73511573` |
| 3 | "Who is she?" | `amphitrite` |
| 4 | the compass, which prints the four branch passwords | `north64` / `south64` / `east64` / `west64` |

Step 3 is the answer to the entry line "I Be The Ruler of the Seven Seas": Amphitrite is
Poseidon's wife. It is accepted in lowercase, which is why the case rule below is stated per
page rather than per site.

The branch chains, in the order their passwords are entered:

| Branch | Passwords, entry to lock |
|---|---|
| South | `south64`, `electricfeel64`, `Gilligan`, `Jonas`, `Thurston`, `Lovey`, `Ginger`, then the locked `b3vye` |
| East | `east64`, `east64`, `witchoftheeast`, `albatross`, then `semaphore` / `20000leagues` / `youshallpass47` on the middle pages, then the locked `c2ozw` |
| West | `west64`, then the locked `wt1jy` |
| North | `north64`, then a whale-themed chain ending on a static "coming soon" page |

`witchoftheeast` sits on an open East page headed "You find a message in a bottle... Could it
be from her?" ("her" being Amphitrite, from the entry line). That page prints the password in
clear under a "Continue Eastward" button, and it is also the first confirmed word carrier of
this hunt: see the next section.

`electricfeel64` and `youshallpass47` are the two passwords that show the author's habit
plainly: the first is a pun on an electric eel, the second inverts Gandalf's "you shall not
pass" because the reader is in fact passing. Both carry a numeric suffix taken from a number
printed on the page itself. That habit is the reason the three remaining answers are read as
puns or planted details rather than as dictionary terms.

Everything up to and including the branch fork is solved: I hold every password from the
entry page through the compass page and through every page each branch passes before its
final locked gate.

## The four branches

North is a decorative dead end: its chain of pages (ending in a "coming soon" page) carries
none of the 12 words. I confirmed this by reading the full content of every page on the
branch; no word-bearing artifact of any kind is present.

West, East, and South each end in one password-gated page I have not opened. I call these
the three insight locks. Opening any of them requires guessing a short, unenumerable string
that answers the riddle text quoted in [clues/author-posts.md](../clues/author-posts.md), not
decoding anything hidden in an image or audio file: no steganographic payload was found on
any page along the way (see analysis/tested.md).

The South branch is a chain of six pages named after five Gilligan's Island castaways in
sequence (Gilligan, the Skipper, Thurston Howell III, Lovey Howell, Ginger), each password a
single Title Case name, before ending on a sixth page titled "Name 6" that asks for the
sixth castaway, the Professor. This last page is the one I have not opened; solving it opens
the entire South branch's downstream chain (a further set of "escape the island" pages) in
one step, since password to `b3vye` is also the key to everything after it.

## Case sensitivity and format, established by direct test

Passwords on this site are case sensitive. I confirmed this on two already-open gates on the
South chain: the page password `Gilligan` succeeds where `gilligan` and `GILLIGAN` both fail,
and `Ginger` succeeds where `ginger` and `GINGER` both fail. Combined with the passwords
already known for every other open gate, the format of the three remaining locks is:

- South (`b3vye`): Title Case, a single token, no digits, no spaces (matches the naming
  pattern of the five prior South pages).
- West (`wt1jy`) and East (`c2ozw`): lowercase, a single token with no spaces (matches every
  other open West/East page password, e.g. `albatross`, `semaphore`, `20000leagues`).

These are per-branch observations, not a site-wide rule. The entry chain's `amphitrite` is
lowercase while the South chain's `Gilligan` and `Ginger` are Title Case, so the author set
the case page by page. A candidate that fits the reading but fails in the branch's usual case
is worth one retry in the other case before it is written off.

No password anywhere on the site I have opened carries a numeric suffix that is not directly
derivable from the page's own content (a number visible in an image on that same page); no
guess should add an arbitrary digit string.

## The 12-word carrier channels

The site's predecessor, "Born to Be Wild" (2021, Apollo/moon theme), was solved and swept by
an unidentified third party; I used its known solution purely as a template for how this
author hides seed words, not as part of the live puzzle. Its seed was
`fortune all man kind one giant step into digital tomorrow virtual moon` with passphrase
`supernova`, assembled from 7 carrier channels. Mapping the same 7 channels onto this hunt:

| # | words | Hunt #1 channel | Hunt #2 equivalent | status here |
|---|---|---|---|---|
| 1 | word 1 | bytes appended after the cover image's EOF marker | Glimmer cover art | refuted: every Hunt #2 cover image I found (Bandcamp, Apple Music, Deezer, ToneDen, and the site's own PNG) is clean; a collage image that looked like a second Hunt #2 cover turned out to be a Hunt #1 teaser predating this hunt |
| 2-4 | words 2-4 | museum gold frames pictured in the book/site | not located outside a gated page | not found on any open page |
| 5-7 | words 5-7 | a forced cultural quotation naming a BIP39 word | pop-culture reference on the East branch | behind the locked `c2ozw` gate |
| 8-9 | words 8-9 | Morse code in an alternate audio mix | West branch "computer" theme or a hypothetical alternate mix | refuted for the public master: the only public 48kHz/24-bit Glimmer audio matches its own official master with no Morse signal; no alternate mix has been found distributed anywhere |
| 10 | word 10 | binary encoding | not located | the only binary string found anywhere on the site is an EXIF comment reading "nope lol", which does not decode to anything |
| 11-12 | words 11-12 | a "future song" ticket prop | inherited endgame page, already open | present, but this is Hunt #1's own endgame carried over, already read, and not new information |
| passphrase | "in the song" | the closing track's title | the Glimmer track title or lyric | not testable without the 12 words |

That table is the Hunt #1 template, and the live site has now refuted it as a model for this
hunt. The real channel is far plainer: a branch page prints the seed words directly, as small
numbered tags, each tag carrying the word's position in the 12.

The message-in-a-bottle page on the East branch, which is open and needs no lock, prints five
of them:

| Position | Word |
|---|---|
| 1 | when |
| 2 | you |
| 3 | depart |
| 4 | find |
| 5 | mystery |

Three consequences. First, the claim that all 12 words sit behind the three locks is wrong:
at least 5 are on an open page, and the locks hold the rest rather than the whole seed.
Second, the circulating fragment is genuine at least through word 5, in that order, which is
why it is now worth chasing rather than dismissing. Third, words 6 to 12 should be looked for
in the same visual form, numbered tags on a page, rather than as a steganographic payload in
an image or an audio file. Every negative in analysis/tested.md that scanned for a hidden
payload was looking for the wrong kind of thing.

The circulating fragment reads "when you depart find mystery hunt gather whale blood ...
virtual moon". Its first five words are now confirmed by the page above, so its tail is worth
taking seriously too. The tail is still not confirmed, and does not derive the wallet: `tools/seedsearch.py` swept every BIP39 word into every position of those 11
words, kept the 1,582 checksum-valid mnemonics, and tested them against 28 candidate
passphrases, and then again over the seven tail positions against 79 passphrases drawn from
the Glimmer lyric, the band's other track titles, and the site's own vocabulary, with no
match either time (see analysis/tested.md). Since words 1 to 5 are now certain, the error is
in words 6 to 12 or in the passphrase, not at the start. "virtual" and "moon" are the last
two words of Hunt #1's own seed, so the tail is the part most likely to be inherited noise.
Treat words 6 to 12 as unknown and look for the pages that print them.
