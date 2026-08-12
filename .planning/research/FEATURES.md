# Feature Research: DSX Validity Frame (v2.0.0)

**Domain:** Statistical-validity gate checks for marketing data science (online controlled
experiments, frequentist and Bayesian, shared paid-media budgets)
**Researched:** 2026-08-07
**Confidence:** MEDIUM overall — see per-item table. Every numeric claim below was traced to a
named academic source (book, journal article, or arXiv preprint) and, where possible, verified
against the paper's own text via `ar5iv`/PDF extraction rather than a secondary summary. Two
items could not be pinned to an exact number and are marked **UNSOURCED**. No vendor blog,
Medium post, or tool-marketing page is cited anywhere in this document, per D-05 and the
downstream-consumer instruction.

This file answers a narrower and more load-bearing question than the standard FEATURES.md
template: for each new check family, **what is the test oracle?** Section 1 (Reference Value
Ledger) is the primary deliverable and should be read first — it is what REQ-P6…P12 will cite
directly. Sections 2–5 recast the same findings into the standard table-stakes /
differentiators / anti-features framing for roadmap consumption.

---

## 1. Reference Value Ledger

One entry per question in the research brief. Each entry states: primary source, the exact
number or formula, whether it is a **fixed constant**, a **formula to implement**, or requires
**simulation**, and a confidence tier from `classify-confidence`.

### 1.1 Pseudo-replication / unit triad — DSX-VAL-020, DSX-VAL-021

**Primary source:** Kish, L. (1965), *Survey Sampling*, Wiley — origin of the design effect.
Cornfield, J. (1978), "Randomization by Group: A Formal Analysis," *American Journal of
Epidemiology* 108:100–102 — the paper that states the consequence for group/cluster-randomized
trials specifically: ignoring the intraclass correlation and the reduced degrees of freedom
inflates Type-I error, and the inflation worsens as ICC increases. Senn, S. (2021), *Statistical
Issues in Drug Development*, 3rd ed., ch. 8 — already the brief's own chosen docstring citation
for `DSX-VAL-020` (units).

**The formula (testable, deterministic):**

```
DEFF = 1 + (m - 1) * ICC
```

where `m` is the average cluster size (observations per assignment unit) and `ICC` is the
intraclass correlation coefficient. `DEFF` is the **variance inflation factor**: the true
sampling variance of the effect estimate is `DEFF` times the variance a naive iid analysis at
the finer (observation) unit would compute. Because the standard-error / CI half-width scales
with `sqrt(variance)`, the naive interval is too narrow by a factor of `sqrt(DEFF)`, not `DEFF`
itself — this is the precise relationship behind the brief's "3 to 10x too narrow" framing.

**Worked published example:** intraclass correlation (ICC) 0.02, average cluster size 29.8 →
`DEFF = 1 + (29.8 - 1) * 0.02 = 1.576`, from Higgins, Eldridge & Li (2024), *Cochrane Handbook
for Systematic Reviews of Interventions*, version 6.5, §23.1.4 and §23.1.4.1 — the formula and
this worked value appear together in the same freely accessible, versioned subsection. At that
DEFF, the naive interval is `sqrt(1.576) ≈ 1.26x` too narrow.

**Correction (decision D-10, 2026-08-12):** an earlier version of this section asserted a design
effect of `3.45` (from ICC = 0.05, m = 50), attributed to a commonly cited cluster-randomized-
trials methods text and to a Cochrane Handbook section reference. Research established that
neither source actually prints that worked value — it was an unsourced computed illustration,
correct in its arithmetic but not attributable to either cited text, which is precisely the
failure decision D-05 exists to catch. The value has been retired under decision D-10 and
replaced above with the Cochrane Handbook's own worked example, rather than corrected in place,
so a reader who has seen `3.45` in an older document knows it was examined and rejected rather
than merely overlooked.

**Arithmetic illustration, not a published example:** to reach the brief's upper bound of "10x
too narrow" (`sqrt(DEFF) = 10` → `DEFF = 100`) requires a high ICC/large-cluster combination —
e.g. ICC = 0.5, m = 199 → DEFF = 100, or more realistically for repeated-measures account-level
clustering with many sessions per account and high within-account correlation. The "3x too
narrow" end of the range (`sqrt(DEFF)=3` → `DEFF=9`) is reached at, e.g., ICC=0.1, m=81. These
two combinations are computed illustrations reasoning toward the brief's "3 to 10x too narrow"
framing, not values printed in any cited source.

**Testability:** `DEFF = 1 + (m-1)*ICC` is a pure arithmetic formula — the unit test is an exact
arithmetic assertion against the Cochrane Handbook's own worked example (ICC=0.02, m=29.8 →
1.576, Higgins, Eldridge & Li 2024, §23.1.4/§23.1.4.1), not a simulation. **Fixed formula + fixed
worked-example constant.**

**Confidence:** MEDIUM (formula independently confirmed across 3 sources: Kish's original
formulation, the Cochrane Handbook's own m=29.8/ICC=0.02 worked example — verified directly in
the handbook's freely accessible text rather than via a secondary reproduction — and Cornfield's
independent statement of the consequence).

**Implementation note:** `DSX-VAL-020/021` per D-02 does not compute DEFF from data — it
adjudicates the **declaration** (`units.analysis` not finer than `units.assignment`,
`dependence.method_family_required` set when `units.observation != units.assignment`). The
DEFF formula is not needed inside the gate; it is needed in the **test fixture and docstring**
that justify why the check fires, and could optionally power a `dsx explain` illustration (e.g.
"at your declared cluster size and an ICC of 0.05, ignoring clustering would understate your
interval by ~1.9x"). This is a differentiator, not a table-stakes requirement — see §3.

### 1.2 Triggering and dilution — DSX-INT-030

**Primary source:** Deng, A. & Hu, V. (2015), "Diluted Treatment Effect Estimation for Trigger
Analysis in Online Controlled Experiments," *WSDM '15*, pp. 349–358 (Kohavi, Tang & Xu cite
this paper directly in *Trustworthy Online Controlled Experiments*, and the brief's own §7
anchor citation for triggering/dilution is Kohavi, Tang & Xu).

**The relationship (formula to implement, with a documented scope limit):** For **additive
(count/absolute-difference) metrics**, under the standard assumption that untriggered units
have identical treatment and control distributions (they were never exposed to the change), the
diluted (all-up, eligible-population) effect is the triggered-subset effect multiplied by the
trigger rate:

```
delta_diluted ≈ delta_triggered * trigger_rate
```

where `trigger_rate = triggered_users / eligible_users`. This is exact for additive metrics
under the no-effect-on-untriggered assumption; Deng & Hu's paper exists specifically because
**this naive multiplication is provably wrong for ratio metrics** (e.g. click-through rate),
where the numerator and denominator dilute at different rates and a per-subgroup weighted
decomposition is required instead of a single scalar multiplication. I was able to confirm the
paper's framing and abstract (it explicitly states practitioners "often apply approximate or
even wrong formulas") and the general shape of its solution (delta per subgroup, weighted by
trigger rate, then combined) via secondary academic description, but could **not** extract the
paper's exact closed-form equation for the ratio-metric case from the PDF text (extraction
failed; the source is genuine but the precise equation is UNSOURCED at the level of an exact
quotable formula for the ratio case).

**Testability:** The additive-metric case (`delta_diluted = delta_triggered * trigger_rate`) is
a **fixed formula**, testable with an exact worked example (e.g. trigger_rate=0.18,
delta_triggered=+5.0pp → delta_diluted=+0.9pp, matching the brief's own
`validity_frame.triggering.expected_trigger_rate: 0.18` fixture value). The ratio-metric
correction is **UNSOURCED at the precise-equation level** — do not encode a specific ratio-metric
formula in a check or fixture without re-deriving it from the WSDM'15 paper directly (a PDF
with selectable text, or ACM DL access, is needed; this was not available in this research
pass).

**Confidence:** MEDIUM for the additive-metric relationship and its direction (dilution
attenuates the estimate by the trigger rate — this is corroborated by multiple independent
descriptions of the paper and is the textbook framing in Kohavi/Tang/Xu). LOW / UNSOURCED for
the exact ratio-metric formula — **flag explicitly for phase-level research** before `DSX-INT-030`
ships a fixture that exercises ratio metrics.

**What the check should actually adjudicate (D-02 scope):** `DSX-INT-030` fires when
`triggering.analysis_population == "eligible"` and `dilution_adjusted` is not `true` — a
declaration check, not a computation. The formula above belongs in the docstring and in the
fixture's evidence file (showing the arithmetic that makes the undeclared dilution wrong), not
in gate-path code.

### 1.3 Continuous monitoring, Bayesian — DSX-PAR-011 (the critical resolution)

**Primary source:** Deng, A., Lu, J. & Chen, S. (2016), "Continuous Monitoring of A/B Tests
without Pain: Optional Stopping in Bayesian Testing," *IEEE DSAA 2016* (arXiv:1602.05549).
Verified directly against the paper's own text (via `ar5iv` HTML rendering of the arXiv
preprint, not a summary).

**Formulation (a) — point null, unbounded horizon.** The paper's own Section 1 states this
explicitly, in the course of motivating why NHST fails under continuous monitoring: *"An
application of the law of the iterated logarithm shows [that] when incoming data are i.i.d.,
continuous monitoring will inflate Type-I error to 100% when the horizon N goes to infinity."*
This is the frequentist-style framing the brief describes: evaluated against a literal point
null with an unbounded stopping horizon, the probability that "stop when P(B>A) > 0.95" is
eventually triggered by pure noise approaches **1**, with no useful finite ceiling. **There is
no fixed number here** — the defining property of this formulation is that it has no ceiling.
It is demonstrable only as a *trend* (empirical false-stop rate strictly increasing toward 1 as
the simulated horizon N grows), never as a single constant a unit test can assert equality or
a tight bound against.

**Formulation (b) — averaged over the prior, Ville's-inequality-type bound.** The paper's
**Theorem 1** is the coherent-stopping-rule result: conditioning on a posterior-odds threshold
`K`, rejecting the null in favor of the alternative carries a probability of false rejection
bounded by `1/(K+1)` (this is the martingale/optional-stopping mechanism that the wider
anytime-valid-inference literature — e.g. Johari, Koomen, Pekelis & Walsh, "Always Valid
Inference," arXiv:1512.04922 / *Operations Research* 70(3), 2022 — describes using Ville's
(1939) inequality; Deng, Lu & Chen's own proof is the same martingale mechanism, stated as
Theorem 1 rather than by that name). This is bounded, horizon-independent, and it holds for
**any** stopping rule — it is the exact statement of "the posterior odds interpretation is
valid under any stopping rule; the false-positive rate of a decision procedure built on it is
not [uncontrolled] — it is *bounded*."

**The clean, testable number:** DSX-PAR-011's own trigger condition is a decision threshold of
`P(B>A) > 0.95`. In posterior-odds terms, `0.95 / 0.05 = K = 19`. Plugging into the Theorem 1
bound: `1/(K+1) = 1/20 = 0.05`. **This is exact and matches the nominal level** — a coherent
Bayesian stopping rule at the 0.95 posterior-probability threshold has a false-positive rate
averaged over the prior that is bounded by exactly 0.05, not "inflated." The paper's own
**Table 1** simulation (Bayes-factor threshold K=9, δ=0.2, N=100) reports empirical Type-I
error rising from **0.018 (fixed horizon)** to **0.060 (continuous, one- and two-sided
stopping)** — i.e., inflation exists but stays in the neighborhood of nominal (0.05), well
under the corresponding ceiling `1/(9+1)=0.10`, and nowhere near the point-null/LIL
formulation's "approaches 100%."

**Which formulation is testable as a fixed reference value:** Formulation (b), the
prior-averaged/Ville's-inequality bound `1/(K+1)`. It does not depend on horizon length, so a
seeded simulation run to a large but finite N can assert its empirical false-stop rate is `≤
1/(K+1)` (with simulation noise tolerance) as a **fixed pass/fail ceiling**. Formulation (a)
cannot be encoded as a fixed reference value at all — by construction it has none.

**Recommendation for what DSX-PAR-011 should assert:** Assert against the **Ville's-inequality
/ prior-averaged bound, `1/(K+1)`**, not the point-null/LIL framing. Concretely:
`DSX-PAR-011` (a declaration-adjudication check, per D-02) should require
`threshold_calibration: {method: simulation, sims: N, fpr: X}` where `X` is declared not to
exceed `1/(K+1)` for the stated decision threshold (K derived from the declared posterior
probability cutoff), OR an informative prior with justification. The **bad fixture** (per brief
§6.5's "Fixture note for M1") should demonstrate the *wrong* mental model — a weak/flat prior
under naive continuous monitoring evaluated **against a point null over a long horizon**,
showing the false-positive rate climbing well past 0.05 as N grows (formulation a, used
narratively to debunk "a weak prior controls peeking") — while the check's own numeric pass/fail
logic is formulation (b)'s `1/(K+1)` ceiling. Document both explicitly in the docstring so a
future reader cannot mistake which quantity is being asserted (this is exactly the confusion
the brief warns will "look like an implementation bug for a day" if conflated).

**Testability class:** Formula (`1/(K+1)`, a fixed constant given K) for the check's pass/fail
logic; **simulation** (seeded, deterministic RNG) for the bad-fixture narrative demonstrating
formulation (a)'s unbounded growth. Both are needed; they serve different purposes and must not
be swapped.

**Confidence:** HIGH-within-LOW-tooling-ceiling — this is the one claim in this document
verified against the actual equations and table in the primary paper (via `ar5iv`, which
renders the arXiv LaTeX source, not a blog description of it). Tier from `classify-confidence
--provider websearch --verified` = MEDIUM; treat this entry as the strongest MEDIUM in the
ledger given direct textual/table verification.

### 1.4 Continuous monitoring, frequentist — DSX-PAR-010

**Primary source:** Armitage, P., McPherson, C.K. & Rowe, B.C. (1969), "Repeated Significance
Tests on Accumulating Data," *Journal of the Royal Statistical Society: Series A* 132(2):
235–244.

**Already implemented in this codebase.** `dsx/mathx.py::inflation_from_peeking()` already
carries this exact table, cited in its own docstring as "Armitage's classic result":

```python
anchors = {1: 0.05, 2: 0.083, 3: 0.107, 4: 0.126, 5: 0.142, 10: 0.193, 20: 0.248}
```

This independently matches everything found in this research pass: secondary academic sources
(Lakens, *Improving Your Statistical Inferences*, ch. 10, citing Armitage et al. 1969 directly)
report the same anchor points — 5 looks → 0.142, and extending further out, 100 looks → 0.374,
1000 looks → 0.530 — confirming the shape (fast initial climb, slow asymptotic approach,
converging toward 1 only in the limit) and the specific 5-look value exactly. `references/
experiment-pitfalls.md` in this repo already states "five looks pushes the true false-positive
rate to roughly 14%; ten looks to 19%," consistent with the table (0.142, 0.193).

**Testability:** Already a **fixed lookup table + interpolation formula**, already tested
(existing code, existing citation). No new research or new reference value is required.

**Recommendation — this is an anti-feature to avoid, not a feature to build:** Per
`PROJECT.md` decision M-02, `DSX-PAR-010` reads the existing `design.peeking_policy` /
`inference.stopping_rule` concept rather than introducing a parallel vocabulary, and per M-01
it is scoped to fire on a **disjoint trigger** from `DSX-EXP-060` (declared continuous-monitoring
design with no sequential method, vs. undeclared interim looks under a fixed horizon).
**`DSX-PAR-010` should reuse `inflation_from_peeking()` and its existing Armitage citation
rather than deriving or re-citing a new table.** Building a second frequentist-inflation table
for `DSX-PAR-010` would (a) violate D-06's spirit of one stable fact per code, (b) duplicate
work with zero new research value, and (c) risk a second table drifting out of sync with the
first. This is the single clearest "avoid duplicating existing checks" finding in this research
pass.

**Confidence:** HIGH-within-LOW-tooling-ceiling. Cross-verified against the existing,
already-shipped, already-tested implementation plus one independent secondary academic
description (Lakens) reproducing the same anchor values from the same primary paper.

### 1.5 Interference / SUTVA — DSX-INT-*

**Primary source (formal statement):** Imbens, G.W. & Rubin, D.B. (2015), *Causal Inference for
Statistics, Social, and Biomedical Sciences*, Cambridge University Press, ch. 1 (Definition 1.1,
brief's own §7 anchor citation).

**Formal SUTVA statement:** *"The potential outcomes for any unit do not vary with the
treatments assigned to other units, and, for each unit, there are no different forms or
versions of each treatment level, which lead to different potential outcomes."* Two
sub-components are conventionally distinguished (no-interference + no hidden variations of
treatment); the interference sub-component is the one directly relevant to `DSX-INT-*`.

**Published magnitude for auction/marketplace cannibalization bias:** Blake, T. & Coey, D.
(2014), "Why Marketplace Experimentation is Harder than It Seems: The Role of Test-Control
Interference," *Proceedings of the 15th ACM Conference on Economics and Computation (EC '14)*.
Using an eBay email-marketing campaign as an empirical case, the paper reports that **ignoring
test-control interference overstated the campaign's effectiveness by a factor of approximately
2x** (their words, "too large by a factor of around two"), and formally shows via a
supply-and-demand framework that the direction and size of the bias depends on supply
elasticity (larger when supply is more inelastic) and is positive when demand is elastic — i.e.
this is not a fixed universal constant, it is a **domain-specific empirical finding with a
worked example**, not a formula a gate could evaluate from a declaration alone.

**Testability:** The SUTVA definition is a fixed, quotable formal statement (usable verbatim in
a docstring, not a numeric test target). The Blake & Coey "factor of ~2" figure is a **specific
published number from one worked case study** — usable as the citation and worked example
behind a fixture (e.g., "a shared-budget interference case where the naive estimate overstated
the effect ~2x," matching the brief's M1 instruction to encode "at least one interference case"
fixture with a documented post-mortem), but it is **not a general formula the check computes**
— the check (per D-02) adjudicates whether `interference.risk`, `interference.mitigation`, and
`interference.residual_note` are declared, not whether a specific bias magnitude was computed.

**Confidence:** MEDIUM (SUTVA statement independently corroborated via the book's own chapter-1
text; Blake & Coey figure corroborated by two independent descriptions of the same published
paper, both citing "a factor of around two").

### 1.6 Missingness — DSX-VAL-*

**Primary source:** Rubin, D.B. (1976), "Inference and Missing Data," *Biometrika* 63(3):
581–592 (origin of the MCAR/MAR/MNAR taxonomy). Little, R.J.A. & Rubin, D.B., *Statistical
Analysis with Missing Data*, Wiley (brief's own §7 anchor citation), chs. 1 and 3 for the
method-validity implications.

**Decision table (exactly what a declaration-adjudicating gate needs):**

| Mechanism | Definition | Complete-case analysis | Mean/single imputation | Multiple imputation (Rubin 1987) / FIML |
|---|---|---|---|---|
| **MCAR** | Missingness independent of both observed and missing values | Valid (unbiased, but inefficient — loses power, not correctness) | Point estimates unbiased for some parameters; standard errors are wrong | Valid, and recovers the lost efficiency |
| **MAR** | Missingness depends on observed values but not the missing value itself, conditional on those observed values | **Invalid in general** (biased unless missingness happens to be unrelated to the analysis model, which is not guaranteed) | Invalid (biased) | Valid, provided the imputation model conditions on the variables that explain the missingness |
| **MNAR** | Missingness depends on the (unobserved) missing value itself, even after conditioning on observed variables | Invalid | Invalid | **Also invalid** unless a model for the missingness mechanism itself is specified (selection models, pattern-mixture models) — this is an **untestable assumption** requiring declared sensitivity analysis, not a method that "fixes" MNAR |

**Testability:** This is a fixed, closed lookup table — not a formula or simulation. It is
directly implementable as a validity matrix: `DSX-VAL-0xx` fires when `missingness.mechanism`
is `MNAR` and `method_implied` is anything other than a sensitivity-analysis-carrying method
(matching the fixture's own `complete_case_with_sensitivity` value), or when `mechanism` is
`not_assessed` at all (since "not assessed" is not a licensed input to any method-validity
decision). **Fixed constant (a decision table, not a number), high implementability.**

**Confidence:** MEDIUM (the MCAR/MAR/MNAR taxonomy and its method-validity implications are
extremely well established and cross-confirmed across a NIH/PMC methodological review, the
Little & Rubin textbook's own framing as reproduced in multiple independent course/review
sources, and Rubin's original 1976 paper title/abstract). This is about as settled as this
literature gets; the main risk is oversimplifying the MAR row (validity of complete-case
analysis under MAR is more nuanced than a blanket "invalid" in some specific regression
contexts — the check should treat MAR + complete-case as HIGH severity, not necessarily
CRITICAL, to leave room for that nuance; do not hard-code "MAR + complete-case is always
wrong" without a hedge).

### 1.7 Identification strength — DSX-VAL-040/041

**Primary source:** Gelman, A., Simpson, D. & Betancourt, M. (2017), "The Prior Can Often Only
Be Understood in the Context of the Likelihood," *Entropy* 19(10):555 (arXiv:1708.07487; brief's
own §7 anchor citation). Verified directly against the paper's own text via `ar5iv`.

**The testable claim:** The paper's central, quotable thesis: *"The practical utility of a
prior distribution within a given analysis... depends critically on... how it interacts with
the assumed probability model for the data in the context of the actual data that are
observed."* Concretely demonstrated with a **non-identifiability example**: in a Gaussian
process model with parameters `σ` (marginal variance) and `κ` (correlation range), only the
product `σ²√κ` is identified by the likelihood — the individual parameters are not separately
identified from data alone. The paper's demonstrated consequence: *"the prior on κ affects the
posterior for σ"* directly and permanently — i.e., under weak/non identification, the
**posterior along the unidentified dimension is just the prior, reshaped by whatever partial
information the likelihood does carry**, which is precisely the mechanism `DSX-VAL-040`/`041`
needs to adjudicate: identification strength (`strong`/`moderate`/`weak`) crossed with
constraint source (`none`/`informative_priors`/`penalisation`/`design_restriction`/
`hierarchical_pooling`).

The paper also gives a second, numerically concrete worked example (sex-ratio birth-rate study):
a flat/uniform prior on the effect produces a posterior with **99.2% probability of a "real"
effect**, while a weakly informative prior (`sd = 0.005`, chosen from independently known
stability of human sex ratios) collapses the posterior mean to **0.2 percentage points** on
essentially the same data — demonstrating, with an exact quoted pair of numbers, that under
weak identification the conclusion is a property of the prior, not the data.

**Testability:** This is a **conceptual/qualitative claim with one exact worked-numbers pair**
(99.2% vs. 0.2pp), not a general formula. It is not directly implementable as a gate-path
computation (D-02 forbids fitting Gaussian processes or reproducing that exact model in the
gate anyway) — its role is as the **docstring citation and possibly a fixture narrative**
justifying why `identification.strength=weak` + `constraint_source=none` is CRITICAL and why
`identification.strength=strong` + a parameter-scale-informative `constraint_source` is a
"the constraint may be doing the work" flag. **Formula: none to implement. Fixed citation +
narrative worked example only.**

**Conventional VIF thresholds for the collinearity evidence field:** The commonly cited
"VIF > 10" rule of thumb originates with Marquardt, D.W. (1970), "Generalized Inverses, Ridge
Regression, Biased Linear Estimation, and Nonlinear Estimation," *Technometrics* 12(3):
591–612. O'Brien, R.M. (2007), "A Caution Regarding Rules of Thumb for Variance Inflation
Factors," *Quality & Quantity* 41: 673–690, is the standard critique: it explicitly argues
against treating VIF > 10 (or 20, or 40) as an automatic disqualifier, noting the appropriate
threshold depends on sample size, the standard error tolerance the analysis can accept, and
whether the collinear predictor is a nuisance covariate or a variable of direct interest.
**The brief's own example (`VIF > 12`) is consistent with, and slightly above, the
conventional-but-contested "10" threshold** — i.e. it is defensible as evidence of weak
identification, but the check should not hard-code "VIF > 10 ⟹ weak" as a bright line the way
D-02 might tempt; per O'Brien, VIF is evidence to be declared and adjudicated for internal
consistency (declared `strength: weak` should be evidenced by *something* like a VIF figure,
an eigenvalue condition number, or a stated non-identifiability argument — not that VIF crosses
a specific universal number).

**Testability for VIF:** Fixed, citable rule-of-thumb constant (10, with Marquardt as origin
and O'Brien as the standard "don't over-trust this" citation) usable as **evidence-presence**
adjudication (does `identification.evidence` name a concrete diagnostic?), not as a
computed pass/fail threshold inside the gate.

**Confidence:** MEDIUM for the Gelman/Simpson/Betancourt claim and its worked numbers (directly
verified against paper text via `ar5iv`). MEDIUM for VIF > 10 as the conventional threshold and
O'Brien 2007 as its standard critique (both independently corroborated by multiple academic
descriptions, though I did not independently pull O'Brien's exact numeric argument from the
paper's own text — this is a slightly weaker verification than 1.3 and 1.7's Gaussian-process
example).

### 1.8 Novelty and primacy — DSX-INT-*

**Primary source (updated from the brief's citation):** The brief cites Kohavi, Tang & Xu for
novelty/primacy generally, but the specific, formally testable estimator for effect stability
over the measurement window is a dedicated paper: Sadeghi, S., Gupta, S., Gramatovici, S., Lu,
J., Ai, H. & Zhang, R. (2021), "Novelty and Primacy: A Long-Term Estimator for Online
Experiments," arXiv:2102.12893 (Microsoft; later published in *Technometrics* 64(4), 2022).
Verified directly against the paper's own text via `ar5iv`.

**The method (formula to implement, no universal fixed threshold):** The paper models the
expected metric value in period `t` as `μ_t = α + β_t + (τ + δ_(t−t0)) I_t`, where `δ_(t−t0)`
is the user-learning (novelty/primacy) component measured from period `t0+1` onward. It
proposes a **difference-in-differences estimator**:

```
δ̂_t = (T_t − T_1) − (C_t − C_1)
```

(treatment-vs-control change from period 1 to period t, differenced against the corresponding
control-side change), with significance assessed via a standard Wald-type confidence interval,
`δ̂_t ± Φ⁻¹(1 − α/2) × sqrt(Var(δ̂_t))`; the effect is judged "stable" if this interval contains
zero for all `t`, and "novelty" or "primacy" if it does not — **there is no universal numeric
threshold** (e.g. no fixed "% decay in N days" figure); significance is assessed per-experiment
against its own estimated variance, exactly as any DiD confidence interval would be.

**Worked numeric example (MSN.com experiment, from the paper):** day-1 treatment effect =
0.244, 95% CI [0.129, 0.360] (clearly non-null); by day 6 the raw effect becomes
statistically insignificant; the DiD novelty-detection statistic at `t=2` is significantly
negative (`δ̂_2 < 0`, p = 0.0083), i.e. the DiD method successfully flags novelty decay from a
concrete, published pair of numbers.

**Testability:** The DiD formula itself is a **fixed formula to implement** (if DSX ever
computed it — but D-02 forbids computing statistics in the gate path). For a
declaration-adjudicating check, the relevant testable unit is narrower: does
`stability.window` exist, does `stability.novelty_primacy_assessed` = true, and does
`stability.evidence` point to a resolvable artifact (mirroring the existing `DSX-CLM-03x`
evidence-resolution pattern already in this codebase)? **No universal numeric threshold exists
to hard-code** — this is the correct place to explicitly note that no single fixed constant is
available or appropriate, and the check should adjudicate presence-and-resolution of a
stability assessment, not a specific percentage-decay cutoff. The MSN worked example (0.244 →
insignificant by day 6, p=0.0083 at day 2) is usable as a fixture/docstring illustration of
what a real novelty-decay pattern looks like, not as a general pass/fail threshold.

**Confidence:** MEDIUM (directly verified against the paper's own model, formula, and worked
numbers via `ar5iv`). This is a stronger and more specific source than the brief's general
Kohavi/Tang/Xu citation and should be added alongside it, not instead of it (Kohavi/Tang/Xu
remains the right citation for the *qualitative* pattern — "run at least one full week, plot by
day" — already encoded in this repo's own `references/experiment-pitfalls.md`).

---

## 2. Feature Landscape Summary

### Table Stakes (a check is not credible without this)

| Feature | Why Expected | Complexity | Notes |
|---|---|---|---|
| Unit-triad declaration check (`DSX-VAL-020/021`) reusing DEFF citation | Pseudo-replication is the single most common Class A failure named in the brief; the primary source (Kish 1965, Cornfield 1978) and worked example (ICC=0.02,m=29.8→1.576, D-10) are settled | LOW | Declaration-only; DEFF formula lives in docstring/fixture, not gate code |
| Dilution declaration check (`DSX-INT-030`) for additive metrics | Kohavi/Tang/Xu name this as one of the two operating-context-specific failures; additive-metric formula is settled and exact | LOW | Ratio-metric formula is UNSOURCED — restrict the check's worked-example fixture to additive metrics until re-derived |
| `DSX-PAR-010` reusing `inflation_from_peeking()` | Already implemented, already cited, already tested — this is the one item requiring zero new research | LOW | Anti-feature to build a second table; see §3 |
| `DSX-PAR-011` asserting the `1/(K+1)` Ville's-inequality bound | This is D-05's hardest test — the brief explicitly names it "the single most important constraint," and only this formulation of the paper's result yields a fixed testable number | MEDIUM | Requires the point-null/prior-averaged distinction to be stated in the docstring, not just implemented silently |
| SUTVA declaration check (`DSX-INT-0xx`) quoting Imbens & Rubin's formal statement | Interference is one of the three bolded, context-specific failures in the brief | LOW | Formal statement is quotable verbatim; magnitude example (Blake & Coey, ~2x) is fixture material, not gate logic |
| Missingness mechanism-vs-method decision table (`DSX-VAL-0xx`) | Little & Rubin's MCAR/MAR/MNAR taxonomy is exactly the "decision table a declaration-adjudicating gate needs," per the research question itself | LOW | Implement as a literal lookup table; hedge the MAR row (see 1.6) |

### Differentiators

| Feature | Value Proposition | Complexity | Notes |
|---|---|---|---|
| `dsx explain` DEFF illustration (1.1) | Turns an abstract "must not be finer than assignment" rule into a concrete "your interval would be ~Nx too narrow" number for the operator — this is exactly D-04's non-blocking teaching mandate | MEDIUM | Optional; requires accepting a declared or default ICC, which is itself a declaration not a computation, to stay inside D-02 |
| Identification-strength worked-example citation (Gelman/Simpson/Betancourt sex-ratio numbers, 1.7) | Gives `DSX-VAL-040/041` an unusually concrete, quotable "prior did the work" example beyond the abstract principle | LOW | Docstring/fixture material only |
| Novelty/primacy DiD-estimator citation (Sadeghi et al. 2021, 1.8) | Upgrades the citation from a qualitative Kohavi/Tang/Xu pattern to a formally specified, published estimator with a worked numeric example | LOW | Add alongside, not instead of, the brief's Kohavi/Tang/Xu citation |

### Anti-Features (do NOT build)

| Anti-Feature | Why it looks appealing | Why it's a problem | Alternative |
|---|---|---|---|
| A second frequentist peeking-inflation table for `DSX-PAR-010` | Feels natural to give the new check its own self-contained citation | Duplicates `inflation_from_peeking()`, already Armitage-cited and tested; risks the two tables drifting apart, violating D-06's spirit | Reuse `dsx.mathx.inflation_from_peeking()` directly; cite the same Armitage et al. (1969) source in the new check's docstring |
| `DSX-PAR-011` asserting the point-null/LIL formulation as a fixed number | It is the more intuitive "peeking is bad" story, and matches the framing many teams already believe | It has **no ceiling** by construction — cannot satisfy D-05's "test against a published reference value" requirement, since there is no fixed value to assert against | Assert against the prior-averaged Ville's-inequality bound `1/(K+1)`; use the point-null/LIL simulation only as bad-fixture narrative, never as the check's pass/fail logic |
| A ratio-metric dilution formula in `DSX-INT-030`'s fixture or docstring | Ratio metrics (CTR, conversion rate) are extremely common in this domain and it's tempting to cover them immediately | The exact Deng & Hu (2015) ratio-metric correction could not be verified against the paper's own text in this research pass (UNSOURCED at the equation level) | Ship the check and fixture against additive/count metrics first (sourced, exact); open a phase-specific research item to pull the ratio-metric equation from the WSDM'15 paper (ACM DL access or a text-selectable PDF) before extending |
| Hard-coding "VIF > 10" (or 12) as a computed pass/fail gate | Feels like an objective, defensible bright line since it's the most commonly cited threshold | O'Brien (2007), the standard citation for this exact threshold, is itself a paper arguing against treating it as universal | Adjudicate whether `identification.evidence` names *a* concrete diagnostic (VIF, condition number, or explicit non-identifiability argument), not whether a specific number crosses 10 |
| A hard numeric novelty/primacy decay threshold (e.g. "effect must be stable within X% by day Y") | Would make `DSX-INT-*` feel more rigorous and code-like | No such universal threshold exists in the primary literature (Sadeghi et al. 2021's significance test is per-experiment, not a fixed percentage) — inventing one would violate D-05 by laundering a plausible-sounding number with no source | Adjudicate presence and evidence-resolution of a stability assessment (`stability.novelty_primacy_assessed`, `stability.evidence` resolving to an artifact), mirroring the existing `DSX-CLM-03x` evidence pattern |

---

## 3. Feature Dependencies

```
DSX-PAR-010 (frequentist monitoring)
    └──reuses──> dsx.mathx.inflation_from_peeking()  [already shipped, already Armitage-cited]

DSX-PAR-011 (Bayesian monitoring)
    └──requires (D-12)──> DSX-PAR-010 ships in the same milestone (symmetric pair)
    └──depends on──> the point-null vs prior-averaged distinction being resolved in the
                      docstring BEFORE the bad fixture is written (brief §6.5 warning)

DSX-VAL-040/041 (identification strength vs constraint source)
    └──independent of paradigm (D-11)──> must not read `inference.paradigm`
    └──uses──> VIF-as-evidence-presence pattern (not a computed threshold)

DSX-INT-030 (dilution)
    └──scoped to──> additive/count metrics only, pending ratio-metric formula research

DSX-VAL-0xx (missingness)
    └──implements──> Little & Rubin decision table directly, no simulation or computation needed
```

### Dependency Notes

- **`DSX-PAR-011` requires `DSX-PAR-010`:** structurally forced by D-12 (symmetric pairs), and
  practically useful — the frequentist check's reuse of an already-shipped, already-tested
  citation is a template for how cheaply the pair can ship once `DSX-PAR-011`'s harder citation
  question (§1.3) is resolved.
- **`DSX-INT-030` should NOT block on the ratio-metric formula:** shipping the additive-metric
  case first, sourced and exact, and explicitly deferring ratio metrics is more consistent with
  D-05 than blocking the whole check on a paper excerpt that could not be extracted in this pass.

---

## 4. MVP Definition (mapped to the brief's own milestone structure)

The brief and `PROJECT.md` already fix M1 → M2a → M2b → M2c → M3 → M4 → M5; this research does
not re-litigate that ordering (per the brief's own instruction). It does inform what is
*ready to ship with a citation and test oracle today* versus what needs a phase-specific
research spike before the check can satisfy D-05.

### Ready now (sourced, testable, no further research needed)

- [ ] `DSX-VAL-020/021` unit triad — Kish/Cornfield/Senn citation and worked DEFF example ready
- [ ] `DSX-PAR-010` — reuse existing `inflation_from_peeking()`, zero new research
- [ ] `DSX-PAR-011` — Deng/Lu/Chen Theorem 1, `1/(K+1)` bound at K=19 → 0.05, verified against paper text
- [ ] `DSX-INT-0xx` SUTVA declaration — Imbens & Rubin formal statement, Blake & Coey worked magnitude
- [ ] `DSX-VAL-0xx` missingness — Little & Rubin decision table, fully specified above
- [ ] `DSX-VAL-040/041` identification — Gelman/Simpson/Betancourt claim + worked numbers, VIF-as-evidence pattern
- [ ] `DSX-INT-0xx` novelty/primacy — Sadeghi et al. 2021 DiD estimator + Kohavi/Tang/Xu qualitative pattern, both as evidence-presence adjudication

### Needs a phase-specific research spike before shipping (flag per brief §6.6/D-13 style)

- [ ] `DSX-INT-030` ratio-metric dilution formula — Deng & Hu (2015) WSDM paper's exact
  equation for ratio metrics could not be extracted in this pass (PDF text extraction failed;
  needs ACM DL access or a text-selectable copy). **Entry condition to promote:** obtain the
  paper's Section on ratio-metric dilution with a selectable-text source, or find a
  peer-reviewed paper that restates the formula verbatim.

---

## 5. Confidence Assessment

| Question | Primary source | Testability class | Confidence | Notes |
|---|---|---|---|---|
| 1.1 Unit triad / DEFF | Kish 1965; Cornfield 1978; Senn 2021 ch.8 | Fixed formula + worked constant | MEDIUM | 3-source corroboration |
| 1.2 Dilution (additive) | Deng & Hu 2015 (WSDM) | Fixed formula | MEDIUM | Additive case only |
| 1.2 Dilution (ratio) | Deng & Hu 2015 (WSDM) | — | **UNSOURCED** | Exact equation not extracted |
| 1.3 Bayesian monitoring — point-null/LIL | Deng, Lu & Chen 2016 §1 | Simulation, no fixed ceiling | MEDIUM | Verified against paper text |
| 1.3 Bayesian monitoring — Ville's bound | Deng, Lu & Chen 2016, Theorem 1 | Fixed formula (`1/(K+1)`) | MEDIUM | Verified against paper text incl. Table 1 |
| 1.4 Frequentist monitoring | Armitage, McPherson & Rowe 1969 | Fixed table (already shipped) | MEDIUM | Cross-verified against existing code + Lakens |
| 1.5 SUTVA statement | Imbens & Rubin 2015 ch.1 | Fixed quotable statement | MEDIUM | Verified against book text |
| 1.5 Interference magnitude | Blake & Coey 2014 (EC'14) | Worked example (~2x, one case) | MEDIUM | Corroborated by 2 independent descriptions |
| 1.6 Missingness | Rubin 1976; Little & Rubin (Wiley) | Fixed decision table | MEDIUM | MAR row needs a hedge |
| 1.7 Identification (Gelman/Simpson/Betancourt) | Gelman, Simpson & Betancourt 2017 | Qualitative claim + worked numbers | MEDIUM | Verified against paper text |
| 1.7 VIF threshold | Marquardt 1970; O'Brien 2007 | Fixed constant, evidence-presence use only | MEDIUM | O'Brien's own argument text not independently pulled |
| 1.8 Novelty/primacy | Sadeghi et al. 2021 (arXiv/Technometrics) | Formula + worked numbers, no universal threshold | MEDIUM | Verified against paper text |

**Overall:** No LOW-confidence claim is presented as authoritative above; the one genuinely
unresolved item (ratio-metric dilution) is explicitly marked UNSOURCED and routed to a
phase-specific research spike rather than filled with a plausible-sounding number.

---

## Sources

Kish, L. (1965). *Survey Sampling*. Wiley.
Cornfield, J. (1978). "Randomization by Group: A Formal Analysis." *American Journal of
Epidemiology* 108:100–102.
Senn, S. (2021). *Statistical Issues in Drug Development*, 3rd ed., ch. 8. Wiley.
Deng, A. & Hu, V. (2015). "Diluted Treatment Effect Estimation for Trigger Analysis in Online
Controlled Experiments." *WSDM '15*, 349–358.
Deng, A., Lu, J. & Chen, S. (2016). "Continuous Monitoring of A/B Tests without Pain: Optional
Stopping in Bayesian Testing." *IEEE DSAA 2016*. arXiv:1602.05549.
Johari, R., Koomen, P., Pekelis, L. & Walsh, D. (2015/2022). "Always Valid Inference:
Continuous Monitoring of A/B Tests." arXiv:1512.04922; *Operations Research* 70(3):1806–1821.
Armitage, P., McPherson, C.K. & Rowe, B.C. (1969). "Repeated Significance Tests on Accumulating
Data." *JRSS Series A* 132(2):235–244.
Lakens, D. *Improving Your Statistical Inferences*, ch. 10 (secondary corroboration of the
Armitage et al. anchor values).
Imbens, G.W. & Rubin, D.B. (2015). *Causal Inference for Statistics, Social, and Biomedical
Sciences*, ch. 1. Cambridge University Press.
Blake, T. & Coey, D. (2014). "Why Marketplace Experimentation is Harder than It Seems: The Role
of Test-Control Interference." *EC '14*.
Rubin, D.B. (1976). "Inference and Missing Data." *Biometrika* 63(3):581–592.
Little, R.J.A. & Rubin, D.B. *Statistical Analysis with Missing Data*. Wiley.
Gelman, A., Simpson, D. & Betancourt, M. (2017). "The Prior Can Often Only Be Understood in the
Context of the Likelihood." *Entropy* 19(10):555. arXiv:1708.07487.
Marquardt, D.W. (1970). "Generalized Inverses, Ridge Regression, Biased Linear Estimation, and
Nonlinear Estimation." *Technometrics* 12(3):591–612.
O'Brien, R.M. (2007). "A Caution Regarding Rules of Thumb for Variance Inflation Factors."
*Quality & Quantity* 41:673–690.
Sadeghi, S., Gupta, S., Gramatovici, S., Lu, J., Ai, H. & Zhang, R. (2021). "Novelty and
Primacy: A Long-Term Estimator for Online Experiments." arXiv:2102.12893; *Technometrics*
64(4), 2022.
Kohavi, R., Tang, D. & Xu, Y. (2020). *Trustworthy Online Controlled Experiments: A Practical
Guide to A/B Testing*. Cambridge University Press. (Brief's own §7 anchor; qualitative framing
for triggering/dilution/novelty-primacy, superseded in specificity by the dedicated papers
above where they exist.)

**In-repo primary source (verified directly, not researched externally):**
`dsx/mathx.py::inflation_from_peeking()` — existing, shipped, Armitage-cited implementation
that `DSX-PAR-010` should reuse rather than duplicate.

---
*Feature research for: DSX Validity Frame (gsd-dsx v2.0.0)*
*Researched: 2026-08-07*
