#!/usr/bin/env python3
"""Show one session by id."""

from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json, read_json, sessions_root  # noqa: E402


def _truncate_turn(t, limit):
    c = t.get("content") or ""
    if len(c) > limit:
        c = c[:limit] + " [..truncated..]"
    return {"role": t.get("role"), "content": c, "ts": t.get("ts")}


def main(argv=None):
    p = argparse.ArgumentParser(description="Show one Paleontology Research Skills session")
    p.add_argument("--id", required=True, help="session_id (without .json)")
    p.add_argument("--full", action="store_true", help="Do not truncate turns")
    p.add_argument("--turn-limit", type=int, default=400, help="Max chars per turn")
    args = p.parse_args(argv)

    root = sessions_root()
    path = root / f"{args.id}.json"
    if not path.exists():
        print_json({"error": f"Session not found: {args.id}", "expected_path": str(path)})
        return
    s = read_json(path, default=None) or {}
    s = dict(s)
    s["_file"] = str(path)
    if not args.full:
        s["turns"] = [_truncate_turn(t, args.turn_limit) for t in (s.get("turns") or [])]
    print_json(s)


if __name__ == "__main__":
    main()
