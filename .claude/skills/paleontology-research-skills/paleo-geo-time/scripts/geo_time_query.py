#!/usr/bin/env python3
"""Query the bundled ICS geological time scale."""
from __future__ import annotations

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json, read_json  # noqa: E402

DATA_PATH = os.path.normpath(os.path.join(_HERE, "..", "data", "ics_timescale.json"))


def _load_intervals():
    data = read_json(DATA_PATH, default=None)
    if not isinstance(data, dict):
        return [], None
    intervals = []
    # The bundled file is grouped by rank under various plural keys.
    for key, items in data.items():
        if not isinstance(items, list):
            continue
        for it in items:
            if isinstance(it, dict):
                d = dict(it)
                d.setdefault("rank", key.rstrip("s").lower())
                intervals.append(d)
    return intervals, data


def _duration(d):
    s = d.get("startMa")
    e = d.get("endMa")
    if s is None or e is None:
        return None
    return round(s - e, 4)


def _normalise(d):
    out = dict(d)
    out["durationMa"] = _duration(d)
    return out


def _by_name(intervals, name):
    n = name.lower().strip()
    return [_normalise(d) for d in intervals
            if (d.get("name", "").lower() == n) or (d.get("id", "").lower() == n)]


def _by_age(intervals, age):
    out = []
    for d in intervals:
        s, e = d.get("startMa"), d.get("endMa")
        if s is None or e is None:
            continue
        if e <= age <= s:
            out.append(_normalise(d))
    return out


# Possible parent-pointer fields in the ICS data, ordered from broadest to finest.
_PARENT_FIELDS = ("eonothem", "era", "period", "epoch", "stage", "parent")


def _matches_parent(d, parent_lc):
    """Check ALL hierarchy fields, not just `parent`. ICS data uses
    fields like `era: mesozoic`, `period: cretaceous` instead of a uniform
    `parent` pointer."""
    for fld in _PARENT_FIELDS:
        v = d.get(fld)
        if isinstance(v, str) and v.lower().strip() == parent_lc:
            return True
    return False


def _list(intervals, rank=None, parent=None):
    out = []
    rn = (rank or "").lower().strip()
    pn = (parent or "").lower().strip()
    for d in intervals:
        if rn and (d.get("rank") or "").lower() != rn:
            continue
        if pn and not _matches_parent(d, pn):
            continue
        out.append(_normalise(d))
    out.sort(key=lambda x: -(x.get("startMa") or 0))
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Query the ICS geological time scale")
    p.add_argument("--period", help="Named interval to look up (any rank)")
    p.add_argument("--age", type=float, help="Find intervals that contain this age (Ma)")
    p.add_argument("--list", action="store_true", help="List intervals")
    p.add_argument("--rank", help="Filter list by rank (eonothem/era/period/epoch/age/stage)")
    p.add_argument("--parent", help="Filter list by parent interval name")
    args = p.parse_args(argv)

    intervals, raw = _load_intervals()
    if not intervals:
        print_json({"error": f"No intervals loaded from {DATA_PATH}", "matches": []})
        return

    if args.period:
        matches = _by_name(intervals, args.period)
        print_json({"query": {"period": args.period}, "matches": matches,
                    "source": (raw or {}).get("source")})
        return
    if args.age is not None:
        matches = _by_age(intervals, args.age)
        print_json({"query": {"age": args.age}, "matches": matches,
                    "source": (raw or {}).get("source")})
        return
    if args.list:
        matches = _list(intervals, args.rank, args.parent)
        print_json({"query": {"list": True, "rank": args.rank, "parent": args.parent},
                    "count": len(matches), "matches": matches,
                    "source": (raw or {}).get("source")})
        return

    print_json({"error": "Provide --period, --age, or --list",
                "version": (raw or {}).get("version"),
                "totalIntervals": len(intervals)})


if __name__ == "__main__":
    main()
