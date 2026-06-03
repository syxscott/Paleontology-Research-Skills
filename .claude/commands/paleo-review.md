---
description: Generate a comprehensive literature-review report on a topic / taxon / formation
argument-hint: <topic> [taxon=...] [formation=...]
allowed-tools: Bash, Read
---

The user wants a comprehensive paleontology literature review. Use the
**paleo-research-assistant** orchestrator:

> $ARGUMENTS

Procedure:

1. Parse $ARGUMENTS for the main topic. If a specific taxon or formation is
   mentioned, pass them as `--taxon` / `--formation`.
2. Run the full pipeline:
   ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-research-assistant/scripts/research_assistant.py \
       --topic "<TOPIC>" \
       [--taxon "<TAXON>"] \
       [--formation "<FORMATION>"] \
       --paper-rows 8 \
       --summarise-top 3 \
       --out-dir paleo_reports
   ```
3. The script prints a JSON with `report_md` (path to the Markdown file).
   Show the user the file path and a brief summary of which stages ran
   (literature / taxonomy / pbdb / stratigraphy).
4. Offer to render the report's Overview section inline.
5. If any stage failed (network, rate-limit), explicitly note it as a
   data gap — do not invent missing content.
