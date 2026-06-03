#!/usr/bin/env python3
"""Generate a 3-bullet heuristic summary from a paper abstract.

Input: --abstract text, OR pipe via stdin, OR --doi to fetch via CrossRef.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json  # noqa: E402

UA = "Paleontology-Research-Skills/1.0 (mailto:noreply@example.org)"
SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")
KEYWORDS = {
    "we", "show", "report", "describe", "demonstrate", "find", "found",
    "discover", "evidence", "conclude", "suggest", "imply", "novel", "first",
    "specimen", "fossil", "phylogen", "stratigraph", "age", "ma",
    "morpholog", "tax", "clade", "diversity",
}


def _score(sentence):
    words = re.findall(r"[A-Za-z]+", sentence.lower())
    if not words:
        return 0.0
    length = min(len(words), 40)
    kw = sum(1 for w in words if any(w.startswith(k) for k in KEYWORDS))
    return length * 0.5 + kw * 4.0


def summarize(text, n=3):
    text = re.sub(r"\s+", " ", (text or "").strip())
    if not text:
        return []
    raw = SENT_RE.split(text)
    sentences = [s.strip() for s in raw if len(s.strip()) > 20]
    if not sentences:
        return [text[:240]]
    ranked = sorted(enumerate(sentences), key=lambda x: _score(x[1]), reverse=True)
    chosen = sorted(ranked[:n], key=lambda x: x[0])
    return [s for _, s in chosen]


def fetch_abstract_by_doi(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='')}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        return None, f"Failed to fetch DOI: {e}"
    msg = data.get("message", {})
    abstract = msg.get("abstract") or ""
    abstract = re.sub(r"</?(jats:)?[a-zA-Z][^>]*>", " ", abstract)
    abstract = re.sub(r"\s+", " ", abstract).strip()
    return abstract, None


def main(argv=None):
    p = argparse.ArgumentParser(description="3-bullet heuristic summary of a paper abstract")
    src = p.add_mutually_exclusive_group()
    src.add_argument("--abstract")
    src.add_argument("--doi")
    p.add_argument("--bullets", type=int, default=3)
    args = p.parse_args(argv)

    text = args.abstract
    note = None
    if args.doi and not text:
        text, err = fetch_abstract_by_doi(args.doi)
        if err:
            print_json({"error": err, "bullets": []})
            return
        note = f"abstract fetched from DOI {args.doi}"
    if not text and not sys.stdin.isatty():
        text = sys.stdin.read()

    bullets = summarize(text or "", n=max(1, args.bullets))
    print_json({"source": "heuristic", "note": note, "bullets": bullets})


if __name__ == "__main__":
    main()
