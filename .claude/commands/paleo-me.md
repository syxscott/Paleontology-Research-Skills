---
description: Show the user's research profile (role, periods, preferences)
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

The user wants to see (or refresh) their research profile. Use the
**paleo-profile** skill:

```bash
python3 "$PRS"/paleo-profile/scripts/profile_show.py
```

If the JSON returned by `profile_show.py --json` indicates the profile is the
unedited default (e.g. `institution == "(unset)"`), gently suggest the user run:

```bash
python3 "$PRS"/paleo-profile/scripts/profile_init.py
```

and then edit `~/.paleontology-research-skills/user.md` to add their actual role, institution,
preferred periods, and citation format.
