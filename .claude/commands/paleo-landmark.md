---
description: Extract geometric morphometric landmarks from a fossil image
argument-hint: <image-path> [num-landmarks=64] [threshold=150]
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

The user wants to extract morphometric landmarks from a fossil image. Use the
**paleo-morphometric** skill on this argument:

> $ARGUMENTS

Procedure:

1. Parse $ARGUMENTS — the first token is the image path; optional `num=N` and
   `threshold=T` follow.
2. Run:
   ```bash
   python3 "$PRS"/paleo-morphometric/scripts/extract_landmarks.py \
       --image "<IMAGE_PATH>" \
       --num-landmarks <NUM_OR_64> \
       --threshold <THR_OR_150> \
       --out-dir morphometric_output \
       --formats json,tps,csv
   ```
3. Then visualise:
   ```bash
   python3 "$PRS"/paleo-morphometric/scripts/visualize_landmarks.py \
       --image "<IMAGE_PATH>" \
       --landmarks morphometric_output/<basename>.json \
       --out morphometric_output/<basename>_annotated.png \
       --show-numbers --show-connections
   ```
4. Report: number of landmarks extracted, files written, and any errors.
   Remind the user to visually verify landmark positions in the annotated PNG.
