# Requirements

**Current milestone:** v2.0.0 DSX Validity Frame (Phases 6–12) — see below.
**Shipped:** v1.1.0–v1.5.0 (Phases 1–5).

---

## Phase 1 (v1.1.0) — complete

- [x] REQ-P1-01 Spec `data[]` supports `profile_path` and `assertions`
- [x] REQ-P1-02 `templates/DATA-PROFILE.yaml` documents the profile contract
- [x] REQ-P1-03 `dsx profile <csv>` writes a profile with `computed_by: dsx-profile` and `source_hash`
- [x] REQ-P1-04 `DSX-DQ-*` blocks execute/verify/ship when assertions disagree with the profile
- [x] REQ-P1-05 Evidence paths resolve on disk; `#anchor` must exist in markdown
- [x] REQ-P1-06 Claim numbers must overlap `results.tests` when tests are present
- [x] REQ-P1-07 Claim type cannot exceed `question_type` strength
- [x] REQ-P1-08 Causal verbs in `decision_rule` blocked when question is descriptive/diagnostic
- [x] REQ-P1-09 Experiments require MPE + `action_if_null`
- [x] REQ-P1-10 Causal/prescriptive questions require non-empty `assumptions` by ship
- [x] REQ-P1-11 Good fixture passes every gate; bad fixture blocks every gate
- [x] REQ-P1-12 Finding catalogue regenerated; tests green
- [x] REQ-P1-13 Capability/plugin version bumped to 1.1.0

## Phase 2 (v1.2.0) — complete

- [x] REQ-P2-01 `visuals[]` supports chart_id, data_input_type, artifact_path, svg_sha256, series_role, run_id
- [x] REQ-P2-02 `DSX-VIZ-013/014` enforce data_input_type × chart matrix
- [x] REQ-P2-03 `DSX-VIZ-063/064` takeaway heuristics
- [x] REQ-P2-04 `DSX-FIG-*` hermetic seals + `dsx seal`; FIGURE-MANIFEST coverage
- [x] REQ-P2-05 `DSX-SMELL-*` for B/G/I/J/K/M
- [x] REQ-P2-06 Verifier Gate A–D protocol; visualize skill + viz-critic updated
- [x] REQ-P2-07 Good/bad fixtures + SVG stubs; version 1.2.0; catalogue current

## Phase 3 (v1.3.0) — complete

- [x] REQ-P3-01 `narrative` / `dashboard` / claim `base_n`/`from_value`/`to_value` in ANALYSIS-SPEC
- [x] REQ-P3-02 `FORBIDDEN-CLAIMS.yaml` template + `references/narrative-discipline.md`
- [x] REQ-P3-03 `DSX-CLM-070` relative % without base; `DSX-CLM-080` limitations for causal|prescriptive|predictive
- [x] REQ-P3-04 `DSX-NAR-*` narrative path, claim⊆file, forbidden wording, dashboard path
- [x] REQ-P3-05 `DSX-SQL-007`–`014` + `DSX-MET-040` warehouse requires sql; timezone → `DSX-MET-041`
- [x] REQ-P3-06 `DSX-CODE-*` fit-before-split entrypoint scan; wired on execute/verify/ship
- [x] REQ-P3-07 Skills/agents/fragments updated (narrate, storyteller, build-model, define-metrics)
- [x] REQ-P3-08 Good/bad fixtures + tests; catalogue regen; version 1.3.0

## Phase 4 (v1.4.0) — complete

- [x] REQ-P4-01 Assumption `checked:true` XOR `waiver` at verify/ship (`DSX-COH-031`)
- [x] REQ-P4-02 Null-as-no-effect requires CI-in-bounds / TOST / `detectable_mde` (`DSX-STA-020`/`021`)
- [x] REQ-P4-03 `comparisons_looked_at` vs multiplicity family (`DSX-EXP-051`/`052`)
- [x] REQ-P4-04 `repro_lock` honest-null (`DSX-REP-050`–`053`)
- [x] REQ-P4-05 Structured `decision.replay` vs `results.tests` (`DSX-DEC-*`)
- [x] REQ-P4-06 Reconciliation class tolerances + `DSX-MET-012`
- [x] REQ-P4-07 Skills/agents/fragments + fixtures/tests; catalogue; version 1.4.0

## Phase 5 (v1.5.0) — complete

- [x] REQ-P5-01 ANALYSIS-SPEC `suppressions[]` with reason + authority; unknown code → exit 2
- [x] REQ-P5-02 `DSX-SPEC-070`–`072` structural findings for bad suppressions
- [x] REQ-P5-03 `chart-review-schema.md` + `templates/CHART-REVIEW.md` (`dsx-chart-review-v1`)
- [x] REQ-P5-04 `dsx-viz-critic` writes CHART-REVIEW; skill `dsx-chart-audit` registered
- [x] REQ-P5-05 Tests for suppressions; catalogue regenerated; version 1.5.0

---

# Milestone v2.0.0 — DSX Validity Frame

**Defined:** 2026-08-07
**Core value:** A statistically invalid analysis must fail at the gate, before the data is touched.
**Binding inputs:** `brief.md` §4 (decisions D-01…D-14), §5 (contract), §6 (milestones), §6.5 (gated backlog), §7 (citations); `.planning/research/` (SUMMARY, STACK, FEATURES, ARCHITECTURE, PITFALLS).

Every check in this milestone is subject to **D-05**: a primary-source citation in the
docstring, and a test against a published reference value. Vendor blogs are inadmissible
in either direction — they cannot justify a check and cannot excuse skipping one.

## Phase 6 (M1) — Contract extension, decision record, paradigm manifest

- [ ] REQ-P6-01 Bundled YAML fallback parser no longer treats the literal `none` as null; `dsx/loader.py` `_NULL` drops `"none"`, and a test asserts the bundled parser and PyYAML agree on `none` for scalars and sequences
- [ ] REQ-P6-02 `ANALYSIS-SPEC.yaml` accepts a `validity_frame:` block with `estimand`, `units`, `identification`, `dependence`, `interference`, `triggering`, `stability`, `sampling_frame`, `missingness` and `measurement` sub-blocks, and the extended spec round-trips
- [ ] REQ-P6-03 `validity_frame` sub-block requiredness is gated by `question_type`: `estimand`, `units` and `measurement` are always required; `interference`, `triggering` and `stability` are required only for causal and experimental question types (M-06)
- [ ] REQ-P6-04 `ANALYSIS-SPEC.yaml` accepts an `inference:` block with `paradigm`, `paradigm_justification`, `declared_at`, `primary_procedure`, `alpha_spending` and `fallback_rule`; the stopping-rule concept is read from the existing `design.peeking_policy`, and no `inference.stopping_rule` field is introduced (M-02)
- [ ] REQ-P6-05 `PEEKING_POLICIES` gains a value denoting continuous monitoring with no sequential correction, distinct from `always_valid` (M-03)
- [ ] REQ-P6-06 Every new closed vocabulary is registered in `dsx/spec.py` and dumped by `dsx vocab`; `dependence.method_family_required` reuses `VARIANCE_ADJUSTMENTS` rather than defining a parallel set (M-09)
- [ ] REQ-P6-07 A decision-record schema and emitter exist as a top-level module, carrying `id`, `layer`, `choice`, `inputs`, `rule`, `citation`, `counterfactual`, `alternatives_rejected`, `confidence` and `escalate`; records serialise append-only and survive a crashed run
- [ ] REQ-P6-08 `dsx explain` renders a readable decision trail from emitted records and always exits `0`, never participating in the block contract (D-04)
- [ ] REQ-P6-09 `DSX-PAR-001` emits an informational paradigm manifest naming which check families applied and which did not, at INFO severity, and cannot block at any gate threshold (D-10)
- [ ] REQ-P6-10 A `dsx/frame/` package exists and an automated AST-based test asserts it never imports from `dsx/checks/`, failing the suite on violation (D-03a, M-04)
- [ ] REQ-P6-11 `scripts/gen-finding-catalogue.py` fails the build when a check lacks a citation marker in its docstring, making D-05 mechanical rather than review-only (M-08)
- [ ] REQ-P6-12 `examples/good-ANALYSIS-SPEC.yaml` still passes every gate at every threshold and `examples/bad-ANALYSIS-SPEC.yaml` is still blocked by every gate, both extended rather than replaced (D-08)
- [ ] REQ-P6-13 At least three real known-bad analyses are committed as fixtures with documented post-mortems, including at least one interference case and one Bayesian continuous-monitoring case
- [ ] REQ-P6-14 `.planning/REVERSALS.md` exists with the D-14 reversal-record template and the `SELF-001` convention documented (M-05)
- [ ] REQ-P6-15 The README documents `suppressions[]` with its authority requirement as the migration path for pre-v2.0.0 specs, and states the known limit that a frame which lies passes (M-07, brief §8)
- [ ] REQ-P6-16 Package version is 2.0.0 and the finding catalogue is regenerated

## Phase 7 (M2a) — Validity frame checks (`DSX-VAL-*`)

- [ ] REQ-P7-01 An estimand missing any of `quantity`, `population`, `contrast`, `time_window` or `falsifier` is blocked, and a falsifier that cannot discriminate any outcome is blocked
- [ ] REQ-P7-02 An analysis unit finer than the assignment unit is blocked, with the design-effect consequence quantified in the finding via `DEFF = 1 + (m-1)·ICC` and a test asserting the published worked value
- [ ] REQ-P7-03 `DSX-VAL-020` and the existing `DSX-EXP-021` do not both fire on the same defect; EXP-021 is unchanged and VAL-020 covers only the `observation` unit that EXP-021 structurally cannot see
- [ ] REQ-P7-04 A declared dependence structure without a matching method family is blocked, using the `VARIANCE_ADJUSTMENTS` vocabulary
- [ ] REQ-P7-05 `DSX-VAL-040` blocks weak identification declared with `constraint_source: none`, and `DSX-VAL-041` flags strong identification whose constraint carries parameter-scale information, both citing Gelman, Simpson & Betancourt (2017)
- [ ] REQ-P7-06 A sampling frame that cannot represent the claim population is blocked, with known exclusions and selection risk declared
- [ ] REQ-P7-07 A missingness mechanism inconsistent with the implied analysis method is blocked, against the Rubin MCAR/MAR/MNAR validity table
- [ ] REQ-P7-08 A measurement construct with no operationalisation, or whose known gaps contradict the claim population, is blocked
- [ ] REQ-P7-09 No `DSX-VAL-*` check reads `inference.paradigm` (D-11), asserted by test

## Phase 8 (M2b) — Interference, triggering, stability (`DSX-INT-*`)

- [ ] REQ-P8-01 A declared interference risk other than `none` without either a mitigation or an explicit residual note is blocked, citing the SUTVA statement in Imbens & Rubin (2015)
- [ ] REQ-P8-02 Shared-budget and marketplace interference patterns are recognised as distinct risks with distinct admissible mitigations
- [ ] REQ-P8-03 `DSX-INT-030` blocks analysis of the eligible population when treatment reaches only the triggered subset and no dilution adjustment is declared, for additive metrics, asserting `delta_diluted = delta_triggered × trigger_rate`
- [ ] REQ-P8-04 Ratio-metric dilution is explicitly out of scope for v2.0.0 and recorded in the gated backlog with the entry condition that the Deng & Hu (2015) ratio-metric equation is obtained from primary source (D-13)
- [ ] REQ-P8-05 An unassessed novelty/primacy effect over the declared stability window is flagged, with the assessment method cited
- [ ] REQ-P8-06 No `DSX-INT-*` check reads `inference.paradigm` (D-11), asserted by test

## Phase 9 (M2c) — Monitoring discipline, symmetric (`DSX-PAR-*`)

- [ ] REQ-P9-01 `DSX-PAR-010` blocks a frequentist design declaring continuous or group-sequential monitoring with no alpha-spending or sequential method, reusing the existing `inflation_from_peeking()` table rather than introducing a second one
- [ ] REQ-P9-02 `DSX-PAR-011` blocks a Bayesian design declaring continuous monitoring with neither threshold calibration nor a justified informative prior, asserting the prior-averaged Ville bound `1/(K+1)` — at the `P(B>A) > 0.95` threshold, `K=19` and the bound is `0.05` — citing Deng, Lu & Chen (2016) Theorem 1
- [ ] REQ-P9-03 The `DSX-PAR-011` docstring states explicitly that it asserts the prior-averaged formulation and not the point-null/law-of-iterated-logarithm formulation, and the fixture traces to the specific theorem
- [ ] REQ-P9-04 `DSX-PAR-002` validates `paradigm_justification` against the closed vocabulary, symmetric across both paradigms with no reason ranked above another
- [ ] REQ-P9-05 Neither `DSX-PAR-010` nor `DSX-PAR-011` can be satisfied by switching the declared `paradigm` value, asserted by test in both directions
- [ ] REQ-P9-06 A documented audit records that neither half of the pair has a cheaper dishonest escape than the other, and the disjunctive `prior_justification` path is no weaker than the sequential-method requirement (D-12)
- [ ] REQ-P9-07 The `DSX-PAR-011` simulation lives under `tests/`, never on the gate path, and is seeded and reproducible (D-02)

## Phase 10 (M3) — Pre-registered inference plan (`DSX-PRE-*`)

- [ ] REQ-P10-01 A fallback rule expressed in the mini-DSL parses to a decidable branch against observed facts, and an unparseable rule exits `2` rather than passing
- [ ] REQ-P10-02 `declared_at` provenance is recorded and its limits are documented — an unverifiable self-declaration is named as such rather than presented as a guarantee
- [ ] REQ-P10-03 A run whose executed procedure differs from the branch the declared rule selects is blocked, with the declared branch and the executed branch both named in the finding
- [ ] REQ-P10-04 A procedure switched after seeing the data is blocked even when the substituted procedure is individually defensible

## Phase 11 (M4) — Frequentist admissibility adjudicator (`DSX-ADM-*`)

- [ ] REQ-P11-01 `references/families.yaml` holds 25–35 estimator families as data, keyed on estimand × family × inference method × dependence handling, parsed by the existing loader
- [ ] REQ-P11-02 Named tests resolve as aliases into families rather than being enumerated as a test catalogue
- [ ] REQ-P11-03 The admissibility function returns a ranked admissible set, naming for each entry the assumptions bought and charged
- [ ] REQ-P11-04 An underdetermined frame returns `no_admissible_procedure` and escalates rather than guessing
- [ ] REQ-P11-05 The adjudicator extends the existing `dsx recommend-test` rather than replacing it
- [ ] REQ-P11-06 D-05 applies to `families.yaml` entries as it does to checks: each family carries a primary-source citation, enforced by the M1 catalogue check

## Phase 12 (M5) — Calibration

- [ ] REQ-P12-01 The known-bad corpus is extended to full size with retracted papers carrying published post-mortems, documented p-hacking cases, and prior work whose answer is now known
- [ ] REQ-P12-02 Corpus cases carry structured catch-attribution tags so backlog entry conditions are machine-countable rather than narrative judgements (D-13)
- [ ] REQ-P12-03 A harness reports catch rate and false-positive rate across the corpus, producing a number
- [ ] REQ-P12-04 `dsx stats --paradigm` reports the frequentist/Bayesian split across the operator's own frame history
- [ ] REQ-P12-05 Each gated-backlog item in brief §6.5 is re-evaluated against its stated entry condition using the measured corpus, and items whose condition cannot be evaluated are removed rather than carried

## Out of Scope — v2.0.0

| Item | Reason |
|---|---|
| Computing test statistics or posteriors on the gate path | Breaks D-01/D-02; gates adjudicate declarations |
| Bayesian procedure admissibility (`DSX-ADM-*` second axis) | Gated backlog; entry condition is M4 shipped **and** `dsx stats --paradigm` showing Bayesian frames above 15% |
| Prior justification and prior sensitivity (`DSX-PAR-020`/`-021`) | Deferred under D-12a — the frequentist specification-sensitivity mirror is not written |
| Convergence declarations (`DSX-PAR-030`) | Deferred under D-12a — the frequentist estimation-convergence mirror is not written |
| Prior predictive check (`DSX-PAR-022`) | Promoted only once its frequentist simulated-data mirror is drafted (REV-001) |
| Ratio-metric dilution | Formula could not be obtained from primary source; shipping a plausible-looking equation would violate D-05 |
| Causal identification strategy checking | `DSX-CAU-*` owns this |
| Survival, time-series and spatial estimation methods | Temporal and spatial dependence are declared types; the methods are out |
| Reading a data warehouse from a gate | Breaks the determinism doctrine |
| A catalogue of every named statistical test | Families, not tests |
| `dsx quiz` fading mode | Entry condition: M5 ships |

## Open items — resolve at phase discuss, do not decide silently

| Item | Phase | Why unresolved |
|---|---|---|
| `method_family_required` cannot express a disjunction under M-09's single-member reuse of `VARIANCE_ADJUSTMENTS`; the brief's example value is `cluster_robust_or_mixed` | 7 (M2a) | Reuse was chosen over a parallel vocabulary; whether the field becomes set-valued is a modelling call best made against real dependence declarations |
| Final numeric code assignments within `DSX-VAL-*`, `DSX-INT-*`, `DSX-ADM-*` beyond those the brief fixes | 7, 8, 11 | D-06 makes numbering irreversible |
| Whether the existing `inflation_from_peeking()` docstring is upgraded to a full D-05 citation (currently "Armitage's classic result", no year or paper) | 9 (M2c) | Pre-existing docstring held to a lower bar than the new checks it will support |

## Traceability

Every v2.0.0 requirement maps to exactly one phase. 53/53 mapped; no orphans, no duplicates.

| Requirement | Phase | Status |
|-------------|-------|--------|
| REQ-P6-01 | Phase 6 | Complete |
| REQ-P6-02 | Phase 6 | Complete |
| REQ-P6-03 | Phase 6 | Complete |
| REQ-P6-04 | Phase 6 | Complete |
| REQ-P6-05 | Phase 6 | Complete |
| REQ-P6-06 | Phase 6 | Complete |
| REQ-P6-07 | Phase 6 | Complete |
| REQ-P6-08 | Phase 6 | Pending |
| REQ-P6-09 | Phase 6 | Pending |
| REQ-P6-10 | Phase 6 | Pending |
| REQ-P6-11 | Phase 6 | Complete |
| REQ-P6-12 | Phase 6 | Complete |
| REQ-P6-13 | Phase 6 | Pending |
| REQ-P6-14 | Phase 6 | Complete |
| REQ-P6-15 | Phase 6 | Complete |
| REQ-P6-16 | Phase 6 | Pending |
| REQ-P7-01 | Phase 7 | Pending |
| REQ-P7-02 | Phase 7 | Pending |
| REQ-P7-03 | Phase 7 | Pending |
| REQ-P7-04 | Phase 7 | Pending |
| REQ-P7-05 | Phase 7 | Pending |
| REQ-P7-06 | Phase 7 | Pending |
| REQ-P7-07 | Phase 7 | Pending |
| REQ-P7-08 | Phase 7 | Pending |
| REQ-P7-09 | Phase 7 | Pending |
| REQ-P8-01 | Phase 8 | Pending |
| REQ-P8-02 | Phase 8 | Pending |
| REQ-P8-03 | Phase 8 | Pending |
| REQ-P8-04 | Phase 8 | Pending |
| REQ-P8-05 | Phase 8 | Pending |
| REQ-P8-06 | Phase 8 | Pending |
| REQ-P9-01 | Phase 9 | Pending |
| REQ-P9-02 | Phase 9 | Pending |
| REQ-P9-03 | Phase 9 | Pending |
| REQ-P9-04 | Phase 9 | Pending |
| REQ-P9-05 | Phase 9 | Pending |
| REQ-P9-06 | Phase 9 | Pending |
| REQ-P9-07 | Phase 9 | Pending |
| REQ-P10-01 | Phase 10 | Pending |
| REQ-P10-02 | Phase 10 | Pending |
| REQ-P10-03 | Phase 10 | Pending |
| REQ-P10-04 | Phase 10 | Pending |
| REQ-P11-01 | Phase 11 | Pending |
| REQ-P11-02 | Phase 11 | Pending |
| REQ-P11-03 | Phase 11 | Pending |
| REQ-P11-04 | Phase 11 | Pending |
| REQ-P11-05 | Phase 11 | Pending |
| REQ-P11-06 | Phase 11 | Pending |
| REQ-P12-01 | Phase 12 | Pending |
| REQ-P12-02 | Phase 12 | Pending |
| REQ-P12-03 | Phase 12 | Pending |
| REQ-P12-04 | Phase 12 | Pending |
| REQ-P12-05 | Phase 12 | Pending |

### Coverage summary

| Phase | Milestone | Requirements | Count |
|-------|-----------|--------------|-------|
| 6 | M1 — Contract extension, decision record, paradigm manifest | REQ-P6-01 … REQ-P6-16 | 16 |
| 7 | M2a — Validity frame checks (`DSX-VAL-*`) | REQ-P7-01 … REQ-P7-09 | 9 |
| 8 | M2b — Interference, triggering, stability (`DSX-INT-*`) | REQ-P8-01 … REQ-P8-06 | 6 |
| 9 | M2c — Monitoring discipline, symmetric (`DSX-PAR-*`) | REQ-P9-01 … REQ-P9-07 | 7 |
| 10 | M3 — Pre-registered inference plan (`DSX-PRE-*`) | REQ-P10-01 … REQ-P10-04 | 4 |
| 11 | M4 — Frequentist admissibility adjudicator (`DSX-ADM-*`) | REQ-P11-01 … REQ-P11-06 | 6 |
| 12 | M5 — Calibration | REQ-P12-01 … REQ-P12-05 | 5 |
| **Total** | — | — | **53** |

See `.planning/ROADMAP.md` for each phase's goal, success criteria, dependencies and
ordering constraints.

---
*v2.0.0 requirements defined: 2026-08-07*
