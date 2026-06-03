---
description: PaleontologyResearchSkills toolkit overview & status
allowed-tools: Bash, Read
---

Show the user a one-page overview of the **paleontology-research-skills** toolkit they have
installed, and a quick status check.

Procedure:

1. Run profile + memory status to confirm everything is wired:
   ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_load.py
   python3 .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_status.py
   ```

2. Present the user with this menu:

   | Slash command | Backed by skill | What it does |
   |---|---|---|
   | `/paleo-fossil <taxon>` | paleo-pbdb | Query PBDB for fossil occurrences |
   | `/paleo-paper <topic>`  | paleo-crossref | Search CrossRef for literature |
   | `/paleo-recall <query>` | paleo-memory | Search local research memory |
   | `/paleo-session [list\|show\|search\|resume]` | paleo-session | Browse / resume sessions |
   | `/paleo-me` | paleo-profile | Show research profile |
   | `/paleo-time <period\|Ma>` | paleo-geo-time | Geological time scale |
   | `/paleo` | (this command) | Toolkit overview |

3. Remind the user that **even without the slash commands**, the skills will
   auto-trigger when their natural-language prompts match. The slash commands
   are just explicit shortcuts.

4. The user data lives at `~/.paleontology-research-skills/` (override with
   `PALEONTOLOGY_RESEARCH_SKILLS_HOME`).
