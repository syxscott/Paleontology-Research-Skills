---
name: paleo-pbdb
description: 🦕 Query the Paleobiology Database (PBDB) for fossil occurrence records. Use when the user asks for fossil occurrences, locality data, taxonomic occurrence counts, stratigraphic context, or "what fossils are found in [formation/period]". Returns JSON with occurrence IDs, taxon names, ages in Ma, coordinates, countries, and formations.
---

# PBDB Fossil Occurrence Query

Queries the Paleobiology Database (https://paleobiodb.org) for fossil occurrence records.

## When to Use

- "Find Allosaurus fossils in the Morrison Formation"
- "How many Tyrannosaurus occurrences are recorded?"
- "What taxa are found in the Yixian Formation?"
- "Show me occurrences of Velociraptor"
- "What dinosaurs lived in the Late Jurassic?"

## When NOT to Use

- Searching literature → use `paleo-crossref`
- Geologic time scale questions → use `paleo-geo-time`
- "What did I research before?" → use `paleo-memory`

## Usage

```bash
# By genus + species
python3 scripts/pbdb_query.py --genus "Tyrannosaurus" --species "rex" --limit 10

# By higher taxon
python3 scripts/pbdb_query.py --base-name "Allosaurus" --limit 20

# Show parsed profile preferences (occurrence limit, open access)
python3 scripts/pbdb_query.py --respect-profile

# Filter by time interval
python3 scripts/pbdb_query.py --base-name "Ammonitida" --min-ma 66.0 --max-ma 145.0
```

## Output

JSON array of occurrence records with:
- `occurrence_id`, `taxon_name`, `taxon_rank`
- `early_interval`, `late_interval` (geological time)
- `max_ma`, `min_ma` (ages in millions of years)
- `coordinates` (lat/lon), `country`, `state`
- `formation`, `lithology`, `environment`
- `reference_no` (PBDB reference ID for citation)

## Data Source

Paleobiology Database (PBDB) — http://paleobiodb.org
- API: `https://paleobiodb.org/data1.2/occs/list.json`
- CC-BY 4.0 license
- 1.5M+ occurrences, 200K+ taxa

## Notes

- No authentication required
- Limit clamped to 1-200 records
- If a genus or species is provided, queries both
- `--base-name` overrides genus/species if provided
