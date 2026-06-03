---
name: paleo-taxonomy
description: 🔬 Lookup the full taxonomic hierarchy (kingdom, phylum, class, order, family, genus, species) for a paleontological taxon. Uses PBDB as primary source. Use when the user asks "what is the classification of X", "what family does Y belong to", "is Z a valid taxon", or "list species in family/order N". Returns a structured hierarchy plus authority and time range.
---

# Taxonomic Classification Lookup

Queries the Paleobiology Database (PBDB) for the full taxonomic hierarchy of a fossil taxon, returning all parent ranks plus authority and stratigraphic range.

## When to Use

- "What is the classification of *Tyrannosaurus rex*?"
- "What family does *Allosaurus* belong to?"
- "Is *Brontosaurus* a valid taxon?"
- "List species in Tyrannosauridae"
- "What's the parent genus of *T. rex*?"

## When NOT to Use

- Modern organism taxonomy → use NCBI/GBIF (out of scope)
- Genetic / molecular phylogeny → use `paleo-crossref` to find phylogenetic papers
- Fossil **occurrences** → use `paleo-pbdb`

## Usage

```bash
# Full hierarchy for a single taxon
python3 scripts/taxonomy_query.py --name "Tyrannosaurus rex"

# Children of a parent taxon (e.g. all genera in a family)
python3 scripts/taxonomy_query.py --children "Tyrannosauridae" --rank genus

# Just check validity
python3 scripts/taxonomy_query.py --name "Brontosaurus" --validity-only

# Cross-reference with NCBI Taxonomy (modern relatives, when applicable)
python3 scripts/ncbi_taxonomy.py --name "Aves"

# Cross-reference with Wikidata (for vernacular names, images, etc.)
python3 scripts/wikidata_taxonomy.py --name "Allosaurus"
```

## Output Format

```json
{
  "source": "PBDB",
  "query": {"name": "Tyrannosaurus rex"},
  "taxon": {
    "name": "Tyrannosaurus rex",
    "rank": "species",
    "status": "valid",
    "authority": "Osborn 1905",
    "extinct": true,
    "time_range_ma": {"max": 72.1, "min": 66.0},
    "first_appearance": "Maastrichtian",
    "last_appearance": "Maastrichtian"
  },
  "hierarchy": [
    {"rank": "kingdom",  "name": "Animalia"},
    {"rank": "phylum",   "name": "Chordata"},
    {"rank": "class",    "name": "Reptilia"},
    {"rank": "order",    "name": "Saurischia"},
    {"rank": "family",   "name": "Tyrannosauridae"},
    {"rank": "genus",    "name": "Tyrannosaurus"},
    {"rank": "species",  "name": "Tyrannosaurus rex"}
  ]
}
```

## Data Sources

- **Primary**: PBDB Taxonomy API (`https://paleobiodb.org/data1.2/taxa/single.json`)
- **Auxiliary**: NCBI Taxonomy (`api.ncbi.nlm.nih.gov`) — modern relatives only
- **Cross-reference**: Wikidata SPARQL endpoint — vernacular names, images

## Notes

- A name reported as `status: "synonym"` or `"replaced"` is flagged in the JSON, and the accepted name is provided in `accepted_name`.
- Authority strings follow standard zoological / botanical convention (e.g. `Osborn 1905`, `(Linnaeus 1758)` with parentheses if combination changed).
- For higher taxa, the hierarchy stops at whatever rank the database resolves.
