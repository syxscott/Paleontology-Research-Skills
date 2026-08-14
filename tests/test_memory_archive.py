"""Regression tests for memory_archive timestamp handling (offline).

Covers the bug where a naive (timezone-less) timestamp crashed the script
with ``TypeError: can't compare offset-naive and offset-aware datetimes``.
"""

import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
_SKILLS = _ROOT / ".claude" / "skills" / "paleontology-research-skills"
sys.path.insert(0, str(_SKILLS / "paleo-memory" / "scripts"))

import memory_archive as ma  # noqa: E402


class TestMemoryArchiveTimestamps(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        os.environ["PALEONTOLOGY_RESEARCH_SKILLS_HOME"] = str(self.tmp)
        self.short = self.tmp / "memory" / "short"
        self.short.mkdir(parents=True)

    def tearDown(self):
        os.environ.pop("PALEONTOLOGY_RESEARCH_SKILLS_HOME", None)

    def _write(self, name, entry):
        (self.short / name).write_text(json.dumps(entry), encoding="utf-8")

    def _run(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            ma.main(list(argv))
        return json.loads(buf.getvalue())

    def test_naive_timestamp_does_not_crash(self):
        self._write("old.json", {"timestamp": "2020-01-01T10:00:00", "summary": "old"})
        out = self._run("--days", "30", "--dry-run")
        self.assertEqual(out["movedCount"], 1)

    def test_aware_timestamp_archives(self):
        self._write("old.json", {"timestamp": "2020-01-01T10:00:00+00:00", "summary": "old"})
        out = self._run("--days", "30", "--dry-run")
        self.assertEqual(out["movedCount"], 1)

    def test_fresh_entry_kept(self):
        now = datetime.now(timezone.utc).isoformat()
        self._write("fresh.json", {"timestamp": now, "summary": "fresh"})
        out = self._run("--days", "30", "--dry-run")
        self.assertEqual(out["kept"], 1)
        self.assertEqual(out["movedCount"], 0)

    def test_corrupt_json_skipped(self):
        # A corrupt entry falls back to file mtime (freshly written → kept),
        # and must never crash the archive run.
        (self.short / "bad.json").write_text("{not json", encoding="utf-8")
        out = self._run("--days", "30", "--dry-run")
        self.assertEqual(out["movedCount"], 0)


if __name__ == "__main__":
    unittest.main()
