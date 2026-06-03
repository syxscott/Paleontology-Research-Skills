#!/usr/bin/env python3
"""Overlay landmarks on the original image as an annotated PNG."""
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

from paleo_common import print_json  # noqa: E402

try:
    from PIL import Image, ImageDraw, ImageFont
    _PIL_OK = True
except ImportError:
    _PIL_OK = False


def _load_landmarks(landmarks_arg):
    """Accepts either a path to landmarks JSON OR an inline JSON string."""
    p = Path(landmarks_arg)
    if p.exists():
        try:
            with p.open("r", encoding="utf-8") as f:
                return json.load(f), None
        except (json.JSONDecodeError, OSError) as e:
            return None, f"Failed to read {p}: {e}"
    try:
        return json.loads(landmarks_arg), None
    except json.JSONDecodeError:
        return None, "Argument is not a valid file path nor valid JSON"


def main(argv=None):
    p = argparse.ArgumentParser(description="Overlay landmarks on an image")
    p.add_argument("--image", required=True)
    p.add_argument("--landmarks", required=True,
                   help="Path to landmarks JSON (from extract_landmarks.py)")
    p.add_argument("--out", required=True, help="Output annotated PNG")
    p.add_argument("--point-size", type=int, default=4)
    p.add_argument("--point-color", default="#FF0000")
    p.add_argument("--line-color", default="#FF000080")
    p.add_argument("--number-color", default="#FFFFFF")
    p.add_argument("--show-numbers", action="store_true")
    p.add_argument("--show-connections", action="store_true")
    p.add_argument("--image-opacity", type=float, default=0.7,
                   help="0.0..1.0; lower = landmarks pop more")
    args = p.parse_args(argv)

    if not _PIL_OK:
        print_json({"error": "Pillow not installed. Run: pip install Pillow"})
        return

    img_path = Path(args.image)
    if not img_path.exists():
        print_json({"error": f"Image not found: {img_path}"})
        return

    payload, err = _load_landmarks(args.landmarks)
    if err or not isinstance(payload, dict):
        print_json({"error": err or "Invalid landmarks JSON"})
        return
    lms = payload.get("landmarks") or []
    if not lms:
        print_json({"error": "No landmarks in input"})
        return

    base = Image.open(img_path).convert("RGBA")
    # Fade base by image_opacity
    if 0.0 <= args.image_opacity <= 1.0:
        alpha = int(255 * args.image_opacity)
        overlay_bg = Image.new("RGBA", base.size, (255, 255, 255, 255 - alpha))
        base = Image.alpha_composite(base, overlay_bg)

    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    r = max(1, int(args.point_size))

    pts = [(float(lm["x"]), float(lm["y"])) for lm in lms]

    # Connecting polygon
    if args.show_connections and len(pts) >= 2:
        draw.polygon(pts, outline=args.line_color)

    # Landmark points
    for x, y in pts:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=args.point_color, outline=args.point_color)

    # Numbers
    if args.show_numbers:
        try:
            font = ImageFont.load_default()
        except OSError:
            font = None
        for i, (x, y) in enumerate(pts):
            draw.text((x + r + 1, y - r - 8), str(i + 1),
                      fill=args.number_color, font=font)

    out = Image.alpha_composite(base, overlay)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    out.convert("RGB").save(args.out)

    print_json({
        "input_image": str(img_path),
        "landmarks_count": len(pts),
        "output": str(args.out),
        "show_numbers": args.show_numbers,
        "show_connections": args.show_connections,
    })


if __name__ == "__main__":
    main()
