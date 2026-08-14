"""Robustness tests for convert.py (offline, no network).

Covers the bugs where malformed JSON or a fake .xls file crashed the script
with a raw traceback instead of a friendly JSON error.
"""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
_SKILLS = _ROOT / ".claude" / "skills" / "paleontology-research-skills"
sys.path.insert(0, str(_SKILLS / "paleo-morphometric-convert" / "scripts"))

import convert  # noqa: E402


class TestConvertRobustness(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        os.environ["PALEONTOLOGY_RESEARCH_SKILLS_HOME"] = str(self.tmp)

    def tearDown(self):
        os.environ.pop("PALEONTOLOGY_RESEARCH_SKILLS_HOME", None)

    def _run(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            convert.main(list(argv))
        return json.loads(buf.getvalue())

    def test_broken_json_returns_error_not_crash(self):
        p = self.tmp / "broken.json"
        p.write_text('{"broken": ', encoding="utf-8")
        out = self._run("--input", str(p), "--to", "tps", "--out", str(self.tmp / "o.tps"))
        self.assertIn("error", out)

    def test_fake_xls_returns_error_not_crash(self):
        p = self.tmp / "fake.xls"
        p.write_text("not a real xls", encoding="utf-8")
        out = self._run("--input", str(p), "--to", "tps", "--out", str(self.tmp / "o.tps"))
        self.assertIn("error", out)

    def test_valid_tps_roundtrip_still_works(self):
        p = self.tmp / "spec.tps"
        p.write_text("LM=3\n0.0  0.0\n1.0  1.0\n2.0  0.0\nID=spec1\n", encoding="utf-8")
        out = self._run("--input", str(p), "--to", "csv", "--out", str(self.tmp / "o.csv"))
        self.assertEqual(out["specimens_count"], 1)
        csv_text = (self.tmp / "o.csv").read_text(encoding="utf-8")
        self.assertEqual(csv_text.count("\n"), 4)  # header + 3 landmark rows

    def test_missing_input_reports_error(self):
        out = self._run("--input", str(self.tmp / "nope.tps"), "--to", "tps", "--out", "x")
        self.assertIn("error", out)


if __name__ == "__main__":
    unittest.main()
