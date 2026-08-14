#!/usr/bin/env python3
"""Optimization Batch O1 — P0 (must-have) files for a public repo."""

import pathlib

ROOT = pathlib.Path(r"D:\GIthub\自制Claude Code skills")

FILES = {}

# ============ 1. requirements.txt ============
FILES[ROOT / "requirements.txt"] = """# Core runtime dependencies — none for the base toolkit
# Everything in paleontology-research-skills uses Python 3.9+ stdlib only
# EXCEPT the optional sub-skills below.
#
# Install optional extras for the morphometric sub-skills:
#   pip install Pillow openpyxl
#
# Or install the package (with extras) via:
#   pip install -e ".[morphometric]"
"""


# ============ 2. requirements-dev.txt ============
FILES[ROOT / "requirements-dev.txt"] = """# Development dependencies
# Install with:  pip install -r requirements-dev.txt

# Test runner (the unit tests use stdlib unittest; pytest is for coverage)
pytest>=7.0
pytest-cov>=4.0

# Optional: lint / format
ruff>=0.4

# Optional extras of the project itself (so dev environment has them all)
Pillow>=10.0
openpyxl>=3.0
"""


# ============ 3. pyproject.toml ============
FILES[ROOT / "pyproject.toml"] = """[build-system]
requires = ["setuptools>=61"]
build-backend = "setuptools.build_meta"

[project]
name = "paleontology-research-skills"
version = "1.0.0"
description = "A modular paleontology research toolkit for Claude Code — 1 parent + 12 focused Agent Skills (PBDB / CrossRef / Semantic Scholar / arXiv / NCBI / Wikidata / Macrostrat / ICS time scale / geometric morphometrics / orchestrator / Chinese news), plus 13 slash commands."
readme = "README.md"
requires-python = ">=3.9"
license = {file = "LICENSE"}
authors = [
    { name = "Syxscott", email = "syxemail@yeah.net" },
]
keywords = [
    "claude-code", "agent-skills", "paleontology", "pbdb",
    "crossref", "morphometrics", "geo-time", "fossil",
    "research", "taxonomy", "stratigraphy",
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
    "Topic :: Scientific/Engineering :: Information Analysis",
]
# Base toolkit has ZERO runtime dependencies
dependencies = []

[project.optional-dependencies]
# Required only for the morphometric sub-skills
morphometric = [
    "Pillow>=10.0",
    "openpyxl>=3.0",
]
dev = [
    "pytest>=7.0",
    "pytest-cov>=4.0",
    "ruff>=0.4",
    "Pillow>=10.0",
    "openpyxl>=3.0",
]

[project.urls]
Homepage = "https://github.com/syxscott/Paleontology-Research-Skills"
Repository = "https://github.com/syxscott/Paleontology-Research-Skills"
"Bug Tracker" = "https://github.com/syxscott/Paleontology-Research-Skills/issues"
"Agent Skills Spec" = "https://agentskills.io/specification"

# This project ships Claude Code skills + slash commands, NOT importable
# Python modules. We still declare layout for IDE friendliness.
[tool.setuptools]
packages = []
include-package-data = true

[tool.ruff]
line-length = 110
target-version = "py39"

[tool.ruff.lint]
# Be opinionated but not heavy-handed
select = ["E", "F", "W", "I", "B", "UP"]
ignore = [
    "E501",   # line too long — we already cap at 110
    "B008",   # function call as default arg — fine for argparse
]

[tool.pytest.ini_options]
testpaths = ["tests"]
"""


# ============ 4. CHANGELOG.md ============
FILES[ROOT / "CHANGELOG.md"] = """# Changelog

All notable changes to **Paleontology Research Skills** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] — 2026-06-03

### Added

- 🦕 **Parent skill** `paleontology-research-skills` as the broad discovery entry.
- 12 focused sub-skills, each independently discoverable:
  - `paleo-pbdb` 🦕 — Paleobiology Database fossil occurrence queries
  - `paleo-crossref` 📄 — CrossRef + Semantic Scholar + arXiv literature search
  - `paleo-memory` 📚 — Local research memory with 384-dim hashing-trick vector search
  - `paleo-session` 📜 — Session history browsing, search, and resume
  - `paleo-profile` 👤 — Double-layer (`soul.md` + `user.md`) research profile
  - `paleo-geo-time` ⏳ — Offline ICS geological time scale (2023-09 chart)
  - `paleo-taxonomy` 🔬 — Full kingdom→species hierarchy (PBDB + NCBI + Wikidata)
  - `paleo-stratigraphy` 🪨 — Formation lookup (PBDB + Macrostrat)
  - `paleo-morphometric` 📐 — 64-landmark extraction from fossil silhouette images
  - `paleo-morphometric-convert` 🔄 — TPS / NTSys / CSV / JSON / Excel conversion
  - `paleo-research-assistant` 🔬 — 5-stage orchestrator → Markdown literature review
  - `paleo-china-news` 🇨🇳 — Chinese paleontology news aggregator
- 13 slash commands (`/paleo`, `/paleo-fossil`, `/paleo-paper`, `/paleo-recall`,
  `/paleo-session`, `/paleo-me`, `/paleo-time`, `/paleo-classify`,
  `/paleo-strat`, `/paleo-landmark`, `/paleo-convert`, `/paleo-review`,
  `/paleo-news`) for explicit, deterministic invocation.
- Shared Python utilities (`paleo_common.py`, `taxonomy.py`).
- Shared data (`stopwords.json`, `geological_periods.json`, `ics_timescale.json`).
- 3 reference documents (`profile-format.md`, `data-locations.md`, `citations.md`).
- 3 report templates (`specimen-report.md`, `literature-review.md`, `session-summary.md`).
- 11 unit tests (covering shared utilities and taxonomy heuristics).
- Architecture and developer guides (`docs/architecture.md`, `docs/development.md`).

### Fixed (during 3 audit passes)

1. SKILL.md sub-skill `name:` ↔ directory-name mismatch (was silently making
   skills un-discoverable in some Claude Code versions).
2. `profile_init.py` status field was inverted (new write reported
   `"overwritten"`, force overwrite reported `"written"`).
3. `memory_archive.py` early-return missed `movedCount`, `cutoffDays`,
   `archiveDir` (output schema was inconsistent).
4. `geo_time_query.py --list --parent X` always returned 0 results because it
   only checked the `parent` field instead of traversing the real ICS hierarchy
   fields (`era`, `period`, `epoch`, etc.).
5. SKILL.md command examples used `../scripts/foo.py` but actual scripts live
   at `scripts/foo.py` (18 occurrences fixed).
6. `subprocess.run` calls in `batch_extract.py` and `research_assistant.py` did
   not pin UTF-8 encoding → crashed on Windows with CJK paths. Fixed with
   `encoding="utf-8", errors="replace"`.
7. `stratigraphy_query.py` returned an empty `{"summary": {}}` when no records
   were found (output schema inconsistent). Fixed to always return the full
   field set with zero / null values.
8. `taxonomy_query.py` returned raw `HTTP 400` from PBDB when a taxon was not
   found. Now maps to `"No taxon found matching 'X' (PBDB has no record)"`.

### Technical highlights

- Strict scientific integrity: no fabrication of taxa, DOIs, or occurrences.
- All scripts handle missing data home / empty results / network errors gracefully.
- All scripts output structured JSON (no stack traces leak to users).
- Base toolkit has **zero runtime dependencies** — pure Python 3.9+ stdlib.
- Morphometric sub-skills are the only optional dependency
  (`pip install Pillow openpyxl`).

[Unreleased]: https://github.com/syxscott/Paleontology-Research-Skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/syxscott/Paleontology-Research-Skills/releases/tag/v1.0.0
"""


# ============ 5. CONTRIBUTING.md ============
FILES[ROOT / "CONTRIBUTING.md"] = """# Contributing to Paleontology Research Skills

Thanks for your interest in contributing! 🦕

This toolkit is a community resource for the paleontology / geosciences community.
Whether you want to add a new data source, fix a bug, improve documentation, or
write a tutorial — pull requests are welcome.

---

## Table of contents

1. [Getting set up](#getting-set-up)
2. [Project layout](#project-layout)
3. [Adding a new sub-skill](#adding-a-new-sub-skill)
4. [Adding a slash command](#adding-a-slash-command)
5. [Running tests](#running-tests)
6. [Code style](#code-style)
7. [Commit message convention](#commit-message-convention)
8. [Pull-request workflow](#pull-request-workflow)
9. [Scientific integrity rules](#scientific-integrity-rules)

---

## Getting set up

```bash
git clone https://github.com/syxscott/Paleontology-Research-Skills.git
cd Paleontology-Research-Skills

# Install dev dependencies (includes Pillow + openpyxl for morphometric)
python -m pip install -r requirements-dev.txt
# or
pip install -e ".[dev]"

# Verify the install:
python -m unittest discover tests        # should report 11 OK
python .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --period Jurassic
```

---

## Project layout

```
.claude/
├── skills/paleontology-research-skills/    # parent + 12 sub-skills
│   ├── SKILL.md                            # parent skill (broad description)
│   ├── scripts/                            # shared Python utilities
│   ├── data/                               # shared static data
│   ├── references/                         # shared reference docs
│   ├── templates/                          # markdown report templates
│   └── paleo-<name>/                       # one directory per sub-skill
│       ├── SKILL.md                        # narrow description + usage
│       └── scripts/*.py                    # implementation
└── commands/                               # slash commands (.md per command)

docs/                                       # architecture + dev guides
tests/                                      # unittest suite
```

The project follows the [Agent Skills specification](https://agentskills.io/specification)
— see `docs/architecture.md` for the design rationale.

---

## Adding a new sub-skill

1. **Pick a name** that's unique, lowercase, hyphenated, ≤ 64 chars, and follows
   the `paleo-<topic>` pattern (e.g. `paleo-isotope`).

2. **Create the directory** under `paleontology-research-skills/`:
   ```
   paleontology-research-skills/
   └── paleo-isotope/
       ├── SKILL.md
       └── scripts/
           └── isotope_query.py
   ```

3. **Write `SKILL.md`** with YAML frontmatter:
   ```markdown
   ---
   name: paleo-isotope
   description: 🧪 <emoji + one paragraph describing exactly when to use this
     skill, including phrases the user might say. Max 1024 characters.>
   ---

   # Isotope Analysis Skill

   ## When to Use
   - "Calculate δ13C from these values"
   - ...

   ## When NOT to Use
   - ...

   ## Usage
   ```bash
   python3 scripts/isotope_query.py --values 1.2,2.3,...
   ```

   ## Output Format
   ...
   ```

   Required: `name:` MUST match the directory name. Description ≤ 1024 chars.

4. **Implement the script** following the established conventions:
   - Shebang + module docstring at top
   - `from __future__ import annotations` for forward references
   - Bootstrap sys.path to find shared `paleo_common`
   - Argparse for CLI
   - Always output a single JSON object via `print_json()`
   - Catch network / file errors and embed them in the JSON

5. **Register in the parent SKILL.md** — add a row to the routing table.

6. **Add a slash command** in `.claude/commands/paleo-isotope.md` (see below).

7. **Update README.md** — add to the "Two ways to invoke" table and tree.

8. **Update CHANGELOG.md** under `## [Unreleased]`.

9. **Write tests** in `tests/test_paleo_<name>.py` (smoke + edge cases).

10. **Run** `python -m unittest discover tests` and the validation script
    (`docs/development.md` shows how).

---

## Adding a slash command

Create `.claude/commands/paleo-<name>.md`:

```markdown
---
description: <one-line user-facing description>
argument-hint: <expected argument shape>
allowed-tools: Bash, Read
---

The user wants <X>. Use the **paleo-<sub-skill>** skill on this argument:

> $ARGUMENTS

Procedure:
1. <step>
2. ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-<sub-skill>/scripts/<script>.py \\
       --arg "<VALUE>"
   ```
3. <how to present the result>
```

The filename (minus `.md`) becomes the slash command name.

---

## Running tests

```bash
# Stdlib unittest:
python -m unittest discover tests

# Or pytest (with coverage):
pytest tests/ --cov=.claude/skills
```

Smoke-test every script:

```bash
for f in $(find .claude -name '*.py' -not -name '__init__.py'); do
  python "$f" --help > /dev/null && echo "OK $f"
done
```

---

## Code style

- **Python 3.9+** stdlib only for the base toolkit. The morphometric sub-skills
  may use **Pillow** and (optionally) **openpyxl** — no other deps without
  prior discussion.
- Use `from __future__ import annotations`.
- Lines wrap at ≤ 110 chars.
- All `print()` to stdout must be a single JSON document — use `print_json()`
  from `paleo_common`.
- Catch network and file I/O errors. Never let a bare `Exception` propagate to
  the user.
- Use `argparse` for all CLI args; no positional args except where it really
  makes sense.
- Add docstrings to public functions.
- Add type hints for new public functions.

Linting (optional but recommended):

```bash
ruff check .
ruff format .
```

---

## Commit message convention

We follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
feat(scope): short description in imperative mood

Longer body explaining what and why (not how).

Refs: #123
```

Common scopes: `pbdb`, `crossref`, `morphometric`, `taxonomy`,
`stratigraphy`, `profile`, `memory`, `session`, `news`,
`research-assistant`, `docs`, `ci`, `release`.

Examples:

- `feat(pbdb): add --interval filter to occurrence query`
- `fix(morphometric): handle images with no foreground gracefully`
- `docs(readme): add Windows installation instructions`

---

## Pull-request workflow

1. **Fork** the repo and create a topic branch:
   ```bash
   git checkout -b feat/add-isotope-skill
   ```

2. **Make changes**, write tests, run the test suite.

3. **Commit** with a Conventional-Commit message.

4. **Push** and open a PR against `main`. The PR template will ask:
   - What does this change?
   - Why?
   - Tests added / updated?
   - Breaking changes?

5. **CI** runs on every push: unit tests across Python 3.9–3.12 on
   Ubuntu, macOS, Windows. All checks must pass.

6. **Review** — at least one approving review is required.

7. **Squash-merge** is the default.

---

## Scientific integrity rules

These rules are absolute. PRs that violate them will be rejected:

- ❌ **No fabricated data.** Never invent species names, DOIs, ages, or fossil
  occurrences. Every claim must trace to a primary source (PBDB, CrossRef,
  ICS, etc.) returned by the tool.
- ❌ **No silent failures.** If a network call fails, the JSON output must
  include an `error` field — never an empty success.
- ❌ **No scope creep into non-paleontology domains.** This toolkit is
  paleontology-specific.
- ✅ **Always cite the data source** in the JSON output (`"source"` field).
- ✅ **Always report uncertainty** for ages (in Ma) and taxonomic decisions.

---

## Reporting bugs

Open an [issue](https://github.com/syxscott/Paleontology-Research-Skills/issues/new/choose)
and include:

- Which skill / script
- Command you ran
- Expected vs actual behavior
- Python version + OS
- Full JSON output (or error message)

For security vulnerabilities, see [`SECURITY.md`](./SECURITY.md).

---

## License

By contributing, you agree your contributions will be licensed under the
[MIT License](./LICENSE).
"""


# ============ 6. .gitattributes (fix CRLF/LF mess) ============
FILES[ROOT / ".gitattributes"] = """# Always use LF line endings inside the repository.
# Windows checkouts will see CRLF locally if core.autocrlf=true,
# but git always stores LF.

* text=auto eol=lf

# Explicit text files
*.py    text eol=lf
*.md    text eol=lf
*.json  text eol=lf
*.toml  text eol=lf
*.yml   text eol=lf
*.yaml  text eol=lf
*.txt   text eol=lf
LICENSE text eol=lf
Makefile text eol=lf

# Binaries (never line-ending convert)
*.png  binary
*.jpg  binary
*.jpeg binary
*.gif  binary
*.tif  binary
*.tiff binary
*.bmp  binary
*.webp binary
*.xlsx binary
*.xls  binary
*.zip  binary
*.gz   binary
*.tar  binary
"""


# ============ 7. README badges (modify existing README) ============
# We'll do this via Edit tool below (need to read current README first)

# Write all files
for path, content in FILES.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote {path.relative_to(ROOT)} ({len(content)} bytes)")

print(f"\nO1 (files): {len(FILES)} written.")
