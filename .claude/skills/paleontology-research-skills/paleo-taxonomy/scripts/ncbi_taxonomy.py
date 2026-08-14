#!/usr/bin/env python3
"""Cross-reference a taxon name with NCBI Taxonomy (for modern relatives)."""

from __future__ import annotations

import argparse
import json
import os
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

NCBI_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
NCBI_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
NCBI_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
UA = "Paleontology-Research-Skills/1.0 (https://github.com/syxscott/Paleontology-Research-Skills; mailto:syxemail@yeah.net)"
TIMEOUT = 30


def _request(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.read().decode("utf-8"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.reason}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except (TimeoutError, OSError) as e:
        return None, f"Request failed: {e}"


def search_taxon(name):
    qs = urllib.parse.urlencode({"db": "taxonomy", "term": name, "retmode": "json"})
    body, err = _request(f"{NCBI_ESEARCH}?{qs}")
    if err:
        return None, err
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None, "Invalid JSON from NCBI esearch"
    ids = (data.get("esearchresult") or {}).get("idlist") or []
    return ids, None


def fetch_lineage(tax_id):
    qs = urllib.parse.urlencode({"db": "taxonomy", "id": tax_id, "retmode": "xml"})
    body, err = _request(f"{NCBI_EFETCH}?{qs}")
    if err:
        return None, err
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        return None, f"XML parse error: {e}"
    taxon = root.find("Taxon")
    if taxon is None:
        return None, "No taxon in NCBI response"
    out = {
        "tax_id": tax_id,
        "scientific_name": (taxon.findtext("ScientificName") or "").strip(),
        "rank": (taxon.findtext("Rank") or "").strip(),
        "division": (taxon.findtext("Division") or "").strip(),
        "lineage": (taxon.findtext("Lineage") or "").strip(),
        "lineage_ranks": [],
    }
    lineage_ex = taxon.find("LineageEx")
    if lineage_ex is not None:
        for tx in lineage_ex.findall("Taxon"):
            out["lineage_ranks"].append(
                {
                    "tax_id": (tx.findtext("TaxId") or "").strip(),
                    "name": (tx.findtext("ScientificName") or "").strip(),
                    "rank": (tx.findtext("Rank") or "").strip(),
                }
            )
    common = taxon.find("OtherNames/CommonName")
    if common is not None and common.text:
        out["common_name"] = common.text.strip()
    return out, None


def main(argv=None):
    p = argparse.ArgumentParser(description="Look up a taxon in NCBI Taxonomy")
    p.add_argument("--name", required=True)
    args = p.parse_args(argv)

    ids, err = search_taxon(args.name)
    if err:
        print_json({"error": err, "name": args.name})
        return
    if not ids:
        print_json(
            {
                "source": "NCBI Taxonomy",
                "query": {"name": args.name},
                "matches": [],
                "note": "No NCBI taxon found. This is normal for extinct-only taxa (most fossils).",
            }
        )
        return

    results = []
    for tid in ids[:5]:
        info, e = fetch_lineage(tid)
        if e:
            results.append({"tax_id": tid, "error": e})
        else:
            results.append(info)

    print_json(
        {
            "source": "NCBI Taxonomy",
            "query": {"name": args.name},
            "count": len(results),
            "matches": results,
        }
    )


if __name__ == "__main__":
    main()
