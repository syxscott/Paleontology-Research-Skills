---
description: Query geological formation/stratigraphy — age, taxa, location
argument-hint: <formation-name> [country=CN]
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

The user wants stratigraphic data on a formation. Use the
**paleo-stratigraphy** skill:

> $ARGUMENTS

Procedure:

1. Parse $ARGUMENTS for the formation name (and optional country code).
2. Run PBDB collections query:
   ```bash
   python3 "$PRS"/paleo-stratigraphy/scripts/stratigraphy_query.py \
       --formation "<FORMATION>" \
       --taxa-limit 20 \
       [--country <CC>]
   ```
3. Optionally enrich with Macrostrat (lithology, member/group hierarchy):
   ```bash
   python3 "$PRS"/paleo-stratigraphy/scripts/macrostrat_query.py \
       --formation "<FORMATION>"
   ```
4. Report: collection count, age range (Ma), intervals, countries/states,
   dominant taxa, lithology (if Macrostrat returns data).
