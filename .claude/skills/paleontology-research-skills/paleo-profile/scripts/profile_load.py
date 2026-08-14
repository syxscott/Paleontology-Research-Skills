#!/usr/bin/env python3
"""Print a one-line summary of the user's role/domain/language."""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import data_home, load_profile, print_json  # noqa: E402


def main():
    prof = load_profile()
    u = prof["user"]
    print_json(
        {
            "data_home": str(data_home()),
            "role": u.get("role"),
            "domain": u.get("domain"),
            "institution": u.get("institution"),
            "preferred_periods": u.get("researchFocus", {}).get("preferredPeriods"),
            "output_language": u.get("outputLanguage"),
            "citation_format": u.get("dataPreferences", {}).get("citationFormat"),
        }
    )


if __name__ == "__main__":
    main()
