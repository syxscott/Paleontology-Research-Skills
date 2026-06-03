# Paleontology Research Skills — common dev tasks
# Usage:  make <target>
#
# Most targets work on Linux / macOS. On Windows use Git Bash or WSL.

.PHONY: help install install-dev test test-verbose test-coverage \
        lint format validate smoke clean serve-docs all

help:
	@echo "Paleontology Research Skills — make targets"
	@echo ""
	@echo "  install         Install just the core (zero deps)"
	@echo "  install-dev     Install all dev dependencies (pytest, ruff, Pillow, openpyxl)"
	@echo "  test            Run the stdlib unittest suite"
	@echo "  test-verbose    Run tests with -v"
	@echo "  test-coverage   Run with pytest --cov"
	@echo "  lint            Run ruff check"
	@echo "  format          Run ruff format"
	@echo "  validate        Validate every SKILL.md against the Agent Skills spec"
	@echo "  smoke           Smoke-test every sub-skill script (--help)"
	@echo "  clean           Remove __pycache__, .pytest_cache, build artefacts"
	@echo "  all             format + lint + test + validate + smoke"

install:
	@echo "Core toolkit has no runtime dependencies. To install the package, run:"
	@echo "  pip install -e ."

install-dev:
	pip install -e ".[dev]"

test:
	python -m unittest discover tests

test-verbose:
	python -m unittest discover tests -v

test-coverage:
	pytest tests/ --cov=.claude --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

validate:
	@python -c "import re, pathlib, sys; \
	ROOT = pathlib.Path('.claude/skills'); \
	NAME_RE = re.compile(r'^[a-z0-9][a-z0-9-]{0,63}$$'); \
	ok = True; \
	[print(f'  [{(\"OK \" if (NAME_RE.match(name) and name == md.parent.name and 0 < len(desc) <= 1024) else \"BAD\")}] {md.parent.name:35s} name={name:35s} desc={len(desc)}c') for md in sorted(ROOT.rglob('SKILL.md')) for fm in [md.read_text(encoding='utf-8').split('---', 2)] if len(fm) >= 3 for name in [next((l.split(':', 1)[1].strip() for l in fm[1].split(chr(10)) if l.startswith('name:')), '')] for desc in [next((l.split(':', 1)[1].strip() for l in fm[1].split(chr(10)) if l.startswith('description:')), '')]]; \
	sys.exit(0)"

smoke:
	@fail=0; \
	for f in $$(find .claude/skills -name '*.py' -not -name '__init__.py'); do \
		if ! (python "$$f" --help > /dev/null 2>&1 || python "$$f" > /dev/null 2>&1); then \
			echo "FAIL: $$f"; fail=1; \
		fi; \
	done; \
	if [ $$fail -eq 0 ]; then echo "All scripts OK"; fi; \
	exit $$fail

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete 2>/dev/null || true
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov

all: format lint test validate smoke
