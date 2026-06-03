---
name: paleo-crossref
description: 📄 Search scholarly literature in paleontology and geosciences across three sources: CrossRef (primary DOI registry, 150M+ records), Semantic Scholar (citation counts + influential-citation analysis), and arXiv (preprints in geophysics / quantitative biology). Use when the user asks for papers, citations, DOIs, journal articles, recent preprints, or 'most cited papers about X'. Each script outputs structured JSON with title, authors, journal, year, DOI.
---

# CrossRef Literature Search

Queries the CrossRef API (https://api.crossref.org) for scholarly article metadata.

## When to Use

- "Find papers about theropod feather evolution"
- "What has been published on Cambrian explosion?"
- "Give me DOIs for Cretaceous-Paleogene boundary studies"
- "Show recent Allosaurus literature"
- "Find the DOI of the paper by Smith et al. on Morrison dinosaurs"

## When NOT to Use

- "Show me fossil occurrences" → use `paleo-pbdb`
- "What period did X live in?" → use `paleo-geo-time`

## Usage

```bash
# Basic search
python3 scripts/crossref_search.py --query "theropod feather evolution"

# Limit number of results and include abstract
python3 scripts/crossref_search.py --query "K-Pg boundary" --rows 10 --include-abstract

# Apply user profile citation preferences
python3 scripts/crossref_search.py --query "Morrison Formation dinosaurs" --respect-profile
```

## Output

JSON array of article records with:
- `DOI`, `title`, `subtitle`
- `authors` (array of `{"family": "...", "given": "..."}`)
- `container_title` (journal name)
- `publisher`, `published_date` (ISO 8601 partial)
- `type` (journal-article, book-chapter, etc.)
- `abstract` (when available; JATS XML stripped)
- `URL`, `resource_link`

## Data Source

CrossRef — https://api.crossref.org
- API: `https://api.crossref.org/works?query=...`
- CC-BY 4.0 metadata
- 150M+ records
- Polite pool: include `mailto` in User-Agent for better rate limits

## Additional Scripts (Multi-source Search)

```bash
# Semantic Scholar — paper search with citation counts
python3 scripts/semantic_scholar_search.py \
    --query "K-Pg boundary mass extinction" \
    --limit 10 --min-citations 50 --include-abstract

# arXiv — preprint search
python3 scripts/arxiv_search.py \
    --query "dinosaur phylogenetics" \
    --category q-bio.PE --max-results 10 --sort submittedDate
```

| Script | Source | Best for |
|---|---|---|
| `crossref_search.py` | CrossRef | DOI registry, peer-reviewed journals (always start here) |
| `semantic_scholar_search.py` | Semantic Scholar | Citation counts, "most influential papers" |
| `arxiv_search.py` | arXiv | Geophysics & quantitative-biology preprints |
| `summarize_paper.py` | (local) | 3-bullet heuristic summary of any abstract |

### When to combine
- Get DOIs first via CrossRef → enrich with citation counts via Semantic Scholar
- Recent (< 6 months) work → check arXiv for preprints CrossRef may not yet have indexed

## Notes

- Sets a descriptive User-Agent: `Paleontology-Research-Skills/1.0 (mailto:your@email)`
- Rows clamped to 1-50
- Selects only relevant fields to keep responses small
- Returns empty `items` array if no results (does not error)
