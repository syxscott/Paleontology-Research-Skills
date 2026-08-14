---
description: Query the ICS geological time scale
argument-hint: <period name> | <age in Ma> | list
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

The user has a geological time question. Use the **paleo-geo-time** skill.

> $ARGUMENTS

Routing (parse $ARGUMENTS):

- If $ARGUMENTS is a **number** (e.g. `100` or `100 Ma`), run:
  ```bash
  python3 "$PRS"/paleo-geo-time/scripts/geo_time_query.py --age <N>
  ```
  Then report ALL intervals that contain that age (from eonothem down to
  the smallest containing stage/epoch).

- If $ARGUMENTS is `list` or `list periods` / `list epochs`, run:
  ```bash
  python3 "$PRS"/paleo-geo-time/scripts/geo_time_query.py --list --rank <rank>
  ```

- Otherwise treat $ARGUMENTS as a named interval:
  ```bash
  python3 "$PRS"/paleo-geo-time/scripts/geo_time_query.py --period "$ARGUMENTS"
  ```

Always report ages in Ma and quote the ICS chart version (`data.version` field).
