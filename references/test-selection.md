# Test selection

Derived, not chosen. `dsx recommend-test <outcome_type> --groups <n>` returns the
same table programmatically and is what the gate checks against.

## Decision table

| Outcome | Groups | Paired | Distribution | Test | Effect size |
|---|---|---|---|---|---|
| proportion | 2 | no | — | two-proportion z (Boschloo's exact test if any expected cell < 5)[^1] | risk difference, Cohen's h |
| proportion | 2 | yes | — | McNemar | odds ratio |
| proportion | 3+ | no | — | chi-square | Cramér's V |
| continuous | 2 | no | normal or n ≥ 200 | **Welch t** | Cohen's d |
| continuous | 2 | no | skewed and n < 200 | Mann-Whitney | rank-biserial r |
| continuous | 2 | yes | normal differences | paired t | Cohen's dz |
| continuous | 2 | yes | skewed differences | Wilcoxon signed-rank | rank-biserial r |
| continuous | 3+ | no | normal, equal variance | ANOVA | omega² |
| continuous | 3+ | no | normal, unequal variance | Welch ANOVA | omega² |
| continuous | 3+ | no | skewed | Kruskal-Wallis | epsilon² |
| count | any | — | variance ≈ mean | Poisson regression | incidence rate ratio |
| count | any | — | variance > mean | negative binomial | incidence rate ratio |
| ordinal | 2 | no | — | Mann-Whitney | rank-biserial r |
| ordinal | 3+ | no | — | Kruskal-Wallis or ordinal logistic | epsilon² |
| time-to-event | any | — | censored | log-rank, Cox | hazard ratio |

[^1]: The small-expected-cell fallback here is Boschloo's unconditional exact test, not the
    traditional Fisher's exact test. Lydersen, Fagerland and Laake (2009), *Statistics in
    Medicine* 28(7):1159-1175, section 9, states directly that the traditional Fisher's exact
    test should practically never be used, and this is the only uniform power domination found
    anywhere in this project's test-selection research — Boschloo's test never has less power
    than the traditional test it replaces, at every parameter value checked. Locator: section 9,
    verified.

## Notes that change the answer

**Prefer Welch over Student's t always.** It costs almost nothing in power when
variances are equal and stays valid when they are not. Testing for equal variance
first and then choosing is a two-stage procedure with worse properties than just
using Welch.

**The CLT rescues non-normality, not non-independence.** At n ≥ 200 per group the
sampling distribution of the mean is approximately normal regardless of the
underlying skew. No sample size fixes dependent observations — that requires
modelling the dependence (clustered SEs, mixed effects, GEE).

**Heavy tails are different from skew.** With extreme outliers the mean itself
may not be the estimand you want. Consider a trimmed mean, a quantile, or the
median, and say which you chose.

**Non-parametric tests do not test the same hypothesis.** Mann-Whitney tests
stochastic dominance, not equality of means. When the distributions have
different shapes, a significant result does not mean the medians differ.

## Assumptions, in order of how much they matter

1. **Independence** — violation invalidates everything, and sample size does not
   help. This is the one to check first.
2. **Equal variance** — use Welch and stop worrying about it.
3. **Normality** — matters at small n only; irrelevant above ~200 per group.

Reversing this order is the most common way assumption-checking becomes theatre:
elaborate Shapiro-Wilk tests on n = 5,000 while clustered observations go
unmentioned.

## Association / agreement

Derived, not chosen — the human-readable mirror of `recommend_association(estimand_kind)`,
kept in lockstep with the code (standing v2.3 rule). Every row is keyed on the **declared**
`estimand_kind`, never inferred from data (the anti-two-stage invariant, REQ-P18-06):
`recommend_association` takes no data, no `n`, no distribution flag — it is a pure
string→acceptable-coefficient-set lookup. The gate `_check_declared_association` compares
the declared coefficient against the acceptable **set** for that kind (like the decision
table's `alternatives`), so a legitimate Spearman-vs-Kendall choice is never over-blocked.

### Correlation — signed/unsigned dependence

| Declared `estimand_kind` | Acceptable coefficient(s) | Effect size | Primary citation |
|---|---|---|---|
| `linear_association` | Pearson r; point-biserial (Pearson r on a `{0,1}` dichotomy) | r, with a **Fisher-z** confidence interval | Pearson (1896); Fisher (1915) for the z-transform CI |
| `monotone_association` | Spearman ρ; Kendall τ-b | ρ or τ-b (rank statistic, own scale) | Spearman (1904); Kendall (1938) |
| `nominal_association` | φ (2×2); Cramér's V (r × c) | φ / Cramér's V | Cramér (1946) — note V's bands are **df-dependent** |

**Scale gate (DSX-STA-050).** Pearson r declared against a declared-`ordinal` operand
(more than two ordered levels) is a mismatch: Pearson assumes a linear, interval-or-better
scale. Redeclare `monotone_association` and use Spearman ρ or Kendall τ-b. A declared
`dichotomous` (2-level) operand and a declared `point_biserial` are **whitelisted** — a
2-level operand *is* point-biserial's home (Pearson r on `{0,1}`), so neither fires 050
(D-03 whitelist).

**Kind gate (DSX-STA-051).** Any correlation-family coefficient
(`pearson_correlation`, `spearman_correlation`, `kendall_tau_b`, `point_biserial`, `phi`,
`cramers_v`) declared for an `agreement` or `method_comparison` estimand is a routing
error: a correlation coefficient measures association, not chance-corrected agreement or
method bias. Route to κ / ICC (agreement) or Bland-Altman (method comparison).

**Catalog-only pointer rows (no routing target — D-13 entry conditions unmet).**

| Item | Status | Why not routed |
|---|---|---|
| Distance correlation (dCor) | **catalog-only** | Detects non-monotone dependence; no fixture, no numeric boundary shipped (REQ-P18-01) |
| Partial correlation | **catalog-only** | Conditions on a covariate set the declaration does not yet carry; pointer only |

### Agreement / reliability

| Declared form | Coefficient | Companion declaration | Primary citation |
|---|---|---|---|
| `agreement`, nominal, 2 raters | Cohen's κ (`cohens_kappa`) | `p_pos` **and** `p_neg` (DSX-STA-062) | Cohen (1960); Feinstein & Cicchetti (1990) Parts I & II |
| `agreement`, ordinal, 2 raters | weighted κ (`weighted_kappa`) | `weights` ∈ {`linear`, `quadratic`} or an explicit matrix (DSX-STA-061); `p_pos` & `p_neg` (DSX-STA-062) | Cohen (1968) |
| `agreement`, nominal, ≥3 raters | Fleiss' κ (`fleiss_kappa`) | `p_pos` **and** `p_neg` (DSX-STA-062) | Fleiss (1971) |
| `agreement`, any level | Krippendorff's α | reference value **α = 0.7598 @ `level: ordinal`** (the same data yields 0.4765/0.7574/0.6621 at nominal/interval/ratio, so `level` is mandatory) | Krippendorff (2004) |
| `agreement`, continuous, reliability | ICC declared as the (`model`, `type`, `definition`) triple (DSX-STA-060) | `model` ∈ {one_way_random, two_way_random, two_way_mixed}; `type` ∈ {single, average}; `definition` ∈ {consistency, absolute_agreement} | Shrout & Fleiss (1979); McGraw & Wong (1996, corrected) |
| `method_comparison` | Bland-Altman (bias + limits of agreement, in measurement units) | — | Bland & Altman (1986) |

**Kappa companions (DSX-STA-062).** An omnibus κ can hide two paradoxes (high raw
agreement with low κ under skewed prevalence, and asymmetric marginals). Feinstein &
Cicchetti (1990) Part I documents the paradoxes; the companion Part II recommends reporting
the two separate positive/negative agreement proportions. This gate therefore requires
**both** `p_pos` and `p_neg` declared alongside any κ-family test.

**ICC bands (Koo & Li 2016), Kendall's W bands** — **catalog-only, named without numeric
boundaries**: the exact band values are unconfirmed at source (Kendall's W has no band
citation anywhere in hand), so no boundary is printed here until a D-05 read confirms it.

**Cronbach's α → McDonald's ω pointer row.** A reliability declaration resting on Cronbach's
α should redirect to **McDonald's ω**: ω drops α's tau-equivalence assumption, which α
silently requires. This is a **pointer/redirect row, not a routing target** — carried with
the deprecation citation (McDonald (1999); Hayes & Coutts (2020) for the α→ω argument), no
finding code minted.
