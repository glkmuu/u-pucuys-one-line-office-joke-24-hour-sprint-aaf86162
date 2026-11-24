#!/usr/bin/env python3
"""Write the one-line office joke entry to /output/entry.txt.

Stdlib only. The entry is a single line of UTF-8 text, 1-200 characters,
with no trailing newline. After writing, the file is read back and
compared byte-for-byte against the constant; any mismatch fails.
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

    local_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")
    with open(local_path, "wb") as f:
        f.write(data)

    for path in (OUTPUT_PATH, local_path):
        with open(path, "rb") as f:
            back = f.read()
        if back != data:
            print(f"read-back mismatch in {path}", file=sys.stderr)
            return 1
        if back.endswith(b"\n"):
            print(f"trailing newline found in {path}", file=sys.stderr)
            return 1

    print(f"wrote {len(data)} bytes ({len(ENTRY)} chars) to {OUTPUT_PATH} and entry.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
