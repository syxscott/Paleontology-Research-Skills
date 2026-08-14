---
name: paleontology-research-skills
description: 🦕 Comprehensive paleontology research toolkit (12 sub-skills): fossil occurrence queries (PBDB), scholarly literature search across CrossRef + Semantic Scholar + arXiv, research memory recall, session history, research profile, ICS geological time scale, taxonomic classification, stratigraphic formation lookup, geometric morphometric landmark extraction, morphometric format conversion, automated literature-review pipeline, and Chinese paleontology news aggregation. Use when the user asks ANY question about fossils, geological time, taxonomy, scientific literature, stratigraphy, morphometrics, or their own research history.
---

# Paleontology Research Skills Research Toolkit

A research assistant toolkit for paleontology built on the [Agent Skills](https://agentskills.io/specification) standard.

This is the **wrapper / discovery entry point**. For specific tasks, load one of the focused sub-skills below. Each sub-skill is independently discoverable and targets one concrete capability.

## Sub-skills

| Sub-skill directory | Trigger this when the user… |
|---------------------|------------------------------|
| `paleontology-research-skills/paleo-profile/` | asks about their research preferences, role, or institution |
| `paleontology-research-skills/paleo-pbdb/`     | asks for fossil occurrences, PBDB data, or specimen localities |
| `paleontology-research-skills/paleo-crossref/` | asks for scientific literature, DOIs, citation metadata (CrossRef + Semantic Scholar + arXiv) |
| `paleontology-research-skills/paleo-memory/`   | asks "did I research X before" or wants prior findings |
| `paleontology-research-skills/paleo-session/`  | asks to list, show, search, or resume past sessions |
| `paleontology-research-skills/paleo-geo-time/` | asks about geological periods, epochs, or ages in Ma |
| `paleontology-research-skills/paleo-taxonomy/` | asks "what is the classification of X" or "what family is Y" — returns full kingdom→species hierarchy |
| `paleontology-research-skills/paleo-stratigraphy/` | asks about a formation/strata: age, location, dominant taxa, lithology |
| `paleontology-research-skills/paleo-morphometric/` | wants to extract geometric morphometric landmarks from a fossil image (TPS/CSV/Excel/JSON output) |
| `paleontology-research-skills/paleo-morphometric-convert/` | wants to convert landmark data between TPS / NTSys / CSV / JSON / Excel |
| `paleontology-research-skills/paleo-research-assistant/` | asks for a "literature review", "background research", or "comprehensive analysis" — orchestrates 5 sub-skills into one Markdown report |
| `paleontology-research-skills/paleo-china-news/` | asks for "中国最新化石发现" or news from Chinese paleontology sources |

## How to use this wrapper

1. Read the user's request.
2. Identify which sub-skill matches.
3. Read that sub-skill's `SKILL.md` for the exact procedure and arguments.
4. If the request touches multiple capabilities (e.g. "summarise my last session on Allosaurus"), call the sub-skills in order: `session` → `profile` → `memory`.

## Data location

User data is stored under `~/.paleontology-research-skills/` on POSIX systems or `%USERPROFILE%\.paleontology-research-skills\` on Windows. Override with the `PALEONTOLOGY_RESEARCH_SKILLS_HOME` environment variable.

| Subdirectory | Contents |
|--------------|----------|
| `soul.md`        | System identity & scientific principles |
| `user.md`        | Personal research preferences |
| `memory/short/`  | Short-term task memory (one JSON per task) |
| `memory/long_term.jsonl` | Promoted long-term memory (one JSON per line) |
| `memory/archive/short/` | Archived short-term memory |
| `sessions/`      | Session transcripts (one JSON per session) |

See `references/data-locations.md` for the full layout.

## Shared utilities

Sub-skill scripts can import shared utilities from the parent directory:

```python
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
from paleo_common import load_profile, normalize_taxon, data_home
```

Available utilities:
- `data_home()` — returns the Paleontology Research Skills data root
- `load_profile(force_reload=False)` — parses `soul.md` + `user.md`
- `normalize_taxon(text)` — extracts the most likely taxon name from a prompt
- `hashing_vector(text, dim=384)` — vectorise text for memory search
- `cosine_similarity(a, b)` — similarity between two vectors
- `search_memory(query, scope='all', top_k=3, min_score=0.12)` — search local memory
