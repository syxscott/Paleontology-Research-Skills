---
description: Aggregate Chinese paleontology / fossil-discovery news
argument-hint: [keyword] [source=nkocs|palaeontology|ivpp|all]
allowed-tools: Bash, Read
---

The user wants Chinese-language paleontology news. Use the
**paleo-china-news** skill:

> $ARGUMENTS

Procedure:

1. Parse $ARGUMENTS — optional keyword filter and optional source restriction.
2. Run:
   ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-china-news/scripts/china_news_fetch.py \
       --limit 10 \
       [--keyword "<KW>"] \
       [--source <SRC>] \
       [--since-days <N>]
   ```
3. Present items with title, source, date (if parsed), and URL.
4. If `errors` is non-empty (a source returned 5xx / timed out), explicitly
   tell the user which source failed and continue with the others.
5. NEVER fabricate news items — if `count == 0`, say so.
