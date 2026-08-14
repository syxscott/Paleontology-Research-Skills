"""Shared utilities for the Paleontology Research Skills skills."""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from pathlib import Path

# ===== Paths =====


def data_home() -> Path:
    override = os.environ.get("PALEONTOLOGY_RESEARCH_SKILLS_HOME")
    if override and override.strip():
        return Path(override).expanduser().resolve()
    return (Path.home() / ".paleontology-research-skills").resolve()


def memory_root() -> Path:
    return data_home() / "memory"


def sessions_root() -> Path:
    return data_home() / "sessions"


def profile_files():
    h = data_home()
    return h / "soul.md", h / "user.md"


# ===== File I/O =====


def read_text_file(path, default=""):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return default


def write_text_file(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(content, encoding="utf-8")


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def write_json(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


# Profile parsing
_HEADING_RE = re.compile(r"^#{2,3}\s+(.+?)\s*:?\s*$")
_ITEM_RE = re.compile(r"^(?:[-*]|\d+\.)\s+(.+)$")
_HR_RE = re.compile(r"^[-*_]{3}$")


def split_sections(md):
    sec = {}
    cur = ""
    for line in md.split("\n"):
        m = _HEADING_RE.match(line)
        if m:
            cur = m.group(1).strip().lower().rstrip(":")
            sec[cur] = []
        elif cur and line.strip():
            sec[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in sec.items()}


def _section_items(text):
    items = []
    for line in text.split("\n"):
        t = line.strip()
        if not t or _HR_RE.match(t):
            continue
        m = _ITEM_RE.match(t)
        if m:
            items.append(m.group(1).strip())
            continue
        if ":" in t:
            v = t.split(":", 1)[1].strip()
            if v:
                items.append(v)
                continue
        if len(t) > 2:
            items.append(t)
    seen, uniq = set(), []
    for i in items:
        k = i.lower().strip()
        if k and k not in seen:
            seen.add(k)
            uniq.append(i)
    return uniq


def _kv(text, key, default=""):
    m = re.search(rf"^{re.escape(key)}\s*:\s*(.+)$", text, flags=re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else default


def load_profile():
    sp, up = profile_files()
    s = read_text_file(sp, _DEFAULT_SOUL)
    u = read_text_file(up, _DEFAULT_USER)
    ss = split_sections(s)
    us = split_sections(u)
    role = _kv(us.get("identity", ""), "Role", "paleontology researcher")
    domain = _kv(us.get("identity", ""), "Domain", "vertebrate paleontology")
    inst = _kv(us.get("identity", ""), "Institution", "")
    lang = us.get("language preference", "")
    out_lang = _kv(lang, "Output language", "Chinese")
    pref_lang = _kv(lang, "Preferred language", "Chinese or English")
    d = us.get("data preferences", "")
    try:
        lim = int(_kv(d, "Default occurrence limit", "50") or "50")
    except ValueError:
        lim = 50
    pre = _kv(d, "Include preprints", "false").lower() == "true"
    oa = _kv(d, "Prefer open access", "true").lower() == "true"
    safety = _section_items(ss.get("safety boundaries", "")) or _section_items(
        ss.get("paleontology-research-skills must not", "")
    )
    return {
        "soul": {
            "identity": ss.get("identity", "").strip(),
            "mission": (_section_items(ss.get("mission", "")) or [""])[0],
            "corePrinciples": _section_items(ss.get("core principles", "")),
            "executionRules": _section_items(ss.get("execution rules", "")),
            "safetyBoundaries": safety,
            "domainScope": {
                "inScope": _section_items(ss.get("in scope", "")),
                "outOfScope": _section_items(ss.get("out of scope", "")),
            },
        },
        "user": {
            "role": role,
            "domain": domain,
            "institution": inst,
            "researchFocus": {
                "primaryInterests": _section_items(us.get("primary interests", "")),
                "preferredPeriods": _section_items(us.get("preferred geological periods", "")),
                "preferredRegions": _section_items(us.get("preferred regions", "")),
            },
            "languagePreference": pref_lang,
            "outputLanguage": out_lang,
            "communicationStyle": _section_items(us.get("communication style", "")),
            "dataPreferences": {
                "defaultOccurrenceLimit": lim,
                "includePreprints": pre,
                "preferOpenAccess": oa,
                "citationFormat": _kv(d, "Citation format", "APA"),
            },
        },
    }


# Memory primitives
_TOK = re.compile(r"[A-Za-z0-9_]+")


def tokenize(text):
    return [t.lower() for t in _TOK.findall(text or "")]


def hashing_vector(text, dim=384):
    counts = {}
    for tok in tokenize(text):
        h = hashlib.md5(tok.encode("utf-8")).hexdigest()
        idx = int(h[:8], 16) % dim
        sign = 1.0 if int(h[8:10], 16) % 2 == 0 else -1.0
        counts[idx] = counts.get(idx, 0.0) + sign
    norm = math.sqrt(sum(v * v for v in counts.values()))
    if norm == 0:
        return {}
    return {k: v / norm for k, v in counts.items()}


def cosine_similarity(a, b):
    if not a or not b:
        return 0.0
    small, big = (a, b) if len(a) < len(b) else (b, a)
    return sum(v * big.get(k, 0.0) for k, v in small.items())


# Defaults
_DEFAULT_SOUL = """## Identity
Paleontology Research Skills is an AI research assistant specialized in paleontology and geosciences.

## Mission
Help users conduct reliable, reproducible paleontological research.

## Core Principles
- Scientific Integrity: never fabricate data, taxa, or papers.
- Verifiability: all claims must be traceable to primary sources.
- Transparency: clearly state data sources and uncertainties.
- Reproducibility: document all queries and parameters.
- Humility: acknowledge limits of current knowledge.

## Data Source Hierarchy
- Paleobiology Database (PBDB) - primary fossil data
- CrossRef - peer-reviewed literature metadata
- Semantic Scholar - citation analysis
- arXiv - preprints (clearly marked)
- NCBI Taxonomy - auxiliary taxonomic data
- Wikidata - cross-reference only

## Execution Rules
- Always verify taxonomic names via PBDB before use.
- Always include DOI for paper citations.
- Always report age ranges with uncertainty (in Ma).
- Always distinguish fact from hypothesis.
- Always note when data is incomplete or disputed.

## Safety Boundaries
- Do not fabricate species names or fossil occurrences.
- Do not invent paper citations or DOIs.
- Do not claim certainty where none exists.
- Do not access paywalled content through unauthorized means.
- Do not provide identification services for commercial fossil trading.
- Do not replace peer review or expert consultation.

## Domain Scope
### In Scope:
- Paleontology (all periods, all taxa)
- Stratigraphy and geological time
- Taxonomy and systematics
- Paleobiology and paleoecology
- Taphonomy and fossil preservation
- Scientific literature analysis

### Out of Scope:
- Modern organism identification
- Commercial fossil appraisal
- Geological resource exploration
- Archaeological artifact analysis
- Creation science or pseudoscience
"""


_DEFAULT_USER = """## Identity
Role: paleontology researcher
Domain: vertebrate paleontology
Institution: (unset)

## Research Focus
### Primary interests:
- Theropod dinosaurs
- Jurassic stratigraphy
- Chinese formations (Yixian, Jiufotang, Shishugou)
- Dinosaur ontogeny and growth
- Paleoecology and paleoenvironment

### Preferred geological periods:
- Jurassic
- Cretaceous

### Preferred regions:
- China (Liaoning, Xinjiang, Sichuan, Yunnan)
- Mongolia
- North America (Hell Creek, Morrison)

## Language Preference
Preferred language: Chinese or English
Output language: Chinese (simplified)

## Communication Style
- Structured scientific responses
- Formal taxonomic nomenclature (italicised genus/species)
- Concise summaries with detailed appendices
- Step-by-step workflow documentation
- Clear distinction between established facts and hypotheses

## Data Preferences
Default occurrence limit: 50
Include preprints: false
Prefer open access: true
Citation format: APA

## Preferred Journals
- Paleobiology
- Cretaceous Research
- Journal of Vertebrate Paleontology
- Nature Communications
- Science Bulletin
- Geological Society of America Bulletin
- Palaeogeography, Palaeoclimatology, Palaeoecology
- Acta Palaeontologica Polonica
- Vertebrata PalAsiatica

## Output Preferences
- Markdown reports
- Structured bibliographies with DOIs
- Chronological data tables
- Geographic distribution summaries
- Reproducible workflow documentation

## Reproducibility Expectations
- Document all query parameters
- Save intermediate results
- Version-control research workflows
- Explicit data source citations
- Method transparency

## Workflow Habits
- Prefer incremental literature reviews
- Prioritise PBDB-verified taxonomic data
- Cross-reference multiple data sources
- Maintain research notes in Obsidian
- Regular data backup
- Weekly research summaries

## Privacy and Safety
- Store research data locally
- Never expose API keys in outputs
- Respect data provider terms of service
- Secure backup of sensitive research data

## Long-term Constraints and Habits
- Prefer open-access publications when available
- Prioritise Chinese fossil localities
- Focus on well-preserved specimens
- Emphasise quantitative analyses
- Maintain collaboration network

## Collaboration Expectations
- Share reproducible workflows
- Credit data sources appropriately
- Respect peer-review confidentiality
- Contribute to community databases (PBDB)
"""


# ===== Taxon normalisation (delegated to taxonomy.py) =====
import sys as _sys  # noqa: E402 - deliberate late import to break cycles

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)
try:
    from taxonomy import extract_taxon_candidate as _extract_taxon
except ImportError:
    _extract_taxon = None


def normalize_taxon(text):
    """Return the most likely taxon name in *text* or None.

    Thin wrapper around :func:`taxonomy.extract_taxon_candidate` so that
    every Paleontology Research Skills sub-skill can ``from paleo_common import normalize_taxon``.
    """
    if _extract_taxon is None:
        return None
    return _extract_taxon(text or "")


# ===== Memory iteration & search =====


def _iter_short_memory():
    short = memory_root() / "short"
    if not short.exists():
        return
    for f in sorted(short.glob("*.json")):
        d = read_json(f, default=None)
        if isinstance(d, dict):
            d.setdefault("task_id", f.stem)
            d.setdefault("source", "short")
            yield d


def _iter_long_memory():
    f = memory_root() / "long_term.jsonl"
    if not f.exists():
        return
    try:
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(d, dict):
                d.setdefault("source", "long")
                yield d
    except OSError:
        return


def _iter_archive_memory():
    arch = memory_root() / "archive" / "short"
    if not arch.exists():
        return
    for f in sorted(arch.glob("*.json")):
        d = read_json(f, default=None)
        if isinstance(d, dict):
            d.setdefault("task_id", f.stem)
            d.setdefault("source", "archive")
            yield d


def _entry_text(entry):
    parts = []
    for key in ("command", "summary", "conclusion", "error", "title", "notes"):
        v = entry.get(key)
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, (list, tuple)):
            parts.extend(str(x) for x in v)
    return " ".join(parts)


def search_memory(query, scope="all", top_k=3, min_score=0.12):
    """Search the user's local memory using hashing-trick vectors."""
    qvec = hashing_vector(query or "")
    if not qvec:
        return []
    iters = []
    if scope in ("all", "short"):
        iters.append(_iter_short_memory())
    if scope in ("all", "long"):
        iters.append(_iter_long_memory())
    if scope in ("all", "archive"):
        iters.append(_iter_archive_memory())
    hits = []
    for it in iters:
        for entry in it:
            text = _entry_text(entry)
            if not text:
                continue
            score = cosine_similarity(qvec, hashing_vector(text))
            if score >= min_score:
                e = dict(entry)
                e["score"] = round(score, 4)
                hits.append(e)
    hits.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    return hits[: max(1, int(top_k))]
