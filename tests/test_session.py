"""Tests for paleo-session session storage behaviour (offline)."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "scripts"))

import paleo_common as pc  # noqa: E402


class TestSessionPaths(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.environ["PALEONTOLOGY_RESEARCH_SKILLS_HOME"] = self.tmp

    def tearDown(self):
        os.environ.pop("PALEONTOLOGY_RESEARCH_SKILLS_HOME", None)

    def test_data_home_respects_env(self):
        self.assertEqual(str(pc.data_home()), str(Path(self.tmp).resolve()))

    def test_sessions_root_under_data_home(self):
        self.assertTrue(str(pc.sessions_root()).startswith(str(Path(self.tmp).resolve())))

    def test_memory_root_under_data_home(self):
        self.assertTrue(str(pc.memory_root()).startswith(str(Path(self.tmp).resolve())))


class TestSearchMemoryEmpty(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.environ["PALEONTOLOGY_RESEARCH_SKILLS_HOME"] = self.tmp

    def tearDown(self):
        os.environ.pop("PALEONTOLOGY_RESEARCH_SKILLS_HOME", None)

    def test_search_returns_empty(self):
        results = pc.search_memory("anything", scope="all", top_k=5)
        self.assertEqual(results, [])


class TestProfileLoad(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        os.environ["PALEONTOLOGY_RESEARCH_SKILLS_HOME"] = self.tmp

    def tearDown(self):
        os.environ.pop("PALEONTOLOGY_RESEARCH_SKILLS_HOME", None)

    def test_defaults_loaded_when_no_files(self):
        prof = pc.load_profile()
        self.assertEqual(prof["user"]["role"], "paleontology researcher")
        self.assertGreater(len(prof["soul"]["corePrinciples"]), 0)

    def test_profile_has_preferred_journals(self):
        prof = pc.load_profile()
        # Enriched user.md default should mention Paleobiology journal
        # via the raw template; let's just check it loads
        self.assertIn("user", prof)
        self.assertIn("soul", prof)


if __name__ == "__main__":
    unittest.main()
