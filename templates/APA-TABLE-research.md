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
