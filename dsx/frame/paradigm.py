"""DSX-PAR-001 — the informational paradigm manifest — and DSX-PAR-010/011 —
the symmetric monitoring-discipline pair.

DSX-PAR-001, for every gate run, names which check families applied given the
declared ``inference.paradigm`` (or its absence) and which did not — and why.
Never blocks (D-10): an unsupported or undeclared paradigm must not be the
cheapest way past the gate, so an operator's honest ``bayesian`` never costs
more than a dishonest ``frequentist`` would have.

Applicability is modelled as data, not as an if/else on one paradigm value
(the promote decision this module implements — see 06-07-PLAN.md's
``<assumption_delta_decision>``): ``_PARADIGM_CONDITIONAL`` is keyed by every
member of ``PARADIGMS``, computed by the same code path regardless of which
one is declared. ``_MONITORING_DISCIPLINE`` (Phase 9, 09-03-PLAN.md) is the
same idiom applied to DSX-PAR-010/DSX-PAR-011: a dict keyed by every member of
``PARADIGMS``, this time a CRITICAL, gate-blocking pair rather than an
informational manifest, and this is the module that ships both halves
together at identical severity (brief D-12) — see
``references/paradigm-symmetry.md`` for the locked clearing-condition
contract.
"""

from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..mathx import inflation_from_peeking
from ..spec import (
    PARADIGM_JUSTIFICATIONS,
    PARADIGMS,
    as_number,
    get,
    is_blank,
    is_blank_text,
    normalize,
)

# Frame/contract families that apply regardless of the declared paradigm
# (D-11: frame-layer checks never branch on paradigm). DSX-PAR-002 is this
# manifest's own Phase 9 sibling — the second half of the symmetric
# monitoring pair's manifest side — independent of which paradigm is
# eventually declared.
_PARADIGM_INDEPENDENT: "tuple[str, ...]" = (
    "DSX-SPEC-08",
    "DSX-VAL-",
    "DSX-INT-",
    "DSX-PRE-",
    "DSX-PAR-002",
)

# Keyed by every member of PARADIGMS (D-12 symmetry) — a test asserts set
# equality with dsx.spec.PARADIGMS, so a future PARADIGMS addition without a
# matching key here fails loudly instead of silently under-reporting.
_PARADIGM_CONDITIONAL: "dict[str, tuple[str, ...]]" = {
    "frequentist": ("DSX-PAR-010", "DSX-ADM-"),
    "bayesian": ("DSX-PAR-011",),
}

# Prefixes with zero shipped code in this build, mapped to the reason a
# reader should not be alarmed they are absent — the phase that ships them.
# T-6-14: this dict is the honesty control. A prefix stays here until the
# phase that ships it lands; two invariant tests in tests/test_dsx.py prove
# every 'applied' prefix resolves to a known code and every prefix here
# resolves to none.
_NOT_SHIPPED: "dict[str, str]" = {
    "DSX-PRE-": "Phase 10 ships DSX-PRE-* (pre-registered inference plan).",
    "DSX-ADM-": "Phase 11 ships DSX-ADM-* (frequentist procedure admissibility).",
}

# The single member of PEEKING_POLICIES both halves of the DSX-PAR-010/011
# pair trigger on. Neither half reads results.interim_looks (D-04): at
# `dsx gate plan` no results: block exists yet, and a trigger depending on it
# would silently become verify/ship-only, making ROADMAP Success Criterion 1
# false.
_UNCONTROLLED_POLICY = "uncontrolled_continuous"

# The primary representation for DSX-PAR-010/DSX-PAR-011 (CONTEXT.md D-06,
# promoted per the 09-03-PLAN.md <assumption_delta_decision>): a dict keyed by
# every member of PARADIGMS, each row naming that paradigm's finding code and
# its tuple of clearing declarations. A contract test asserts
# set(_MONITORING_DISCIPLINE) == set(PARADIGMS), that every clearing tuple has
# the same length, and that "threshold_calibration" is in every one — a
# future PARADIGMS member added without a matching row here fails loudly.
#
# Three structural facts make the table symmetric (references/paradigm-symmetry.md):
#   1. Exactly two clearing declarations per row — never one, never three,
#      the same count on both sides.
#   2. Exactly one of the two, threshold_calibration, is shared by both rows —
#      the same field, checked by the same predicate, on either side.
#   3. Each row's one paradigm-specific declaration (alpha_spending for
#      frequentist, prior_justification for bayesian) is a non-blank free-text
#      scalar evaluated by the same text-only predicate (is_blank_text) as the
#      shared field — no field on either side carries a stronger evidentiary
#      bar than the other.
_MONITORING_DISCIPLINE: "dict[str, tuple[str, tuple[str, ...]]]" = {
    "frequentist": ("DSX-PAR-010", ("alpha_spending", "threshold_calibration")),
    "bayesian": ("DSX-PAR-011", ("prior_justification", "threshold_calibration")),
}


def _blank_clearing_declarations(
    inference: dict, fields: "tuple[str, ...]"
) -> "list[str]":
    """Return the subset of ``fields`` that are blank under ``inference``.

    The mechanical proof of cost symmetry (brief D-12): every clearing
    declaration for every paradigm in ``_MONITORING_DISCIPLINE`` is evaluated
    by this one function — no per-paradigm and no per-field code path exists
    anywhere in the pair. A clearing declaration is satisfied only by
    non-blank text (``is_blank_text``), identically for every paradigm and
    every field, so no row can be cleared by a value that carries no declared
    content — a bare number or boolean is blank here even though
    ``is_blank`` itself would call it present; a list or mapping is blank
    here even when non-empty (empty containers were already blank under
    ``is_blank``).
    """
    return [name for name in fields if is_blank_text(inference.get(name))]


def _check_monitoring_discipline(spec: dict, report: Report) -> None:
    """Emit DSX-PAR-010 (frequentist) and DSX-PAR-011 (bayesian) — the atomic,
    symmetric monitoring-discipline pair (REQ-P9-01, REQ-P9-02, brief D-12).

    Both codes trigger on exactly one condition: ``design.peeking_policy``
    normalizes to ``uncontrolled_continuous``. Per D-04, ``results.interim_looks``
    is never read here — at ``dsx gate plan`` no ``results:`` block exists
    yet, and a trigger depending on it would silently become verify/ship-only,
    making ROADMAP Success Criterion 1 false. Disjointness from
    ``DSX-EXP-060`` (``dsx/checks/design.py::_check_peeking``) follows by
    construction: that check only fires for the empty and ``fixed_horizon``
    policies and reads ``results.interim_looks``, neither of which this
    function touches.

    The row for the declared paradigm applies when one is declared and is a
    member of ``PARADIGMS``; every row applies when the paradigm is blank,
    absent, or not a member — closing the undeclared-paradigm escape at
    CRITICAL without spending a new code number (``dsx/cli.py``'s
    ``GATE_THRESHOLDS`` is CRITICAL at ``plan`` and ``execute``). Declaring a
    paradigm therefore never adds a finding, it only ever removes one (brief
    D-10) — this is also why ``DSX-PAR-002`` (HIGH, plan 09-05) does not need
    to block at ``plan`` on its own: the uncontrolled design is already
    blocked regardless of whether a paradigm was declared.

    Citation: (DSX-PAR-010) Armitage, P., McPherson, C. K. & Rowe, B. C.
    (1969), "Repeated Significance Tests on Accumulating Data", Journal of
    the Royal Statistical Society, Series A (General), volume 132, issue 2,
    pages 235-244, DOI 10.2307/2343787. Same unverified-locator flag as
    ``dsx.mathx.inflation_from_peeking()``, which this check reuses directly
    (no second table, REQ-P9-01): the full text is subscriber-only at Oxford
    University Press, Wiley and JSTOR, and no table or page number within the
    paper was verified — naming one would be the fabricated locator brief D-05
    exists to prevent.
    Reference value: (DSX-PAR-010) at a nominal alpha of 0.05, the true
    type-I error is 0.142 at five interim looks and 0.248 at twenty (the same
    anchors ``inflation_from_peeking()`` itself is pinned against). Because
    the number of looks is by definition undeclared and unbounded under an
    uncontrolled-continuous policy, these two named anchors are the honest
    form of the figure — a range, not a single realised count, which is also
    what distinguishes this finding from ``DSX-EXP-060`` at a glance (that
    finding names an exact realised look count).

    Citation: (DSX-PAR-011) Deng, A., Lu, J. & Chen, S. (2016), "Continuous
    Monitoring of A/B Tests without Pain: Optional Stopping in Bayesian
    Testing", IEEE DSAA 2016. Theorem 1 states the optional-stopping equality
    that licenses this figure under known prior odds; the bound itself — "the
    risk of false discovery at most 1/(1+K)" — is unnumbered prose
    immediately following Theorem 1 and again in the paper's Section 3.2, so
    citing Theorem 1 alone for the number 1/(K+1) would be a locator error.
    Reference value: (DSX-PAR-011) 1/(K+1) is exactly 0.05 at K = 19, the
    posterior odds implied by a P(B>A) > 0.95 decision threshold. This check
    asserts the prior-averaged formulation, and explicitly not the point-null
    / law-of-iterated-logarithm formulation — under which type-I error tends
    to one as the horizon grows and no fixed ceiling exists, which is exactly
    why that formulation cannot be encoded as a reference value. 1/(K+1)
    equals 1-p identically, so at p = 0.95 the bound 0.05 is just 1-p; the
    non-trivial content Theorem 1 supplies is that this identity survives
    evaluation at a random stopping time, under known prior odds — a declared
    posterior probability computed off a flat prior is not the operator's
    real false-discovery risk, a matter for the remedy text and human review,
    never something the gate can adjudicate. Type-I error (the chance of
    false rejection when the null is true) and false-discovery risk (the
    chance of false rejection given that rejection was decided) are different
    conditioning events with no simple relationship between them — that
    difference is the signature of the different denominator, 1/(K+1) versus
    1/k. Ville's inequality gives the different bound 1/k, about 0.0526 at
    k = 19, and is never a substitute; Deng, Lu and Chen never cite Ville.
    Structural criterion: presence only, for both codes. The blocking
    decision is a set-membership computation over the data-driven
    ``_MONITORING_DISCIPLINE`` map, evaluated by one shared predicate
    (``_blank_clearing_declarations``) — no statistic, posterior, or
    arithmetic over any operator-declared value (including
    ``inference.decision_threshold``, which is never read here) is computed
    on the gate path.
    """
    policy = normalize(get(spec, "design.peeking_policy") or "")
    if policy != _UNCONTROLLED_POLICY:
        return

    inference = spec.get("inference")
    if not isinstance(inference, dict):
        inference = {}

    declared = get(spec, "inference.paradigm")
    paradigm = normalize(declared) if not is_blank(declared) else ""

    if paradigm in _MONITORING_DISCIPLINE:
        rows: "dict[str, tuple[str, tuple[str, ...]]]" = {
            paradigm: _MONITORING_DISCIPLINE[paradigm]
        }
    else:
        rows = dict(_MONITORING_DISCIPLINE)

    for _row_paradigm, (code, clearing_fields) in rows.items():
        blank = _blank_clearing_declarations(inference, clearing_fields)
        if len(blank) < len(clearing_fields):
            continue  # at least one clearing declaration is non-blank

        if code == "DSX-PAR-010":
            alpha = as_number(get(spec, "design.alpha")) or 0.05
            five = inflation_from_peeking(5, alpha)
            twenty = inflation_from_peeking(20, alpha)
            report.add(
                "DSX-PAR-010",
                "CRITICAL",
                "Uncontrolled continuous monitoring under a frequentist "
                "paradigm with no monitoring discipline declared",
                detail=(
                    "design.peeking_policy is uncontrolled_continuous: interim "
                    "looks continue with no sequential correction and no "
                    "anytime-valid method. The number of looks under this "
                    "policy is by definition undeclared and unbounded, so the "
                    "honest figure is a range at named anchors: at a nominal "
                    f"alpha of {alpha:.2f}, the true type-I error is "
                    f"approximately {five:.3f} at five interim looks and "
                    f"{twenty:.3f} at twenty "
                    "(dsx.mathx.inflation_from_peeking; no second table)."
                ),
                remedy=(
                    "Declare a non-blank text value in inference.alpha_spending "
                    "or inference.threshold_calibration to satisfy this check "
                    "structurally (presence, not quality) — a number, a "
                    "boolean, or an empty value does not clear it. The honest "
                    "fix is to change design.peeking_policy to sequential_obf, "
                    "sequential_pocock, or always_valid, which is the only "
                    "fix that actually controls the error rate a peeked test "
                    "accumulates."
                ),
                where="spec.design.peeking_policy",
                inflated_alpha_at_5_looks=round(five, 4),
                inflated_alpha_at_20_looks=round(twenty, 4),
            )
        else:  # DSX-PAR-011
            report.add(
                "DSX-PAR-011",
                "CRITICAL",
                "Uncontrolled continuous monitoring under a bayesian "
                "paradigm with no monitoring discipline declared",
                detail=(
                    "design.peeking_policy is uncontrolled_continuous: interim "
                    "looks continue with no sequential correction and no "
                    "anytime-valid method. Under the prior-averaged "
                    "formulation (Deng, Lu & Chen 2016), the risk of false "
                    "discovery at a P(B>A) > 0.95 decision threshold is "
                    "bounded by 1/(K+1) = 1/20 = 0.05 at K = 19 — a fixed "
                    "reference anchor, never a computation over any "
                    "operator-declared value. Theorem 1 licenses that bound "
                    "under optional stopping with known prior odds; the "
                    "bound itself is unnumbered prose following Theorem 1 "
                    "and again in the paper's Section 3.2."
                ),
                remedy=(
                    "Declare a non-blank text value in "
                    "inference.prior_justification or "
                    "inference.threshold_calibration to satisfy this check "
                    "structurally (presence, not quality — prior-justification "
                    "quality is DSX-PAR-020's job, deferred to a later "
                    "milestone) — a number, a boolean, or an empty value does "
                    "not clear it. The honest fix is to change "
                    "design.peeking_policy to sequential_obf, "
                    "sequential_pocock, or always_valid."
                ),
                where="spec.design.peeking_policy",
            )

        report.context.setdefault("decisions", []).append(
            DecisionRecord(
                id="",
                invocation_id="",
                layer="deterministic",
                choice=f"{code} fired: paradigm={paradigm or 'undeclared'}",
                inputs=["design.peeking_policy", "inference.paradigm", *clearing_fields],
                rule=(
                    "design.peeking_policy == 'uncontrolled_continuous' and "
                    "every clearing declaration in "
                    "_MONITORING_DISCIPLINE[paradigm] is blank."
                ),
                citation=(
                    "Armitage, McPherson & Rowe (1969), Repeated Significance "
                    "Tests on Accumulating Data"
                    if code == "DSX-PAR-010"
                    else "Deng, Lu & Chen (2016), Continuous Monitoring of "
                    "A/B Tests without Pain"
                ),
                counterfactual=(
                    f"Declaring a non-blank {' or '.join(clearing_fields)} "
                    f"would have cleared {code}."
                ),
            ).to_dict()
        )


def _check_paradigm_justification(spec: dict, report: Report) -> None:
    """Emit DSX-PAR-002 — requiredness for ``inference.paradigm_justification``,
    and the requiredness half of a missing ``inference.paradigm`` under an
    uncontrolled design (REQ-P9-04, D-08, D-09, brief D-12).

    Two mutually exclusive cases by construction — one requires a declared
    paradigm, the other requires a blank one — so at most one finding is
    ever emitted:

      - ``inference.paradigm`` normalizes to a member of ``PARADIGMS`` and
        ``inference.paradigm_justification`` is blank or absent: a paradigm
        was declared but the reason for it was not.
      - ``inference.paradigm`` does not normalize to a member of
        ``PARADIGMS`` — blank, absent, or a non-blank string outside the
        vocabulary — *and* ``design.peeking_policy`` normalizes to
        ``uncontrolled_continuous``: no paradigm this spec can actually be
        checked against was declared, under a design that needs one. The
        unrecognised case reads the same as the blank one deliberately:
        ``_check_monitoring_discipline`` already treats it that way, and
        before 07-REVIEW.md CR-01 a typo'd paradigm matched neither branch
        and cleared this code entirely.

    Never *reports* membership. ``DSX-SPEC-085``
    (``dsx/spec.py::_validate_inference_shape``) owns whether a declared
    ``paradigm_justification`` is a recognised member of
    ``PARADIGM_JUSTIFICATIONS`` — a committed test pins the real
    ``examples/bad-ANALYSIS-SPEC.yaml`` fixture at exactly one
    ``DSX-SPEC-085`` finding for its out-of-vocabulary
    ``paradigm_justification`` and zero ``DSX-PAR-002`` findings (T-9-14).
    Re-checking membership here would emit two codes for one defect;
    ``PARADIGM_JUSTIFICATIONS`` is read only to list the seven allowed
    reasons in the remedy text, by iterating the live vocabulary in sorted
    order — never a hand-written subset, never an adjective distinguishing
    one reason from another (brief D-12; the failure mode this guards
    against is named in brief D-12 itself: a reason like ``team_convention``
    or ``vendor_constraint`` quietly acquiring a weaker path later).

    Citation: Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of
    A/B Tests without Pain: Optional Stopping in Bayesian Testing", IEEE
    DSAA 2016 — the same primary source this module's other checks cite, for
    the proposition that a decision procedure's realised error rate is
    paradigm-dependent, which is what makes an undeclared or unjustified
    paradigm a real gap rather than a formality. The exact section/theorem
    locator within this paper is unverified at time of writing — the same
    unverified-locator flag carried by this module's other citations of the
    same source, escalated per D-05 rather than invented.
    Structural criterion: a usability test over one field at a time — is
    there a value here this spec can be checked against — never a
    membership *report* (``DSX-SPEC-085`` owns emitting the vocabulary
    violation, and a spec whose only defect is an out-of-vocabulary
    ``paradigm_justification`` still yields exactly one ``DSX-SPEC-085``
    finding and zero ``DSX-PAR-002`` findings, T-9-14). The identical path
    applies to every member of ``PARADIGM_JUSTIFICATIONS`` and of
    ``PARADIGMS``: no per-member or per-paradigm branch exists in this
    function — the only vocabulary read is the whole-set membership test
    that folds an unrecognised ``paradigm`` into the undeclared case.
    """
    declared_paradigm = get(spec, "inference.paradigm")
    paradigm = normalize(declared_paradigm) if not is_blank(declared_paradigm) else ""
    justification = get(spec, "inference.paradigm_justification")
    policy = normalize(get(spec, "design.peeking_policy") or "")

    if paradigm in PARADIGMS and is_blank(justification):
        allowed = ", ".join(sorted(PARADIGM_JUSTIFICATIONS))
        report.add(
            "DSX-PAR-002",
            "HIGH",
            f"inference.paradigm ({paradigm}) is declared with no paradigm_justification",
            detail=(
                "A paradigm was declared but the reason for choosing it was "
                "not. The justification is what makes an honest paradigm "
                "choice cheaper to declare than a dishonest one — without "
                "it, a genuinely-reasoned declaration cannot be told apart "
                "from a paradigm chosen only to dodge a stricter check."
            ),
            remedy=(
                "Declare a non-blank inference.paradigm_justification, one "
                f"of: {allowed}."
            ),
            where="spec.inference.paradigm_justification",
        )
        counterfactual = (
            "Declaring a non-blank inference.paradigm_justification (any "
            f"of: {allowed}) would have cleared DSX-PAR-002."
        )
    elif paradigm not in PARADIGMS and policy == _UNCONTROLLED_POLICY:
        # `paradigm not in PARADIGMS` covers blank/absent *and* the third
        # reachable state: a non-blank string outside the vocabulary. This
        # is a usability test on one field ("is there a paradigm this spec
        # can actually be checked against"), not the membership *report* —
        # DSX-SPEC-085 still owns telling the author their value is not a
        # member, and still fires alone for that. Without this, a typo'd
        # paradigm passed both branches and silently cleared DSX-PAR-002
        # under a design that needs a declaration (07-REVIEW.md CR-01).
        members = ", ".join(sorted(PARADIGMS))
        report.add(
            "DSX-PAR-002",
            "HIGH",
            "inference.paradigm is not declared under an uncontrolled continuous design",
            detail=(
                "design.peeking_policy is uncontrolled_continuous and no "
                "recognised inference.paradigm is declared. With no "
                "recognised paradigm declared, "
                "every paradigm-conditional check currently applies — "
                "declaring one narrows the checks that apply to this spec, "
                "it never adds to them."
            ),
            remedy=f"Declare inference.paradigm, one of: {members}.",
            where="spec.inference.paradigm",
        )
        counterfactual = (
            f"Declaring inference.paradigm (one of: {members}) would have "
            "cleared DSX-PAR-002, and narrowed which paradigm-conditional "
            "checks apply to this spec."
        )
    else:
        return

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=f"DSX-PAR-002 fired: paradigm={paradigm or 'undeclared'}",
            inputs=[
                "inference.paradigm", "inference.paradigm_justification",
                "design.peeking_policy",
            ],
            rule=(
                "inference.paradigm declared as a PARADIGMS member with a "
                "blank paradigm_justification, or inference.paradigm blank "
                "under an uncontrolled_continuous design."
            ),
            citation="Deng, Lu & Chen (2016), Continuous Monitoring of A/B Tests without Pain",
            counterfactual=counterfactual,
        ).to_dict()
    )


def check(spec: dict) -> Report:
    """Emit DSX-PAR-001 — the informational paradigm manifest.

    Citation: Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of
    A/B Tests without Pain: Optional Stopping in Bayesian Testing", IEEE
    DSAA 2016 — the primary source establishing that a decision procedure's
    realised error rate is paradigm-dependent, which is what makes an
    undeclared paradigm a real gap rather than a formality. The exact
    section/theorem locator within this paper is unverified at time of
    writing (same citation, same flag as
    ``dsx/spec.py::_validate_inference_shape``, escalated in the 06-06 plan
    summary rather than invented); author/year/title/venue match brief.md
    section 7.
    Structural criterion: a set-membership computation over a data-driven
    applicability map (``_PARADIGM_INDEPENDENT``, ``_PARADIGM_CONDITIONAL``,
    ``_NOT_SHIPPED``), keyed by every member of ``PARADIGMS`` plus the
    no-usable-declaration case — no numeric threshold or statistic is
    computed here. "No usable declaration" covers blank, absent, and a
    non-blank value outside ``PARADIGMS``; all three take the union of
    every conditional family, matching ``_check_monitoring_discipline``'s
    own fallback so this manifest can never report a family as not applied
    in a report where that family fired (07-REVIEW.md CR-01).
    """
    report = Report(check="paradigm")

    declared = get(spec, "inference.paradigm")
    paradigm = normalize(declared) if not is_blank(declared) else ""

    universe: "set[str]" = set(_PARADIGM_INDEPENDENT)
    for prefixes in _PARADIGM_CONDITIONAL.values():
        universe.update(prefixes)

    selected: "set[str]" = set(_PARADIGM_INDEPENDENT)
    if paradigm in _PARADIGM_CONDITIONAL:
        selected.update(_PARADIGM_CONDITIONAL[paradigm])
    else:
        # Undeclared *or* unrecognised: select every paradigm-conditional
        # family's prefixes (the union), not none of them. Declaring a
        # paradigm never adds a finding, it only ever removes one (brief
        # D-10) — this is what closes the undeclared-paradigm escape from
        # DSX-PAR-010/DSX-PAR-011 at CRITICAL without spending a new code
        # (09-03-PLAN.md, Question 1).
        #
        # The `else` covers both because inference.paradigm has a third
        # reachable state beyond "member of PARADIGMS" and "blank": a
        # non-blank string outside the vocabulary (a typo such as
        # `bayesain`). Membership is not enforced anywhere that blocks
        # `dsx gate plan` — DSX-SPEC-085 reports it at HIGH, below plan's
        # CRITICAL threshold — so that state reaches this function live.
        # _check_monitoring_discipline below already treats it exactly like
        # an undeclared paradigm and evaluates both DSX-PAR-010 and
        # DSX-PAR-011 for it. An `elif not paradigm` here would leave those
        # two out of `selected` while they fired, making this manifest
        # assert the opposite of what the same run evaluated — the one
        # failure mode D-10 exists to prevent.
        for prefixes in _PARADIGM_CONDITIONAL.values():
            selected.update(prefixes)

    applied = sorted(selected - set(_NOT_SHIPPED))
    not_applied_prefixes = sorted(universe - set(applied))
    not_applied = {
        prefix: _NOT_SHIPPED.get(prefix, "not selected for the declared paradigm")
        for prefix in not_applied_prefixes
    }

    applied_text = ", ".join(applied) if applied else "(none)"
    not_applied_text = "; ".join(
        f"{prefix} ({reason})" for prefix, reason in not_applied.items()
    ) or "(none)"
    # Three cases, not two — an unrecognised paradigm widens the applied set
    # exactly like an undeclared one, and the manifest has to say why, or a
    # reader sees both DSX-PAR-010 and DSX-PAR-011 applied under a declared
    # paradigm with no explanation. The vocabulary itself stays
    # DSX-SPEC-085's to report; this only names the consequence.
    if paradigm in _PARADIGM_CONDITIONAL:
        applicability_note = ""
    elif paradigm:
        applicability_note = (
            f"\ninference.paradigm ({paradigm}) is not a recognised paradigm, "
            "so every paradigm-conditional family applies until a recognised "
            "one is declared"
        )
    else:
        applicability_note = (
            "\nno paradigm is declared, so every paradigm-conditional "
            "family applies until one is"
        )
    detail = f"applied: {applied_text}\nnot applied: {not_applied_text}{applicability_note}"
    remedy = (
        "Informational only — naming the gap plainly is what removes the "
        "incentive to misdeclare a paradigm just to look checked (D-10)."
    )

    # The title is a single f-string literal at the call site (not a
    # pre-assigned variable) so scripts/gen-finding-catalogue.py's AST
    # extractor — which requires a Constant/JoinedStr literal in this
    # position — can read it; a dynamic segment collapses to '<…>' there,
    # same convention every other dsx/checks/*.py module already follows.
    report.add(
        "DSX-PAR-001",
        "INFO",
        f"paradigm manifest — inference.paradigm: {paradigm or 'undeclared'}",
        detail=detail,
        remedy=remedy,
        where="spec.inference.paradigm",
        applied=applied,
        not_applied=not_applied,
    )

    other_paradigms = [p for p in PARADIGMS if p != paradigm]
    if paradigm:
        choice = f"paradigm={paradigm}"
        other = other_paradigms[0] if other_paradigms else None
        counterfactual = (
            f"Declaring {other!r} instead would select "
            f"{', '.join(_PARADIGM_CONDITIONAL.get(other, ())) or '(no additional families)'} "
            "in place of this run's paradigm-conditional set."
            if other
            else "No other member of PARADIGMS exists to declare instead."
        )
    else:
        choice = "paradigm=undeclared"
        counterfactual = (
            "Declaring any member of PARADIGMS would select only that "
            "paradigm's conditional family set, dropping the other "
            "paradigm's family that currently applies because none is "
            "declared."
        )

    report.context.setdefault("decisions", []).append(
        DecisionRecord(
            id="",
            invocation_id="",
            layer="deterministic",
            choice=choice,
            inputs=["inference.paradigm"],
            rule=(
                "applied = (paradigm-independent + paradigm-conditional[declared]) "
                "- not-shipped; identical computation for every member of "
                "PARADIGMS (D-12 symmetry)."
            ),
            citation="Deng, Lu & Chen (2016), Continuous Monitoring of A/B Tests without Pain",
            counterfactual=counterfactual,
        ).to_dict()
    )

    _check_monitoring_discipline(spec, report)
    _check_paradigm_justification(spec, report)

    return report
