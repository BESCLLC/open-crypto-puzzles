# Leads, in full

## 1. Retry the West lock (`wt1jy`) in Title Case

The puzzle-wide "always lowercase" assumption is refuted (see analysis/tested.md): the site
is case sensitive, and the South branch's passwords are Title Case. About 1,560 of the
roughly 2,100 West candidates tried so far were submitted almost entirely in lowercase, on
the strength of that now-refuted assumption. The Title Case form of the same candidate list
has not been meaningfully tried. This costs minutes: it is a re-submission of an
already-generated word list with the case changed, not new research. Confirmed if any
candidate opens the page; there is no clean way to kill this lead short of trying it, since
the case question was never actually tested on this specific gate.

## 2. Retry the East lock (`c2ozw`) on the exact Gandalf "does not end here" phrasing

The East riddle chain traces a "Rime of the Ancient Mariner" retelling crossed with a
Fellowship of the Ring beat: the semaphore-decoded password on an earlier page,
`youshallpass47`, is a direct reference to Gandalf at the bridge of Khazad-dum, and the
locked page's riddle text ends on "is this the end?", which matches Pippin's line to Gandalf
after his fall and return, the well known film reply beginning "End? No,...doesn't end
here." The exact phrasing of that line as a password has not been tried; variants that were
tried and failed are
`gandalfthewhite`, `theturnofthetide`, `flyyoufools`, `mithrandir`, and `endno`. Costs
minutes.

## 3. Reverse image search the `LifeFlashBeforeEyes.mp4` clip stills

This video sits on `pxsqo`, the page immediately before the locked `c2ozw` gate, and shows a
sequence of memory-like clips: a couple pointing at the sky, a woman in a white dress on a
dune, yellow flowers, a campsite, pizza on a boat. If any of these frames is a still from an
identifiable film or music video, that title is a strong candidate for the East password.
This has not been attempted; it needs a reverse image search tool and costs on the order of
an hour.

## 4. Treat the South lock (`b3vye`) as the branch's master key, with a fresh reading of its pun

Opening `b3vye` is worth more than opening West or East, since its password also opens the
entire downstream South chain (a further "escape the island" sequence of pages) in one step.
The full enumerable Gilligan's Island canon (radio pilot, opening and closing credits, reunion
films, animated spinoffs, comics) has been checked with no hit, so the answer is more likely
an off-canon play on the page's own slug,
`havingfunwiththeurl-ilovedthisshowasakid` ("having fun with the url, I loved this show as a
kid"), possibly following the same style of planted, deliberate detail the author used on the
West riddle (the misspelling "unbridaled"). This is the highest-value lead but has no bounded
cost: it needs a new interpretation of the pun, not a longer list of candidates. A community
Reddit thread on this hunt (88 comments) contains one reader's guess ("use a different
title"), explicitly not an author-confirmed answer, and it did not lead anywhere when tried.

## 5. Exhaust any partial reconstruction of the seed before trusting it

A reader supplied a 12-word reconstruction with 11 slots filled and one empty, with no stated
provenance. The words are not recorded in this repository: nothing corroborates them, and an
11 of 12 reconstruction published against a live escrow mostly helps a sniper.

The method is worth keeping even though that particular fragment did not pay out. One unknown
slot is bounded where the three insight locks are not: only the checksum-closing candidates
for the gap are derivable at all (147 of 2048 in this case), so the gap costs seconds and the
passphrase is the entire real cost. `tools/search_missing_word.py` automates it. 155,232
(word, passphrase) pairs were checked with 0 hits; see
[word10-reconstruction.md](word10-reconstruction.md) for the families covered and the oracle
certification behind the negative.

Confirmed if any candidate reaches an oracle MATCH. A no-hit result confirms nothing either
way about the words, since a passphrase outside the list explains it equally well. It supplies
no password for any gate, so it does not displace leads 1 through 4.

## External help

I have not contacted the band or its community about this puzzle. The site's own "get hints"
mechanism only covers the first 3 introductory steps (the EXIF coordinates and the compass),
all of which are already solved; it does not reach the 3 insight locks, so it offers no
lever here even if used.
