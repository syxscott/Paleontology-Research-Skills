#!/usr/bin/env python3
"""Search the user's local research memory by semantic similarity."""
from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import search_memory, print_json, data_home  # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(description="Semantic search of Paleontology Research Skills memory")
    p.add_argument("--query", required=True)
    p.add_argument("--scope", choices=["all", "short", "long", "archive"], default="all")
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--min-score", type=float, default=0.12)
    args = p.parse_args(argv)

    hits = search_memory(args.query, scope=args.scope, top_k=args.top_k, min_score=args.min_score)
    print_json({
        "query": args.query,
        "scope": args.scope,
        "data_home": str(data_home()),
        "count": len(hits),
        "results": hits,
    })


if __name__ == "__main__":
    main()
