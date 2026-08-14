"""Tests for paleo-geo-time queries (offline ICS data)."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPT = (
    _HERE.parent
    / ".claude"
    / "skills"
    / "paleontology-research-skills"
    / "paleo-geo-time"
    / "scripts"
    / "geo_time_query.py"
)


def run(args):
    """Run the script as subprocess and parse JSON output."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(
        [sys.executable, str(_SCRIPT)] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        timeout=30,
    )
    return json.loads(r.stdout) if r.stdout else {}


class TestGeoTime(unittest.TestCase):
    def test_period_jurassic(self):
        d = run(["--period", "Jurassic"])
        self.assertEqual(len(d["matches"]), 1)
        m = d["matches"][0]
        self.assertEqual(m["name"], "Jurassic")
        self.assertAlmostEqual(m["startMa"], 201.4, places=1)
        self.assertAlmostEqual(m["endMa"], 145.0, places=1)
        self.assertAlmostEqual(m["durationMa"], 56.4, places=1)

    def test_period_case_insensitive(self):
        d_upper = run(["--period", "JURASSIC"])
        d_lower = run(["--period", "jurassic"])
        self.assertEqual(d_upper["matches"][0]["id"], d_lower["matches"][0]["id"])

    def test_nonexistent_period(self):
        d = run(["--period", "Foobarian"])
        self.assertEqual(d["matches"], [])

    def test_age_100_ma(self):
        d = run(["--age", "100"])
        # 100 Ma is Late Cretaceous - should match Phanerozoic, Mesozoic, Cretaceous, and a stage
        names = {m["name"] for m in d["matches"]}
        self.assertIn("Phanerozoic", names)
        self.assertIn("Mesozoic", names)
        self.assertIn("Cretaceous", names)

    def test_age_negative_returns_empty(self):
        d = run(["--age", "-100"])
        self.assertEqual(d["matches"], [])

    def test_list_periods(self):
        d = run(["--list", "--rank", "period"])
        self.assertEqual(d["count"], 12)  # 12 standard periods
        names = [m["name"] for m in d["matches"]]
        for p in ["Cambrian", "Jurassic", "Cretaceous", "Quaternary"]:
            self.assertIn(p, names)

    def test_list_mesozoic_periods(self):
        d = run(["--list", "--rank", "period", "--parent", "Mesozoic"])
        self.assertEqual(d["count"], 3)
        names = sorted(m["name"] for m in d["matches"])
        self.assertEqual(names, ["Cretaceous", "Jurassic", "Triassic"])

    def test_list_cenozoic_periods(self):
        d = run(["--list", "--rank", "period", "--parent", "Cenozoic"])
        self.assertEqual(d["count"], 3)
        names = sorted(m["name"] for m in d["matches"])
        self.assertEqual(names, ["Neogene", "Paleogene", "Quaternary"])


if __name__ == "__main__":
    unittest.main()
