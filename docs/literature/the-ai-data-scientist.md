# The AI Data Scientist — what DSX took from it, and what it refused

**Paper:** Akimov, F., Nwadike, M.S., Iklassov, Z. and Takáč, M. (2025), *The AI Data
Scientist*, arXiv:2508.18113v1 (Mohamed bin Zayed University of Artificial
Intelligence). Read in full from the arXiv HTML on 2026-08-20 (Phase 11.1) and again on
2026-09-06 for this record. The full text is deliberately **not** committed to this
repository; the arXiv listing is the source of record.

**Why it matters to this project.** The paper is the clearest published statement of
the pattern DSX exists to gate: six large-language-model subagents — Data Cleaning,
Hypothesis, Preprocessing, Feature Engineering, Model Training, Call-to-Action —
running in sequence from a raw table to a business recommendation in about ten
minutes. Its worked code (Tables 1, 2 and 5) is executable, so it could be reproduced
stage for stage rather than argued with. That reproduction is
`examples/known-bad/full-frame-cleaning-*`: before Phase 11.1 the gate passed it with
**zero findings**; afterwards it blocks at `dsx gate execute` on three CRITICAL codes
and one HIGH. That measured before/after is the strongest evidence in this repository
that the gate catches something real.

This document records, section by section, which of the paper's ideas are present in
DSX, which are present as the thing DSX catches, and which are deliberately on the
backlog with an entry condition. It exists so a reader who knows the paper can see
that the project engaged with it rather than ignored it.

## The mapping

| # | Paper idea (section) | DSX position | Where it lives | Status |
|---|---|---|---|---|
| 1 | Six subagents in sequence, passing structured JSON metadata forward (§2) | The contract **is** the handoff — but declaration-first, not data-first: the architect writes `ANALYSIS-SPEC.yaml` before any data is touched, and every later role reads it. `EDA.md` front-matter, `DATA-PROFILE.yaml`, `DATA-DICTIONARY.md` and the `DECISIONS.jsonl` trail carry the measured facts between stages. | `agents/dsx-analysis-architect.md`; `capabilities/dsx/fragments/executor.md` ("read `EDA.md` front-matter first"); `templates/EDA.md`; `dsx/decisions.py` | Present |
| 2 | Data Cleaning subagent: mean/median/MICE imputation and z-score/IQR outlier removal over the whole frame (§2.1) | Refused. Statistics fitted on the full frame before the split are leakage (taxonomy type 3). The entrypoint scan fires on the paper's own idioms; the spec can declare where each cleaning step was fitted and is held to it. | `DSX-CODE-020` (CRITICAL) in `dsx/checks/code.py`; `data[].cleaning[].fit_on` with `DSX-ML-023`/`024`; `references/leakage-taxonomy.md` | Present, as a catch |
| 3 | Hypothesis subagent: LLM proposes hypotheses, each tested against the target on the full frame at p < 0.05, accepted ones appended as feature columns (§2.2, Tables 1 and 5) | Refused twice over. A test that sees the target before the split, then decides which features survive, is target-informed selection; a stream of hypotheses accepted at 0.05 with no declared family is the garden of forking paths. DSX's hypothesis register routes each untested belief to a carrier a check already reads — `assumptions[]` or a pre-declared `design.multiplicity.family[]` — and promotion from exploratory to confirmatory is a spec amendment, never an append. | `DSX-CODE-030` (statistical test sees the target); `DSX-EXP-050`–`053` and `results.comparisons_looked_at`; the hypothesis register in `skills/dsx-explore-data/SKILL.md`; ML-auditor heuristic 7 | Present, as a catch and a protocol |
| 4 | Table 1: a broad toolkit of tests the subagent may choose from | Tests are derived, not chosen: `dsx recommend-test` returns the procedure from the outcome shape, group count, pairing and dependence, with a primary-source citation per row. Looking at the data and then choosing the rule is the two-stage pattern D-01/D-02 ban. | `references/test-selection.md`; `references/families.yaml`; `tests/test_no_shapiro_autoswitch.py` | Present, stronger |
| 5 | Preprocessing subagent: `min_max_scaler.fit_transform(data[['Balance']])` on the whole frame (§2.3, Table 2) | Refused. A post-split fit whose first argument is not a training frame fires; the whole-pipeline boundary is a declaration the code is audited against. | `DSX-CODE-021`; `DSX-CODE-001`–`003`; `model.preprocessing_fit_on` | Present, as a catch |
| 6 | Binning a continuous column unless a full-frame test found a numeric relationship (§2.3) | Recorded as a compound leak: information loss plus a target-adjacent decision made on a full-frame test. | Discretisation note in `references/leakage-taxonomy.md`, citing §2.3 directly | Present, as guidance |
| 7 | Feature Engineering: roughly 200 features per cycle, each "traceable to the hypothesis that motivated it" (§2.4, Table 3) | The traceability idea is accepted in principle and sits on the gated backlog as a per-feature provenance list. The volume is refused: every feature is screened against a leakage lexicon, and exclusions must be declared. | `DSX-ML-030`–`032`; `model.features_excluded_for_leakage`; `brief.md` §6.5 item 7 | Present as a catch; per-feature provenance list now **satisfied** — attributed miss via `DSX-ML-034` on `feature-origin-only-leak` (see below) |
| 8 | Model Training: 18 regression and 18 classification candidates, grid or random search, stacking and voting ensembles, k-fold, reports accuracy/F1 or RMSE/R² (§2.5, Table 4) | Refused as preprocessing leakage at model-selection scale. A declared algorithm owes a selection ledger; selecting on the test set is CRITICAL; selecting on the same folds as the reported score is HIGH; a reported score must say where it came from and how much its folds vary; a baseline is required; imbalance-unsafe metrics are flagged; and, since v2.4.1, error metrics are compared in the right direction. | `model.selection_ledger` with `DSX-ML-090`/`091`/`092`; `results.model_score_source` and `fold_scores` with `DSX-ML-052`/`053`; `DSX-ML-050`/`051`; `DSX-ML-041`/`043`; `model.metric_direction`; leakage-taxonomy type 3 sub-case; ML-auditor heuristic 8 | Present, as a catch |
| 9 | Call-to-Action: "customers using fewer than two products are 25% more likely to leave", followed by "offer bundled incentives", with KPIs, timelines and post-deployment monitoring (§2.6, Figure 4) | Two halves. The plain-language, KPI-anchored, monitored recommendation is adopted and made gate-readable: `revisit_when` (a metric, a threshold, a time anchor) is what retires a recommendation. The example itself is refused: a prescriptive claim under a descriptive churn question with no identification strategy is exactly what the flagship fixture blocks. | `decision.revisit_when` (`DSX-COH-040`); `decision.replay`; `action_if_null`; `limitations` (`DSX-CLM-080`); What / So What / Now What in `skills/dsx-narrate`; `examples/known-bad/prescriptive-churn-recommendation-*` (`DSX-COH-001`/`010`, `DSX-CLM-020`) | Present, stronger |
| 10 | A magnitude ("25% more likely") reported from a chi-square test that computed no such magnitude (§2.6, Table 5) | The paper-shaped instances already fire: a relative percentage must declare its base, and every reported test must carry an effect size. The residual — an absolute magnitude no test computed — is on the backlog. | `DSX-CLM-070`; `DSX-STA-012`; `brief.md` §6.5 item 8 | Present; magnitude residual now **satisfied** — attributed miss via `DSX-CLM-034` on `magnitude-without-computed-effect` |
| 11 | Safeguards: power checks and false-discovery-rate control (§6) | Present, but required *before* the tests rather than applied afterwards: power arithmetic at design time, a declared correction from a closed vocabulary that includes Benjamini–Hochberg, and a declared family. | `dsx power`; the power-reporting gate; `MULTIPLICITY_CORRECTIONS`; `design.multiplicity` | Present |
| 12 | Fairness testing and subgroup performance checks (§6) | Lives in the agent prompts as a guardrail — the architect asks who bears the cost if the recommendation is wrong for a subgroup; the storyteller must name it — and in the Simpson-reversal check over declared segments. A declaration-level check is on the backlog behind a primary source with operationalisable criteria. | `agents/dsx-analysis-architect.md` step 1; `agents/dsx-data-storyteller.md`; `results.segments`; `brief.md` §6.5 item 9 | Agent guardrail; declaration-level gate now present — catch via `DSX-COH-041` on `subgroup-harm-without-disposition` |
| 13 | Causal caution: associations validated by tests are not causes (§6, §7) | Present as structure, not caution: the claim type may not exceed the question type; causal verbs are tiered and gated; a causal question owes an identification strategy from a closed vocabulary. | `IDENTIFICATION_STRATEGIES`; causal verb tiers in `dsx/spec.py`; `DSX-CAU-*`, `DSX-COH-*`, `DSX-CLM-*` | Present, stronger |
| 14 | Subagents "revisited multiple times ... several cycles of hypothesis refinement ... to enhance predictive performance" (§2) | Refused. Refining until the model predicts is test-set contamination through iteration (taxonomy type 7). The exploratory-to-confirmatory handshake runs one way: an EDA candidate becomes a declared test through a spec amendment, and the comparisons ledger counts every look. | `references/leakage-taxonomy.md` type 7; `DSX-ML-070`–`072`; `results.comparisons_looked_at`; the candidate handshake in `skills/dsx-explore-data` | Present, as a catch |
| 15 | Evaluation on Kaggle datasets against expert notebooks; proof-of-concept on public leaderboards (§3, §5) | Not applicable to a gate library. The analogue is the calibration corpus: a measured miss-rate over attributable misses, a false-positive rate over clean controls, and per-tier catch strata. As of the Phase-30 terminal re-baseline (2026-09-10): 42 known-bad specs, 15 good-control specs, every `DSX-VIZ-*` code the declared target of a fixture. | `examples/known-bad/`, `examples/good-corpus/`, `tests/test_known_bad_corpus.py` | Analogue present |
| 16 | A three-layer safety framework: automated statistical sanity checks, output guardrails, human escalation (§5) | Present: deterministic gates; forbidden-claim and narrative checks; decision records the gate emits instead of stopping to teach, and a human queue for what only a person can answer. | `dsx gate`; `DSX-NAR-*`, `templates/FORBIDDEN-CLAIMS.yaml`; D-04 and `dsx explain`; `.planning/HUMAN-QUEUE.md` | Present |
| 17 | Multi-LLM cost strategy, retrieval-augmented interfaces, role-based access (§5) | Out of scope by design: no language model is on the gate path, and the gate path is standard-library Python only. | D-01 | Not applicable |
| 18 | Datasets that change over time; updating hypotheses dynamically (§7) | Partly present, agent-side: the EDA rerun contract, the population-stability step in the predictive branch, `revisit_when`, and off-gate-path reproduction. No drift computation on the gate path, deliberately. | `skills/dsx-explore-data` steps 5E and 13; `skills/dsx-reproduce`; D-02 | Partial, by design |
| 19 | A conversational, human-guided analysis loop (§7) | Adopted for the project's own development rather than for the gate: every blocking choice reaches a person as a decision block with a recommendation and a default. | `.claude/skills/decision-format`; `.planning/HUMAN-QUEUE.md` | Present, for the ceremony |

## The three ideas taken as positives

1. **Structured handoff between stages.** The paper's metadata notes became, in DSX,
   the contract plus the measured artifacts each role reads. The difference in
   direction matters: the spec is written before the data is seen, so the handoff
   carries commitments, not discoveries.
2. **Every claim traceable to a validated test.** Adopted in reverse. The paper tests,
   then claims; DSX declares the test, then runs it, then permits the claim whose
   verb the design licenses. Same traceability, opposite order, and the order is the
   whole point.
3. **A call to action with a monitoring trigger.** The paper's KPI-anchored
   recommendation with post-deployment tracking became `revisit_when`, a field the
   gate reads, so a recommendation carries the condition that retires it.

## What was refused, and the evidence for refusing it

The paper's pipeline was transcribed in its own stage order as
`examples/known-bad/full-frame-cleaning-entrypoint.py` and its specification declares
an honest training-only preprocessing boundary above it. Measured at `dsx gate
execute` before Phase 11.1: exit 0, no findings. Measured after: `DSX-CODE-020`,
`DSX-CODE-021` and `DSX-CODE-030` at CRITICAL and `DSX-ML-090` at HIGH, recorded in
the corpus harness's target map and re-measured on every test run. The refusals in the
table above are not opinions about the paper; they are the codes that fire against
its own code.

## What was deferred, and how it was promoted (D-13)

Three of the paper's ideas were judged sound and are held on the gated backlog in
`brief.md` §6.5 with an entry condition each. Under D-13 an item without evidence
stays where it is, and under D-14 promoting one without new evidence is itself a
finding. **All three conditions are now met at the Phase-30 terminal re-baseline (2026-09-10)** — each was promoted only after its corpus case was built and measured live, never on an estimate.

| Backlog item | Entry condition | Standing |
|---|---|---|
| Per-feature provenance list (origin, method, fitted-on, motivating result) — item 7 | A corpus case whose target defect is attributable **only** through feature origin: no name pattern matches, no fit call is visible, no declaration contradicts | **Satisfied (Phase 27, 2026-09-07).** `examples/known-bad/feature-origin-only-leak-*` measured a LIVE MISS at all four gate points; `DSX-ML-034` was minted under D-05 (Kaufman 2012 — secondary-corroborated at mint time; read first-hand from the ACM PDF on 2026-09-10, locators Sec. 3.1 p. 15:8 and Sec. 3.2 eq. (3) p. 15:9) to attribute it — declaration-only, so it buys attribution, not a catch |
| Magnitude-without-computed-effect residual — item 8 | A corpus case that passes every claims check while asserting a magnitude no reported test computed | **Satisfied (Phase 28, 2026-09-07).** `examples/known-bad/magnitude-without-computed-effect-*` measured a LIVE MISS — the claimed metric is computed by no `results.tests` entry while `DSX-CLM-033` clears on the collision — and `DSX-CLM-034` was minted under D-05 (Wilkinson & TFSI 1999) to attribute it |
| Subgroup-harm declaration for prescriptive work — item 9 | A primary source with operationalisable criteria (D-05) **and** a corpus case where subgroup harm was the documented failure | **Satisfied (Phase 29, 2026-09-08).** Gail & Simon (1985) supplied the qualitative-interaction definition and Obermeyer et al. 2019 the documented public case; `examples/known-bad/subgroup-harm-without-disposition-*` measured a LIVE MISS pre-mint and `DSX-COH-041` was minted to **catch** it — a real closed catch (PRESENT/DETECTED) firing CRITICAL at plan/verify/ship, the corpus's first `kind: target` |

Each was promoted the honest way — find the case, add it to the corpus (an attributed
miss for items 7 and 8, a detected target for item 9), and let the measured re-baseline
make the argument, recorded in `.planning/phases/30-calibration-rebaseline/30-READOUT.md`.

## How to read this alongside the paper

The paper describes what an autonomous pipeline does. This project describes what has
to be true before that pipeline's output can be believed, and checks it with code that
runs in a gate. The two are not in competition: a pipeline like the paper's, run inside
these gates, would be blocked at exactly the four places the corpus fixture is blocked
and would have to declare its splits, its selection, its family of tests and the verb
its design licenses before its recommendation could ship.
