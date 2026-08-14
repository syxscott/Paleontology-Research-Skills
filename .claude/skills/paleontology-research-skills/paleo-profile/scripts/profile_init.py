#!/usr/bin/env python3
"""Initialise (or re-initialise) the user's soul.md and user.md files.

By default refuses to overwrite an existing file unless ``--force`` is given.
"""

from __future__ import annotations

import argparse
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SHARED = os.path.normpath(os.path.join(_HERE, "..", "..", "scripts"))
if _SHARED not in sys.path:
    sys.path.insert(0, _SHARED)

from paleo_common import (  # noqa: E402  # noqa: E402
    _DEFAULT_SOUL,
    _DEFAULT_USER,
    data_home,
    print_json,
    profile_files,
    write_text_file,
)


def main(argv=None):
    p = argparse.ArgumentParser(description="Initialise the Paleontology Research Skills profile files")
    p.add_argument("--force", action="store_true", help="Overwrite existing profile files")
    args = p.parse_args(argv)

    sp, up = profile_files()
    sp.parent.mkdir(parents=True, exist_ok=True)

    actions = []
    for path, content, _label in ((sp, _DEFAULT_SOUL, "soul.md"), (up, _DEFAULT_USER, "user.md")):
        existed = path.exists()
        if existed and not args.force:
            actions.append(
                {"file": str(path), "status": "skipped", "note": "exists; use --force to overwrite"}
            )
        else:
            write_text_file(path, content)
            status = "overwritten" if existed else "written"
            actions.append({"file": str(path), "status": status, "bytes": len(content)})
    print_json({"data_home": str(data_home()), "actions": actions})


if __name__ == "__main__":
    main()
