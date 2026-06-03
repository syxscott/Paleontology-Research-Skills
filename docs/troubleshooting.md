# Troubleshooting

Common errors and how to fix them.

---

## Installation

### `ModuleNotFoundError: No module named 'PIL'`

The morphometric sub-skills need Pillow. Install:

```bash
pip install Pillow
```

Or, install with all optional extras:

```bash
pip install -r requirements-dev.txt
# or
pip install -e ".[morphometric]"
```

### `ModuleNotFoundError: No module named 'openpyxl'`

Only needed for Excel export. Install:

```bash
pip install openpyxl
```

If you don't need Excel, just use `--formats json,tps,csv` (skipping `xlsx`).

### `command not found: python3`

Windows often only has `python` (not `python3`). The skill scripts use
`python3` in their `SKILL.md` examples but Claude is smart enough to translate.
For direct CLI use, replace `python3` with `python`.

---

## Skills not loading

### Claude doesn't auto-trigger any skill

1. Confirm the skill is installed: `ls ~/.claude/skills/paleontology-research-skills/` (or `.claude/skills/...` for project-scope).
2. **Restart Claude Code** — skills are loaded at session start.
3. Check `SKILL.md` frontmatter: run the validation script:
   ```bash
   python -c "
   import re, pathlib
   for md in pathlib.Path('.claude/skills').rglob('SKILL.md'):
       fm = md.read_text(encoding='utf-8').split('---', 2)
       print(md, '->', 'OK' if len(fm) >= 3 else 'BAD frontmatter')
   "
   ```
4. Try the slash command instead (`/paleo-fossil ...`) — if that works, the
   skill is fine, just the auto-trigger didn't match.

### Sub-skill `name:` mismatches its directory

Agent Skills spec **requires** `name:` to match the parent directory name.
If you rename a directory, you must also update the `name:` in its `SKILL.md`:

```yaml
---
name: paleo-pbdb       # MUST match the directory: paleo-pbdb/
description: ...
---
```

---

## Network errors

### `HTTP 429: Too Many Requests`

You hit a rate limit on an upstream API.

| Source | Limit | Workaround |
|---|---|---|
| PBDB | Generous (no published limit) | Just retry after a few seconds |
| CrossRef | 50/sec polite-pool | Use the `mailto:` UA (already set) |
| Semantic Scholar | ~1/sec without key | Get a free key, set `S2_API_KEY` env (custom extension) |
| arXiv | 3/sec | Add `time.sleep(1)` between calls |
| Macrostrat | Generous | Just retry |
| Wikidata SPARQL | Strict during outages | Retry after several minutes |
| nkocs.com / IVPP | Unpublished, often 5xx | Best effort; expected to sometimes fail |

### `Network error: timed out`

The remote API is slow or unreachable. The script always returns a clean
error JSON in this case — your output JSON will have an `error` field.

For arxiv specifically, their server is intermittently slow. Retry after
30 seconds.

### `SSL: UNEXPECTED_EOF_WHILE_READING`

Usually a transient TLS issue on the upstream server. Retry.

---

## Windows-specific

### `UnicodeDecodeError: 'gbk' codec can't decode byte ...`

Set the encoding before invoking Python:

```cmd
set PYTHONIOENCODING=utf-8
python script.py
```

Or in PowerShell:

```powershell
$env:PYTHONIOENCODING="utf-8"; python script.py
```

If you see this error inside one of OUR scripts (not your own wrapper), it's a
bug — please [file an issue](https://github.com/syxscott/Paleontology-Research-Skills/issues/new/choose).

### CJK characters in paths

All sub-skill scripts have been tested with Chinese filenames and directory
paths. If you hit a path error, please report with the exact path used.

---

## Morphometric

### `No usable foreground component (size=0, need ≥ N)`

The thresholded image has no foreground pixels in the largest connected
component. Try:

- Lower `--threshold` (default 150; try 100 → more sensitive)
- Pre-process the image to a binary silhouette (black fossil on white)
- Verify the image really has a fossil (open it!)

### `Boundary too short (N pts < required)`

The image is too small or the shape is too simple to support N semilandmarks.
Try:

- Smaller `--num-landmarks` (e.g. 32 instead of 64)
- Higher-resolution image
- Verify the fossil shape isn't a 1-pixel-wide line

### Landmarks look weird in the visualisation

The most common cause is **wrong threshold**. The boundary tracer found the
edge of the IMAGE rather than the fossil. Re-run with:

```bash
python visualize_landmarks.py --image fossil.png --landmarks out/fossil.json --out check.png --show-numbers
```

If the landmarks form a square around the image edge → threshold is too high
(everything is foreground). Lower it.

If only part of the fossil is traced → threshold is too low (parts of the
fossil are below the cutoff). Raise it.

---

## Data files

### Where is `~/.paleontology-research-skills/`?

- Linux / macOS: `/home/<user>/.paleontology-research-skills/` (or `$HOME/.paleontology-research-skills`)
- Windows: `C:\Users\<user>\.paleontology-research-skills\`

Override with `PALEONTOLOGY_RESEARCH_SKILLS_HOME` environment variable:

```bash
export PALEONTOLOGY_RESEARCH_SKILLS_HOME=/data/paleo
```

### How do I reset my profile?

```bash
python .claude/skills/paleontology-research-skills/paleo-profile/scripts/profile_init.py --force
```

⚠️ This overwrites both `soul.md` and `user.md`. Back them up first if customised.

---

## Performance

### Morphometric extraction is slow on large images

The pure-Python boundary tracer is O(N) in image area. For a 4000×4000 image
(16 megapixels), expect 30–60 seconds per image. Workarounds:

- Resize the image first (`Image.thumbnail((1000, 1000))`)
- Process overnight in batch mode

### Research-assistant takes > 60 seconds

It runs up to 5 network calls + 3-5 abstract summaries sequentially.
30-60 seconds is normal. To speed up:

- Reduce `--paper-rows` (e.g. 5 instead of 10)
- Reduce `--summarise-top` (e.g. 1 instead of 5)
- Use `--skip-stratigraphy` / `--skip-taxonomy` to drop stages you don't need

---

## Still stuck?

- Search [Issues](https://github.com/syxscott/Paleontology-Research-Skills/issues)
- Ask in [Discussions](https://github.com/syxscott/Paleontology-Research-Skills/discussions)
- File a new bug report (`/paleo-fossil` template, or [bug report form](https://github.com/syxscott/Paleontology-Research-Skills/issues/new/choose))
