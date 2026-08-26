# DSX Validity Frame: a Class A failure subsystem for GSD-DSX

Seed brief for `/gsd-new-project --auto @brief.md`.

This is an **extension to [GSD-DSX](https://github.com/RafaelBraga-Kribitz/GSD-DSX)**, not a
new capability overlay. It adds five check families, one contract block and one non-blocking
renderer to an existing, installed, tested codebase.

---

## 1. What this is

DSX already covers experiment power, multiplicity, ML leakage, SQL, visualisation, claims,
decision replay and reproducibility. Those checks all assume the layer underneath them is
sound. This subsystem checks that layer: whether the question, the population, the unit of
analysis, the dependence structure, the interference risk, the missingness mechanism, the
measurement and the declared inferential paradigm are coherent enough for any DSX finding to
mean anything.

The operating context is **marketing data science, where roughly 60% of the work is online
controlled experiments**, running under both frequentist and Bayesian paradigms and often on
shared paid-media budgets. The check set is weighted accordingly.

**New finding-code families:**

| Family | Covers |
| --- | --- |
| `DSX-VAL-*` | Validity frame: estimand, unit triad, dependence, sampling frame, missingness, measurement |
| `DSX-INT-*` | Interference and triggering: SUTVA violation, spillover, dilution, novelty and primacy |
| `DSX-PRE-*` | Pre-registered inference plan: declared branch versus executed branch |
| `DSX-PAR-*` | Paradigm adjudication, **symmetric across frequentist and Bayesian by construction** |
| `DSX-ADM-*` | Procedure admissibility (frequentist in v1, Bayesian in v2) |

---

## 2. Problem

A statistically invalid foundation does not fail loudly. It produces confident numbers, clean
charts and a persuasive readout, and it is discovered by someone else, later, at which point
the project and the analyst's credibility go in the bin together.

The failures that do this are recoverable only by collecting new data. Test choice, by
contrast, is recoverable by reanalysis. The scope is therefore weighted almost entirely above
that line.

| Class A failure (unrecoverable) | Mechanism | Covered today? |
| --- | --- | --- |
| No estimand | The question was never a decidable quantity, so nothing computed can answer it | Partial (`decision_rule`) |
| Unit triad mismatch | Observation, assignment and analysis units disagree; pseudo-replication makes intervals 3 to 10x too narrow | Partial (`DSX-EXP-*`) |
| Dependence ignored | Clustered, repeated-measures or temporal data analysed as iid; same consequence | No |
| **Weak identification treated as strong** | Observational, collinear data (MMM: TV, search and social spend all rising together at Black Friday) where the design cannot separate the parameters. Unconstrained estimation returns sign-flipped or absurd coefficients and the readout looks normal. **Paradigm-independent**: it breaks OLS and an unconstrained Bayesian model alike | No |
| **Interference / SUTVA violation** | Shared paid-media budget, marketplace, geo or social spillover. The treatment arm cannibalises control through the auction; the measured effect is a mixture of treatment and cannibalisation | No |
| **Triggering and dilution** | Effect measured on everyone eligible while treatment only reaches the triggered subset; the estimate is attenuated by an unstated factor | No |
| Sampling frame mismatch | The number is correct; the claim is about a population the sample cannot represent | No |
| Post-hoc specification | Test switching, outcome switching, peeking; nominal error rates become fiction | Partial |
| **Prior doing the work instead of the data** | Under a weak prior with continuous monitoring, or an unjustified informative prior, the conclusion is a property of the prior and is invisible in the readout | No |
| Missingness mechanism ignored | Complete-case analysis under MNAR biases every estimate | No |
| Measurement invalidity | The metric does not measure the construct in the claim; no statistical fix exists | Partial (`DSX-MET-*`) |
| Novelty and primacy | Effect is not stable across the measurement window; the reported average describes no ongoing state | No |

The three bolded rows are the ones most specific to this operating context, and they are the
reason this subsystem exists rather than a test catalogue.

---

## 3. Goals, in priority order

1. **Risk reduction.** Make Class A failures blocking findings with computed or
   declaration-checkable evidence, not advice in a prompt.
2. **Operator learning.** Every decision, deterministic or stochastic, is recorded with its
   inputs, the rule applied, the citation behind the rule, and the counterfactual that would
   have changed it.
3. **Portfolio value.** Explicitly tertiary. Do not trade scope or rigour for demo appeal.

### Non-goals for v1

- Computing test statistics or posteriors inside the gate path.
- **Bayesian procedure recommendation and admissibility.** Gated backlog, 6.5.
- **Prior justification, prior sensitivity and convergence declarations.** Gated backlog, 6.5,
  deferred under D-12a because their frequentist counterparts are not written. What *is* in v1
  is the symmetric monitoring pair (M2c), which is a monitoring-discipline check that happens
  to have a Bayesian half, not a Bayesian milestone.
- Causal identification strategy checking. `DSX-CAU-*` owns this.
- Survival, time-series and spatial estimation *methods*. Temporal and spatial dependence are
  first-class declared dependence types; the methods are out.
- Reading a data warehouse from a gate.
- A catalogue of every named statistical test.

---

## 4. Decisions already made (do not re-litigate in discuss)

| ID | Decision | Rationale |
| --- | --- | --- |
| D-01 | Gate path is stdlib-only Python, hermetic, no third-party imports | A gate that breaks on a missing dependency is a gate that gets turned off. Inherited from DSX. |
| D-02 | Gates **adjudicate declarations**, they do not compute statistics or posteriors | Preserves D-01. This is why the Bayesian declaration checks are cheap: none of them fit a model. |
| D-03 | **Extend DSX in place.** One install, one contract file, one gate, one test suite, one catalogue. | The highest-value checks are cross-cutting: procedure admissibility needs the frame *and* the inference plan; unit reconciliation needs the frame *and* the SQL. A check spanning two contracts cannot live cleanly in either of two plugins. Two gates would also need an ordering policy, a threshold intersection nobody wrote down, and duplicated suppression scopes. |
| D-03a | Maintain an **extractable module boundary** anyway: `dsx/frame/` imports nothing from `dsx/checks/` except `Report` and `Finding`; the family ontology lives in `references/families.yaml` as data | If in six months there are still no upward imports, extraction is a `git filter-repo`. If there are, the separation was never real. |
| D-04 | **Never block to teach.** Gates emit a machine-readable decision record; the non-blocking `dsx explain` renders it as a lesson. | A gate that stops to explain is disabled on a deadline, losing both the guardrail and the lesson. |
| D-05 | No check ships without (a) a citation to a primary source in its docstring and (b) a test against a published reference value | Prevents laundering a language model's statistics knowledge into code carrying the authority of a blocking gate. **The single most important constraint in the project.** If velocity pressure arrives, cut checks, never this. |
| D-06 | Finding codes are never renumbered | A suppression written today stays valid. Inherited from DSX. |
| D-07 | **Resolved by D-03:** codes live in the DSX namespace, prefixed per family as listed in section 1 | No second namespace to reconcile. |
| D-08 | Fixtures are the contract: `examples/good-ANALYSIS-SPEC.yaml` passes every gate at every threshold; `examples/bad-ANALYSIS-SPEC.yaml` is blocked by every gate. Both are extended, not replaced. | Inherited from DSX. Installer self-test asserts both. |
| D-09 | Adversarial framing questions are a **fixed interrogation**, not free-form challenge | Told to challenge freely, an agent either agrees or manufactures objections, and the operator cannot tell which. Fixed questions are reliable and their answers are gate-checkable. |
| D-10 | **An unsupported or unimplemented paradigm is never a blocking finding on its own.** It emits an informational manifest naming which checks ran and which did not. | Blocking on `paradigm: bayesian` makes typing `frequentist` the cheapest way past the gate. That is the exact distortion this subsystem exists to prevent. |
| D-11 | **Frame-layer checks never read `paradigm`.** | Estimand, units, dependence, interference, triggering, sampling frame, missingness and measurement are paradigm-independent. A prior does not save you from pseudo-replication. If a frame check needs to branch on paradigm, it is in the wrong layer. |
| D-12 | **Paradigm-specific checks ship in symmetric pairs.** Every rigour requirement imposed on one paradigm must have its counterpart on the other, or neither ships. | Asymmetric enforcement is how a tool silently steers method choice. The `DSX-PAR-*` family name exists to make the symmetry structural rather than remembered. |
| D-12a | **D-12 is also the scoping rule, not only the fairness rule.** A paradigm-specific check is in scope when its counterpart is also in scope. If one half of a pair has no counterpart written, both halves defer together. | This resolves what would otherwise be an estimate-driven scope argument. It is what moves prior sensitivity and convergence out of v1 (section 6.5) and what keeps the monitoring pair in (M2c). |
| D-13 | **Deferred checks carry an entry condition, not a wish.** Every item in section 6.5 names the evidence from the M5 corpus that promotes it. Items with no stated entry condition are removed from the backlog, not carried. | "We estimate this matters" is how a backlog becomes a graveyard. A trigger tied to a measured catch rate is falsifiable; a priority is not. |
| D-14 | **Reversing any decision in this table requires a reversal record**: the decision, the new evidence, and what would have made the original correct. A reversal with no new evidence is itself a finding, logged as `SELF-001` in `.planning/REVERSALS.md`. | The decision record in 5.5 exists because "here is what I chose" is weaker than "here is what would change it." That discipline should apply to this table before it applies to anyone's analysis. Three decisions in this brief were already reversed during drafting; two had new evidence and one did not. |

---

## 5. The contract

Everything below is an **extension to `ANALYSIS-SPEC.yaml`**, written before the data is
touched. No new contract file (D-03).

### 5.1 `validity_frame:` block

```yaml
validity_frame:

  estimand:
    quantity: "difference in 7-day activation rate"
    population: "new non-bot signups, DACH, 2026-06-01 to 2026-06-14"
    contrast: "checklist onboarding vs current"
    time_window: "7 days from signup"
    falsifier: "CI or credible interval includes zero, or lower bound below +1.0pp"

  units:
    observation: session
    assignment: account
    analysis: account              # DSX-VAL-020: must not be finer than assignment

  identification:
    strength: weak                 # strong | moderate | weak
      # strong  = randomised, parameters separated by design
      # weak    = observational and collinear; the data alone cannot separate the parameters
    evidence: "VIF > 12 on paid_search vs paid_social; see DATA-PROFILE.yaml"
    constraint_source: informative_priors_from_lift_tests
      # none | informative_priors | penalisation | design_restriction | hierarchical_pooling
    constraint_justification: "channel ROI priors from Q1 2026 geo lift tests, RESULTS.md#geo-lift"
      # DSX-VAL-040 fires when strength is weak and constraint_source is none
      # DSX-VAL-041 fires when strength is strong and constraint_source carries
      #   parameter-scale information (the constraint may be doing the work)

  dependence:
    structure: clustered           # none | clustered | repeated_measures | temporal | spatial | hierarchical
    cluster_var: account_id
    method_family_required: cluster_robust_or_mixed

  interference:
    risk: shared_budget            # none | shared_budget | marketplace | geo_spillover | social_graph | shared_inventory
    mechanism: "both arms bid into the same Google Ads budget; lift in treatment cannibalises control"
    mitigation: geo_split          # none | geo_split | cluster_randomisation | time_split | budget_isolation | modelled
    residual_note: "cross-border DACH spillover not eliminated; estimate is a lower bound"

  triggering:
    eligible_population: "all new signups"
    triggered_definition: "reached onboarding step 2"
    analysis_population: triggered # eligible | triggered
    expected_trigger_rate: 0.18
    dilution_adjusted: true        # DSX-INT-030 if analysing eligible without adjustment

  stability:
    window: "14 days"
    novelty_primacy_assessed: true
    evidence: "RESULTS.md#week1-vs-week2"

  sampling_frame:
    source: "signups table, DACH region filter"
    claim_population: "all new DACH signups"
    known_exclusions: ["bot-flagged", "internal test accounts"]
    selection_risk: "none identified"

  missingness:
    mechanism: MAR                 # MCAR | MAR | MNAR | not_assessed
    rate: 0.04
    method_implied: complete_case_with_sensitivity

  measurement:
    construct: "activation"
    operationalisation: ">=1 core action within 7 days"
    known_gaps: "excludes mobile web, ~6% of traffic"
```

### 5.2 `inference:` block, both paradigms

```yaml
inference:
  paradigm: frequentist            # frequentist | bayesian
  paradigm_justification: team_convention
    # closed vocabulary, both paradigms, no reason ranked above another:
    #   prior_information_available | sequential_monitoring_required
    #   decision_theoretic_loss_specified | small_sample_informative_prior
    #   regulatory_requirement | team_convention | vendor_constraint
  stopping_rule: fixed_horizon     # fixed_horizon | group_sequential | optional_continuous
  declared_at: pre_data

  # --- frequentist branch ---
  primary_procedure: cluster_robust_welch
  alpha_spending: null             # DSX-PAR-010 if stopping_rule != fixed_horizon and this is null
  fallback_rule: >
    if clusters < 30 -> wild cluster bootstrap, 9999 reps, seed 42

  # --- bayesian branch ---
  # prior: {family: beta, alpha: 1, beta: 1, scale: weakly_informative}
  # prior_justification: "..."                      # DSX-PAR-020
  # prior_predictive: {run: true, evidence: "...", outcome_scale_sane: true}  # DSX-PAR-022
  # prior_sensitivity: {priors_tried: [...], conclusion_stable: true}   # DSX-PAR-021
  # decision_threshold: "P(uplift > 0.01) > 0.95"
  # threshold_calibration: {method: simulation, sims: 10000, fpr: 0.048}  # DSX-PAR-011
  # convergence: {rhat_max: 1.01, ess_min: 400, divergences: 0}         # DSX-PAR-030
```

### 5.3 The symmetric monitoring pair (D-12)

The single most important check in the paradigm family, and the one most specific to online
controlled experiments:

| Code | Fires when | Why |
| --- | --- | --- |
| `DSX-PAR-010` | `stopping_rule` is `optional_continuous` or `group_sequential`, `paradigm: frequentist`, and no alpha-spending or sequential method declared | Uncontrolled Type I inflation under repeated looks |
| `DSX-PAR-011` | `stopping_rule` is `optional_continuous`, `paradigm: bayesian`, and neither `threshold_calibration` nor an informative `prior` with justification is declared | The posterior is valid under any stopping rule. **The error rate of a decision procedure built on it is not.** Under a weak prior with continuous monitoring, the false-positive rate of "stop when P(B>A) > 0.95" inflates substantially. Teams that adopt Bayesian testing specifically to stop worrying about peeking frequently make their error rate worse while believing they solved it. |

Neither paradigm gets the easy road. This pair ships together or neither ships.

### 5.4 The paradigm manifest (D-10)

```
[INFO] DSX-PAR-001  Bayesian paradigm declared.
    applied:     DSX-VAL-*, DSX-INT-*, DSX-PRE-*, DSX-PAR-002, DSX-PAR-011
    not applied: DSX-PAR-020, DSX-PAR-021 (prior justification and sensitivity)
                 DSX-PAR-030 (convergence declarations)
                 DSX-ADM-*   (procedure admissibility adjudication)
    detail:      The frame checks above are paradigm-independent and did run. Threshold
                 calibration under continuous monitoring (DSX-PAR-011) did run. Prior and
                 convergence checks are deferred pending their frequentist counterparts
                 (D-12a); see section 6.5 for the entry conditions. Their absence means a
                 prior doing the work instead of the data will NOT be caught here.
```

Informational, never blocking. Naming the gap removes the incentive to misdeclare.

### 5.5 The decision record

Emitted by every step, deterministic and stochastic alike.

```yaml
- id: DEC-004
  layer: deterministic            # deterministic | stochastic
  choice: "analysis_unit = account, not session"
  inputs: [validity_frame.units.assignment, validity_frame.dependence.structure]
  rule: "DSX-VAL-020: analysis unit must not be finer than assignment unit"
  citation: "Senn (2021), Statistical Issues in Drug Development, ch. 8"
  counterfactual: "if assignment were per-session, session would be admissible"
  alternatives_rejected: []       # stochastic entries only
  confidence: high                # stochastic entries only: high | contested
  escalate: false
```

The `counterfactual` field is what does the teaching. "Here is what I chose" is weak
learning. "Here is what would have to be different for me to choose otherwise" is the rule
rather than the instance, and the rule is what transfers.

---

## 6. Milestones

Ordered by catastrophe-prevention value per unit of work, which is also the order that
maximises what the operator learns while building.

### M1: Contract extension, decision record, real fixtures
Extend `ANALYSIS-SPEC.yaml` with the `validity_frame:` block and the paradigm-aware
`inference:` block. Extend closed vocabularies and `dsx vocab`. Decision-record schema,
emitter, and the non-blocking `dsx explain` renderer. Extend both existing fixtures.

**`DSX-PAR-001`, the paradigm manifest (5.4), ships here, not in M2c.** The moment `paradigm`
exists in the contract, someone can declare `bayesian`, and the behaviour when they do must be
defined from that moment. Leaving the manifest until M2c would leave an undefined window in
which the only sane implementations are "block" (the failure D-10 forbids) or "silently pass"
(worse). This is an ordering constraint, not a preference.

**Pull forward from M5:** encode three or four real known-bad analyses as fixtures now, not
at the end. They cost little here and they make every later check answerable to a real
failure rather than to a model of failure. At least one should be an interference case and
one a Bayesian continuous-monitoring case.

*Done when:* the extended spec round-trips, both fixtures behave per D-08, the real-case
fixtures are committed with their documented post-mortems, and `dsx explain` renders a
readable decision trail.

### M2a: Validity frame checks (`DSX-VAL-*`)
Estimand completeness and falsifiability. Unit triad reconciliation. Dependence declared with
a matching method family. **Identification strength versus constraint source (`DSX-VAL-040`,
`-041`).** Sampling frame versus claim population. Missingness mechanism versus implied
method. Construct-to-metric mapping.

The identification pair is paradigm-independent and therefore belongs here rather than in the
prior family, per D-11. A weakly identified design with no constraint breaks a frequentist
regression and an unconstrained Bayesian model in the same way; a strongly identified design
whose conclusion rests on a parameter-scale constraint is suspect under either paradigm. This
is the check that catches "flat priors on an MMM" and "ridge penalty tuned on the inference
sample" with one rule.

### M2b: Interference, triggering, stability (`DSX-INT-*`)
SUTVA risk declared with a mitigation or an explicit residual note. Shared-budget and
marketplace patterns. Triggered-versus-eligible analysis population with dilution adjustment.
Novelty and primacy assessment over the declared window.

*This milestone is the largest single risk reduction for a 60%-A/B-test workload and is
uncovered by every tool in this space.*

### M2c: Monitoring discipline, symmetric (`DSX-PAR-010`, `DSX-PAR-011`, `DSX-PAR-002`)

**Three checks, not eight.** This is deliberately not "the Bayesian milestone."

`DSX-PAR-010` (frequentist continuous monitoring with no alpha-spending or sequential method)
is unavoidably v1: repeated looks are the most common failure in online controlled
experiments, and the workload is 60% experiments. D-12 then *forces* `DSX-PAR-011`, because
shipping the frequentist half alone would penalise one paradigm for a discipline the other
escapes, which is exactly the steering D-12 exists to prevent. `DSX-PAR-002`
(`paradigm_justification` against the closed vocabulary) is symmetric by construction and
costs a vocabulary lookup.

So the scope question here is not "does Bayesian earn a slot in v1." It is "does monitoring
discipline earn a slot," and that question answers itself. The paradigm symmetry follows from
D-12 rather than from an estimate of how much Bayesian work is coming.

*Done when:* `DSX-PAR-010` and `DSX-PAR-011` both exist, both fire on their respective bad
fixtures, both carry citations per D-05, and neither can be satisfied by switching the
`paradigm` value.

*Explicitly not in this milestone:* prior justification, prior sensitivity, convergence
declarations. See 6.5.

### M3: Pre-registered inference plan (`DSX-PRE-*`)
The fallback-rule mini-DSL, `declared_at` provenance, and the reconciliation gate verifying
the executed procedure matches the branch the declared rule selects against observed facts.

*Done when:* a run that switches procedure after seeing the data is blocked, with the
declared branch and the executed branch both named in the finding.

### M4: Frequentist admissibility adjudicator (`DSX-ADM-*`)
The estimator-family ontology as data in `references/families.yaml`: roughly 25 to 35
families keyed on `estimand x family x inference method x dependence handling`, named tests
as aliases resolving into families. Admissibility function, ranking policy, explicit
`no_admissible_procedure -> escalate` branch. Extends the existing `dsx recommend-test`.

*Done when:* it returns a ranked admissible set with assumptions bought and charged, and
refuses rather than guessing when the frame is underdetermined.

### M5: Calibration
Extend the M1 corpus to full size: retracted papers with published post-mortems, documented
p-hacking cases, and the operator's own past work where the answer is now known. Harness
reporting catch rate and false-positive rate. Add `dsx stats --paradigm`, reporting the
frequentist/Bayesian split across the operator's own frame history.

*Done when:* there is a number. Without it, "reduced risk" is a feeling. If the paradigm
split comes back 100% frequentist after twenty projects, that is either an accurate
reflection of the work or evidence the tool is steering; the number is the only way to tell.

## 6.5 Gated backlog (D-13)

Every item names the evidence that promotes it. Nothing here ships on the strength of an
estimate about future workload, including the operator's own.

| Item | Symmetric counterpart (D-12a) | Entry condition |
| --- | --- | --- |
| Prior justification and prior sensitivity (`DSX-PAR-020`, `-021`) | Frequentist specification sensitivity: does the conclusion survive alternative model specifications? **Not written.** | Both halves are written, **and** the M5 corpus contains at least three cases where absence of either permitted a false pass |
| **Prior predictive check (`DSX-PAR-022`)** | **Now writable:** frequentist simulated-data check on the prior-free specification, does the model generate sane outcome-scale values before fitting. | **Promoted to M2c-adjacent once the mirror is drafted.** Reversal logged, see note below. |
| Convergence declarations (`DSX-PAR-030`) | Frequentist estimation convergence: mixed-model non-convergence, separation in logistic models. **Not written.** | Same, at least two cases |
| Bayesian procedure admissibility (`DSX-ADM-*`, second axis) | The frequentist ontology (M4) | M4 ships, **and** `dsx stats --paradigm` shows Bayesian frames above 15% of the operator's history |
| `dsx quiz` fading mode | n/a, not a check | M5 ships. Weekly, on a sample of past decisions, never inline. |
| **v2.1 Analytic Surface** (Phases 13–16 as a milestone) | n/a, not a paradigm-specific check | **Phase 12 (M5) closed.** Does not reopen Phases 7–12. Comparison recorded in `.planning/research/SURFACE.md` (2026-08-26); README claims from those repos are not D-05 sources. |
| Task playbooks: `dsx-cohort`, `dsx-funnel`, `dsx-root-cause`, `dsx-segment`; EDA hypothesis register; What / So What / Now What narrative; engagement-mode routing onto ceremony tiers; executor preference for `scripts/*.py` | n/a, skill-only — **no new `DSX-*` codes** | Phase 12 closed. Skill-only files may be *drafted* after Phase 6 in parallel; they do not gate v2.0.0 and they do not add finding codes. |
| Compounding (`docs/dsx/learnings/`), portable `DATA-DICTIONARY.md`, optional AI-assistance disclosure when `dsx.domain` is `research`, slash-command aliases, file-drop hook → `dsx profile` (or a documented skip if GSD Core exposes no overlay hooks) | n/a, skill-only — **no new blocking codes** | Phase 12 closed. Same draft-after-Phase-6 rule as the row above. |
| CUPED as a `VARIANCE_ADJUSTMENTS` member plus a check that CUPED covariates are declared pre-experiment (post-treatment covariate blocks) | n/a — variance reduction is paradigm-independent (D-11) | Phase 12 closed, **and** Deng, Xu, Kohavi and Walker (2013), *Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data*, WSDM '13, is cited in the check docstring naming the exact formulation, with a test against a published worked value. The Unified Framework playbook snippet is not an admissible citation. |
| Cohort-grain and funnel-step fields on `ANALYSIS-SPEC.yaml`, with survivorship-bias and changing-denominator findings | n/a | Phase 12 closed, **and** each new code carries its own D-05 citation at implement time. A code whose citation is not in hand stays in this table rather than shipping on a plausible-sounding rule. |
| `dsx-reproduce` skill writing `REPRO-REPORT.md`; gate checks the report exists and named numbers overlap; Phase 12 corpus tags gain `protocol_adherence` | n/a | Phase 12 closed. The skill may execute the entrypoint; the **gate path must not** (D-01/D-02). Does not replace catch rate / false-positive rate. |

Note what D-12a does here: prior sensitivity is deferred **not** because Bayesian work is
speculative, but because its frequentist mirror does not exist yet, so shipping it alone would
violate D-12. That is a structural reason, not a forecast. It also means the cheapest route to
promoting these items is writing the missing counterparts, which is honest work either way.

The v2.1 rows are operator-surface work, not a silent rewrite of M2–M5. Brief §3 still
ranks risk reduction first. Opening v2.1 before Phase 12 has a measured catch rate would
trade the interference and paradigm-symmetry checks — which none of the comparison packs
gate — for playbooks those packs already ship as markdown. Skill-only drafts after Phase 6
are allowed; finding codes and vocabulary members are not.

**Explicitly not entering this backlog** (anti-features from the 2026-08-26 comparison;
see SURFACE.md §4): Docker as a required runtime; MLflow or Great Expectations on the
gate path; Jupyter notebooks as the shipped artifact; auto-running Shapiro–Wilk and
silently switching the test; SEM / HLM / IRT or any second catalogue of named tests;
bundled education datasets; a `/batch-analysis` path that skips the plan gate.

### Reversal record REV-001 (D-14)

**Reversed:** the blanket deferral of the prior family under D-12a.
**New evidence:** the identification-strength framing supplies a writable frequentist mirror
for two of the four deferred items. Prior predictive checking mirrors simulated-data checking;
prior strength versus identification mirrors penalisation strength versus identification. The
original deferral assumed no mirror existed. It did, and I had not looked for it.
**What would have made the original correct:** if prior choice had no frequentist analogue,
which is false for regularisation and true only for genuine subjective-belief priors.
**What did not change:** `DSX-PAR-021` (sensitivity) and `DSX-PAR-030` (convergence) stay
deferred. Their mirrors remain unwritten.

### Fixture note for M1

The growth-marketing content ecosystem widely asserts that a weakly informative prior
"controls false positives while peeking." **This is false**, and it is the single most
load-bearing misconception in this domain. The posterior is valid under any stopping rule; the
error rate of a decision procedure built on it is not. A weak prior delays threshold crossing
slightly and does not control the rate. Encode a spec asserting this as a **bad fixture** for
`DSX-PAR-011`, with a simulation reproducing the inflation. Vendor blogs, Medium posts and
tool marketing are not admissible citations under D-05 in either direction: they cannot
justify a check and they cannot excuse skipping one.

**Set up the simulation deliberately, because the two natural setups give different numbers.**
Against a *point null* (B and A identical, unbounded horizon), the error rate of "stop when
P(B>A) > 0.95" grows without a useful ceiling: the law of the iterated logarithm guarantees
eventual crossing. Averaged over the *prior*, a martingale bound (Ville's inequality) caps the
probability of ever crossing a posterior-odds threshold k at roughly 1/k, so the inflation is
bounded and much smaller. Both are correct statements about different quantities. Decide which
one `DSX-PAR-011` is asserting before writing the fixture, state it in the docstring, and
choose the reference value to match. A fixture built against one formulation and checked
against the other will look like an implementation bug for a day.

## 6.6 Open items for discuss

These are unresolved, and the planner should not silently pick a side.

1. **`DSX-PAR-010` overlaps existing `DSX-EXP-*` peeking checks.** The existing check catches
   peeking under a declared fixed horizon. The new one catches a declared continuous-monitoring
   design with no sequential method. Decide whether this is one check with a widened trigger or
   two codes. D-06 makes the answer irreversible.
2. **`references/families.yaml` is named in D-03a but not built until M4.** Do not scaffold it
   in M1 to satisfy the boundary rule. An empty ontology file sitting unused for three
   milestones accumulates speculative structure that then has to be unpicked.
3. **`SELF-001` in `.planning/REVERSALS.md` (D-14) has no enforcement mechanism yet.** It is a
   convention until something checks it. Decide whether that is acceptable for v1 or whether it
   becomes a `dsx` subcommand.

---

## 7. Reference sources

Anchor D-05 citations here rather than sprawling.

Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* (triggering, dilution,
interference, novelty and primacy, SRM). Imbens and Rubin, *Causal Inference for Statistics,
Social, and Biomedical Sciences* (SUTVA, estimands). Hernan and Robins, *Causal Inference:
What If* (estimands, identification). Gelman and Hill, *Data Analysis Using Regression and
Multilevel/Hierarchical Models* (dependence, units). Lohr, *Sampling: Design and Analysis*
(frames, selection). Little and Rubin, *Statistical Analysis with Missing Data* (mechanisms).
Senn, *Statistical Issues in Drug Development* (design, units, multiplicity). Gelman et al.,
*Bayesian Data Analysis*, 3rd ed. (priors, sensitivity). Vehtari et al. (2021), "Rank-normalized
R-hat" (convergence diagnostics and thresholds). Gelman et al. (2020), "Bayesian Workflow"
(prior predictive checking, the workflow the guardrail framing informally describes). Gelman,
Simpson and Betancourt (2017), "The Prior Can Often Only Be Understood in the Context of the
Likelihood" (why prior strength is meaningless without identification, the source for
`DSX-VAL-040/041`). Deng, Lu and Chen (2016), "Continuous Monitoring of A/B Tests without
Pain" (error rates under optional stopping, the source for `DSX-PAR-011`). Deng, Xu,
Kohavi and Walker (2013), "Improving the Sensitivity of Online Controlled Experiments by
Utilizing Pre-Experiment Data," *WSDM '13* (CUPED; D-05 candidate for the queued v2.1
variance-adjustment member — confirm the exact formulation and a published worked value
from the paper before the check ships; comparison-repo playbooks are not a source).

---

## 8. Known limits, to be stated in the README

The gate checks declarations against declarations. **A frame that lies passes.** The insurance
against a bad question is still a human who knows the domain reading the frame before the data
is touched. What this changes is that the review becomes cheap, structured and repeatable, so
it actually happens.

---

## 9. Runtime and constraints

Python 3.9+, stdlib only on the gate path. GSD Core >= 1.6. Extends the existing DSX package,
no fork, no second installer, no patched upstream workflows. Exit codes remain the contract:
`0` pass, `1` block, `2` could not run.
