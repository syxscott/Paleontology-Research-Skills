#!/usr/bin/env python3
"""Search across all sessions using hashing-trick vector similarity."""
from __future__ import annotations

import argparse
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import (  # noqa: E402
    sessions_root, read_json, print_json,
    hashing_vector, cosine_similarity,
)


def _session_text(s):
    parts = [s.get("title") or "", s.get("summary") or ""]
    parts += list(s.get("topic_tags") or [])
    for t in s.get("turns") or []:
        c = t.get("content") or ""
        if isinstance(c, str):
            parts.append(c)
    return " ".join(p for p in parts if p)


def _snippets(text, query, max_snippets=2, window=120):
    qwords = [w for w in re.findall(r"[A-Za-z0-9]+", query.lower()) if len(w) > 2]
    if not qwords:
        return []
    pattern = re.compile("|".join(re.escape(w) for w in qwords), re.IGNORECASE)
    out = []
    for m in pattern.finditer(text):
        start = max(0, m.start() - window // 2)
        end = min(len(text), m.end() + window // 2)
        snippet = text[start:end].strip()
        if snippet not in out:
            out.append(snippet)
        if len(out) >= max_snippets:
            break
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Search Paleontology Research Skills sessions")
    p.add_argument("--query", required=True)
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--min-score", type=float, default=0.10)
    args = p.parse_args(argv)

    root = sessions_root()
    if not root.exists():
        print_json({"query": args.query, "count": 0, "results": [], "note": "no sessions yet"})
        return

    qvec = hashing_vector(args.query)
    hits = []
    for f in root.glob("*.json"):
        s = read_json(f, default=None)
        if not isinstance(s, dict):
            continue
        text = _session_text(s)
        if not text:
            continue
        score = cosine_similarity(qvec, hashing_vector(text))
        if score >= args.min_score:
            hits.append({
                "session_id": s.get("session_id") or f.stem,
                "title": s.get("title"),
                "ended_at": s.get("ended_at"),
                "topic_tags": s.get("topic_tags") or [],
                "score": round(score, 4),
                "matched_snippets": _snippets(text, args.query),
                "file": str(f),
            })
    hits.sort(key=lambda x: x["score"], reverse=True)
    hits = hits[: max(1, args.top_k)]
    print_json({"query": args.query, "count": len(hits), "results": hits, "sessionsRoot": str(root)})


if __name__ == "__main__":
    main()
