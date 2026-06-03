---
name: paleo-profile
description: 👤 Load and apply the user's research profile from `~/.paleontology-research-skills/soul.md` and `~/.paleontology-research-skills/user.md`. Use when the user asks "what do you know about my research", or when starting any task where the user's scientific role, domain, preferred periods/regions, citation style, or output language should influence the response. Also use when the user asks to initialize or inspect their profile.
---

# Paleontology Research Skills Research Profile

Loads the user's research profile from their `~/.paleontology-research-skills/soul.md` (system identity + scientific principles) and `~/.paleontology-research-skills/user.md` (personal research preferences), and presents the structured fields to the model.

## When to Use

- "What do you know about my research interests?"
- "What are my preferred citation formats?"
- "Show me my profile."
- "Initialize my profile."
- Before any task where the user's role, language, or research focus should affect the response.

## When NOT to Use

- "Find fossils in PBDB" → use `paleo-pbdb` instead
- "Search for literature" → use `paleo-crossref`
- "What did I research last week?" → use `paleo-memory`

## Usage

```bash
# Show the parsed profile as JSON
python3 scripts/profile_show.py --json

# Pretty-print human-readable profile
python3 scripts/profile_show.py

# Initialise (or re-initialise) the profile files
python3 scripts/profile_init.py

# Just show the user's role and language
python3 scripts/profile_load.py
```

## Output

`profile_show.py` returns a JSON object like:

```json
{
  "user": {
    "role": "paleontology researcher",
    "domain": "vertebrate paleontology",
    "institution": "China University of Geosciences (Wuhan)",
    "researchFocus": {
      "primaryInterests": ["Theropod dinosaurs", "Jurassic stratigraphy"],
      "preferredPeriods": ["Jurassic", "Cretaceous"],
      "preferredRegions": ["China (Liaoning, Xinjiang)"]
    },
    "languagePreference": "Chinese or English",
    "outputLanguage": "Chinese (simplified)",
    "citationFormat": "APA"
  },
  "soul": {
    "mission": "Help users conduct reliable, reproducible paleontological research.",
    "corePrinciples": ["Scientific Integrity: ...", "Verifiability: ..."],
    "safetyBoundaries": ["Do not fabricate species names ..."]
  }
}
```

## Notes

- The skill reads from `~/.paleontology-research-skills/soul.md` and `~/.paleontology-research-skills/user.md`. If neither exists, the bundled minimal defaults are used (see `scripts/paleo_common.py` for `_DEFAULT_SOUL` / `_DEFAULT_USER`).
- Override the data root with the `PALEONTOLOGY_RESEARCH_SKILLS_HOME` environment variable.
- The profile is purely advisory — apply it to the user's request and continue with the actual task (e.g., look up specimens, search literature).
