# Examples — end-to-end workflows

These are concrete walkthroughs you can copy-paste. Replace placeholders.

---

## Workflow 1 — Quick literature scan on a topic

**Goal**: "What's the recent literature on theropod feather evolution?"

### Way A: natural language (lazy)

In Claude Code, just say:

> Find recent papers on theropod feather evolution.

Claude auto-triggers `paleo-crossref`.

### Way B: slash command (explicit)

```
/paleo-paper theropod feather evolution
```

### Way C: raw script (reproducible)

```bash
python .claude/skills/paleontology-research-skills/paleo-crossref/scripts/crossref_search.py \
    --query "theropod feather evolution" \
    --rows 15 \
    --include-abstract \
    --filter-from-year 2020 \
    --respect-profile
```

---

## Workflow 2 — Verify a taxon name and get its hierarchy

**Goal**: "Is *Brontosaurus* a valid taxon? What family is it in?"

```
/paleo-classify Brontosaurus
```

Or:

```bash
python .claude/skills/paleontology-research-skills/paleo-taxonomy/scripts/taxonomy_query.py \
    --name "Brontosaurus"
```

Output includes status (`valid` / `synonym`), authority, full hierarchy
(kingdom→phylum→class→order→family→genus), and time range.

---

## Workflow 3 — Investigate a geological formation

**Goal**: "What's the Yixian Formation — age, location, dominant taxa?"

```
/paleo-strat Yixian
```

Or stack two scripts for richer data:

```bash
# PBDB collections + dominant taxa
python .claude/skills/paleontology-research-skills/paleo-stratigraphy/scripts/stratigraphy_query.py \
    --formation "Yixian" --taxa-limit 30

# Macrostrat lithology + columns
python .claude/skills/paleontology-research-skills/paleo-stratigraphy/scripts/macrostrat_query.py \
    --formation "Yixian"
```

---

## Workflow 4 — Full literature-review report (orchestrator)

**Goal**: "Write a literature review on *Allosaurus* paleobiology."

```
/paleo-review Allosaurus paleobiology
```

Or with extra context:

```bash
python .claude/skills/paleontology-research-skills/paleo-research-assistant/scripts/research_assistant.py \
    --topic "Allosaurus paleobiology" \
    --taxon "Allosaurus" \
    --formation "Morrison" \
    --paper-rows 10 \
    --summarise-top 5 \
    --out-dir reports/
```

Output: a Markdown file with sections **Overview**, **Literature**,
**Taxonomy**, **Occurrences**, **Stratigraphy**, **References**, **Limitations**.

The script runs 5 stages — if a stage fails (network, rate-limit) the report
explicitly notes "data unavailable" and continues.

---

## Workflow 5 — Morphometric pipeline on a fossil image

**Goal**: Extract 64 semi-landmarks from an ammonoid photo, export to TPS for
MorphoJ.

### Step 1: extract

```
/paleo-landmark ammonoid_001.png
```

Or:

```bash
python .claude/skills/paleontology-research-skills/paleo-morphometric/scripts/extract_landmarks.py \
    --image ammonoid_001.png \
    --num-landmarks 64 \
    --threshold 150 \
    --out-dir results/ \
    --formats json,tps,csv
```

### Step 2: visualise (always check!)

```bash
python .claude/skills/paleontology-research-skills/paleo-morphometric/scripts/visualize_landmarks.py \
    --image ammonoid_001.png \
    --landmarks results/ammonoid_001.json \
    --out results/ammonoid_001_check.png \
    --show-numbers --show-connections
```

If landmarks look misplaced, adjust `--threshold` (default 150 — lower = more
foreground sensitive).

### Step 3: batch-process a directory

```bash
python .claude/skills/paleontology-research-skills/paleo-morphometric/scripts/batch_extract.py \
    --image-dir specimens/ \
    --out-dir morphometric_results/ \
    --num-landmarks 64 \
    --formats json \
    --aggregate tps,csv,xlsx
```

You'll get one JSON per specimen plus aggregated TPS / CSV / Excel for the
whole batch.

### Step 4: convert to another format

```bash
# TPS → Excel for inspection
python .claude/skills/paleontology-research-skills/paleo-morphometric-convert/scripts/convert.py \
    --input morphometric_results/all_specimens.tps \
    --to xlsx \
    --out morphometric_results/all_specimens.xlsx
```

---

## Workflow 6 — Time-scale lookups

**Goal**: "When did the Triassic start? What period contains 250 Ma?"

```bash
# By name
python .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --period Triassic

# By age
python .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py --age 250

# List all periods of an era
python .claude/skills/paleontology-research-skills/paleo-geo-time/scripts/geo_time_query.py \
    --list --parent Mesozoic --rank period
```

All offline — uses bundled ICS chart (2023-09).

---

## Workflow 7 — Personal research memory

After Claude does some research, save it to your local memory store, then
later recall via natural-language query.

```bash
# Status of your memory store
python .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_status.py

# Search for prior research
python .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_search.py \
    --query "Allosaurus Morrison stratigraphy" \
    --top-k 5

# List recent entries
python .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_list.py \
    --scope all --limit 20

# Archive old short-term memory
python .claude/skills/paleontology-research-skills/paleo-memory/scripts/memory_archive.py \
    --days 30
```

Or in Claude Code:

> Did I research the Yixian Formation before?

Auto-triggers `paleo-memory`.

---

## Workflow 8 — Chinese fossil news

```
/paleo-news 恐龙
```

Or:

```bash
python .claude/skills/paleontology-research-skills/paleo-china-news/scripts/china_news_fetch.py \
    --keyword "恐龙" \
    --since-days 30 \
    --limit 10
```

Note: this scrapes public Chinese fossil news sites which may rate-limit or
change HTML structure. Errors per source are reported in the output.
