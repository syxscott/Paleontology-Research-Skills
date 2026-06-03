---
description: Show the user's research profile (role, periods, preferences)
allowed-tools: Bash, Read
---

The user wants to see (or refresh) their research profile. Use the
**paleo-profile** skill:

```bash
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_show.py
```

If the JSON returned by `profile_show.py --json` indicates the profile is the
unedited default (e.g. `institution == "(unset)"`), gently suggest the user run:

```bash
python3 .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py
```

and then edit `~/.paleontology-research-skills/user.md` to add their actual role, institution,
preferred periods, and citation format.
