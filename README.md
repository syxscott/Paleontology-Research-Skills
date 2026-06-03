# Paleontology Research Skills 🦕

> A modular paleontology research toolkit packaged as a **nested Claude Code
> Agent Skill**. One parent skill (`paleontology-research-skills`) acts as the
> broad discovery entry; **twelve focused sub-skills** each handle one
> concrete capability — and there are **thirteen slash commands** for explicit
> manual invocation.

[![Agent Skills](https://img.shields.io/badge/spec-Agent_Skills-blue)](https://agentskills.io/specification)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-purple?logo=anthropic&logoColor=white)](https://github.com/anthropics/claude-code)
[![Skills: 13](https://img.shields.io/badge/skills-13-orange)](#-sub-skill-cheat-sheet)
[![Slash commands: 13](https://img.shields.io/badge/slash_commands-13-orange)](#way-2-slash-commands-explicit-manual-control)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)](./CHANGELOG.md)

---

## 📑 Table of contents

- [Why a nested layout?](#-why-a-nested-layout)
- [Directory layout](#-directory-layout)
- [Two ways to invoke the toolkit](#-two-ways-to-invoke-the-toolkit)
  - [Way 1: natural-language prompts](#way-1-natural-language-prompts-skills-auto-trigger)
  - [Way 2: slash commands](#way-2-slash-commands-explicit-manual-control)
- [Installation](#-installation)
- [Smoke test](#-smoke-test)
- [Design principles](#-design-principles)
- [Contributing](#-contributing)
- [Changelog](./CHANGELOG.md)
- [License](#-license)

---

## ✨ Why a nested layout?

The official Agent Skills specification supports recursive `SKILL.md`
discovery — i.e. any subdirectory containing a `SKILL.md` is registered as its
own independent skill. This lets us:

1. Expose **one wide entry point** (`paleontology-research-skills`) so the model can discover the
   whole toolkit even from vague prompts ("help me with my fossil research").
2. Expose **six narrow sub-skills** so the model picks the exact right tool
   for precise prompts ("find Allosaurus fossils in PBDB").
3. Share Python utilities and data files across all sub-skills through the
   parent directory (`paleontology-research-skills/scripts/`, `paleontology-research-skills/data/`).

---

## 🗂 Directory layout

```
.claude/
├── skills/
│   └── paleontology-research-skills/                  # ★ Parent skill (broad discovery)
│       ├── SKILL.md
│       ├── scripts/                                # Shared Python utilities
│       │   ├── paleo_common.py                     #   profile, memory, vector search
│       │   └── taxonomy.py                         #   taxon-name heuristics
│       ├── data/                                   # Shared static data
│       │   ├── stopwords.json
│       │   └── geological_periods.json
│       ├── references/                             # Shared reference docs
│       │   ├── profile-format.md
│       │   ├── data-locations.md
│       │   └── citations.md
│       ├── templates/                              # Markdown output templates
│       │   ├── specimen-report.md
│       │   ├── literature-review.md
│       │   └── session-summary.md
│       │
│       ├── paleo-pbdb/                  🦕  PBDB fossil query
│       ├── paleo-crossref/              📄  CrossRef + Semantic Scholar + arXiv
│       ├── paleo-memory/                📚  Local research memory
│       ├── paleo-session/               📜  Session history
│       ├── paleo-profile/               👤  Research preferences
│       ├── paleo-geo-time/              ⏳  ICS time scale
│       ├── paleo-taxonomy/              🔬  Kingdom→species hierarchy + NCBI + Wikidata
│       ├── paleo-stratigraphy/          🪨  Formation lookup + Macrostrat
│       ├── paleo-morphometric/          📐  Landmark extraction (Pillow)
│       ├── paleo-morphometric-convert/  🔄  TPS/NTSys/CSV/JSON/Excel converter
│       ├── paleo-research-assistant/    🔬  5-stage literature-review orchestrator
│       └── paleo-china-news/            🇨🇳  Chinese fossil-news aggregator
│
└── commands/                                       # Slash commands (manual entry-points)
    ├── paleo.md                         # /paleo            – toolkit overview
    ├── paleo-fossil.md                  # /paleo-fossil     – PBDB query
    ├── paleo-paper.md                   # /paleo-paper      – literature search
    ├── paleo-recall.md                  # /paleo-recall     – memory search
    ├── paleo-session.md                 # /paleo-session    – session router
    ├── paleo-me.md                      # /paleo-me         – profile
    ├── paleo-time.md                    # /paleo-time       – geological time scale
    ├── paleo-classify.md                # /paleo-classify   – taxonomic hierarchy
    ├── paleo-strat.md                   # /paleo-strat      – stratigraphy lookup
    ├── paleo-landmark.md                # /paleo-landmark   – morphometric extraction
    ├── paleo-convert.md                 # /paleo-convert    – landmark format conversion
    ├── paleo-review.md                  # /paleo-review     – auto literature review
    └── paleo-news.md                    # /paleo-news       – Chinese fossil news
```

---

## 🎯 Two ways to invoke the toolkit

### Way 1: natural-language prompts (skills auto-trigger)

Claude reads each sub-skill's `description` and auto-loads the right one when
your prompt matches. **No special syntax — just ask.**

| If you say… | Claude auto-loads |
|---|---|
| *"find Allosaurus fossils in Morrison Formation"* | `paleo-pbdb` |
| *"find papers about K-Pg boundary"* | `paleo-crossref` |
| *"what's the classification of Tyrannosaurus rex?"* | `paleo-taxonomy` |
| *"what's in the Yixian Formation?"* | `paleo-stratigraphy` |
| *"extract landmarks from this ammonoid image"* | `paleo-morphometric` |
| *"convert this TPS file to Excel"* | `paleo-morphometric-convert` |
| *"write a literature review on theropod feathers"* | `paleo-research-assistant` |
| *"中国最近的化石发现"* | `paleo-china-news` |
| *"did I research Yixian Formation before?"* | `paleo-memory` |
| *"show my last 3 sessions"* | `paleo-session` |
| *"what do you know about my research?"* | `paleo-profile` |
| *"when did the Jurassic start?"* | `paleo-geo-time` |

### Way 2: slash commands (explicit manual control)

For deterministic invocation, type a slash command:

| Slash command | What it does | Backed by |
|---|---|---|
| `/paleo` | Toolkit overview & status | (router) |
| `/paleo-fossil <taxon>` | Query PBDB for fossil occurrences | `paleo-pbdb` |
| `/paleo-paper <topic>` | Search CrossRef / Semantic Scholar / arXiv | `paleo-crossref` |
| `/paleo-recall <query>` | Search local research memory | `paleo-memory` |
| `/paleo-session [list\|show\|search\|resume]` | Session management | `paleo-session` |
| `/paleo-me` | Show research profile | `paleo-profile` |
| `/paleo-time <period\|Ma>` | Geological time scale | `paleo-geo-time` |
| `/paleo-classify <taxon>` | Full kingdom→species hierarchy | `paleo-taxonomy` |
| `/paleo-strat <formation>` | Formation age / taxa / location | `paleo-stratigraphy` |
| `/paleo-landmark <image>` | Extract 64 GM landmarks from fossil image | `paleo-morphometric` |
| `/paleo-convert <file> <fmt>` | TPS / NTSys / CSV / JSON / Excel conversion | `paleo-morphometric-convert` |
| `/paleo-review <topic>` | Generate full literature-review Markdown report | `paleo-research-assistant` |
| `/paleo-news [keyword]` | Aggregate Chinese paleontology news | `paleo-china-news` |

Examples:
```
/paleo-fossil Allosaurus
/paleo-paper theropod feather evolution
/paleo-classify Tyrannosaurus rex
/paleo-strat Yixian
/paleo-landmark ammonoid.png
/paleo-convert specimens.tps xlsx
/paleo-review Yixian Formation paleobiology
/paleo-news 恐龙
/paleo-recall Yixian Formation
/paleo-time Jurassic
/paleo-time 100
```

> ℹ️ Skills and slash commands **share the same underlying scripts** — slash
> commands are just explicit shortcuts. Either path arrives at the same code.

---

## 🚀 Installation

### As a user-scope toolkit (recommended — works in every project)

```bash
# POSIX
mkdir -p ~/.claude/skills ~/.claude/commands
cp -r .claude/skills/paleontology-research-skills  ~/.claude/skills/
cp    .claude/commands/paleo*.md     ~/.claude/commands/

# Windows (PowerShell)
$dest = "$env:USERPROFILE\.claude"
New-Item -ItemType Directory -Force "$dest\skills","$dest\commands" | Out-Null
Copy-Item -Recurse .claude\skills\paleontology-research-skills "$dest\skills\"
Copy-Item .claude\commands\paleo*.md "$dest\commands\"
```

### As a project-scope toolkit

Drop the entire `.claude/` folder into your project — Claude Code auto-discovers
both `skills/` and `commands/` on the next session.

### Initialise your profile (recommended)

```bash
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py
```

This writes default `~/.paleontology-research-skills/soul.md` and `~/.paleontology-research-skills/user.md`;
edit `user.md` to set your role, institution, preferred periods, language.

---

## 🧪 Smoke test

```bash
# All scripts respond to --help without imports failing
python3 .claude/skills/paleontology-research-skills/paleo-pbdb/scripts/pbdb_query.py --help
python3 .claude/skills/paleontology-research-skills/paleo-crossref/scripts/crossref_search.py --help
python3 .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_status.py
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_show.py
python3 .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --period Jurassic

# Unit tests
python3 -m unittest discover tests
```

---

## 📐 Design principles

- **One skill, one capability.** Each sub-skill has a tight `description`
  so the model triggers it precisely.
- **No external dependencies.** Everything runs on Python 3.9+ stdlib (no
  `requests`, no `numpy`, no embeddings API).
- **Fail gracefully.** Missing data dirs return empty results, not stack traces.
- **Reproducible.** Every script prints its parameters in the output JSON.
- **No fabrication.** Scripts only return what their data source reports;
  they never invent records, citations, or DOIs.

---

## 🤝 Contributing

Pull requests are welcome! See [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the
full guide, including how to add a new sub-skill, code style, and the PR
workflow.

For bug reports and feature requests, please use the
[GitHub Issues](https://github.com/syxscott/Paleontology-Research-Skills/issues/new/choose).

For security vulnerabilities, see [`SECURITY.md`](./SECURITY.md).

Code of Conduct: [Contributor Covenant 2.1](./CODE_OF_CONDUCT.md).

---

## 📜 License

MIT — see [LICENSE](./LICENSE).

Bundled data attributions:

- **PBDB** data: CC-BY 4.0 (https://paleobiodb.org)
- **CrossRef** metadata: CC-BY 4.0 (https://www.crossref.org)
- **Semantic Scholar** metadata: ODC-BY 1.0 (https://www.semanticscholar.org)
- **arXiv** metadata: CC0 (https://arxiv.org)
- **NCBI Taxonomy**: Public domain (https://www.ncbi.nlm.nih.gov/taxonomy)
- **Wikidata**: CC0 (https://www.wikidata.org)
- **Macrostrat**: CC-BY 4.0 (https://macrostrat.org)
- **ICS** chart: International Commission on Stratigraphy (https://stratigraphy.org)

The morphometric landmark extractor is inspired by the **DeepMorph** algorithm
by Xiaokang Liu (China University of Geosciences, Wuhan).

