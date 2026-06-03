# Frequently asked questions

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
