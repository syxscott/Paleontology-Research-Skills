---
description: Query PBDB for fossil occurrences of a taxon
argument-hint: <taxon-name or natural-language description>
allowed-tools: Bash, Read
---
Before running any script, resolve the toolkit root (supports both
**user-level** install at `~/.claude/skills/` and **project-level** install at
`.claude/skills/`):

```bash
if [ -d "$HOME/.claude/skills/paleontology-research-skills" ]; then
  PRS="$HOME/.claude/skills/paleontology-research-skills"
else
  PRS=".claude/skills/paleontology-research-skills"
fi
```

The user wants fossil occurrences. Use the **paleo-pbdb** skill to query the
Paleobiology Database for:

> $ARGUMENTS

Procedure:
1. Identify the taxon name (genus or higher) from the user's request.
2. Run the PBDB query script with `--respect-profile` so the user's preferred
   occurrence limit applies:
   ```bash
   python3 "$PRS"/paleo-pbdb/scripts/pbdb_query.py \
       --base-name "<TAXON>" --respect-profile
   ```
   If the user supplied an age range, also pass `--min-ma` / `--max-ma`.
3. Summarise the JSON result for the user: total occurrence count, geological
   intervals covered, dominant formations, age range in Ma, and a brief
   geographic spread (countries/states).
4. Always cite **Paleobiology Database (https://paleobiodb.org, CC-BY 4.0)** as
   the source.
5. Do **not** invent any record that is not present in the returned JSON.
