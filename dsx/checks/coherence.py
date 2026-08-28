"""Question ↔ claim ↔ decision coherence. Codes DSX-COH-*.

The analytical question sets the ceiling on what the deliverable may claim, and
the decision block is what stops a result being re-interpreted after the fact.
These checks keep those three blocks from silently disagreeing.
"""

from __future__ import annotations

from ..findings import Report
from ..spec import (
    as_number,
    causal_verb_matches,
    get,
    is_blank,
    items,
    normalize,
    revisit_when_is_discriminating,
    section,
)

# Strength ladder: a claim may not exceed the question's strength.
# diagnostic and association sit at the same rung (within-sample attribution).
QUESTION_STRENGTH = {
    "descriptive": 0,
    "diagnostic": 1,
    "predictive": 2,
    "causal": 3,
    "prescriptive": 4,
}

CLAIM_STRENGTH = {
    "descriptive": 0,
    "association": 1,
    "predictive": 2,
    "causal": 3,
    "prescriptive": 4,
}


def check(spec: dict, *, strict: bool = False) -> Report:
    """Run coherence checks.

    ``strict=True`` (verify/ship) escalates empty assumptions on causal work to
    CRITICAL; plan uses the default HIGH so scaffolding can land before the
    assumption list is complete.
    """
    report = Report(check="coherence")
    qtype = normalize(str(get(spec, "question_type") or ""))
    _check_claim_ceiling(spec, qtype, report)
    _check_decision_language(spec, qtype, report)
    _check_experiment_decision(spec, report)
    _check_revisit_completeness(spec, qtype, report)
    _check_assumptions(spec, qtype, report, strict=strict)
    return report


def _check_claim_ceiling(spec: dict, qtype: str, report: Report) -> None:
    if not qtype or qtype not in QUESTION_STRENGTH:
        return
    q_strength = QUESTION_STRENGTH[qtype]
    for index, claim in enumerate(items(spec, "claims")):
        ctype = normalize(str(claim.get("type", "")))
        if ctype not in CLAIM_STRENGTH:
            continue
        c_strength = CLAIM_STRENGTH[ctype]
        if c_strength > q_strength:
            report.add(
                "DSX-COH-001",
                "CRITICAL",
                f"Claim type {ctype!r} exceeds question_type {qtype!r}",
                detail=(
                    f"Claim[{index}]: “{str(claim.get('text', ''))[:120]}”. "
                    "The question framing does not license this strength of claim."
                ),
                remedy=(
                    "Raise question_type to match the claim, or retype the claim "
                    "downward (e.g. causal → association)."
                ),
                where=f"spec.claims[{index}].type",
            )
        else:
            report.ok(f"claim[{index}] type {ctype} ≤ question {qtype}")


def _check_decision_language(spec: dict, qtype: str, report: Report) -> None:
    if qtype not in {"descriptive", "diagnostic"}:
        return
    decision = section(spec, "decision")
    rule = str(decision.get("decision_rule") or "")
    if is_blank(rule):
        return
    lowered = rule.lower()
    hits = causal_verb_matches(lowered)
    if hits:
        report.add(
            "DSX-COH-010",
            "CRITICAL",
            f"Decision rule uses causal language under question_type={qtype}",
            detail=(
                f"Matched: {', '.join(hits[:4])}. A {qtype} question cannot "
                "support a causal decision rule — either the question is causal "
                "or the rule is overclaiming."
            ),
            remedy=(
                "Set question_type to causal/prescriptive and declare an "
                "identification strategy, or rewrite the decision rule without "
                "causal verbs."
            ),
            where="spec.decision.decision_rule",
        )


def _check_experiment_decision(spec: dict, report: Report) -> None:
    design = section(spec, "design")
    if normalize(str(design.get("kind", ""))) != "experiment":
        return
    decision = section(spec, "decision")
    mpe = as_number(decision.get("minimum_practical_effect"))
    if mpe is None:
        report.add(
            "DSX-COH-020",
            "CRITICAL",
            "Experiment decision block incomplete (MPE or action_if_null)",
            detail=(
                "Sample size is meaningless without the smallest effect that "
                "would change the decision. Without it the experiment is sized "
                "by convenience."
            ),
            remedy="Set decision.minimum_practical_effect before locking planned_n_per_arm.",
            where="spec.decision.minimum_practical_effect",
        )
    if is_blank(decision.get("action_if_null")):
        report.add(
            "DSX-COH-020",
            "CRITICAL",
            "Experiment decision block incomplete (MPE or action_if_null)",
            detail=(
                "Without a pre-committed null action, a null result will be "
                "reframed as 'directionally positive' after the fact."
            ),
            remedy="Write what happens when no effect is detected, before results exist.",
            where="spec.decision.action_if_null",
        )
    if mpe is not None and not is_blank(decision.get("action_if_null")):
        report.ok("experiment decision block has MPE and action_if_null")


def _check_revisit_completeness(spec: dict, qtype: str, report: Report) -> None:
    """Emit DSX-COH-040 when a prescriptive question or an experiment design has
    no usable re-visit trigger declared.

    Citation: Nosek, B.A., Ebersole, C.R., DeHaven, A.C. & Mellor, D.T. (2018),
    "The preregistration revolution", Proceedings of the National Academy of
    Sciences 115(11):2600-2606, DOI 10.1073/pnas.1708274114 — locking a decision
    rule before data exist is what makes it checkable afterward; a re-visit
    trigger is the same discipline applied to when a locked recommendation may
    be reopened. D-16 candidate; unverified locator (no section/page confirmed)
    pending the human D-05 source read (HQ-3).

    Structural criterion: structural presence/absence of a discriminating,
    time-anchored re-open trigger (``revisit_when_is_discriminating()``) — no
    numeric threshold, effect size or statistic is computed anywhere on this
    path (D-02). A prescriptive question and an experiment design are two
    triggers of the SAME fact ("no usable re-visit trigger declared"); blank,
    placeholder and refusal-token declarations all collapse into it via the
    same predicate, and both triggers true fire exactly one finding.
    """
    design = section(spec, "design")
    is_experiment = normalize(str(design.get("kind", ""))) == "experiment"
    if qtype != "prescriptive" and not is_experiment:
        return
    decision = section(spec, "decision")
    revisit_when = decision.get("revisit_when")
    if revisit_when_is_discriminating(revisit_when):
        report.ok("decision.revisit_when is discriminating and window-anchored")
        return
    report.add(
        "DSX-COH-040",
        "CRITICAL",
        "decision.revisit_when is missing or not a usable re-visit trigger",
        detail=(
            f"Declared value: {revisit_when!r}. A prescriptive recommendation or "
            "an experiment needs a named metric, a threshold, and a time anchor "
            "for when the decision gets revisited — otherwise it is a permanent "
            "commitment made before the data."
        ),
        remedy=(
            "Write decision.revisit_when as a discriminating condition with a "
            "time anchor, e.g. 'activation_rate below +1.0pp at the 2026-Q4 "
            "review' or 'churn above 5% for 8 weeks'."
        ),
        where="spec.decision.revisit_when",
    )


def _check_assumptions(
    spec: dict, qtype: str, report: Report, *, strict: bool
) -> None:
    if qtype not in {"causal", "prescriptive"}:
        return
    assumptions = items(spec, "assumptions")
    if not assumptions:
        detail = (
            "Causal and prescriptive answers rest on assumptions. An empty list "
            "means none have been named, so none can be checked or waived."
        )
        remedy = (
            "Declare each material assumption with rationale and impact_if_wrong. "
            "Mark checked: true once tested, or record an explicit waiver."
        )
        if strict:
            report.add(
                "DSX-COH-030",
                "CRITICAL",
                "Causal/prescriptive question has an empty assumptions list",
                detail=detail,
                remedy=remedy,
                where="spec.assumptions",
            )
        else:
            report.add(
                "DSX-COH-030",
                "HIGH",
                "Causal/prescriptive question has an empty assumptions list",
                detail=detail,
                remedy=remedy,
                where="spec.assumptions",
            )
        return

    report.ok(f"{len(assumptions)} assumption(s) declared")
    if not strict:
        return

    for index, assumption in enumerate(assumptions):
        checked = assumption.get("checked") is True
        waiver = assumption.get("waiver")
        has_waiver = isinstance(waiver, str) and bool(waiver.strip())
        if checked or has_waiver:
            continue
        report.add(
            "DSX-COH-031",
            "HIGH",
            f"Assumption[{index}] is neither checked nor waived",
            detail=(
                f"“{str(assumption.get('assumption', ''))[:120]}”. "
                "At verify/ship every declared assumption needs checked: true or a "
                "non-blank waiver."
            ),
            remedy="Set checked: true after testing, or write waiver: with why it cannot be tested.",
            where=f"spec.assumptions[{index}]",
        )
