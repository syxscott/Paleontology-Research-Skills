---
description: Lookup full taxonomic classification (kingdom→species)
argument-hint: <taxon-name>
allowed-tools: Bash, Read
---

The user wants the full taxonomic hierarchy for a taxon. Use the
**paleo-taxonomy** skill:

> $ARGUMENTS

Procedure:

1. Run PBDB hierarchy lookup:
   ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-taxonomy/scripts/taxonomy_query.py \
       --name "$ARGUMENTS"
   ```
2. If the taxon has modern relatives (e.g. Aves, Mammalia), optionally also run:
   ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-taxonomy/scripts/ncbi_taxonomy.py \
       --name "$ARGUMENTS"
   ```
3. For vernacular names / Chinese label, optionally run:
   ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-taxonomy/scripts/wikidata_taxonomy.py \
       --name "$ARGUMENTS"
   ```
4. Present hierarchy as a `kingdom → phylum → ... → species` tree.
   Always cite **PBDB** as the primary source.
