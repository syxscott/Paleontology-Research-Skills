# Paleontology Research Skills Data Locations

All user data is stored under a single root, defaulting to:

| Platform | Default root |
|----------|--------------|
| POSIX (macOS / Linux) | `~/.paleontology-research-skills/` |
| Windows | `%USERPROFILE%\.paleontology-research-skills\` |

Override with the environment variable **`PALEONTOLOGY_RESEARCH_SKILLS_HOME`** (absolute path).

The root is resolved at runtime by `paleo_common.data_home()`.

---

## Directory layout

```
$PALEONTOLOGY_RESEARCH_SKILLS_HOME/
├── soul.md                       # System identity & scientific principles
├── user.md                       # Personal research preferences
├── memory/
│   ├── short/                    # Short-term task memory (one JSON per task)
│   │   └── <task_id>.json
│   ├── long_term.jsonl           # Promoted long-term memory (one JSON per line)
│   └── archive/
│       └── short/                # Archived short-term tasks (memory_archive.py)
│           └── <task_id>.json
└── sessions/                     # Session transcripts (one JSON per session)
    └── <session_id>.json
```

---

## File specifications

### `short/<task_id>.json` (short-term memory)

```json
{
  "task_id": "2025-05-21-pbdb-allosaurus",
  "timestamp": "2025-05-21T09:14:00Z",
  "command": "paleo-pbdb --base-name Allosaurus fragilis",
  "status": "success",
  "summary": "Returned 47 occurrences from Morrison Fm.",
  "tags": ["Allosaurus", "Morrison", "Jurassic"]
}
```

### `long_term.jsonl` (long-term memory; one JSON per line)

```jsonl
{"task_id":"2025-05-21-...","timestamp":"...","command":"...","summary":"...","conclusion":"..."}
{"task_id":"2025-05-22-...","timestamp":"...","command":"...","summary":"...","conclusion":"..."}
```

Long-term memory is intended for stable conclusions; short-term is the raw log.
Promotion from short → long is a manual / out-of-band step (handled by the
parent application, not by these skills).

### `sessions/<session_id>.json` (session transcript)

See [session/SKILL.md](../session/SKILL.md) for the full schema.

---

## Discovery rules

Every memory / session script begins by calling `paleo_common.data_home()` and
**fails gracefully** if the directory does not exist:

- `memory_search.py` returns `{"count": 0, "results": []}`
- `memory_list.py` returns `{"count": 0, "entries": []}`
- `session_list.py` returns `{"count": 0, "sessions": []}`

This means a fresh install (no data yet) never errors — the user simply gets an
empty result and can start populating data.

---

## Migration notes

If you change `PALEONTOLOGY_RESEARCH_SKILLS_HOME`, you must manually move the existing contents.
The skills do not auto-migrate.

To re-initialise the profile in a new location:

```bash
PALEONTOLOGY_RESEARCH_SKILLS_HOME=/path/to/new python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py
```
