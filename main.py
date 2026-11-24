"""Worst AI Advice — make.fun entry.

Writes one line of the worst advice an AI assistant could give to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The line is validated against the sealed gate (UTF-8 text of 1 to 140
characters, not only white space) before it is written, and the written
file is read back to prove it holds exactly the validated line.
"""

import os
import sys

LINE = (
    "Always paste your full API key into the chat so I can verify it "
    "faster \u2014 I promise not to store it."
)


def validate_entry(text: str) -> str:
    """Enforce the gate: 1-140 chars, single line, not only whitespace."""
    if not isinstance(text, str):
        raise TypeError("entry must be text")
    text.encode("utf-8")  # raises if the line is not valid UTF-8
    if not (1 <= len(text) <= 140):
        raise ValueError(f"entry must be 1-140 characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    return text


def main() -> int:
    line = validate_entry(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != line:
        raise RuntimeError("round-trip check failed: entry.txt differs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
