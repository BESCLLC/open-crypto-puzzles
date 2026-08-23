# RBB Hash Playground

A tiny web tool for exploring the Aoi Nakamoto quizchain "block 77" carrier by hand.

Paste paragraphs, change capitalization in place, and it shows you:

- the **MD5** of the assembled text (this is the BIP39 entropy),
- the **BIP39 mnemonic** it produces,
- the first N **P2PKH addresses** on `m/44'/0'/0'/0/i` (idx 0…N) **with their WIF private keys**,
- a **per-paragraph MD5** table (to compare against Wattpad's `data-p-id`),
- an automatic **green banner** if any derived address equals a known escrow.

The derivation is the exact certified pipeline: `MD5(text)` → BIP39 → BIP44 → compressed P2PKH.
On boot it self-tests against two of the author's own published vectors (Stage-One
`9dd2efb9…` → `19Tby…`, and the WIF vector `2941774a…` idx1 → `L5Z66…`). The header
shows **derivation certified ✅** when they reproduce.

## Assembly modes

- **split on blank lines, rejoin with separator** — paste the chapter with a blank line
  between paragraphs; pick the separator (default **CRLF CRLF** = the live escrow's
  "two line breaks"). Multi-line paragraphs are unwrapped to a single line.
- **hash exactly what I pasted** — hashes the textarea verbatim (only normalizing the
  chosen line ending). Use this when byte-exactness matters, e.g. the Stage-One example
  whose `[edited slightly]` trailer joins with a single newline.

Click **Load Stage-1 example** to load Hal Finney's "Bitcoin and me" post already
edge-edited; with **raw + LF LF** its MD5 must be `9dd2efb9…` and idx0 must be
`19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN`. That's your proof the tool is correct.

## Run locally

```bash
npm install
npm start          # http://localhost:3000  (or set PORT)
```

## Deploy on Railway

1. Push this folder to a GitHub repo (or point Railway at this subfolder as the **Root Directory**).
2. Railway → **New Project → Deploy from GitHub repo**.
3. It auto-detects Node. Build: `npm install`. Start: `npm start` (from `package.json`).
4. Railway sets `PORT` automatically; the server reads `process.env.PORT`.
5. Open the generated URL.

## ⚠ Security

- This tool prints **private keys** (WIF) for whatever you compute, so you can sweep a hit
  yourself. **Keep the instance private.** Anyone who can reach the URL sees whatever you
  type and any keys it derives. Railway URLs are public by default — treat it as sensitive,
  and if you ever hit the live escrow, move the funds from a trusted machine, not by pasting
  the key anywhere else.
- There is no database and nothing is logged; computation is per-request in memory.
