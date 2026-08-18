#!/usr/bin/env python3
"""
Download the exact bytes of the author's own posts and of the two source texts.

Everything in this folder that is still open turns on one question: which exact
byte sequence went into MD5. Every attempt so far has worked from a
transcription, and a transcription silently normalises the things that decide
the hash -- curly quotes, apostrophes, ellipses, line endings, and where one
paragraph stops and the next starts.

Reddit's JSON endpoint returns `selftext`, the raw markdown the author typed,
character for character. That removes the transcription from the loop entirely.
This script fetches it, along with the Wattpad chapter in both the rendered and
the stored form, and writes each to its own file.

Nothing downloaded here is committed: these are third-party texts the repository
does not redistribute. The default output directory is outside the repo and the
repo's .gitignore does not need to know about it.

Run it somewhere with open outbound HTTPS:

    python3 tools/fetch_sources.py --out ~/aoi-sources

Then check what arrived:

    python3 tools/fetch_sources.py --out ~/aoi-sources --verify

Reddit rate-limits anonymous JSON requests; the script pauses between them and
retries. If a fetch 429s repeatedly, wait a few minutes and run it again -- it
skips files it already has.
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request

UA = "open-crypto-puzzles/1.0 (source archival for puzzle analysis)"

# The author's own posts. The Reddit JSON endpoint returns the raw markdown of
# each, which is what she copied from when she hashed.
REDDIT = {
    "block77-stage-one": "https://www.reddit.com/r/Grycoin/comments/ca6jxv/.json",
    "block76":           "https://www.reddit.com/r/Grycoin/comments/cgcv9i/.json",
    "rbb-discussion":    "https://www.reddit.com/r/Grycoin/comments/chn8un/.json",
    # Grycoin Block 2, the worked example that states the format. Its escrow is
    # spent, so reversing it measures every convention instead of assuming one.
    # The listing search below finds its id if this direct guess misses.
    "grycoin-listing":   "https://www.reddit.com/r/Grycoin/new/.json?limit=100",
}

OTHER = {
    # The Real Big Block's source text, in both the form a reader sees and the
    # form Wattpad stores. The author says she typed blank lines between
    # paragraphs; the stored form does not have them, so both are needed.
    "wattpad-chapter.html":
        "https://www.wattpad.com/apiv2/storytext?id=720888559",
    "wattpad-chapter-meta.json":
        "https://www.wattpad.com/api/v3/story_parts/720888559"
        "?fields=id,title,modifyDate,text_url,photo_url",
    # Block 77 Stage One's source text.
    "finney-bitcoin-and-me.html":
        "https://bitcointalk.org/index.php?topic=155054.0",
}


def get(url, tries=4):
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code in (429, 503):
                wait = 5 * (attempt + 1)
                print(f"    {last}, waiting {wait}s", flush=True)
                time.sleep(wait)
                continue
            break
        except Exception as e:                       # noqa: BLE001
            last = str(e)
            time.sleep(3)
    raise RuntimeError(f"{url}: {last}")


def save(out, name, data):
    path = os.path.join(out, name)
    with open(path, "wb") as fh:
        fh.write(data)
    print(f"    {name}  {len(data):,} bytes  sha256 "
          f"{hashlib.sha256(data).hexdigest()[:16]}")
    return path


def fetch_all(out):
    os.makedirs(out, exist_ok=True)
    listing = None
    for name, url in REDDIT.items():
        target = os.path.join(out, name + ".json")
        if os.path.exists(target):
            print(f"  {name}: already have it")
            if name == "grycoin-listing":
                listing = json.load(open(target, encoding="utf-8"))
            continue
        print(f"  {name}")
        data = get(url)
        save(out, name + ".json", data)
        if name == "grycoin-listing":
            listing = json.loads(data)
        time.sleep(3)

    # Pull every post the listing holds as its own raw-markdown file. Block 2 is
    # in here; so is anything else she wrote that a transcription might garble.
    if listing:
        posts = listing.get("data", {}).get("children", [])
        print(f"  listing holds {len(posts)} posts")
        os.makedirs(os.path.join(out, "posts"), exist_ok=True)
        for p in posts:
            d = p.get("data", {})
            pid, title = d.get("id"), (d.get("title") or "")
            body = d.get("selftext")
            if not pid or body is None:
                continue
            slug = "".join(c if c.isalnum() else "-" for c in title)[:60]
            fn = os.path.join("posts", f"{pid}_{slug}.txt")
            if not os.path.exists(os.path.join(out, fn)):
                save(out, fn, body.encode("utf-8"))

    for name, url in OTHER.items():
        if os.path.exists(os.path.join(out, name)):
            print(f"  {name}: already have it")
            continue
        print(f"  {name}")
        try:
            save(out, name, get(url))
        except RuntimeError as e:
            print(f"    FAILED: {e}")
        time.sleep(2)


def verify(out):
    """Report what is present and, for each Reddit post, its exact character mix.

    The point of the fetch is the characters a transcription would have lost, so
    this prints them rather than a byte count.
    """
    if not os.path.isdir(out):
        print(f"{out}: no such directory")
        return 1
    # Written as escapes rather than literals: these are exactly the characters
    # a transcription loses, so the file that hunts for them must not contain
    # them itself.
    interesting = {
        "curly apostrophe": "\u2019", "curly open quote": "\u201c",
        "curly close quote": "\u201d", "ellipsis char": "\u2026",
        "en dash": "\u2013", "em dash": "\u2014", "nbsp": "\u00a0",
        "CR": "\r", "LF": "\n",
    }
    for root, _dirs, files in os.walk(out):
        for f in sorted(files):
            path = os.path.join(root, f)
            raw = open(path, "rb").read()
            rel = os.path.relpath(path, out)
            print(f"\n{rel}  {len(raw):,} bytes")
            if not (f.endswith(".txt") or f.endswith(".json")):
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                print("    not UTF-8")
                continue
            counts = {k: text.count(v) for k, v in interesting.items()}
            print("    " + ", ".join(f"{k} {n}" for k, n in counts.items() if n))
            if f.endswith(".txt"):
                paras = [p for p in text.split("\n\n") if p.strip()]
                print(f"    {len(paras)} blank-line-separated paragraphs")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.path.expanduser("~/aoi-sources"),
                    help="directory to write into (default ~/aoi-sources)")
    ap.add_argument("--verify", action="store_true",
                    help="report on what has already been downloaded")
    args = ap.parse_args()
    if args.verify:
        return verify(args.out)
    print(f"writing to {args.out}")
    fetch_all(args.out)
    print("\ndone. Now run with --verify, and send back the output.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
