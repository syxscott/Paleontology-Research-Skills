#!/usr/bin/env python3
"""Batch-extract landmarks from every image in a directory.

Calls extract_landmarks.py on each file, then optionally writes a
multi-specimen TPS file aggregating all results.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json, read_json  # noqa: E402

EXTRACT_SCRIPT = Path(_HERE) / "extract_landmarks.py"
DEFAULT_EXTS = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp", ".bmp")


def _list_images(image_dir):
    p = Path(image_dir)
    if not p.exists():
        return []
    out = []
    for f in sorted(p.iterdir()):
        if f.is_file() and f.suffix.lower() in DEFAULT_EXTS:
            out.append(f)
    return out


def _aggregate_tps(json_files, out_path):
    """Write a multi-specimen TPS file."""
    parts = []
    for jf in json_files:
        payload = read_json(jf, default=None)
        if not isinstance(payload, dict):
            continue
        lms = payload.get("landmarks") or []
        if not lms:
            continue
        parts.append(f"LM={len(lms)}")
        for lm in lms:
            parts.append(f"{lm['x']:.4f}  {lm['y']:.4f}")
        if payload.get("image_path"):
            parts.append(f"IMAGE={Path(payload['image_path']).name}")
        parts.append(f"ID={payload['specimen_id']}")
        parts.append(f"SCALE={payload.get('scale', 1.0):.4f}")
        parts.append("")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("\n".join(parts), encoding="utf-8")


def _aggregate_csv(json_files, out_path):
    rows = ["specimen_id,landmark_id,x,y,type,name"]
    for jf in json_files:
        payload = read_json(jf, default=None)
        if not isinstance(payload, dict):
            continue
        sid = payload["specimen_id"]
        for lm in payload.get("landmarks") or []:
            rows.append(f"{sid},{lm['id']},{lm['x']:.4f},{lm['y']:.4f},{lm['type']},{lm['name']}")
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text("\n".join(rows) + "\n", encoding="utf-8")


def _aggregate_excel(json_files, out_path):
    try:
        from openpyxl import Workbook
    except ImportError:
        return False
    wb = Workbook()
    # Summary sheet
    summary = wb.active
    summary.title = "Summary"
    summary.append(["specimen_id", "landmark_id", "x", "y", "type", "name", "scale"])
    for jf in json_files:
        payload = read_json(jf, default=None)
        if not isinstance(payload, dict):
            continue
        sid = payload["specimen_id"]
        scale = payload.get("scale", 1.0)
        for lm in payload.get("landmarks") or []:
            summary.append([sid, lm["id"], lm["x"], lm["y"], lm["type"], lm["name"], scale])
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    return True


def main(argv=None):
    p = argparse.ArgumentParser(description="Batch-extract landmarks from a directory of fossil images")
    p.add_argument("--image-dir", required=True)
    p.add_argument("--out-dir", default="morphometric_output")
    p.add_argument("--num-landmarks", type=int, default=64)
    p.add_argument("--threshold", type=int, default=150)
    p.add_argument("--formats", default="json,tps,csv", help="Per-specimen formats: json,tps,csv,xlsx")
    p.add_argument(
        "--aggregate", default="tps,csv", help="Aggregated formats: tps (multi-specimen TPS), csv, xlsx"
    )
    p.add_argument("--scale", type=float, default=1.0)
    args = p.parse_args(argv)

    images = _list_images(args.image_dir)
    if not images:
        print_json({"error": f"No images found in {args.image_dir}", "supported_exts": list(DEFAULT_EXTS)})
        return

    results = []
    out_root = Path(args.out_dir)
    per_specimen_dir = out_root / "per_specimen"
    per_specimen_dir.mkdir(parents=True, exist_ok=True)

    for img in images:
        cmd = [
            sys.executable,
            str(EXTRACT_SCRIPT),
            "--image",
            str(img),
            "--num-landmarks",
            str(args.num_landmarks),
            "--threshold",
            str(args.threshold),
            "--out-dir",
            str(per_specimen_dir),
            "--formats",
            args.formats,
            "--scale",
            str(args.scale),
        ]
        # IMPORTANT on Windows: force UTF-8 for subprocess pipes,
        # otherwise CJK paths/text in stdout will hit GBK and crash.
        env = os.environ.copy()
        env.setdefault("PYTHONIOENCODING", "utf-8")
        try:
            r = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=120,
                env=env,
            )
            entry = {"image": str(img), "ok": r.returncode == 0}
            try:
                entry["result"] = json.loads(r.stdout) if r.stdout else None
            except json.JSONDecodeError:
                entry["raw_stdout"] = (r.stdout or "")[:300]
                entry["raw_stderr"] = (r.stderr or "")[:300]
        except subprocess.TimeoutExpired:
            entry = {"image": str(img), "ok": False, "error": "extraction timed out"}
        except (OSError, subprocess.SubprocessError) as e:
            entry = {"image": str(img), "ok": False, "error": str(e)}
        results.append(entry)

    # Aggregate
    json_files = []
    for img in images:
        candidate = per_specimen_dir / f"{img.stem}.json"
        if candidate.exists():
            json_files.append(candidate)

    agg_written = {}
    for fmt in [s.strip().lower() for s in args.aggregate.split(",") if s.strip()]:
        if fmt == "tps":
            tps = out_root / "all_specimens.tps"
            _aggregate_tps(json_files, tps)
            agg_written["tps"] = str(tps)
        elif fmt == "csv":
            csv = out_root / "all_specimens.csv"
            _aggregate_csv(json_files, csv)
            agg_written["csv"] = str(csv)
        elif fmt in ("xlsx", "excel"):
            xl = out_root / "all_specimens.xlsx"
            ok = _aggregate_excel(json_files, xl)
            agg_written["xlsx"] = str(xl) if ok else "openpyxl not installed"

    print_json(
        {
            "image_dir": args.image_dir,
            "out_dir": args.out_dir,
            "total_images": len(images),
            "successful": sum(1 for r in results if r.get("ok")),
            "aggregated_files": agg_written,
            "per_specimen_dir": str(per_specimen_dir),
            "timestamp": dt.datetime.now(tz=dt.timezone.utc).isoformat(),
            "results_preview": results[:3],
        }
    )


if __name__ == "__main__":
    main()
