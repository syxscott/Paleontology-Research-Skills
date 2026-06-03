---
name: paleo-geo-time
description: ⏳ Query the official ICS (International Commission on Stratigraphy) geological time scale. Use when the user asks "when did the Jurassic start", "what period contains 100 Ma", "list all epochs of the Cenozoic", or similar geo-chronology questions. Returns periods, epochs, eras, and ages in Ma (millions of years ago).
---

# Geological Time Scale Query

Looks up periods, epochs, eras, and ages from the bundled ICS time scale (`./data/ics_timescale.json`).

## When to Use

- "When did the Jurassic begin?"
- "What period contains 100 Ma?"
- "List all epochs of the Cenozoic"
- "How long did the Cretaceous last?"
- "What's the boundary between Permian and Triassic?"

## When NOT to Use

- Fossil occurrences → use `paleo-pbdb`
- Scientific literature → use `paleo-crossref`

## Usage

```bash
# Look up one named interval
python3 scripts/geo_time_query.py --period "Jurassic"

# What interval contains an age (Ma)
python3 scripts/geo_time_query.py --age 100

# List everything at a particular rank
python3 scripts/geo_time_query.py --list --rank period

# List children of a parent
python3 scripts/geo_time_query.py --list --parent "Cenozoic"
```

## Output

```json
{
  "query": {"period": "Jurassic"},
  "matches": [
    {
      "id": "jurassic",
      "name": "Jurassic",
      "rank": "period",
      "startMa": 201.4,
      "endMa": 145.0,
      "durationMa": 56.4,
      "parent": "Mesozoic"
    }
  ]
}
```

## Data Source

International Commission on Stratigraphy (ICS) — https://stratigraphy.org
- Bundled snapshot version: 2023-09
- Updates: replace `./data/ics_timescale.json` when ICS publishes a new chart.
