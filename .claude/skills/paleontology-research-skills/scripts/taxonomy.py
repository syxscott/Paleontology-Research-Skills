"""Taxonomic name inference utilities for Paleontology Research Skills.

Pattern-based, offline taxon-name detection (no external service). Heuristic:
a capitalized word is treated as a taxon candidate unless it is a known
stopword, a geological period, a common scientific noun, or it fails the
length/suffix test.

The authoritative stopword / period lists live in the bundled JSON data files
(`data/stopwords.json`, `data/geological_periods.json`); the frozensets below
are loaded at import time, with built-in defaults as a fallback when the
data files are missing or unreadable.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

# ===== Built-in fallback lists (used only if the data files are missing) =====

_BUILTIN_TAXON_STOPWORDS = frozenset(
    {
        "Use",
        "Find",
        "Show",
        "List",
        "Get",
        "Query",
        "Search",
        "Look",
        "Check",
        "Give",
        "Tell",
        "What",
        "Which",
        "Where",
        "When",
        "Who",
        "How",
        "I",
        "We",
        "You",
        "They",
        "The",
        "This",
        "That",
        "These",
        "Those",
        "A",
        "An",
        "And",
        "Or",
        "But",
        "For",
        "With",
        "Without",
        "From",
        "Into",
        "Can",
        "Could",
        "Should",
        "Would",
        "May",
        "Might",
        "Must",
        "Will",
        "Shall",
        "Need",
        "Want",
        "Have",
        "Has",
        "Had",
        "Do",
        "Does",
        "Did",
        "Is",
        "Are",
        "Was",
        "Were",
        "Be",
        "Been",
        "Being",
        "Let",
        "Please",
        "About",
        "Above",
        "After",
        "Below",
        "Under",
        "Over",
        "Between",
        "Among",
        "During",
        "Before",
        "Open",
        "Close",
        "Start",
        "Stop",
        "Run",
        "Build",
        "Make",
        "Create",
        "Now",
        "Then",
        "Here",
        "There",
        "All",
        "Any",
        "Some",
        "No",
        "Not",
        "My",
        "Your",
        "His",
        "Her",
        "Its",
        "Our",
        "Their",
        "More",
        "Most",
        "Other",
        "Such",
        "Same",
        "Own",
        "Just",
        "Only",
        "Also",
        "Very",
        "Too",
        # Common scientific nouns that otherwise pass the length/suffix heuristic
        "Fossil",
        "Fossils",
        "Dinosaur",
        "Dinosaurs",
        "Mammal",
        "Mammals",
        "Species",
        "Specimen",
        "Specimens",
        "Skeleton",
        "Skeletons",
        "Bone",
        "Bones",
        "Teeth",
        "Tooth",
        "Skull",
        "Formation",
        "Group",
        "Member",
        "Fauna",
        "Flora",
        "Ecosystem",
        "Evidence",
        "Record",
        "Records",
        "Research",
        "Study",
        "Studies",
        "Paper",
        "Papers",
        "Journal",
        "Database",
        "Sample",
        "Samples",
        "Bed",
        "Site",
        "Section",
        "Remains",
        "Tissue",
        "Age",
        "Epoch",
        "Era",
        "Boundary",
        "Data",
        "Sediment",
        "Sediments",
    }
)

_BUILTIN_GEOLOGICAL_PERIODS = frozenset(
    {
        "Cambrian",
        "Ordovician",
        "Silurian",
        "Devonian",
        "Carboniferous",
        "Permian",
        "Triassic",
        "Jurassic",
        "Cretaceous",
        "Paleogene",
        "Neogene",
        "Quaternary",
        "Paleocene",
        "Eocene",
        "Oligocene",
        "Miocene",
        "Pliocene",
        "Pleistocene",
        "Holocene",
    }
)

# ===== Data loading: JSON files are authoritative, built-ins are fallback =====


def _load_lists():
    stopwords = set(_BUILTIN_TAXON_STOPWORDS)
    periods = set(_BUILTIN_GEOLOGICAL_PERIODS)
    data_dir = Path(__file__).resolve().parent.parent / "data"
    try:
        sw = json.loads((data_dir / "stopwords.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        sw = {}
    if isinstance(sw, dict):
        lst = sw.get("taxonStopwords")
        if isinstance(lst, list):
            stopwords.update(str(w) for w in lst)
        gl = sw.get("geologicalPeriods")
        if isinstance(gl, list):
            periods.update(str(w) for w in gl)
    try:
        gp = json.loads((data_dir / "geological_periods.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        gp = {}
    if isinstance(gp, dict):
        plist = gp.get("periods")
        if isinstance(plist, list):
            periods.update(str(p.get("name")) for p in plist if isinstance(p, dict) and p.get("name"))
    return frozenset(stopwords), frozenset(periods)


TAXON_STOPWORDS, GEOLOGICAL_PERIODS = _load_lists()

# Common Latin/scientific suffixes for taxa. We require EITHER a recognized
# suffix OR a length >= 6 to accept a candidate, which filters out most
# common English words like "Use" / "Find".
TAXON_SUFFIX_RE = re.compile(
    r"(idae|inae|aceae|opsida|phyta|mycota|formes|us|a|um|ia|yx|is|os|er|ix)$", re.IGNORECASE
)

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
