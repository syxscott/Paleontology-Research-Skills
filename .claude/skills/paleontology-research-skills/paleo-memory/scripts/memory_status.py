#!/usr/bin/env python3
"""Report counts and paths of the local memory store."""

from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import data_home, memory_root, print_json  # noqa: E402


def main():
    h = memory_root()
    short_dir = h / "short"
    long_file = h / "long_term.jsonl"
    arch_dir = h / "archive" / "short"
    short_count = len(list(short_dir.glob("*.json"))) if short_dir.exists() else 0
    long_count = 0
    if long_file.exists():
        try:
            for line in long_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    long_count += 1
        except OSError:
            long_count = 0
    arch_count = len(list(arch_dir.glob("*.json"))) if arch_dir.exists() else 0
    print_json(
        {
            "shortCount": short_count,
            "longCount": long_count,
            "archiveCount": arch_count,
            "memoryRoot": str(h),
            "shortDir": str(short_dir),
            "longFile": str(long_file),
            "archiveDir": str(arch_dir),
            "dataHome": str(data_home()),
        }
    )


if __name__ == "__main__":
    main()
