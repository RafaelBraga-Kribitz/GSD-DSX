# Roadmap

**Current milestone:** v2.0.0 DSX Validity Frame — Phases 6–12
**Shipped:** v1.1.0–v1.5.0 — Phases 1–5
**Granularity:** standard (phase structure fixed by `brief.md` §6; the seven milestones map 1:1 onto phases)

## Phases

- [x] **Phase 1: DQ + Evidence + Coherence** - profile contract, hermetic DQ gates, evidence resolution, question↔claim↔decision coherence (v1.1.0)
- [x] **Phase 2: Viz proof + plot construction** - chart matrix, figure seals, viz smells, Gate A–D verifier protocol (v1.2.0)
- [x] **Phase 3: Storytelling + code reality** - narrative discipline, forbidden-claim SSOT, SQL anti-patterns, entrypoint smells (v1.3.0)
- [x] **Phase 4: Analytical logic depth + stats extensions** - assumption checkoffs, TOST/CI/MDE, multiplicity, repro_lock, decision replay (v1.4.0)
- [x] **Phase 5: Chart review + suppressions** - ADR-authorised `suppressions[]`, scored CHART-REVIEW.md (v1.5.0)
- [x] **Phase 6: Contract extension, decision record, paradigm manifest** - `validity_frame:`/`inference:` blocks, decision records, `dsx explain`, `DSX-PAR-001`, D-05/D-03a enforcement (M1) — completed 2026-08-10
- [ ] **Phase 7: Validity frame checks (`DSX-VAL-*`)** - estimand, unit triad, dependence, identification strength, sampling frame, missingness, measurement (M2a)
- [ ] **Phase 8: Interference, triggering, stability (`DSX-INT-*`)** - SUTVA risk, shared-budget/marketplace patterns, triggered-vs-eligible dilution, novelty/primacy (M2b)
- [x] **Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`)** - the atomic `DSX-PAR-010`/`-011` pair plus `DSX-PAR-002` (M2c) — completed 2026-08-13
- [ ] **Phase 10: Pre-registered inference plan (`DSX-PRE-*`)** - fallback-rule DSL, `declared_at` provenance, declared-vs-executed branch reconciliation (M3)
- [ ] **Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`)** - `references/families.yaml`, ranked admissible set, `no_admissible_procedure` escalation (M4)
- [ ] **Phase 12: Calibration** - full known-bad corpus, measured catch rate and FPR, `dsx stats --paradigm`, backlog re-evaluation (M5)

---

## Phase 1 — DQ + Evidence + Coherence (v1.1.0) — COMPLETE

**Dimensions strengthened:** 1 (Analytical Question), 4 (Missing Evidence), 5 (Data Quality)

- `DATA-PROFILE.yaml` contract + `dsx profile` CSV runner (stdlib)
- Hermetic `DSX-DQ-*` gates against assertions ↔ profile
- Evidence pointer resolution (`DSX-CLM-031`–`033`)
- Question ↔ claim ↔ decision coherence (`DSX-COH-*`)
- Skill/fragment updates; fixtures; catalogue; tests

## Phase 2 — Viz proof + plot construction (v1.2.0) — COMPLETE

**Dimensions:** 3 (Chart Type), 8 (Plot Construction), 9 (Visual Design)

- Chart_Audit Gate A–D ordering in verifier fragment
- `DSX-SMELL-*` from code smells B/G/I/J/K/M; richer `visuals[]` fields
- Figure manifest + `svg_sha256` (`DSX-FIG-*`); `dsx seal`
- Hermetic Glyph-ready seals when `renderer: glyph` (no live MCP)
- `data_input_type` × chart capability matrix
- Takeaway heuristics (≠ name; digit/comparison)

## Phase 3 — Storytelling + code reality (v1.3.0) — COMPLETE

**Dimensions:** 6 (Code Quality), 10 (Communication / Storytelling)

- Narrative deliverable path; `%` without base lint; limitations required
- Forbidden-claim SSOT regexes (universal + optional phase file)
- Entrypoint smell scan; require `metric.sql` for warehouse sources
- Broader SQL anti-patterns; optional `dashboard:` for BI

## Phase 4 — Analytical logic depth + stats extensions (v1.4.0) — COMPLETE

**Dimensions:** 2 (Analytical Logic), 7 (Statistical Issues extensions)

- Causal assumption checkoffs / waivers (`DSX-COH-031`)
- Null-as-no-effect requires TOST/CI-in-bounds or detectable MDE (`DSX-STA-020`/`021`)
- Exploratory comparison count vs multiplicity family (`DSX-EXP-051`/`052`)
- `repro_lock` honest-null pattern (`DSX-REP-050`–`053`)
- Decision replay against `results.tests` (`DSX-DEC-*`)
- Metric reconciliation class tolerances (`DSX-MET-012` + class defaults)

## Phase 5 — Chart review + suppressions (v1.5.0) — COMPLETE

**Dimensions:** Chart Audit residual (scored review artifact, ADR suppressions)

- ANALYSIS-SPEC `suppressions[]` with reason + authority; unknown codes → exit 2
- `DSX-SPEC-070`–`072` for malformed/unknown suppressions
- `templates/CHART-REVIEW.md` + `references/chart-review-schema.md` (`dsx-chart-review-v1`)
- `dsx-viz-critic` writes CHART-REVIEW.md; skill `dsx-chart-audit` for standalone runs

---

## Phase Details — v2.0.0 DSX Validity Frame

Every phase below that ships checks carries the **D-05 bar**: each new check has a
primary-source citation in its docstring naming the *exact formulation*, and a test
against a published reference value (or a named structural criterion from that source
where the check is structural rather than numeric). If velocity pressure arrives, cut
checks, never this.

### Phase 6: Contract extension, decision record, paradigm manifest

**Goal**: The v2.0.0 contract surface exists and is trustworthy to read — `validity_frame:`
and `inference:` parse correctly, decision records accumulate and render, the paradigm
manifest is defined the moment `paradigm` becomes declarable, and D-05/D-03a are enforced
mechanically before any check family exists to violate them.

**Depends on**: Phase 5 (v1.5.0 shipped). **Blocks Phases 7–12** — no later family has
anything to read, import, or cite without this phase.

**Requirements**: REQ-P6-01, REQ-P6-02, REQ-P6-03, REQ-P6-04, REQ-P6-05, REQ-P6-06,
REQ-P6-07, REQ-P6-08, REQ-P6-09, REQ-P6-10, REQ-P6-11, REQ-P6-12, REQ-P6-13, REQ-P6-14,
REQ-P6-15, REQ-P6-16

**Ordering constraints** (within phase):

1. **REQ-P6-01 before REQ-P6-02.** The loader `_NULL` fix lands before the `validity_frame:`
   schema. Four frame fields (`dependence.structure`, `interference.risk`,
   `interference.mitigation`, `missingness.mechanism`) use `none` as a legitimate declared
   value and would otherwise parse as null. Reproduced: `_parse_yaml_subset("x: [none, clustered]")`
   returns `[None, "clustered"]` today.

2. **REQ-P6-09 ships here, not in Phase 9.** The instant `inference.paradigm` is a legal
   field an operator can declare `bayesian`, and the behaviour when they do must be defined
   from that moment. The only alternatives in the gap are "block" (which D-10 forbids) or
   "silently pass" (worse). Ordering constraint, not preference.

3. **REQ-P6-10 and REQ-P6-11 before the first frame check carries logic.** The D-03a AST
   boundary test and the citation-marker build check must exist before Phase 7 opens
   `frame/val.py`, or there is a window where a violation lands undetected.

**Success Criteria** (what must be TRUE):

  1. `_parse_yaml_subset("x: [none, clustered]")` returns `["none", "clustered"]` and a test
     asserts the bundled parser and PyYAML agree on `none` for scalars and sequences; only
     then does a spec carrying full `validity_frame:` + `inference:` blocks round-trip, with
     every new closed vocabulary dumped by `dsx vocab`, `dependence.method_family_required`
     typed against `VARIANCE_ADJUSTMENTS`, `PEEKING_POLICIES` carrying a member for
     uncontrolled continuous monitoring distinct from `always_valid`, and no
     `inference.stopping_rule` field anywhere.

  2. `dsx gate` exits `0` at plan/execute/verify/ship on the extended
     `examples/good-ANALYSIS-SPEC.yaml` and `1` at plan and at ship on the extended
     `examples/bad-ANALYSIS-SPEC.yaml`, with the two existing D-08 tests unchanged; a
     descriptive-question spec that omits `interference`/`triggering`/`stability` **entirely**
     also exits `0`, while a causal spec omitting them blocks.

  3. A `paradigm: bayesian` spec that is otherwise clean exits `0` at `dsx gate ship` with the
     `DSX-PAR-001` manifest printed on stdout naming which check families applied and which
     did not — INFO cannot flip the exit code at any configured threshold — and `dsx explain`
     exits `0` rendering that run's decision trail from an append-only `DECISIONS.jsonl` that
     survives a crashed run.

  4. D-05 and D-03a are mechanical, not review-only: `scripts/gen-finding-catalogue.py --check`
     exits non-zero on a check whose docstring lacks a citation marker, and the AST boundary
     test fails when a `dsx/frame/*.py` module imports `dsx.checks.*` — each proven against a
     deliberately violating case in the suite.

  5. At least three known-bad fixtures (≥1 interference case, ≥1 Bayesian continuous-monitoring
     case) are committed with documented post-mortems and pass `dsx validate` structurally —
     the code-specific block assertions land with the phase that ships each code — alongside
     `.planning/REVERSALS.md` with the D-14 template and `SELF-001` convention, README text for
     the `suppressions[]` migration path and the "a frame that lies passes" limit, version
     2.0.0, and a regenerated finding catalogue.

**Plans:** 13/13 plans executed

Plans:
**Wave 1**

- [x] 06-01-PLAN.md — loader `_NULL` fix + the ten new closed vocabularies, `uncontrolled_continuous`, and the `_VOCABULARIES` registry behind `dsx vocab` (wave 1)
- [x] 06-02-PLAN.md — `dsx/decisions.py`: record schema, fsync-per-record append, tolerant reader, invocation identity and frame digest (wave 1)
- [x] 06-03-PLAN.md — D-05 made mechanical in `scripts/gen-finding-catalogue.py`, proven against a deliberately violating fixture (wave 1)
- [x] 06-04-PLAN.md — `.planning/REVERSALS.md`, README migration path + known limit + the two tiers of D-05 rigour, PROJECT.md gate-point amendment (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 06-05-PLAN.md — extend both canonical fixtures and scaffold the template with `validity_frame:` and `inference:`; pin the round-trip (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 06-06-PLAN.md — `_validate_validity_frame_shape` / `_validate_inference_shape` under `DSX-SPEC-080`–`086`, with question_type-gated requiredness (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 06-07-PLAN.md — `dsx/frame/` + the D-03a AST boundary test + `DSX-PAR-001`, the INFO paradigm manifest, registered at all four gate points (wave 4)
- [x] 06-08-PLAN.md — the known-bad seed corpus: interference, frequentist and Bayesian uncontrolled-continuous, each with a sourced post-mortem (wave 4)

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 06-09-PLAN.md — `dsx explain` (never blocks) + the `add_common` refactor + the gate-path `DECISIONS.jsonl` write (wave 5)

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 06-10-PLAN.md — version 2.0.0 across every manifest, catalogue regeneration, and the closing phase gate (wave 6)

**Wave 7** *(gap closure — blocked on Wave 6 completion; closes `06-VERIFICATION.md`)*

- [x] 06-11-PLAN.md — BLOCKER: no decision-trail failure mode can change a gate exit code, `dsx explain` returns 0 by construction, WR-02 concurrency limitation documented (wave 7)
- [x] 06-12-PLAN.md — correct the known-bad corpus's false gate claim and pin the real guarantee with gate-level tests (wave 7)
- [x] 06-13-PLAN.md — boundary-safe D-05 allow-list, corrected `inference:` validation comment, collapsed dead branch in `_package_for` (wave 7)

### Phase 7: Validity frame checks (`DSX-VAL-*`)

**Goal**: The paradigm-independent content of the frame is adjudicated — a missing or
unfalsifiable estimand, a unit triad that guarantees pseudo-replication, dependence declared
with no method family, weak identification dressed as strong, a sampling frame that cannot
carry the claim population, a missingness mechanism the implied method cannot survive, and a
measurement construct with no operationalisation each block before the data is touched.

**Depends on**: Phase 6 (contract, vocabularies, `dsx/frame/` package, boundary test).
**Blocks Phase 11** — `references/families.yaml` is keyed in part on the
`validity_frame.dependence` taxonomy this phase establishes.

**Requirements**: REQ-P7-01, REQ-P7-02, REQ-P7-03, REQ-P7-04, REQ-P7-05, REQ-P7-06,
REQ-P7-07, REQ-P7-08, REQ-P7-09

**Ordering constraints**: None internal. No hard ordering against Phases 8 and 9 — the three
read disjoint sub-blocks and could be parallelised; sequenced here by catastrophe-prevention
value per unit of work.

**Open items** (resolve at discuss, do not decide silently): whether
`dependence.method_family_required` becomes set-valued, since M-09's reuse of
`VARIANCE_ADJUSTMENTS` cannot express the brief's `cluster_robust_or_mixed`; final numeric code
assignments within `DSX-VAL-*` beyond those the brief fixes (D-06 makes numbering irreversible).

**Success Criteria** (what must be TRUE):

  1. `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` exits `1` at
     `dsx gate plan` naming `DSX-VAL-040`; a spec declaring strong identification whose
     constraint carries parameter-scale information surfaces `DSX-VAL-041` at HIGH — printed
     but non-blocking at plan, blocking at verify/ship — both citing Gelman, Simpson &
     Betancourt (2017).

  2. A spec whose `units.observation` is finer than `units.assignment` with no dependence
     method family exits `1` under `DSX-VAL-020`, and the finding text quantifies the
     consequence via `DEFF = 1 + (m-1)·ICC`, with a test asserting the published worked value.

  3. `DSX-VAL-020` and the existing `DSX-EXP-021` never both fire on the same defect: a fixture
     tripping `DSX-EXP-021` produces no `DSX-VAL-020` and vice versa, and `dsx gate` output on
     the existing v1.5.0 `DSX-EXP-020/021` fixtures is unchanged.

  4. Each of estimand incompleteness/non-falsifiability, dependence-declared-without-method-family,
     sampling frame vs claim population, missingness mechanism vs implied method (against the
     Rubin MCAR/MAR/MNAR validity table), and measurement construct/operationalisation gaps
     blocks its own bad fixture and passes the extended good fixture — every check carrying a
     primary-source citation naming the exact formulation plus a test against a published
     reference value or a named structural criterion.

  5. A test asserts that no `dsx/frame/val.py` code path reads `inference.paradigm` (D-11),
     failing the suite if one is introduced.

**Plans:** 7/7 plans executed

Plans:
**Wave 1**

- [x] 07-01-PLAN.md — shared contract constants and the design-effect helper (wave 1)
- [x] 07-02-PLAN.md — citation ledger extension and the unpublished-number correction (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 07-03-PLAN.md — `dsx/frame/val.py` lands with the estimand checks, all build plumbing and the no-paradigm-read invariant (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 07-04-PLAN.md — unit triad and unit drift, with the template and interference fixture repaired in the same commits (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 07-05-PLAN.md — dependence and identification, with the template repair and the documented corpus allow-list entry (wave 4)

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 07-06-PLAN.md — sampling frame, missingness and measurement, with the good fixture repaired in the same commit (wave 5)

**Wave 6** *(blocked on Wave 5 completion)*

- [x] 07-07-PLAN.md — the weak-identification fixture, its post-mortem, and the corpus-test conflict resolution (wave 6)

### Phase 8: Interference, triggering, stability (`DSX-INT-*`)

**Goal**: The largest uncovered risk class for a 60%-experiment workload is adjudicated —
declared interference with no mitigation and no residual note, shared-budget and marketplace
patterns treated as distinct risks, triggered-versus-eligible analysis populations with no
dilution adjustment, and unassessed novelty/primacy over the declared stability window.

**Depends on**: Phase 6. No hard dependency on Phase 7 or Phase 9 — the sub-blocks are
disjoint (`interference`/`triggering`/`stability` vs the rest), so this phase could run in
parallel with either.

**Requirements**: REQ-P8-01, REQ-P8-02, REQ-P8-03, REQ-P8-04, REQ-P8-05, REQ-P8-06

**Ordering constraints**: None internal. Ratio-metric dilution is descoped up front
(REQ-P8-04) — shipping a plausible-looking equation obtained from a secondary source would
violate D-05.

**Open items**: final numeric code assignments within `DSX-INT-*` beyond `DSX-INT-030`, which
the brief fixes verbatim and D-06 makes irreversible.

**Success Criteria** (what must be TRUE):

  1. `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` exits `1` at
     `dsx gate plan` naming `DSX-INT-010`; the same spec with an admissible `mitigation` or an
     explicit `residual_note` added exits `0` — citing the SUTVA statement in Imbens & Rubin
     (2015).

  2. Shared-budget and marketplace interference resolve to distinct declared risks with distinct
     admissible mitigations: a fixture applying a marketplace-only mitigation to a shared-budget
     risk still exits `1`.

  3. `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` exits `1` under `DSX-INT-030`
     when an additive metric is analysed on the eligible population with no dilution adjustment
     declared, and a test asserts `delta_diluted = delta_triggered × trigger_rate` against the
     Deng & Hu (2015) published counterexample — the paper's time-to-success case, where the
     paper reports a true effect of −26 msec against the naive formula's −18 msec. Time-to-success
     is itself a ratio metric, so the paper prints this pair to show the additive formula failing
     there, which means the same test also proves the additive-only scope boundary success
     criterion 4 requires. (Corrected per 08-CONTEXT.md D-10: the previous wording asked for a
     value the paper publishes, but the full camera-ready contains no additive worked example at
     all — every number in it is for a ratio metric — so the original wording asked for something
     the paper does not contain.)

  4. A ratio metric under triggering is explicitly out of scope rather than silently adjudicated:
     `DSX-INT-030` does not fire on it, its docstring states the additive-only scope, and
     `brief.md` §6.5 carries an entry condition naming the per-unit trigger and outcome data that
     Formula (3) in §3.3 requires reaching the gate — because that equation sums over individual
     users and has no closed-form scalar multiplier, unlike the additive Formula (1) — and notes
     the item may be permanently out of scope for a declaration-only gate rather than merely
     deferred. (Corrected per 08-CONTEXT.md D-12: the previous wording conditioned the item on
     retrieving the equation from a primary source; that retrieval was already achievable — the
     paper is freely public and Formula (3) is readable today — so the condition was already met
     and would have unblocked the item immediately, which was never the intent.) (D-13)

  5. An unassessed novelty/primacy effect over the declared stability window is flagged at
     verify/ship with the assessment method cited, and a test asserts no
     `dsx/frame/interference.py` code path reads `inference.paradigm` (D-11).

**Plans:** 8/9 plans executed

Plans:
**Wave 1**

- [x] 08-01-PLAN.md — the published dilution formula in the math kernel, with its
      counterexample test and range validation (wave 1)

- [x] 08-02-PLAN.md — corpus prophylaxis: honest stability declarations, the per-fixture
      target-defect map, and the new triggering-dilution fixture pair (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 08-03-PLAN.md — `dsx/frame/interference.py` lands with `DSX-INT-010`/`011`, the
      risk-to-mitigation map and all build plumbing in one commit (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 08-04-PLAN.md — `DSX-INT-030`, the additive metric partition, and the gated-backlog
      row recording why ratio-metric dilution stays out of scope (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 08-05-PLAN.md — `DSX-INT-040` at HIGH with its disjointness statement, plus the
      malformed-shape hardening sweep over all four codes (wave 4)

**Wave 5** *(blocked on Wave 4 completion)*

- [x] 08-06-PLAN.md — the two success-criteria corrections and the matching REQ-P8-04
      amendment; the phase's only writer of the tracking files (wave 5)

**Wave 6** *(gap closure — blocked on Wave 5 completion)*

- [x] 08-07-PLAN.md — close the `DSX-INT-010`/`011` out-of-vocabulary mitigation bypass
      (08-VERIFICATION.md CR-01) and the four warning-level review items (wave 6)

**Wave 7** *(gap closure — blocked on Wave 6 completion)*

- [x] 08-08-PLAN.md — close the `DSX-INT-010` out-of-vocabulary `interference.risk` bypass
      (08-VERIFICATION.md gap 1 / 08-REVIEW.md CR-01), keeping `DSX-INT-011` provably
      untouched (wave 7)

**Wave 8** *(gap closure — blocked on Wave 7 completion)*

- [ ] 08-09-PLAN.md — close the `DSX-INT-030` out-of-vocabulary `triggering.analysis_population`
      bypass (08-VERIFICATION.md gap 2 / 08-REVIEW.md CR-02), correct the decision trail, and
      tighten the weak `DSX-SPEC-082` gate assertion (WR-01) (wave 8)

### Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`)

**Goal**: Uncontrolled continuous monitoring blocks under both paradigms, neither half can be
escaped by retyping `paradigm`, and neither half is cheaper to satisfy dishonestly than the
other. Three checks, symmetric by construction — deliberately not "the Bayesian phase".

**Depends on**: Phase 6 (the `inference:` block, the `PEEKING_POLICIES` member, `DSX-PAR-001`,
and the Bayesian continuous-monitoring known-bad fixture). No hard dependency on Phase 7 or 8.

**Requirements**: REQ-P9-01, REQ-P9-02, REQ-P9-03, REQ-P9-04, REQ-P9-05, REQ-P9-06, REQ-P9-07

**Ordering constraints**: **`DSX-PAR-010` and `DSX-PAR-011` are atomic (D-12)** — both ship or
neither ships, at identical severity. This phase cannot be marked complete with one half
delivered; a half-shipped pair is precisely the silent paradigm-steering the family exists to
prevent.

**Open items**: whether the pre-existing `inflation_from_peeking()` docstring ("Armitage's
classic result", no year or paper) is upgraded to a full D-05 citation now that new checks
depend on it.

**Success Criteria** (what must be TRUE):

  1. A frequentist spec declaring the uncontrolled-continuous `design.peeking_policy` with no
     `alpha_spending` and no sequential method exits `1` at `dsx gate plan` naming
     `DSX-PAR-010`, reusing the existing `inflation_from_peeking()` table rather than a second
     one, while `DSX-EXP-060`'s own fixtures and output are unchanged (M-01).

  2. `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` — the spec asserting
     that a weakly informative prior controls false positives while peeking — exits `1` naming
     `DSX-PAR-011`, and a test asserts the prior-averaged bound `1/(K+1)`: at the
     `P(B>A) > 0.95` threshold, `K = 19` and the bound is `0.05`, traced to Deng, Lu & Chen
     (2016) Theorem 1 — whose likelihood-ratio argument is not Ville's inequality, which
     gives the different bound `1/k` (`1/19 ≈ 0.0526`) and must not be substituted.

  3. The `DSX-PAR-011` docstring states explicitly that it asserts the prior-averaged
     formulation and **not** the point-null / law-of-iterated-logarithm formulation, and the
     fixture comments the theorem its number traces to — so a mismatch reads as a formulation
     question in five minutes, not an implementation bug for a day.

  4. Switching `paradigm` cannot buy a pass in either direction: the `DSX-PAR-010` bad fixture
     retyped to `bayesian` still exits `1` (now under `DSX-PAR-011`), and the `DSX-PAR-011` bad
     fixture retyped to `frequentist` still exits `1` (now under `DSX-PAR-010`) — asserted by
     test both ways; `DSX-PAR-002` requires `paradigm_justification` (presence and
     requiredness only) and `DSX-SPEC-085` validates it against the closed vocabulary,
     with no reason ranked above another (D-08 — membership is not duplicated so one
     defect cannot emit two codes).

  5. Both codes ship together at identical severity, and a committed audit records the cheapest
     dishonest satisfaction path for each half, showing the disjunctive `prior_justification`
     route is no weaker than the sequential-method requirement (D-12); the `DSX-PAR-011`
     simulation lives under `tests/`, seeded and reproducible, and never on the gate path (D-02).

**Plans**: 7/7 plans executed

Plans:
**Wave 1**

- [x] 09-01-PLAN.md — Symmetry audit written first, plus the three new `inference:` fields the pair reads (wave 1)
- [x] 09-02-PLAN.md — `inflation_from_peeking()` citation upgrade and the seeded, off-gate-path simulation (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 09-03-PLAN.md — The atomic pair `DSX-PAR-010` and `DSX-PAR-011`, both halves in one commit at CRITICAL (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 09-04-PLAN.md — Known-bad corpus prose corrected, and a positive-content test under the symmetry audit (wave 3)
- [x] 09-05-PLAN.md — `DSX-PAR-002` requiredness and the fourteen-case symmetry proof (wave 3)

**Wave 4** *(gap closure — `09-VERIFICATION.md` gap 1 / `09-REVIEW.md` CR-01, REQ-P9-06)*

- [x] 09-06-PLAN.md — Text-only clearing predicate (`is_blank_text`) closes the bare-`0`/`false` escape, and the symmetry audit is corrected to match (wave 4)

**Wave 5** *(gap closure — `09-VERIFICATION.md` gap 2 / `09-REVIEW.md` CR-02, REQ-P9-03)*

- [x] 09-07-PLAN.md — `DSX-PAR-011`'s emitted finding text and the known-bad fixture comment stop committing the Theorem 1 locator error (wave 5)

**Wave note (atomicity, D-12):** `DSX-PAR-010` and `DSX-PAR-011` are both delivered by a single
plan, 09-03, in a single commit at the identical severity `CRITICAL`. They cannot land separately.
The phase is incomplete until both are green; a half-shipped pair is a stop-and-report condition.

### Phase 10: Pre-registered inference plan (`DSX-PRE-*`)

**Goal**: The declared inference plan is held to the executed one — a fallback rule parses to a
decidable branch, `declared_at` provenance is named for the unverifiable self-declaration it is,
and a procedure switched after seeing the data is blocked with both branches named.

**Depends on**: Phase 6 (hard — `inference.fallback_rule`, `declared_at`, and the decision-record
channel). Soft dependency on Phase 7: the brief's own fallback-rule example references
`clusters`, whose meaning only settles once `validity_frame.dependence` is enforced.

**Requirements**: REQ-P10-01, REQ-P10-02, REQ-P10-03, REQ-P10-04

**Ordering constraints**: Registered at verify/ship only — there is no executed branch to
reconcile against at plan or execute.

**Success Criteria** (what must be TRUE):

  1. A fallback rule in the mini-DSL (e.g. `if clusters < 30 -> wild cluster bootstrap`)
     resolves to exactly one branch against the declared observed facts, and an unparseable rule
     exits `2` — could-not-run — never `0`.

  2. A run whose executed procedure differs from the branch the declared rule selects exits `1`
     at `dsx gate verify`, with both the declared branch and the executed branch named in the
     finding text.

  3. A procedure switched after seeing the data exits `1` even when the substituted procedure is
     individually defensible — a fixture whose substitution is a strictly more conservative test
     still blocks.

  4. `declared_at` provenance is recorded and named as an unverifiable self-declaration in both
     the finding remedy and the README rather than presented as a guarantee; where a content lock
     over `validity_frame:` + `inference:` is captured at plan, reconciliation compares the
     recorded bytes, not the declared string.

  5. Every `DSX-PRE-*` check carries a primary-source citation naming its exact formulation plus
     a test against a published reference value or a named structural criterion, and a test
     asserts every `DSX-PRE-*` code is reachable from at least one `GATE_PROFILES` entry.

**Plans**: 6 plans

Plans:
**Wave 1**

- [ ] 10-01-PLAN.md — Fact registry and the arrow-triggered fallback-rule mini-language (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 10-02-PLAN.md — `DSX-PRE-010` and `DSX-PRE-030`, plus all five D-13 guards in one commit (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 10-03-PLAN.md — `DSX-PRE-020` content-lock reconciliation and the missing-header exit 2 (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 10-04-PLAN.md — Registration at verify/ship and the test-harness blast radius (wave 4)

**Wave 5** *(blocked on Wave 4 completion)*

- [ ] 10-05-PLAN.md — The `post-hoc-procedure-switch` known-bad fixture pair and its corpus test (wave 5)
- [ ] 10-06-PLAN.md — README known limits, the `brief.md` §7 citation anchor, STATE.md (wave 5)

**Wave note (guard atomicity, D-13):** the five forcing guards trip on the first
`report.add("DSX-PRE-…")` call site, not on the `GATE_PROFILES` edit — `known_codes()` scans source
and ignores registration. They are therefore fixed inside 10-02, in the same commit as the first
code. Separately, the `GATE_PROFILES` edit and the `tests/test_known_bad_corpus.py::_gate_findings`
repair are both inside 10-04 and must land in one commit: registering `prereg` without the harness
repair makes every existing fixture stop at exit 2 at verify and ship, surfacing as a JSON decoding
error rather than a legible assertion.

### Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`)

**Goal**: Given a coherent frame, the tool names which frequentist procedures are admissible and
what each one costs in assumptions — and refuses rather than guesses when the frame is
underdetermined.

**Depends on**: Phase 7 (hard — `references/families.yaml` is keyed in part on the
`validity_frame.dependence` taxonomy; building the ontology before that taxonomy is stable risks
keying it on a shape that changes underneath it) and Phase 6. Neither
`references/families.yaml` nor `dsx/frame/admissibility.py` is created before this phase
(brief §6.6 item 2 — an empty ontology accumulates speculative structure).

**Requirements**: REQ-P11-01, REQ-P11-02, REQ-P11-03, REQ-P11-04, REQ-P11-05, REQ-P11-06

**Ordering constraints**: The ontology is built from the calibration corpus and the known-bad
fixtures, not from taxonomic completeness — a family is added when a real case needs it. The
`no_admissible_procedure → escalate` branch is the scope-bounding mechanism, so there is no
completeness pressure on the alias list.

**Open items**: final numeric code assignments within `DSX-ADM-*` beyond those the brief fixes.

**Success Criteria** (what must be TRUE):

  1. `references/families.yaml` holds 25–35 estimator families as data keyed on
     estimand × family × inference method × dependence handling, parsed by the existing
     `dsx.loader.load()` with no new parser, and named tests resolve as aliases into families
     rather than being enumerated as a test catalogue.

  2. `dsx recommend-test` returns a ranked admissible set naming, per entry, the assumptions
     bought and the assumptions charged — the existing subcommand extended, not replaced, with
     its v1.5.0 behaviour on existing specs unchanged.

  3. A deliberately underdetermined frame returns `no_admissible_procedure` and exits `1` under
     the escalating code at CRITICAL rather than falling back to the nearest-sounding family,
     and an unrecognised alias escalates rather than resolving.

  4. A `families.yaml` entry with no citation fails the build via the Phase 6 catalogue check,
     and the adjudicator refuses to rank an uncited family — D-05 binds the ontology data
     exactly as it binds check code.

  5. Every family entry traces to a fixture or corpus case that needed it, and a test asserts no
     `families.yaml` entry declares a Bayesian inference method — the axis space is capped to
     v1's frequentist scope, with Bayesian admissibility left in the gated backlog.

**Plans**: TBD

### Phase 12: Calibration

**Goal**: There is a number. Measured catch rate and false-positive rate across a full-size
known-bad corpus, a paradigm split across the operator's own frame history, and every
gated-backlog entry condition either evaluated against measured evidence or removed.

**Depends on**: Phases 6–11. Necessarily last — this phase measures everything before it, and
the backlog entry conditions it evaluates (including "`dsx stats --paradigm` shows Bayesian
frames above 15%") cannot be evaluated until it ships.

**Requirements**: REQ-P12-01, REQ-P12-02, REQ-P12-03, REQ-P12-04, REQ-P12-05

**Ordering constraints**: REQ-P12-02 (structured catch-attribution tags) is instrumented as each
corpus case is added, not retrofitted after "full size" is declared reached — otherwise "three
cases where absence permitted a false pass" is a debate, not a count.

**Success Criteria** (what must be TRUE):

  1. The known-bad corpus is extended from the Phase 6 seed set to full size — retracted papers
     with published post-mortems, documented p-hacking cases, and prior work whose answer is now
     known — each case committed as a spec + post-mortem pair.

  2. A harness run over the corpus reports a catch rate and a false-positive rate as numbers,
     reproducibly, with per-case pass/block recorded and attributable to specific codes.

  3. Every corpus case carries structured, machine-readable catch-attribution tags naming which
     currently-absent code would have caught it, so each `brief.md` §6.5 entry condition is
     counted rather than argued (D-13).

  4. `dsx stats --paradigm` exits `0` and reports the frequentist/Bayesian split across the
     operator's own frame history — the value the Bayesian-admissibility entry condition is
     stated against.

  5. Each gated-backlog item is re-evaluated against its stated entry condition using the
     measured corpus, and any item whose condition cannot be evaluated is removed from §6.5
     rather than carried — with a D-14 reversal record where a removal reverses a prior decision.

**Plans**: TBD

---

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. DQ + Evidence + Coherence | — | Complete | v1.1.0 |
| 2. Viz proof + plot construction | — | Complete | v1.2.0 |
| 3. Storytelling + code reality | — | Complete | v1.3.0 |
| 4. Analytical logic depth + stats extensions | — | Complete | v1.4.0 |
| 5. Chart review + suppressions | — | Complete | v1.5.0 |
| 6. Contract extension, decision record, paradigm manifest | 13/13 | Complete | 2026-08-10 |
| 7. Validity frame checks (`DSX-VAL-*`) | 7/7 | In Progress|  |
| 8. Interference, triggering, stability (`DSX-INT-*`) | 8/9 | In Progress|  |
| 9. Monitoring discipline, symmetric (`DSX-PAR-*`) | 7/7 | Complete | 2026-08-13 |
| 10. Pre-registered inference plan (`DSX-PRE-*`) | 0/TBD | Not started | - |
| 11. Frequentist admissibility adjudicator (`DSX-ADM-*`) | 0/TBD | Not started | - |
| 12. Calibration | 0/TBD | Not started | - |

## Dependency graph — v2.0.0

```
Phase 6 (M1) ──┬──> Phase 7 (M2a) ──┬──> Phase 10 (M3, soft) ──┐
               │                    │                          │
               ├──> Phase 8 (M2b)   └──> Phase 11 (M4, hard) ───┼──> Phase 12 (M5)
               │                                               │
               └──> Phase 9 (M2c) ─────────────────────────────┘
```

- Phase 6 is the only true single point every other phase depends on.
- Phases 7, 8 and 9 are mutually independent and could be parallelised; they are listed in
  the brief's order, which is catastrophe-prevention value per unit of work.

- Phase 10 is soft-sequenced after Phase 7 (fallback-rule DSL semantics).
- Phase 11 hard-depends on Phase 7 (dependence taxonomy).
- Phase 12 is terminal by construction.

## Coverage

All 53 v2.0.0 requirements map to exactly one phase. No orphans, no duplicates.

| Phase | Requirements | Count |
|-------|--------------|-------|
| 6 | REQ-P6-01 … REQ-P6-16 | 16 |
| 7 | REQ-P7-01 … REQ-P7-09 | 9 |
| 8 | REQ-P8-01 … REQ-P8-06 | 6 |
| 9 | REQ-P9-01 … REQ-P9-07 | 7 |
| 10 | REQ-P10-01 … REQ-P10-04 | 4 |
| 11 | REQ-P11-01 … REQ-P11-06 | 6 |
| 12 | REQ-P12-01 … REQ-P12-05 | 5 |
| **Total** | | **53** |
