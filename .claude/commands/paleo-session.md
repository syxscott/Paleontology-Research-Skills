---
description: List, show, search, or resume PaleontologyResearchSkills sessions
argument-hint: list | show <id> | search <query> | resume <id>
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

The user wants to interact with their session history. Use the
**paleo-session** skill. The argument controls the sub-action:

> $ARGUMENTS

Routing:

| First word of $ARGUMENTS | Run |
|---|---|
| `list` (or empty) | `session_list.py --limit 20` |
| `show <id>` | `session_show.py --id <id>` |
| `search <query>` | `session_search.py --query "<query>" --top-k 5` |
| `resume <id>` | `session_resume.py --id <id>` |

All scripts live in `$PRS/paleo-session/scripts/`.

For `resume`: the output is meant to be **silently injected into context** as
a "where we left off" note, not echoed verbatim to the user. Tell the user
"resumed session X" and then continue the actual research task.
