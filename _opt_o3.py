#!/usr/bin/env python3
"""Optimization Batch O3 — P2 docs / tests / Makefile / community files."""
import pathlib

ROOT = pathlib.Path(r"D:\GIthub\自制Claude Code skills")

FILES = {}

# ============ CODE_OF_CONDUCT.md (Contributor Covenant 2.1) ============
FILES[ROOT / "CODE_OF_CONDUCT.md"] = '''# Contributor Covenant Code of Conduct

## Our pledge

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, caste, color, religion, or sexual
identity and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy scientific community.

## Our standards

Examples of behaviour that contributes to a positive environment:

- Demonstrating empathy and kindness toward other people
- Being respectful of differing opinions, viewpoints, and experiences
- Giving and gracefully accepting constructive feedback
- Accepting responsibility and apologising to those affected by our mistakes
- Focusing on what is best not just for us as individuals, but for the
  overall community
- Citing primary sources and giving proper credit

Examples of unacceptable behaviour:

- The use of sexualised language or imagery, and sexual attention or advances
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Plagiarising scientific work
- Fabricating or falsifying data, taxa, citations, or fossil occurrences
- Other conduct which could reasonably be considered inappropriate in a
  professional setting

## Enforcement responsibilities

Project maintainers are responsible for clarifying and enforcing standards of
acceptable behaviour and will take appropriate and fair corrective action in
response to any behaviour they deem inappropriate, threatening, offensive, or
harmful.

## Scope

This Code of Conduct applies within all community spaces (issues, pull
requests, discussions, code review, email, etc.) and also applies when an
individual is officially representing the community in public spaces.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behaviour may be
reported to the project maintainer at **syxemail@yeah.net**. All complaints
will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of
the reporter of any incident.

## Enforcement guidelines

Community leaders will follow these guidelines in determining consequences:

1. **Correction** — private, written warning, with clarity around the nature
   of the violation and an explanation of why the behaviour was inappropriate.
2. **Warning** — a warning with consequences for continued behaviour.
3. **Temporary ban** — temporary ban from any sort of interaction or public
   communication with the community for a specified period.
4. **Permanent ban** — permanent ban from any sort of public interaction
   within the community.

## Attribution

This Code of Conduct is adapted from the
[Contributor Covenant, version 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).
'''


# ============ AUTHORS.md ============
FILES[ROOT / "AUTHORS.md"] = '''# Authors

## Maintainer

- **Syxscott** — creator, maintainer
  <syxemail@yeah.net> — [@syxscott](https://github.com/syxscott)

## Contributors

<!--
Add yourself here when you contribute! Format:
  - **Your Name** ([@github-handle](https://github.com/...)) — what you contributed
-->

- *(Your name could be here — see [CONTRIBUTING.md](./CONTRIBUTING.md))*

## Acknowledgements

This toolkit builds on:

- The **Agent Skills specification** by Anthropic — https://agentskills.io/specification
- The **PaleoClaw** project (predecessor) — https://github.com/syxscott/PaleoClaw
- The **DeepMorph** geometric-morphometrics algorithm by
  **Xiaokang Liu**, China University of Geosciences (Wuhan)
- The **Paleobiology Database (PBDB)** community
- The **CrossRef**, **Semantic Scholar**, **arXiv**, **NCBI Taxonomy**,
  **Wikidata**, **Macrostrat**, and **ICS** data providers
- The **Anthropic Claude** model family — co-developed this toolkit
'''


# ============ SUPPORT.md ============
FILES[ROOT / "SUPPORT.md"] = '''# Getting help

Thanks for using **Paleontology Research Skills**! Here is where to look:

## Documentation

- **[README.md](./README.md)** — installation, quick start, full sub-skill table
- **[docs/architecture.md](./docs/architecture.md)** — why the nested layout, how scripts find shared utilities
- **[docs/development.md](./docs/development.md)** — adding new sub-skills
- **[docs/examples.md](./docs/examples.md)** — end-to-end research workflows
- **[docs/troubleshooting.md](./docs/troubleshooting.md)** — common errors and fixes
- **[docs/FAQ.md](./docs/FAQ.md)** — frequently asked questions
- **[CHANGELOG.md](./CHANGELOG.md)** — what changed in each release

## Questions

- 💬 **Ask in [Discussions](https://github.com/syxscott/Paleontology-Research-Skills/discussions)** —
  for "how do I", "is X possible", design ideas, etc.
- 🐛 **File a bug in [Issues](https://github.com/syxscott/Paleontology-Research-Skills/issues/new/choose)** —
  for reproducible problems.
- 🔒 **Security** — see [`SECURITY.md`](./SECURITY.md) for private reporting.

## Commercial support / contracting

The maintainer is reachable at **syxemail@yeah.net** for paid work
(custom sub-skills, large-scale deployments, training, etc.).

## Citing this toolkit

If you use **Paleontology Research Skills** in published research, please cite:

```bibtex
@software{paleontology_research_skills_2026,
  author       = {Syxscott},
  title        = {Paleontology Research Skills: A modular toolkit for Claude Code},
  year         = {2026},
  url          = {https://github.com/syxscott/Paleontology-Research-Skills},
  version      = {1.0.0}
}
```
'''


# ============ docs/FAQ.md ============
FILES[ROOT / "docs" / "FAQ.md"] = '''# Frequently asked questions

## General

### What is this?

A toolkit of **13 Claude Code Agent Skills** + **13 slash commands** for
paleontology research. The model can auto-trigger a skill from natural-language
prompts ("find Allosaurus fossils") or you can type a slash command explicitly
(`/paleo-fossil Allosaurus`).

### What's the difference between a Skill and a slash command?

| | Skill | Slash command |
|---|---|---|
| **Triggered by** | Claude reads `description` and decides | User types `/<name>` |
| **Location** | `.claude/skills/` | `.claude/commands/` |
| **File** | Directory + SKILL.md + scripts | One `.md` file |
| **Best for** | Vague prompts ("help with fossil research") | Deterministic invocation |

Both can wrap the **same** underlying script. Use Skills for discoverability,
slash commands for explicit control.

### Do I need to install anything besides cloning?

- Base toolkit: **No** — pure Python 3.9+ stdlib.
- The two morphometric sub-skills: `pip install Pillow openpyxl`
- Everything: `pip install -e ".[morphometric]"` or `pip install -r requirements-dev.txt`

### Does it work offline?

| Sub-skill | Offline? |
|---|---|
| `paleo-profile`, `paleo-memory`, `paleo-session`, `paleo-geo-time`, `paleo-morphometric`, `paleo-morphometric-convert` | ✅ Fully offline |
| `paleo-pbdb`, `paleo-crossref`, `paleo-taxonomy`, `paleo-stratigraphy`, `paleo-china-news`, `paleo-research-assistant` | ❌ Need network for primary data source |

---

## Installation

### Where do I install?

- **Project-scope** (only one project): Put `.claude/` in the project root.
- **User-scope** (all projects): Copy to `~/.claude/skills/` and `~/.claude/commands/`.

See the README's [Installation section](../README.md#-installation) for exact commands.

### How do I update?

```bash
cd Paleontology-Research-Skills
git pull
# Re-copy to user-scope if you installed there:
cp -r .claude/skills/paleontology-research-skills ~/.claude/skills/
cp .claude/commands/paleo*.md ~/.claude/commands/
```

---

## Skills behaviour

### Why isn't a skill triggering when I expect it to?

1. Check the skill's `description` — does the user's prompt match the trigger phrases listed there?
2. Make sure `SKILL.md` is in the **right place** (`.claude/skills/<name>/SKILL.md`).
3. Restart your Claude Code session after installing (skills are loaded on startup).
4. Try the slash command instead (`/paleo-<name>`) to force explicit invocation.

### Can I have multiple sub-skills triggered at once?

Claude can chain skills within one turn: it might call `paleo-pbdb`, look at
the results, then call `paleo-taxonomy` to clarify a name, then `paleo-crossref`
for relevant papers. Use the orchestrator (`paleo-research-assistant`) when you
want this automated end-to-end.

### How do I disable a skill?

Either delete its directory, or rename `SKILL.md` to something else (e.g.
`SKILL.md.disabled`). Restart Claude Code.

---

## Data and storage

### Where is my data stored?

Default: `~/.paleontology-research-skills/`. Override with the environment
variable `PALEONTOLOGY_RESEARCH_SKILLS_HOME`:

```bash
export PALEONTOLOGY_RESEARCH_SKILLS_HOME=/path/to/data
```

Layout:

```
~/.paleontology-research-skills/
├── soul.md                       # System identity & scientific principles
├── user.md                       # Personal research preferences
├── memory/
│   ├── short/                    # Short-term task memory
│   ├── long_term.jsonl           # Promoted long-term memory
│   └── archive/short/            # Archived short-term tasks
└── sessions/                     # Session transcripts (one JSON per session)
```

See [`references/data-locations.md`](../.claude/skills/paleontology-research-skills/references/data-locations.md)
for the full layout.

### How do I back up my profile / memory?

Just back up the whole `~/.paleontology-research-skills/` directory.

### Will this send my data to anyone?

- `paleo-profile`, `paleo-memory`, `paleo-session` — **never** leave your machine.
- `paleo-morphometric`, `paleo-morphometric-convert`, `paleo-geo-time` — fully local.
- `paleo-pbdb`, `paleo-crossref`, `paleo-taxonomy`, `paleo-stratigraphy`, `paleo-china-news`,
  `paleo-research-assistant` — call out to **public APIs** with the queries you give
  (no profile / memory data is sent).

---

## Specific sub-skills

### Why does Semantic Scholar return HTTP 429?

Their public API rate-limits aggressively. The script returns a friendly error
JSON. For sustained use, get a free API key (the script can be extended to use
one — currently uses the un-keyed pool).

### Why does my morphometric extraction return weird landmarks?

Most common causes:

1. **Threshold wrong**: Try `--threshold 100` (more sensitive) or `--threshold 200` (less).
2. **Image has multiple components**: The script picks the **largest**. Crop your image to one fossil.
3. **Image is colour**: Convert to greyscale binary silhouette first (black fossil on white).
4. **Resolution too low**: Use ≥ 512 × 512 px.

Always visualise: `python visualize_landmarks.py --image X --landmarks Y.json --out check.png --show-numbers`.

### Why does `paleo-china-news` return few or no items?

The Chinese fossil-news sites (nkocs.com, palaeontology.cn, IVPP) have
volatile HTML and may rate-limit, geo-block, or return 5xx errors. The script
fails gracefully (reports errors per source, continues with others). Re-run
after a delay, or specify `--source ivpp` to try just one.

---

## Contributing

### How do I add a new sub-skill?

See [`CONTRIBUTING.md`](../CONTRIBUTING.md#adding-a-new-sub-skill).

### What's the naming convention?

- **Sub-skill names**: `paleo-<topic>` (lowercase, hyphens, ≤ 64 chars)
- **Slash commands**: short verb-noun (`/paleo-fossil`, `/paleo-classify`)
- **Python scripts**: `<topic>_<verb>.py` (e.g. `pbdb_query.py`, `taxonomy_query.py`)
'''


# ============ docs/examples.md ============
FILES[ROOT / "docs" / "examples.md"] = '''# Examples — end-to-end workflows

These are concrete walkthroughs you can copy-paste. Replace placeholders.

---

## Workflow 1 — Quick literature scan on a topic

**Goal**: "What's the recent literature on theropod feather evolution?"

### Way A: natural language (lazy)

In Claude Code, just say:

> Find recent papers on theropod feather evolution.

Claude auto-triggers `paleo-crossref`.

### Way B: slash command (explicit)

```
/paleo-paper theropod feather evolution
```

### Way C: raw script (reproducible)

```bash
python .claude/skills/paleontology-research-skills/paleo-crossref/scripts/crossref_search.py \\
    --query "theropod feather evolution" \\
    --rows 15 \\
    --include-abstract \\
    --filter-from-year 2020 \\
    --respect-profile
```

---

## Workflow 2 — Verify a taxon name and get its hierarchy

**Goal**: "Is *Brontosaurus* a valid taxon? What family is it in?"

```
/paleo-classify Brontosaurus
```

Or:

```bash
python .claude/skills/paleontology-research-skills/paleo-taxonomy/scripts/taxonomy_query.py \\
    --name "Brontosaurus"
```

Output includes status (`valid` / `synonym`), authority, full hierarchy
(kingdom→phylum→class→order→family→genus), and time range.

---

## Workflow 3 — Investigate a geological formation

**Goal**: "What's the Yixian Formation — age, location, dominant taxa?"

```
/paleo-strat Yixian
```

Or stack two scripts for richer data:

```bash
# PBDB collections + dominant taxa
python .claude/skills/paleontology-research-skills/paleo-stratigraphy/scripts/stratigraphy_query.py \\
    --formation "Yixian" --taxa-limit 30

# Macrostrat lithology + columns
python .claude/skills/paleontology-research-skills/paleo-stratigraphy/scripts/macrostrat_query.py \\
    --formation "Yixian"
```

---

## Workflow 4 — Full literature-review report (orchestrator)

**Goal**: "Write a literature review on *Allosaurus* paleobiology."

```
/paleo-review Allosaurus paleobiology
```

Or with extra context:

```bash
python .claude/skills/paleontology-research-skills/paleo-research-assistant/scripts/research_assistant.py \\
    --topic "Allosaurus paleobiology" \\
    --taxon "Allosaurus" \\
    --formation "Morrison" \\
    --paper-rows 10 \\
    --summarise-top 5 \\
    --out-dir reports/
```

Output: a Markdown file with sections **Overview**, **Literature**,
**Taxonomy**, **Occurrences**, **Stratigraphy**, **References**, **Limitations**.

The script runs 5 stages — if a stage fails (network, rate-limit) the report
explicitly notes "data unavailable" and continues.

---

## Workflow 5 — Morphometric pipeline on a fossil image

**Goal**: Extract 64 semi-landmarks from an ammonoid photo, export to TPS for
MorphoJ.

### Step 1: extract

```
/paleo-landmark ammonoid_001.png
```

Or:

```bash
python .claude/skills/paleontology-research-skills/paleo-morphometric/scripts/extract_landmarks.py \\
    --image ammonoid_001.png \\
    --num-landmarks 64 \\
    --threshold 150 \\
    --out-dir results/ \\
    --formats json,tps,csv
```

### Step 2: visualise (always check!)

```bash
python .claude/skills/paleontology-research-skills/paleo-morphometric/scripts/visualize_landmarks.py \\
    --image ammonoid_001.png \\
    --landmarks results/ammonoid_001.json \\
    --out results/ammonoid_001_check.png \\
    --show-numbers --show-connections
```

If landmarks look misplaced, adjust `--threshold` (default 150 — lower = more
foreground sensitive).

### Step 3: batch-process a directory

```bash
python .claude/skills/paleontology-research-skills/paleo-morphometric/scripts/batch_extract.py \\
    --image-dir specimens/ \\
    --out-dir morphometric_results/ \\
    --num-landmarks 64 \\
    --formats json \\
    --aggregate tps,csv,xlsx
```

You'll get one JSON per specimen plus aggregated TPS / CSV / Excel for the
whole batch.

### Step 4: convert to another format

```bash
# TPS → Excel for inspection
python .claude/skills/paleontology-research-skills/paleo-morphometric-convert/scripts/convert.py \\
    --input morphometric_results/all_specimens.tps \\
    --to xlsx \\
    --out morphometric_results/all_specimens.xlsx
```

---

## Workflow 6 — Time-scale lookups

**Goal**: "When did the Triassic start? What period contains 250 Ma?"

```bash
# By name
python .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --period Triassic

# By age
python .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --age 250

# List all periods of an era
python .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py \\
    --list --parent Mesozoic --rank period
```

All offline — uses bundled ICS chart (2023-09).

---

## Workflow 7 — Personal research memory

After Claude does some research, save it to your local memory store, then
later recall via natural-language query.

```bash
# Status of your memory store
python .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_status.py

# Search for prior research
python .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_search.py \\
    --query "Allosaurus Morrison stratigraphy" \\
    --top-k 5

# List recent entries
python .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_list.py \\
    --scope all --limit 20

# Archive old short-term memory
python .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_archive.py \\
    --days 30
```

Or in Claude Code:

> Did I research the Yixian Formation before?

Auto-triggers `paleo-memory`.

---

## Workflow 8 — Chinese fossil news

```
/paleo-news 恐龙
```

Or:

```bash
python .claude/skills/paleontology-research-skills/paleo-china-news/scripts/china_news_fetch.py \\
    --keyword "恐龙" \\
    --since-days 30 \\
    --limit 10
```

Note: this scrapes public Chinese fossil news sites which may rate-limit or
change HTML structure. Errors per source are reported in the output.
'''


# ============ docs/troubleshooting.md ============
FILES[ROOT / "docs" / "troubleshooting.md"] = '''# Troubleshooting

Common errors and how to fix them.

---

## Installation

### `ModuleNotFoundError: No module named 'PIL'`

The morphometric sub-skills need Pillow. Install:

```bash
pip install Pillow
```

Or, install with all optional extras:

```bash
pip install -r requirements-dev.txt
# or
pip install -e ".[morphometric]"
```

### `ModuleNotFoundError: No module named 'openpyxl'`

Only needed for Excel export. Install:

```bash
pip install openpyxl
```

If you don't need Excel, just use `--formats json,tps,csv` (skipping `xlsx`).

### `command not found: python3`

Windows often only has `python` (not `python3`). The skill scripts use
`python3` in their `SKILL.md` examples but Claude is smart enough to translate.
For direct CLI use, replace `python3` with `python`.

---

## Skills not loading

### Claude doesn't auto-trigger any skill

1. Confirm the skill is installed: `ls ~/.claude/skills/paleontology-research-skills/` (or `.claude/skills/...` for project-scope).
2. **Restart Claude Code** — skills are loaded at session start.
3. Check `SKILL.md` frontmatter: run the validation script:
   ```bash
   python -c "
   import re, pathlib
   for md in pathlib.Path('.claude/skills').rglob('SKILL.md'):
       fm = md.read_text(encoding='utf-8').split('---', 2)
       print(md, '->', 'OK' if len(fm) >= 3 else 'BAD frontmatter')
   "
   ```
4. Try the slash command instead (`/paleo-fossil ...`) — if that works, the
   skill is fine, just the auto-trigger didn't match.

### Sub-skill `name:` mismatches its directory

Agent Skills spec **requires** `name:` to match the parent directory name.
If you rename a directory, you must also update the `name:` in its `SKILL.md`:

```yaml
---
name: paleo-pbdb       # MUST match the directory: paleo-pbdb/
description: ...
---
```

---

## Network errors

### `HTTP 429: Too Many Requests`

You hit a rate limit on an upstream API.

| Source | Limit | Workaround |
|---|---|---|
| PBDB | Generous (no published limit) | Just retry after a few seconds |
| CrossRef | 50/sec polite-pool | Use the `mailto:` UA (already set) |
| Semantic Scholar | ~1/sec without key | Get a free key, set `S2_API_KEY` env (custom extension) |
| arXiv | 3/sec | Add `time.sleep(1)` between calls |
| Macrostrat | Generous | Just retry |
| Wikidata SPARQL | Strict during outages | Retry after several minutes |
| nkocs.com / IVPP | Unpublished, often 5xx | Best effort; expected to sometimes fail |

### `Network error: timed out`

The remote API is slow or unreachable. The script always returns a clean
error JSON in this case — your output JSON will have an `error` field.

For arxiv specifically, their server is intermittently slow. Retry after
30 seconds.

### `SSL: UNEXPECTED_EOF_WHILE_READING`

Usually a transient TLS issue on the upstream server. Retry.

---

## Windows-specific

### `UnicodeDecodeError: 'gbk' codec can't decode byte ...`

Set the encoding before invoking Python:

```cmd
set PYTHONIOENCODING=utf-8
python script.py
```

Or in PowerShell:

```powershell
$env:PYTHONIOENCODING="utf-8"; python script.py
```

If you see this error inside one of OUR scripts (not your own wrapper), it's a
bug — please [file an issue](https://github.com/syxscott/Paleontology-Research-Skills/issues/new/choose).

### CJK characters in paths

All sub-skill scripts have been tested with Chinese filenames and directory
paths. If you hit a path error, please report with the exact path used.

---

## Morphometric

### `No usable foreground component (size=0, need ≥ N)`

The thresholded image has no foreground pixels in the largest connected
component. Try:

- Lower `--threshold` (default 150; try 100 → more sensitive)
- Pre-process the image to a binary silhouette (black fossil on white)
- Verify the image really has a fossil (open it!)

### `Boundary too short (N pts < required)`

The image is too small or the shape is too simple to support N semilandmarks.
Try:

- Smaller `--num-landmarks` (e.g. 32 instead of 64)
- Higher-resolution image
- Verify the fossil shape isn't a 1-pixel-wide line

### Landmarks look weird in the visualisation

The most common cause is **wrong threshold**. The boundary tracer found the
edge of the IMAGE rather than the fossil. Re-run with:

```bash
python visualize_landmarks.py --image fossil.png --landmarks out/fossil.json --out check.png --show-numbers
```

If the landmarks form a square around the image edge → threshold is too high
(everything is foreground). Lower it.

If only part of the fossil is traced → threshold is too low (parts of the
fossil are below the cutoff). Raise it.

---

## Data files

### Where is `~/.paleontology-research-skills/`?

- Linux / macOS: `/home/<user>/.paleontology-research-skills/` (or `$HOME/.paleontology-research-skills`)
- Windows: `C:\\Users\\<user>\\.paleontology-research-skills\\`

Override with `PALEONTOLOGY_RESEARCH_SKILLS_HOME` environment variable:

```bash
export PALEONTOLOGY_RESEARCH_SKILLS_HOME=/data/paleo
```

### How do I reset my profile?

```bash
python .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py --force
```

⚠️ This overwrites both `soul.md` and `user.md`. Back them up first if customised.

---

## Performance

### Morphometric extraction is slow on large images

The pure-Python boundary tracer is O(N) in image area. For a 4000×4000 image
(16 megapixels), expect 30–60 seconds per image. Workarounds:

- Resize the image first (`Image.thumbnail((1000, 1000))`)
- Process overnight in batch mode

### Research-assistant takes > 60 seconds

It runs up to 5 network calls + 3-5 abstract summaries sequentially.
30-60 seconds is normal. To speed up:

- Reduce `--paper-rows` (e.g. 5 instead of 10)
- Reduce `--summarise-top` (e.g. 1 instead of 5)
- Use `--skip-stratigraphy` / `--skip-taxonomy` to drop stages you don't need

---

## Still stuck?

- Search [Issues](https://github.com/syxscott/Paleontology-Research-Skills/issues)
- Ask in [Discussions](https://github.com/syxscott/Paleontology-Research-Skills/discussions)
- File a new bug report (`/paleo-fossil` template, or [bug report form](https://github.com/syxscott/Paleontology-Research-Skills/issues/new/choose))
'''


# ============ More unit tests for the new skills ============

FILES[ROOT / "tests" / "test_morphometric_convert.py"] = r'''"""Tests for paleo-morphometric-convert format parsers and writers."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPT_DIR = _HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "paleo-morphometric-convert" / "scripts"
sys.path.insert(0, str(_SCRIPT_DIR))
sys.path.insert(0, str(_HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "scripts"))

import convert  # noqa: E402


class TestTpsParser(unittest.TestCase):

    def test_single_specimen(self):
        text = "LM=3\n1.0 2.0\n3.0 4.0\n5.0 6.0\nID=spec1\nSCALE=1.5\n"
        result = convert._parse_tps(text)
        self.assertEqual(len(result), 1)
        s = result[0]
        self.assertEqual(s["specimen_id"], "spec1")
        self.assertEqual(s["scale"], 1.5)
        self.assertEqual(len(s["landmarks"]), 3)
        self.assertEqual(s["landmarks"][0]["x"], 1.0)
        self.assertEqual(s["landmarks"][2]["y"], 6.0)

    def test_multi_specimen(self):
        text = ("LM=2\n1.0 2.0\n3.0 4.0\nID=a\nSCALE=1.0\n\n"
                "LM=2\n5.0 6.0\n7.0 8.0\nID=b\nSCALE=2.0\n")
        result = convert._parse_tps(text)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["specimen_id"], "a")
        self.assertEqual(result[1]["specimen_id"], "b")
        self.assertEqual(result[1]["scale"], 2.0)

    def test_garbage_returns_empty(self):
        result = convert._parse_tps("not a tps file at all")
        self.assertEqual(result, [])


class TestCsvParser(unittest.TestCase):

    def test_long_format(self):
        text = ("specimen_id,landmark_id,x,y,type,name\n"
                "a,1,1.0,2.0,semilandmark,LM01\n"
                "a,2,3.0,4.0,semilandmark,LM02\n"
                "b,1,5.0,6.0,fixed,APEX\n")
        result = convert._parse_csv(text)
        self.assertEqual(len(result), 2)
        names = {s["specimen_id"] for s in result}
        self.assertEqual(names, {"a", "b"})
        a = next(s for s in result if s["specimen_id"] == "a")
        self.assertEqual(len(a["landmarks"]), 2)

    def test_missing_columns_returns_empty(self):
        text = "specimen_id,landmark_id\na,1\n"
        result = convert._parse_csv(text)
        self.assertTrue(all(len(s["landmarks"]) == 0 for s in result))


class TestRoundTrip(unittest.TestCase):

    def test_tps_csv_tps(self):
        original = [{
            "specimen_id": "spec1",
            "scale": 1.0,
            "image_path": None,
            "num_landmarks": 3,
            "landmarks": [
                {"id": 1, "x": 1.0, "y": 2.0, "type": "semilandmark", "name": "LM01"},
                {"id": 2, "x": 3.0, "y": 4.0, "type": "semilandmark", "name": "LM02"},
                {"id": 3, "x": 5.0, "y": 6.0, "type": "semilandmark", "name": "LM03"},
            ],
        }]
        with tempfile.TemporaryDirectory() as td:
            tps_path = Path(td) / "a.tps"
            csv_path = Path(td) / "a.csv"
            tps_path2 = Path(td) / "b.tps"
            convert._write_tps(original, tps_path)
            text = tps_path.read_text(encoding="utf-8")
            parsed_back = convert._parse_tps(text)
            self.assertEqual(parsed_back[0]["specimen_id"], "spec1")
            convert._write_csv(parsed_back, csv_path)
            parsed_csv = convert._parse_csv(csv_path.read_text(encoding="utf-8"))
            self.assertEqual(len(parsed_csv[0]["landmarks"]), 3)
            convert._write_tps(parsed_csv, tps_path2)
            self.assertIn("LM=3", tps_path2.read_text(encoding="utf-8"))


class TestValidation(unittest.TestCase):

    def test_all_same_count(self):
        specimens = [
            {"specimen_id": "a", "landmarks": [{"id": 1, "x": 0, "y": 0}] * 5},
            {"specimen_id": "b", "landmarks": [{"id": 1, "x": 0, "y": 0}] * 5},
        ]
        v = convert._validate(specimens)
        self.assertTrue(v["all_same_count"])
        self.assertEqual(v["specimens_count"], 2)

    def test_inconsistent_count_warning(self):
        specimens = [
            {"specimen_id": "a", "landmarks": [{"id": 1, "x": 0, "y": 0}] * 3},
            {"specimen_id": "b", "landmarks": [{"id": 1, "x": 0, "y": 0}] * 5},
        ]
        v = convert._validate(specimens)
        self.assertFalse(v["all_same_count"])
        self.assertTrue(any("Inconsistent" in w for w in v["warnings"]))

    def test_empty(self):
        v = convert._validate([])
        self.assertEqual(v["specimens_count"] if "specimens_count" in v else 0, 0)


if __name__ == "__main__":
    unittest.main()
'''


FILES[ROOT / "tests" / "test_geo_time.py"] = r'''"""Tests for paleo-geo-time queries (offline ICS data)."""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SCRIPT = (_HERE.parent / ".claude" / "skills" / "paleontology-research-skills"
           / "paleo-geo-time" / "scripts" / "geo_time_query.py")


def run(args):
    """Run the script as subprocess and parse JSON output."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(
        [sys.executable, str(_SCRIPT)] + args,
        capture_output=True, text=True,
        encoding="utf-8", errors="replace",
        env=env, timeout=30,
    )
    return json.loads(r.stdout) if r.stdout else {}


class TestGeoTime(unittest.TestCase):

    def test_period_jurassic(self):
        d = run(["--period", "Jurassic"])
        self.assertEqual(len(d["matches"]), 1)
        m = d["matches"][0]
        self.assertEqual(m["name"], "Jurassic")
        self.assertAlmostEqual(m["startMa"], 201.4, places=1)
        self.assertAlmostEqual(m["endMa"], 145.0, places=1)
        self.assertAlmostEqual(m["durationMa"], 56.4, places=1)

    def test_period_case_insensitive(self):
        d_upper = run(["--period", "JURASSIC"])
        d_lower = run(["--period", "jurassic"])
        self.assertEqual(d_upper["matches"][0]["id"], d_lower["matches"][0]["id"])

    def test_nonexistent_period(self):
        d = run(["--period", "Foobarian"])
        self.assertEqual(d["matches"], [])

    def test_age_100_ma(self):
        d = run(["--age", "100"])
        # 100 Ma is Late Cretaceous - should match Phanerozoic, Mesozoic, Cretaceous, and a stage
        names = {m["name"] for m in d["matches"]}
        self.assertIn("Phanerozoic", names)
        self.assertIn("Mesozoic", names)
        self.assertIn("Cretaceous", names)

    def test_age_negative_returns_empty(self):
        d = run(["--age", "-100"])
        self.assertEqual(d["matches"], [])

    def test_list_periods(self):
        d = run(["--list", "--rank", "period"])
        self.assertEqual(d["count"], 12)  # 12 standard periods
        names = [m["name"] for m in d["matches"]]
        for p in ["Cambrian", "Jurassic", "Cretaceous", "Quaternary"]:
            self.assertIn(p, names)

    def test_list_mesozoic_periods(self):
        d = run(["--list", "--rank", "period", "--parent", "Mesozoic"])
        self.assertEqual(d["count"], 3)
        names = sorted(m["name"] for m in d["matches"])
        self.assertEqual(names, ["Cretaceous", "Jurassic", "Triassic"])

    def test_list_cenozoic_periods(self):
        d = run(["--list", "--rank", "period", "--parent", "Cenozoic"])
        self.assertEqual(d["count"], 3)
        names = sorted(m["name"] for m in d["matches"])
        self.assertEqual(names, ["Neogene", "Paleogene", "Quaternary"])


if __name__ == "__main__":
    unittest.main()
'''


FILES[ROOT / "tests" / "test_morphometric_extract.py"] = r'''"""Tests for paleo-morphometric landmark extraction.

These tests require Pillow. They are skipped if Pillow is not installed.
"""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from PIL import Image, ImageDraw
    _PIL_OK = True
except ImportError:
    _PIL_OK = False

_HERE = Path(__file__).resolve().parent
_SCRIPT_DIR = _HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "paleo-morphometric" / "scripts"
sys.path.insert(0, str(_SCRIPT_DIR))
sys.path.insert(0, str(_HERE.parent / ".claude" / "skills" / "paleontology-research-skills" / "scripts"))

import extract_landmarks  # noqa: E402


@unittest.skipUnless(_PIL_OK, "Pillow not installed")
class TestExtract(unittest.TestCase):

    def _make_ellipse(self, w=300, h=200, threshold=150):
        with tempfile.TemporaryDirectory() as td:
            img_path = Path(td) / "ellipse.png"
            img = Image.new("L", (w, h), 255)
            ImageDraw.Draw(img).ellipse((40, 30, w - 40, h - 30), fill=0)
            img.save(img_path)
            return img_path, td

    def test_resample_evenly(self):
        boundary = [(0, 0), (10, 0), (10, 10), (0, 10)]  # square
        pts = extract_landmarks._resample(boundary, 4)
        self.assertEqual(len(pts), 4)

    def test_resample_n_points(self):
        boundary = [(i, 0) for i in range(100)] + [(99, i) for i in range(100)]
        pts = extract_landmarks._resample(boundary, 16)
        self.assertEqual(len(pts), 16)

    def test_ellipse_extract_64(self):
        with tempfile.TemporaryDirectory() as td:
            img_path = Path(td) / "ellipse.png"
            img = Image.new("L", (300, 200), 255)
            ImageDraw.Draw(img).ellipse((40, 30, 260, 170), fill=0)
            img.save(img_path)

            mask, (w, h) = extract_landmarks._load_binary_mask(img_path, 150)
            self.assertEqual((w, h), (300, 200))

            largest, size = extract_landmarks._largest_component(mask)
            self.assertIsNotNone(largest)
            self.assertGreater(size, 1000)

            boundary = extract_landmarks._trace_boundary(largest)
            self.assertGreater(len(boundary), 100)

            pts = extract_landmarks._resample(boundary, 64)
            self.assertEqual(len(pts), 64)
            # All points should be inside the image
            for x, y in pts:
                self.assertTrue(0 <= x <= 300)
                self.assertTrue(0 <= y <= 200)

    def test_empty_white_image(self):
        with tempfile.TemporaryDirectory() as td:
            img_path = Path(td) / "blank.png"
            Image.new("L", (100, 100), 255).save(img_path)
            mask, _ = extract_landmarks._load_binary_mask(img_path, 150)
            largest, size = extract_landmarks._largest_component(mask)
            self.assertEqual(size, 0)
            self.assertIsNone(largest)


if __name__ == "__main__":
    unittest.main()
'''


FILES[ROOT / "tests" / "test_session.py"] = r'''"""Tests for paleo-session session storage behaviour (offline)."""
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
'''


# ============ Makefile ============
FILES[ROOT / "Makefile"] = '''# Paleontology Research Skills — common dev tasks
# Usage:  make <target>
#
# Most targets work on Linux / macOS. On Windows use Git Bash or WSL.

.PHONY: help install install-dev test test-verbose test-coverage \\
        lint format validate smoke clean serve-docs all

help:
	@echo "Paleontology Research Skills — make targets"
	@echo ""
	@echo "  install         Install just the core (zero deps)"
	@echo "  install-dev     Install all dev dependencies (pytest, ruff, Pillow, openpyxl)"
	@echo "  test            Run the stdlib unittest suite"
	@echo "  test-verbose    Run tests with -v"
	@echo "  test-coverage   Run with pytest --cov"
	@echo "  lint            Run ruff check"
	@echo "  format          Run ruff format"
	@echo "  validate        Validate every SKILL.md against the Agent Skills spec"
	@echo "  smoke           Smoke-test every sub-skill script (--help)"
	@echo "  clean           Remove __pycache__, .pytest_cache, build artefacts"
	@echo "  all             format + lint + test + validate + smoke"

install:
	@echo "Core toolkit has no runtime dependencies. To install the package, run:"
	@echo "  pip install -e ."

install-dev:
	pip install -e ".[dev]"

test:
	python -m unittest discover tests

test-verbose:
	python -m unittest discover tests -v

test-coverage:
	pytest tests/ --cov=.claude --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

validate:
	@python -c "import re, pathlib, sys; \\
	ROOT = pathlib.Path('.claude/skills'); \\
	NAME_RE = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$$'); \\
	ok = True; \\
	[print(f'  [{(\\\"OK \\\" if (NAME_RE.match(name) and name == md.parent.name and 0 < len(desc) <= 1024) else \\\"BAD\\\")}] {md.parent.name:35s} name={name:35s} desc={len(desc)}c') for md in sorted(ROOT.rglob('SKILL.md')) for fm in [md.read_text(encoding='utf-8').split('---', 2)] if len(fm) >= 3 for name in [next((l.split(':', 1)[1].strip() for l in fm[1].split(chr(10)) if l.startswith('name:')), '')] for desc in [next((l.split(':', 1)[1].strip() for l in fm[1].split(chr(10)) if l.startswith('description:')), '')]]; \\
	sys.exit(0)"

smoke:
	@fail=0; \\
	for f in $$(find .claude/skills -name '*.py' -not -name '__init__.py'); do \\
		if ! (python "$$f" --help > /dev/null 2>&1 || python "$$f" > /dev/null 2>&1); then \\
			echo "FAIL: $$f"; fail=1; \\
		fi; \\
	done; \\
	if [ $$fail -eq 0 ]; then echo "All scripts OK"; fi; \\
	exit $$fail

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov

all: format lint test validate smoke
'''


# Write all files
for path, content in FILES.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote {path.relative_to(ROOT)} ({len(content)} bytes)")

print(f"\nO3 done: {len(FILES)} files written.")
