"""Smoke tests for paleo_common shared utilities."""
import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", ".claude", "skills", "paleontology-research-skills", "scripts"))
sys.path.insert(0, _SHARED)

import paleo_common as pc  # noqa: E402


class TestPaleoCommon(unittest.TestCase):

    def test_data_home_returns_path(self):
        self.assertTrue(str(pc.data_home()))

    def test_load_profile_has_defaults(self):
        # Set PALEONTOLOGY_RESEARCH_SKILLS_HOME to a non-existent path so we get defaults
        os.environ["PALEONTOLOGY_RESEARCH_SKILLS_HOME"] = os.path.join(_HERE, "_does_not_exist")
        prof = pc.load_profile()
        self.assertIn("user", prof)
        self.assertIn("soul", prof)
        self.assertEqual(prof["user"]["role"], "paleontology researcher")

    def test_hashing_vector_is_deterministic(self):
        v1 = pc.hashing_vector("Allosaurus Morrison Formation")
        v2 = pc.hashing_vector("Allosaurus Morrison Formation")
        self.assertEqual(v1, v2)

    def test_cosine_similarity_self_is_one(self):
        v = pc.hashing_vector("Tyrannosaurus rex Hell Creek")
        sim = pc.cosine_similarity(v, v)
        self.assertAlmostEqual(sim, 1.0, places=5)

    def test_cosine_similarity_unrelated_is_low(self):
        a = pc.hashing_vector("Allosaurus Morrison Jurassic")
        b = pc.hashing_vector("Trilobite Cambrian Burgess Shale")
        sim = pc.cosine_similarity(a, b)
        self.assertLess(sim, 0.5)

    def test_normalize_taxon_finds_genus(self):
        self.assertEqual(pc.normalize_taxon("Find Allosaurus fossils please"), "Allosaurus")
        self.assertIsNone(pc.normalize_taxon("hi there"))

    def test_search_memory_empty(self):
        os.environ["PALEONTOLOGY_RESEARCH_SKILLS_HOME"] = os.path.join(_HERE, "_does_not_exist")
        results = pc.search_memory("anything", scope="all", top_k=3)
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
