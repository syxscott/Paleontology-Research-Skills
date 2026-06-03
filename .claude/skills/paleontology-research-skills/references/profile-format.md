# Paleontology Research Skills Profile Format

The user profile is stored as **two markdown files** at the Paleontology Research Skills data root
(`~/.paleontology-research-skills/` by default; override with `PALEONTOLOGY_RESEARCH_SKILLS_HOME`):

| File | Purpose |
|------|---------|
| `soul.md` | System identity, scientific principles, safety boundaries |
| `user.md` | Personal research preferences (role, periods, language, etc.) |

Both files are parsed by `paleo_common.load_profile()` using a forgiving
Markdown parser. Headings, list items, and `Key: value` lines are all extracted.

---

## `soul.md` (System Identity)

```markdown
## Identity
Paleontology Research Skills is an AI research assistant specialised in paleontology and geosciences.

## Mission
Help users conduct reliable, reproducible paleontological research.

## Core Principles
- Scientific Integrity: never fabricate data, taxa, or papers.
- Verifiability: all claims must be traceable to primary sources.
- Transparency: clearly state data sources and uncertainties.
- Reproducibility: document all queries and parameters.
- Humility: acknowledge limits of current knowledge.

## Execution Rules
- Always verify taxonomic names via PBDB before use.
- Always include DOI for paper citations.
- Always report age ranges with uncertainty (in Ma).

## Safety Boundaries
- Do not fabricate species names or fossil occurrences.
- Do not invent paper citations or DOIs.
- Do not claim certainty where none exists.
- Do not access paywalled content through unauthorised means.

## Domain Scope
### In scope:
- Paleontology (all periods, all taxa)
- Stratigraphy and geological time
- Taxonomy and systematics

### Out of scope:
- Modern organism identification
- Commercial fossil appraisal
- Creation science or pseudoscience
```

### Required sections

| Section | Required? | Used as |
|---------|-----------|---------|
| `## Identity` | yes | `soul.identity` (string) |
| `## Mission` | yes | `soul.mission` (single line) |
| `## Core Principles` | yes | `soul.corePrinciples` (list) |
| `## Execution Rules` | yes | `soul.executionRules` (list) |
| `## Safety Boundaries` | yes | `soul.safetyBoundaries` (list) |
| `## Domain Scope` + `### In scope:` / `### Out of scope:` | recommended | `soul.domainScope` |

---

## `user.md` (Personal Preferences)

```markdown
## Identity
Role: paleontology researcher
Domain: vertebrate paleontology
Institution: China University of Geosciences (Wuhan)

## Research Focus
### Primary interests:
- Theropod dinosaurs
- Jurassic stratigraphy
- Chinese formations (Yixian, Jiufotang)

### Preferred geological periods:
- Jurassic
- Cretaceous

### Preferred regions:
- China (Liaoning, Xinjiang)
- Mongolia

## Language Preference
Preferred language: Chinese or English
Output language: Chinese (simplified)

## Data Preferences
Default occurrence limit: 50
Include preprints: false
Prefer open access: true
Citation format: APA
```

### Recognised keys

| Section | Key | Type | Default |
|---------|-----|------|---------|
| `## Identity` | `Role` | string | `"paleontology researcher"` |
| `## Identity` | `Domain` | string | `"vertebrate paleontology"` |
| `## Identity` | `Institution` | string | `""` |
| `## Language Preference` | `Preferred language` | string | `"Chinese or English"` |
| `## Language Preference` | `Output language` | string | `"Chinese"` |
| `## Data Preferences` | `Default occurrence limit` | int | `50` |
| `## Data Preferences` | `Include preprints` | bool (`true`/`false`) | `false` |
| `## Data Preferences` | `Prefer open access` | bool | `true` |
| `## Data Preferences` | `Citation format` | string | `"APA"` |

`### Primary interests:`, `### Preferred geological periods:`, `### Preferred
regions:` are all list-typed (markdown bullet points).

---

## Initialising the files

```bash
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py          # create only if missing
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py --force  # overwrite
```

## Inspecting the parsed profile

```bash
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_show.py            # pretty
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_show.py --json     # machine-readable
```
