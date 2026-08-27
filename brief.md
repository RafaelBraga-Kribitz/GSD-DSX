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
| Feature-provenance per-feature list (origin, method, fitted-on, motivating result) | Not a paradigm-paired item. | The M5 corpus contains at least one case whose target defect is attributable **only** through feature origin — no name pattern matches, no fit call is visible, and no declaration contradicts. Until then the leakage principle is covered elsewhere; this buys attribution, not a catch (2026-08-20 paper-evaluation integration) |
| Magnitude-without-computed-effect residual (absolute magnitudes; relative % that declares its base) | Not a paradigm-paired item. | A corpus case passes all claims checks while asserting a magnitude no reported test computed. The paper-shaped instances all fire `DSX-CLM-070` and the per-test effect-size finding already (2026-08-20) |
| Subgroup-harm declaration for prescriptive work | Not a paradigm-paired item. | A primary source with operationalisable criteria (D-05) **and** a corpus case where subgroup harm was the documented failure. Until promoted, the question lives in the architect and storyteller prompts as an agent guardrail (2026-08-20) |

Note what D-12a does here: prior sensitivity is deferred **not** because Bayesian work is
speculative, but because its frequentist mirror does not exist yet, so shipping it alone would
violate D-12. That is a structural reason, not a forecast. It also means the cheapest route to
promoting these items is writing the missing counterparts, which is honest work either way.

### Phase 12 re-evaluation of the gated backlog (REQ-P12-05, 2026-08-27)

Phase 12 measured the numbers this section exists to wait for and re-evaluated
every row against its own entry condition. **Disposition: carry eight, remove one.**
Each carried item names the measured count, rate or split it rests on; nothing is
promoted by manufacturing a case to hit a threshold (D-02/D-15).

- **Prior justification / sensitivity** (item 1) — **carried.** Its frequentist
  mirror (specification sensitivity) is still unwritten under D-12a, so no corpus
  count can promote it; the cheapest route remains writing the mirror.
- **Prior predictive check `DSX-PAR-022`** (item 2) — **already promoted** (REV-001);
  the row records the reversal.
- **Convergence declarations `DSX-PAR-030`** (item 3) — **carried,** same structural
  reason as item 1: the frequentist convergence mirror is unwritten (D-12a).
- **Bayesian procedure admissibility, second axis** (item 4) — **carried; explicitly
  NOT auto-promoted.** Its condition needs M4 shipped **and** `dsx stats --paradigm`
  above 15% Bayesian. The measured operator split (plan 12-02) is **empty — zero
  distinct frames** across the operator's real `.planning` history (the polluted
  `examples/**` and `templates/**` floors excluded by construction), so the honest
  share is below 15%. That non-promotion is exactly what the number is for
  (§6, "Done when: there is a number").
- **`dsx quiz` fading mode** (item 5) — **carried, prerequisite-pending:** it ships
  on M5, which has not shipped.
- **Ratio-metric dilution** (item 6) — **removed as structurally unevaluable;** see
  "Removed / permanently out of scope (D-14)" below and REV-002.
- **Feature-provenance per-feature list** (item 7) — **carried.** Promotion needs a
  corpus case whose target defect is attributable *only* through feature origin. The
  three measured ABSENT-partition misses (plan 12-05: undisclosed forking, data
  fabrication, undisclosed selective exclusion; miss-rate 3/3) are not that case —
  data fabrication is a provenance-of-data miss, not a per-feature-origin attribution —
  so the naming case has not appeared. Not manufactured.
- **Magnitude-without-computed-effect residual** (item 8) — **carried; likely none.**
  No corpus case passes all claims checks while asserting an uncomputed magnitude; the
  paper-shaped instances already fire `DSX-CLM-070` and the per-test effect-size finding.
- **Subgroup-harm declaration for prescriptive work** (item 9) — **carried.** Promotion
  needs an admissible D-05 source with operationalisable criteria **and** a corpus case
  where subgroup harm was the documented failure; neither is in the measured corpus.

The calibration backdrop these dispositions read: the measured headline is
**(miss-rate 1.0, FPR 0.0)** — zero false positives over the twelve-spec good-control
corpus (plan 12-05, 0/12), a benign per-family friction column over the same corpus
(plan 12-06, reported raw and net), and a 3/3 miss on the semantic-defect class a
declaration-only gate structurally cannot catch. Those misses are what items 1/3/7/9
would eventually address; none is promotable on today's measured evidence.

### Removed / permanently out of scope (D-14)

Phase 12's systematic re-evaluation (REQ-P12-05) recognised one item's entry condition
as structurally unreachable rather than merely unmet, and removed it. It is relocated
here verbatim — not deleted and not softened back to the access premise D-12 proved
false — with the reversal recorded as REV-002.

| Item | Symmetric counterpart (D-12a) | Entry condition |
| --- | --- | --- |
| **Ratio-metric dilution for trigger analysis** (Deng & Hu 2015 Formula (3), §3.3) | **Not a paradigm-paired item.** The additive case ships this milestone as `DSX-INT-030`; this is its unshipped extension, not a frequentist/Bayesian mirror under D-12a. | **A source of per-unit trigger and outcome data reaching the gate.** Formula (3) sums over individual users (`∆Overall(X) = (1/N) Σ_Tr TR_i × (TrX_iT − TrX_iC)`) and has no closed-form scalar multiplier, so it cannot be evaluated from a declaration alone the way the additive Formula (1) can. The paper itself is freely available and the equation is readable today — access was never the blocker. This item may be **permanently out of scope** for a declaration-only gate, not merely deferred: the determinism doctrine that keeps computation off the gate path (D-01/D-02) is what forbids evaluating it here, and that constraint does not lift with more time. |

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
eventual crossing. Averaged over the *prior*, Deng, Lu & Chen (2016) Theorem 1 caps the
false-discovery risk of stopping at a posterior-odds threshold K at 1/(K+1) — at K = 19, exactly
0.05 — so the inflation is bounded and much smaller. Do not substitute Ville's inequality here:
it gives the different bound 1/k (1/19 ≈ 0.0526 at the same threshold) and is not the argument
Theorem 1 makes. Both are correct statements about different quantities. Decide which
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
interference, novelty and primacy, SRM; the shared-budget interference chapter locator is
Chapter 22, *Leakage and Interference between Variants*, pages 226 to 234, verified — closing
the unverified-locator flag recorded in `06-08-SUMMARY.md` and `06-VERIFICATION.md`). Imbens
and Rubin, *Causal Inference for Statistics,
Social, and Biomedical Sciences* (SUTVA, estimands). Hernan and Robins, *Causal Inference:
What If* (estimands, identification). International Council for Harmonisation (2019), the
E9(R1) addendum on estimands and sensitivity analysis, document reference
EMA/CHMP/ICH/436221/2017 at Step 5, sections A.3.2 and A.3.3 (estimand completeness, the source
for `DSX-VAL-010`). Hernan and Robins (2016), *American Journal of Epidemiology* volume 183
issue 8, pages 758 to 764, Table 1 (a second, distinct publication by the same authors as the
*What If* text above, anchoring `DSX-VAL-010` alongside the E9(R1) addendum). Popper (1959,
2002 reissue), *The Logic of Scientific Discovery*, Part I Chapter 1 section 6 on falsifiability
as a criterion of demarcation, pages 17 to 18 (the source for `DSX-VAL-011`). Gelman and Hill
(2007), *Data Analysis Using Regression and Multilevel/Hierarchical Models*, Cambridge
University Press (dependence, units; the exact chapter locator within it is unverified).
Cameron and Miller (2015), "A Practitioner's Guide to Cluster-Robust Inference", *Journal of
Human Resources* volume 50 issue 2, pages 317 to 372 (the source for `DSX-VAL-030`; Section VI,
*Few Clusters*, is now the verified section locator for the few-clusters guidance, with Section
II for the estimator and Section IV for the clustering dimension — partially closing the
unverified-locator flag recorded in `07-01-SUMMARY.md`. Caveat: the accepted manuscript jumps
from Section VIII to Section XI, so the typeset journal numbering may differ; the manuscript
numbering is the verified object). Lohr (2021), *Sampling: Design and Analysis*, third edition,
Chapter 1 sections 1.2, 1.3 and 1.3.4, and Chapter 16 section 16.1 (frames, selection, the
source for `DSX-VAL-050`). Little and Rubin (2019), *Statistical Analysis with Missing Data*,
third edition, Chapter 3 section 3.2 (mechanisms, the source for `DSX-VAL-060`). White and
Carlin (2010), *Statistics in Medicine* volume 29 issue 28, pages 2920 to 2931, digital object
identifier 10.1002/sim.3944 (the companion source establishing that complete-case analysis can
be unbiased under missing-at-random, also anchoring `DSX-VAL-060`). Senn, *Statistical Issues
in Drug Development* (design, units, multiplicity). Kish (1965), *Survey Sampling*, section 8.2
and page 258 for the design-effect definition and pages 161 to 162 for the intraclass
correlation (the source for `DSX-VAL-020`; section 8.2 was confirmed for the design-effect
definition, and a section number for the design-effect formula itself is unverified). Higgins,
Eldridge and Li (2024), the *Cochrane Handbook
for Systematic Reviews of Interventions*, version 6.5, sections 23.1.4 and 23.1.4.1 (carrying
the published design-effect worked value, also anchoring `DSX-VAL-020`). Gelman et al.,
*Bayesian Data Analysis*, 3rd ed. (priors, sensitivity). Vehtari et al. (2021), "Rank-normalized
R-hat" (convergence diagnostics and thresholds). Gelman et al. (2020), "Bayesian Workflow"
(prior predictive checking, the workflow the guardrail framing informally describes). Gelman,
Simpson and Betancourt (2017), "The Prior Can Often Only Be Understood in the Context of the
Likelihood", *Entropy* 19(10), 555, section 3.3 ("For complex models, certain aspects of the
prior will always be relevant") and section 1.2 ("Existing methods for setting priors already
depend on the likelihood") (why prior strength is meaningless without identification, the
source for `DSX-VAL-040/041`; cited by section number and by title together because whether the
typeset journal version uses the same section numbers as the arXiv preprint version is
unverified). Deng, Lu and Chen (2016), "Continuous Monitoring of A/B Tests without
Pain" (error rates under optional stopping, the source for `DSX-PAR-011`). Cronbach and Meehl
(1955), "Construct Validity in Psychological Tests", *Psychological Bulletin* volume 52 issue
4, pages 281 to 302, the nomological net discussion at page 290 (the source for
`DSX-VAL-070`). Gelman, A. and Loken, E. (2014), "The Statistical Crisis in Science",
*American Scientist*, volume 102, issue 6, pages 460-465 (the source for the `DSX-PRE-*`
family — anchors the distinction between a test prechosen from a set of possible tests and a
test computed from the data in an environment where a different test would have been
performed given different data, which is the exact claim `DSX-PRE-010`/`-020`/`-030` enforce;
page 460, unnumbered section "How to Test a Hypothesis", for rule resolution and the content
lock, and page 463, the unnumbered section opening "Menstrual Cycles and Voting", for procedure
reconciliation. The article carries no numbered sections, tables or theorems, so page plus
unnumbered heading is the most precise locator available, and naming a section number would be
the fabricated locator this citation rule exists to prevent. The Greek symbol the paper uses
for the selection function is rendered unreliably by optical character recognition in both
freely available scans — the prose was cross-verified word for word between two independent
copies, but the symbol was not — so it is taken from the authors' unpublished 2013 Columbia
working paper, which carries no digital object identifier, venue or pagination and is a
notation source only, never the published record). Two secondary sources sit beside it, each
scoped so neither is promoted into the primary anchor: Simmons, J. P., Nelson, L. D. and
Simonsohn, U. (2011), "False-Positive Psychology", *Psychological Science*, volume 22, issue
11, pages 1359-1366, digital object identifier 10.1177/0956797611417632, page 1365 (supports
only the claim that a substituted procedure is itself a new researcher degree of freedom, the
`DSX-PRE-030` remedy's no-merit-consultation rule — never the primary anchor). Nosek, B. A.,
Ebersole, C. R., DeHaven, A. C. and Mellor, D. T. (2018), "The preregistration revolution",
*PNAS*, volume 115, issue 11, pages 2600-2606, digital object identifier
10.1073/pnas.1708274114, section "Preregistration in Practice" (supports only the rule that a
declared deviation stays legal, the `post_data` branch of the content lock; section headings
were verified and per-sentence page numbers were not, so no page may be cited for an individual
sentence from it).

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
