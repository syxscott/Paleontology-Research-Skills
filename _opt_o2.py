#!/usr/bin/env python3
"""Optimization Batch O2 — P1 quality: CI, issue/PR templates, SECURITY,
shared constants, code unification."""

import pathlib
import re

ROOT = pathlib.Path(r"D:\GIthub\自制Claude Code skills")
PARENT = ROOT / ".claude" / "skills" / "paleontology-research-skills"
GH = ROOT / ".github"

FILES = {}

# ============ 1. SECURITY.md ============
FILES[ROOT / "SECURITY.md"] = """# Security Policy

## Supported versions

| Version | Supported          |
|---------|--------------------|
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a vulnerability

If you discover a security issue in **Paleontology Research Skills**, please
report it **privately** so it can be fixed before disclosure:

1. **Preferred**: Email the maintainer at **syxemail@yeah.net**
   with the subject line `SECURITY: <short description>`.
2. **Alternative**: Open a
   [private security advisory](https://github.com/syxscott/Paleontology-Research-Skills/security/advisories/new)
   on GitHub.

Please include:

- Affected skill / script / version
- Steps to reproduce
- Impact assessment (data exposure, RCE, DoS, etc.)
- Suggested mitigation (if any)

We aim to acknowledge reports within **5 business days** and to publish a
patch within **30 days** for high-severity issues.

## Scope

In-scope security concerns include:

- Command injection via user input passed to subprocess
- Path traversal in profile / memory / session paths
- Excessive resource consumption (memory, CPU) from crafted input
- Vulnerabilities in bundled data (e.g. malformed ICS JSON)
- Leakage of credentials or local data to upstream APIs

**Out-of-scope** (not security issues — open a regular Issue):

- Bugs in scientific results (use Issues, not security)
- Rate-limiting from upstream APIs (PBDB, CrossRef, etc.)
- Failures of the optional `Pillow` / `openpyxl` dependencies

## Disclosure

After a fix is released, we will publish a CVE-style advisory in the
[Security tab](https://github.com/syxscott/Paleontology-Research-Skills/security)
and credit reporters who wish to be acknowledged.
"""


# ============ 2. CI workflow: tests across Python versions × OS ============
FILES[GH / "workflows" / "test.yml"] = """name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  unittest:
    name: unittest (${{ matrix.os }} / Py ${{ matrix.python }})
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python: ["3.9", "3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}

      - name: Install optional deps (Pillow, openpyxl)
        run: |
          python -m pip install --upgrade pip
          pip install Pillow openpyxl

      - name: Run unittest suite
        run: python -m unittest discover tests -v
        env:
          PYTHONIOENCODING: utf-8

      - name: Smoke-test every sub-skill script
        shell: bash
        run: |
          fail=0
          for f in $(find .claude/skills -name "*.py" -not -name "__init__.py"); do
            if ! (python "$f" --help > /dev/null 2>&1 || python "$f" > /dev/null 2>&1); then
              echo "FAIL: $f"; fail=1
            fi
          done
          exit $fail
        env:
          PYTHONIOENCODING: utf-8
          PALEONTOLOGY_RESEARCH_SKILLS_HOME: ${{ runner.temp }}/paleo-home

      - name: Offline functional sanity (geo-time)
        run: |
          python .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --period Jurassic
        env:
          PYTHONIOENCODING: utf-8
"""


# ============ 3. CI workflow: validate Agent Skills frontmatter ============
FILES[GH / "workflows" / "validate-skills.yml"] = """name: Validate Skills

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Validate every SKILL.md against the Agent Skills spec
        run: |
          python <<\'PY\'
          import re, pathlib, sys

          ROOT = pathlib.Path(".claude/skills")
          NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
          all_ok = True

          for md in sorted(ROOT.rglob("SKILL.md")):
              text = md.read_text(encoding="utf-8")
              fm = text.split("---", 2)
              if len(fm) < 3:
                  print(f"::error file={md}::missing YAML frontmatter")
                  all_ok = False
                  continue
              name = next((l.split(":", 1)[1].strip()
                          for l in fm[1].split("\\n") if l.startswith("name:")), "")
              desc = next((l.split(":", 1)[1].strip()
                          for l in fm[1].split("\\n") if l.startswith("description:")), "")

              if not NAME_RE.match(name):
                  print(f"::error file={md}::name '{name}' does not match ^[a-z0-9][a-z0-9-]{{0,63}}$")
                  all_ok = False
              if name != md.parent.name:
                  print(f"::error file={md}::name '{name}' does not match parent directory '{md.parent.name}'")
                  all_ok = False
              if not desc:
                  print(f"::error file={md}::missing description")
                  all_ok = False
              elif len(desc) > 1024:
                  print(f"::error file={md}::description {len(desc)} chars > 1024 limit")
                  all_ok = False
              else:
                  print(f"OK: {md.parent.name} (name={name}, desc={len(desc)} chars)")

          sys.exit(0 if all_ok else 1)
          PY

      - name: Validate slash commands have description
        run: |
          python <<\'PY\'
          import pathlib, sys
          all_ok = True
          for md in sorted(pathlib.Path(".claude/commands").glob("*.md")):
              text = md.read_text(encoding="utf-8")
              if "description:" not in text.split("---", 2)[1] if "---" in text else "":
                  print(f"::error file={md}::missing description in frontmatter")
                  all_ok = False
              else:
                  print(f"OK: /{md.stem}")
          sys.exit(0 if all_ok else 1)
          PY
"""


# ============ 4. CI workflow: lint with ruff (warning only) ============
FILES[GH / "workflows" / "lint.yml"] = """name: Lint

on:
  pull_request:
    branches: [main]

jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff
      - name: Ruff check (informational, does not fail CI)
        run: ruff check . --output-format=github || true
      - name: Ruff format check
        run: ruff format --check . || true
"""


# ============ 5. Issue templates ============
FILES[GH / "ISSUE_TEMPLATE" / "config.yml"] = """blank_issues_enabled: false
contact_links:
  - name: 💬 Question / discussion
    url: https://github.com/syxscott/Paleontology-Research-Skills/discussions
    about: For general questions and ideas, please use Discussions.
  - name: 🔒 Security issue
    url: https://github.com/syxscott/Paleontology-Research-Skills/security/advisories/new
    about: For security vulnerabilities, please file a private advisory.
"""


FILES[GH / "ISSUE_TEMPLATE" / "bug_report.yml"] = """name: 🐛 Bug report
description: Something doesn't work as expected.
title: "[bug] "
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for reporting a bug! Please fill in the fields below so we can reproduce.

  - type: dropdown
    id: skill
    attributes:
      label: Which skill / script?
      options:
        - paleo-pbdb
        - paleo-crossref
        - paleo-memory
        - paleo-session
        - paleo-profile
        - paleo-geo-time
        - paleo-taxonomy
        - paleo-stratigraphy
        - paleo-morphometric
        - paleo-morphometric-convert
        - paleo-research-assistant
        - paleo-china-news
        - parent (paleontology-research-skills)
        - slash command
        - shared utilities (paleo_common / taxonomy)
        - other / not sure
    validations:
      required: true

  - type: textarea
    id: command
    attributes:
      label: Command you ran
      description: Exact CLI invocation (or natural-language prompt to Claude Code)
      render: bash
      placeholder: |
        python3 .claude/skills/paleontology-research-skills/paleo-pbdb/scripts/pbdb_query.py --base-name Allosaurus --limit 5
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected behavior
    validations:
      required: true

  - type: textarea
    id: actual
    attributes:
      label: Actual behavior (paste JSON output or error message)
      render: text
    validations:
      required: true

  - type: input
    id: python
    attributes:
      label: Python version
      placeholder: "3.12.0"
    validations:
      required: true

  - type: dropdown
    id: os
    attributes:
      label: Operating system
      options:
        - Linux
        - macOS
        - Windows
        - WSL
        - other
    validations:
      required: true

  - type: input
    id: install
    attributes:
      label: Installation scope
      description: How did you install (project-scope `.claude/` or user-scope `~/.claude/`)?
      placeholder: "user-scope"

  - type: textarea
    id: extra
    attributes:
      label: Anything else?
      description: Logs, screenshots, related issues, etc.
"""


FILES[GH / "ISSUE_TEMPLATE" / "feature_request.yml"] = """name: ✨ Feature request
description: Suggest a new capability or improvement.
title: "[feat] "
labels: ["enhancement"]
body:
  - type: textarea
    id: problem
    attributes:
      label: What problem does this solve?
      description: Describe the use-case or pain point.
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed solution
      description: What should happen? How would the user invoke it?
    validations:
      required: true

  - type: dropdown
    id: kind
    attributes:
      label: Kind of change
      options:
        - New sub-skill
        - Extend existing sub-skill
        - New slash command
        - New data source / API
        - Documentation
        - Build / CI
        - Other
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives considered

  - type: textarea
    id: extra
    attributes:
      label: Additional context
"""


FILES[GH / "ISSUE_TEMPLATE" / "skill_request.yml"] = """name: 🦕 New sub-skill proposal
description: Propose a new sub-skill (e.g. paleo-isotope, paleo-amber, paleo-trace).
title: "[skill] paleo-<name>: "
labels: ["enhancement", "new-skill"]
body:
  - type: input
    id: name
    attributes:
      label: Proposed skill name
      placeholder: "paleo-isotope"
      description: Must be lowercase, hyphenated, ≤64 chars (Agent Skills spec).
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: One-paragraph description
      description: Use the exact tone of an existing SKILL.md (≤1024 chars).
      placeholder: |
        🧪 Compute stable-isotope ratios (δ13C, δ18O, δ15N) from paired
        substrate/standard measurements. Use when the user asks ...
    validations:
      required: true

  - type: textarea
    id: triggers
    attributes:
      label: When should Claude trigger this skill?
      placeholder: |
        - "Calculate δ13C from these CO2 measurements"
        - "Compare oxygen isotopes between samples X and Y"
        - ...
    validations:
      required: true

  - type: textarea
    id: data_source
    attributes:
      label: Primary data source / API
      description: e.g. a public REST API, a bundled JSON dataset, or pure calculation
    validations:
      required: true

  - type: textarea
    id: out_of_scope
    attributes:
      label: When NOT to use this skill
"""


# ============ 6. PR template ============
FILES[GH / "PULL_REQUEST_TEMPLATE.md"] = """## Summary

<!-- One sentence: what does this PR change? -->

## Why

<!-- The user-visible reason. Link to the issue if any. -->

Refs: #

## Type of change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds capability)
- [ ] 🦕 New sub-skill
- [ ] ⚡ Performance improvement
- [ ] 📚 Documentation only
- [ ] 🔧 Build / CI / tooling
- [ ] 💥 Breaking change (would require users to update their setup)

## Checklist

- [ ] My code follows the style in `CONTRIBUTING.md`
- [ ] I have updated the relevant `SKILL.md` if behavior changed
- [ ] I have updated `CHANGELOG.md` under `## [Unreleased]`
- [ ] I have added tests in `tests/` (or explained why none are needed)
- [ ] All existing tests still pass (`python -m unittest discover tests`)
- [ ] Smoke test passes (`python <script> --help` for every changed script)
- [ ] If I added a new sub-skill, I also:
  - [ ] Added a row to the parent `SKILL.md` routing table
  - [ ] Updated `README.md`
  - [ ] (Optional) Created a `/paleo-<x>` slash command

## Scientific integrity

- [ ] Output JSON cites the data source (`"source"` field)
- [ ] No fabricated taxa, DOIs, ages, or occurrences
- [ ] Network errors are caught and embedded in JSON (no stack traces leak)

## Screenshots / output

<!-- Paste the JSON output or a screenshot showing the new behavior -->

```json

```
"""


# ============ 7. dependabot config ============
FILES[GH / "dependabot.yml"] = """version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "ci"
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "monthly"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"
      - "python"
"""


# ============ 8. FUNDING.yml (placeholder) ============
FILES[GH / "FUNDING.yml"] = """# These links appear under the "Sponsor" button on GitHub.
# Uncomment / customise as you create funding accounts.

# github: [syxscott]
# patreon: <username>
# open_collective: <slug>
# ko_fi: <username>
# custom: ["https://yoursite/donate"]
"""


# Write all files
for path, content in FILES.items():
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    print(f"  wrote {path.relative_to(ROOT)} ({len(content)} bytes)")


# ============ 9. Unify UA + TIMEOUT across all skill scripts ============
print("\n--- Unifying UA + TIMEOUT across skill scripts ---")

CANONICAL_UA = (
    "Paleontology-Research-Skills/1.0 "
    "(https://github.com/syxscott/Paleontology-Research-Skills; "
    "mailto:syxemail@yeah.net)"
)
CANONICAL_TIMEOUT = 30

# Patterns to replace
UA_PATTERNS = [
    re.compile(r'UA = "Paleontology-Research-Skills/1\.0 \(https://paleoclaw\.local; mailto:[^"]+\)"'),
    re.compile(
        r'UA = "Paleontology-Research-Skills/1\.0 \(https://paleontology-research-skills\.local; mailto:[^"]+\)"'
    ),
    re.compile(r'UA = "Paleontology-Research-Skills/1\.0 \(mailto:[^"]+\)"'),
]

unified_ua = 0
unified_timeout = 0

for py in PARENT.rglob("*.py"):
    if "__pycache__" in str(py):
        continue
    text = py.read_text(encoding="utf-8")
    orig = text

    # Unify UA
    for pat in UA_PATTERNS:
        text = pat.sub(f'UA = "{CANONICAL_UA}"', text)

    # Special case for china_news_fetch.py's Mozilla-style UA
    text = re.sub(
        r'UA = \("Mozilla/5\.0 \(compatible; Paleontology-Research-Skills/1\.0; "[^)]*\)',
        f'UA = ("Mozilla/5.0 (compatible; {CANONICAL_UA[:-1]}; respectful crawler)")',
        text,
    )

    # Unify TIMEOUT (rename DEFAULT_TIMEOUT → TIMEOUT, value 30)
    text = re.sub(r"^DEFAULT_TIMEOUT = \d+", f"TIMEOUT = {CANONICAL_TIMEOUT}", text, flags=re.MULTILINE)
    text = re.sub(r"^TIMEOUT = \d+", f"TIMEOUT = {CANONICAL_TIMEOUT}", text, flags=re.MULTILINE)
    # Rename uses of DEFAULT_TIMEOUT inside function bodies
    text = text.replace("DEFAULT_TIMEOUT", "TIMEOUT")

    if text != orig:
        py.write_text(text, encoding="utf-8", newline="\n")
        if "UA = " in text and "UA = " in orig:
            unified_ua += 1
        unified_timeout += 1
        print(f"  unified {py.relative_to(ROOT)}")

print(f"\nO2 done: {len(FILES)} new files + {unified_timeout} scripts unified.")
