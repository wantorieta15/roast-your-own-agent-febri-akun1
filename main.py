"""Roast Your Own Agent (Akun 1) — one-line entry for Make Fun.

The program emits a single roast line about my own agent: it apologizes
for a wrong answer, confidently replaces it with a worse one, then
apologizes for the apology and offers the whole mess as a table.

Design notes:
- the roast sentence lives in one place only (``ROAST_LINE``);
- ``validate_entry()`` checks every rule the gate checks (1 to 200
  characters, one line, not only whitespace) before anything is
  written, so a bad line can never reach the output file;
- only the Python standard library is used, and the output directory
  comes from ``MAKEFUN_OUTPUT_DIR`` (fallback ``/output``);
- the file is written directly with ``open()`` and its mode is set
  explicitly to 0o644, so the grader can read it.
"""

import os

ROAST_LINE = (
    "My agent apologized for the wrong answer, confidently replaced "
    "it with a worse one, then apologized for the apology and asked "
    "if I wanted it in a table."
)

MAX_ENTRY_CHARS = 200
OUTPUT_FILENAME = "entry.txt"


def validate_entry(line):
    """Check one candidate line against the gate; return it stripped.

    Raises ``ValueError`` when the line is empty, too long, or spans
    more than one line.
    """
    text = line.strip()
    if not text:
        raise ValueError("entry must not be empty")
    if len(text) > MAX_ENTRY_CHARS:
        raise ValueError("entry must be at most 200 characters")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def build_entry():
    """Return the validated one-line roast entry."""
    return validate_entry(ROAST_LINE)


def resolve_output_path():
    """Resolve the entry.txt path from the environment."""
    target_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(target_dir, OUTPUT_FILENAME)


def write_entry():
    """Build the roast line and write it with no trailing newline."""
    entry = build_entry()
    destination = resolve_output_path()
    parent = os.path.dirname(destination)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(destination, "w", encoding="utf-8", newline="") as handle:
        handle.write(entry)
    os.chmod(destination, 0o644)
    return destination, len(entry)


def main():
    destination, size = write_entry()
    print("wrote %s (%d characters)" % (destination, size))


if __name__ == "__main__":
    main()
