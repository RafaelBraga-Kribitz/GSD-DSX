"""DSX-INT-* — interference, triggering and stability (Phase 8).

This module adjudicates ``validity_frame.interference``: is a declared
interference/SUTVA risk actually addressed. Phase 6's
``_validate_validity_frame_shape`` (``dsx/spec.py``) already owns shape — is
the ``interference:`` sub-block present, is each field a member of its closed
vocabulary. A missing sub-block is ``DSX-SPEC-080``/``DSX-SPEC-081``
territory, never a ``DSX-INT-*`` finding; firing here on top of that would
double-report a single defect.

Two of the family's four codes ship in this plan: ``DSX-INT-010`` (a declared
risk with no mitigation and no real residual note) and ``DSX-INT-011`` (a
declared mitigation that is not admissible for the declared risk). The
remaining two — ``DSX-INT-030`` (triggering/dilution) and ``DSX-INT-040``
(novelty/primacy) — arrive behind the same ``check()`` dispatcher in later
plans of this phase.

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
    get,
    is_blank,
    is_placeholder_or_refusal,
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
    anywhere in this module.
    """
    report = Report(check="interference")

    frame = section(spec, "validity_frame")
    if not frame:
        return report
    if not needs_causal_block(spec):
        return report

    _check_interference_unaddressed(frame, report)
    _check_interference_mitigation_admissibility(frame, report)

    return report
