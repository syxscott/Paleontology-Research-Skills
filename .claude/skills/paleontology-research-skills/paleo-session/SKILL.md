---
name: paleo-session
description: 📜 Browse, search, and resume the user's session history stored under `~/.paleontology-research-skills/sessions/`. Use when the user asks to "list my recent sessions", "show session X", "search sessions for Y", or "resume my last session on Z". Each session is a JSON file containing turns, commands, and a final summary.
---

# Paleontology Research Skills Session History

Lists, inspects, and searches the user's research sessions. A session is one bounded research workflow (one or more turns ending in a summary) and is stored as `~/.paleontology-research-skills/sessions/<session_id>.json`.

## When to Use

- "Show me my recent sessions"
- "What did I do in session 2025-05-21-allosaurus?"
- "Search my sessions for Yixian"
- "Resume my last session on K-Pg boundary"
- "List sessions from last week"

## When NOT to Use

- Looking up TASK-level memory (smaller, more granular) → use `paleo-memory`
- Profile / preferences → use `paleo-profile`
- Live PBDB / CrossRef queries → use `paleo-pbdb` / `paleo-crossref`

## Usage

```bash
# List the 20 most recent sessions
python3 scripts/session_list.py --limit 20

# Show one session (turns + summary)
python3 scripts/session_show.py --id 2025-05-21-allosaurus

# Search all sessions for a term
python3 scripts/session_search.py --query "Yixian Formation" --top-k 5

# Build a context-resume payload for a session
python3 scripts/session_resume.py --id 2025-05-21-allosaurus
```

## Session File Format

```json
{
  "session_id": "2025-05-21-allosaurus",
  "title": "Allosaurus morphological comparison",
  "started_at": "2025-05-21T09:14:00Z",
  "ended_at": "2025-05-21T11:42:00Z",
  "topic_tags": ["Allosaurus", "Morrison", "theropod"],
  "turns": [
    {"role": "user", "content": "Find Allosaurus fragilis fossils in Morrison Formation"},
    {"role": "assistant", "content": "..."}
  ],
  "commands": [
    {"tool": "paleo-pbdb", "args": {"base_name": "Allosaurus fragilis"}, "count": 47}
  ],
  "summary": "Identified 47 occurrences; dominant in Morrison Fm; Late Jurassic.",
  "open_questions": ["Are there Asian relatives?", "Age range refinement"]
}
```

## Output

`session_list.py`:
```json
{"count": 12, "sessions": [{"session_id": "...", "title": "...", "ended_at": "...", "topic_tags": [...]}]}
```

`session_show.py`: the full session JSON (truncated turns by default).

`session_search.py`:
```json
{"query": "...", "results": [{"session_id": "...", "score": 0.31, "matched_snippets": ["..."]}]}
```

`session_resume.py`: a compact JSON suitable to inject into the model's context (title, last summary, open questions, last 3 turns).
