#!/usr/bin/env python3
"""Search arXiv for paleontology / geosciences preprints.

API: http://export.arxiv.org/api/query (Atom XML)
Categories of interest:
  - q-bio.PE        Quantitative Biology — Populations and Evolution
  - q-bio.QM        Quantitative Biology — Quantitative Methods
  - physics.geo-ph  Geophysics
  - physics.bio-ph  Biological Physics

Note: arXiv has limited paleontology coverage. For most paleo work,
prefer CrossRef (`crossref_search.py`) or check bioRxiv / EarthArXiv directly.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json  # noqa: E402

ARXIV_API = "http://export.arxiv.org/api/query"
UA = "Paleontology-Research-Skills/1.0 (https://github.com/syxscott/Paleontology-Research-Skills; mailto:syxemail@yeah.net)"
TIMEOUT = 30

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def _request(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/atom+xml"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode("utf-8"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except (TimeoutError, OSError) as e:
        return None, f"Request failed: {e}"


def _txt(el, path):
    n = el.find(path, NS)
    return (n.text or "").strip() if n is not None and n.text else ""


def _parse_entry(entry):
    arxiv_id_url = _txt(entry, "atom:id")
    arxiv_id = arxiv_id_url.rsplit("/", 1)[-1] if arxiv_id_url else None
    authors = []
    for a in entry.findall("atom:author", NS):
        name = a.find("atom:name", NS)
        if name is not None and name.text:
            authors.append({"name": name.text.strip()})
    cats = []
    for c in entry.findall("atom:category", NS):
        t = c.get("term")
        if t:
            cats.append(t)
    pdf_url = None
    for link in entry.findall("atom:link", NS):
        if link.get("title") == "pdf" or link.get("type") == "application/pdf":
            pdf_url = link.get("href")
            break
    doi = _txt(entry, "arxiv:doi") or None
    journal_ref = _txt(entry, "arxiv:journal_ref") or None
    summary = _txt(entry, "atom:summary")
    summary = re.sub(r"\s+", " ", summary).strip()
    return {
        "arxiv_id": arxiv_id,
        "title": re.sub(r"\s+", " ", _txt(entry, "atom:title")).strip(),
        "authors": authors,
        "categories": cats,
        "primary_category": cats[0] if cats else None,
        "published": _txt(entry, "atom:published"),
        "updated": _txt(entry, "atom:updated"),
        "DOI": doi,
        "journal_reference": journal_ref,
        "pdf_url": pdf_url,
        "abstract_url": arxiv_id_url,
        "abstract": summary,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Search arXiv for paleontology / geosciences preprints")
    p.add_argument("--query", required=True)
    p.add_argument(
        "--category", default=None, help="Restrict to one arXiv category (e.g. q-bio.PE, physics.geo-ph)"
    )
    p.add_argument("--max-results", type=int, default=10)
    p.add_argument("--sort", choices=["relevance", "submittedDate", "lastUpdatedDate"], default="relevance")
    p.add_argument("--order", choices=["ascending", "descending"], default="descending")
    p.add_argument("--include-abstract", action="store_true")
    args = p.parse_args(argv)

    parts = [f"all:{args.query}"]
    if args.category:
        parts.append(f"cat:{args.category}")
    search = " AND ".join(parts)

    params = {
        "search_query": search,
        "start": 0,
        "max_results": max(1, min(args.max_results, 50)),
        "sortBy": args.sort,
        "sortOrder": args.order,
    }
    qs = urllib.parse.urlencode(params)
    url = f"{ARXIV_API}?{qs}"
    body, err = _request(url)
    if err:
        print_json({"error": err, "url": url, "items": []})
        return
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print_json({"error": f"XML parse error: {e}", "items": []})
        return

    entries = root.findall("atom:entry", NS)
    items = [_parse_entry(e) for e in entries]
    if not args.include_abstract:
        for it in items:
            it.pop("abstract", None)

    total = _txt(root, "{http://a9.com/-/spec/opensearch/1.1/}totalResults")
    print_json(
        {
            "source": "arXiv",
            "query": args.query,
            "category": args.category,
            "total_results": int(total) if total.isdigit() else None,
            "count": len(items),
            "items": items,
        }
    )


if __name__ == "__main__":
    main()
