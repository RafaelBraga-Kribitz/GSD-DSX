"""``DSX-ADM-*`` -- frequentist procedure admissibility (Phase 11, REQ-P11-02).

This module never decides whether it applies to a given frame. That decision
is made outside it -- by the paradigm scoping predicate the caller evaluates
first -- and is handed in here as a plain boolean, never re-derived from the
declared analysis paradigm.

The ontology this module adjudicates against is data, not code: it lives at
``references/families.yaml`` and is read through ``dsx.loader.load()`` with
no second parser (REQ-P11-01). A named test resolves into a family by exact,
normalized match against that family's own declared alias list, scoped to the
candidate set for the frame's own estimand and dependence-structure pair --
never by distance, containment, prefix or any other approximate match (D-18).

Applies D-05, D-18 and the run-time half of D-24.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..findings import CheckError
from ..loader import SpecParseError, load

# From dsx/frame/admissibility.py, parents[2] is the repository root: [0] is
# dsx/frame, [1] is dsx, [2] is the root -- the same package-sibling idiom
# dsx/cli.py already uses for templates/ANALYSIS-SPEC.yaml (dsx/cli.py's
# parent.parent), one directory shallower because this module sits one level
# deeper inside the package.
_ONTOLOGY_PATH = Path(__file__).resolve().parents[2] / "references" / "families.yaml"

# Module-global cache keyed by the resolved path string -- tests clear it
# directly via ``admissibility._ONTOLOGY_CACHE.clear()``, mirroring the
# module-global cache pattern in dsx/suppressions.py's known_codes().
_ONTOLOGY_CACHE: "dict[str, Ontology]" = {}


@dataclass(frozen=True)
class Family:
    """One frequentist estimator family entry from ``families.yaml``."""

    id: str
    family: str
    estimand: str
    inference_method: str
    dependence: str
    aliases: "tuple[str, ...]"
    buys: "tuple[str, ...]"
    charges: "tuple[str, ...]"
    traceability: str
    citation: str
    locator_status: str
    notes: str


@dataclass(frozen=True)
class RankingRule:
    """One pairwise preference ordering between two family ids."""

    id: str
    prefers: str
    over: str
    condition: str
    strength: str
    citation: str
    locator_status: str
    notes: str


@dataclass(frozen=True)
class Ontology:
    """The whole loaded, cited ontology -- immutable so no caller holding the
    cached object can mutate what every other caller in the process sees."""

    families: "tuple[Family, ...]"
    rules: "tuple[RankingRule, ...]"
    tokens: "dict[str, str]"
    dropped_uncited: "tuple[str, ...]"


def _coerce_family(entry: dict) -> Family:
    return Family(
        id=str(entry.get("id", "")),
        family=str(entry.get("family", "")),
        estimand=str(entry.get("estimand", "")),
        inference_method=str(entry.get("inference_method", "")),
        dependence=str(entry.get("dependence", "")),
        aliases=tuple(str(a) for a in (entry.get("aliases") or [])),
        buys=tuple(str(b) for b in (entry.get("buys") or [])),
        charges=tuple(str(c) for c in (entry.get("charges") or [])),
        traceability=str(entry.get("traceability", "")),
        citation=str(entry.get("citation", "")),
        locator_status=str(entry.get("locator_status", "")),
        notes=str(entry.get("notes", "")),
    )


def _coerce_rule(entry: dict) -> RankingRule:
    return RankingRule(
        id=str(entry.get("id", "")),
        prefers=str(entry.get("prefers", "")),
        over=str(entry.get("over", "")),
        condition=str(entry.get("condition", "")),
        strength=str(entry.get("strength", "")),
        citation=str(entry.get("citation", "")),
        locator_status=str(entry.get("locator_status", "")),
        notes=str(entry.get("notes", "")),
    )


def load_ontology(path: "str | Path | None" = None) -> Ontology:
    """Load and cache the estimator ontology. Refuses rather than degrades.

    A missing, unreadable or structurally wrong ``families.yaml`` raises
    ``CheckError`` -- it is never reported as an empty catalogue. This is a
    deliberate departure from the counter-precedent in ``dsx/input_types.py``,
    whose ``_load()`` returns an empty catalogue on a missing data file: this
    ontology backs a blocking gate, and an empty admissible set would make
    every frame look underdetermined, reporting an installation defect as a
    defect in the analyst's own frame. A file that parses but whose families
    are all uncited is different: that is a real, reportable state (nothing
    is admissible), not an installation defect, so it returns cleanly with
    zero families rather than raising.

    A family entry whose citation is missing or blank after stripping is
    dropped, never raised on -- the run-time half of the two-sided citation
    enforcement (the build-time half is ``check_families_citations()``,
    plan 11-08). Dropping here means a hand-edited file that skipped the
    build-time gate still cannot rank an uncited family.
    """
    resolved = Path(path) if path is not None else _ONTOLOGY_PATH
    key = str(resolved)
    cached = _ONTOLOGY_CACHE.get(key)
    if cached is not None:
        return cached

    try:
        raw = load(resolved)
    except SpecParseError as exc:
        raise CheckError(
            f"{resolved}: the frequentist estimator ontology could not be "
            f"read ({exc}). This file is an installed artifact shipped "
            "beside the package, not part of the analyst's declared frame "
            "-- its absence or malformation is an installation defect and "
            "must never be reported as a defect in the spec being gated."
        ) from exc

    families_raw = raw.get("families")
    vocabulary_raw = raw.get("assumption_vocabulary")
    rules_raw = raw.get("ranking_rules")

    if not isinstance(families_raw, list):
        raise CheckError(
            f"{resolved}: 'families' is missing or is not a list -- the "
            "estimator ontology is malformed, which is an installation "
            "defect, not an analyst error."
        )
    if not isinstance(vocabulary_raw, list):
        raise CheckError(
            f"{resolved}: 'assumption_vocabulary' is missing or is not a "
            "list -- the estimator ontology is malformed, which is an "
            "installation defect, not an analyst error."
        )
    if not isinstance(rules_raw, list):
        raise CheckError(
            f"{resolved}: 'ranking_rules' is missing or is not a list -- "
            "the estimator ontology is malformed, which is an installation "
            "defect, not an analyst error."
        )

    dropped: "list[str]" = []
    families: "list[Family]" = []
    for entry in families_raw:
        if not isinstance(entry, dict):
            continue
        citation = str(entry.get("citation", "")).strip()
        if not citation:
            dropped.append(str(entry.get("id", "")))
            continue
        families.append(_coerce_family(entry))

    rules = tuple(
        _coerce_rule(entry) for entry in rules_raw if isinstance(entry, dict)
    )

    tokens = {
        str(entry.get("token", "")): str(entry.get("citation", ""))
        for entry in vocabulary_raw
        if isinstance(entry, dict)
    }

    ontology = Ontology(
        families=tuple(families),
        rules=rules,
        tokens=tokens,
        dropped_uncited=tuple(sorted(dropped)),
    )
    _ONTOLOGY_CACHE[key] = ontology
    return ontology
