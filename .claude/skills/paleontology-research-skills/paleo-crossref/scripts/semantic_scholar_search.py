#!/usr/bin/env python3
"""Search Semantic Scholar Graph API for papers (with citation counts).

API docs: https://api.semanticscholar.org/graph/v1
- No API key required for low-volume use
- Returns up to 100 results per request
- Provides citation counts, influential citations, references
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json, load_profile  # noqa: E402

S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_PAPER = "https://api.semanticscholar.org/graph/v1/paper"
UA = "Paleontology-Research-Skills/1.0 (mailto:noreply@example.org)"
TIMEOUT = 30

DEFAULT_FIELDS = (
    "paperId,title,abstract,year,authors,venue,externalIds,"
    "citationCount,influentialCitationCount,openAccessPdf,publicationDate,"
    "publicationTypes,journal,fieldsOfStudy"
)


def _request(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")[:200]
        except Exception:
            pass
        return None, f"HTTP {e.code}: {e.reason} {body}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except (TimeoutError, OSError, json.JSONDecodeError) as e:
        return None, f"Request failed: {e}"


def _author(a):
    return {"name": a.get("name"), "authorId": a.get("authorId")}


def _normalize(p):
    ext = p.get("externalIds") or {}
    return {
        "paperId": p.get("paperId"),
        "title": p.get("title"),
        "authors": [_author(a) for a in (p.get("authors") or [])],
        "year": p.get("year"),
        "venue": p.get("venue"),
        "journal_name": (p.get("journal") or {}).get("name"),
        "DOI": ext.get("DOI"),
        "arxiv_id": ext.get("ArXiv"),
        "pubmed_id": ext.get("PubMed"),
        "citationCount": p.get("citationCount"),
        "influentialCitationCount": p.get("influentialCitationCount"),
        "openAccessPdf": (p.get("openAccessPdf") or {}).get("url"),
        "publicationDate": p.get("publicationDate"),
        "publicationTypes": p.get("publicationTypes"),
        "fieldsOfStudy": p.get("fieldsOfStudy"),
        "abstract": p.get("abstract"),
        "URL": f"https://www.semanticscholar.org/paper/{p.get('paperId')}" if p.get("paperId") else None,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Search Semantic Scholar for papers")
    p.add_argument("--query", required=True)
    p.add_argument("--limit", type=int, default=10, help="1..100")
    p.add_argument("--min-citations", type=int, default=None,
                   help="Only return papers with >= N citations")
    p.add_argument("--year", help="Year or range: 2020 | 2018-2022 | 2020-")
    p.add_argument("--field", help="Restrict to fieldsOfStudy, e.g. 'Geology' or 'Biology'")
    p.add_argument("--include-abstract", action="store_true")
    p.add_argument("--respect-profile", action="store_true")
    args = p.parse_args(argv)

    if args.respect_profile:
        prof = load_profile()
        if not args.include_abstract and prof["user"]["dataPreferences"]["preferOpenAccess"]:
            args.include_abstract = True

    limit = max(1, min(args.limit, 100))
    params = {"query": args.query, "limit": limit, "fields": DEFAULT_FIELDS}
    if args.year:
        params["year"] = args.year
    if args.field:
        params["fieldsOfStudy"] = args.field

    qs = urllib.parse.urlencode(params)
    url = f"{S2_SEARCH}?{qs}"
    data, err = _request(url)
    if err:
        print_json({"error": err, "url": url, "items": []})
        return

    items = [_normalize(p) for p in (data.get("data") or [])]
    if args.min_citations is not None:
        items = [it for it in items if (it.get("citationCount") or 0) >= args.min_citations]
    if not args.include_abstract:
        for it in items:
            it.pop("abstract", None)

    print_json({
        "source": "Semantic Scholar",
        "query": args.query,
        "total_results": data.get("total"),
        "count": len(items),
        "items": items,
    })


if __name__ == "__main__":
    main()
