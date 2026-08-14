"""Regression tests for session_list mixed naive/aware timestamp handling (offline).

Covers the bug where sorting sessions with a mixture of timezone-aware and
timezone-naive ``started_at`` values raised a TypeError.
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
sys.path.insert(0, str(_SKILLS / "paleo-session" / "scripts"))

import session_list  # noqa: E402


class TestSessionListMixedTimestamps(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        os.environ["PALEONTOLOGY_RESEARCH_SKILLS_HOME"] = str(self.tmp)
        self.sessions = self.tmp / "sessions"
        self.sessions.mkdir()

    def tearDown(self):
        os.environ.pop("PALEONTOLOGY_RESEARCH_SKILLS_HOME", None)

    def _write_session(self, name, started_at):
        (self.sessions / f"{name}.json").write_text(
            json.dumps({"session_id": name, "started_at": started_at, "title": name}),
            encoding="utf-8",
        )

    def test_mixed_timestamps_do_not_crash(self):
        self._write_session("naive", "2026-01-01T10:00:00")
        self._write_session("aware", "2026-01-01T10:00:00+00:00")
        buf = io.StringIO()
        with redirect_stdout(buf):
            session_list.main(["--limit", "20"])
        out = json.loads(buf.getvalue())
        self.assertEqual(out["count"], 2)

    def test_no_sessions_dir(self):
        os.rmdir(self.sessions)
        buf = io.StringIO()
        with redirect_stdout(buf):
            session_list.main(["--limit", "20"])
        out = json.loads(buf.getvalue())
        self.assertEqual(out["count"], 0)


if __name__ == "__main__":
    unittest.main()
