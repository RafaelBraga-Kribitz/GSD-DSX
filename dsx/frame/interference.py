"""DSX-INT-* — interference, triggering and stability (Phase 8).

This module adjudicates ``validity_frame.interference``: is a declared
interference/SUTVA risk actually addressed. Phase 6's
``_validate_validity_frame_shape`` (``dsx/spec.py``) already owns shape — is
the ``interference:`` sub-block present, is each field a member of its closed
vocabulary. A missing sub-block is ``DSX-SPEC-080``/``DSX-SPEC-081``
territory, never a ``DSX-INT-*`` finding; firing here on top of that would
double-report a single defect.

All four of the family's codes ship as of this plan: ``DSX-INT-010`` (a
declared risk with no mitigation and no real residual note), ``DSX-INT-011``
(a declared mitigation that is not admissible for the declared risk),
``DSX-INT-030`` (an additive metric analysed on the eligible population with
no declared dilution adjustment), and ``DSX-INT-040`` (a declared novelty or
primacy assessment that was never carried out, or was carried out with no
evidence pointer). ``DSX-INT-040`` is the family's only non-CRITICAL code —
HIGH, blocking from ``verify`` and ``ship`` but not ``plan`` — by severity
alone; no ``GATE_THRESHOLDS`` edit accompanies it.

D-11/D-16 (mechanically proven by ``tests/test_frame_boundary.py``'s
``TestFrameParadigmReadBoundary``): no code path in this module reads the
declared inference paradigm field, in any form — not through the dotted-path
helper, not by direct dictionary indexing, and not in a message string. A
prior does not save an analysis from an unaddressed SUTVA violation; a check
that branches on the declared paradigm is in the wrong layer.
"""

from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..spec import (
    INTERFERENCE_MITIGATIONS,
    INTERFERENCE_RISKS,
    METRIC_TYPES,
    get,
    is_blank,
    is_placeholder_or_refusal,
    items,
    needs_causal_block,
    normalize,
    section,
)

# The risk-to-mitigation admissibility map (D-05, D-07): a capability matrix, not a
# vocabulary — mirrors _PARADIGM_CONDITIONAL (dsx/frame/paradigm.py), including the
# set-equality-with-INTERFERENCE_RISKS contract test in tests/test_frame_interference.py.
# Keyed by every member of dsx.spec.INTERFERENCE_RISKS so a future vocabulary addition
# without a matching cell fails loudly rather than silently under-reporting.
#
# The structural criterion (D-06): a mitigation is admissible only where it operates on
# the same interference channel the risk names. This mapping is NOT a printed table from
# any cited source — Kohavi, Tang & Xu (2020) Chapter 22 was verified for the EXISTENCE
# AND NAMING of the technique set only (publisher index, not the unreachable running
# text); no cell below is quoted from the book. Two facts from that verified index, not
# papered over: "modelled" has no index entry at all — it is not a book-named technique,
# so every "modelled" cell rests on the structural criterion alone, never a citation; and
# the book names a fifth technique the vocabulary omits, "network egocentric
# randomization" (page 233) — noted here, not added, because a vocabulary member is
# contract surface this phase is not scoped for.
_RISK_MITIGATION_MAP: "dict[str, frozenset[str]]" = {
    # The check short-circuits before consulting this cell (see the "none" guard in
    # both helpers below); the empty set documents that "none" grants no mitigation
    # any special status, it is simply never reached.
    "none": frozenset(),
    # Channel: a shared, capacity-limited pool.
    "shared_budget": frozenset(
        {
            "budget_isolation",  # separate, non-competing budgets remove the pool itself
            "time_split",  # arms are never concurrent, so there is no shared window to compete over
            "modelled",  # the interference is estimated and adjusted for statistically, same channel
        }
    ),
    # Channel: the matching/auction mechanism through which one side's treatment moves
    # the other side's outcomes.
    "marketplace": frozenset(
        {
            "cluster_randomisation",  # randomising whole market segments keeps both sides of an interaction inside one arm
            "geo_split",  # a local market is the natural cluster when the market is geographic
            "time_split",  # the two sides of the market never meet across arms
            "modelled",  # the interference is estimated and adjusted for statistically
        }
    ),
    # Channel: geographic adjacency.
    "geo_spillover": frozenset(
        {
            "geo_split",  # directly contains the leakage at its own grain
            "cluster_randomisation",  # a geography is a cluster; clustering at or above the leakage scale contains it
            "modelled",  # the interference is estimated and adjusted for statistically
        }
    ),
    # Channel: the edges of a social or referral graph.
    "social_graph": frozenset(
        {
            "cluster_randomisation",  # graph communities as clusters keep edges inside one arm
            "modelled",  # the interference is estimated and adjusted for statistically
        }
    ),
    # Channel: a shared, finite stock.
    "shared_inventory": frozenset(
        {
            # the vocabulary's only primitive for splitting a shared pool per arm; applies to
            # an inventory pool as much as a budget
            "budget_isolation",
            "time_split",  # arms never draw concurrently
            "cluster_randomisation",  # clustering at the inventory-pool grain (e.g. a warehouse) contains the draw
            "modelled",  # the interference is estimated and adjusted for statistically
        }
    ),
}

# A partition over dsx.spec.METRIC_TYPES (D-11), not a parallel metric vocabulary — the
# split-vocabulary pattern decisions M-02 and M-09 already rejected for this codebase.
# _ADDITIVE_METRIC_TYPES is the set DSX-INT-030 adjudicates: a metric of one of these
# types, analysed on the eligible population with no declared dilution adjustment,
# reports an effect diluted toward zero by the untriggered share (Deng & Hu 2015,
# Formula (1)). _RATIO_METRIC_TYPES — ratio and rate — is explicitly OUT OF SCOPE for
# this milestone under REQ-P8-04: Deng & Hu's ratio-metric equation (Formula (3), §3.3)
# sums over individual users and has no closed-form scalar multiplier, so it cannot be
# evaluated from a declaration alone (see brief.md §6.5's ratio-metric dilution row).
# percentile and index are in neither set and are therefore unadjudicated by
# DSX-INT-030 — not swept into either bucket by default (D-11; decision D-11 in
# 08-CONTEXT.md is explicit that this silence is deliberate). Neither constant is
# registered in dsx.spec._VOCABULARIES, for the same reason DEPENDENCE_ADMISSIBLE_METHODS
# is not: each references an existing vocabulary's members rather than defining new ones.
_ADDITIVE_METRIC_TYPES: "frozenset[str]" = frozenset({"count", "sum", "average"})
_RATIO_METRIC_TYPES: "frozenset[str]" = frozenset({"ratio", "rate"})


def _check_interference_unaddressed(frame: dict, report: Report) -> None:
    """Emit DSX-INT-010 when a declared interference risk has no mitigation and no
    real residual note.

    Fires when ``validity_frame.interference.risk`` is a member of
    ``dsx.spec.INTERFERENCE_RISKS`` other than ``none``, the declared
    ``mitigation`` is ``none`` or absent, and ``residual_note`` is blank, an
    angle-bracket placeholder, or a refusal token
    (``is_placeholder_or_refusal()``). A declared, non-``none`` mitigation
    routes to ``_check_interference_mitigation_admissibility`` (DSX-INT-011)
    instead — the two codes are disjoint by construction: this one requires
    the absence of a declared mitigation, that one requires its presence
    (proven by Test 6 in ``tests/test_frame_interference.py``).

    Citation: Imbens, G.W. and Rubin, D.B. (2015), *Causal Inference for
    Statistics, Social, and Biomedical Sciences*, Cambridge University Press,
    section 1.6, Assumption 1.1, page 10, with sub-sections 1.6.1 "SUTVA: No
    Interference" at pages 10 to 11 and 1.6.2 "SUTVA: No Hidden Variations of
    Treatments" at pages 11 to 12. Assumption 1.1, quoted verbatim: "The
    potential outcomes for any unit do not vary with the treatments assigned
    to other units, and, for each unit, there are no different forms or
    versions of each treatment level, which lead to different potential
    outcomes." The book's own sub-section heading says "Variations", not
    "versions", even though the assumption's own text uses "versions" — the
    heading is what is commonly misquoted.
    Structural criterion: a declared interference risk other than none, with
    no mitigation applied and no non-placeholder residual note, asserts the
    stable-unit-treatment-value assumption by silence rather than by
    argument.
    """
    risk = get(frame, "interference.risk")
    normalized_risk = normalize(risk) if not is_blank(risk) else "none"
    if normalized_risk == "none" or normalized_risk not in INTERFERENCE_RISKS:
        # DSX-SPEC-082 territory (out-of-vocabulary) or the honestly-declared
        # no-risk case; either way there is nothing for this check to judge.
        return

    # Judgment point: a real, recognised interference risk is declared.
    mitigation = get(frame, "interference.mitigation")
    residual_note = get(frame, "interference.residual_note")
    normalized_mitigation = normalize(mitigation) if not is_blank(mitigation) else "none"
    mitigation_absent = normalized_mitigation == "none"
    residual_missing = is_placeholder_or_refusal(residual_note)
    unaddressed = mitigation_absent and residual_missing

    if unaddressed:
        admissible_listed = ", ".join(sorted(_RISK_MITIGATION_MAP.get(normalized_risk, ())))
        report.add(
            "DSX-INT-010",
            "CRITICAL",
            f"interference risk {normalized_risk} declared with no mitigation and no residual note",
            detail=(
                f"validity_frame.interference.risk is {risk!r} with mitigation "
                f"{mitigation!r} and residual_note {residual_note!r}. Neither escape "
                "is present: no mitigation admissible for this risk was declared, "
                "and no non-placeholder residual note explains what remains "
                "unaddressed. A declared interference risk with no design-level "
                "answer and no honest acknowledgement asserts SUTVA by silence."
            ),
            remedy=(
                "Declare a mitigation admissible for the declared risk — for "
                f"{normalized_risk!r}, one of: {admissible_listed or '(none admissible)'} "
                "— or write a residual_note stating plainly what interference "
                "remains unaddressed and why it is accepted."
            ),
            where="spec.validity_frame.interference.mitigation",
        )

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                f"DSX-INT-010 {'fired' if unaddressed else 'clear'}: "
                f"risk={normalized_risk}, mitigation={normalized_mitigation}"
            ),
            inputs=[
                "validity_frame.interference.risk",
                "validity_frame.interference.mitigation",
                "validity_frame.interference.residual_note",
            ],
            rule=(
                "DSX-INT-010 fires when interference.risk is a non-'none' member "
                "of INTERFERENCE_RISKS, interference.mitigation is 'none' or "
                "blank, and interference.residual_note is blank, an "
                "angle-bracket placeholder, or a refusal token under "
                "is_placeholder_or_refusal()."
            ),
            citation=(
                "Imbens & Rubin (2015), Causal Inference for Statistics, "
                "Social, and Biomedical Sciences, section 1.6"
            ),
            counterfactual=(
                "Declaring a mitigation admissible for this risk, or writing a "
                "non-placeholder residual note, would have cleared DSX-INT-010."
                if unaddressed
                else "A blank/none mitigation with no honest residual note "
                "would have fired DSX-INT-010."
            ),
        ).to_dict()
    )


def _check_interference_mitigation_admissibility(frame: dict, report: Report) -> None:
    """Emit DSX-INT-011 when a declared mitigation is not admissible for the
    declared interference risk.

    Fires only when ``validity_frame.interference.mitigation`` is a member of
    ``dsx.spec.INTERFERENCE_MITIGATIONS`` other than ``none`` and is not a
    member of ``_RISK_MITIGATION_MAP[risk]`` for the declared, normalized
    risk. Because it requires a declared non-``none`` mitigation and
    DSX-INT-010 (``_check_interference_unaddressed``) requires the absence of
    one, the two codes are disjoint by construction (proven by Test 6 in
    ``tests/test_frame_interference.py``).

    Citation: Kohavi, R., Tang, D. and Xu, Y. (2020), *Trustworthy Online
    Controlled Experiments: A Practical Guide to A/B Testing*, Cambridge
    University Press, Chapter 22 "Leakage and Interference between Variants",
    pages 230 to 233, **for the existence and naming of the technique set
    only**, verified from the publisher's own index at
    ``https://assets.cambridge.org/97811087/24265/index/9781108724265_index.pdf``.
    The chapter's running text is unreachable; no cell in
    ``_RISK_MITIGATION_MAP`` is quoted from the book — the table is derived
    from the structural criterion below, not from the chapter. "modelled" has
    no index entry in this chapter at all — it is not a book-named technique,
    so every "modelled" cell rests on the structural criterion alone. The
    book also names a fifth technique the vocabulary omits, "network
    egocentric randomization" (page 233) — noted, not added; a vocabulary
    member is contract surface this phase is not scoped for.
    Optional further citation (D-20): Blake, T. and Coey, D. (2014), "Why
    Marketplace Experimentation is Harder than It Seems", EC '14, section 3 —
    ignoring test-control interference gives effectiveness estimates too
    large by a factor of around two, the empirical case for marketplace being
    a distinct interference channel from shared_budget. Cited by section, not
    page: the authors' own copy carries no EC '14 proceedings pagination.
    Structural criterion: a mitigation is admissible only where it operates
    on the same interference channel the risk names.
    """
    risk = get(frame, "interference.risk")
    normalized_risk = normalize(risk) if not is_blank(risk) else "none"
    if normalized_risk == "none" or normalized_risk not in INTERFERENCE_RISKS:
        return

    mitigation = get(frame, "interference.mitigation")
    normalized_mitigation = normalize(mitigation) if not is_blank(mitigation) else "none"
    if normalized_mitigation == "none" or normalized_mitigation not in INTERFERENCE_MITIGATIONS:
        return

    # Judgment point: a real risk and a real, declared, non-'none' mitigation.
    admissible = _RISK_MITIGATION_MAP.get(normalized_risk, frozenset())
    inadmissible = normalized_mitigation not in admissible

    if inadmissible:
        admissible_listed = ", ".join(sorted(admissible)) or "(none admissible)"
        report.add(
            "DSX-INT-011",
            "CRITICAL",
            f"mitigation {normalized_mitigation} is not admissible for interference risk {normalized_risk}",
            detail=(
                f"validity_frame.interference.risk is {risk!r} and mitigation is "
                f"{mitigation!r}. The declared mitigation does not operate on the "
                f"channel {normalized_risk!r} names. Admissible mitigations for "
                f"{normalized_risk!r}: {admissible_listed}."
            ),
            remedy=(
                f"Declare a mitigation admissible for {normalized_risk!r}: "
                f"{admissible_listed}."
            ),
            where="spec.validity_frame.interference.mitigation",
        )

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                f"DSX-INT-011 {'fired' if inadmissible else 'clear'}: "
                f"risk={normalized_risk}, mitigation={normalized_mitigation}"
            ),
            inputs=[
                "validity_frame.interference.risk",
                "validity_frame.interference.mitigation",
            ],
            rule=(
                "DSX-INT-011 fires when interference.mitigation is a non-'none' "
                "member of INTERFERENCE_MITIGATIONS and is not a member of "
                "_RISK_MITIGATION_MAP[normalize(risk)]."
            ),
            citation="Kohavi, Tang & Xu (2020), Trustworthy Online Controlled Experiments, Chapter 22",
            counterfactual=(
                f"Declaring one of {sorted(admissible)} instead would have "
                "cleared DSX-INT-011."
                if inadmissible
                else f"Declaring a mitigation outside {sorted(admissible)} would "
                "have fired DSX-INT-011."
            ),
        ).to_dict()
    )


def _check_triggering_dilution(spec: dict, frame: dict, report: Report) -> None:
    """Emit DSX-INT-030 when an additive metric is analysed on the eligible
    population with no declared dilution adjustment.

    Fires when ``validity_frame.triggering.analysis_population`` is
    ``eligible``, ``validity_frame.triggering.dilution_adjusted`` is not the
    literal boolean ``True``, and at least one declared top-level ``metrics``
    entry has a normalized ``type`` that is a member of
    ``_ADDITIVE_METRIC_TYPES``. One finding is emitted for the spec, not one
    per metric — the defect is the single missing adjustment declaration.
    A metric with no declared ``type`` is neither additive nor ratio; it
    cannot be classified, so it is skipped rather than adjudicated, and one
    ``DecisionRecord`` naming the skip and its reason is appended for each —
    never a finding (``dsx.spec._validate_metrics`` already treats ``type``
    as optional; firing on an undeclared type would be a new requiredness
    rule this phase is not scoped to add). The check's own fire/clear
    judgment is recorded exactly once, and only when at least one additive
    metric was found to adjudicate: a spec whose only declared metrics carry
    no type has nothing for this check to judge, and produces only the skip
    record(s) (Test 7 in ``tests/test_frame_interference.py``).

    Citation: Deng, A. and Hu, V. (2015), "Diluted Treatment Effect
    Estimation for Trigger Analysis in Online Controlled Experiments", WSDM
    '15, Formula (1) in section 2.1, derived in section 3.2; camera-ready at
    https://alexdeng.github.io/public/files/wsdm2015-dilution.pdf, ACM
    Digital Library DOI 10.1145/2684822.2685307. The formula as printed:
    ∆overall = ∆Tr × N_Tr/N, under three preconditions stated in the same
    section: the metric is additive, there is no treatment effect for
    untriggered units, and the treatment has no effect on the trigger
    complement. The paper writes the user trigger rate as N_Tr/N; its own
    symbol TR means a different, per-user quantity in section 3.3, and the
    contract field this check reads is ``expected_trigger_rate`` — never
    ``trigger_rate``.
    Structural criterion: analysing an additive metric on the eligible
    population when treatment can only have reached the triggered subset,
    with no adjustment declared, reports an effect diluted toward zero by
    the untriggered share; this check adjudicates the declaration rather
    than computing the correction. Ratio metrics are explicitly out of
    scope: the paper's own time-to-success counterexample shows the additive
    formula above failing for a ratio metric, and the ratio-metric equation
    (Formula (3), section 3.3) sums over individual users with no
    closed-form scalar multiplier. ``dsx.mathx.diluted_effect`` holds the
    reference implementation of the additive formula above and is never
    called from this gate path (D-09).
    """
    triggering = section(frame, "triggering")
    if not triggering:
        return

    population = get(triggering, "analysis_population")
    normalized_population = normalize(population) if not is_blank(population) else ""
    if normalized_population != "eligible":
        return

    # Judgment point: the analysis population is eligible. The rest of this
    # function decides whether an additive metric was analysed with no
    # declared dilution adjustment.
    dilution_adjusted = triggering.get("dilution_adjusted")
    # Deliberate identity comparison, never is_blank(): is_blank(False) is
    # False (a bool is none of is_blank's blank shapes — None, empty string,
    # empty collection), so an is_blank() check here would never fire on the
    # literal `dilution_adjusted: false` the template and three of the four
    # corpus fixtures all declare. Do not "simplify" this back to is_blank().
    not_adjusted = dilution_adjusted is not True
    expected_trigger_rate = get(triggering, "expected_trigger_rate")

    additive_metrics: "list[str]" = []
    for metric in items(spec, "metrics"):
        if not isinstance(metric, dict):
            continue
        name = metric.get("name")
        mtype = normalize(metric.get("type", ""))
        if not mtype:
            report.context.setdefault("decisions", []).append(
                DecisionRecord(
                    id="",
                    invocation_id="",
                    layer="deterministic",
                    choice=f"DSX-INT-030 skip: metric {name!r} has no declared type",
                    inputs=[f"metrics[].type (metric {name!r})"],
                    rule=(
                        "A metric with no declared type cannot be classified "
                        "additive or ratio and is therefore not adjudicated by "
                        "DSX-INT-030."
                    ),
                    counterfactual=(
                        f"Declaring an additive type ({', '.join(sorted(_ADDITIVE_METRIC_TYPES))}) "
                        f"for metric {name!r} would have made it eligible for this "
                        "check's judgment."
                    ),
                ).to_dict()
            )
            continue
        if mtype in _ADDITIVE_METRIC_TYPES:
            additive_metrics.append(f"{name} ({mtype})")
        # Every other declared type — ratio, rate, percentile, index, or any
        # value outside dsx.spec.METRIC_TYPES — is neither additive nor
        # skipped; it is simply not this check's concern and is ignored.

    if not additive_metrics:
        return

    fired = not_adjusted

    if fired:
        listed_metrics = ", ".join(additive_metrics)
        rate_note = (
            f" The declared expected_trigger_rate is {expected_trigger_rate!r}."
            if not is_blank(expected_trigger_rate)
            else ""
        )
        report.add(
            "DSX-INT-030",
            "CRITICAL",
            "additive metric analysed on the eligible population with no dilution adjustment declared",
            detail=(
                f"validity_frame.triggering.analysis_population is {population!r} with "
                f"dilution_adjusted {dilution_adjusted!r}. Additive metric(s) analysed: "
                f"{listed_metrics}.{rate_note} A metric with no declared type is not "
                "adjudicated by this check — deleting a metric's type declaration is a "
                "live escape from this CRITICAL check; the decision trail records each "
                "such skip but does not close the hole."
            ),
            remedy=(
                "Declare validity_frame.triggering.dilution_adjusted: true once the "
                "adjustment has actually been made, or analyse the triggered population "
                "instead. dsx.mathx.diluted_effect is the reference implementation of "
                "the additive dilution arithmetic."
            ),
            where="spec.validity_frame.triggering.dilution_adjusted",
        )

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                f"DSX-INT-030 {'fired' if fired else 'clear'}: "
                f"analysis_population={normalized_population}, "
                f"dilution_adjusted={dilution_adjusted!r}, "
                f"additive_metrics={additive_metrics}"
            ),
            inputs=[
                "validity_frame.triggering.analysis_population",
                "validity_frame.triggering.dilution_adjusted",
                "metrics[].type",
            ],
            rule=(
                "DSX-INT-030 fires when triggering.analysis_population is "
                "'eligible', triggering.dilution_adjusted is not the literal "
                "boolean True, and at least one declared metric's normalized "
                "type is a member of _ADDITIVE_METRIC_TYPES."
            ),
            citation=(
                "Deng & Hu (2015), Diluted Treatment Effect Estimation for "
                "Trigger Analysis in Online Controlled Experiments, Formula (1)"
            ),
            counterfactual=(
                "Declaring dilution_adjusted: true, or analysing the triggered "
                "population instead, would have cleared DSX-INT-030."
                if fired
                else "An eligible-population analysis of these additive "
                "metric(s) with dilution_adjusted not true would have fired "
                "DSX-INT-030."
            ),
        ).to_dict()
    )


def _check_stability_assessment(frame: dict, report: Report) -> None:
    """Emit DSX-INT-040 when a declared novelty or primacy assessment was
    never carried out, or was carried out with no evidence pointer.

    Fires when ``validity_frame.stability`` is present (a non-empty mapping —
    the same presence gate ``_check_triggering_dilution`` uses for
    ``triggering``, so an absent or malformed sub-block, including an empty
    mapping, degrades to no finding rather than being distinguished from
    absence) and either ``novelty_primacy_assessed`` is not the literal
    boolean ``True``, or it is ``True`` and ``evidence`` is blank, an
    angle-bracket placeholder, or a refusal token
    (``is_placeholder_or_refusal()``). One finding is emitted, never two,
    naming which of the two cases was hit. The absent-sub-block case belongs
    to ``DSX-SPEC-081`` (Phase 6 D-11); firing here on top of it would
    double-report a single defect.

    This is the family's only HIGH code — the severity alone, with no
    ``GATE_THRESHOLDS`` edit, is what blocks ``verify`` and ``ship`` and not
    ``plan`` (D-02).

    Citation: Sadeghi, S. et al. (2021), "Novelty and Primacy: A Long-Term
    Estimator for Online Experiments", arXiv:2102.12893v1, Equation (13) in
    section 4.2 for the general difference-in-differences estimator and
    Equation (9) in section 4.1 for the three-period case. The published
    p-value 0.0083 attaches to Equation (9) and not to Equation (13) —
    section 4.4 of the preprint says so explicitly. Technometrics
    64(4):524-534 (2022) is cited alongside as the version of record, but
    never for the equation numbers or the values: it is paywalled, the
    arXiv record holds only version 1 from February 2021, and the preprint
    was never synced to the accepted manuscript, so agreement between the
    two is unverified.
    Structural criterion: a declared stability window with no completed
    novelty or primacy assessment, or an assessment with no evidence
    pointer, leaves the time-stability of the reported effect asserted
    rather than checked. This check reads the declaration and does not open
    the evidence file: resolving the pointer needs the evidence helpers in
    ``dsx/checks/claims.py``, which the D-03a import boundary forbids
    ``dsx/frame/`` from reaching. Doing it properly means extracting those
    helpers into a standard-library-only peer module — the move already
    made for the decision-record module (``dsx/decisions.py``) — and this is
    a candidate for whichever later phase next needs the same thing. The
    assessment method is cited here in the docstring rather than declared in
    a configuration field, because there is no ``stability.method`` field in
    the contract and adding one is contract surface this phase is not
    scoped for.
    """
    stability = section(frame, "stability")
    if not stability:
        # Absent, malformed, or an empty mapping all degrade identically —
        # DSX-SPEC-081 owns the absent case, and an empty mapping carries
        # nothing to adjudicate.
        return

    # Judgment point: the stability sub-block is present.
    window = get(stability, "window")
    assessed = stability.get("novelty_primacy_assessed")
    # Deliberate identity comparison, never is_blank(): is_blank(False) is
    # False (a bool is none of is_blank's blank shapes), so an is_blank()
    # check here would never fire on the literal `novelty_primacy_assessed:
    # false` the template and (pre plan 08-02) several corpus fixtures
    # declared. Do not "simplify" this back to is_blank().
    not_assessed = assessed is not True
    evidence = get(stability, "evidence")
    evidence_missing = is_placeholder_or_refusal(evidence)

    if not_assessed:
        case = "unassessed"
        fired = True
    else:
        case = "unevidenced"
        fired = evidence_missing

    if fired:
        if case == "unassessed":
            where = "spec.validity_frame.stability.novelty_primacy_assessed"
            case_text = (
                f"novelty_primacy_assessed is {assessed!r} — no completed novelty or "
                "primacy assessment is declared over this window."
            )
        else:
            where = "spec.validity_frame.stability.evidence"
            case_text = (
                f"novelty_primacy_assessed is true but stability.evidence is "
                f"{evidence!r}, which is blank or a placeholder — the assessment is "
                "declared with no supporting record."
            )
        report.add(
            "DSX-INT-040",
            "HIGH",
            f"novelty/primacy assessment {case} for the declared stability window",
            detail=(
                f"validity_frame.stability.window is {window!r}. {case_text} This is "
                "not DSX-EXP-030: that code adjudicates design.duration_days against "
                "a minimum-week floor; this code adjudicates whether a novelty or "
                "primacy assessment was carried out and evidenced over the declared "
                "stability window, not the window's length."
            ),
            remedy=(
                "Run the novelty/primacy assessment over the declared window and "
                "record where the result lives (e.g. a RESULTS.md anchor), then set "
                "validity_frame.stability.novelty_primacy_assessed: true and point "
                "validity_frame.stability.evidence at that record."
            ),
            where=where,
        )

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=(
                f"DSX-INT-040 {'fired' if fired else 'clear'}: "
                f"novelty_primacy_assessed={assessed!r}, evidence={evidence!r}"
            ),
            inputs=[
                "validity_frame.stability.novelty_primacy_assessed",
                "validity_frame.stability.evidence",
            ],
            rule=(
                "DSX-INT-040 fires when the stability sub-block is present and "
                "novelty_primacy_assessed is not the literal boolean True, or it is "
                "True and stability.evidence is blank, an angle-bracket placeholder, "
                "or a refusal token under is_placeholder_or_refusal()."
            ),
            citation=(
                "Sadeghi et al. (2021), Novelty and Primacy: A Long-Term Estimator "
                "for Online Experiments, arXiv:2102.12893v1, Eq. (13)/(9)"
            ),
            counterfactual=(
                "Declaring novelty_primacy_assessed: true with a real evidence "
                "pointer would have cleared DSX-INT-040."
                if fired
                else "novelty_primacy_assessed not true, or true with a blank or "
                "placeholder evidence, would have fired DSX-INT-040."
            ),
        ).to_dict()
    )


def check(spec: dict) -> Report:
    """Emit the interference-family findings (``DSX-INT-*``).

    Reads ``validity_frame:`` and degrades to an empty report — never a
    traceback — when the block is absent or is not a dictionary (an absent
    block is already ``DSX-SPEC-080`` territory, so this function does not
    re-report it), and when ``dsx.spec.needs_causal_block(spec)`` is false
    (D-16): the causal-only sub-blocks this module adjudicates do not apply
    to a descriptive/observational spec, and ``templates/ANALYSIS-SPEC.yaml``
    depends on that skip to clear ``dsx gate plan`` unedited.

    Structural criterion: dispatches to one private helper per adjudicated
    concept; no numeric threshold, effect size or statistic is computed
    anywhere in this module. Guards against a non-dict ``spec`` itself
    (``dsx.spec.section``/``needs_causal_block`` both call ``.get()`` on
    their argument unconditionally, so a spec that is a string, list, or
    other non-mapping value must be intercepted here before either is
    reached — never by a try/except, matching the rest of this module).
    """
    report = Report(check="interference")

    if not isinstance(spec, dict):
        return report

    frame = section(spec, "validity_frame")
    if not frame:
        return report
    if not needs_causal_block(spec):
        return report

    _check_interference_unaddressed(frame, report)
    _check_interference_mitigation_admissibility(frame, report)
    _check_triggering_dilution(spec, frame, report)
    _check_stability_assessment(frame, report)

    return report
