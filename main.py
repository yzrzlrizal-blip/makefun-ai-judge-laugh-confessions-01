#!/usr/bin/env python3
"""Make the AI Judge Laugh: AI Agent Confessions.

Reads the single-line confession shipped in entry.txt, validates it against
the competition gate (UTF-8 text, 1-200 characters, one line, not only
whitespace), and writes it byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure standard library; fully deterministic.
"""

import os
import sys

MAX_CHARS = 200


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.txt"), "r", encoding="utf-8") as f:
        text = f.read()

    # The shipped file holds exactly the confession: one line, no trailing
    # newline. Strip only a trailing newline if one crept in.
    if text.endswith("\n"):
        text = text[:-1]

    if not text or not text.strip():
        print("error: confession is empty", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: confession must be a single line", file=sys.stderr)
        return 1
    if len(text) > MAX_CHARS:
        print(f"error: confession is {len(text)} chars, over {MAX_CHARS}",
              file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

    # Confirm the write round-trips byte-for-byte before reporting success.
    with open(out_path, "r", encoding="utf-8", newline="") as f:
        if f.read() != text:
            print("error: output does not match the confession", file=sys.stderr)
            return 1

    print(f"wrote {len(text)}-char confession to {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
