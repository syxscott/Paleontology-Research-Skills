"""Tests for paleo-morphometric landmark extraction.

These tests require Pillow. They are skipped if Pillow is not installed.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from PIL import Image, ImageDraw
    _PIL_OK = True
except ImportError:
    _PIL_OK = False

_HERE = Path(__file__).resolve().parent
_SCRIPT_DIR = _HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "paleo-morphometric" / "scripts"
sys.path.insert(0, str(_SCRIPT_DIR))
sys.path.insert(0, str(_HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "scripts"))

import extract_landmarks  # noqa: E402


@unittest.skipUnless(_PIL_OK, "Pillow not installed")
class TestExtract(unittest.TestCase):

    def _make_ellipse(self, w=300, h=200, threshold=150):
        with tempfile.TemporaryDirectory() as td:
            img_path = Path(td) / "ellipse.png"
            img = Image.new("L", (w, h), 255)
            ImageDraw.Draw(img).ellipse((40, 30, w - 40, h - 30), fill=0)
            img.save(img_path)
            return img_path, td

    def test_resample_evenly(self):
        boundary = [(0, 0), (10, 0), (10, 10), (0, 10)]  # square
        pts = extract_landmarks._resample(boundary, 4)
        self.assertEqual(len(pts), 4)

    def test_resample_n_points(self):
        boundary = [(i, 0) for i in range(100)] + [(99, i) for i in range(100)]
        pts = extract_landmarks._resample(boundary, 16)
        self.assertEqual(len(pts), 16)

    def test_ellipse_extract_64(self):
        with tempfile.TemporaryDirectory() as td:
            img_path = Path(td) / "ellipse.png"
            img = Image.new("L", (300, 200), 255)
            ImageDraw.Draw(img).ellipse((40, 30, 260, 170), fill=0)
            img.save(img_path)

            mask, (w, h) = extract_landmarks._load_binary_mask(img_path, 150)
            self.assertEqual((w, h), (300, 200))

            largest, size = extract_landmarks._largest_component(mask)
            self.assertIsNotNone(largest)
            self.assertGreater(size, 1000)

            boundary = extract_landmarks._trace_boundary(largest)
            self.assertGreater(len(boundary), 100)

            pts = extract_landmarks._resample(boundary, 64)
            self.assertEqual(len(pts), 64)
            # All points should be inside the image
            for x, y in pts:
                self.assertTrue(0 <= x <= 300)
                self.assertTrue(0 <= y <= 200)

    def test_empty_white_image(self):
        with tempfile.TemporaryDirectory() as td:
            img_path = Path(td) / "blank.png"
            Image.new("L", (100, 100), 255).save(img_path)
            mask, _ = extract_landmarks._load_binary_mask(img_path, 150)
            largest, size = extract_landmarks._largest_component(mask)
            self.assertEqual(size, 0)
            self.assertIsNone(largest)


if __name__ == "__main__":
    unittest.main()
