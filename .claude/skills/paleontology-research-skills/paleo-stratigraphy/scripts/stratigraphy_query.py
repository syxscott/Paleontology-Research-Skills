#!/usr/bin/env python3
"""Query PBDB for fossil-bearing formations/strata."""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import print_json  # noqa: E402

PBDB_COLLS = "https://paleobiodb.org/data1.2/colls/list.json"
PBDB_OCCS = "https://paleobiodb.org/data1.2/occs/list.json"
UA = "Paleontology-Research-Skills/1.0 (mailto:noreply@example.org)"
TIMEOUT = 30


def _request(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except (TimeoutError, OSError, json.JSONDecodeError) as e:
        return None, f"Request failed: {e}"


def query_collections(formation, country=None, interval=None, limit=500):
    params = {"show": "loc,strat,time,refattr", "limit": limit}
    if formation:
        params["formation"] = formation
    if interval:
        params["interval"] = interval
    if country:
        params["cc"] = country
    qs = urllib.parse.urlencode(params)
    return _request(f"{PBDB_COLLS}?{qs}")


def query_top_taxa(formation, taxa_limit=20):
    params = {"formation": formation, "show": "class", "limit": 500}
    qs = urllib.parse.urlencode(params)
    data, err = _request(f"{PBDB_OCCS}?{qs}")
    if err:
        return [], err
    counter = Counter()
    for r in (data.get("records") or []):
        name = r.get("tna") or r.get("idn")
        if name:
            counter[name] += 1
    return [{"name": n, "occurrences": c} for n, c in counter.most_common(taxa_limit)], None


def _summarise(records):
    """Aggregate collection records into a summary.

    Always returns the same JSON shape, even when records is empty —
    this keeps downstream tooling (e.g. paleo-research-assistant) simple.
    """
    if not records:
        return {
            "collection_count": 0,
            "age_range_ma": {"max": None, "min": None},
            "intervals": [],
            "countries": [],
            "states": [],
            "formations_in_query": [],
            "lithologies": [],
        }
    max_ma, min_ma = -1.0, 1e18
    intervals = set()
    countries = Counter()
    states = Counter()
    formations = Counter()
    lithos = Counter()
    for r in records:
        eag = r.get("eag")
        lag = r.get("lag")
        if isinstance(eag, (int, float)):
            max_ma = max(max_ma, float(eag))
        if isinstance(lag, (int, float)):
            min_ma = min(min_ma, float(lag))
        for k in ("oei", "oli"):
            v = r.get(k)
            if v:
                intervals.add(v)
        cc = r.get("cc2")
        if cc:
            countries[cc] += 1
        st = r.get("stp")
        if st:
            states[st] += 1
        f = r.get("sfm")
        if f:
            formations[f] += 1
        lt = r.get("lt1") or r.get("lt2")
        if lt:
            lithos[lt] += 1
    return {
        "collection_count": len(records),
        "age_range_ma": {
            "max": (round(max_ma, 3) if max_ma >= 0 else None),
            "min": (round(min_ma, 3) if min_ma < 1e18 else None),
        },
        "intervals": sorted(intervals),
        "countries": [{"code": c, "count": n} for c, n in countries.most_common()],
        "states": [{"name": s, "count": n} for s, n in states.most_common(10)],
        "formations_in_query": [{"name": f, "count": n} for f, n in formations.most_common(20)],
        "lithologies": [{"name": l, "count": n} for l, n in lithos.most_common(10)],
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Query PBDB for strata/formations")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--formation")
    grp.add_argument("--interval", help="Geological interval, e.g. 'Late Cretaceous'")
    p.add_argument("--country", help="ISO 2-letter country code (e.g. CN, US, MN)")
    p.add_argument("--limit", type=int, default=500)
    p.add_argument("--taxa-limit", type=int, default=20,
                   help="When --formation is set, also fetch the top-N taxa")
    p.add_argument("--collections-detail", action="store_true",
                   help="Include the raw collections array in output (large!)")
    args = p.parse_args(argv)

    data, err = query_collections(args.formation, args.country, args.interval,
                                  max(1, min(args.limit, 5000)))
    if err:
        print_json({"error": err, "query": {"formation": args.formation,
                                            "interval": args.interval,
                                            "country": args.country}})
        return

    records = data.get("records") or []
    summary = _summarise(records)

    out = {
        "source": "PBDB",
        "query": {"formation": args.formation,
                  "interval": args.interval,
                  "country": args.country,
                  "limit": args.limit},
        "summary": summary,
    }

    if args.formation:
        taxa, terr = query_top_taxa(args.formation, args.taxa_limit)
        if terr:
            out["dominant_taxa_error"] = terr
        else:
            out["summary"]["dominant_taxa"] = taxa

    if args.collections_detail:
        out["collections"] = records

    print_json(out)


if __name__ == "__main__":
    main()
