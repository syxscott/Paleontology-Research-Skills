"""Taxonomic name inference utilities.

Extracted from OpenClaw v1.7.0 to be shared across all Paleontology Research Skills skills.
"""
from __future__ import annotations

import re
from typing import Optional

# Common English words that often appear as sentence-initial capitalized words
# but are not taxonomic names. We skip these when scanning for a taxon candidate
# to avoid passing words like "Use", "Find", "Show" to PBDB.
TAXON_STOPWORDS = frozenset({
    "Use", "Find", "Show", "List", "Get", "Query", "Search", "Look",
    "Check", "Give", "Tell", "What", "Which", "Where", "When", "Who", "How",
    "I", "We", "You", "They", "The", "This", "That", "These", "Those",
    "A", "An", "And", "Or", "But", "For", "With", "Without", "From", "Into",
    "Can", "Could", "Should", "Would", "May", "Might", "Must", "Will", "Shall",
    "Need", "Want", "Have", "Has", "Had", "Do", "Does", "Did", "Is", "Are",
    "Was", "Were", "Be", "Been", "Being", "Let", "Please", "About", "Above",
    "After", "Below", "Under", "Over", "Between", "Among", "During", "Before",
    "Open", "Close", "Start", "Stop", "Run", "Build", "Make", "Create",
    "Now", "Then", "Here", "There", "All", "Any", "Some", "No", "Not",
    "My", "Your", "His", "Her", "Its", "Our", "Their", "More", "Most",
    "Other", "Such", "Same", "Own", "Just", "Only", "Also", "Very", "Too",
})

# Geological periods / epochs / eras that should not be treated as taxa
GEOLOGICAL_PERIODS = frozenset({
    "Cambrian", "Ordovician", "Silurian", "Devonian", "Carboniferous",
    "Permian", "Triassic", "Jurassic", "Cretaceous",
    "Paleogene", "Neogene", "Quaternary",
    "Paleocene", "Eocene", "Oligocene", "Miocene", "Pliocene",
    "Pleistocene", "Holocene",
})

# Common Latin/scientific suffixes for taxa. We require EITHER a recognized
# suffix OR a length >= 6 to accept a candidate, which filters out most
# common English words like "Use" / "Find".
TAXON_SUFFIX_RE = re.compile(r"(idae|inae|aceae|opsida|phyta|mycota|formes|us|a|um|ia|yx|is|os|er|ix)$", re.IGNORECASE)

TAXON_NAME_RE = re.compile(r"\b([A-Z][a-z]{2,})\b")


def is_likely_taxon(word: str) -> bool:
    if not word:
        return False
    if word in TAXON_STOPWORDS:
        return False
    if word in GEOLOGICAL_PERIODS:
        return False
    if len(word) < 6 and not TAXON_SUFFIX_RE.search(word):
        return False
    return True


def extract_taxon_candidate(text: str) -> Optional[str]:
    """Return the first likely taxon name found in the text, or None."""
    for match in TAXON_NAME_RE.finditer(text or ""):
        candidate = match.group(1).strip()
        if is_likely_taxon(candidate):
            return candidate
    return None
