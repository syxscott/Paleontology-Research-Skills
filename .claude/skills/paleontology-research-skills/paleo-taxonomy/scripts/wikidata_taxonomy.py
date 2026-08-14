#!/usr/bin/env python3
"""Cross-reference a taxon with Wikidata via SPARQL (vernacular names, image, common labels)."""

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

from paleo_common import print_json  # noqa: E402

WD_SPARQL = "https://query.wikidata.org/sparql"
UA = "Paleontology-Research-Skills/1.0 (https://github.com/syxscott/Paleontology-Research-Skills; mailto:syxemail@yeah.net)"
TIMEOUT = 30


def run_sparql(query):
    qs = urllib.parse.urlencode({"query": query, "format": "json"})
    url = f"{WD_SPARQL}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/sparql-results+json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except (TimeoutError, OSError, json.JSONDecodeError) as e:
        return None, f"Request failed: {e}"


def search(name):
    # SPARQL: find Wikidata items whose taxon name matches
    # Escape backslash, double quote, and newlines for the SPARQL string literal.
    safe = (name or "").replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
    query = (
        "SELECT ?item ?itemLabel ?taxonName ?parentLabel ?rank ?rankLabel ?image ?cnLabel ?enLabel WHERE {\n"
        '  ?item wdt:P225 "' + safe + '" .\n'
        "  OPTIONAL { ?item wdt:P171 ?parent . }\n"
        "  OPTIONAL { ?item wdt:P105 ?rank . }\n"
        "  OPTIONAL { ?item wdt:P18 ?image . }\n"
        '  OPTIONAL { ?item rdfs:label ?cn FILTER(LANG(?cn) = "zh") . BIND(?cn AS ?cnLabel) }\n'
        '  OPTIONAL { ?item rdfs:label ?en FILTER(LANG(?en) = "en") . BIND(?en AS ?enLabel) }\n'
        '  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,zh" . }\n'
        "  BIND(?itemLabel AS ?taxonName)\n"
        "}\n"
        "LIMIT 5"
    )
    return run_sparql(query)


def main(argv=None):
    p = argparse.ArgumentParser(description="Look up a taxon on Wikidata via SPARQL")
    p.add_argument("--name", required=True)
    args = p.parse_args(argv)

    data, err = search(args.name)
    if err:
        print_json({"error": err, "name": args.name, "matches": []})
        return

    bindings = ((data or {}).get("results") or {}).get("bindings") or []
    matches = []
    for b in bindings:

        def _v(k, binding=b):
            x = binding.get(k)
            return x.get("value") if x else None

        matches.append(
            {
                "wikidata_id": (_v("item") or "").rsplit("/", 1)[-1],
                "label": _v("itemLabel"),
                "taxon_name": _v("taxonName"),
                "rank": _v("rankLabel"),
                "parent": _v("parentLabel"),
                "image": _v("image"),
                "chinese_label": _v("cnLabel"),
                "english_label": _v("enLabel"),
            }
        )

    print_json(
        {
            "source": "Wikidata",
            "query": {"name": args.name},
            "count": len(matches),
            "matches": matches,
        }
    )


if __name__ == "__main__":
    main()
