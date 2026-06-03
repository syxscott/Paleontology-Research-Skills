#!/usr/bin/env python3
"""Archive old short-term memory entries."""
from __future__ import annotations

import argparse
import datetime as dt
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import memory_root, print_json, read_json  # noqa: E402


def _ts(entry, path):
    raw = entry.get("timestamp") or entry.get("created_at")
    if isinstance(raw, str):
        try:
            return dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            pass
    try:
        return dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc)
    except OSError:
        return dt.datetime.now(tz=dt.timezone.utc)


def main(argv=None):
    p = argparse.ArgumentParser(description="Archive old short-term memory entries")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    short_dir = memory_root() / "short"
    arch_dir = memory_root() / "archive" / "short"
    moved, kept = [], 0
    if not short_dir.exists():
        print_json({"moved": [], "movedCount": 0, "kept": 0,
                    "cutoffDays": args.days, "dryRun": args.dry_run,
                    "note": "no short-term memory directory yet",
                    "shortDir": str(short_dir), "archiveDir": str(arch_dir)})
        return

    cutoff = dt.datetime.now(tz=dt.timezone.utc) - dt.timedelta(days=args.days)
    arch_dir.mkdir(parents=True, exist_ok=True)
    for f in short_dir.glob("*.json"):
        entry = read_json(f, default={}) or {}
        ts = _ts(entry, f)
        if ts < cutoff:
            target = arch_dir / f.name
            if not args.dry_run:
                try:
                    f.replace(target)
                except OSError as e:
                    moved.append({"file": f.name, "error": str(e)})
                    continue
            moved.append({"file": f.name, "timestamp": ts.isoformat(), "target": str(target)})
        else:
            kept += 1
    print_json({
        "moved": moved,
        "movedCount": len(moved),
        "kept": kept,
        "cutoffDays": args.days,
        "dryRun": args.dry_run,
        "shortDir": str(short_dir),
        "archiveDir": str(arch_dir),
    })


if __name__ == "__main__":
    main()
