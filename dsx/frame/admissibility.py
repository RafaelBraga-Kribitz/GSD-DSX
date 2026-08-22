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
from functools import cmp_to_key
from pathlib import Path

from ..decisions import DecisionRecord
from ..findings import CheckError, Report
from ..loader import SpecParseError, load
from ..spec import get, is_blank, is_blank_text, normalize

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


# Non-rule placement reasons -- named constants so a test asserts against a
# name rather than a repeated string literal. Neither is a RankingRule id
# and neither ever collides with one: ranking_rules: ids in families.yaml are
# authored short handles (e.g. "welch_over_students"), never these two
# reserved sentences.
_MANSKI_RULE = "manski_fewer_assumptions_charged"
_TIEBREAK_RULE = "lexicographic_id_tiebreak"


@dataclass(frozen=True)
class RankedEntry:
    """One ranked admissible-set entry -- the shape both `admissible_families()`
    (task 2) and `DSX-ADM-010` (task 3) build on. `rank` runs 1 upward with no
    gaps; `placed_by` names the mechanism that placed this entry immediately
    below its predecessor -- a `RankingRule.id`, `_MANSKI_RULE`, or
    `_TIEBREAK_RULE` -- and is the empty string for the rank-1 entry, because
    nothing sits above it to place it."""

    rank: int
    id: str
    family: str
    buys: "tuple[str, ...]"
    charges: "tuple[str, ...]"
    citation: str
    locator_status: str
    notes: str
    placed_by: str


def _preference_reason(
    preferred_id: str, dominated_id: str, applicable_rules: "tuple[RankingRule, ...]"
) -> "str | None":
    """The id of the applicable rule whose `prefers` is `preferred_id` and whose
    `over` is `dominated_id`, or `None` when no such rule is applicable."""
    for rule in applicable_rules:
        if rule.prefers == preferred_id and rule.over == dominated_id:
            return rule.id
    return None


def rank_admissible(
    candidates: "tuple[Family, ...]", rules: "tuple[RankingRule, ...]"
) -> "tuple[RankedEntry, ...]":
    """Order `candidates` by a cited pairwise rule table, a fewer-assumptions
    credibility fallback, and a lexicographic identifier tiebreak -- never by
    a numeric score.

    This is a rule table and not a scoring function, because admissibility is
    a partial order by construction: no uniformly most powerful test exists
    for a two-sided or a general composite alternative, so no single number
    could honestly stand in for "how good is this family" across every
    candidate pair. The fewer-assumptions fallback branch is Manski's Law of
    Decreasing Credibility (Manski, C.F. (2003), Partial Identification of
    Probability Distributions, Introduction) -- a statement about how much an
    analyst has to assume to license a conclusion, about credibility, never
    about statistical efficiency or power. The base sort by
    `(len(charges), id)` plus a stable comparator-driven sort is what
    guarantees the same candidate set always produces the same order, even if
    the pairwise rules in `references/families.yaml` ever stopped being
    mutually transitive: the base ordering is itself a total order, so the
    combined result never depends on which order the caller happened to pass
    `candidates` in.

    Returns an empty tuple for an empty `candidates`, and a single rank-1
    entry with an empty `placed_by` for a one-element `candidates` -- neither
    case raises.
    """
    if not candidates:
        return ()

    candidate_ids = frozenset(family.id for family in candidates)
    applicable_rules = tuple(
        rule
        for rule in rules
        if rule.prefers in candidate_ids and rule.over in candidate_ids
    )

    base_ordering = sorted(candidates, key=lambda family: (len(family.charges), family.id))

    def _compare(a: Family, b: Family) -> int:
        if _preference_reason(a.id, b.id, applicable_rules) is not None:
            return -1
        if _preference_reason(b.id, a.id, applicable_rules) is not None:
            return 1
        if len(a.charges) != len(b.charges):
            return -1 if len(a.charges) < len(b.charges) else 1
        if a.id != b.id:
            return -1 if a.id < b.id else 1
        return 0

    ordered = sorted(base_ordering, key=cmp_to_key(_compare))

    entries: "list[RankedEntry]" = []
    for index, family in enumerate(ordered):
        if index == 0:
            placed_by = ""
        else:
            predecessor = ordered[index - 1]
            reason = _preference_reason(predecessor.id, family.id, applicable_rules)
            if reason is not None:
                placed_by = reason
            elif len(predecessor.charges) != len(family.charges):
                placed_by = _MANSKI_RULE
            else:
                placed_by = _TIEBREAK_RULE
        entries.append(
            RankedEntry(
                rank=index + 1,
                id=family.id,
                family=family.family,
                buys=family.buys,
                charges=family.charges,
                citation=family.citation,
                locator_status=family.locator_status,
                notes=family.notes,
                placed_by=placed_by,
            )
        )
    return tuple(entries)


def dominating_rules(
    family_id: str,
    candidates: "tuple[Family, ...]",
    rules: "tuple[RankingRule, ...]",
) -> "tuple[RankingRule, ...]":
    """Rules whose `over` is `family_id` and whose `prefers` is also a member
    of `candidates`, ordered as they appear in `rules` (ontology order).

    This is the predicate `DSX-ADM-010` (task 3) keys on, kept separate from
    `rank_admissible()` so that ordering a candidate set and asserting a
    domination against one specific family stay two different questions.
    Returns an empty tuple for a one-element `candidates` -- a lone candidate
    can never be dominated by a rule whose preferred side is absent from its
    own candidate set.
    """
    if len(candidates) <= 1:
        return ()
    candidate_ids = frozenset(family.id for family in candidates)
    return tuple(
        rule
        for rule in rules
        if rule.over == family_id and rule.prefers in candidate_ids
    )


# admissible_families()'s refusal vocabulary -- module-level string constants
# so a test can assert the cause set never silently grows a fourth member.
# The count is load-bearing (D-16): three distinct causes -- a required axis
# blank or absent, the complete (estimand, dependence) key matching zero
# families, and a declared procedure label that resolves to no family in the
# candidate set (or resolves only outside it) -- collapse into the single
# DSX-ADM-020 finding in task 3, because all three share one remedy and
# finding numbers are irreversible (D-06). Splitting them into separate codes
# later would burn irreversible code numbers for no operator benefit.
_REFUSAL = "no_admissible_procedure"
_CAUSE_BLANK_AXIS = "required_axis_blank"
_CAUSE_NO_MATCHING_FAMILY = "no_matching_family"
_CAUSE_UNRESOLVED = "declared_procedure_unresolved"
_REFUSAL_CAUSES = (_CAUSE_BLANK_AXIS, _CAUSE_NO_MATCHING_FAMILY, _CAUSE_UNRESOLVED)


def _ranked_entry_to_dict(entry: RankedEntry) -> "dict[str, object]":
    """Convert one ``RankedEntry`` into a plain, JSON-serialisable dict --
    every tuple field becomes a list, matching the pure-return-shape contract
    ``admissible_families()`` promises its own caller."""
    return {
        "rank": entry.rank,
        "id": entry.id,
        "family": entry.family,
        "buys": list(entry.buys),
        "charges": list(entry.charges),
        "citation": entry.citation,
        "locator_status": entry.locator_status,
        "notes": entry.notes,
        "placed_by": entry.placed_by,
    }


def admissible_families(spec: "dict | None") -> "dict[str, object]":
    """Rank the admissible procedure set for one declared frame -- a pure,
    total function mirroring the split already shipped in
    ``dsx/checks/stats.py`` between the pure ``recommend_test()`` and the
    ``Report``-emitting ``_check_declared_test()``. No ``Report``, no
    finding, no ``DecisionRecord``, no file write happens anywhere in this
    function -- that split is what lets ``dsx/cli.py::cmd_recommend`` call
    the ranking directly without a gate report, and what lets task 3's
    ``check()`` call this function exactly once and read every judgement it
    needs off the returned dict.

    Reads the two frame axes with the dotted-path helper
    (``validity_frame.estimand.type``, ``validity_frame.dependence.structure``)
    and the declared procedure with ``declared_procedure(spec)`` (plan
    11-05), which reads the paradigm-neutral procedure block as a plain
    mapping chain rather than a combined dotted-path string. ``get()``
    already degrades a non-mapping ``spec`` to its default, so a ``None`` or
    non-dict ``spec`` reaches the same blank-axis refusal shape as a real
    spec with blank axes, rather than raising.

    Every dataclass and tuple is converted to a list or dict before
    returning, so the result survives ``json.dumps`` unchanged and calling
    this function twice on the same spec produces byte-identical JSON.

    The three refusal causes are checked in a fixed order -- blank axis,
    then no matching family, then unresolved declared procedure -- and
    exactly one is ever reported, because a spec can be blank *and* miss
    every family at once, and the order has to be a property of this
    function, not of which branch happened to be written first.
    """
    ontology = load_ontology()

    estimand = get(spec, "validity_frame.estimand.type")
    dependence = get(spec, "validity_frame.dependence.structure")
    declared = declared_procedure(spec)

    resolution = resolve_declared_procedure(ontology, estimand, dependence, declared)

    base: "dict[str, object]" = {
        "estimand": estimand if isinstance(estimand, str) else (estimand or ""),
        "dependence": dependence if isinstance(dependence, str) else (dependence or ""),
        "declared_procedure": declared,
        "resolution": resolution.status,
        "resolved_family": resolution.family_id,
        # The number of families the ontology loaded after uncited entries
        # were dropped -- lets an operator reading `dsx recommend-test`
        # output tell an empty admissible set caused by a narrow frame apart
        # from one caused by a stripped ontology.
        "ontology_entries": len(ontology.families),
    }

    if is_blank(estimand) or is_blank(dependence):
        return {
            **base,
            "admissible": [],
            "refusal": _REFUSAL,
            "refusal_cause": _CAUSE_BLANK_AXIS,
        }

    candidates = candidate_families(ontology, estimand, dependence)
    if not candidates:
        return {
            **base,
            "admissible": [],
            "refusal": _REFUSAL,
            "refusal_cause": _CAUSE_NO_MATCHING_FAMILY,
        }

    ranked = rank_admissible(candidates, ontology.rules)
    admissible_list = [_ranked_entry_to_dict(entry) for entry in ranked]

    if resolution.status in ("unresolved", "outside_candidate_set"):
        return {
            **base,
            "admissible": admissible_list,
            "refusal": _REFUSAL,
            "refusal_cause": _CAUSE_UNRESOLVED,
        }

    return {
        **base,
        "admissible": admissible_list,
        "refusal": "",
        "refusal_cause": "",
    }


def _check_declared_procedure_ranking(
    result: "dict[str, object]", report: Report
) -> "tuple[str, RankingRule] | tuple[None, None]":
    """Emit DSX-ADM-010 when the declared procedure resolved into its own
    candidate set and a cited pairwise ordering rule names another candidate
    as preferred over it.

    Citation: the four cited orderings' own sources, as they appear in
    ``references/families.yaml``'s ``ranking_rules:`` block --
    Delacre, Lakens and Leys (2017, together with the 2022 Correction) and
    Zimmerman (2004) for Welch over Student's t; Lydersen, Fagerland and
    Laake (2009) for Boschloo over Fisher's exact; MacKinnon, Nielsen and
    Webb (2023) for the CV3 wild-bootstrap-over-CV1 reliability ordering;
    Lin (2013) and Freedman (2008) for the interacted-adjustment ordering.
    The ranking rule table itself is data in that file, not a constant in
    this module -- this function never hand-transcribes a rule's condition,
    strength or citation into its own text.

    Structural criterion: fires when a declared ordering rule in the loaded
    ontology names another candidate family as preferred over the resolved
    one -- a set-membership test over the loaded rule table
    (``dominating_rules()``), with no statistic and no threshold computed
    here. Scoped to a cited pairwise rule and nothing else: the declared
    family merely sitting below another on the fewer-assumptions criterion
    or on the identifier tiebreak never fires this code, because the
    fewer-assumptions criterion is a statement about credibility rather than
    about efficiency and the tiebreak is an arbitrary but stable convention
    -- emitting a HIGH finding, which blocks at verify and ship, on either
    would overstate what the sources support.

    No published number is asserted as a ``Reference value:`` here. Brief
    D-02 forbids computing any test statistic on the gate path, so there is
    no number for a reference value to check against, and brief D-28's
    preference for a National Institute of Standards and Technology
    reference value applies to a computation this family deliberately does
    not perform. The published reference values that do exist for these
    estimators live in ``references/families.yaml``'s per-family ``notes:``,
    where the estimator they belong to is defined -- a later reader should
    not helpfully add one here.
    """
    if result["resolution"] != "in_candidate_set":
        return None, None

    resolved_family = result["resolved_family"]
    ontology = load_ontology()
    candidates = candidate_families(ontology, result["estimand"], result["dependence"])
    rules = dominating_rules(resolved_family, candidates, ontology.rules)
    if not rules:
        return None, None

    rule = rules[0]
    report.add(
        "DSX-ADM-010",
        "HIGH",
        "Declared procedure is admissible but a cited ordering prefers another family",
        detail=(
            f"Ranking rule {rule.id!r} (citation: {rule.citation}) states that "
            f"{rule.prefers!r} is preferred over {rule.over!r} when {rule.condition} "
            f"-- strength: {rule.strength}."
        ),
        remedy=(
            f"Prefer {rule.prefers!r} when {rule.condition} -- the declared "
            "procedure remains admissible, but this cited ordering ranks "
            "another family above it."
        ),
        where="spec.primary_procedure",
    )
    return "DSX-ADM-010", rule


def _check_no_admissible_procedure(
    result: "dict[str, object]", report: Report
) -> "str | None":
    """Emit DSX-ADM-020 for whichever of the three collapsed causes fired --
    a required axis blank or absent, the complete axis pair matching zero
    families, or a declared procedure label that resolves to no family in
    its own candidate set (including a label that resolves only outside it)
    -- one finding, never two.

    Citation: Manski, C.F. (2003), Partial Identification of Probability
    Distributions, Springer, Introduction, section "Partial Identification
    and Credible Inference" -- the credibility of an inference decreases with
    the strength of the assumptions maintained. Cited by named principle and
    section title, never by page: the statement is verified from the
    author's pre-publication manuscript and the typeset page number is not.

    Structural criterion: fires when the ranked admissible set is empty for
    any of the three collapsed causes, or when a declared label resolves to
    no family in the candidate set -- a membership test over data, with no
    statistic computed anywhere on this path.

    No published number is asserted as a ``Reference value:`` here, for the
    same reason recorded on ``_check_declared_procedure_ranking``: brief
    D-02 forbids computing any test statistic on the gate path, and brief
    D-28's National Institute of Standards and Technology preference applies
    to a computation this family deliberately does not perform. A later
    reader should not helpfully add one here.
    """
    if result["refusal"] != _REFUSAL:
        return None

    cause = result["refusal_cause"]
    estimand = result["estimand"]
    dependence = result["dependence"]
    declared = result["declared_procedure"]
    resolution_status = result["resolution"]
    resolved_family = result["resolved_family"]

    if cause == _CAUSE_BLANK_AXIS:
        if is_blank(estimand):
            where = "spec.validity_frame.estimand.type"
            detail = (
                "validity_frame.estimand.type is blank or absent, so no "
                "candidate family can be matched against this frame."
            )
        else:
            where = "spec.validity_frame.dependence.structure"
            detail = (
                "validity_frame.dependence.structure is blank or absent, so "
                "no candidate family can be matched against this frame."
            )
    elif cause == _CAUSE_NO_MATCHING_FAMILY:
        where = "spec.validity_frame"
        detail = (
            f"No family in the ontology declares the pair "
            f"(estimand={estimand!r}, dependence={dependence!r}); zero "
            "candidate families exist for this frame."
        )
    else:  # _CAUSE_UNRESOLVED
        where = "spec.primary_procedure"
        if resolution_status == "unresolved":
            detail = (
                f"The declared procedure {declared!r} does not match any "
                "known alias in the ontology; no nearest match was attempted."
            )
        else:  # outside_candidate_set
            detail = (
                f"The declared procedure {declared!r} resolved to family "
                f"{resolved_family!r}, which is outside this frame's own "
                f"candidate set (estimand={estimand!r}, dependence={dependence!r})."
            )

    report.add(
        "DSX-ADM-020",
        "CRITICAL",
        "No admissible procedure for the declared frame",
        detail=detail,
        remedy=(
            "Complete the frame's estimand type and dependence structure, or "
            "name a procedure the ontology recognises for this frame."
        ),
        where=where,
    )
    return "DSX-ADM-020"


def check(spec: dict, *, applies_to_frame: bool = True) -> Report:
    """Emit DSX-ADM-010 (HIGH) and DSX-ADM-020 (CRITICAL) -- the frequentist
    procedure admissibility adjudicator (REQ-P11-03, REQ-P11-04).

    ``applies_to_frame`` is a plain boolean handed in by the caller. The
    scoping decision this parameter answers -- whether this check family
    applies to a frequentist frame -- is computed entirely outside this
    module (``dsx/frame/paradigm.py::applies_to_frequentist_admissibility``)
    and never re-derived here. Defaults to ``True`` so a direct call
    carrying no scoping information behaves the same way that predicate
    itself widens on an undeclared or unrecognised school of inference:
    treated as in scope, never silently excused.

    Returns an empty ``Report``, with no finding and no decision record,
    when ``applies_to_frame`` is false or ``spec`` is not a mapping --
    matching every other frame check's degrade-not-raise habit for a
    malformed spec.

    Calls ``admissible_families(spec)`` exactly once and both private
    helpers read its returned dict; neither helper re-derives the ranked set
    or the resolution. Never calls ``report.ok(...)`` -- confirmed by grep
    that no module under ``dsx/frame/`` calls it; the clear path in every
    frame check is an empty finding list plus a decision record, and
    ``11-RESEARCH.md``'s description of ``report.ok`` as the frame
    convention does not match the tree.

    Appends exactly one ``DecisionRecord`` per call that got past the two
    guards above -- the first shipped use of both ``escalate`` and
    ``alternatives_rejected`` (D-17). ``escalate`` is set to ``True`` on
    every refusal path and left ``False`` otherwise: without it, ``dsx
    explain`` renders a refusal exactly like an ordinary deterministic
    choice, and the operator never learns the tool refused rather than
    decided. ``alternatives_rejected`` carries the ranked-but-not-top family
    ids, in rank order, whenever a ranked set exists.
    """
    report = Report(check="admissibility")

    if not applies_to_frame or not isinstance(spec, dict):
        return report

    result = admissible_families(spec)

    fired_code: "str | None" = None
    fired_rule: "RankingRule | None" = None
    if result["refusal"] == _REFUSAL:
        fired_code = _check_no_admissible_procedure(result, report)
    elif result["resolution"] == "in_candidate_set":
        fired_code, fired_rule = _check_declared_procedure_ranking(result, report)

    ranked_ids = [entry["id"] for entry in result["admissible"]]
    alternatives_rejected = ranked_ids[1:]

    if fired_code == "DSX-ADM-020":
        choice = f"DSX-ADM-020 fired: {result['refusal_cause']}"
        rule_text = (
            "DSX-ADM-020 fires when the ranked admissible set is empty for "
            "any of three collapsed causes (a blank required axis, zero "
            "matching families, or a declared procedure resolving to no "
            "family in its own candidate set), or when a declared label "
            "resolves only outside its own candidate set."
        )
        citation = (
            "Manski, C.F. (2003), Partial Identification of Probability "
            'Distributions, Springer, Introduction, section "Partial '
            'Identification and Credible Inference"'
        )
        counterfactual = (
            "Completing the blank axis, declaring axes that match a known "
            "family, or naming a procedure the ontology resolves into this "
            "frame's own candidate set would have cleared DSX-ADM-020."
        )
        escalate = True  # escalate=True on every DSX-ADM-020 refusal path (D-17)
    elif fired_code == "DSX-ADM-010":
        choice = (
            f"DSX-ADM-010 fired: {fired_rule.id} prefers {fired_rule.prefers!r} "
            f"over the declared {result['resolved_family']!r}"
        )
        rule_text = (
            "DSX-ADM-010 fires when a cited pairwise ordering rule in the "
            "ontology names another candidate family as preferred over the "
            "resolved one -- never on the fewer-assumptions criterion or "
            "the identifier tiebreak alone."
        )
        citation = fired_rule.citation
        counterfactual = (
            f"Declaring {fired_rule.prefers!r} instead of the resolved "
            "family would have cleared DSX-ADM-010."
        )
        escalate = False
    else:
        choice = (
            "DSX-ADM clear: the resolved procedure is not dominated by any "
            "cited ordering rule, and an admissible procedure exists for "
            "this frame"
            if result["admissible"]
            else "DSX-ADM clear: no candidate family exists to rank for "
            "this frame"
        )
        rule_text = (
            "DSX-ADM-010 fires only when a cited ordering rule prefers "
            "another candidate over the resolved one; DSX-ADM-020 fires "
            "only when the admissible set is empty or a declared label "
            "fails to resolve into its own candidate set. Neither "
            "condition holds here."
        )
        citation = ""
        counterfactual = (
            "An empty admissible set, an unresolved declared procedure, or "
            "a cited rule naming another family as preferred would have "
            "fired DSX-ADM-020 or DSX-ADM-010 instead."
        )
        escalate = False

    # First shipped use of DecisionRecord.escalate and alternatives_rejected
    # (D-17) -- see this function's own docstring for why escalate matters.
    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=choice,
            inputs=[
                "validity_frame.estimand.type",
                "validity_frame.dependence.structure",
                "the declared primary procedure field",
            ],
            rule=rule_text,
            citation=citation,
            counterfactual=counterfactual,
            alternatives_rejected=alternatives_rejected,
            escalate=escalate,
        ).to_dict()
    )

    return report
