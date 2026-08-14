"""Smoke tests for taxonomy helpers."""

import os
import sys
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(
    os.path.join(_HERE, "..", ".claude", "skills", "paleontology-research-skills", "scripts")
)
sys.path.insert(0, _SHARED)

from taxonomy import extract_taxon_candidate, is_likely_taxon  # noqa: E402


class TestTaxonomy(unittest.TestCase):
    def test_stopwords_rejected(self):
        for w in ("Use", "Find", "Show", "What", "Where"):
            self.assertFalse(is_likely_taxon(w), f"{w} should be rejected")

    def test_periods_rejected(self):
        for w in ("Jurassic", "Cretaceous", "Permian"):
            self.assertFalse(is_likely_taxon(w))

    def test_taxon_accepted(self):
        for w in ("Allosaurus", "Tyrannosaurus", "Velociraptor", "Diplodocus"):
            self.assertTrue(is_likely_taxon(w), f"{w} should be accepted")

    def test_extract_first_candidate(self):
        self.assertEqual(extract_taxon_candidate("Please find Allosaurus fossils"), "Allosaurus")
        self.assertIsNone(extract_taxon_candidate("Hello world"))


class TestCommonNounRejection(unittest.TestCase):
    """Regression: common scientific nouns must not be treated as taxa."""

    def test_scientific_nouns_rejected(self):
        for w in (
            "Fossil",
            "Dinosaur",
            "Mammal",
            "Species",
            "Formation",
            "Sample",
            "Record",
            "Research",
            "Skeleton",
            "Evidence",
        ):
            self.assertFalse(is_likely_taxon(w), f"{w} should be rejected")

    def test_real_genera_still_accepted(self):
        for w in ("Allosaurus", "Tyrannosaurus", "Velociraptor", "Ammonites", "Trilobita", "Ichthyosauria"):
            self.assertTrue(is_likely_taxon(w), f"{w} should be accepted")

    def test_prompt_with_common_nouns(self):
        self.assertIsNone(extract_taxon_candidate("Show me Dinosaur data"))
        self.assertIsNone(extract_taxon_candidate("look at the Fossil record"))
        self.assertEqual(
            extract_taxon_candidate("what is the classification of Tyrannosaurus rex"),
            "Tyrannosaurus",
        )


if __name__ == "__main__":
    unittest.main()
