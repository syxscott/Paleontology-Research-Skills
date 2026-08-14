# Changelog

All notable changes to **Paleontology Research Skills** are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- `convert.py`: malformed JSON input no longer crashes with a traceback —
  returns a structured error instead (was a silent empty result).
- `convert.py`: legacy `.xls` files are explicitly rejected with a clear
  message ("convert to .xlsx first") instead of crashing inside openpyxl.
- `memory_archive.py`: entries with timezone-naive timestamps no longer crash
  with `TypeError: can't compare offset-naive and offset-aware datetimes`.
- `session_list.py`: sessions mixing naive and aware `started_at` values no
  longer crash when sorted.
- Slash commands (`commands/paleo*.md`): now resolve the toolkit root at
  runtime, supporting both user-level (`~/.claude/skills/`) and project-level
  (`.claude/skills/`) installs. Previously they only worked with a
  project-level install.
- `taxonomy.py`: common scientific nouns ("Fossil", "Dinosaur", "Mammal",
  …) are no longer mis-detected as taxon names; the stopword / geological
  period lists are now loaded from the bundled JSON data files (authoritative)
  with built-in fallbacks.
- `geo_time_query.py`: `--rank` help no longer advertises `stage`/`age`
  (the bundled ICS data only contains eonothem/era/period/epoch).
- `ics_timescale.json`: fixed the misspelled `eonotheMs` top-level key
  (`eonothems`).
- `wikidata_taxonomy.py`: SPARQL string literals now escape backslashes and
  newlines (previously only double quotes).
- `crossref_search.py`: date-parts with `null` entries no longer render as
  `"2020-None-None"`.
- CI: `lint.yml` now actually fails on ruff violations (removed `|| true`);
  `validate-skills.yml` command-frontmatter check no longer silently passes
  files without frontmatter.
- Code style: whole-tree `ruff check` and `ruff format` now pass cleanly
  (E701/E702 compact-style rules explicitly allowed in `pyproject.toml`).

### Added

- Regression tests: `tests/test_memory_archive.py` (timestamp handling),
  `tests/test_convert_robustness.py` (malformed input handling),
  `tests/test_session_list.py` (mixed naive/aware timestamps),
  common-noun rejection tests in `tests/test_taxonomy.py` (38 → 51 tests).

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
