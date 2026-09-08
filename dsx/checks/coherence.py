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
    _check_subgroup_harm_disposition(spec, qtype, report)
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


def _sign(value: float) -> int:
    """Sign convention reused verbatim from metrics.py:352-353 — never recomputed
    or diverged, so ``harmed(S)`` here means exactly what an opposing segment means
    to ``_check_simpsons_paradox``."""
    return (value > 0) - (value < 0)


def _ci_excludes_zero(ci: object) -> bool:
    """Latent OR-arm of the harm trigger (D-29 trigger predicate).

    A declared two-bound interval excludes zero when both bounds share a non-zero
    sign. results.segments[] carries no ``ci`` field on today's schema
    (templates/ANALYSIS-SPEC.yaml:260 is ``[{ name, effect, n }]``), so this arm is
    written in to honour the scope's OR but never bites until the segment schema
    gains a ``ci`` — the ``n >= floor`` arm is the one that fires today.
    """
    if not isinstance(ci, (list, tuple)) or len(ci) != 2:
        return False
    lo = as_number(ci[0])
    hi = as_number(ci[1])
    if lo is None or hi is None:
        return False
    return _sign(lo) == _sign(hi) and _sign(lo) != 0


def _check_subgroup_harm_disposition(spec: dict, qtype: str, report: Report) -> None:
    """Emit DSX-COH-041 when a prescriptive recommendation leaves a declared,
    opposite-sign minority segment above the disposition floor without a matching
    ``decision.subgroup_harm[]`` row (CRITICAL), or with an ``accept`` row whose
    rationale is blank (HIGH).

    Citation: Gail, M. & Simon, R. (1985), "Testing for qualitative interactions
    between treatment effects and patient subsets", Biometrics 41(2):361-372, PMID
    4027319 — the MOTIVATING DEFINITION only: a qualitative (crossover) interaction
    is treatment effects of opposite sign across subsets, which is precisely when a
    segment counts as *harmed* relative to a recommendation's premised direction.
    Gail & Simon describe a formal likelihood-ratio TEST for qualitative
    interaction; this check runs NO such test and computes NO statistic on the gate
    path (D-02). It does not cite Gail & Simon as authority for the enforcement
    mechanic — only for the definition of when a declared segment is harmed.

    Structural criterion: a pure structural read of declared fields — a
    ``results.segments[]`` entry whose declared ``effect`` opposes
    ``results.overall_effect`` by ``_sign`` (metrics.py:352-353, reused verbatim)
    AND whose declared ``n >= decision.subgroup_harm_floor`` (default 0) must carry
    a ``decision.subgroup_harm[]`` row matched by ``segment`` name. No threshold,
    interval, or statistic is computed here; the obligation is enforced as a
    declaration, the DSX-COH-040 mould applied to subgroup harm.

    Bounded catch: this buys attribution over HONESTLY-DECLARED segments, not
    detection of hidden harm. A spec that omits the harmed segment, lies about its
    sign, or declares a gamed floor above the segment's n still passes — the catch
    is "you declared a harmed segment above the floor and failed to disposition it",
    never "you have a harmed subgroup".
    """
    if qtype != "prescriptive":
        return
    results = section(spec, "results")
    overall = as_number(results.get("overall_effect"))
    segments = items(results, "segments")
    if overall is None or len(segments) < 2:
        return
    overall_sign = _sign(overall)
    if overall_sign == 0:
        return

    decision = section(spec, "decision")
    floor = as_number(decision.get("subgroup_harm_floor"))
    if floor is None:
        floor = 0.0

    rows_by_segment: dict[str, dict] = {}
    for row in items(decision, "subgroup_harm"):
        rows_by_segment[normalize(str(row.get("segment", "")))] = row

    for segment in segments:
        effect = as_number(segment.get("effect"))
        if effect is None or _sign(effect) != -overall_sign:
            continue  # only opposite-sign segments are candidates
        n = as_number(segment.get("n"))
        above_floor = n is not None and n >= floor
        if not (above_floor or _ci_excludes_zero(segment.get("ci"))):
            continue
        name = str(segment.get("name", "?"))
        row = rows_by_segment.get(normalize(name))
        if row is None:
            report.add(
                "DSX-COH-041",
                "CRITICAL",
                f"Opposing segment {name!r} above the disposition floor carries no "
                "decision.subgroup_harm[] row",
                detail=(
                    f"Segment {name!r} moves {effect:+.6g} against the {overall:+.6g} "
                    "aggregate this prescriptive recommendation rolls out, at declared "
                    f"n={segment.get('n')} (floor {floor:g}). A recommendation to act on "
                    "the aggregate while a declared minority is harmed must state what "
                    "happens to that minority."
                ),
                remedy=(
                    "Add a decision.subgroup_harm[] row for this segment with a "
                    "disposition (accept | exclude | mitigate) and, for accept, a "
                    "rationale — or declare a subgroup_harm_floor above its n and defend "
                    "why the cut is too small to act on."
                ),
                where="spec.decision.subgroup_harm",
            )
        elif normalize(str(row.get("disposition", ""))) == "accept" and is_blank(
            row.get("rationale")
        ):
            report.add(
                "DSX-COH-041",
                "HIGH",
                f"decision.subgroup_harm[] accepts harm to {name!r} without a rationale",
                detail=(
                    f"Segment {name!r} opposes the aggregate at {effect:+.6g} and its "
                    "row disposition is 'accept', but the rationale is blank. An accept "
                    "is the one disposition that proceeds despite the harm; it needs a "
                    "stated justification a reviewer can challenge."
                ),
                remedy=(
                    "Write decision.subgroup_harm[].rationale for this accept row, or "
                    "change the disposition to exclude/mitigate."
                ),
                where="spec.decision.subgroup_harm",
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
