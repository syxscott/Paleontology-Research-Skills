#!/usr/bin/env python3
"""Query the Paleobiology Database for a taxon's full classification hierarchy."""

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

PBDB_SINGLE = "https://paleobiodb.org/data1.2/taxa/single.json"
PBDB_LIST = "https://paleobiodb.org/data1.2/taxa/list.json"
TIMEOUT = 30
UA = "Paleontology-Research-Skills/1.0 (https://github.com/syxscott/Paleontology-Research-Skills; mailto:syxemail@yeah.net)"

# Standard rank hierarchy from high to low
RANK_ORDER = [
    "kingdom",
    "phylum",
    "subphylum",
    "class",
    "subclass",
    "infraclass",
    "superorder",
    "order",
    "suborder",
    "infraorder",
    "superfamily",
    "family",
    "subfamily",
    "tribe",
    "genus",
    "subgenus",
    "species",
    "subspecies",
]


def _request(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except (TimeoutError, OSError) as e:
        return None, f"Request failed: {e}"


def _hierarchy_from_record(rec):
    """Extract the parent-rank chain from a PBDB taxon record with show=class,phylo."""
    pairs = [
        ("kingdom", "kgl"),
        ("phylum", "phl"),
        ("class", "cll"),
        ("order", "odl"),
        ("family", "fml"),
        ("genus", "gnl"),
    ]
    out = []
    for rank, key in pairs:
        v = rec.get(key)
        if v:
            out.append({"rank": rank, "name": v})
    own_rank = (rec.get("rnk_str") or rec.get("rnk") or "").lower() if isinstance(rec.get("rnk"), str) else ""
    own_name = rec.get("nam") or rec.get("tna") or ""
    if own_name and (not out or out[-1]["name"] != own_name):
        if own_rank and own_rank in RANK_ORDER:
            out.append({"rank": own_rank, "name": own_name})
        else:
            out.append({"rank": "(unknown)", "name": own_name})
    return out


def _query_single(name):
    params = {"name": name, "show": "attr,app,class,phylo,size,parent"}
    qs = urllib.parse.urlencode(params)
    data, err = _request(f"{PBDB_SINGLE}?{qs}")
    if err:
        # PBDB returns HTTP 400 when the name is malformed OR when there
        # is simply no such taxon in their database. Map both to a
        # friendly "not found" message rather than a raw HTTP status.
        if "HTTP 400" in err or "HTTP 404" in err:
            return None, f"No taxon found matching '{name}' (PBDB has no record)"
        return None, err
    if not isinstance(data, dict):
        return None, "PBDB returned non-dict"
    records = data.get("records") or []
    if not records:
        return None, f"No taxon found matching '{name}'"
    rec = records[0]
    rank_map = {
        2: "subspecies",
        3: "species",
        4: "subgenus",
        5: "genus",
        6: "subtribe",
        7: "tribe",
        8: "subfamily",
        9: "family",
        10: "superfamily",
        11: "infraorder",
        12: "suborder",
        13: "order",
        14: "superorder",
        15: "infraclass",
        16: "subclass",
        17: "class",
        18: "superclass",
        19: "subphylum",
        20: "phylum",
        21: "superphylum",
        22: "subkingdom",
        23: "kingdom",
        24: "unranked",
    }
    rank_raw = rec.get("rnk")
    rank_str = rank_map.get(rank_raw, "") if isinstance(rank_raw, int) else (rank_raw or "")
    accepted = rec.get("acn") or rec.get("nam")
    status = "valid" if rec.get("nam") == accepted else "synonym"
    taxon_info = {
        "name": rec.get("nam"),
        "accepted_name": accepted,
        "rank": rank_str,
        "status": status,
        "authority": (rec.get("att") or "").strip() or None,
        "extinct": rec.get("ext") == 1 or rec.get("ext") is True,
        "time_range_ma": {
            "max": rec.get("fea"),
            "min": rec.get("lla"),
        },
        "first_appearance": rec.get("tei"),
        "last_appearance": rec.get("tli"),
        "pbdb_taxon_id": rec.get("oid"),
        "n_occurrences": rec.get("noc"),
    }
    rec["nam"] = rec.get("nam")
    rec["rnk_str"] = rank_str
    return {"taxon": taxon_info, "raw": rec}, None


def _query_children(parent_name, rank_filter):
    params = {"base_name": parent_name, "rel": "all_children", "limit": 500, "show": "attr"}
    if rank_filter:
        params["rank"] = rank_filter
    qs = urllib.parse.urlencode(params)
    data, err = _request(f"{PBDB_LIST}?{qs}")
    if err:
        return None, err
    if not isinstance(data, dict):
        return None, "PBDB returned non-dict"
    rank_map = {
        3: "species",
        5: "genus",
        9: "family",
        13: "order",
        17: "class",
        20: "phylum",
        23: "kingdom",
    }
    children = []
    for r in data.get("records") or []:
        rk_raw = r.get("rnk")
        rk = rank_map.get(rk_raw, "") if isinstance(rk_raw, int) else (rk_raw or "")
        children.append(
            {
                "name": r.get("nam"),
                "rank": rk,
                "authority": (r.get("att") or "").strip() or None,
                "taxon_id": r.get("oid"),
            }
        )
    return children, None


def main(argv=None):
    p = argparse.ArgumentParser(description="Query PBDB for taxonomic classification")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--name", help="Taxon name (any rank)")
    grp.add_argument("--children", dest="children", help="Parent taxon — return all descendants")
    p.add_argument(
        "--rank",
        help="When using --children, filter to this rank only (species/genus/family/order/class/etc.)",
    )
    p.add_argument("--validity-only", action="store_true", help="Only report whether the name is valid")
    args = p.parse_args(argv)

    if args.children:
        children, err = _query_children(args.children, args.rank)
        if err:
            print_json({"error": err, "parent": args.children, "children": []})
            return
        print_json(
            {
                "source": "PBDB",
                "query": {"parent": args.children, "rank_filter": args.rank},
                "count": len(children),
                "children": children,
            }
        )
        return

    result, err = _query_single(args.name)
    if err:
        print_json({"error": err, "query": {"name": args.name}})
        return

    taxon = result["taxon"]
    raw = result["raw"]

    if args.validity_only:
        print_json(
            {
                "source": "PBDB",
                "query": {"name": args.name},
                "is_valid": taxon["status"] == "valid",
                "status": taxon["status"],
                "accepted_name": taxon["accepted_name"],
            }
        )
        return

    hierarchy = _hierarchy_from_record(raw)
    print_json(
        {
            "source": "PBDB",
            "query": {"name": args.name},
            "taxon": taxon,
            "hierarchy": hierarchy,
        }
    )


if __name__ == "__main__":
    main()
