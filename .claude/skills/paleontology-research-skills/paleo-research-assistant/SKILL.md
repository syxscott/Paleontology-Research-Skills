---
name: paleo-research-assistant
description: 🔬 Comprehensive paleontology literature-review automation. Orchestrates the full pipeline: paleo-crossref (find papers) → summarize_paper (top-N abstracts) → paleo-taxonomy (verify taxa) → paleo-pbdb (occurrences) → paleo-stratigraphy (geological context). Synthesises results into a structured Markdown report. Use when the user asks for "a literature review on X", "background research for [topic]", "research summary for [taxon/formation]", or "comprehensive analysis of [group]".
---

# Research Assistant — Automated Literature Review

Orchestrates the entire `paleontology-research-skills` toolkit to produce a comprehensive Markdown research report on a topic / taxon / formation.

## When to Use

- "Write a literature review on Yixian Formation theropods"
- "Background research for Allosauridae"
- "Comprehensive analysis of the Cambrian explosion"
- "Research summary for *Confuciusornis*"
- "Grant proposal background on K-Pg boundary recovery"

## When NOT to Use

- A single targeted query → use the specific sub-skill (`paleo-pbdb`, `paleo-crossref`, etc.)
- Drafting prose / writing the actual review text → that is the user's / model's job after this script gives them the raw materials

## Pipeline

```
User request: <topic / taxon / formation>
       │
       ▼
1. paleo-crossref            → find top-N papers on the topic
       │
       ▼
2. summarize_paper           → 3-bullet summary of each top paper
       │
       ▼
3. paleo-taxonomy            → verify taxon hierarchy (if a taxon is named)
       │
       ▼
4. paleo-pbdb                → fossil occurrence data (if applicable)
       │
       ▼
5. paleo-stratigraphy        → formation context (if applicable)
       │
       ▼
Synthesise → structured Markdown report (sections: Overview, Literature,
             Taxonomy, Occurrences, Stratigraphy, References, Limitations)
```

## Usage

```bash
# Full pipeline on a taxon
python3 scripts/research_assistant.py \
    --topic "Allosaurus" \
    --taxon "Allosaurus" \
    --paper-rows 8 \
    --out-dir reports/

# Full pipeline on a formation
python3 scripts/research_assistant.py \
    --topic "Yixian Formation paleobiology" \
    --formation "Yixian" \
    --paper-rows 8

# Topic only (no PBDB / stratigraphy)
python3 scripts/research_assistant.py \
    --topic "K-Pg boundary mass extinction" \
    --paper-rows 10

# Skip particular stages
python3 scripts/research_assistant.py \
    --topic "morphometrics of trilobites" \
    --skip-stratigraphy --skip-pbdb
```

## Output

A Markdown report saved to `<out-dir>/<topic-slug>-<timestamp>.md` plus a
JSON manifest with every sub-script's raw output.

### Report sections

```markdown
# Research Report — <topic>

**Generated**: 2026-06-03T14:30:00Z
**By**: paleo-research-assistant (paleontology-research-skills v1.0)

## 1. Overview
(human-written; this is the section the model will expand on)

## 2. Literature
- Top N papers (CrossRef) with bullet summaries
- Citation counts (Semantic Scholar, when available)

## 3. Taxonomy
- Verified hierarchy from PBDB
- Authority + first/last appearance

## 4. Fossil Occurrences (PBDB)
- Count, age range, geography
- Top localities & formations

## 5. Stratigraphic Context
- Formation age, location, lithology
- Dominant fauna

## 6. References (with DOIs)

## 7. Limitations & Data Gaps
```

## Notes

- Each sub-script runs **independently**; if one fails (e.g., network issue) the report flags that section as "data unavailable" and continues.
- Total runtime: typically 30-60 seconds (5-7 HTTP requests).
- No fabrication: every claim in the final report is traceable to a sub-script's JSON output.
