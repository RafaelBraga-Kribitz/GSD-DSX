#!/usr/bin/env python3
"""Generate dsx/data/input_types.json from references/input-type-inventory.md.

The inventory is the source of truth for item content (id, name, signature,
columns, example, use_for, pattern_code) and is never rewritten by this script —
every one of those fields is copied verbatim out of the JSON block in the
Markdown file.

This script only *adds* two fields per item, which are what make the catalogue
usable as a deterministic gate:

  family      the coarse data_input_type this shape belongs to
  admissible  the dsx mark names permitted for this shape

Run after editing the inventory:

    python scripts/gen-input-types.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references" / "input-type-inventory.md"
TARGET = ROOT / "dsx" / "data" / "input_types.json"

# IT id -> coarse family. Derived from the declared signature, not from prose.
FAMILY: dict[str, str] = {
    "IT001": "bivariate-simple",
    "IT002": "bivariate-dual",
    "IT003": "trivariate",
    "IT004": "single-value",
    "IT005": "categorical-value",
    "IT006": "grouped-categorical",
    "IT007": "composition",
    "IT008": "grouped-categorical",
    "IT009": "event-time",
    "IT010": "geospatial",
    "IT011": "categorical-multi",
    "IT012": "trivariate",
    "IT013": "bivariate-dual",
    "IT014": "interval-range",
    "IT015": "grouped-categorical",
    "IT016": "composition",
    "IT017": "financial-ohlc",
    "IT018": "time-series",
    "IT019": "single-value",
    "IT020": "composition",
    "IT021": "matrix",
    "IT022": "hierarchical",
    "IT023": "composition",
    "IT024": "hierarchical",
    "IT025": "single-value",
    "IT026": "categorical-value",
    "IT027": "categorical-multi",
    "IT028": "matrix",
    "IT029": "categorical-multi",
    "IT030": "categorical-value",
    "IT031": "categorical-multi",
    "IT032": "categorical-multi",
    "IT033": "grouped-categorical",
    "IT034": "bivariate-dual",
    "IT035": "composition",
    "IT036": "interval-range",
    "IT037": "hierarchical",
    "IT038": "bivariate-simple",
    "IT039": "categorical-multi",
    "IT040": "interval-range",
}

# Marks admitted for a shape *beyond* its family's set, because the catalogue
# names a specific mark the family does not carry. Additive only.
EXTRA_MARKS: dict[str, set[str]] = {
    "IT011": {"population_pyramid", "butterfly"},
    "IT014": {"gantt", "timeline"},
    "IT036": {"gantt", "timeline"},
    "IT017": {"candlestick", "ohlc_bar"},
    "IT022": {"pie", "donut"},
    "IT024": {"icicle"},
    "IT037": {"icicle"},
    "IT028": {"heatmap"},
}

# Where the permitted list is deliberately narrower than the catalogue's own
# `use_for` text. The two fields do different jobs: `use_for` is descriptive —
# what people do with this shape — and `admissible` is prescriptive — what this
# tool will let through a gate. A prescriptive list being narrower than a
# descriptive one is correct, not inconsistent. Recorded per item so the
# difference reads as a decision rather than a defect.
NARROWED: dict[str, str] = {
    "IT025": (
        "use_for names a gauge; gauge is excluded. A gauge encodes one number as "
        "arc length against a maximum the author picks, so the reader decodes a "
        "proportion that the data never asserted. big_number states the value "
        "without implying a scale; bullet states it against a target that has to "
        "be declared."
    ),
}

# Signatures that more than one catalogue entry shares. The lookup is keyed on
# the shape, so these collapse to one answer by construction — which is only
# safe while their admissible sets are identical. Asserted at generation time.
SHARED_SIGNATURE_GROUPS: list[list[str]] = [
    ["IT004", "IT019", "IT025"],  # all [numeric]
]


def main() -> int:
    if not SOURCE.exists():
        print(f"missing source: {SOURCE}", file=sys.stderr)
        return 1

    text = SOURCE.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)
    if not match:
        print("no JSON block found in the inventory", file=sys.stderr)
        return 1

    data = json.loads(match.group(1))
    items = data["input_types"]

    expected = [f"IT{n:03d}" for n in range(1, 41)]
    actual = [item["id"] for item in items]
    if actual != expected:
        print(f"id drift: expected {len(expected)} ids IT001..IT040, got {len(actual)}", file=sys.stderr)
        return 1

    # Imported lazily so this script can run before the package is importable.
    sys.path.insert(0, str(ROOT))
    from dsx.spec import CHART_CAPABILITIES  # noqa: E402

    out = []
    for item in items:
        it_id = item["id"]
        family = FAMILY[it_id]
        if family not in CHART_CAPABILITIES:
            print(f"{it_id}: family {family!r} missing from CHART_CAPABILITIES", file=sys.stderr)
            return 1
        admissible = set(CHART_CAPABILITIES[family]) | EXTRA_MARKS.get(it_id, set())
        record = dict(item)  # verbatim fields preserved
        record["family"] = family
        record["admissible"] = sorted(admissible)
        if it_id in NARROWED:
            record["narrowed_from_use_for"] = NARROWED[it_id]
        out.append(record)

    # A shared signature must resolve to a single answer, or the lookup is
    # ambiguous at its own key. Fail generation rather than ship the ambiguity.
    by_id = {record["id"]: record for record in out}
    for group in SHARED_SIGNATURE_GROUPS:
        signatures = {by_id[i]["signature"] for i in group}
        admissibles = {tuple(by_id[i]["admissible"]) for i in group}
        if len(signatures) != 1:
            print(f"{group}: expected one shared signature, got {signatures}", file=sys.stderr)
            return 1
        if len(admissibles) != 1:
            print(
                f"{group} share signature {signatures.pop()} but disagree on admissible marks: "
                f"{admissibles}. Either give them a discriminating field or make them agree.",
                file=sys.stderr,
            )
            return 1

    payload = {
        "metadata": {
            **data.get("metadata", {}),
            "generated_by": "scripts/gen-input-types.py",
            "source": "references/input-type-inventory.md",
            "note": (
                "id/name/signature/columns/example/use_for/pattern_code are copied "
                "verbatim from the inventory. family and admissible are added here."
            ),
            "use_for_vs_admissible": (
                "use_for is descriptive (what people do with this shape); admissible "
                "is prescriptive (what passes a gate). Where the prescriptive list is "
                "narrower, the item carries a narrowed_from_use_for field giving the "
                "reason. A narrower prescriptive list is a decision, not a defect."
            ),
            "shared_signatures": (
                "IT004, IT019 and IT025 all declare signature [numeric]. The lookup is "
                "keyed on shape, so they resolve to one identical answer. Generation "
                "fails if their admissible sets ever diverge, because that would make "
                "the lookup ambiguous at its own key."
            ),
        },
        "input_types": out,
    }

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {TARGET.relative_to(ROOT)} ({len(out)} input types)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
