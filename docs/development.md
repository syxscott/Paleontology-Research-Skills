# Development Guide

## Adding a new sub-skill

1. Create a new directory under `.claude/skills/paleontology-research-skills/`:
   ```
   .claude/skills/paleontology-research-skills/<new-skill>/
   ├── SKILL.md
   └── scripts/
       └── <main-script>.py
   ```
2. The `SKILL.md` frontmatter MUST include:
   - `name:` — globally unique, lowercase, hyphens, 64 chars max.
   - `description:` — one paragraph (max 1024 chars). State *when to use* and *when NOT to use*.
3. The script should import shared utilities via the sys.path idiom (see `docs/architecture.md`).
4. Add the new sub-skill to the parent's `paleontology-research-skills/SKILL.md` cheat-sheet table.

## Testing

```bash
# Unit tests (when added)
python3 -m unittest discover tests

# Smoke test all scripts
for s in .claude/skills/paleontology-research-skills/*/scripts/*.py; do
  echo "=== $s ==="
  python3 "$s" --help || echo "(no --help)"
done
```

## Style

- Python 3.9+ stdlib only (no third-party imports in skill scripts).
- Every script ends in `if __name__ == "__main__": main()`.
- Every script prints exactly one JSON object via `paleo_common.print_json()`.
- `argparse` for all CLI arguments; no positional args.
- Errors go in the JSON output, never as a stack trace to the user.
