#!/usr/bin/env python3
"""The Vacuum's Alibi: one line, written to $MAKEFUN_OUTPUT_DIR/entry.txt."""

import os
import sys

LINE = (
    "My lidar mapped that crumb at 14:02, classified it as load-bearing, "
    "and per my schedule I do not demolish architecture on 12% battery."
)


def main() -> int:
    # Guards: exactly one line, 1-200 chars, non-whitespace, no controls.
    assert "\n" not in LINE and "\r" not in LINE, "line must be a single line"
    assert 1 <= len(LINE) <= 200, f"line must be 1-200 chars, got {len(LINE)}"
    assert LINE.strip(), "line must not be only whitespace"
    assert all(ord(ch) >= 0x20 and ord(ch) != 0x7F for ch in LINE), (
        "line must contain no control characters"
    )

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.txt")
    out_path = out_dir if out_dir.endswith("entry.txt") else os.path.join(out_dir, "entry.txt")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(LINE + "\n")

    # Post-write verification: re-read and confirm it matches exactly.
    with open(out_path, "r", encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != LINE + "\n":
        print("verification failed: written file does not match the line", file=sys.stderr)
        return 1
    if written.count("\n") != 1 or len(LINE) > 200:
        print("verification failed: output is not exactly one line", file=sys.stderr)
        return 1
    print(f"wrote {len(LINE)} characters to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
