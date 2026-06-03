#!/usr/bin/env python3
"""Extract N semilandmarks from a single fossil image silhouette.

Algorithm:
  1. Grayscale + threshold to binary
  2. Largest 4-connected foreground component
  3. Moore-neighbourhood boundary trace
  4. Arc-length resample to N points
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json  # noqa: E402

try:
    from PIL import Image
    _PIL_OK = True
except ImportError:
    _PIL_OK = False


# ========== Pure-Python image utilities ==========

def _load_binary_mask(image_path, threshold):
    """Open image, return (binary_mask, (width, height)).
    `binary_mask` is a list of lists of bool (True = foreground).
    Foreground = darker than threshold (typical: dark fossil on light bg).
    """
    img = Image.open(image_path).convert("L")
    w, h = img.size
    px = img.load()
    mask = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            if px[x, y] <= threshold:
                mask[y][x] = True
    return mask, (w, h)


def _largest_component(mask):
    """Return a mask for the largest 4-connected foreground component."""
    h = len(mask)
    w = len(mask[0]) if h else 0
    visited = [[False] * w for _ in range(h)]
    best_size = 0
    best_mask = None
    for sy in range(h):
        for sx in range(w):
            if not mask[sy][sx] or visited[sy][sx]:
                continue
            # iterative flood fill
            stack = [(sx, sy)]
            cur_mask = [[False] * w for _ in range(h)]
            size = 0
            while stack:
                x, y = stack.pop()
                if x < 0 or x >= w or y < 0 or y >= h:
                    continue
                if visited[y][x] or not mask[y][x]:
                    continue
                visited[y][x] = True
                cur_mask[y][x] = True
                size += 1
                stack.append((x + 1, y))
                stack.append((x - 1, y))
                stack.append((x, y + 1))
                stack.append((x, y - 1))
            if size > best_size:
                best_size = size
                best_mask = cur_mask
    return best_mask, best_size


def _trace_boundary(mask):
    """Moore-neighbourhood boundary tracing.

    Returns ordered list of (x, y) boundary pixels traversed clockwise,
    starting from the topmost-leftmost foreground pixel.
    """
    h = len(mask)
    w = len(mask[0]) if h else 0
    if not h or not w:
        return []
    # Find start: top-down, left-to-right
    start = None
    for y in range(h):
        for x in range(w):
            if mask[y][x]:
                start = (x, y)
                break
        if start:
            break
    if not start:
        return []
    # 8-neighbours in clockwise order starting from N
    DIRS = [(0, -1), (1, -1), (1, 0), (1, 1),
            (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    boundary = [start]
    cur = start
    # Direction we came from on the first move — set so we start checking from E
    from_dir = 6  # came from W
    safety_cap = w * h * 4 + 10
    while True:
        # Start checking from the direction one step counter-clockwise of from_dir
        start_check = (from_dir + 2) % 8
        found = False
        for i in range(8):
            d = (start_check + i) % 8
            dx, dy = DIRS[d]
            nx, ny = cur[0] + dx, cur[1] + dy
            if 0 <= nx < w and 0 <= ny < h and mask[ny][nx]:
                cur = (nx, ny)
                # The direction we came FROM is the opposite of d
                from_dir = (d + 4) % 8
                boundary.append(cur)
                found = True
                break
        if not found:
            break
        if cur == start and len(boundary) > 1:
            boundary.pop()  # remove duplicate start
            break
        if len(boundary) > safety_cap:
            break
    return boundary


def _resample(boundary, n):
    """Resample boundary to N evenly-spaced points along arc length."""
    if not boundary or n < 1:
        return []
    if len(boundary) == 1:
        return [boundary[0]] * n
    # Cumulative arc length along the closed loop
    cum = [0.0]
    for i in range(1, len(boundary)):
        dx = boundary[i][0] - boundary[i - 1][0]
        dy = boundary[i][1] - boundary[i - 1][1]
        cum.append(cum[-1] + (dx * dx + dy * dy) ** 0.5)
    # Close the loop
    dx = boundary[0][0] - boundary[-1][0]
    dy = boundary[0][1] - boundary[-1][1]
    total = cum[-1] + (dx * dx + dy * dy) ** 0.5
    if total == 0:
        return [boundary[0]] * n

    out = []
    step = total / n
    seg_idx = 0
    for i in range(n):
        target = i * step
        # Walk segments until cum[seg_idx+1] >= target
        while seg_idx + 1 < len(cum) and cum[seg_idx + 1] < target:
            seg_idx += 1
        if seg_idx + 1 >= len(cum):
            # last partial segment back to start
            seg_start = cum[-1]
            seg_end = total
            p0 = boundary[-1]
            p1 = boundary[0]
        else:
            seg_start = cum[seg_idx]
            seg_end = cum[seg_idx + 1]
            p0 = boundary[seg_idx]
            p1 = boundary[seg_idx + 1]
        seg_len = seg_end - seg_start
        if seg_len == 0:
            out.append((float(p0[0]), float(p0[1])))
        else:
            t = (target - seg_start) / seg_len
            x = p0[0] + t * (p1[0] - p0[0])
            y = p0[1] + t * (p1[1] - p0[1])
            out.append((float(x), float(y)))
    return out


# ========== Export ==========

def _save_json(out_path, payload):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _save_tps(out_path, payload):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    lines = [f"LM={payload['num_landmarks']}"]
    for lm in payload["landmarks"]:
        lines.append(f"{lm['x']:.4f}  {lm['y']:.4f}")
    if payload.get("image_path"):
        lines.append(f"IMAGE={Path(payload['image_path']).name}")
    lines.append(f"ID={payload['specimen_id']}")
    lines.append(f"SCALE={payload.get('scale', 1.0):.4f}")
    Path(out_path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _save_csv(out_path, payload):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    rows = ["specimen_id,landmark_id,x,y,type,name"]
    sid = payload["specimen_id"]
    for lm in payload["landmarks"]:
        rows.append(
            f"{sid},{lm['id']},{lm['x']:.4f},{lm['y']:.4f},"
            f"{lm['type']},{lm['name']}"
        )
    Path(out_path).write_text("\n".join(rows) + "\n", encoding="utf-8")


def _save_excel(out_path, payload):
    try:
        from openpyxl import Workbook
    except ImportError:
        return False, "openpyxl not installed (pip install openpyxl)"
    wb = Workbook()
    ws = wb.active
    ws.title = payload["specimen_id"][:31] or "specimen"
    ws.append(["landmark_id", "x", "y", "type", "name"])
    for lm in payload["landmarks"]:
        ws.append([lm["id"], lm["x"], lm["y"], lm["type"], lm["name"]])
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    wb.save(out_path)
    return True, None


def export(payload, out_dir, formats, base_name):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = {}
    errors = {}
    for fmt in formats:
        fmt = fmt.strip().lower()
        target = out_dir / f"{base_name}.{fmt}"
        if fmt == "json":
            _save_json(target, payload); written["json"] = str(target)
        elif fmt == "tps":
            _save_tps(target, payload); written["tps"] = str(target)
        elif fmt == "csv":
            _save_csv(target, payload); written["csv"] = str(target)
        elif fmt in ("xlsx", "excel"):
            target = out_dir / f"{base_name}.xlsx"
            ok, err = _save_excel(target, payload)
            if ok: written["xlsx"] = str(target)
            else:  errors["xlsx"] = err
        else:
            errors[fmt] = "Unknown format"
    return written, errors


# ========== Main ==========

def main(argv=None):
    p = argparse.ArgumentParser(description="Extract N landmarks from a fossil silhouette image")
    p.add_argument("--image", required=True)
    p.add_argument("--num-landmarks", type=int, default=64)
    p.add_argument("--threshold", type=int, default=150,
                   help="Binarization threshold (0-255). Foreground = pixel <= threshold.")
    p.add_argument("--out-dir", default="morphometric_output")
    p.add_argument("--formats", default="json,tps,csv",
                   help="Comma-separated: json,tps,csv,xlsx")
    p.add_argument("--specimen-id", default=None,
                   help="ID for this specimen (default: image filename stem)")
    p.add_argument("--scale", type=float, default=1.0,
                   help="Scale factor for TPS (e.g. pixels per mm)")
    args = p.parse_args(argv)

    if not _PIL_OK:
        print_json({"error": "Pillow not installed. Run: pip install Pillow",
                    "image": args.image, "landmarks": []})
        return

    image_path = Path(args.image).expanduser().resolve()
    if not image_path.exists():
        print_json({"error": f"Image not found: {image_path}", "landmarks": []})
        return

    specimen_id = args.specimen_id or image_path.stem
    num = max(3, int(args.num_landmarks))
    thr = max(0, min(255, int(args.threshold)))

    try:
        mask, (w, h) = _load_binary_mask(image_path, thr)
    except (OSError, ValueError) as e:
        print_json({"error": f"Failed to load image: {e}", "image": str(image_path), "landmarks": []})
        return

    largest, comp_size = _largest_component(mask)
    if not largest or comp_size < num:
        print_json({"error": f"No usable foreground component (size={comp_size}, "
                             f"need ≥ {num}). Adjust --threshold.",
                    "image": str(image_path),
                    "image_size": {"width": w, "height": h},
                    "landmarks": []})
        return

    boundary = _trace_boundary(largest)
    if len(boundary) < num:
        print_json({"error": f"Boundary too short ({len(boundary)} pts < {num}). "
                             f"Image likely too small or shape too simple.",
                    "image": str(image_path), "landmarks": []})
        return

    pts = _resample(boundary, num)

    landmarks = [
        {"id": i + 1, "x": round(x, 4), "y": round(y, 4),
         "type": "semilandmark", "name": f"LM{i+1:02d}"}
        for i, (x, y) in enumerate(pts)
    ]

    payload = {
        "specimen_id": specimen_id,
        "image_path": str(image_path),
        "image_size": {"width": w, "height": h},
        "num_landmarks": num,
        "threshold": thr,
        "scale": float(args.scale),
        "landmarks": landmarks,
        "timestamp": dt.datetime.now(tz=dt.timezone.utc).isoformat(),
        "algorithm": "boundary-trace + arc-length-resample",
        "boundary_pixel_count": len(boundary),
        "component_size_px": comp_size,
    }

    written, errors = export(payload, args.out_dir, args.formats.split(","), specimen_id)

    print_json({
        "specimen_id": specimen_id,
        "image": str(image_path),
        "image_size": {"width": w, "height": h},
        "num_landmarks": num,
        "threshold": thr,
        "component_size_px": comp_size,
        "boundary_pixel_count": len(boundary),
        "files_written": written,
        "export_errors": errors,
        "landmarks_preview": landmarks[:5],
    })


if __name__ == "__main__":
    main()
