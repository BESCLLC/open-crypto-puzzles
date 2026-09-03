# Exhausting a single unknown BIP39 slot

## Why this note exists

A reader supplied a partial 12-word reconstruction of this hunt's seed: 11 words filled in,
one slot empty. The words themselves are deliberately not recorded here. They came with no
stated provenance, none of the three insight locks has been opened to corroborate any of
them, and publishing an 11 of 12 reconstruction on an open escrow would hand a sniper most
of the work. What is recorded here is the method and the result, both of which are useful
to the next reader regardless of whether that particular fragment was real.

## The shape of the problem

A 12-word mnemonic with exactly one unknown slot is bounded, unlike the three insight locks.
There are 2048 candidates for the gap, and only those whose BIP39 checksum closes are
derivable at all: for the fragment in question, 147 of 2048. At a measured 118 pairs per
second on 4 cores, the gap itself is exhaustible in about a second. The passphrase is the
unbounded half, and it is where all the cost sits.

`tools/search_missing_word.py` implements this. It takes a 12-slot template with one `?`,
filters by checksum, and crosses the survivors with a passphrase list.

## Result

| Passphrase family | Count | Pairs | Result |
|---|---|---|---|
| Empty passphrase alone | 1 | 147 | 0 hits |
| Empty, plus the Glimmer title, `supernova`, site passwords, band-name variants | 27 | 3,969 | 0 hits |
| Glimmer title and lyric phrases, cased/spaced/joined, plus site-theme strings | 1,029 | 151,263 | 0 hits, 1,280s |

Confirmed complete and negative: **155,232 pairs, 0 hits.** A further family (all 4,096 cased
BIP39 words as passphrase, 602,112 pairs; N/D/t = 602,112 / 118 per sec / 85 minutes, inside
the two-hour budget rule in AGENTS.md) was run separately and is recorded in
[tested.md](tested.md) only if and when it completed.

## Oracle used, and how it was verified

`tools/oracle.py` would not run on the machine this sweep was done on: `bip_utils` pulls in
`crcmod`, whose `setup.py` fails against modern setuptools with
`AttributeError: install_layout`. Setting `SETUPTOOLS_USE_DISTUTILS=stdlib` before
`pip install` fixes it, and this is now noted in the README so the next reader does not lose
the time I did.

`tools/oracle_pure.py` was written before that workaround was found and is kept because it
needs no compiled dependency at all. It is verified three ways:

1. Its own `--selftest`: the official BIP39 seed vector, the official BIP84 vector address at
   `m/84'/0'/0'/0/0` (the exact path this puzzle uses), and the published xpub-to-escrow
   identity, plus rejection of a known-wrong mnemonic.
2. A differential test against `bip_utils` once that was installable: 25 random mnemonics
   crossed with 5 passphrases agree byte for byte on both the BIP39 seed and the derived
   `m/84'/0'/0'/0/0` address.
3. `tools/oracle.py --selftest` passes on the same machine, so the two agree on the escrow
   identity.

This closes a gap the original documents about itself. `tools/oracle.py` calls its
BIP39-mnemonic-to-seed leg uncertified for want of a known-good vector; the public BIP39 and
BIP84 test vectors supply one, so mnemonic-in to address-out now has a positive control end
to end.

## What a negative here does and does not mean

A no-hit result of this kind cannot separate two hypotheses: that the 11 words are right and
the passphrase was not in the list, or that at least one of the words is wrong, in which case
no passphrase list would ever hit. Only opening one of the three insight locks separates
them, which is what the hunt has needed all along. A partial reconstruction supplies no
password for any gate, so it does not displace leads 1 through 4.
