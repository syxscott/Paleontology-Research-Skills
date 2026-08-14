#!/usr/bin/env python3
"""Show the parsed profile in full (JSON or pretty)."""

from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import data_home, load_profile, print_json, profile_files  # noqa: E402


def _pretty(prof):
    u = prof["user"]
    s = prof["soul"]
    sp, up = profile_files()
    lines = []
    lines.append(f"Paleontology Research Skills profile  (data_home = {data_home()})")
    lines.append(f"  soul.md : {sp}")
    lines.append(f"  user.md : {up}")
    lines.append("")
    lines.append("[User]")
    lines.append(f"  role:        {u.get('role')}")
    lines.append(f"  domain:      {u.get('domain')}")
    lines.append(f"  institution: {u.get('institution') or '(unset)'}")
    rf = u.get("researchFocus", {})
    lines.append(f"  interests:   {', '.join(rf.get('primaryInterests') or []) or '(none)'}")
    lines.append(f"  periods:     {', '.join(rf.get('preferredPeriods') or []) or '(none)'}")
    lines.append(f"  regions:     {', '.join(rf.get('preferredRegions') or []) or '(none)'}")
    lines.append(f"  language:    {u.get('outputLanguage')}  (preferred: {u.get('languagePreference')})")
    dp = u.get("dataPreferences", {})
    lines.append(
        f"  data prefs:  limit={dp.get('defaultOccurrenceLimit')} "
        f"preprints={dp.get('includePreprints')} OA={dp.get('preferOpenAccess')} "
        f"cite={dp.get('citationFormat')}"
    )
    lines.append("")
    lines.append("[Soul]")
    lines.append(f"  mission:     {s.get('mission')}")
    cp = s.get("corePrinciples") or []
    lines.append(f"  principles ({len(cp)}):")
    for p in cp:
        lines.append(f"    - {p}")
    sb = s.get("safetyBoundaries") or []
    lines.append(f"  safety ({len(sb)}):")
    for p in sb:
        lines.append(f"    - {p}")
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description="Show parsed Paleontology Research Skills profile")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    prof = load_profile()
    if args.json:
        print_json(prof)
    else:
        print(_pretty(prof))


if __name__ == "__main__":
    main()
