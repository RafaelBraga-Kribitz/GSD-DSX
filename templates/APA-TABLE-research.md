# Research statistical results table — APA style (template)

This template is an **optional aid for the research domain** (`dsx.domain == research`),
mirroring `templates/DISCLOSURE-research.md`. It is a **template, not a third-party
dependency**: nothing is installed and nothing is imported.

It **does not replace or relax the marketing-domain ship requirements.** The marketing
ship path still requires a narrative, a sealed figure, and claim evidence, enforced by
the existing `DSX-NAR-*`, `DSX-FIG-*` and `DSX-CLM-*` codes — all unchanged. This table
is an analyst artifact like `EDA.md`: written, read, ungated. It mints no finding code.

## Results table

Report each contrast in one row. Fill every column; delete a column with a one-line
reason if it genuinely does not apply.

| Group / condition | n | M | SD | Statistic (symbol) | df | p | Effect size (kind) | 95% CI |
|---|---|---|---|---|---|---|---|---|
| Control | … | … | … | t = … | … | … | d = … | […, …] |
| Treatment | … | … | … | t = … | … | … | d = … | […, …] |

*Note.* M and SD are the group mean and standard deviation. The statistic column names
the test and its symbol (e.g. *t*, *F*, *χ²*, *U*); *df* are its degrees of freedom; *p*
is the exact two-sided p value (report `p < .001` only below that floor). The effect size
names its kind (Cohen's *d*, Hedges' *g*, Cohen's *h*, …) and the **95% CI** is the
confidence interval **on the effect size**, not on the raw difference unless stated.

**Normality is a declared shape-and-n property, never a test the tool ran to pick the
test.** Do not run a Shapiro-Wilk (or similar) normality test and switch the recommended
test on its result — that is the assumption-checking-as-theatre failure. Follow the fixed
assumption order in `references/test-selection.md`: independence first, then equal variance
(use Welch), then normality (which matters at small *n* only). State the assumed shape and
the per-group *n*, and let those — not a normality test statistic — justify the test.

## Correlation and agreement magnitude bands — labeled conventions, never blocking

These bands are **labeled conventions, not gated thresholds.** They are reported here as an
analyst aid; **conventions never block.** The tool's blocking magnitude guard (via
`mathx.interpret_effect`) is deliberately kept to Cohen's *d* / *h* / *r* only — it is never
widened to adjudicate a correlation or agreement convention, because a flat `abs(value)` band
is statistically wrong for these kinds (Cramér's *V* thresholds are degrees-of-freedom–
dependent; φ and Kendall's *W* are unsigned with a different null). Read these as convention,
apply judgement, and never treat a band edge as a pass/fail line.

**Cohen's / weighted kappa (κ) — Landis & Koch (1977), *Biometrics* 33(1):159–174, a
labeled convention.** Representative bands: κ < 0.00 *poor* · 0.00–0.20 *slight* · 0.21–0.40
*fair* · 0.41–0.60 *moderate* · 0.61–0.80 *substantial* · 0.81–1.00 *almost perfect*.
Handling of a value that lands exactly on a boundary is a labeled convention choice, not the
paper's exact wording.

**Krippendorff's α — reference value 0.7598 at level = ordinal.** The reference value is
**level-of-measurement dependent and must always carry its level**: the same data yields
0.4765 (nominal), 0.7598 (ordinal), 0.7574 (interval), 0.6621 (ratio). A level-free α is
under-specified — always state the level alongside the number.

**ICC (Koo & Li 2016) and Kendall's *W* — named, catalog-only, no numeric band.** These ship
as **named pointers with no boundary values pinned**: the ICC (Koo–Li) boundaries are
unconfirmed at source, and **no band citation exists** for Kendall's *W* anywhere in hand —
so this template asserts no numeric band for either. Distance correlation, partial
correlation, and the Cronbach's α → McDonald's ω redirect are likewise pointer rows only,
with no magnitude band.
