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
    AUTOCORRELATION_HANDLINGS,
    ESTIMAND_KINDS,
    ICC_DEFINITIONS,
    ICC_MODELS,
    ICC_TYPES,
    KAPPA_WEIGHT_TOKENS,
    OPERAND_SCALES,
    POSTHOC_FAMILY_MAP,
    POWER_REPORTING_TYPES,
    PROPORTION_CI_METHODS,
    SPHERICITY_CORRECTIONS,
    VARIANCE_TEST_ROLES,
    VARIANCE_TESTS,
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
    # Phase 19 (REQ-P19-01/02/06/07): the six SCALAR closed-vocab routing fields.
    # A mis-slotted value is loud via the same DSX-STA-040 for free — zero new
    # code for the recognition half. The NESTED analysis.resampling.method and the
    # str-or-list analysis.trend_test are validated in the Wave-2 (19-C) gate
    # helpers, not this flat loop; analysis.dose_score_scheme is deliberately NOT
    # registered here (its gate trigger is dose_scores presence, not membership).
    ("sphericity_correction", SPHERICITY_CORRECTIONS),
    ("autocorrelation_handling", AUTOCORRELATION_HANDLINGS),
    ("variance_test", VARIANCE_TESTS),
    ("variance_test_role", VARIANCE_TEST_ROLES),
    ("power_reporting_type", POWER_REPORTING_TYPES),
    ("proportion_ci_method", PROPORTION_CI_METHODS),
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


# ── Phase 19 dataless routing tables (REQ-P19-01/02/04/05/06/07) ───────────────
#
# Seven pure, DATALESS routing functions modelled EXACTLY on recommend_association:
# each takes ONLY declared-context string argument(s) — NO data, NO n, NO
# distribution flag — normalizes its input, looks up an acceptable SET, and returns
# a dict carrying at least a `tests` frozenset plus a citation label; each raises
# ValueError for an out-of-route declared context. The absence of any data/n
# parameter is the mechanical anti-two-stage proof (REQ-P18-06), asserted by the
# two no-autoswitch modules. NO route ever names a DEPRECATED procedure (D-04):
# no Mauchly-conditional (recommend_rm), no SNK / unprotected-LSD (recommend_posthoc,
# via POSTHOC_FAMILY_MAP), no Wald default (recommend_proportion_ci), no observed /
# post-hoc power (recommend_power). No numeric boundary is encoded (D-07).

# Declared RM measurement kind -> acceptable RM-omnibus SET. The continuous route
# is the UNCONDITIONAL Greenhouse-Geisser one-way RM-ANOVA (the RM analog of
# always-Welch) — never a two-stage / Mauchly-conditional procedure.
_RM_ROUTES: "dict[str, tuple[frozenset[str], str]]" = {
    "continuous": (frozenset({"rm_anova_gg"}), "unconditional Greenhouse-Geisser RM-ANOVA (1959)"),
    "ranks": (frozenset({"friedman", "page_l"}), "Friedman; Page's L for an ordered alternative"),
    "ordinal": (frozenset({"friedman", "page_l"}), "Friedman; Page's L for an ordered alternative"),
    "binary": (frozenset({"cochran_q"}), "Cochran's Q for binary repeated measures"),
}

# Declared trend context -> acceptable ordered-trend SET.
_TREND_ROUTES: "dict[str, tuple[frozenset[str], str]]" = {
    "ordered_trend": (
        frozenset({"cochran_armitage", "jonckheere_terpstra", "mann_kendall", "sens_slope"}),
        "Cochran-Armitage / Jonckheere-Terpstra / Mann-Kendall + Sen's slope",
    ),
    "dose_response": (
        frozenset({"cochran_armitage", "jonckheere_terpstra"}),
        "Cochran-Armitage (declared dose scores) / Jonckheere-Terpstra",
    ),
    "temporal": (
        frozenset({"mann_kendall", "sens_slope"}),
        "Mann-Kendall + Sen's slope (declared autocorrelation handling, Hamed-Rao 1998)",
    ),
}

# Declared variance-test ROLE -> acceptable disposition SET (OQ-6). The
# precondition role's ONLY acceptable disposition is to NOT pretest — use Welch
# unconditionally — so it never endorses a variance pretest as a location gate.
_VARIANCE_ROLE_ROUTES: "dict[str, tuple[frozenset[str], str]]" = {
    "scale_estimand": (
        frozenset({"levene", "brown_forsythe", "fligner_killeen", "bartlett"}),
        "a variance test reported as a scale estimand with a CI (Zimmerman 2004, extended)",
    ),
    "precondition_to_location": (
        frozenset({"use_welch_unconditionally"}),
        "no variance pretest gates the location test — use Welch unconditionally",
    ),
}

# Declared resampling PURPOSE -> acceptable method SET drawn from RESAMPLING_METHODS,
# with the house default. BCa is the house default for an interval; a permutation
# test is the default for a hypothesis test. The full {method, seed, unit, B}
# quadruple is validated in the Wave-2 gate, not here; B's value is never checked.
_RESAMPLING_ROUTES: "dict[str, tuple[frozenset[str], str, str]]" = {
    "interval": (
        frozenset({"percentile_bootstrap", "bca"}), "bca",
        "BCa / percentile bootstrap interval (Efron-Tibshirani 1993; Davidson-MacKinnon 2000)",
    ),
    "confidence_interval": (
        frozenset({"percentile_bootstrap", "bca"}), "bca",
        "BCa / percentile bootstrap interval (Efron-Tibshirani 1993; Davidson-MacKinnon 2000)",
    ),
    "hypothesis_test": (
        frozenset({"permutation"}), "permutation",
        "permutation test for an exchangeable null (Davidson-MacKinnon 2000)",
    ),
    "test": (
        frozenset({"permutation"}), "permutation",
        "permutation test for an exchangeable null (Davidson-MacKinnon 2000)",
    ),
}

# Declared proportion/count CONTEXT -> acceptable interval-method SET, house
# default Wilson. Wald is NEVER a member (Brown-Cai-DasGupta 2001; the n cutoff
# below which Wald misbehaves is confirm-at-source, not encoded).
_PROPORTION_CI_ROUTES: "dict[str, tuple[frozenset[str], str, str]]" = {
    "proportion": (
        frozenset({"wilson", "clopper_pearson", "jeffreys", "agresti_coull"}), "wilson",
        "Wilson score interval, house default (Brown-Cai-DasGupta 2001)",
    ),
    "single_proportion": (
        frozenset({"wilson", "clopper_pearson", "jeffreys", "agresti_coull"}), "wilson",
        "Wilson score interval, house default (Brown-Cai-DasGupta 2001)",
    ),
    "binomial": (
        frozenset({"wilson", "clopper_pearson", "jeffreys", "agresti_coull"}), "wilson",
        "Wilson score interval, house default (Brown-Cai-DasGupta 2001)",
    ),
}

# The power-reporting forms this project ENDORSES — deliberately excludes the
# tautological observed / post-hoc power (Hoenig-Heisey 2001). recommend_power
# routes EVERY recognised reporting type (including a declared observed/post_hoc)
# to this endorsed set, so the misuse is redirected, never echoed back.
_ENDORSED_POWER_FORMS = frozenset({"a_priori", "design", "mde_sensitivity"})
_DEPRECATED_POWER_FORMS = frozenset({"observed", "post_hoc"})


def recommend_rm(measure_kind: str) -> dict[str, object]:
    """Dataless declared-RM-measurement-kind -> acceptable RM-omnibus SET.

    Takes ONLY the declared measurement kind (continuous / ranks / binary) — no
    data, no n, no sphericity estimate. The continuous route is the UNCONDITIONAL
    Greenhouse-Geisser RM-ANOVA and NEVER a two-stage / Mauchly-conditional
    procedure (D-04). Raises ValueError for a non-repeated-measure kind.
    """
    kind = normalize(measure_kind)
    if kind not in _RM_ROUTES:
        raise ValueError(
            f"no repeated-measures routing for measure_kind {measure_kind!r}; "
            f"expected one of {', '.join(sorted(_RM_ROUTES))}"
        )
    tests, citation = _RM_ROUTES[kind]
    return {"tests": tests, "citation": citation}


def recommend_trend(trend_context: str) -> dict[str, object]:
    """Dataless declared-trend-context -> acceptable ordered-trend SET.

    Takes ONLY the declared trend context — no data, no n. Raises ValueError for a
    context with no trend route.
    """
    ctx = normalize(trend_context)
    if ctx not in _TREND_ROUTES:
        raise ValueError(
            f"no trend routing for trend_context {trend_context!r}; "
            f"expected one of {', '.join(sorted(_TREND_ROUTES))}"
        )
    tests, citation = _TREND_ROUTES[ctx]
    return {"tests": tests, "citation": citation}


def recommend_variance_role(role: str) -> dict[str, object]:
    """Dataless declared-variance-test-ROLE -> acceptable disposition SET (OQ-6).

    Takes ONLY the declared role — no data, no n, no location-test result. The
    precondition role NEVER endorses a variance pretest as a location-choice gate:
    its only acceptable disposition is to use Welch unconditionally. Raises
    ValueError for an unrecognised role.
    """
    r = normalize(role)
    if r not in _VARIANCE_ROLE_ROUTES:
        raise ValueError(
            f"no variance-role routing for role {role!r}; "
            f"expected one of {', '.join(sorted(_VARIANCE_ROLE_ROUTES))}"
        )
    tests, citation = _VARIANCE_ROLE_ROUTES[r]
    return {"tests": tests, "citation": citation}


def recommend_resampling(purpose: str) -> dict[str, object]:
    """Dataless declared-resampling-PURPOSE -> acceptable method SET + house default.

    Takes ONLY the declared purpose — no data, no B, no seed. The returned `tests`
    is drawn from RESAMPLING_METHODS with `default` the house choice (BCa for an
    interval). Raises ValueError for an unrecognised purpose.
    """
    p = normalize(purpose)
    if p not in _RESAMPLING_ROUTES:
        raise ValueError(
            f"no resampling routing for purpose {purpose!r}; "
            f"expected one of {', '.join(sorted(_RESAMPLING_ROUTES))}"
        )
    tests, default, citation = _RESAMPLING_ROUTES[p]
    return {"tests": tests, "default": default, "citation": citation}


def recommend_posthoc(omnibus: str) -> dict[str, object]:
    """Dataless declared-OMNIBUS -> acceptable post-hoc SET (exactly POSTHOC_FAMILY_MAP).

    Takes ONLY the declared omnibus (family) — no data, no n. The returned `tests`
    is exactly POSTHOC_FAMILY_MAP[family] and therefore NEVER contains a DEPRECATED
    post-hoc (snk, unprotected_lsd — never a member of any acceptable set, D-04).
    Raises ValueError for an omnibus with no post-hoc family.
    """
    family = normalize(omnibus)
    if family not in POSTHOC_FAMILY_MAP:
        raise ValueError(
            f"no post-hoc routing for omnibus {omnibus!r}; "
            f"expected one of {', '.join(sorted(POSTHOC_FAMILY_MAP))}"
        )
    return {
        "tests": POSTHOC_FAMILY_MAP[family],
        "citation": "protected post-hoc matched to the declared omnibus family "
        "(Games-Howell 1976; Hayter 1986)",
    }


def recommend_power(reporting_type: str) -> dict[str, object]:
    """Dataless declared-power-reporting-TYPE -> ENDORSED reporting-form SET.

    Takes ONLY the declared reporting type — no data, no observed effect. EVERY
    recognised type (including a declared observed / post_hoc) routes to the
    endorsed set {a_priori, design, mde_sensitivity}; the tautological observed /
    post-hoc power is NEVER echoed back as endorsed (Hoenig-Heisey 2001). Raises
    ValueError for an unrecognised reporting type.
    """
    t = normalize(reporting_type)
    if t not in POWER_REPORTING_TYPES:
        raise ValueError(
            f"no power routing for reporting_type {reporting_type!r}; "
            f"expected one of {', '.join(sorted(POWER_REPORTING_TYPES))}"
        )
    return {
        "tests": _ENDORSED_POWER_FORMS,
        "deprecated": _DEPRECATED_POWER_FORMS,
        "citation": "a-priori / design / sensitivity power only; observed and "
        "post-hoc power are tautological (Hoenig-Heisey 2001; Lakens 2022)",
    }


def recommend_proportion_ci(context: str) -> dict[str, object]:
    """Dataless declared-proportion-CONTEXT -> acceptable interval-method SET.

    Takes ONLY the declared context — no data, no n. The returned `tests` contains
    Wilson (house `default`), Clopper-Pearson, Jeffreys and Agresti-Coull and
    NEVER Wald (Brown-Cai-DasGupta 2001; the n cutoff is confirm-at-source, not
    encoded). Raises ValueError for an unrecognised context.
    """
    ctx = normalize(context)
    if ctx not in _PROPORTION_CI_ROUTES:
        raise ValueError(
            f"no proportion-CI routing for context {context!r}; "
            f"expected one of {', '.join(sorted(_PROPORTION_CI_ROUTES))}"
        )
    tests, default, citation = _PROPORTION_CI_ROUTES[ctx]
    return {"tests": tests, "default": default, "citation": citation}


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
            _check_declared_advanced_stats(analysis, spec, report)
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
    _check_declared_advanced_stats(section(spec, "analysis"), spec, report)
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


def _check_declared_advanced_stats(analysis: dict, spec: dict, report: Report) -> None:
    """Dispatch the seven declaration-only Phase-19 advanced-stats gate groups.

    Mirrors ``_check_declared_association`` (D-01's "hybrid, not fold-in"): a thin
    dispatcher over per-family helpers, each carrying its OWN attributable D-05
    docstring (19-RESEARCH.md Pattern 1) because ``gen-finding-catalogue.py`` resolves
    each code's ``Citation:`` from its nearest-enclosing ``FunctionDef`` — a monolith
    emitting all ten under one docstring would launder seven distinct citation
    obligations. Every predicate compares DECLARED strings/structures against a closed
    vocabulary or a presence check — never data (the anti-two-stage invariant,
    REQ-P19-*). Wired at BOTH ``check()`` call sites (the not-tests early return and the
    post-loop return, 19-RESEARCH.md Pattern 2), so a pure declaration-only Phase-19 spec
    with no ``results.tests`` is still gated.
    """
    if not analysis:
        return
    _check_declared_rm_sphericity(analysis, report)
    _check_declared_trend(analysis, report)
    _check_declared_resampling(analysis, report)
    _check_declared_posthoc(analysis, report)
    _check_declared_variance_role(analysis, report)
    _check_declared_power_reporting(analysis, report)
    _check_declared_proportion_count(analysis, report)


def _check_declared_rm_sphericity(analysis: dict, report: Report) -> None:
    """DSX-STA-070: a declared two-stage Mauchly-conditional sphericity correction.

    Citation: Greenhouse, S.W. and Geisser, S. (1959), Psychometrika 24(2):95-112 — the
    unconditional epsilon-adjusted RM-ANOVA this gate steers toward, named as a
    bibliographic locator ONLY: the epsilon is computed from the data at source, never a
    boundary printed here, and this is NOT the reversed 1958 Annals paper. Maxwell, S.E.
    and Delaney, H.D. (2004), Designing Experiments and Analyzing Data, ch.11-12, is a
    catalog-paraphrase for the two-stage critique.
    Structural criterion: declaration-only string comparison against the declared
    analysis.sphericity_correction; fires only on the exact 'mauchly_conditional' two-stage
    token and NEVER on the mere presence of a repeated-measures design (D-06 over-block
    guard — the mixed-model/GEE route has no sphericity step).
    """
    if normalize(analysis.get("sphericity_correction", "")) == "mauchly_conditional":
        report.add(
            "DSX-STA-070",
            "HIGH",
            "Two-stage Mauchly-conditional sphericity correction declared",
            detail=(
                "'mauchly_conditional' is the two-stage 'test Mauchly, then decide whether "
                "to correct' procedure: the pre-test's low power inflates the Type I error "
                "of the conditional path. The house route is the unconditional "
                "Greenhouse-Geisser (or Huynh-Feldt) correction applied always — the RM "
                "analog of always-Welch."
            ),
            remedy=(
                "Declare sphericity_correction as unconditional_gg or unconditional_hf and "
                "apply it unconditionally."
            ),
            where="spec.analysis.sphericity_correction",
        )


def _check_declared_trend(analysis: dict, report: Report) -> None:
    """DSX-STA-080/081: a declared trend test missing its required companion.

    Citation: Cochran, W.G. (1954), Biometrics 10(4):417-451 and Armitage, P. (1955),
    Biometrics 11(3):375-386 [DSX-STA-080, the dose-score requirement]. Hamed, K.H. and
    Rao, A.R. (1998), Journal of Hydrology 204(1-4):182-196 [DSX-STA-081, the
    effective-sample-size autocorrelation correction], named as a bibliographic locator
    ONLY — the lag threshold at which autocorrelation must be handled is NOT hard-coded here.
    Structural criterion: declaration-only presence checks against the declared
    analysis.trend_test (str OR list — non-blank normalized tokens collected into a set) and
    its declared companions. DSX-STA-080 fires on a declared cochran_armitage with
    is_blank(analysis.dose_scores); DSX-STA-081 on a declared mann_kendall/sens_slope with
    is_blank(analysis.autocorrelation_handling) — an is_blank predicate, NOT membership, so a
    declared 'none'/'independent' is non-blank and SATISFIES (Pitfall 5).
    """
    raw = analysis.get("trend_test")
    if isinstance(raw, (list, tuple, set)):
        tokens = {normalize(token) for token in raw if not is_blank(token)}
    elif not is_blank(raw):
        tokens = {normalize(raw)}
    else:
        tokens = set()

    if "cochran_armitage" in tokens and is_blank(analysis.get("dose_scores")):
        report.add(
            "DSX-STA-080",
            "HIGH",
            "Cochran-Armitage trend declared without dose scores",
            detail=(
                "A Cochran-Armitage trend test is defined by the dose scores assigned to the "
                "ordered categories; with a blank analysis.dose_scores the trend is undefined. "
                "The scores must be declared, not inferred from the data."
            ),
            remedy=(
                "Declare analysis.dose_scores (a scheme such as equally_spaced / midrank, or "
                "explicit values)."
            ),
            where="spec.analysis.dose_scores",
        )

    if tokens & {"mann_kendall", "sens_slope"} and is_blank(
        analysis.get("autocorrelation_handling")
    ):
        report.add(
            "DSX-STA-081",
            "HIGH",
            "Mann-Kendall / Sen's slope trend declared without an autocorrelation handling",
            detail=(
                "Mann-Kendall and Sen's slope assume serially independent observations; an "
                "autocorrelated temporal series inflates the trend test unless the handling is "
                "declared. A declared 'none' or 'independent' is a non-blank, explicit "
                "satisfaction — this fires only on a blank declaration."
            ),
            remedy=(
                "Declare analysis.autocorrelation_handling (none / independent if truly iid, or "
                "hamed_rao / prewhitening / yue_pilon)."
            ),
            where="spec.analysis.autocorrelation_handling",
        )


def _check_declared_resampling(analysis: dict, report: Report) -> None:
    """DSX-STA-090: a declared resampling block missing part of its {method, seed, B, unit}.

    Citation: Davidson, R. and MacKinnon, J.G. (2000), Econometric Reviews 19(1):55-68,
    named as catalog-only — B's VALUE is never checked, only its presence (the exactness
    floor vs recommended-minimum-B distinction is confirm-at-source, never printed). Efron,
    B. (1987), JASA 82(397):171-185, is a bibliographic locator ONLY; the BCa acronym is NOT
    attributed to that text.
    Structural criterion: presence-only completeness check over the declared
    analysis.resampling block. Fires ONCE naming the missing member(s) of {method, seed, B,
    unit}; never four codes, never a check of B's value.
    """
    resampling = analysis.get("resampling")
    if not isinstance(resampling, dict):
        return
    missing = [name for name in ("method", "seed", "B", "unit") if is_blank(resampling.get(name))]
    if missing:
        report.add(
            "DSX-STA-090",
            "HIGH",
            "Resampling declared without a complete {method, seed, B, unit} quadruple",
            detail=(
                "A reproducible resample is defined by all four of method, seed, B (the number "
                "of resamples) and unit (the exchangeability unit FOR the resample — cluster/block "
                "vs iid, not a reuse of the design's randomization unit). Missing: "
                f"{', '.join(missing)}. (B's value is not checked — only that it is declared.)"
            ),
            remedy=f"Declare the missing analysis.resampling member(s): {', '.join(missing)}.",
            where="spec.analysis.resampling",
        )


def _check_declared_posthoc(analysis: dict, report: Report) -> None:
    """DSX-STA-100: a declared post-hoc not in the acceptable family for the declared omnibus.

    Citation: Hayter, A.J. (1986), JASA 81(396):1000-1004, named as catalog-only (NOT the
    1984 Annals paper; no numeric alpha printed). Games, P.A. and Howell, J.F. (1976),
    Journal of Educational Statistics 1(2):113-125, a period-correct bibliographic locator.
    Structural criterion: membership test of normalize(analysis.posthoc) against
    POSTHOC_FAMILY_MAP.get(normalize(analysis.omnibus), frozenset()); both fields must be
    non-blank (is_blank short-circuit). A deprecated post-hoc is never a member of any
    acceptable set.
    """
    if is_blank(analysis.get("omnibus")) or is_blank(analysis.get("posthoc")):
        return
    omnibus = normalize(analysis.get("omnibus", ""))
    posthoc = normalize(analysis.get("posthoc", ""))
    if posthoc not in POSTHOC_FAMILY_MAP.get(omnibus, frozenset()):
        report.add(
            "DSX-STA-100",
            "HIGH",
            f"Post-hoc '{posthoc}' is not matched to the declared '{omnibus}' omnibus family",
            detail=(
                "A post-hoc procedure is only valid for the omnibus family whose error "
                "structure it corrects for. The declared post-hoc is not in the acceptable set "
                "for the declared omnibus (a deprecated post-hoc such as SNK is never a member "
                "of any acceptable set)."
            ),
            remedy=(
                "Declare a post-hoc matched to the omnibus family (e.g. games_howell/dunnett_t3 "
                "for welch_anova; dunn/nemenyi for kruskal_wallis)."
            ),
            where="spec.analysis.posthoc",
        )


def _check_declared_variance_role(analysis: dict, report: Report) -> None:
    """DSX-STA-110: a declared variance test used as a location-test precondition.

    Citation: Zimmerman, D.W. (2004), British Journal of Mathematical and Statistical
    Psychology 57(1):173-181, a bibliographic locator. The finding is catalog-scoped to the
    two-group case with an explicit principled-extension flag: the mechanism (a variance
    pre-test gating a location test corrupts the location test's error rate) is invariant to
    group count, but the empirical k-group magnitude is UNVERIFIED. Bancroft, T.A. (1944) is
    a not-in-hand backlog item, named not pinned.
    Structural criterion: keys on the DECLARED analysis.variance_test_role after membership
    of analysis.variance_test in VARIANCE_TESTS — fires on a blank role (declaration
    incompleteness) OR precondition_to_location. SILENT on scale_estimand (the scale test IS
    the correct primary analysis when scale is the estimand); never keys on the presence of
    Levene/BF/Bartlett/Fligner alone (D-06).
    """
    if normalize(analysis.get("variance_test", "")) not in VARIANCE_TESTS:
        return
    role = analysis.get("variance_test_role")
    if is_blank(role) or normalize(role) == "precondition_to_location":
        report.add(
            "DSX-STA-110",
            "HIGH",
            "Variance test declared as a precondition to a location test",
            detail=(
                "Gating a location test (t / ANOVA) on a variance pre-test corrupts the "
                "location test's error rate — the pre-test's own error compounds with it. When "
                "scale is genuinely the estimand, declare variance_test_role: scale_estimand and "
                "the scale test IS the primary analysis. A blank role is a declaration-"
                "incompleteness block."
            ),
            remedy=(
                "Drop the pre-test and use a heteroscedasticity-robust location test (e.g. "
                "Welch), or declare variance_test_role: scale_estimand if scale is the estimand."
            ),
            where="spec.analysis.variance_test_role",
        )


def _check_declared_power_reporting(analysis: dict, report: Report) -> None:
    """DSX-STA-111: a declared observed / post-hoc power reporting.

    Citation: Hoenig, J.M. and Heisey, D.M. (2001), The American Statistician 55(1):19-24,
    named as catalog-only — the observed-power/p-value identity is scope-pinned and this gate
    fires NARROWLY (only observed / post_hoc). Lakens, D. (2022), Collabra: Psychology
    8(1):33267, a bibliographic locator; the MDE-sensitivity framing is the catalog's
    paraphrase, NOT attributed to Lakens.
    Structural criterion: membership of normalize(analysis.power_reporting_type) in
    {observed, post_hoc}. a_priori / design / mde_sensitivity do NOT fire (D-06 narrow;
    broadening is a D-13 deferral).
    """
    if normalize(analysis.get("power_reporting_type", "")) in {"observed", "post_hoc"}:
        report.add(
            "DSX-STA-111",
            "HIGH",
            "Observed / post-hoc power reporting declared",
            detail=(
                "Observed (post-hoc) power is a deterministic transform of the p-value — it "
                "adds no information beyond it and cannot justify accepting a null. Power is a "
                "design-time quantity; report an a-priori power or an MDE-sensitivity analysis "
                "instead."
            ),
            remedy=(
                "Declare power_reporting_type as a_priori, design, or mde_sensitivity; do not "
                "report observed/post-hoc power in a readout."
            ),
            where="spec.analysis.power_reporting_type",
        )


def _check_declared_proportion_count(analysis: dict, report: Report) -> None:
    """DSX-STA-120/121/122: proportion-interval and count-model declaration defects.

    Citation: Brown, L.D., Cai, T.T. and DasGupta, A. (2001), Statistical Science
    16(2):101-133 [DSX-STA-120, the Wald-interval critique — n-independent, the n<=40 cutoff
    is NOT hard-coded]. McCullagh, P. and Nelder, J.A. (1989), Generalized Linear Models
    (2nd ed.), Ch.6 Log-Linear Models, chapter-granular [DSX-STA-121, exposure without offset
    — section 6.2 is NOT pinned]. For DSX-STA-122 the internal completeness doctrine — a point
    NNT ships with its interval because its sampling distribution is discontinuous — with
    Altman, D.G., Deeks, J.J. and Sackett, D.L. (1998), BMJ 317:1309-1312 named as a
    row-bibliography confirm-at-execute item, NOT an owed gate-code read.
    Structural criterion: declaration-only equality/presence checks. DSX-STA-120 fires on
    normalize(analysis.proportion_ci_method) == 'wald' (n-independent). DSX-STA-121 on a
    declared analysis.exposure with is_blank(analysis.offset). DSX-STA-122 on a declared
    analysis.nnt with is_blank(analysis.nnt_ci).
    """
    if normalize(analysis.get("proportion_ci_method", "")) == "wald":
        report.add(
            "DSX-STA-120",
            "HIGH",
            "Wald proportion interval declared",
            detail=(
                "The Wald interval for a proportion has poor coverage (it can even run below 0 "
                "or above 1) and misbehaves worst near 0/1 and at small n — n-independently a "
                "worse default than the score-based alternatives. The n below which it is "
                "unusable is not printed here."
            ),
            remedy=(
                "Declare proportion_ci_method as wilson, clopper_pearson, jeffreys, or "
                "agresti_coull (Wilson is the house default)."
            ),
            where="spec.analysis.proportion_ci_method",
        )
    if not is_blank(analysis.get("exposure")) and is_blank(analysis.get("offset")):
        report.add(
            "DSX-STA-121",
            "HIGH",
            "Exposure declared without an offset",
            detail=(
                "A declared analysis.exposure means the counts are over unequal exposure "
                "windows; a rate model needs that exposure entered as a fixed-coefficient offset "
                "(log exposure), not as a free covariate. A blank analysis.offset leaves the "
                "exposure unmodelled."
            ),
            remedy="Declare analysis.offset (e.g. log_person_years) alongside the exposure.",
            where="spec.analysis.offset",
        )
    if not is_blank(analysis.get("nnt")) and is_blank(analysis.get("nnt_ci")):
        report.add(
            "DSX-STA-122",
            "HIGH",
            "NNT declared without a confidence interval",
            detail=(
                "A point number-needed-to-treat is uninterpretable alone: its sampling "
                "distribution is discontinuous (it passes through infinity when the risk "
                "difference crosses zero), so a declared analysis.nnt must ship with its "
                "interval."
            ),
            remedy="Declare analysis.nnt_ci (the confidence interval) alongside the point NNT.",
            where="spec.analysis.nnt_ci",
        )
