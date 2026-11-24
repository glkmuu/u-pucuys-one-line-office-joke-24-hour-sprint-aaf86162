#!/usr/bin/env python3
"""Write the one-line office joke entry to /output/entry.txt.

Stdlib only. The entry is a single line of UTF-8 text, 1-200 characters,
with no trailing newline. /output/entry.txt is written and read back
byte-for-byte; any mismatch fails. The copy next to this script is
best-effort only: the grader runs with a read-only repository, so a
strict local write would abort an otherwise valid entry.
"""

import os
import sys

ENTRY = "Our daily standup meeting now has chairs, which is fitting, because nobody in it has stood up for anything in years."

OUTPUT_PATH = "/output/entry.txt"


def main() -> int:
    data = ENTRY.encode("utf-8")
    # Gate: 1-200 characters, one line, no leading/trailing whitespace.
    if not 1 <= len(ENTRY) <= 200:
        print(f"entry length {len(ENTRY)} out of range 1-200", file=sys.stderr)
        return 1
    if ENTRY != ENTRY.strip() or "\n" in ENTRY or "\r" in ENTRY:
        print("entry must be a single line with no newline", file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)

    # Best-effort local copy (see module docstring).
    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    local_written = False
    try:
        with open(local_path, "wb") as f:
            f.write(data)
        local_written = True
    except OSError as exc:
        print(f"warning: local copy skipped ({exc})", file=sys.stderr)

    for path in [OUTPUT_PATH] + ([local_path] if local_written else []):
        with open(path, "rb") as f:
            back = f.read()
        if back != data:
            print(f"read-back mismatch in {path}", file=sys.stderr)
            return 1
        if back.endswith(b"\n"):
            print(f"trailing newline found in {path}", file=sys.stderr)
            return 1

    print(f"wrote {len(data)} bytes ({len(ENTRY)} chars) to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
