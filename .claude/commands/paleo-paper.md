---
description: Search CrossRef for paleontology literature
argument-hint: <topic / keywords>
allowed-tools: Bash, Read
---

The user wants scholarly literature on a paleontology topic. Use the
**paleo-crossref** skill to search CrossRef for:

> $ARGUMENTS

Procedure:
1. Run the CrossRef search with the user's request as the query, including
   abstracts when available:
   ```bash
   python3 .claude/skills/paleontology-research-skills/paleo-crossref/scripts/crossref_search.py \
       --query "$ARGUMENTS" --rows 10 --include-abstract --respect-profile
   ```
2. For the top 3 most relevant results, optionally call
   `summarize_paper.py --doi <DOI>` to get a 3-bullet summary of the abstract.
3. Present each paper with: title, first author + et al, year, journal, DOI.
4. Apply the user's preferred citation format (see `paleo-profile`); default APA.
5. **Never invent a DOI, title, or author** that does not appear in the JSON
   returned by the script.
