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

## Repeated measures

Derived, not chosen — the human-readable mirror of `recommend_rm(measure_kind)`, kept in
lockstep with the code (standing v2.3 rule). Every row is keyed on the **declared** measurement
kind and the declared `analysis.sphericity_correction`, never inferred from data (the
anti-two-stage invariant, REQ-P18-06): `recommend_rm` takes no data, no `n`, no sphericity
estimate — a pure string→acceptable-omnibus-set lookup.

| Declared measurement kind | Acceptable RM omnibus | Effect size | Primary citation |
|---|---|---|---|
| continuous | **unconditional Greenhouse-Geisser one-way RM-ANOVA** (`rm_anova_gg`) | partial η² / generalized η² | Greenhouse & Geisser (1959), *Psychometrika* 24(2):95-112 |
| ranks / ordinal | Friedman (`friedman`); Page's L (`page_l`) for an ordered alternative | Kendall's W | Friedman (1937); Page (1963) |
| binary | Cochran's Q (`cochran_q`) | — | Cochran (1950) |

**Pointer rows (route outward, not a routing target).**

| Item | Status | Points to |
|---|---|---|
| Linear mixed model (LMM) | **pointer** | An unbalanced or missing-cell RM design belongs in a mixed model, not RM-ANOVA |
| GEE | **pointer** | A population-averaged repeated contrast on a non-Gaussian outcome |

**Sphericity is declared and unconditional — never a two-stage Mauchly gate (DSX-STA-070,
Wave 2).** The house recommendation is the **unconditional** Greenhouse-Geisser (or
Huynh-Feldt) correction — the RM analog of always-Welch. The Wave-2 DSX-STA-070 gate fires on
a declared `mauchly_conditional` sphericity_correction (the two-stage "test Mauchly, then decide
whether to correct" procedure), never on `unconditional_gg` / `unconditional_hf`. Greenhouse &
Geisser (1959), *Psychometrika* 24(2):95-112, is cited as a **bibliographic locator only**: the
ε is **computed from the data at source**, never a boundary printed here.

## Trend

Mirror of `recommend_trend(trend_context)`, keyed on the **declared** trend context plus its
declared companions (`analysis.dose_scores`, `analysis.autocorrelation_handling`). Dataless: no
`n`, no distribution — the scores and the autocorrelation handling are **declared**, not read
off the data.

| Declared trend context | Acceptable trend test | Companion declaration required | Primary citation |
|---|---|---|---|
| ordered dose / proportion | Cochran-Armitage (`cochran_armitage`) | `analysis.dose_scores` present | Cochran (1954); Armitage (1955) |
| ordered groups | Jonckheere-Terpstra (`jonckheere_terpstra`) | the ordering declared | Jonckheere (1954); Terpstra (1952) |
| temporal | Mann-Kendall + Sen's slope (`mann_kendall`, `sens_slope`) | `analysis.autocorrelation_handling` present | Mann (1945); Kendall (1975); Sen (1968); Hamed & Rao (1998) for the autocorrelation correction |

**Dose scores are declared (DSX-STA-080, Wave 2).** A declared Cochran-Armitage trend with a
**blank** `analysis.dose_scores` is the Wave-2 trigger: the scores must be declared, not inferred.
**Autocorrelation handling is declared (DSX-STA-081, Wave 2).** A declared Mann-Kendall with a
**blank** `analysis.autocorrelation_handling` fires; a declared `none` / `independent` is
non-blank and **satisfies** (the gate keys on is_blank, not on membership). Hamed & Rao (1998)
is cited for the effective-sample-size correction; the **lag threshold** at which
autocorrelation must be handled is **not printed here — confirm at source**.

## Categorical

Mirror of the categorical routing. **This section mints ZERO finding codes** — REQ-P19-03 is
delivered as rows plus one deprecated row, one surfaced row, one pointer row, and one honesty
footnote only. The absent DSX-STA-06x decade is the deliberate tell.

| Declared table / question | Default test | Effect size | Primary citation |
|---|---|---|---|
| r × c independence | **N-1 chi-square** (the default replacing Yates) | Cramér's V | Campbell (2007), *Statistics in Medicine* 26(19):3661-3675 |
| goodness of fit | exact multinomial (small); Pearson χ² GOF (large) | — | — |
| r × c, likelihood-ratio | G-test | Cramér's V | — |

**Deprecated / surfaced / pointer rows.**

| Item | Status | Why / route |
|---|---|---|
| Yates' continuity correction | **deprecated** | Over-corrects; **use the N-1 chi-square instead** — Campbell (2007), *Stat Med* 26(19):3661-3675. The smallest-expected-count condition (≥ 1) is **confirm-at-source, not printed** as a boundary here. |
| Cochran-Mantel-Haenszel (CMH) with declared stratification (`analysis.cmh_strata`) | **surfaced** | Non-blocking this phase — the CMH-stratifier gate is a named **D-13 deferral**. The declared strata are surfaced, not gated. |
| Log-linear model | **pointer** | A ≥ 3-way contingency structure belongs in a log-linear model — McCullagh & Nelder, *Generalized Linear Models* (2nd ed.), **Ch. 6** (section number confirm-at-source, not pinned) |

[^p19-ffh]: **Fisher-Freeman-Halton honesty footnote.** There is **no practical unconditional
    r × c exact test with a shipping implementation** in hand — the Fisher-Freeman-Halton
    extension is catalog-only, an explicit D-13 entry condition. No fixture, no numeric boundary,
    and no routing target is claimed for it here.

## Resampling

Mirror of `recommend_resampling(purpose)`, keyed on the **declared** `analysis.resampling` block.
Dataless: the purpose is declared, not inferred from the data's shape.

| Declared purpose | Acceptable method | House default | Primary citation |
|---|---|---|---|
| interval / confidence interval | percentile bootstrap; **BCa** | **BCa** (`bca`) | Efron & Tibshirani (1993); Davidson & MacKinnon (2000) |
| hypothesis test | permutation | permutation | Davidson & MacKinnon (2000) |

**The resampling declaration is the full quadruple (DSX-STA-090, Wave 2).** The Wave-2 gate
requires a declared `analysis.resampling` carrying **all four** of `{method, seed,
resampling-unit, B}` — where the **resampling-unit** is the exchangeability unit *for the
resample* (cluster/block vs iid), a dedicated `analysis.resampling.unit` field, **not** a reuse
of the design's randomization unit. **B's value is never checked.** An **exactness floor** (the
smallest B at which the permutation p-value is even attainable) must not be conflated with a
**recommended-minimum B**; both are **confirm-at-source and neither is printed here or gated** —
Davidson & MacKinnon (2000).

## Post-hoc

Mirror of `recommend_posthoc(omnibus)` — the returned set is exactly `POSTHOC_FAMILY_MAP[family]`,
keyed on the **declared** `analysis.omnibus`. Dataless: no `n`, no group means.

| Declared omnibus | Acceptable post-hoc | House default | Primary citation |
|---|---|---|---|
| Welch ANOVA (`welch_anova`) | Games-Howell (`games_howell`); Dunnett's T3 (`dunnett_t3`) | **Games-Howell** | Games & Howell (1976) |
| ANOVA (`anova`) | Tukey HSD / Tukey-Kramer; Dunnett; Scheffé | Tukey-Kramer | Tukey (1953); Kramer (1956); Dunnett (1955); Scheffé (1953) |
| Kruskal-Wallis (`kruskal_wallis`) | Dunn; Nemenyi | Dunn | Dunn (1964) |
| Friedman (`friedman`) | Nemenyi; Conover | Nemenyi | Nemenyi (1963); Conover (1999) |

**Deprecated rows.**

| Item | Status | Why / route |
|---|---|---|
| Student-Newman-Keuls (SNK) | **deprecated** | Does not control the familywise error rate at k ≥ 4; **use a protected post-hoc instead** — Hayter (1986), *JASA* 81(396):1000-1004 |
| Unprotected LSD at k > 3 | **deprecated** | Fisher's LSD is only protected at k = 3; the k = 3 vs k ≥ 4 boundary is **confirm-at-source**, **no numeric α printed** — Hayter (1986), *JASA* 81(396):1000-1004 |

**The post-hoc is matched to the declared omnibus family (DSX-STA-100, Wave 2).** The Wave-2 gate
matches the declared `analysis.posthoc` against the acceptable set for the declared
`analysis.omnibus` family. A deprecated post-hoc (SNK, unprotected LSD at k > 3) is **never a
member** of any acceptable set.

## Proportion and count extras

Mirror of `recommend_proportion_ci(context)` and the count-model pointers, keyed on **declared**
fields. Dataless: no `n` reaches the router — the n-dependent choice is the gate's concern, not
the router's.

| Declared quantity | Acceptable interval / method | House default | Primary citation |
|---|---|---|---|
| single proportion | Wilson score; Clopper-Pearson; Jeffreys; Agresti-Coull | **Wilson** (`wilson`) | Brown, Cai & DasGupta (2001) |
| one-sample count vs a rate | exact binomial / exact Poisson | exact | — |
| risk difference (RD) | Newcombe interval (surfaced) | Newcombe | Newcombe (1998) |
| odds ratio (OR) | Woolf interval (surfaced, not gated) | Woolf | Woolf (1955) |
| number needed to treat (NNT) | NNT **with a mandatory CI** | — | Altman (1998) |

**Pointer / deprecated rows.**

| Item | Status | Why / route |
|---|---|---|
| Zero-inflated / hurdle count model | **pointer** | An excess-zero count structure belongs in a ZIP / hurdle model — pointer only, no routing target this phase |
| Vuong test (ZIP vs standard) | **deprecated** | **Misuse-finding only**: the null sits on the parameter-space boundary, violating Vuong's interior-point prerequisite — Wilson (2015), *Economics Letters* 127:51-53. **No replacement test is endorsed.** |

**Wave-2 gates (DSX-STA-120/121/122).** A declared **Wald** proportion interval fires
DSX-STA-120 (n-independent; the n cutoff below which Wald misbehaves is **not hard-coded** —
Brown, Cai & DasGupta 2001). A declared `analysis.exposure` with **no** `analysis.offset` fires
DSX-STA-121. A declared `analysis.nnt` with **no** `analysis.nnt_ci` fires DSX-STA-122.
