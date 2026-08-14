---
description: Aggregate Chinese paleontology / fossil-discovery news
argument-hint: [keyword] [source=nkocs|palaeontology|ivpp|all]
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

The user wants Chinese-language paleontology news. Use the
**paleo-china-news** skill:

> $ARGUMENTS

Procedure:

1. Parse $ARGUMENTS — optional keyword filter and optional source restriction.
2. Run:
   ```bash
   python3 "$PRS"/paleo-china-news/scripts/china_news_fetch.py \
       --limit 10 \
       [--keyword "<KW>"] \
       [--source <SRC>] \
       [--since-days <N>]
   ```
3. Present items with title, source, date (if parsed), and URL.
4. If `errors` is non-empty (a source returned 5xx / timed out), explicitly
   tell the user which source failed and continue with the others.
5. NEVER fabricate news items — if `count == 0`, say so.
