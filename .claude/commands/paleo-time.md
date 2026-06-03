---
description: Query the ICS geological time scale
argument-hint: <period name> | <age in Ma> | list
allowed-tools: Bash, Read
---

The user has a geological time question. Use the **paleo-geo-time** skill.

> $ARGUMENTS

Routing (parse $ARGUMENTS):

- If $ARGUMENTS is a **number** (e.g. `100` or `100 Ma`), run:
  ```bash
  python3 .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --age <N>
  ```
  Then report ALL intervals that contain that age (from eonothem down to
  the smallest containing stage/epoch).

- If $ARGUMENTS is `list` or `list periods` / `list epochs`, run:
  ```bash
  python3 .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --list --rank <rank>
  ```

- Otherwise treat $ARGUMENTS as a named interval:
  ```bash
  python3 .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --period "$ARGUMENTS"
  ```

Always report ages in Ma and quote the ICS chart version (`data.version` field).
