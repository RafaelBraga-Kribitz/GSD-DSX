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

Two of the family's nine planned codes ship in this plan (``DSX-VAL-010``,
``DSX-VAL-011``, both about the ``estimand`` sub-block). Plans 07-04, 07-05
and 07-06 add the remaining seven private helpers behind the same ``check()``
dispatcher — each new helper is one call added to ``check()``, not a
restructure.

D-11 (mechanically proven by ``tests/test_frame_boundary.py``'s
``TestFrameParadigmReadBoundary``): no code path in this module reads
``inference.paradigm``, in any form — not through ``get()``, not by direct
dictionary indexing, not in a message string. A prior does not save an
analysis from pseudo-replication; a check that branches on the declared
paradigm is in the wrong layer.
"""

from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
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
