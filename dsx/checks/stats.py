"""Statistical validity checks. Codes DSX-STA-*.

Two jobs. First, a decision table that derives the correct test from the shape of
the data — so "which test?" stops being a judgement call and becomes a lookup.
Second, enforcement of the reporting contract: an effect size and an interval,
every time, because a p-value alone answers a question nobody asked.
"""

from __future__ import annotations

from typing import Any

from ..findings import Report
from .. import mathx
from ..mathx import EFFECT_SIZE_KINDS, apply_correction, interpret_effect
from ..spec import (
    ESTIMAND_KINDS,
    ICC_DEFINITIONS,
    ICC_MODELS,
    ICC_TYPES,
    KAPPA_WEIGHT_TOKENS,
    OPERAND_SCALES,
    as_number,
    get,
    is_blank,
    items,
    normalize,
    section,
)

OUTCOME_TYPES = {"proportion", "continuous", "count", "ordinal", "time_to_event"}

# analysis-block routing fields whose declared value must be a member of a closed
# vocabulary. All are guarded by the SAME DSX-STA-040 from a single call site — no new
# code minted (REQ-P17-05) — and the guard runs INDEPENDENTLY of whether a test is declared
# (17-CONTEXT.md D-01: a mis-slotted routing value is a loud decidable error, never a silent
# no-op). ESTIMAND_KINDS is a name->description dict; `in` tests its keys. operand_scale
# (OPERAND_SCALES, Phase 18 REQ-P18-03) joins here so a mis-slotted scale is loud via
# DSX-STA-040 for free — zero new code for the recognition half of the DSX-STA-050 gate.
_MEMBERSHIP_FIELDS: "tuple[tuple[str, Any], ...]" = (
    ("outcome_type", OUTCOME_TYPES),
    ("estimand_kind", ESTIMAND_KINDS),
    ("operand_scale", OPERAND_SCALES),
)

# The correlation-coefficient family DSX-STA-051 keys on: a declared test that measures
# association, wrongly declared for an agreement/method_comparison estimand. Kept module-level
# so recommend_association's acceptable sets and the gate cannot drift.
CORRELATION_FAMILY = {
    "pearson_correlation", "spearman_correlation", "kendall_tau_b",
    "point_biserial", "phi", "cramers_v",
}

# Dataless routing table: each association estimand_kind -> (acceptable-coefficient
# frozenset, effect-size token, citation label). The three association kinds only;
# agreement/method_comparison/ordered_trend route elsewhere (recommend_association raises).
_ASSOCIATION_ROUTES: "dict[str, tuple[frozenset[str], str, str]]" = {
    "linear_association": (
        frozenset({"pearson_correlation", "point_biserial"}),
        "fisher_z",
        "Pearson r with a Fisher-z confidence interval",
    ),
    "monotone_association": (
        frozenset({"spearman_correlation", "kendall_tau_b"}),
        "rho_or_tau_b",
        "Spearman rho / Kendall tau-b",
    ),
    "nominal_association": (
        frozenset({"phi", "cramers_v"}),
        "phi_or_cramers_v",
        "phi (2x2) / Cramer's V (r x c)",
    ),
}

# Tests that assume approximate normality of the sampling distribution.
PARAMETRIC_TESTS = {
    "t_test", "students_t", "welch_t", "paired_t", "anova", "welch_anova",
    "linear_regression", "pearson_correlation", "z_test", "two_proportion_z",
}

NONPARAMETRIC_TESTS = {
    "mann_whitney", "wilcoxon_signed_rank", "kruskal_wallis", "spearman_correlation",
    "fisher_exact", "boschloo_exact", "mcnemar", "chi_square", "permutation_test", "bootstrap",
}

# Rule of thumb above which the CLT makes a mean-based test safe despite skew.
CLT_SAFE_N = 200


def recommend_test(
    outcome_type: str,
    n_groups: int,
    paired: bool = False,
    normal: "bool | None" = None,
    equal_variance: "bool | None" = None,
    n_per_group: "int | None" = None,
    overdispersed: "bool | None" = None,
) -> dict[str, object]:
    """Derive the appropriate test from the data's shape.

    Returns ``{"test", "rationale", "alternatives", "effect_size"}``. Pure and
    total — every input combination yields a recommendation.
    """
    outcome = normalize(outcome_type)
    if outcome not in OUTCOME_TYPES:
        raise ValueError(
            f"unknown outcome_type {outcome_type!r}; expected one of {', '.join(sorted(OUTCOME_TYPES))}"
        )
    if n_groups < 1:
        raise ValueError("n_groups must be >= 1")

    large_sample = n_per_group is not None and n_per_group >= CLT_SAFE_N
    normal_enough = normal is True or (normal is None and large_sample) or large_sample

    if outcome == "proportion":
        if n_groups <= 2 and paired:
            return _rec("mcnemar", "Paired binary outcomes compare discordant pairs only.",
                        ["exact_mcnemar"], "odds_ratio")
        if n_groups <= 2:
            return _rec(
                "two_proportion_z",
                "Two independent proportions with adequate expected cell counts.",
                ["boschloo_exact (any expected cell < 5)", "chi_square", "bootstrap"],
                "risk_difference + cohens_h",
            )
        return _rec("chi_square", "Three or more independent proportions.",
                    ["fisher_exact (sparse cells)", "multinomial_regression"], "cramers_v")

    if outcome == "continuous":
        if n_groups <= 2 and paired:
            if normal_enough:
                return _rec("paired_t", "Paired continuous outcomes with approximately normal differences.",
                            ["wilcoxon_signed_rank", "bootstrap"], "cohens_dz")
            return _rec("wilcoxon_signed_rank", "Paired continuous outcomes with non-normal differences.",
                        ["paired_t on transformed scale", "bootstrap"], "rank_biserial_r")
        if n_groups <= 2:
            if not normal_enough:
                return _rec(
                    "mann_whitney",
                    "Two independent groups, non-normal and below the CLT-safe sample size.",
                    ["welch_t after transformation", "permutation_test", "bootstrap"],
                    "rank_biserial_r",
                )
            if equal_variance is True:
                return _rec(
                    "welch_t",
                    "Two independent groups. Welch is recommended even under equal variance — "
                    "it costs almost no power and stays valid when the assumption fails.",
                    ["students_t", "permutation_test"],
                    "cohens_d",
                )
            return _rec("welch_t", "Two independent groups with unequal or unverified variances.",
                        ["mann_whitney", "bootstrap"], "cohens_d")
        if not normal_enough:
            return _rec("kruskal_wallis", "Three or more independent groups, non-normal.",
                        ["welch_anova after transformation", "permutation_test"], "epsilon_squared")
        if equal_variance is False:
            return _rec("welch_anova", "Three or more groups with unequal variances.",
                        ["kruskal_wallis"], "omega_squared")
        return _rec("anova", "Three or more independent groups, approximately normal, equal variance.",
                    ["welch_anova", "kruskal_wallis"], "omega_squared")

    if outcome == "count":
        if overdispersed:
            return _rec(
                "negative_binomial_regression",
                "Count outcome with variance exceeding the mean.",
                ["quasi_poisson", "poisson with robust SEs"],
                "incidence_rate_ratio",
            )
        return _rec(
            "poisson_regression",
            "Count outcome with variance approximately equal to the mean. Check dispersion "
            "before trusting the standard errors.",
            ["negative_binomial_regression", "bootstrap"],
            "incidence_rate_ratio",
        )

    if outcome == "ordinal":
        if n_groups <= 2:
            return _rec("mann_whitney", "Two groups on an ordinal scale — ranks, not means.",
                        ["ordinal_logistic_regression", "permutation_test"], "rank_biserial_r")
        return _rec("kruskal_wallis", "Three or more groups on an ordinal scale.",
                    ["ordinal_logistic_regression"], "epsilon_squared")

    return _rec("log_rank", "Time-to-event outcome with censoring.",
                ["cox_proportional_hazards", "restricted_mean_survival_time"], "hazard_ratio")


def _rec(test: str, rationale: str, alternatives: list[str], effect: str) -> dict[str, object]:
    return {"test": test, "rationale": rationale, "alternatives": alternatives, "effect_size": effect}


def recommend_association(estimand_kind: str) -> dict[str, object]:
    """Dataless string->acceptable-coefficient-SET lookup for the three association kinds.

    The anti-two-stage proof (REQ-P18-06): this function takes NO data, NO n, NO
    distribution flag — only the declared ``estimand_kind`` — so it is a mechanically
    verifiable routing table, a stronger guarantee than a branch of a function that already
    accepts data-shape arguments (contrast ``recommend_test``). Returns
    ``{"tests", "effect_size", "citation"}`` where ``tests`` is the acceptable-coefficient
    frozenset for the kind. Raises ``ValueError`` for a kind with no association route
    (``agreement`` / ``method_comparison`` route to kappa/ICC/Bland-Altman;
    ``ordered_trend`` routes to trend tests — all out of this function's scope).
    """
    kind = normalize(estimand_kind)
    if kind not in _ASSOCIATION_ROUTES:
        raise ValueError(
            f"no association routing for estimand_kind {estimand_kind!r}; "
            f"expected one of {', '.join(sorted(_ASSOCIATION_ROUTES))}"
        )
    tests, effect_size, citation = _ASSOCIATION_ROUTES[kind]
    return {"tests": tests, "effect_size": effect_size, "citation": citation}


# ── Checks ───────────────────────────────────────────────────────────────────


def check(spec: dict) -> Report:
    report = Report(check="stats")
    results = section(spec, "results")
    tests = items(results, "tests")
    alpha = as_number(get(spec, "design.alpha"))
    if alpha is None:
        alpha = 0.05

    if not tests:
        analysis = section(spec, "analysis")
        if analysis:
            _check_declared_test(analysis, spec, report)
            _check_declared_association(analysis, spec, report)
        return report

    pvalues: list[float] = []
    for index, test in enumerate(tests):
        where = f"spec.results.tests[{index}]"
        label = test.get("metric") or f"test {index}"
        _check_reporting_contract(test, label, where, alpha, report)
        p = as_number(test.get("p_value"))
        if p is not None:
            pvalues.append(p)
            _check_practical_significance(test, p, label, where, alpha, report)
            _check_null_acceptance(test, p, label, where, alpha, spec, report)

    _check_correction_applied(spec, pvalues, alpha, report)
    _check_declared_test(section(spec, "analysis"), spec, report)
    _check_declared_association(section(spec, "analysis"), spec, report)
    return report


def _check_reporting_contract(
    test: dict, label: str, where: str, alpha: float, report: Report
) -> None:
    p = as_number(test.get("p_value"))
    effect = as_number(test.get("effect"))
    ci = test.get("ci")
    has_ci = isinstance(ci, (list, tuple)) and len(ci) == 2 and all(
        as_number(v) is not None for v in ci
    )

    if p is None and effect is None:
        report.add(
            "DSX-STA-001", "HIGH", f"Result for '{label}' reports neither an effect nor a p-value",
            remedy="Report the effect estimate first, then its interval, then the p-value.",
            where=where,
        )
        return

    if effect is None:
        report.add(
            "DSX-STA-002",
            "HIGH",
            f"Result for '{label}' reports a p-value with no effect size",
            detail=(
                "A p-value measures evidence against the null, not the size of anything. With "
                "a large enough sample every trivial difference becomes significant."
            ),
            remedy="Report the effect in the metric's own units, plus a standardized effect size.",
            where=where,
        )
    if not has_ci:
        report.add(
            "DSX-STA-003",
            "HIGH",
            f"Result for '{label}' has no confidence interval",
            detail=(
                "The interval carries the precision of the estimate. Without it the reader "
                "cannot distinguish a tight null from an underpowered shrug."
            ),
            remedy=f"Report the {(1 - alpha):.0%} CI as [lower, upper].",
            where=where,
        )
    if effect is not None and has_ci:
        report.ok(f"'{label}' reports effect and interval")

    if p is not None and p == 0:
        report.add(
            "DSX-STA-004", "LOW", f"p-value for '{label}' is reported as exactly 0",
            detail="A p-value is never exactly zero; this is a rounding artefact.",
            remedy="Report as p < 0.001.", where=where,
        )

    if has_ci and effect is not None:
        lower, upper = as_number(ci[0]), as_number(ci[1])
        if lower is not None and upper is not None and not lower <= effect <= upper:
            report.add(
                "DSX-STA-005",
                "HIGH",
                f"Effect for '{label}' lies outside its own confidence interval",
                detail=f"effect={effect:.6g}, CI=[{lower:.6g}, {upper:.6g}].",
                remedy="The estimate and interval disagree — recompute both from the same fit.",
                where=where,
            )
        if lower is not None and upper is not None and p is not None:
            crosses_zero = lower <= 0 <= upper
            if crosses_zero and p < alpha:
                report.add(
                    "DSX-STA-006",
                    "HIGH",
                    f"'{label}' is significant (p={p:.4g}) but its CI includes the null",
                    detail=f"CI=[{lower:.6g}, {upper:.6g}] spans 0 while p < {alpha}.",
                    remedy="p-value and interval are inconsistent. Check they come from the same model.",
                    where=where,
                )
            if not crosses_zero and p >= alpha:
                report.add(
                    "DSX-STA-007",
                    "HIGH",
                    f"'{label}' is not significant (p={p:.4g}) but its CI excludes the null",
                    detail=f"CI=[{lower:.6g}, {upper:.6g}] excludes 0 while p >= {alpha}.",
                    remedy="Reconcile the interval and the test — one of them is from a different model.",
                    where=where,
                )


def _check_practical_significance(
    test: dict, p: float, label: str, where: str, alpha: float, report: Report
) -> None:
    """Practical-significance and effect-magnitude guards (DSX-STA-010/011/012).

    Structural criterion: the recognised effect_size_kind set is exactly the domain of
    mathx.interpret_effect's band table, imported here as EFFECT_SIZE_KINDS so the
    membership guard that PRECEDES interpret_effect cannot drift from the dispatch it
    protects. A kind outside that set fires DSX-STA-012 (MEDIUM) rather than calling
    interpret_effect, whose ValueError-on-unknown-kind must never reach the gate path.
    """
    effect = as_number(test.get("effect"))
    standardized = as_number(test.get("standardized_effect"))
    practical = as_number(test.get("minimum_practical_effect"))

    if p < alpha and practical is not None and effect is not None and abs(effect) < abs(practical):
        report.add(
            "DSX-STA-010",
            "HIGH",
            f"'{label}' is statistically significant but below the practical threshold",
            detail=(
                f"effect={effect:.6g} against a declared minimum practical effect of "
                f"{practical:.6g}. Significance here reflects sample size, not importance."
            ),
            remedy=(
                "Report it as a detected but immaterial difference, and do not let it drive "
                "the recommendation."
            ),
            where=where,
        )

    if p < alpha and standardized is not None:
        kind = normalize(test.get("effect_size_kind", "d"))
        if kind in EFFECT_SIZE_KINDS:
            magnitude = interpret_effect(kind, standardized)
            if magnitude == "negligible":
                report.add(
                    "DSX-STA-011",
                    "MEDIUM",
                    f"'{label}' is significant with a negligible effect size ({kind}={standardized:.3g})",
                    detail="Conventional thresholds place this below the smallest interpretable band.",
                    remedy="Lead the write-up with the magnitude, not the p-value.",
                    where=where,
                )
        elif kind in getattr(mathx, "REPORT_ONLY_EFFECT_KINDS", frozenset()):
            # Cross-plan seam (18-CONTEXT.md D-06, owned jointly with Plan 18-B). A kind in
            # the report-only registry (kappa/ICC/Kendall's W/phi/Cramer's V/tau-b/rho) is
            # RECOGNISED — neither DSX-STA-011 nor DSX-STA-012 fires — because its magnitude
            # is a labeled convention, never a gated threshold (REQ-P18-05: conventions never
            # block). EFFECT_SIZE_KINDS is deliberately NOT widened; interpret_effect's flat
            # abs() band would be statistically wrong for these kinds (Cramer's V is
            # df-dependent; phi/W are unsigned). The registry is read via a defensive
            # module-attribute access with an empty default so this branch is inert until
            # Plan 18-B lands mathx.REPORT_ONLY_EFFECT_KINDS, then activates automatically.
            report.ok(
                f"'{label}' declares effect_size_kind={kind}; magnitude is a labeled "
                "convention, not a gated band"
            )
        else:
            report.add(
                "DSX-STA-012",
                "MEDIUM",
                f"'{label}' declares an unrecognised effect_size_kind ({kind!r})",
                detail=(
                    f"effect_size_kind normalises to {kind!r}, which is not one of the "
                    f"recognised kinds {sorted(EFFECT_SIZE_KINDS)}. The magnitude guard "
                    "(DSX-STA-011) is silently skipped for this test, so a negligible "
                    "effect could pass unflagged."
                ),
                remedy=(
                    "Declare one of d (Cohen's d), h (Cohen's h) or r as the "
                    "effect_size_kind so the magnitude guard applies."
                ),
                where=where,
            )


def _check_null_acceptance(
    test: dict, p: float, label: str, where: str, alpha: float, spec: dict, report: Report
) -> None:
    if p < alpha:
        return
    interpretation = normalize(str(test.get("interpretation", "")))
    null_phrases = ("no_effect", "no_difference", "equivalent", "same", "no_impact", "unchanged")
    if not any(phrase in interpretation for phrase in null_phrases):
        return

    bound = as_number(test.get("equivalence_bound"))
    if bound is None:
        bound = as_number(get(spec, "design.equivalence_bound"))
    ci = test.get("ci")
    ci_ok = False
    if bound is not None and isinstance(ci, (list, tuple)) and len(ci) == 2:
        lo, hi = as_number(ci[0]), as_number(ci[1])
        if lo is not None and hi is not None and abs(lo) <= bound and abs(hi) <= bound:
            ci_ok = True

    tost = test.get("tost") if isinstance(test.get("tost"), dict) else {}
    lower_p = as_number(tost.get("lower_p"))
    upper_p = as_number(tost.get("upper_p"))
    tost_ok = (
        lower_p is not None
        and upper_p is not None
        and lower_p < alpha
        and upper_p < alpha
    )

    detectable = as_number(test.get("detectable_mde"))
    if detectable is None:
        detectable = as_number(get(spec, "results.detectable_mde"))

    if ci_ok or tost_ok:
        report.ok(f"'{label}' null interpretation backed by equivalence/TOST evidence")
        return
    if detectable is not None:
        report.ok(f"'{label}' null interpretation scoped by detectable_mde={detectable}")
        return

    if bound is not None and not ci_ok and not tost_ok:
        report.add(
            "DSX-STA-021",
            "HIGH",
            f"'{label}' declares equivalence_bound={bound:g} but CI/TOST do not prove it",
            detail=(
                "An equivalence bound without a CI wholly inside ±bound (or passing "
                "TOST p-values) does not license a 'no effect' claim."
            ),
            remedy=(
                "Ensure ci lies inside ±equivalence_bound, or report tost.lower_p and "
                "tost.upper_p both below alpha, or set detectable_mde and phrase as inconclusive."
            ),
            where=where,
        )
        return

    report.add(
        "DSX-STA-020",
        "HIGH",
        f"'{label}' interprets p={p:.4g} as evidence of no effect",
        detail=(
            "Failing to reject the null is not evidence for it. The data may simply be too "
            "thin to detect an effect that is present and material."
        ),
        remedy=(
            "Run an equivalence test (TOST) against a declared bound with CI inside ±bound, "
            "or report detectable_mde and phrase the finding as inconclusive."
        ),
        where=where,
    )


def _check_correction_applied(
    spec: dict, pvalues: list[float], alpha: float, report: Report
) -> None:
    if len(pvalues) < 2:
        return
    method = get(spec, "design.multiplicity.correction")
    if is_blank(method) or normalize(method) == "none":
        return  # already raised as DSX-EXP-050
    try:
        adjusted, rejected = apply_correction(str(method), pvalues, alpha)
    except ValueError as exc:
        report.add("DSX-STA-030", "MEDIUM", "Multiplicity correction could not be applied",
                   detail=str(exc), where="spec.design.multiplicity.correction")
        return

    naive = [p < alpha for p in pvalues]
    flipped = [i for i, (n, r) in enumerate(zip(naive, rejected)) if n and not r]
    report.context["adjusted_pvalues"] = [round(p, 6) for p in adjusted]
    if flipped:
        report.add(
            "DSX-STA-031",
            "HIGH",
            f"{len(flipped)} result(s) lose significance after {normalize(method)} correction",
            detail=(
                "Indices "
                + ", ".join(str(i) for i in flipped)
                + f" are significant at raw alpha={alpha} but not after correction. Adjusted "
                "p-values: "
                + ", ".join(f"{adjusted[i]:.4g}" for i in flipped)
            ),
            remedy=(
                "Report the adjusted p-values and revise any claim resting on the uncorrected "
                "ones. Do not present both and pick the friendlier number."
            ),
            where="spec.results.tests",
            flipped_indices=flipped,
        )
    else:
        report.ok(f"all results survive {normalize(method)} correction")


def _check_declared_test(analysis: dict, spec: dict, report: Report) -> None:
    """Compare the declared test against the one the decision table derives.

    Also enforces closed-vocabulary membership for the analysis-block routing fields
    (outcome_type, estimand_kind) — independently of whether a test is declared, so a
    mis-slotted routing value is always a loud DSX-STA-040 (17-CONTEXT.md D-01), never a
    silent no-op.
    """
    if not analysis:
        return

    # Closed-vocabulary membership guard: one DSX-STA-040 per mis-slotted routing field,
    # from a single call site (REQ-P17-05 — reuse the code, mint none). Pure string
    # membership — is_blank short-circuit, then exact normalized equality — with no
    # n_groups / paired coupling. Runs before, and independently of, the declared-test
    # comparison, so both fields are checked even when analysis.test is absent.
    for field_name, vocabulary in _MEMBERSHIP_FIELDS:
        raw = analysis.get(field_name, "")
        if is_blank(raw):
            continue
        value = normalize(raw)
        if value not in vocabulary:
            report.add(
                "DSX-STA-040", "MEDIUM", f"analysis.{field_name} {value!r} is not recognised",
                detail="Allowed: " + ", ".join(sorted(vocabulary)),
                remedy="Declare a recognised value so test selection can be checked.",
                where=f"spec.analysis.{field_name}",
            )

    declared = normalize(analysis.get("test", ""))
    outcome_type = normalize(analysis.get("outcome_type", ""))
    if not declared or not outcome_type:
        return
    if outcome_type not in OUTCOME_TYPES:
        # Already reported by the membership loop above; don't derive a test from an
        # outcome_type the decision table cannot key on.
        return

    n_groups = int(as_number(analysis.get("n_groups")) or 2)
    n_per_group = as_number(analysis.get("n_per_group"))
    recommendation = recommend_test(
        outcome_type,
        n_groups,
        paired=bool(analysis.get("paired")),
        normal=analysis.get("normality_ok"),
        equal_variance=analysis.get("equal_variance"),
        n_per_group=int(n_per_group) if n_per_group else None,
        overdispersed=analysis.get("overdispersed"),
    )
    report.context["recommended_test"] = recommendation

    recommended = str(recommendation["test"])
    acceptable = {recommended} | {
        normalize(alt.split(" ")[0]) for alt in recommendation["alternatives"]  # type: ignore[union-attr]
    }
    if declared not in acceptable:
        report.add(
            "DSX-STA-041",
            "HIGH",
            f"Declared test '{declared}' does not match the data's shape",
            detail=(
                f"For a {outcome_type} outcome across {n_groups} "
                f"{'paired' if analysis.get('paired') else 'independent'} group(s), the "
                f"indicated test is '{recommended}' — {recommendation['rationale']} "
                f"Acceptable alternatives: {', '.join(recommendation['alternatives'])}."  # type: ignore[arg-type]
            ),
            remedy=f"Use '{recommended}' and report {recommendation['effect_size']} as the effect size.",
            where="spec.analysis.test",
            recommended=recommended,
        )
    else:
        report.ok(f"declared test '{declared}' matches the decision table")

    if declared in PARAMETRIC_TESTS:
        unaddressed = [
            name
            for name in ("normality_ok", "equal_variance", "independence_ok")
            if analysis.get(name) is None
        ]
        if unaddressed:
            report.add(
                "DSX-STA-042",
                "MEDIUM",
                f"Parametric test '{declared}' with unassessed assumptions",
                detail="Not declared: " + ", ".join(unaddressed),
                remedy=(
                    "Record each assumption as true/false with the diagnostic used. "
                    "Independence is the one that cannot be fixed after the fact."
                ),
                where="spec.analysis",
            )
        elif analysis.get("independence_ok") is False:
            report.add(
                "DSX-STA-043",
                "CRITICAL",
                "Independence assumption is declared violated",
                detail=(
                    "Non-independent observations invalidate the standard errors of every test "
                    "in the parametric family. Unlike normality, sample size does not rescue it."
                ),
                remedy="Model the dependence structure — clustered SEs, mixed effects, or GEE.",
                where="spec.analysis.independence_ok",
            )


def _check_declared_association(analysis: dict, spec: dict, report: Report) -> None:
    """Dispatch the two declaration-only association/agreement gate groups.

    Sits beside ``_check_declared_test`` (D-01's "hybrid, not fold-in"): the two are
    deliberately independent, so a correlation/agreement declaration is gated on the
    DECLARED estimand_kind and test/agreement fields — never on data (the anti-two-stage
    invariant, REQ-P18-06). Wired at BOTH ``check()`` call sites (the not-tests early
    return and the post-loop return, 18-RESEARCH.md Pattern 2), so a pure declaration-only
    spec with no ``results.tests`` is still gated. The body is split into two private
    helpers by predicate group so each carries its own attributable D-05 docstring
    (18-RESEARCH.md Pattern 1).
    """
    if not analysis:
        return
    _check_correlation_scale_kind(analysis, report)
    _check_agreement_completeness(analysis, report)


def _check_correlation_scale_kind(analysis: dict, report: Report) -> None:
    """DSX-STA-050/051: declared correlation coefficient vs declared scale/kind.

    Citation: rests on the internal Phase-17 estimand_kind/scale definitions
    (dsx/spec.py ESTIMAND_KINDS / OPERAND_SCALES) for the scale->admissible-coefficient
    doctrine; the external doctrinal scale citation is a named, presence-only D-07
    not-in-hand disposition — no fabricated page/section locator is printed
    (18-CONTEXT.md D-07). The DSX-STA-051 routing correction rests on the same internal
    Phase-17 estimand_kind vocabulary.
    Structural criterion: declaration-only string comparison against ANALYSIS-SPEC.yaml's
    analysis: block; never reads results.tests or any computed statistic. DSX-STA-050 fires
    only for Pearson r against a declared-ordinal operand (the ordinal-vs-dichotomous split
    IS D-03's ">2 levels" whitelist — point_biserial and a declared-dichotomous operand
    never reach the firing branch); absent operand_scale is non-blocking.
    """
    declared_test = normalize(analysis.get("test", ""))
    estimand_kind = normalize(analysis.get("estimand_kind", ""))
    operand_scale = normalize(analysis.get("operand_scale", ""))

    if declared_test == "pearson_correlation" and operand_scale == "ordinal":
        report.add(
            "DSX-STA-050",
            "HIGH",
            "Pearson correlation declared against a declared-ordinal operand",
            detail=(
                "Pearson r assumes a linear, interval-or-better scale. An ordinal operand "
                "with more than two ordered levels calls for a monotone rank measure. "
                "(A 2-level operand is declared 'dichotomous' — point-biserial's home — and "
                "is whitelisted; this fires only on a declared 'ordinal' scale.)"
            ),
            remedy=(
                "Redeclare estimand_kind as monotone_association and use "
                "spearman_correlation or kendall_tau_b."
            ),
            where="spec.analysis.test",
        )

    if declared_test in CORRELATION_FAMILY and estimand_kind in ("agreement", "method_comparison"):
        report.add(
            "DSX-STA-051",
            "HIGH",
            f"Correlation coefficient '{declared_test}' declared for a {estimand_kind} estimand",
            detail=(
                "A correlation coefficient measures association, not chance-corrected "
                "agreement or method bias. Correlation is high whenever two raters/methods "
                "move together even under a constant offset — exactly the disagreement "
                "agreement statistics exist to catch."
            ),
            remedy=(
                "Route to kappa/ICC (agreement) or Bland-Altman (method_comparison); "
                "redeclare estimand_kind if the association reading was intended."
            ),
            where="spec.analysis.test",
        )


def _check_agreement_completeness(analysis: dict, report: Report) -> None:
    """DSX-STA-060/061/062: agreement declarations, presence + membership only.

    Citation: Shrout, P.E. and Fleiss, J.L. (1979), Psychological Bulletin 86(2):420-428;
    McGraw, K.O. and Wong, S.P. (1996, corrected edition), Psychological Methods 1(1):30-46
    [the ICC (model, type, definition) triple]. Feinstein, A.R. and Cicchetti, D.V. (1990),
    J. Clin. Epidemiol. 43(6):543-549 (Part I, the two paradoxes) and Cicchetti, D.V. and
    Feinstein, A.R. (1990), 43(6):551-558 (Part II, the p_pos/p_neg reporting
    recommendation) [the kappa companions — the HQ-16-corrected D-04 reading].
    Structural criterion: presence + closed-vocabulary membership over declared sub-fields
    only; never a coherence judgment (ICC combination-coherence is deferred as candidate
    DSX-STA-063, 18-CONTEXT.md D-05) and never a numeric-agreement computation. The weights
    guard branches on isinstance BEFORE any normalize (18-RESEARCH.md Pitfall 5), so an
    explicit weight matrix is never stringified.
    """
    # DSX-STA-060 — ICC declared (an icc dict, or test == icc) without a complete,
    # in-vocabulary (model, type, definition) triple. Presence + membership, fire once.
    icc = analysis.get("icc") if isinstance(analysis.get("icc"), dict) else None
    if icc is not None or normalize(analysis.get("test", "")) == "icc":
        icc = icc or {}
        for field_name, vocab in (
            ("model", ICC_MODELS),
            ("type", ICC_TYPES),
            ("definition", ICC_DEFINITIONS),
        ):
            value = icc.get(field_name)
            if is_blank(value) or normalize(value) not in vocab:
                report.add(
                    "DSX-STA-060",
                    "HIGH",
                    "ICC declared without a complete (model, type, definition) triple",
                    detail=(
                        f"Missing or unrecognised: analysis.icc.{field_name}. "
                        "An ICC value is uninterpretable without all three: the model "
                        "(one_way_random / two_way_random / two_way_mixed), the type "
                        "(single / average) and the definition (consistency / "
                        "absolute_agreement)."
                    ),
                    remedy="Declare all three of analysis.icc.model, .type and .definition.",
                    where=f"spec.analysis.icc.{field_name}",
                )
                break

    # DSX-STA-061 — weighted kappa without recognised weights. isinstance branch BEFORE any
    # normalize: a string is checked against KAPPA_WEIGHT_TOKENS; a non-empty list/tuple is
    # accepted as a declared explicit weight matrix (presence, not validity); anything else
    # (blank / bare number / dict) fires. Never stringifies a matrix (Pitfall 5).
    if normalize(analysis.get("test", "")) == "weighted_kappa":
        weights = analysis.get("weights")
        if isinstance(weights, str):
            weights_ok = normalize(weights) in KAPPA_WEIGHT_TOKENS
        elif isinstance(weights, (list, tuple)):
            weights_ok = len(weights) > 0
        else:
            weights_ok = False
        if not weights_ok:
            report.add(
                "DSX-STA-061",
                "HIGH",
                "Weighted kappa declared without recognised weights",
                detail=(
                    "weighted_kappa needs a declared weighting scheme: 'linear' or "
                    "'quadratic', or an explicit weight matrix. An unweighted kappa is a "
                    "different statistic (declare cohens_kappa instead)."
                ),
                remedy=(
                    "Declare analysis.weights as 'linear', 'quadratic', or an explicit "
                    "weight matrix."
                ),
                where="spec.analysis.weights",
            )

    # DSX-STA-062 — kappa-family test missing either companion. BOTH p_pos AND p_neg are
    # required (D-04, the HQ-16-corrected Feinstein-Cicchetti Part II reading).
    if normalize(analysis.get("test", "")) in ("cohens_kappa", "weighted_kappa", "fleiss_kappa"):
        if is_blank(analysis.get("p_pos")) or is_blank(analysis.get("p_neg")):
            report.add(
                "DSX-STA-062",
                "HIGH",
                "Kappa declared without its p_pos/p_neg companions",
                detail=(
                    "Feinstein & Cicchetti (1990) Part I documents two paradoxes an omnibus "
                    "kappa can hide (high raw agreement with low kappa under skewed "
                    "prevalence, and asymmetric marginals); Part II recommends reporting the "
                    "separate positive and negative agreement proportions alongside it. Both "
                    "p_pos and p_neg are required, not either one."
                ),
                remedy="Declare both analysis.p_pos and analysis.p_neg alongside the kappa.",
                where="spec.analysis",
            )
