#!/usr/bin/env python3
"""Search CrossRef for paleontology literature metadata."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import load_profile, print_json  # noqa: E402

CR_URL = "https://api.crossref.org/works"
UA = "Paleontology-Research-Skills/1.0 (https://paleontology-research-skills.local; mailto:noreply@example.org)"
DEFAULT_TIMEOUT = 30

_JATS_RE = re.compile(r"</?(jats:)?[a-zA-Z][^>]*>")
_WS_RE = re.compile(r"\s+")


def strip_jats(text):
    if not text:
        return ""
    cleaned = _JATS_RE.sub(" ", text)
    return _WS_RE.sub(" ", cleaned).strip()


def _date(parts):
    if not parts:
        return None
    p = parts[0] if isinstance(parts, list) else parts
    return "-".join(str(x).zfill(2) for x in p)


def _author(a):
    return {"family": a.get("family", ""), "given": a.get("given", "")}


def _normalize(item, include_abstract):
    out = {
        "DOI": item.get("DOI"),
        "title": (item.get("title") or [""])[0],
        "subtitle": (item.get("subtitle") or [""])[0] or None,
        "authors": [_author(a) for a in (item.get("author") or [])],
        "container_title": (item.get("container-title") or [""])[0] or None,
        "publisher": item.get("publisher"),
        "published_date": _date(((item.get("issued") or {}).get("date-parts"))),
        "type": item.get("type"),
        "URL": item.get("URL"),
        "resource_link": ((item.get("resource") or {}).get("primary") or {}).get("URL"),
    }
    if include_abstract and item.get("abstract"):
        out["abstract"] = strip_jats(item["abstract"])
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Search CrossRef for paleontology literature")
    p.add_argument("--query", required=True)
    p.add_argument("--rows", type=int, default=10)
    p.add_argument("--include-abstract", action="store_true")
    p.add_argument("--respect-profile", action="store_true")
    p.add_argument("--filter-from-year", type=int, default=None,
                   help="Only include works published in or after this year")
    args = p.parse_args(argv)

    if args.respect_profile:
        prof = load_profile()
        if not args.include_abstract and prof["user"]["dataPreferences"]["preferOpenAccess"]:
            args.include_abstract = True

    rows = max(1, min(args.rows, 50))
    params = {
        "query": args.query,
        "rows": rows,
        "select": "DOI,title,subtitle,author,container-title,publisher,issued,type,URL,resource,abstract",
    }
    if args.filter_from_year:
        params["filter"] = f"from-pub-date:{args.filter_from_year}"

    qs = urllib.parse.urlencode(params)
    url = f"{CR_URL}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print_json({"error": f"HTTP {e.code}: {e.reason}", "url": url, "items": []})
        return
    except urllib.error.URLError as e:
        print_json({"error": f"Network error: {e.reason}", "url": url, "items": []})
        return
    except (TimeoutError, OSError) as e:
        print_json({"error": f"Request failed: {e}", "url": url, "items": []})
        return

    msg = data.get("message", {})
    items = [_normalize(it, args.include_abstract) for it in (msg.get("items") or [])]
    print_json({
        "source": "CrossRef",
        "query": args.query,
        "total_results": msg.get("total-results"),
        "count": len(items),
        "items": items,
    })


if __name__ == "__main__":
    main()
