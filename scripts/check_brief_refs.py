#!/usr/bin/env python3
"""Verify brief.md section 7 carries the D-17 citation-ledger extension.

Checked by this script (07-02-PLAN.md, task 1 acceptance criteria):

1. Section 7 contains each of ten required substrings — the six newly added
   sources plus the three re-pinned/re-cited existing entries.
2. Section 7 contains the word "unverified" at least three times — one for
   the Kish section locator, one for the Gelman/Simpson/Betancourt typeset-
   version caveat, one for the Gelman and Hill chapter locator.
3. Section 7 contains "3rd ed." or "third edition" for both Lohr and Little
   and Rubin.
4. Section 7 does NOT contain the string "Conley" — Conley (1999) is
   deliberately excluded (only training-knowledge attribution was
   available for it).

This repository checks out CRLF on Windows (see .claude/CLAUDE.md), so the
section-7 extraction regex tolerates \\r\\n as well as \\n.

Exit code 0 on success, 1 on any failed criterion.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BRIEF = ROOT / "brief.md"

REQUIRED_SUBSTRINGS = (
    "E9(R1)",
    "Hernan and Robins (2016)",
    "Popper",
    "Kish (1965)",
    "Cochrane Handbook",
    "Cronbach and Meehl (1955)",
    "Lohr (2021)",
    "Little and Rubin (2019)",
    "White and Carlin (2010)",
    "Cameron and Miller (2015)",
)

FORBIDDEN_SUBSTRINGS = ("Conley",)

MIN_UNVERIFIED_COUNT = 3


def extract_section_7(text: str) -> str:
    """Return the body of '## 7. Reference sources', up to the next '---'."""
    match = re.search(
        r"##\s*7\.\s*Reference sources\r?\n\r?\n(.*?)\r?\n\r?\n---",
        text,
        re.S,
    )
    if not match:
        raise SystemExit("FAIL: could not locate '## 7. Reference sources' section in brief.md")
    return match.group(1)


def main() -> int:
    if not BRIEF.exists():
        print(f"FAIL: {BRIEF} does not exist", file=sys.stderr)
        return 1

    text = BRIEF.read_text(encoding="utf-8")
    section_raw = extract_section_7(text)
    # The flowing-paragraph convention hard-wraps at ~100 columns, so a
    # citation string can be split across a line break (e.g. "White and\r\n
    # Carlin (2010)"). Collapse all whitespace runs to a single space before
    # substring matching so wrapping is not mistaken for missing content.
    section = re.sub(r"\s+", " ", section_raw)

    failures: list[str] = []

    print("Checking brief.md section 7 (D-17 citation-ledger extension)...")

    for needle in REQUIRED_SUBSTRINGS:
        present = needle in section
        print(f"  [{'ok' if present else 'FAIL'}] contains {needle!r}")
        if not present:
            failures.append(f"missing required string: {needle!r}")

    for needle in FORBIDDEN_SUBSTRINGS:
        absent = needle not in section
        print(f"  [{'ok' if absent else 'FAIL'}] does not contain {needle!r}")
        if not absent:
            failures.append(f"forbidden string present: {needle!r}")

    unverified_count = section.count("unverified")
    ok = unverified_count >= MIN_UNVERIFIED_COUNT
    print(
        f"  [{'ok' if ok else 'FAIL'}] contains 'unverified' at least "
        f"{MIN_UNVERIFIED_COUNT} times (found {unverified_count})"
    )
    if not ok:
        failures.append(
            f"'unverified' appears {unverified_count} times, need >= {MIN_UNVERIFIED_COUNT}"
        )

    # Window-based check: the edition marker must appear near the entry it
    # pins, not merely somewhere in section 7 (which would trivially pass on
    # the strength of one edition and say nothing about the other).
    WINDOW = 250
    for label, needle in (
        ("Lohr", "Lohr (2021)"),
        ("Little and Rubin", "Little and Rubin (2019)"),
    ):
        pos = section.find(needle)
        nearby = section[pos : pos + WINDOW] if pos != -1 else ""
        has_edition = pos != -1 and ("3rd ed." in nearby or "third edition" in nearby)
        print(f"  [{'ok' if has_edition else 'FAIL'}] '3rd ed.' or 'third edition' present near {label}")
        if not has_edition:
            failures.append(f"no edition marker ('3rd ed.' / 'third edition') found near {label}")

    if failures:
        print("\nFAILED checks:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
