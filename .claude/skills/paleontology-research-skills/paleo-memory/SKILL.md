---
name: paleo-memory
description: 📚 Search the user's local research memory (~/.paleontology-research-skills/paleo-memory/) for prior conversations, findings, and notes. Use when the user asks "did I research X before", "what did I find about Y", or wants to recall past conclusions. Returns the most semantically similar past tasks using a hashing-trick vector search (no external API required).
---

# Paleontology Research Skills Memory Recall

Searches the user's local research memory using a built-in hashing-trick TF-IDF vector index. All processing is local — no data leaves the machine.

## When to Use

- "Did I research Allosaurus before?"
- "What did I find about the Yixian Formation in past sessions?"
- "Show my prior findings on K-Pg boundary"
- "Recall my past PBDB queries"
- "List my recent long-term memory entries"

## When NOT to Use

- Listing/browsing past SESSIONS (not tasks) → use `paleo-session`
- "What are my research interests?" → use `paleo-profile`
- Real-time queries on PBDB/CrossRef → use `paleo-pbdb` / `paleo-crossref`

## Usage

```bash
# Semantic search across short + long + archive memory
python3 scripts/memory_search.py --query "Allosaurus Morrison"

# Limit to long-term memory only
python3 scripts/memory_search.py --query "K-Pg boundary" --scope long

# Show status of memory store
python3 scripts/memory_status.py

# List recent long-term memory entries
python3 scripts/memory_list.py --scope long --limit 20
```

## Output

For `memory_search.py`, JSON array of:
- `task_id`, `source` (short/long/archive), `score` (0-1 cosine similarity)
- `command`, `status`, `timestamp`
- `summary` or `error` (whichever is available)

For `memory_list.py`, JSON array of memory entries with full metadata.

For `memory_status.py`:
```json
{
  "shortCount": 42,
  "longCount": 8,
  "memoryRoot": "/home/user/.paleontology-research-skills/memory",
  "shortDir": "/home/user/.paleontology-research-skills/paleo-memory/short",
  "longFile": "/home/user/.paleontology-research-skills/paleo-memory/long_term.jsonl"
}
```

## Data Source

User's local memory at `~/.paleontology-research-skills/paleo-memory/`:
- `short/*.json` — short-term task memory (one JSON per task)
- `long_term.jsonl` — promoted long-term memory (one JSON per line)
- `archive/short/*.json` — archived short-term memory

## Notes

- Search uses a built-in 384-dim hashing-trick vector space (no external embeddings).
- Default min score: 0.12. Increase for stricter results.
- The tool is designed to fail gracefully — if the memory directory doesn't exist, returns empty results.
