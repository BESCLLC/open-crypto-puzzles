# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the
ranking.

## 0. The video's own tags, and the substring rule, both confirmed from source

Re-reading the challenge video's title and description in full, against the
blog post in full, settles three things that reorder everything below. All
three come from the author's own published wording, not from inference.

**The video has tags, and he names them as a hiding place.** The description
sets out the rules: "12 wallet seed words- 6 are hidden in this video
(description, tags, title, video basically could be anywhere in this video)
6.words are hidden in original post." The word "tags" is his. The blog post's
tags are where `fork` sat unread for 6 years; the video's tags have never been
read at all. They are not visible on the page, they live in the HTML
`meta name="keywords"` element, which is exactly why the blog ones were missed.
This is the single highest-value unexamined surface in the puzzle and it costs
one page-source view, no compute.

**The substring rule is confirmed, and it points at a specific word.** The
planted video sentence, quoted from the description in full:

> Don't expect anything easy there will be dark fog on the lake. Also It is not
> impossible.

The author, asked whether a list word could hide inside a longer written word,
said yes and offered "possible" inside its own negation, formed with the prefix
"im-", as his own example. That was recorded here as an unconfirmed mechanism.
It is not: he was describing this sentence. `possible` is a BIP39 word and it is
written inside `impossible` in his own planted text. `also`, in the same
sentence, is a BIP39 word standing on its own. Neither has appeared in any
sweep in `analysis/tested.md`.

Note what hid this. The second sentence never appears in `clues/author-posts.md`;
it is paraphrased there as "a short assurance that the challenge can, in fact,
be solved". The paraphrase exists because this repository's own style check
forbids the word, and the check made no exception for quoted source text. A
rule about how I write suppressed what the author wrote, and what it suppressed
is a candidate seed word. `tools/validate.py` now exempts blockquotes and
backticked spans for that reason.

**The word budget is per source, not per planted sentence.** Both texts say the
same thing: 6 words "in this video ... basically could be anywhere in this
video", and 6 "in this Post". Every sweep so far drew the pool from the 5
absurd sentences plus a few metadata words, on the assumption that the absurd
sentences carry the whole payload. `fork` already disproved that assumption
once. The post alone contains 89 BIP39-valid words; the video title and
description contain 37.

Two corrections to the pools used in the sweeps below: `top` was swept as a
video-side metadata word, but it appears in the post ("top ten altcoins"), not
in the video at all; and `finish` reaches the pool only by stemming the
description's "finished".

Ranked consequence. Read the video tags first, since they are free. Then the
cheapest sweep that contains new information is the planted-sentence pools plus
`also` and `possible`: 1,365 video subsets by 364 post subsets, 22,537,569,600
derivations over both water branches, about 8 hours on one rented GPU. That is
a smaller space than lead 1 below and it tests 2 words that lead 1 does not
contain.

What would confirm it: a match. What would kill it: exhaustion with 0 match,
under the same witness protocol as every prior sweep.

## 1. Extend the swept word pool with connecting words (liaisons)

Every completed sweep (`analysis/tested.md`) draws its non-anchor words from
full words in the 5 planted sentences and confirmed metadata (tags, title,
hook line). None of them include short connecting words from the same
sentences: prepositions, articles, and conjunctions such as "there", "will",
"also", "you", "more", "can", "then" (video side) or "only", "because",
"there", "like" (post side). These words are cheap to add: the private
research's own P2 estimate, before the metadata extension, priced this
addition at 15/14 words per side, 1.36x10^10 derivations, about 3.8 hours on
one GPU. Extending the already-metadata-inclusive R1 pool the same way is a
comparable-sized addition.

What would confirm it: a match within the extended set.
What would kill it: exhausting the extended set with 0 match, the same witness
protocol as every prior sweep.
Cost: hours on one rented GPU.

## 2. Extend further to substrings of longer words

The author, asked directly whether a list word could be hidden inside a
longer written word, answered yes and gave "possible" inside its own
negation, formed with the prefix "im-", as his own example, though the
surrounding conversation suggests he may have
meant the paraphrase-hint mechanism rather than a substring mechanism (see
README, "What is understood"). This is confirmed as an open question, not a
confirmed mechanism. If it is real, plausible substrings already identified in
the source texts include "cat" (cattle), "ill" (will), "hen" (then), "like"
(likely), "cause" and "use" (because), "health" (healthy), "hunt" (hunter),
and "inner" (dinner). The private research's own P3 estimate for a
substring-inclusive sweep, before the metadata extension, was 21/20 words per
side, 2.78x10^11 derivations, about 77 hours on one GPU (later re-priced
downward once a faster kernel was validated at 792,000 derivations/second).

What would confirm it: a match within the substring-extended set.
What would kill it: exhausting it with 0 match.
Cost: on the order of a day on one rented GPU at the validated 792,000
derivations/second rate; re-price before running, since kernel throughput
changes this estimate directly.

## 3. Read the video and post one more time for a metadata-style hidden word

If leads 1 and 2 both return negative, the most likely remaining explanation
is that one word lives in a part of the source material not yet identified as
a metadata surface, the same way the blog post's tags were missed until
2026-08-15. The video's own metadata (its tags, description formatting, or
on-screen text) and the post's remaining unread surfaces (any HTML attribute
resembling `article:tag`, image alt text) have not been re-examined with the
same "check every metadata field" method that found `fork` in the post's tags.

What would confirm it: a new word found in an unexamined metadata field,
tested through `tools/oracle.py` after being combined with the already-mapped
words.
What would kill it: a full metadata re-read producing nothing new; there is no
natural exhaustion point for this lead beyond a careful, complete pass.
Cost: an hour of directed reading, not a sweep.
