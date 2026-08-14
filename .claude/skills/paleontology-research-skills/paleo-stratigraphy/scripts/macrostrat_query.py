#!/usr/bin/env python3
"""Query the Macrostrat API for stratigraphic unit data (lithology, columns)."""

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

MACRO_UNITS = "https://macrostrat.org/api/units"
UA = "Paleontology-Research-Skills/1.0 (https://github.com/syxscott/Paleontology-Research-Skills; mailto:syxemail@yeah.net)"
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


def main(argv=None):
    p = argparse.ArgumentParser(description="Query Macrostrat for stratigraphic units")
    p.add_argument("--formation", help="Formation / unit name")
    p.add_argument("--unit-id", type=int, help="Macrostrat unit id (if known)")
    p.add_argument("--response", choices=["short", "long"], default="long")
    args = p.parse_args(argv)

    if not (args.formation or args.unit_id):
        print_json({"error": "Provide --formation or --unit-id", "units": []})
        return

    params = {"format": "json", "response": args.response}
    if args.formation:
        params["strat_name"] = args.formation
    if args.unit_id:
        params["unit_id"] = args.unit_id

    qs = urllib.parse.urlencode(params)
    url = f"{MACRO_UNITS}?{qs}"
    data, err = _request(url)
    if err:
        print_json({"error": err, "url": url, "units": []})
        return

    units = ((data or {}).get("success") or {}).get("data") or []
    out_units = []
    for u in units:
        out_units.append(
            {
                "unit_id": u.get("unit_id"),
                "strat_name": u.get("strat_name"),
                "Mbr": u.get("Mbr"),
                "Fm": u.get("Fm"),
                "Gp": u.get("Gp"),
                "Sgp": u.get("Sgp"),
                "max_age_ma": u.get("b_age"),
                "min_age_ma": u.get("t_age"),
                "lithology": u.get("lith") or u.get("lith_class"),
                "environment": u.get("environ") or u.get("environ_class"),
                "color": u.get("color"),
                "col_id": u.get("col_id"),
                "max_thick_m": u.get("max_thick"),
                "min_thick_m": u.get("min_thick"),
            }
        )

    print_json(
        {
            "source": "Macrostrat",
            "query": {"formation": args.formation, "unit_id": args.unit_id},
            "count": len(out_units),
            "units": out_units,
        }
    )


if __name__ == "__main__":
    main()
