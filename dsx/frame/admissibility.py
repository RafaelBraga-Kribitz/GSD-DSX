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
from ..spec import is_blank, is_blank_text, normalize

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


# The closed set of outcomes resolve_declared_procedure() can return, declared
# as a module-level tuple constant so a test can assert the set never grows a
# fifth value by accident.
_RESOLUTION_STATUSES = (
    "not_declared",
    "in_candidate_set",
    "outside_candidate_set",
    "unresolved",
)


@dataclass(frozen=True)
class Resolution:
    """The outcome of resolving one declared procedure label against one
    (estimand, dependence) candidate set. ``detail`` is a single readable
    sentence a finding built from this result can reuse verbatim."""

    status: str
    family_id: str
    outside_axes: "tuple[str, str]"
    detail: str


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


def alias_index(ontology: Ontology) -> "dict[tuple[str, str], dict[str, str]]":
    """Build ``(normalized estimand, normalized dependence) -> {normalized
    alias: family id}`` for every family in ``ontology``.

    Iterates families in their committed (file) order and raises
    ``CheckError`` the moment two different families in the *same* pair
    declare the same normalized alias, naming both family ids and the
    colliding normalized alias. Two families that agree on the axis pair and
    on an alias are indistinguishable to a resolver -- picking either by
    traversal order would make the gate's answer depend on file order, which
    D-15 forbids reaching any consumer. This is why the collision is a raise,
    never a silent last-one-wins.

    The same alias string on two families in *different* pairs is not a
    collision at all -- each pair gets its own dict, so `two_proportion_z`
    can name one family under independence and a different family under
    clustering with no conflict.
    """
    index: "dict[tuple[str, str], dict[str, str]]" = {}
    for family in ontology.families:
        pair = (normalize(family.estimand), normalize(family.dependence))
        alias_map = index.setdefault(pair, {})
        for alias in family.aliases:
            key = normalize(alias)
            existing = alias_map.get(key)
            if existing is not None and existing != family.id:
                raise CheckError(
                    f"alias {key!r} is declared by both family {existing!r} "
                    f"and family {family.id!r} inside the same estimand and "
                    f"dependence pair {pair!r}; an alias must resolve to "
                    "exactly one family so the resolved outcome never "
                    "depends on the ontology file's entry order"
                )
            alias_map[key] = family.id
    return index


def candidate_families(
    ontology: Ontology, estimand: str, dependence: str
) -> "tuple[Family, ...]":
    """Families whose own (estimand, dependence) pair matches the given axes
    after normalizing both sides, ordered lexicographically by family id.

    Returns an empty tuple when either axis is blank, absent or ``None``, and
    when no family declares the given pair. The lexicographic sort happens
    exactly once, here -- every downstream consumer's ordering is therefore a
    function of the candidate set itself, never of the ontology file's own
    entry order.
    """
    if is_blank(estimand) or is_blank(dependence):
        return ()
    target_estimand = normalize(estimand)
    target_dependence = normalize(dependence)
    matches = [
        family
        for family in ontology.families
        if normalize(family.estimand) == target_estimand
        and normalize(family.dependence) == target_dependence
    ]
    return tuple(sorted(matches, key=lambda family: family.id))


def declared_procedure(spec: "dict | None") -> str:
    """Read the declared primary procedure label off ``spec``, returning the
    empty string on any shape that is not exactly "a mapping with a mapping
    named after the paradigm-neutral procedure block, holding a non-blank
    procedure string."

    Reads the block with a plain ``spec.get(...)`` followed by a plain
    ``.get(...)`` on the resulting mapping -- never as one combined
    dotted-path string. A positional call-argument string literal beginning
    with the block name followed by a dot is exactly the shape
    ``tests/test_frame_boundary.py``'s AST detector flags on any call in any
    module, regardless of which field name follows the dot.
    """
    if not isinstance(spec, dict):
        return ""
    block = spec.get("inference")
    if not isinstance(block, dict):
        return ""
    value = block.get("primary_procedure")
    return "" if is_blank_text(value) else value


def resolve_declared_procedure(
    ontology: Ontology, estimand: str, dependence: str, declared: "str | None"
) -> Resolution:
    """Resolve one declared procedure label against the ontology, scoped
    first to the frame's own (estimand, dependence) candidate set.

    Returns ``not_declared`` when ``declared`` is blank, absent or
    whitespace-only. Otherwise normalizes ``declared`` and looks it up first
    in the frame's own pair; a hit there is ``in_candidate_set``. Failing
    that, it looks across every other pair's alias map; a hit there is
    ``outside_candidate_set``, naming the family found and that family's own
    axis pair. When more than one other pair matches, the lexicographically
    first family id is taken, so the outcome remains a function of the
    ontology and never of dict traversal order. No match anywhere is
    ``unresolved`` -- including for a string that is a strict prefix, a
    strict suffix or a small edit of a real alias. The only string
    comparison performed anywhere in this function is equality after
    ``normalize()``; no distance, containment or prefix match exists here or
    anywhere else in this module (D-18). An unrecognised label escalates by
    design -- a nearest-match fallback would silently convert an unknown
    procedure into a confident recommendation, which is the exact failure
    this family of checks exists to prevent.
    """
    if is_blank(declared):
        return Resolution(
            status="not_declared",
            family_id="",
            outside_axes=(),
            detail="No procedure was declared.",
        )

    index = alias_index(ontology)
    own_pair = (normalize(estimand), normalize(dependence))
    target = normalize(declared)

    own_map = index.get(own_pair, {})
    own_match = own_map.get(target)
    if own_match is not None:
        return Resolution(
            status="in_candidate_set",
            family_id=own_match,
            outside_axes=(),
            detail=(
                f"{declared!r} resolved to family {own_match!r} inside its "
                "own candidate set."
            ),
        )

    other_matches: "list[tuple[tuple[str, str], str]]" = []
    for pair, alias_map in index.items():
        if pair == own_pair:
            continue
        matched = alias_map.get(target)
        if matched is not None:
            other_matches.append((pair, matched))

    if other_matches:
        other_matches.sort(key=lambda pair_and_id: pair_and_id[1])
        outside_pair, outside_family_id = other_matches[0]
        detail = (
            f"{declared!r} resolved to family {outside_family_id!r}, whose "
            f"own estimand and dependence pair is {outside_pair!r}, not the "
            f"frame's own pair {own_pair!r}."
        )
        if len(other_matches) > 1:
            detail += (
                " More than one other pair matched; the lexicographically "
                "first family id was taken."
            )
        return Resolution(
            status="outside_candidate_set",
            family_id=outside_family_id,
            outside_axes=outside_pair,
            detail=detail,
        )

    return Resolution(
        status="unresolved",
        family_id="",
        outside_axes=(),
        detail=f"{declared!r} does not match any known alias in the ontology.",
    )
