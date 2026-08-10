"""Deterministic chart lookup keyed on the shape of the data.

The agent should never ask an open question about which chart to use. It names
the shape of the data (an IT id from the IT001-IT040 inventory, or one of the
coarse family names) and, where known, the relationship the chart argues. This
module returns the permitted marks. Nothing here is a judgement call.

Source of truth for item content is ``references/input-type-inventory.md``.
``dsx/data/input_types.json`` is generated from it by
``scripts/gen-input-types.py``.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

_DATA = Path(__file__).resolve().parent / "data" / "input_types.json"

_IT_PATTERN = re.compile(r"^it[\s_-]*0*(\d{1,3})$", re.I)


class UnknownShape(KeyError):
    """Raised when a shape key matches neither an IT id nor a family name."""


@lru_cache(maxsize=1)
def _load() -> dict[str, Any]:
    if not _DATA.exists():
        return {"metadata": {}, "input_types": []}
    with _DATA.open(encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _by_id() -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in _load().get("input_types", [])}


def canonical_id(raw: str) -> str | None:
    """Normalise ``it1``/``IT-001``/``IT001`` to ``IT001``. None if not an IT id."""
    if not isinstance(raw, str):
        return None
    match = _IT_PATTERN.match(raw.strip())
    if not match:
        return None
    number = int(match.group(1))
    if not 1 <= number <= 999:
        return None
    candidate = f"IT{number:03d}"
    return candidate if candidate in _by_id() else None


def input_types() -> list[dict[str, Any]]:
    """Every catalogue entry, in id order."""
    return list(_load().get("input_types", []))


def get(shape: str) -> dict[str, Any]:
    """Look up one entry by IT id. Raises UnknownShape if there is no such id."""
    it_id = canonical_id(shape)
    if it_id is None:
        raise UnknownShape(shape)
    return _by_id()[it_id]


def family_of(shape: str) -> str | None:
    """The coarse data_input_type for an IT id, or None if not an IT id."""
    it_id = canonical_id(shape)
    return _by_id()[it_id]["family"] if it_id else None


def permitted(shape: str, relationship: str | None = None) -> list[str]:
    """Marks permitted for this shape, narrowed by relationship when given.

    ``shape`` is an IT id (``IT007``) or a coarse family (``composition``).
    When ``relationship`` is supplied and the intersection is non-empty, the
    result is the intersection — the marks that satisfy both constraints. An
    empty intersection returns the shape's own set rather than nothing, because
    "no chart is valid" is almost always a mis-declared relationship rather than
    a real dead end, and the caller needs something to report.
    """
    from .checks.viz import RELATIONSHIP_CHARTS
    from .spec import CHART_CAPABILITIES

    it_id = canonical_id(shape)
    if it_id:
        allowed = set(_by_id()[it_id]["admissible"])
    else:
        key = str(shape).strip().lower().replace("_", "-")
        if key not in CHART_CAPABILITIES:
            raise UnknownShape(shape)
        allowed = set(CHART_CAPABILITIES[key])

    if relationship:
        rel = str(relationship).strip().lower().replace("-", "_")
        narrowed = allowed & set(RELATIONSHIP_CHARTS.get(rel, ()))
        if narrowed:
            return sorted(narrowed)

    return sorted(allowed)


def known_shapes() -> list[str]:
    """Every accepted shape key: the 40 IT ids plus the coarse family names."""
    from .spec import DATA_INPUT_TYPES

    return sorted(_by_id()) + sorted(DATA_INPUT_TYPES)
