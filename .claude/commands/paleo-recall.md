---
description: Search local research memory for prior findings
argument-hint: <topic / question>
allowed-tools: Bash, Read
---

The user wants to recall something from prior research. Use the
**paleo-memory** skill to search the local memory store for:

> $ARGUMENTS

Procedure:
1. Run a semantic search across all memory scopes:
   ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_search.py \
       --query "$ARGUMENTS" --scope all --top-k 5
   ```
2. If `count == 0`, tell the user the memory store has no matching entries
   (do not invent past findings).
3. For each hit, show the `task_id`, `timestamp`, score, and summary or
   conclusion. Order by score (already sorted by the script).
4. If the user is interested in one specific hit, you can also call
   `memory_list.py --scope <short|long|archive>` to inspect raw entries.
