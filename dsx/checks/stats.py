"""Statistical validity checks. Codes DSX-STA-*.

Two jobs. First, a decision table that derives the correct test from the shape of
the data — so "which test?" stops being a judgement call and becomes a lookup.
Second, enforcement of the reporting contract: an effect size and an interval,
every time, because a p-value alone answers a question nobody asked.
"""

from __future__ import annotations

from ..findings import Report
from ..mathx import EFFECT_SIZE_KINDS, apply_correction, interpret_effect
from ..spec import as_number, get, is_blank, items, normalize, section

OUTCOME_TYPES = {"proportion", "continuous", "count", "ordinal", "time_to_event"}

# Tests that assume approximate normality of the sampling distribution.
PARAMETRIC_TESTS = {
    "t_test", "students_t", "welch_t", "paired_t", "anova", "welch_anova",
    "linear_regression", "pearson_correlation", "z_test", "two_proportion_z",
}

NONPARAMETRIC_TESTS = {
    "mann_whitney", "wilcoxon_signed_rank", "kruskal_wallis", "spearman_correlation",
    "fisher_exact", "mcnemar", "chi_square", "permutation_test", "bootstrap",
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
                ["fisher_exact (any expected cell < 5)", "chi_square", "bootstrap"],
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
    """Compare the declared test against the one the decision table derives."""
    if not analysis:
        return
    declared = normalize(analysis.get("test", ""))
    outcome_type = normalize(analysis.get("outcome_type", ""))
    if not declared or not outcome_type:
        return
    if outcome_type not in OUTCOME_TYPES:
        report.add(
            "DSX-STA-040", "MEDIUM", f"analysis.outcome_type {outcome_type!r} is not recognised",
            detail="Allowed: " + ", ".join(sorted(OUTCOME_TYPES)),
            remedy="Declare the outcome's measurement type so test selection can be checked.",
            where="spec.analysis.outcome_type",
        )
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
