#!/usr/bin/env python3
"""List recent session files from ~/.paleontology-research-skills/sessions/."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json, read_json, sessions_root  # noqa: E402


def _ts(session, path):
    raw = session.get("ended_at") or session.get("started_at")
    if isinstance(raw, str):
        try:
            ts = dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
            if ts.tzinfo is None:
                ts = ts.replace(tzinfo=dt.timezone.utc)
            return ts
        except ValueError:
            pass
    try:
        return dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc)
    except OSError:
        return dt.datetime.min.replace(tzinfo=dt.timezone.utc)


def main(argv=None):
    p = argparse.ArgumentParser(description="List recent Paleontology Research Skills sessions")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--since-days", type=int, default=None)
    p.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Filter to sessions whose topic_tags include this tag (can repeat)",
    )
    args = p.parse_args(argv)

    root = sessions_root()
    if not root.exists():
        print_json({"count": 0, "sessions": [], "note": "no sessions yet", "sessionsRoot": str(root)})
        return

    items = []
    for f in root.glob("*.json"):
        s = read_json(f, default=None)
        if not isinstance(s, dict):
            continue
        ts = _ts(s, f)
        items.append((ts, s, f))

    if args.since_days:
        cutoff = dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(days=args.since_days)
        items = [t for t in items if t[0] >= cutoff]
    if args.tag:
        want = {t.lower() for t in args.tag}
        items = [t for t in items if any(str(tag).lower() in want for tag in (t[1].get("topic_tags") or []))]

    items.sort(key=lambda t: t[0], reverse=True)
    items = items[: max(1, args.limit)]

    sessions = []
    for ts, s, f in items:
        sessions.append(
            {
                "session_id": s.get("session_id") or f.stem,
                "title": s.get("title"),
                "started_at": s.get("started_at"),
                "ended_at": s.get("ended_at") or ts.isoformat(),
                "topic_tags": s.get("topic_tags") or [],
                "turn_count": len(s.get("turns") or []),
                "summary": (s.get("summary") or "")[:240],
                "file": str(f),
            }
        )
    print_json({"count": len(sessions), "sessions": sessions, "sessionsRoot": str(root)})


if __name__ == "__main__":
    main()
