"""DSX-PAR-001 — the informational paradigm manifest.

For every gate run, names which check families applied given the declared
``inference.paradigm`` (or its absence) and which did not — and why. Never
blocks (D-10): an unsupported or undeclared paradigm must not be the cheapest
way past the gate, so an operator's honest ``bayesian`` never costs more than
a dishonest ``frequentist`` would have.

Applicability is modelled as data, not as an if/else on one paradigm value
(the promote decision this module implements — see 06-07-PLAN.md's
``<assumption_delta_decision>``): ``_PARADIGM_CONDITIONAL`` is keyed by every
member of ``PARADIGMS``, computed by the same code path regardless of which
one is declared.
"""

from __future__ import annotations

from ..decisions import DecisionRecord
from ..findings import Report
from ..spec import PARADIGMS, get, is_blank, normalize

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
    "DSX-VAL-": "Phase 7 ships DSX-VAL-* (estimand, dependence, identification strength).",
    "DSX-INT-": "Phase 8 ships DSX-INT-* (interference/SUTVA, triggering, dilution).",
    "DSX-PRE-": "Phase 10 ships DSX-PRE-* (pre-registered inference plan).",
    "DSX-PAR-002": "Phase 9 ships DSX-PAR-002 alongside the symmetric monitoring pair.",
    "DSX-PAR-010": "Phase 9 ships DSX-PAR-010 (frequentist monitoring discipline).",
    "DSX-PAR-011": "Phase 9 ships DSX-PAR-011 (bayesian monitoring discipline).",
    "DSX-ADM-": "Phase 11 ships DSX-ADM-* (frequentist procedure admissibility).",
}


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
    undeclared case — no numeric threshold or statistic is computed here.
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
    detail = (
        f"applied: {applied_text}\n"
        f"not applied: {not_applied_text}"
        + ("" if paradigm else "\nno paradigm-conditional family was selected")
    )
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
            "Declaring any member of PARADIGMS would select that paradigm's "
            "conditional family set in place of none."
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

    return report
