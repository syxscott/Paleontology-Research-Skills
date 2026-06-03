---
name: paleo-stratigraphy
description: 🪨 Look up geological formations / strata data — age, location, lithology, and the fossil taxa found there. Uses PBDB collections + Macrostrat when available. Use when the user asks "what age is the Yixian Formation", "where is the Morrison Formation", "what fossils are in the Hell Creek Formation", or wants to correlate strata across regions.
---

# Stratigraphic Formation Lookup

Queries fossil-bearing geological formations from PBDB (and Macrostrat where available) — returning age, geography, lithology, and the assemblage of taxa recorded.

## When to Use

- "How old is the Yixian Formation?"
- "What's the geographic extent of the Morrison Formation?"
- "What dinosaurs are found in the Hell Creek Formation?"
- "List formations of Late Cretaceous age in China"
- "Correlate the Djadokhta and Barun Goyot formations"

## When NOT to Use

- Specific fossil occurrences without a formation context → use `paleo-pbdb`
- Modern lithology / petrology → out of scope
- Mineral resource exploration → out of scope

## Usage

```bash
# Look up a formation by name (PBDB collections)
python3 scripts/stratigraphy_query.py --formation "Yixian"

# What taxa occur in a formation (limit how many distinct taxa)
python3 scripts/stratigraphy_query.py --formation "Hell Creek" --taxa-limit 30

# Cross-correlation: all formations of a given age range
python3 scripts/stratigraphy_query.py --interval "Late Cretaceous"

# Filter by country
python3 scripts/stratigraphy_query.py --formation "Yixian" --country CN

# Macrostrat enrichment (lithology, units, columns)
python3 scripts/macrostrat_query.py --formation "Morrison"
```

## Output Format

```json
{
  "source": "PBDB",
  "query": {"formation": "Yixian"},
  "summary": {
    "collection_count": 84,
    "occurrence_count": 1247,
    "age_range_ma": {"max": 130.5, "min": 122.0},
    "intervals": ["Aptian", "Barremian"],
    "countries": ["CN"],
    "states": ["Liaoning"],
    "dominant_taxa": [
      {"name": "Confuciusornis sanctus", "occurrences": 84},
      {"name": "Sinornithosaurus", "occurrences": 42}
    ]
  },
  "collections": [...]
}
```

## Data Sources

- **Primary**: Paleobiology Database collections (`https://paleobiodb.org/data1.2/colls/list.json`)
- **Auxiliary**: Macrostrat (`https://macrostrat.org/api/units`) — lithology, column data

## Notes

- Formation names are case-insensitive but spelling-sensitive (use the canonical name, e.g. "Hell Creek" not "Hell-Creek").
- For Chinese formations, use the English transliteration (Yixian, Jiufotang, Shishugou).
- Multiple formations may share the same name in different regions — the script reports all and lets you filter by country.
