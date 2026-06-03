#!/usr/bin/env python3
"""Re-export an existing landmarks JSON file to TPS / CSV / Excel."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

# reuse the export helpers from extract_landmarks.py
sys.path.insert(0, _HERE)
from extract_landmarks import export  # noqa: E402
from paleo_common import print_json  # noqa: E402


def main(argv=None):
    p = argparse.ArgumentParser(description="Re-export a landmarks JSON to other formats")
    p.add_argument("--input", required=True, help="Landmarks JSON file")
    p.add_argument("--out-dir", default="morphometric_converted")
    p.add_argument("--format", default="tps,csv,xlsx",
                   help="Comma-separated: tps,csv,xlsx,json")
    args = p.parse_args(argv)

    src = Path(args.input)
    if not src.exists():
        print_json({"error": f"Input not found: {src}"})
        return

    try:
        payload = json.loads(src.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print_json({"error": f"Failed to read JSON: {e}"})
        return

    written, errors = export(payload, args.out_dir,
                             [f.strip().lower() for f in args.format.split(",")],
                             payload.get("specimen_id") or src.stem)
    print_json({
        "input": str(src),
        "files_written": written,
        "errors": errors,
    })


if __name__ == "__main__":
    main()
