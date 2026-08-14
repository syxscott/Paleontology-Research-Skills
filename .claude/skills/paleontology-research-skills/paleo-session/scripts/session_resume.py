#!/usr/bin/env python3
"""Build a compact context payload to resume a session.

The output is intended to be injected into the model's context as a brief
"where we left off" summary, NOT to be printed to the user verbatim.
"""

from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json, read_json, sessions_root  # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(description="Build a resume payload for a session")
    p.add_argument("--id", required=True, help="session_id (without .json)")
    p.add_argument("--last-n-turns", type=int, default=3)
    p.add_argument("--turn-limit", type=int, default=400)
    args = p.parse_args(argv)

    root = sessions_root()
    path = root / f"{args.id}.json"
    if not path.exists():
        print_json({"error": f"Session not found: {args.id}", "expected_path": str(path)})
        return
    s = read_json(path, default={}) or {}
    turns = s.get("turns") or []
    tail = turns[-max(1, args.last_n_turns) :]
    out_turns = []
    for t in tail:
        c = t.get("content") or ""
        if len(c) > args.turn_limit:
            c = c[: args.turn_limit] + " [..truncated..]"
        out_turns.append({"role": t.get("role"), "content": c})
    payload = {
        "session_id": s.get("session_id") or path.stem,
        "title": s.get("title"),
        "topic_tags": s.get("topic_tags") or [],
        "summary": s.get("summary"),
        "open_questions": s.get("open_questions") or [],
        "last_commands": (s.get("commands") or [])[-5:],
        "last_turns": out_turns,
        "started_at": s.get("started_at"),
        "ended_at": s.get("ended_at"),
    }
    print_json(payload)


if __name__ == "__main__":
    main()
