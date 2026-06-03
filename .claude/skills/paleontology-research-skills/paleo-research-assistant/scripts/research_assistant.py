#!/usr/bin/env python3
"""Orchestrator: run the full paleontology research pipeline and emit a Markdown report.

Calls (in order):
  1. paleo-crossref/scripts/crossref_search.py
  2. paleo-crossref/scripts/summarize_paper.py  (for top N abstracts)
  3. paleo-taxonomy/scripts/taxonomy_query.py
  4. paleo-pbdb/scripts/pbdb_query.py
  5. paleo-stratigraphy/scripts/stratigraphy_query.py
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json  # noqa: E402

PARENT = Path(_HERE).parent.parent  # paleontology-research-skills/


def _slugify(s):
    s = re.sub(r"[^A-Za-z0-9_\- ]+", "", s)
    return re.sub(r"\s+", "-", s.strip()).lower() or "report"


def _run(script_rel, args, timeout=60):
    """Run a sibling script and return its parsed JSON output (or {error: ...})."""
    script = PARENT / script_rel
    if not script.exists():
        return {"error": f"Script not found: {script}"}
    cmd = [sys.executable, str(script)] + list(args)
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=timeout, env=env,
        )
    except subprocess.TimeoutExpired:
        return {"error": f"Sub-script timed out: {script.name}", "command": cmd}
    except (OSError, subprocess.SubprocessError) as e:
        return {"error": str(e), "command": cmd}
    if r.returncode != 0:
        return {"error": f"Sub-script failed (code {r.returncode})",
                "stderr": (r.stderr or "")[:300]}
    try:
        return json.loads(r.stdout) if r.stdout else {"error": "empty output"}
    except json.JSONDecodeError:
        return {"error": "Non-JSON output", "raw": (r.stdout or "")[:300]}


def _format_authors(authors, max_show=3):
    if not authors:
        return "(no authors)"
    names = []
    for a in authors[:max_show]:
        if "family" in a or "given" in a:
            given = a.get("given") or ""
            family = a.get("family") or ""
            names.append(f"{family}, {given[0]}." if given and family else (family or given))
        elif "name" in a:
            names.append(a["name"])
    suffix = " et al." if len(authors) > max_show else ""
    return ", ".join(names) + suffix


def _render_report(state):
    """Render the synthesis Markdown."""
    topic = state["topic"]
    taxon = state.get("taxon")
    formation = state.get("formation")
    now = dt.datetime.now(tz=dt.timezone.utc).isoformat(timespec="seconds")

    md = []
    md.append(f"# Research Report — {topic}\n")
    md.append(f"**Generated**: {now}  ")
    md.append(f"**By**: `paleo-research-assistant` (paleontology-research-skills v1.0)\n")
    if taxon: md.append(f"**Target taxon**: *{taxon}*  ")
    if formation: md.append(f"**Target formation**: {formation}\n")
    md.append("\n---\n")

    # 1. Overview
    md.append("## 1. Overview\n")
    md.append(f"_This report compiles primary-source data on **{topic}** from the "
              "Paleobiology Database (PBDB), CrossRef, and (optionally) "
              "Macrostrat, Semantic Scholar, and arXiv. All findings below are "
              "machine-extracted and should be reviewed before scientific use._\n")

    # 2. Literature
    md.append("\n## 2. Literature (CrossRef)\n")
    lit = state.get("literature") or {}
    items = lit.get("items") or []
    if not items:
        md.append(f"_No papers returned (error: {lit.get('error', 'n/a')})._\n")
    else:
        md.append(f"Top {len(items)} papers (of {lit.get('total_results', '?')} total matches):\n")
        for i, it in enumerate(items, 1):
            md.append(f"{i}. **{it.get('title', '?')}**  ")
            md.append(f"   {_format_authors(it.get('authors'))} ({it.get('published_date') or 'n.d.'})  ")
            md.append(f"   *{it.get('container_title') or 'unknown journal'}*  ")
            doi = it.get("DOI")
            if doi:
                md.append(f"   DOI: [{doi}](https://doi.org/{doi})  ")
            # bullet summary
            summary = (state.get("summaries") or {}).get(doi or it.get("title"))
            if summary and summary.get("bullets"):
                md.append("   _Summary (heuristic):_")
                for b in summary["bullets"]:
                    md.append(f"   - {b}")
            md.append("")

    # 3. Taxonomy
    md.append("\n## 3. Taxonomy\n")
    tax = state.get("taxonomy")
    if not taxon:
        md.append("_No taxon specified (skipped)._\n")
    elif not tax or "error" in tax:
        md.append(f"_Lookup failed: {tax.get('error') if tax else 'no data'}_\n")
    else:
        t = tax.get("taxon") or {}
        md.append(f"**Taxon**: *{t.get('name')}* ({t.get('rank') or '?'}) — {t.get('authority') or 'no authority'}  ")
        md.append(f"**Status**: {t.get('status') or '?'}  ")
        tr = t.get("time_range_ma") or {}
        if tr.get("max") or tr.get("min"):
            md.append(f"**Time range**: {tr.get('max')} – {tr.get('min')} Ma  ")
        md.append("\n**Hierarchy**:")
        for h in tax.get("hierarchy") or []:
            md.append(f"- `{h['rank']:>8s}`: {h['name']}")

    # 4. PBDB occurrences
    md.append("\n## 4. Fossil Occurrences (PBDB)\n")
    occs = state.get("occurrences")
    if not taxon:
        md.append("_No taxon specified (skipped)._\n")
    elif not occs or "error" in occs:
        md.append(f"_Query failed: {occs.get('error') if occs else 'no data'}_\n")
    else:
        recs = occs.get("records") or []
        md.append(f"**Total occurrences returned**: {len(recs)}  ")
        # Aggregate
        if recs:
            from collections import Counter
            ints = Counter(r.get("early_interval") for r in recs if r.get("early_interval"))
            fms = Counter(r.get("formation") for r in recs if r.get("formation"))
            cs = Counter(r.get("country") for r in recs if r.get("country"))
            md.append(f"**Top intervals**: {', '.join(f'{k} ({v})' for k, v in ints.most_common(5))}  ")
            md.append(f"**Top formations**: {', '.join(f'{k} ({v})' for k, v in fms.most_common(5))}  ")
            md.append(f"**Countries**: {', '.join(f'{k} ({v})' for k, v in cs.most_common(5))}  ")

    # 5. Stratigraphy
    md.append("\n## 5. Stratigraphic Context\n")
    strat = state.get("stratigraphy")
    if not formation:
        md.append("_No formation specified (skipped)._\n")
    elif not strat or "error" in strat:
        md.append(f"_Query failed: {strat.get('error') if strat else 'no data'}_\n")
    else:
        s = strat.get("summary") or {}
        ar = s.get("age_range_ma") or {}
        md.append(f"**Formation**: {formation}  ")
        md.append(f"**Collection count**: {s.get('collection_count')}  ")
        md.append(f"**Age range**: {ar.get('max')} – {ar.get('min')} Ma  ")
        md.append(f"**Intervals**: {', '.join(s.get('intervals') or [])}  ")
        cs2 = s.get("countries") or []
        if cs2:
            md.append(f"**Countries**: {', '.join(c.get('code', '?') for c in cs2[:5])}  ")
        dt2 = s.get("dominant_taxa") or []
        if dt2:
            md.append("\n**Dominant taxa**:")
            for r in dt2[:10]:
                md.append(f"- *{r['name']}* — {r['occurrences']} occurrences")

    # 6. References
    md.append("\n## 6. References (with DOIs)\n")
    if items:
        for it in items:
            doi = it.get("DOI")
            md.append(f"- {_format_authors(it.get('authors'))} ({it.get('published_date') or 'n.d.'}). "
                      f"*{it.get('title', '?')}*. {it.get('container_title') or 'unknown'}. "
                      f"{'https://doi.org/' + doi if doi else (it.get('URL') or '')}")
    else:
        md.append("_None._")

    # 7. Limitations
    md.append("\n## 7. Limitations & Data Gaps\n")
    md.append("- CrossRef does not index every paleontology journal. For Chinese-language journals, additional searches in CNKI / Wanfang are recommended.")
    md.append("- PBDB coverage is biased toward North American and European fossils; non-Western collections may be under-represented.")
    md.append("- Automated abstract summaries are heuristic — verify against the original paper before quoting.")
    md.append("- Taxonomic status may have changed since the last PBDB synchronisation.")

    md.append("\n---\n")
    md.append("_Generated by `paleo-research-assistant` from the `paleontology-research-skills` toolkit._\n")
    return "\n".join(md)


def main(argv=None):
    p = argparse.ArgumentParser(description="Run the full paleo research pipeline")
    p.add_argument("--topic", required=True, help="Research topic (used for CrossRef query)")
    p.add_argument("--taxon", help="Optional taxon (for taxonomy + PBDB stages)")
    p.add_argument("--formation", help="Optional formation (for stratigraphy stage)")
    p.add_argument("--paper-rows", type=int, default=8)
    p.add_argument("--summarise-top", type=int, default=3,
                   help="Generate heuristic 3-bullet summaries for the top-N papers")
    p.add_argument("--out-dir", default="paleo_reports")
    p.add_argument("--skip-literature", action="store_true")
    p.add_argument("--skip-taxonomy", action="store_true")
    p.add_argument("--skip-pbdb", action="store_true")
    p.add_argument("--skip-stratigraphy", action="store_true")
    args = p.parse_args(argv)

    state = {
        "topic": args.topic,
        "taxon": args.taxon,
        "formation": args.formation,
        "stages": [],
        "started_at": dt.datetime.now(tz=dt.timezone.utc).isoformat(timespec="seconds"),
    }

    # Stage 1: CrossRef
    if not args.skip_literature:
        state["stages"].append("literature")
        state["literature"] = _run(
            "paleo-crossref/scripts/crossref_search.py",
            ["--query", args.topic, "--rows", str(args.paper_rows), "--include-abstract"],
            timeout=45,
        )
    # Stage 1b: Summarise top-N abstracts
    state["summaries"] = {}
    items = (state.get("literature") or {}).get("items") or []
    if items and args.summarise_top > 0:
        state["stages"].append("summaries")
        for it in items[: max(1, args.summarise_top)]:
            abstract = it.get("abstract") or ""
            if not abstract:
                continue
            doi_or_title = it.get("DOI") or it.get("title")
            s = _run(
                "paleo-crossref/scripts/summarize_paper.py",
                ["--abstract", abstract, "--bullets", "3"],
                timeout=15,
            )
            state["summaries"][doi_or_title] = s

    # Stage 2: Taxonomy
    if args.taxon and not args.skip_taxonomy:
        state["stages"].append("taxonomy")
        state["taxonomy"] = _run(
            "paleo-taxonomy/scripts/taxonomy_query.py",
            ["--name", args.taxon],
            timeout=30,
        )

    # Stage 3: PBDB occurrences
    if args.taxon and not args.skip_pbdb:
        state["stages"].append("pbdb")
        state["occurrences"] = _run(
            "paleo-pbdb/scripts/pbdb_query.py",
            ["--base-name", args.taxon, "--limit", "100"],
            timeout=45,
        )

    # Stage 4: Stratigraphy
    if args.formation and not args.skip_stratigraphy:
        state["stages"].append("stratigraphy")
        state["stratigraphy"] = _run(
            "paleo-stratigraphy/scripts/stratigraphy_query.py",
            ["--formation", args.formation, "--taxa-limit", "20"],
            timeout=45,
        )

    state["completed_at"] = dt.datetime.now(tz=dt.timezone.utc).isoformat(timespec="seconds")

    # Render report
    md = _render_report(state)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = _slugify(args.topic)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    md_path = out_dir / f"{slug}-{stamp}.md"
    json_path = out_dir / f"{slug}-{stamp}.json"
    md_path.write_text(md, encoding="utf-8")
    json_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

    print_json({
        "topic": args.topic,
        "taxon": args.taxon,
        "formation": args.formation,
        "stages_run": state["stages"],
        "report_md": str(md_path),
        "report_json": str(json_path),
        "report_size_bytes": md_path.stat().st_size,
        "started_at": state["started_at"],
        "completed_at": state["completed_at"],
    })


if __name__ == "__main__":
    main()
