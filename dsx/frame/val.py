"""DSX-VAL-* — the validity-frame content checks (Phase 7).

Phase 6's ``_validate_validity_frame_shape`` (``dsx/spec.py``) already checks
*shape*: is the ``validity_frame:`` block present, is each required sub-block
present, does each closed-vocabulary sub-field hold a member of its
vocabulary. This module checks *content* of a sub-block that is present and
structurally well-formed: is the estimand it declares actually complete, and
is it actually falsifiable. Do not duplicate the shape checks here — a
missing sub-block is Phase 6's ``DSX-SPEC-080``/``DSX-SPEC-081`` territory,
and firing a ``DSX-VAL-*`` code on top of that would double-report a single
defect.

Two of the family's nine planned codes shipped in plan 07-03 (``DSX-VAL-010``,
``DSX-VAL-011``, both about the ``estimand`` sub-block). This plan (07-04)
adds two more: ``DSX-VAL-020`` (the unit triad — ``units.observation`` finer
than ``units.assignment`` with no method family declared) and
``DSX-VAL-021`` (unit drift — the validity frame's own unit declarations
disagreeing with ``design:``'s). Plans 07-05 and 07-06 add the remaining
five private helpers behind the same ``check()`` dispatcher — each new
helper is one call added to ``check()``, not a restructure.

D-11 (mechanically proven by ``tests/test_frame_boundary.py``'s
``TestFrameParadigmReadBoundary``): no code path in this module reads the
declared inference paradigm field, in any form — not through ``get()``, not
by direct dictionary indexing, not in a message string. A prior does not
save an analysis from pseudo-replication; a check that branches on the
declared paradigm is in the wrong layer.
"""

from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..mathx import design_effect
from ..spec import (
    falsifier_is_discriminating,
    get,
    is_blank,
    is_placeholder_or_refusal,
    normalize,
)

# The four estimand attributes DSX-VAL-010 requires present. `falsifier` is
# deliberately excluded — it routes entirely through DSX-VAL-011
# (_check_estimand_falsifiability), so a blank falsifier fires exactly one
# code, not two (D-05, disambiguating D-02 and D-05 read together).
_ESTIMAND_REQUIRED_FIELDS: "tuple[str, ...]" = (
    "quantity",
    "population",
    "contrast",
    "time_window",
)

_ESTIMAND_CITATION = (
    "International Council for Harmonisation (ICH) (2019), E9(R1) Addendum, "
    "EMA/CHMP/ICH/436221/2017, Step 5, section A.3.3 (\"Estimand attributes\") "
    "and section A.3.2; Hernan, M.A. & Robins, J.M. (2016), American Journal of "
    "Epidemiology 183(8):758-764, Table 1; Popper, K.R. (1959/2002 reissue), "
    "The Logic of Scientific Discovery, Part I, Chapter 1, section 6"
)

# The design-effect illustration inputs (D-10, D-11): the Cochrane Handbook's
# own worked example, not derived from any spec field — the contract has no
# cluster-size or intraclass-correlation field anywhere to derive one from.
_UNIT_TRIAD_ICC = 0.02
_UNIT_TRIAD_M = 29.8

_UNIT_TRIAD_CITATION = (
    "Kish, L. (1965), Survey Sampling, section 8.2, page 258 (design-effect "
    "definition) and pages 161-162 (intraclass correlation); Higgins, J.P.T., "
    "Eldridge, S. and Li, T. (2024), Cochrane Handbook for Systematic Reviews "
    "of Interventions version 6.5, sections 23.1.4 and 23.1.4.1. The section "
    "number inside Kish for the design-effect formula itself is UNVERIFIED — "
    "only the page numbers above were confirmed; do not invent one."
)

_UNIT_DRIFT_CITATION = (
    "Hernan, M.A. & Robins, J.M. (2020), Causal Inference: What If, Chapter 1, "
    "section 1.2 (\"Average causal effects\")"
)


def check(spec: dict) -> Report:
    """Emit the validity-frame content findings (``DSX-VAL-*``).

    Reads ``validity_frame:`` and degrades to an empty report — never a
    traceback — when the block is absent or is not a dictionary (threat
    T-7-01: a malformed sub-block must not take the whole gate down). This is
    deliberately distinct from Phase 6's shape check: an absent block is
    already ``DSX-SPEC-080`` territory, so this function does not re-report
    it.

    Structural criterion: dispatches to one private helper per adjudicated
    concept; no numeric threshold, effect size or statistic is computed
    anywhere in this module (D-02).
    """
    report = Report(check="val")

    frame = get(spec, "validity_frame")
    if not isinstance(frame, dict):
        return report

    _check_estimand_completeness(frame, report)
    _check_estimand_falsifiability(frame, report)
    _check_unit_triad(spec, frame, report)
    _check_unit_drift(spec, frame, report)

    estimand = frame.get("estimand")
    if isinstance(estimand, dict):
        blank_fields = [
            name for name in _ESTIMAND_REQUIRED_FIELDS if is_blank(estimand.get(name))
        ]
        discriminating = falsifier_is_discriminating(estimand.get("falsifier"))
        choice = (
            "estimand completeness: "
            + ("blocked" if blank_fields else "passed")
            + "; estimand falsifiability: "
            + ("passed" if discriminating else "blocked")
        )
        counterfactual = (
            "A declaration with quantity, population, contrast and time_window all "
            "present, and a falsifier naming a discriminating predicate or a numeric "
            "threshold, would have produced neither DSX-VAL-010 nor DSX-VAL-011."
        )
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice=choice,
                inputs=[
                    f"validity_frame.estimand.{name}"
                    for name in (*_ESTIMAND_REQUIRED_FIELDS, "falsifier")
                ],
                rule=(
                    "DSX-VAL-010 fires when any of quantity, population, contrast or "
                    "time_window is blank under is_blank(); DSX-VAL-011 fires when "
                    "falsifier_is_discriminating(falsifier) is False — blank, an "
                    "angle-bracket placeholder, a refusal token, or prose naming no "
                    "discriminating predicate and no numeric/percentage-point token."
                ),
                citation=_ESTIMAND_CITATION,
                counterfactual=counterfactual,
            ).to_dict()
        )

    units = frame.get("units")
    if isinstance(units, dict):
        observation = units.get("observation")
        assignment = units.get("assignment")
        dependence = frame.get("dependence")
        method_family = (
            dependence.get("method_family_required") if isinstance(dependence, dict) else None
        )
        triad_blocked = (
            not is_blank(observation)
            and not is_blank(assignment)
            and normalize(observation) != normalize(assignment)
            and is_blank(method_family)
        )
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice="unit triad: " + ("blocked" if triad_blocked else "passed"),
                inputs=[
                    "validity_frame.units.observation",
                    "validity_frame.units.assignment",
                    "validity_frame.dependence.method_family_required",
                ],
                rule=(
                    "DSX-VAL-020 fires when normalize(units.observation) != "
                    "normalize(units.assignment) and dependence.method_family_required is "
                    "blank under is_blank(); either unit being blank skips the comparison."
                ),
                citation=_UNIT_TRIAD_CITATION,
                counterfactual=(
                    "A spec where the observation unit equals the assignment unit, or "
                    "where dependence.method_family_required names an admissible method "
                    "family, would have produced no DSX-VAL-020."
                ),
            ).to_dict()
        )

        design = spec.get("design")
        design = design if isinstance(design, dict) else {}
        assignment_for_drift = units.get("assignment")
        analysis = units.get("analysis")
        randomization_unit = design.get("randomization_unit")
        design_analysis_unit = design.get("analysis_unit")
        drift_blocked = (
            not is_blank(assignment_for_drift)
            and not is_blank(randomization_unit)
            and normalize(assignment_for_drift) != normalize(randomization_unit)
        ) or (
            not is_blank(analysis)
            and not is_blank(design_analysis_unit)
            and normalize(analysis) != normalize(design_analysis_unit)
        )
        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice="unit drift: " + ("blocked" if drift_blocked else "passed"),
                inputs=[
                    "validity_frame.units.assignment",
                    "design.randomization_unit",
                    "validity_frame.units.analysis",
                    "design.analysis_unit",
                ],
                rule=(
                    "DSX-VAL-021 fires once per disagreeing pair: "
                    "normalize(units.assignment) != normalize(design.randomization_unit), "
                    "or normalize(units.analysis) != normalize(design.analysis_unit); each "
                    "comparison is skipped unless both of its sides are non-blank."
                ),
                citation=_UNIT_DRIFT_CITATION,
                counterfactual=(
                    "A spec where the validity frame's assignment and analysis units "
                    "agree with design.randomization_unit and design.analysis_unit "
                    "respectively would have produced no DSX-VAL-021."
                ),
            ).to_dict()
        )

    return report


def _check_estimand_completeness(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-010 when a required estimand attribute is blank.

    Citation: International Council for Harmonisation (ICH) (2019), E9(R1)
    Addendum, EMA/CHMP/ICH/436221/2017, Step 5, section A.3.3 ("Estimand
    attributes") and section A.3.2; Hernan, M.A. & Robins, J.M. (2016),
    American Journal of Epidemiology 183(8):758-764, Table 1; Hernan, M.A. &
    Robins, J.M. (2020), Causal Inference: What If, Chapter 1, section 1.2
    ("Average causal effects").

    Honesty disclosure (D-05's whole point): the five-field estimand
    decomposition this module uses (quantity, population, contrast,
    time_window, falsifier) is project-defined. The addendum and Hernan and
    Robins (2016) each name four of the five attributes checked here, but
    neither treats ``falsifier`` as an estimand attribute at all, and
    ``time_window`` appears in the addendum as a sub-specification of the
    estimand rather than as one of its named attributes. No cited source
    states this five-field decomposition as written; it is this project's own
    grouping, adopted for decidability, not asserted as a published result.

    Structural criterion: presence (non-blank, per ``is_blank()``) of the
    four required sub-fields quantity, population, contrast and time_window.
    ``falsifier`` is intentionally excluded from this criterion — it is
    adjudicated separately by ``_check_estimand_falsifiability`` (DSX-VAL-011)
    so a blank falsifier fires exactly one code, not two.
    """
    estimand = frame.get("estimand")
    if not isinstance(estimand, dict):
        return

    blank_fields = [
        name for name in _ESTIMAND_REQUIRED_FIELDS if is_blank(estimand.get(name))
    ]
    if not blank_fields:
        return

    detail = (
        "Blank estimand attribute(s): "
        + ", ".join(blank_fields)
        + ". A blank falsifier is not counted here — see DSX-VAL-011."
    )
    remedy = (
        "Name all four attributes: quantity (the difference, rate or quantity being "
        "estimated, e.g. 'difference in 7-day activation rate'), population (who the "
        "estimate covers, e.g. 'new non-bot signups, 2026-06-01 to 2026-06-14'), "
        "contrast (what is being compared, e.g. 'onboarding checklist vs current "
        "onboarding'), and time_window (the period over which the effect is measured, "
        "e.g. '7 days from signup')."
    )
    report.add(
        "DSX-VAL-010",
        "CRITICAL",
        "estimand is missing required attribute(s)",
        detail=detail,
        remedy=remedy,
        where="spec.validity_frame.estimand",
    )


def _check_estimand_falsifiability(frame: dict, report: Report) -> None:
    """Emit DSX-VAL-011 when the estimand's falsifier does not discriminate.

    Citation: Popper, K.R. (1959/2002 reissue), The Logic of Scientific
    Discovery, Part I, Chapter 1, section 6 ("Falsifiability as a Criterion
    of Demarcation"), pages 17-18.
    Structural criterion: the falsifier must name at least one observable
    outcome under which the claim is withdrawn — tested via
    ``falsifier_is_discriminating()``, which requires a comparison predicate
    (``FALSIFIER_DISCRIMINATORS``) or a numeric/percentage-point token, and
    is False for a blank, angle-bracket-placeholder or refusal-token value.
    """
    estimand = frame.get("estimand")
    if not isinstance(estimand, dict):
        return

    falsifier = estimand.get("falsifier")
    if falsifier_is_discriminating(falsifier):
        return

    if is_placeholder_or_refusal(falsifier):
        detail = (
            f"falsifier {falsifier!r} is blank, an angle-bracket placeholder, or a "
            "refusal token — no honest falsifier was declared."
        )
    else:
        detail = (
            f"falsifier {falsifier!r} is present but names no discriminating predicate "
            "(e.g. 'includes zero', 'crosses', 'below', 'above', 'exceeds') and no "
            "numeric or percentage-point threshold."
        )
    remedy = (
        "Name at least one observable outcome under which the claim would be "
        "withdrawn — a discriminating predicate plus a numeric threshold, in the "
        "shape of the good fixture's falsifier: '95% CI on the activation uplift "
        "includes zero, or its lower bound sits below +1.0pp'."
    )
    report.add(
        "DSX-VAL-011",
        "HIGH",
        "estimand falsifier does not discriminate",
        detail=detail,
        remedy=remedy,
        where="spec.validity_frame.estimand.falsifier",
    )


def _check_unit_triad(spec: dict, frame: dict, report: Report) -> None:
    """Emit DSX-VAL-020 when the observation unit is finer than the
    assignment unit and no method family accounts for the resulting
    dependence.

    Citation: Kish, L. (1965), Survey Sampling, section 8.2, page 258
    (design-effect definition) and pages 161-162 (intraclass correlation);
    Higgins, J.P.T., Eldridge, S. and Li, T. (2024), Cochrane Handbook for
    Systematic Reviews of Interventions version 6.5, sections 23.1.4 and
    23.1.4.1. The section number inside Kish for the design-effect formula
    itself is UNVERIFIED — only the page numbers above were confirmed; do not
    invent one.

    The number this function prints (the Cochrane Handbook's own worked
    example: an intraclass correlation of 0.02 and an average cluster size of
    29.8 yielding 1.576) is a fixed illustration, never a figure computed
    from this spec. The contract carries no cluster-size field and no
    intraclass-correlation field anywhere (D-11), and D-02 forbids computing
    a statistic on the gate path in any case — the gate has nothing to
    compute from even if it wanted to.

    Structural criterion: normalize(units.observation) != normalize(units.assignment)
    (D-08 — plain string inequality, deliberate: the units fields carry no
    closed, orderable vocabulary in this contract, so an ordering that could
    rank one unit finer than another would have to be invented) with
    dependence.method_family_required blank under is_blank(). Either unit
    being blank skips the comparison entirely — a blank unit is Phase 6's
    shape territory, not this check's.

    Known risk, accepted (D-08): a spec naming the same unit two ways (e.g.
    'user' vs 'user_id') fires this at CRITICAL on a naming inconsistency,
    not a true dependence defect. The remedy names both ways out so an
    author hitting this can tell which one applies.
    """
    units = frame.get("units")
    if not isinstance(units, dict):
        return

    observation = units.get("observation")
    assignment = units.get("assignment")
    if is_blank(observation) or is_blank(assignment):
        return
    if normalize(observation) == normalize(assignment):
        return

    dependence = frame.get("dependence")
    method_family = (
        dependence.get("method_family_required") if isinstance(dependence, dict) else None
    )
    if not is_blank(method_family):
        return

    deff = design_effect(_UNIT_TRIAD_M, _UNIT_TRIAD_ICC)
    detail = (
        f"observation unit {observation!r} is finer than assignment unit {assignment!r}, "
        "with no validity_frame.dependence.method_family_required declared. Observations "
        "sharing an assignment unit are correlated with one another; treating the finer "
        "observation unit as independent understates variance. The design effect "
        "DEFF = 1 + (m - 1) x ICC quantifies the inflation: an intraclass correlation of "
        f"{_UNIT_TRIAD_ICC} and an average cluster size of {_UNIT_TRIAD_M} yield "
        f"DEFF = {deff:g} (dsx.mathx.design_effect({_UNIT_TRIAD_M}, {_UNIT_TRIAD_ICC})), "
        "so the true standard error is roughly sqrt(DEFF) times the naive one and an "
        "interval computed at the naive standard error is too narrow by that same factor. "
        "This number is a fixed illustration from the Cochrane Handbook's own published "
        "worked example — it is not computed from this spec. The contract carries no "
        "cluster-size or intraclass-correlation field anywhere, so there is nothing here "
        "to compute your own design effect from."
    )
    remedy = (
        "Either align the two unit names if they denote the same thing — a naming "
        f"inconsistency between {observation!r} and {assignment!r} (e.g. 'user' vs "
        "'user_id') also fires this finding — or declare "
        "validity_frame.dependence.method_family_required (cluster_robust, delta_method, "
        "bootstrap_cluster, or mixed_effects) to account for the dependence between them."
    )
    report.add(
        "DSX-VAL-020",
        "CRITICAL",
        "observation unit finer than assignment unit with no method family declared",
        detail=detail,
        remedy=remedy,
        where="spec.validity_frame.units",
    )


def _check_unit_drift(spec: dict, frame: dict, report: Report) -> None:
    """Emit DSX-VAL-021 when the validity frame's own unit declarations
    disagree with ``design:``'s.

    Citation: Hernan, M.A. & Robins, J.M. (2020), Causal Inference: What If,
    Chapter 1, section 1.2 ("Average causal effects") — the unit a claim is
    made about must be fixed before the claim is made.

    Structural criterion: string agreement (after ``normalize()``) between
    two declarations of the same unit across two blocks — no ordering, no
    ranking, no judgment of whether a mismatch is handled. Two comparisons,
    and nothing else: ``validity_frame.units.assignment`` against
    ``design.randomization_unit``, and ``validity_frame.units.analysis``
    against ``design.analysis_unit``. Each comparison is skipped unless both
    of its sides are non-blank — there is nothing to disagree with when one
    side is undeclared.

    This is pure agreement detection between two blocks (D-09), and that is
    the whole of its job. It does not assess whether a mismatch is handled —
    that judgment belongs to ``DSX-EXP-021`` (``dsx/checks/design.py``) for
    the design block's own randomization/analysis pair, and to
    ``DSX-VAL-020`` for the validity frame's own observation/assignment
    pair. No suppression logic connects this check to either of those —
    the disjointness is achieved by reading disjoint field pairs, not by one
    check silencing another.
    """
    units = frame.get("units")
    if not isinstance(units, dict):
        return

    design = spec.get("design")
    design = design if isinstance(design, dict) else {}

    assignment = units.get("assignment")
    randomization_unit = design.get("randomization_unit")
    if (
        not is_blank(assignment)
        and not is_blank(randomization_unit)
        and normalize(assignment) != normalize(randomization_unit)
    ):
        report.add(
            "DSX-VAL-021",
            "HIGH",
            "validity frame assignment unit disagrees with design randomization unit",
            detail=(
                f"validity_frame.units.assignment is {assignment!r}, but "
                f"design.randomization_unit is {randomization_unit!r} — the two "
                "declarations of the assignment unit disagree."
            ),
            remedy=(
                "Align validity_frame.units.assignment and design.randomization_unit to "
                "name the same unit; this check cannot know which declaration is right."
            ),
            where="spec.validity_frame.units.assignment",
        )

    analysis = units.get("analysis")
    design_analysis_unit = design.get("analysis_unit")
    if (
        not is_blank(analysis)
        and not is_blank(design_analysis_unit)
        and normalize(analysis) != normalize(design_analysis_unit)
    ):
        report.add(
            "DSX-VAL-021",
            "HIGH",
            "validity frame analysis unit disagrees with design analysis unit",
            detail=(
                f"validity_frame.units.analysis is {analysis!r}, but "
                f"design.analysis_unit is {design_analysis_unit!r} — the two "
                "declarations of the analysis unit disagree."
            ),
            remedy=(
                "Align validity_frame.units.analysis and design.analysis_unit to name "
                "the same unit; this check cannot know which declaration is right."
            ),
            where="spec.validity_frame.units.analysis",
        )
