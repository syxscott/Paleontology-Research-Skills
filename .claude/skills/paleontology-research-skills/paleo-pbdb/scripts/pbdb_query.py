#!/usr/bin/env python3
"""Query the Paleobiology Database (PBDB) for fossil occurrence records.

When --respect-profile is supplied the default occurrence limit is read from
the parsed user profile (`~/.paleontology-research-skills/user.md`).

Output: JSON object on stdout with a ``records`` array of trimmed PBDB entries.
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

from paleo_common import load_profile, normalize_taxon, print_json  # noqa: E402

PBDB_URL = "https://paleobiodb.org/data1.2/occs/list.json"
TIMEOUT = 30
UA = "Paleontology-Research-Skills/1.0 (https://github.com/syxscott/Paleontology-Research-Skills; mailto:syxemail@yeah.net)"


def _request(params):
    qs = urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    url = f"{PBDB_URL}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "url": url, "records": []}
    except urllib.error.URLError as e:
        return {"error": f"Network error: {e.reason}", "url": url, "records": []}
    except (TimeoutError, OSError) as e:
        return {"error": f"Request failed: {e}", "url": url, "records": []}
    return data


def _normalize(rec):
    """Trim PBDB record fields to the subset surfaced to the model."""
    coords = None
    if rec.get("lat") is not None:
        coords = {"lat": rec.get("lat"), "lng": rec.get("lng")}
    return {
        "occurrence_id": rec.get("oid"),
        "taxon_name": rec.get("tna") or rec.get("idn"),
        "taxon_rank": rec.get("rnk"),
        "early_interval": rec.get("oei"),
        "late_interval": rec.get("oli"),
        "max_ma": rec.get("eag"),
        "min_ma": rec.get("lag"),
        "coordinates": coords,
        "country": rec.get("cc2"),
        "state": rec.get("stp"),
        "formation": rec.get("sfm"),
        "lithology": rec.get("ggc"),
        "environment": rec.get("env"),
        "reference_no": rec.get("rid"),
    }


def main(argv=None):
    p = argparse.ArgumentParser(description="Query PBDB for fossil occurrences")
    p.add_argument("--genus")
    p.add_argument("--species")
    p.add_argument("--base-name", dest="base_name",
                   help="Higher taxon (overrides genus/species), e.g. Allosaurus")
    p.add_argument("--interval", help="Geological interval, e.g. Late Jurassic")
    p.add_argument("--min-ma", type=float, dest="min_ma")
    p.add_argument("--max-ma", type=float, dest="max_ma")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--respect-profile", action="store_true",
                   help="Apply user profile defaults (occurrence limit, etc.)")
    p.add_argument("--prompt", help="Natural-language prompt; taxon will be extracted")
    args = p.parse_args(argv)

    if args.respect_profile:
        prof = load_profile()
        if not args.limit or args.limit == 20:
            args.limit = prof["user"]["dataPreferences"]["defaultOccurrenceLimit"]

    if args.prompt and not (args.base_name or args.genus):
        candidate = normalize_taxon(args.prompt)
        if candidate:
            args.base_name = candidate

    if not any([args.base_name, args.genus, args.species, args.interval]):
        print_json({"error": "Provide at least one of --base-name / --genus / --species / --interval",
                    "records": []})
        return

    limit = max(1, min(int(args.limit or 20), 200))

    params = {"show": "coords,strat,env,ref,class,attr", "limit": limit}
    if args.base_name:
        params["base_name"] = args.base_name
    else:
        if args.genus:
            params["taxon_name"] = (args.genus + " " + (args.species or "")).strip()
    if args.interval:
        params["interval"] = args.interval
    if args.min_ma is not None:
        params["min_ma"] = args.min_ma
    if args.max_ma is not None:
        params["max_ma"] = args.max_ma

    data = _request(params)
    if "error" in data:
        print_json({"error": data["error"], "url": data.get("url"), "records": []})
        return

    records = [_normalize(r) for r in (data.get("records") or [])]
    print_json({
        "source": "PBDB",
        "query": params,
        "count": len(records),
        "records": records,
    })


if __name__ == "__main__":
    main()
