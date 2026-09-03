# Leads, in full

Lead 5 is the one to do first: it is the only one that is legwork rather than
guesswork, and the page that prompted it proves the words are printed in the open.

## 1. West lock (`wt1jy`): read "unbridaled" as a pointer to The Princess Bride

The riddle's misspelling is the planted detail, and it spells out where the answer comes
from: "unbridaled" carries "bridal", and Ross Ulbricht ran Silk Road under the alias Dread
Pirate Roberts, a name taken from The Princess Bride. The point of that character in the
film is that the name is not one man: it is handed on from holder to holder, so whoever
wears it is the Dread Pirate Roberts. That is the exact shape of the riddle, which lists a
real pirate (Blackbeard), the founder of Napster (Shawn Fanning), the drummer who sued the
file sharers (Lars Ulrich), Ulbricht, and the two Pirate Bay founders, and then asks the
reader which of them they are. The answer the riddle is fishing for is the name they all
share, not any one of their names.

Candidates in the format this branch already uses (lowercase, one token, no digits), best
first: `dreadpirateroberts`, `roberts`, `westley`, `princessbride`, `cummerbund` (the
predecessor Westley names when he explains the succession), `asyouwish`.

Confirmed if one of them opens `wt1jy`. Killed if all six fail, because this reading
predicts a name out of that one film and nothing else. Cost: minutes.

Untested. I wrote this reading from the riddle text; no candidate here has been submitted to
the site yet, so nothing in this section is a negative.

## 2. East lock (`c2ozw`): answer the second half of the Gandalf line, not the first

An earlier page on this branch carries `youshallpass47`, which fixes the branch's reference.
The locked page does not only ask whether this is the end: it says images start flashing
before the reader's eyes and asks whether they are a life passing or hallucinations. In the
scene being quoted, Gandalf answers Pippin's "I didn't think it would end this way" in two
parts, and the riddle asks about both of them. The first part is the refusal ("End? No"),
which is where every candidate tried so far has gone: `gandalfthewhite`, `theturnofthetide`,
`flyyoufools`, `mithrandir`, `endno`. The second part is the vision itself, which is what the
riddle's "images start flashing before your eyes" is pointing at:

> The grey rain-curtain of this world rolls back, and all turns to silver glass, and then you
> see it. White shores, and beyond, a far green country under a swift sunrise.

That half is untried. Candidates, lowercase single tokens, best first: `whiteshores`,
`silverglass`, `fargreencountry`, `swiftsunrise`, `greyraincurtain`.

There is a second family, and it now has harder evidence behind it than the first. An open
page earlier on this same branch prints the password `witchoftheeast` in clear, which puts
The Wizard of Oz on the East branch as a fact rather than as a reading. Oz answers the
riddle's actual question better than Tolkien does: the riddle asks whether the images are a
life passing or hallucinations, and the ending of Oz is precisely the argument over whether
what Dorothy saw was real or a dream. On that reading the answer to "is this the end?" is her
line on waking: `theresnoplacelikehome`, `noplacelikehome`, and then `kansas`, `dorothy`,
`overtherainbow`, `emeraldcity`, `toto`, `yellowbrickroad`.

Try the Oz family first. Confirmed if one opens `c2ozw`. Cost: minutes. Untested, same caveat
as lead 1.

## 3. South lock (`b3vye`): "Name 6" may want the first-season credit, not a character name

The five pages before the lock are passwords `Gilligan`, `Jonas`, `Thurston`, `Lovey`,
`Ginger`: the castaways in the order the show's own opening credits use, by given name, with
Ginger fifth because Tina Louise's contract put her last in the titles. Castaway six is the
Professor, and the riddle's "the other guy" separates him from Mary Ann. But the show's
enumerable canon of names for him is exhausted with no hit, and `Roy`, `Roy Hinkley`,
`Professor` and `Russell` are all reported rejected.

What has not been tried is the thing the show itself called him. For the whole first season
the last line of the theme song did not name the Professor or Mary Ann: it sang "and the
rest", and photos and credits for Russell Johnson and Dawn Wells were left out of the
opening. Bob Denver forced the change for season two. So the sixth castaway, in the version
of the show being quoted, has no name: he is "the rest". That reading also fits the author's
habit of hiding the answer in a deliberate detail rather than in a longer list of names.

Candidates in the branch's Title Case format: `TheRest`, `Rest`, `AndTheRest`; and the name
forms in the branch's own given-name pattern that are not on the rejected list: `Hinkley`,
`RoyHinkley`, `RoyHinkleyJr`.

This lock is still worth the most: its password also opens the whole downstream South chain
in one step. Confirmed if one candidate opens `b3vye`. Cost: minutes. Untested.

## 4. Reverse image search the `LifeFlashBeforeEyes.mp4` clip stills

This video sits on `pxsqo`, the page immediately before the locked `c2ozw` gate, and shows a
sequence of memory-like clips: a couple pointing at the sky, a woman in a white dress on a
dune, yellow flowers, a campsite, pizza on a boat. If any of these frames is a still from an
identifiable film or music video, that title is a strong candidate for the East password.
This has not been attempted; it needs a reverse image search tool and costs on the order of
an hour. Note that lead 2 predicts the clip is set dressing for the Gandalf vision rather
than a quotation in its own right, so a hit on lead 2 kills this one.

## 5. Re-walk every open page looking for numbered word tags, North first

This is now the highest-value lead of the five, and it is ordinary work rather than an
insight problem. The East branch's message-in-a-bottle page prints seed words 1 to 5 as small
numbered tags in plain sight (see analysis/mechanism.md). That is the hunt's word channel: not
bytes after an image's EOF marker, not Morse in an alternate mix, just words printed on a
page with their position next to them. Words 6 to 12 are very likely printed the same way,
and the search for them so far was looking for hidden payloads instead.

North first, for two reasons. It is the branch written off as carrying none of the 12 words,
and the circulating fragment's tail contains "whale", which is the North branch's own theme.
If a numbered tag turns up anywhere on North, the dead-end finding in analysis/tested.md is
wrong and the branch is a carrier like the others.

Confirmed or killed by re-reading every open page on all four branches for numbered tags;
cost: an hour or two, no new insight required.

## External help

I have not contacted the band or its community about this puzzle. The site's own "get hints"
mechanism only covers the first 3 introductory steps (the EXIF coordinates and the compass),
all of which are already solved; it does not reach the 3 insight locks, so it offers no lever
here even if used.
