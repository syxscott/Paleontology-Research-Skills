---
description: Convert morphometric landmark data between TPS, CSV, JSON, Excel, NTSys
argument-hint: <input-file> <to-format> [out-path]
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

The user wants to convert a morphometric landmark dataset between formats.
Use the **paleo-morphometric-convert** skill:

> $ARGUMENTS

Procedure:

1. Parse $ARGUMENTS for the input file path and target format
   (`tps`, `csv`, `json`, `nts`, `xlsx`).
2. Run:
   ```bash
   python3 "$PRS"/paleo-morphometric-convert/scripts/convert.py \
       --input "<INPUT>" \
       --to <FORMAT> \
       --out "<OUTPUT or default>"
   ```
3. If the user said "validate" / "check" without specifying a target format,
   add `--validate` instead of `--to`.
4. Report specimens count, landmarks per specimen, and any validation warnings.
