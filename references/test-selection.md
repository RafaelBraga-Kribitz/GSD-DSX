# Test selection

Derived, not chosen. `dsx recommend-test <outcome_type> --groups <n>` returns the
same table programmatically and is what the gate checks against.

## Decision table

| Outcome | Groups | Paired | Distribution | Test | Effect size |
|---|---|---|---|---|---|
| proportion | 2 | no | — | two-proportion z (Fisher exact if any expected cell < 5) | risk difference, Cohen's h |
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
