#!/usr/bin/env python3
"""List recent entries from the local memory store."""
from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import (  # noqa: E402
    _iter_short_memory, _iter_long_memory, _iter_archive_memory,
    print_json, data_home,
)


def main(argv=None):
    p = argparse.ArgumentParser(description="List recent Paleontology Research Skills memory entries")
    p.add_argument("--scope", choices=["all", "short", "long", "archive"], default="all")
    p.add_argument("--limit", type=int, default=20)
    args = p.parse_args(argv)

    iters = []
    if args.scope in ("all", "short"):
        iters += list(_iter_short_memory())
    if args.scope in ("all", "long"):
        iters += list(_iter_long_memory())
    if args.scope in ("all", "archive"):
        iters += list(_iter_archive_memory())

    iters.sort(key=lambda e: e.get("timestamp") or e.get("created_at") or "", reverse=True)
    cut = iters[:max(1, args.limit)]
    print_json({
        "scope": args.scope,
        "data_home": str(data_home()),
        "count": len(cut),
        "entries": cut,
    })


if __name__ == "__main__":
    main()
