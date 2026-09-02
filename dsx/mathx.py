"""Deterministic statistics kernel — stdlib only, no scipy required.

Everything a guardrail needs to *compute* rather than *assert*: normal and
chi-square tails, power and sample size, multiplicity corrections, sequential
boundaries, effect sizes.

Why reimplement instead of importing scipy: these functions run inside blocking
gates. A gate that errors because the user's environment lacks scipy is a gate
that gets disabled. Every function here is pure, dependency-free and unit-tested
against reference values.
"""

from __future__ import annotations

import math
from typing import Sequence

# ── Normal distribution ──────────────────────────────────────────────────────


def norm_cdf(x: float) -> float:
    """Standard normal CDF. Exact to machine precision via ``math.erfc``."""
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def norm_sf(x: float) -> float:
    """Upper tail: P(Z > x)."""
    return 0.5 * math.erfc(x / math.sqrt(2.0))


# Acklam's rational approximation coefficients for the inverse normal CDF.
_A = (
    -3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02,
    1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00,
)
_B = (
    -5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02,
    6.680131188771972e01, -1.328068155288572e01,
)
_C = (
    -7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00,
    -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00,
)
_D = (
    7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00,
    3.754408661907416e00,
)
_P_LOW = 0.02425
_P_HIGH = 1.0 - _P_LOW


def norm_ppf(p: float) -> float:
    """Inverse standard normal CDF (quantile function).

    Acklam's approximation followed by one Halley refinement step, giving
    ~1e-15 absolute accuracy across the representable range.
    """
    if not 0.0 < p < 1.0:
        if p == 0.0:
            return -math.inf
        if p == 1.0:
            return math.inf
        raise ValueError(f"norm_ppf requires 0 < p < 1, got {p!r}")

    if p < _P_LOW:
        q = math.sqrt(-2.0 * math.log(p))
        x = (((((_C[0] * q + _C[1]) * q + _C[2]) * q + _C[3]) * q + _C[4]) * q + _C[5]) / (
            (((_D[0] * q + _D[1]) * q + _D[2]) * q + _D[3]) * q + 1.0
        )
    elif p <= _P_HIGH:
        q = p - 0.5
        r = q * q
        x = (((((_A[0] * r + _A[1]) * r + _A[2]) * r + _A[3]) * r + _A[4]) * r + _A[5]) * q / (
            ((((_B[0] * r + _B[1]) * r + _B[2]) * r + _B[3]) * r + _B[4]) * r + 1.0
        )
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        x = -(((((_C[0] * q + _C[1]) * q + _C[2]) * q + _C[3]) * q + _C[4]) * q + _C[5]) / (
            (((_D[0] * q + _D[1]) * q + _D[2]) * q + _D[3]) * q + 1.0
        )

    # Halley refinement against the exact CDF.
    e = norm_cdf(x) - p
    u = e * math.sqrt(2.0 * math.pi) * math.exp(x * x / 2.0)
    return x - u / (1.0 + x * u / 2.0)


def z_two_sided(alpha: float) -> float:
    """Critical value for a two-sided test at level ``alpha``."""
    _check_prob(alpha, "alpha")
    return norm_ppf(1.0 - alpha / 2.0)


def z_one_sided(alpha: float) -> float:
    _check_prob(alpha, "alpha")
    return norm_ppf(1.0 - alpha)


# ── Chi-square ───────────────────────────────────────────────────────────────


def _lower_gamma_series(a: float, x: float) -> float:
    """Regularized lower incomplete gamma P(a, x) by series expansion."""
    if x <= 0.0:
        return 0.0
    ap = a
    total = 1.0 / a
    term = total
    for _ in range(1000):
        ap += 1.0
        term *= x / ap
        total += term
        if abs(term) < abs(total) * 1e-16:
            break
    return total * math.exp(-x + a * math.log(x) - math.lgamma(a))


def _upper_gamma_cf(a: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(a, x) by continued fraction."""
    tiny = 1e-300
    b = x + 1.0 - a
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 1000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < tiny:
            d = tiny
        c = b + an / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-16:
            break
    return h * math.exp(-x + a * math.log(x) - math.lgamma(a))


def chi2_sf(x: float, df: int) -> float:
    """Upper-tail probability P(X > x) for a chi-square with ``df`` degrees of freedom."""
    if df < 1:
        raise ValueError("df must be >= 1")
    if x <= 0.0:
        return 1.0
    a, xx = df / 2.0, x / 2.0
    if xx < a + 1.0:
        return max(0.0, min(1.0, 1.0 - _lower_gamma_series(a, xx)))
    return max(0.0, min(1.0, _upper_gamma_cf(a, xx)))


def chi2_gof(observed: Sequence[float], expected: Sequence[float]) -> tuple[float, float, int]:
    """Pearson goodness-of-fit. Returns ``(statistic, p_value, df)``."""
    if len(observed) != len(expected):
        raise ValueError("observed and expected must be the same length")
    if len(observed) < 2:
        raise ValueError("need at least two categories")
    if any(e <= 0 for e in expected):
        raise ValueError("expected counts must be strictly positive")
    stat = sum((o - e) ** 2 / e for o, e in zip(observed, expected))
    df = len(observed) - 1
    return stat, chi2_sf(stat, df), df


# ── Sample size and power ────────────────────────────────────────────────────


def sample_size_two_proportions(
    baseline: float, mde_absolute: float, alpha: float = 0.05, power: float = 0.80
) -> int:
    """Per-arm sample size for a two-sided two-proportion test.

    Standard normal approximation with a pooled null variance:

        n = (z_{1-a/2}·sqrt(2·p̄·q̄) + z_{1-b}·sqrt(p1·q1 + p2·q2))² / delta²

    ``mde_absolute`` is in the same units as ``baseline`` (0.02 == 2 percentage
    points). Returns the ceiling — the smallest n that attains the target power.
    """
    _check_prob(baseline, "baseline", exclusive=True)
    _check_prob(alpha, "alpha")
    _check_prob(power, "power")
    if mde_absolute == 0:
        raise ValueError("mde_absolute must be non-zero")

    p1 = baseline
    p2 = baseline + abs(mde_absolute)
    if not 0.0 < p2 < 1.0:
        raise ValueError(f"baseline + mde = {p2} is outside (0, 1)")

    pbar = (p1 + p2) / 2.0
    za = z_two_sided(alpha)
    zb = norm_ppf(power)
    numerator = (
        za * math.sqrt(2.0 * pbar * (1.0 - pbar))
        + zb * math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))
    ) ** 2
    return math.ceil(numerator / (p2 - p1) ** 2)


def sample_size_two_means(
    sd: float, mde_absolute: float, alpha: float = 0.05, power: float = 0.80
) -> int:
    """Per-arm sample size for a two-sided two-sample mean comparison."""
    if sd <= 0:
        raise ValueError("sd must be positive")
    if mde_absolute == 0:
        raise ValueError("mde_absolute must be non-zero")
    _check_prob(alpha, "alpha")
    _check_prob(power, "power")
    za = z_two_sided(alpha)
    zb = norm_ppf(power)
    return math.ceil(2.0 * ((za + zb) ** 2) * (sd**2) / (mde_absolute**2))


def power_two_proportions(
    baseline: float, mde_absolute: float, n_per_arm: int, alpha: float = 0.05
) -> float:
    """Achieved power for a two-sided two-proportion test at a given per-arm n."""
    _check_prob(baseline, "baseline", exclusive=True)
    _check_prob(alpha, "alpha")
    if n_per_arm < 1:
        raise ValueError("n_per_arm must be >= 1")

    p1 = baseline
    p2 = baseline + abs(mde_absolute)
    if not 0.0 < p2 < 1.0:
        raise ValueError(f"baseline + mde = {p2} is outside (0, 1)")

    pbar = (p1 + p2) / 2.0
    za = z_two_sided(alpha)
    se_alt = math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))
    if se_alt == 0:
        return 1.0
    z = (
        abs(p2 - p1) * math.sqrt(n_per_arm)
        - za * math.sqrt(2.0 * pbar * (1.0 - pbar))
    ) / se_alt
    return norm_cdf(z)


def mde_two_proportions(
    baseline: float, n_per_arm: int, alpha: float = 0.05, power: float = 0.80
) -> float:
    """Smallest absolute effect detectable at the given n, alpha and power.

    Solved by bisection on the monotone power curve — no closed form exists once
    the alternative variance depends on the effect.
    """
    _check_prob(baseline, "baseline", exclusive=True)
    if n_per_arm < 1:
        raise ValueError("n_per_arm must be >= 1")

    lo, hi = 1e-9, min(1.0 - baseline, baseline) * 0.999999
    if hi <= lo:
        hi = min(1.0 - baseline, 0.5) * 0.999999
    if power_two_proportions(baseline, hi, n_per_arm, alpha) < power:
        return hi
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if power_two_proportions(baseline, mid, n_per_arm, alpha) < power:
            lo = mid
        else:
            hi = mid
    return hi


# ── Effect sizes ─────────────────────────────────────────────────────────────


def cohens_h(p1: float, p2: float) -> float:
    """Effect size for a difference between two proportions."""
    _check_prob(p1, "p1")
    _check_prob(p2, "p2")
    return 2.0 * math.asin(math.sqrt(p2)) - 2.0 * math.asin(math.sqrt(p1))


def cohens_d(mean1: float, mean2: float, sd1: float, sd2: float, n1: int, n2: int) -> float:
    """Standardized mean difference with a pooled standard deviation."""
    if n1 < 2 or n2 < 2:
        raise ValueError("both groups need n >= 2")
    if sd1 < 0 or sd2 < 0:
        raise ValueError("standard deviations must be non-negative")
    pooled_var = ((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2)
    if pooled_var == 0:
        return 0.0
    return (mean2 - mean1) / math.sqrt(pooled_var)


# The effect-size kinds interpret_effect knows how to band. Hoisted to module
# level as the single source of truth so dsx/checks/stats.py's membership guard
# (DSX-STA-012) tests the same frozenset interpret_effect dispatches on, and the
# recognised set on the two sides cannot drift.
EFFECT_SIZE_KINDS = frozenset({"d", "h", "r"})


def interpret_effect(kind: str, value: float) -> str:
    """Conventional magnitude label. Deliberately conservative wording.

    The recognised set is the module-level EFFECT_SIZE_KINDS, so the caller-side
    membership guard and this dispatch share one source of truth and cannot drift.
    """
    v = abs(value)
    table = {
        "d": ((0.2, "negligible"), (0.5, "small"), (0.8, "medium")),
        "h": ((0.2, "negligible"), (0.5, "small"), (0.8, "medium")),
        "r": ((0.1, "negligible"), (0.3, "small"), (0.5, "medium")),
    }
    if kind not in EFFECT_SIZE_KINDS:
        raise ValueError(
            f"unknown effect kind {kind!r}; expected one of {sorted(EFFECT_SIZE_KINDS)}"
        )
    bands = table[kind]
    for threshold, label in bands:
        if v < threshold:
            return label
    return "large"


# ── Report-only convention bands (Plan 18-B; REQ-P18-05; 18-CONTEXT.md D-06/D-07) ─
#
# LABELED CONVENTIONS for correlation/agreement effect sizes. They are
# RECOGNISED (so a declared convention kind is not mistaken for an unknown) but
# are NEVER used as a blocking magnitude band. This surface is deliberately
# SEPARATE from EFFECT_SIZE_KINDS / interpret_effect (the {d, h, r} blocking
# domain above, which stays frozen). Two reasons widening the blocking domain
# would be WRONG (D-06): (1) it would let DSX-STA-011 adjudicate a convention as
# a gated boundary, violating REQ-P18-05's "never as blocking thresholds"; (2)
# interpret_effect uses a flat abs(value) band, which is statistically wrong for
# these kinds — Cramer's V thresholds are df-dependent, and phi / Kendall's W are
# unsigned with a different null. So the bands live here, report-only, wired only
# into the ungated templates/APA-TABLE-research.md (which mints no finding code).

# The recognition set the DSX-STA-012 branch in dsx/checks/stats.py (Plan 18-A)
# consults: a kind in here is a report-only convention — recognised, but never
# banded by a blocking code. Deliberately DISJOINT from the blocking
# EFFECT_SIZE_KINDS; adding any of these to EFFECT_SIZE_KINDS is the D-06
# prohibition (the firewall test asserts the disjointness and the equality).
REPORT_ONLY_EFFECT_KINDS = frozenset(
    {"kappa", "icc", "kendalls_w", "phi", "cramers_v", "tau_b", "rho"}
)

# Landis & Koch (1977), Biometrics 33(1):159-174 — the published kappa band
# boundaries, PINNED as a LABELED CONVENTION (D-07). Each tuple is
# (upper_bound_inclusive, label). Edge-tie handling — a value that lands exactly
# ON a boundary takes the LOWER band — is a labeled CONVENTION CHOICE here, NOT
# claimed as the paper's exact wording (the published table is stated over
# 2-decimal ranges with gaps at .21/.41/... ; a continuous band needs a tie
# rule, and this is ours). Report-only: never fed into interpret_effect /
# DSX-STA-011.
KAPPA_BANDS_CITATION = "Landis & Koch (1977), Biometrics 33(1):159-174"
KAPPA_BANDS = (
    (0.00, "poor"),
    (0.20, "slight"),
    (0.40, "fair"),
    (0.60, "moderate"),
    (0.80, "substantial"),
    (1.00, "almost perfect"),
)

# Krippendorff's alpha reference value, PINNED at level=ordinal (0.7598,
# confirmed at source, HQ-16 B4 corrected). The value is LEVEL-OF-MEASUREMENT
# DEPENDENT and MUST always carry its level (D-07): the SAME data yields a
# different alpha at each level, so a level-free pin would be wrong. The table is
# level-keyed precisely so the ordinal value is reachable only by asking for the
# ordinal level. Report-only reference value, never on any gate compute path.
KRIPPENDORFF_REFERENCE_CITATION = (
    "Krippendorff's alpha reference value confirmed at source (HQ-16 B4); "
    "level-of-measurement dependent — the value must carry its level"
)
KRIPPENDORFF_REFERENCE = {
    "nominal": 0.4765,
    "ordinal": 0.7598,
    "interval": 0.7574,
    "ratio": 0.6621,
}

# Named CATALOG-ONLY convention entries (D-07): recognised by NAME only, with NO
# numeric boundary and NO fabricated locator. A D-05 read is owed before any of
# these ships a pinned band. Each value is a human-readable note only.
CONVENTION_CATALOG = {
    "icc": (
        "ICC magnitude bands (Koo & Li 2016) — catalog-only: the exact boundary "
        "values are unconfirmed at source, so NO numeric band is pinned here. A "
        "D-05 read is owed before any ICC band ships."
    ),
    "kendalls_w": (
        "Kendall's W magnitude bands — catalog-only: no band citation exists "
        "anywhere in the repo or the HQ-16 pack, so NO numeric boundary is "
        "asserted. A D-05 read is owed before any Kendall's W band ships."
    ),
    "distance_correlation": (
        "Distance correlation (dCor) — catalog/pointer only: no numeric "
        "magnitude band is pinned; the D-13 promotion entry conditions are unmet."
    ),
    "partial_correlation": (
        "Partial correlation — catalog/pointer only: no numeric magnitude band "
        "is pinned."
    ),
    "cronbach_to_omega": (
        "Cronbach's alpha -> McDonald's omega — pointer/redirect only, not a "
        "routing target: catalog-only with deprecation citations, no band."
    ),
}


def label_convention_band(kind: str, value: float) -> str:
    """Report-only magnitude label for a convention effect-size kind.

    DISTINCT from interpret_effect: this is a LABELED CONVENTION, never a gated
    band. It is NEVER called by the blocking DSX-STA-011 guard, and — unlike
    interpret_effect — it does NOT raise for a report-only / catalog-only kind
    (raising would let it masquerade as a blocking guard). For ``kappa`` it
    returns the Landis & Koch (1977) band label (a pinned convention, edge-tie
    to the lower band). For any other kind it returns a "convention, no gated
    boundary" style label, naming the convention so the caller can surface it.
    """
    k = kind.strip().lower() if isinstance(kind, str) else ""
    if k == "kappa":
        for upper, label in KAPPA_BANDS:
            if value <= upper:
                return label
        return "almost perfect"
    # Every other kind (report-only or catalog-only) is a labeled convention with
    # no gated boundary; it never raises, so it can never masquerade as a block.
    return "convention, no gated boundary"


def proportion_diff_ci(
    p1: float, n1: int, p2: float, n2: int, alpha: float = 0.05
) -> tuple[float, float]:
    """Wald confidence interval for ``p2 - p1``."""
    _check_prob(p1, "p1")
    _check_prob(p2, "p2")
    if n1 < 1 or n2 < 1:
        raise ValueError("group sizes must be >= 1")
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z = z_two_sided(alpha)
    diff = p2 - p1
    return diff - z * se, diff + z * se


# ── Multiplicity ─────────────────────────────────────────────────────────────


def bonferroni(pvalues: Sequence[float], alpha: float = 0.05) -> tuple[list[float], list[bool]]:
    """Bonferroni-adjusted p-values and rejection flags."""
    _validate_pvalues(pvalues)
    m = len(pvalues)
    adjusted = [min(1.0, p * m) for p in pvalues]
    return adjusted, [p <= alpha for p in adjusted]


def holm(pvalues: Sequence[float], alpha: float = 0.05) -> tuple[list[float], list[bool]]:
    """Holm-Bonferroni step-down. Controls FWER, uniformly more powerful than Bonferroni."""
    _validate_pvalues(pvalues)
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adjusted = [0.0] * m
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, min(1.0, (m - rank) * pvalues[idx]))
        adjusted[idx] = running
    return adjusted, [p <= alpha for p in adjusted]


def benjamini_hochberg(
    pvalues: Sequence[float], alpha: float = 0.05
) -> tuple[list[float], list[bool]]:
    """Benjamini-Hochberg step-up. Controls FDR under independence or PRDS."""
    _validate_pvalues(pvalues)
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    adjusted = [0.0] * m
    running = 1.0
    for rank in range(m - 1, -1, -1):
        idx = order[rank]
        running = min(running, min(1.0, pvalues[idx] * m / (rank + 1)))
        adjusted[idx] = running
    return adjusted, [p <= alpha for p in adjusted]


CORRECTIONS = {
    "bonferroni": bonferroni,
    "holm": holm,
    "benjamini_hochberg": benjamini_hochberg,
    "bh": benjamini_hochberg,
    "fdr": benjamini_hochberg,
}


def apply_correction(
    method: str, pvalues: Sequence[float], alpha: float = 0.05
) -> tuple[list[float], list[bool]]:
    key = method.strip().lower()
    if key not in CORRECTIONS:
        raise ValueError(
            f"unknown correction {method!r}; expected one of {', '.join(sorted(CORRECTIONS))}"
        )
    return CORRECTIONS[key](pvalues, alpha)


# ── Sequential testing ───────────────────────────────────────────────────────


def obrien_fleming_boundary(k: int, total_looks: int, alpha: float = 0.05) -> float:
    """O'Brien-Fleming z-boundary at interim look ``k`` of ``total_looks``.

    Conservative early, approaching the fixed-horizon critical value at the final
    look. Used to answer the only question that matters at a peeking gate: was the
    observed z compared against the right threshold?
    """
    if not 1 <= k <= total_looks:
        raise ValueError("require 1 <= k <= total_looks")
    return z_two_sided(alpha) * math.sqrt(total_looks / k)


def pocock_boundary(total_looks: int, alpha: float = 0.05) -> float:
    """Constant Pocock z-boundary, tabulated for alpha=0.05 and interpolated elsewhere."""
    if total_looks < 1:
        raise ValueError("total_looks must be >= 1")
    table = {1: 1.960, 2: 2.178, 3: 2.289, 4: 2.361, 5: 2.413, 6: 2.453, 7: 2.485,
             8: 2.512, 9: 2.535, 10: 2.555}
    base = table.get(min(total_looks, 10), 2.555)
    if alpha == 0.05:
        return base
    # Scale the tabulated inflation to the requested alpha.
    return base * z_two_sided(alpha) / 1.959963984540054


def inflation_from_peeking(total_looks: int, alpha: float = 0.05) -> float:
    """Approximate true type-I error when a fixed-horizon test is peeked ``n`` times.

    Interpolated log-linearly between the tabulated anchor values below, then
    scaled by alpha/0.05.

    Citation: Armitage, P., McPherson, C. K. & Rowe, B. C. (1969), "Repeated
    Significance Tests on Accumulating Data", Journal of the Royal Statistical
    Society, Series A (General), volume 132, issue 2, pages 235-244,
    DOI 10.2307/2343787. The anchors below correspond to the paper's normal,
    known-variance, equal-group-size case at a two-sided nominal alpha of
    0.05 — the paper tabulates three distributional cases (binomial, normal,
    exponential), and this is not the only one.
    The full text is subscriber-only at Oxford University Press, Wiley and
    JSTOR. No table number and no page number within the paper was verified —
    naming one would be the fabricated locator brief D-05 exists to prevent.
    Jennison & Turnbull's table is equally unobtainable and is not cited
    either.
    Reference value: the six anchors below (0.083 at 2 looks, 0.107 at 3,
    0.126 at 4, 0.142 at 5, 0.193 at 10, 0.248 at 20) are verified by
    independent computation, not by citation: exact numerical quadrature by
    recursive convolution over the continuation region, cross-checked against
    a seeded Monte Carlo run of four million paths, reproducing 0.08314,
    0.10728, 0.12620, 0.14171, 0.19338 and 0.24793 respectively. The
    widely-circulated figure of 0.246 at twenty looks is wrong; this table's
    0.248 is right — the two independent methods agree at 0.2479, more than
    five Monte Carlo standard errors away from 0.246.
    """
    if total_looks < 1:
        raise ValueError("total_looks must be >= 1")
    anchors = {1: 0.05, 2: 0.083, 3: 0.107, 4: 0.126, 5: 0.142, 10: 0.193, 20: 0.248}
    if total_looks in anchors:
        value = anchors[total_looks]
    else:
        keys = sorted(anchors)
        if total_looks > keys[-1]:
            value = anchors[keys[-1]]
        else:
            lo = max(k for k in keys if k < total_looks)
            hi = min(k for k in keys if k > total_looks)
            weight = (math.log(total_looks) - math.log(lo)) / (math.log(hi) - math.log(lo))
            value = anchors[lo] + weight * (anchors[hi] - anchors[lo])
    return min(1.0, value * alpha / 0.05)


def design_effect(m: float, icc: float) -> float:
    """The factor by which the variance of an estimate is inflated when observations
    inside a cluster are correlated and the analysis is run at a level finer than the
    true dependence unit.

    Citation: Kish, L. (1965), Survey Sampling, section 8.2, page 258
    (design-effect definition) and pages 161-162 (intraclass correlation);
    Higgins, J.P.T., Eldridge, S. and Li, T. (2024), Cochrane Handbook for
    Systematic Reviews of Interventions version 6.5, sections 23.1.4 and
    23.1.4.1.
    Section 8.2 was confirmed for the design-effect definition; no section
    number was confirmed for the design-effect formula itself, and that
    locator is UNVERIFIED — do not invent one.
    Reference value: an intraclass correlation of 0.02 and an average cluster size of
    29.8 yield 1.576 — the Cochrane Handbook's own published worked example.
    """
    if m < 1:
        raise ValueError(f"m (average cluster size) must be >= 1, got {m!r}")
    if not 0.0 <= icc <= 1.0:
        raise ValueError(f"icc (intraclass correlation) must be in [0, 1], got {icc!r}")
    return 1.0 + (m - 1.0) * icc


def diluted_effect(delta_triggered: float, user_trigger_rate: float) -> float:
    """The naive all-up ("diluted") effect obtained by scaling a triggered-subgroup
    effect by the share of the eligible population that triggered.

    Citation: Deng, A. & Hu, V. (2015), "Diluted Treatment Effect Estimation for
    Trigger Analysis in Online Controlled Experiments", WSDM '15, Formula (1) in
    section 2.1, derived in section 3.2; camera-ready at
    https://alexdeng.github.io/public/files/wsdm2015-dilution.pdf, ACM Digital
    Library DOI 10.1145/2684822.2685307. The formula as printed:
    ∆overall = ∆Tr × N_Tr/N. This identity holds under three preconditions
    stated in the same section: the metric is additive, there is no treatment
    effect for untriggered units, and the treatment has no effect on the
    trigger complement.
    Reference value: the paper's own time-to-success counterexample (section
    2.1) publishes a true effect of -26 msec against a naive-formula value of
    -18 msec for that example. Time-to-success is a ratio metric, and the
    paper prints this pair precisely to show the additive formula above does
    not hold there — this function is therefore scoped to additive metrics
    only. The ratio case is Formula (3) in section 3.3; it sums over
    individual users, has no closed-form scalar multiplier, and is
    deliberately not implemented here. The exact triggered effect (∆Tr) and
    user trigger rate (N_Tr/N) behind the published -18 msec are UNVERIFIED —
    the -26/-18 msec pair itself was confirmed in the paper's own text, the
    two individual inputs that multiply to -18 were not. Do not invent them,
    and do not back-solve a pair that happens to multiply to -18.

    ``user_trigger_rate`` is the paper's N_Tr/N — the share of the eligible
    population that triggered. It is deliberately not named ``trigger_rate``:
    the paper's own ``TR`` symbol means a different, per-user quantity
    (section 3.3), and the contract field is
    ``validity_frame.triggering.expected_trigger_rate``, not ``trigger_rate``.
    """
    if not 0.0 <= user_trigger_rate <= 1.0:
        raise ValueError(f"user_trigger_rate must be in [0, 1], got {user_trigger_rate!r}")
    return delta_triggered * user_trigger_rate


def cuped_theta(cov_xy: float, var_x: float) -> float:
    """The CUPED coefficient θ = Cov(Y, X) / Var(X) for a pre-experiment covariate X.

    Citation: Deng, A., Xu, Y., Kohavi, R. & Walker, T. (2013), "Improving the
    Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data",
    WSDM '13, pp. 123-132, DOI 10.1145/2433396.2433413. The adjusted metric is
    Ŷ_cv = Ȳ − θ(X̄ − E[X]) with the variance-minimising θ = Cov(Y, X)/Var(X).
    Reference value: Cov(Y,X)=0.5 and Var(X)=2.0 give θ=0.25.

    This is reference arithmetic only — it is imported by no gate-path check.
    """
    if var_x == 0:
        raise ValueError("var_x must be non-zero; θ is undefined for a degenerate covariate")
    return cov_xy / var_x


def cuped_variance_reduction(rho: float) -> float:
    """The fractional variance reduction ρ² from a pre-experiment covariate correlated
    ρ with the outcome: Var(Ŷ_cv) = Var(Ȳ)(1 − ρ²).

    Citation: Deng, A., Xu, Y., Kohavi, R. & Walker, T. (2013), "Improving the
    Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data",
    WSDM '13, pp. 123-132, DOI 10.1145/2433396.2433413.
    Reference value: the paper's own derived identity ρ=0.5 → variance reduction
    ρ²=0.25 (a 25% reduction; variance ratio 1−ρ²=0.75). The paper's ~50% Bing
    headline is EMPIRICAL (ρ ≈ 0.707), not a derived identity — kept as context only;
    the pinned worked value is ρ²=0.25 at ρ=0.5.

    This is reference arithmetic only — it is imported by no gate-path check.
    """
    if not -1.0 <= rho <= 1.0:
        raise ValueError(f"rho (correlation) must be in [-1, 1], got {rho!r}")
    return rho ** 2


# ── Sample ratio mismatch ────────────────────────────────────────────────────


def srm_test(
    observed: Sequence[int], expected_ratio: Sequence[float]
) -> tuple[float, float, int]:
    """Sample-ratio-mismatch chi-square test.

    ``expected_ratio`` is normalized internally, so ``[1, 1]`` and ``[0.5, 0.5]``
    are equivalent. Returns ``(statistic, p_value, df)``.
    """
    if len(observed) != len(expected_ratio):
        raise ValueError("observed and expected_ratio must be the same length")
    total = sum(observed)
    if total <= 0:
        raise ValueError("total observed count must be positive")
    ratio_sum = sum(expected_ratio)
    if ratio_sum <= 0:
        raise ValueError("expected_ratio must sum to a positive number")
    expected = [total * r / ratio_sum for r in expected_ratio]
    return chi2_gof(observed, expected)


# ── Internals ────────────────────────────────────────────────────────────────


def _check_prob(value: float, name: str, exclusive: bool = False) -> None:
    lo, hi = (0.0, 1.0)
    ok = (lo < value < hi) if exclusive else (lo <= value <= hi)
    if not ok:
        bound = "(0, 1)" if exclusive else "[0, 1]"
        raise ValueError(f"{name} must be in {bound}, got {value!r}")


def _validate_pvalues(pvalues: Sequence[float]) -> None:
    if not pvalues:
        raise ValueError("pvalues must be non-empty")
    for i, p in enumerate(pvalues):
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"pvalues[{i}] = {p!r} is outside [0, 1]")
