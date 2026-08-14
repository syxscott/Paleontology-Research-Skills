# Paleontology Research Skills — Architecture

This document explains *why* the project is laid out the way it is.

## 1. Nested skill structure

```
.claude/skills/
└── paleontology-research-skills/            ← parent SKILL.md, broad description
    ├── pbdb/             ← child SKILL.md, narrow description
    ├── crossref/         ← child SKILL.md
    ├── memory/           ← child SKILL.md
    ├── session/          ← child SKILL.md
    ├── profile/          ← child SKILL.md
    └── geo-time/         ← child SKILL.md
```

The [Agent Skills specification](https://agentskills.io/specification) supports
*recursive `SKILL.md` discovery*, so every subdirectory's `SKILL.md` registers
as an independent skill that the model can trigger directly. We exploit this to
get the best of both worlds:

| Aspect | Parent (`paleontology-research-skills`) | Children |
|--------|----------------------|----------|
| `description` | broad, multi-topic | one narrow capability each |
| Triggers on | vague prompts | precise prompts |
| Body | "use sub-skill X for Y" map | exact procedure & arguments |
| Owns | shared scripts/data/refs | one or more focused scripts |

## 2. Shared resource access

All sub-skill scripts use the **same idiom** to import shared utilities:

```python
import os, sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)
from paleo_common import load_profile, normalize_taxon, print_json
```

This:
- Works regardless of the user's `cwd`.
- Requires no `pip install -e .`.
- Keeps each sub-skill's `scripts/` directory tiny — only the script(s) that
  are *specific* to that capability.

## 3. Data root

All persistent user data lives under **one** root: `~/.paleontology-research-skills/` (override
with `PALEONTOLOGY_RESEARCH_SKILLS_HOME`). This makes backups / migration trivial.

See [`.claude/skills/paleontology-research-skills/references/data-locations.md`](../.claude/skills/paleontology-research-skills/references/data-locations.md)
for the exact directory layout.

## 4. Output convention

Every script that returns data prints **one JSON object** to stdout, with at
minimum:

| Field | Meaning |
|-------|---------|
| `source` or `data_home` | where the data came from |
| `query` or `scope` | the exact parameters used |
| `count` | number of records in the result |
| (records) | typed array with the actual results |

This keeps tool output cheap to embed back into the model's context.

## 5. Failure model

Scripts **never throw** for "data not found" — they return `{"count": 0, ...}`
with a `note` explaining what's missing. They only return errors via
`{"error": "..."}` for genuine errors (network failure, malformed argument,
missing required input).

## 6. No external dependencies

Every script runs on Python 3.9+ standard library. This is deliberate:

- Skills can be installed without a virtual environment.
- No surprise upgrades.
- Memory similarity uses a built-in 384-dim hashing-trick — no embedding API.
