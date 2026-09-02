# gsd-dsx

**Data science, analytics and BI rigour for GSD Core.**

## Purpose

Specialise the GSD phase loop for analytical work without forking gsd-core.
Agents fill structured contracts; deterministic Python gates block the loop when
the contracts and artifacts do not hold up.

## Core Value

A statistically invalid analysis must fail at the gate, before the data is
touched — not later, in someone else's review.

## Success bar — ten quality dimensions

Every analytical phase that ships under dsx must satisfy these with code where
decidable, and with strong agent guardrails where judgement is required:

1. Analytical Question
2. Analytical Logic
3. Chart Type
4. Missing Evidence
5. Data Quality
6. Code Quality
7. Statistical Issues
8. Plot Construction
9. Visual Design
10. Communication and Data Storytelling

## Determinism doctrine

| Stochastic (agent judgement) | Deterministic (code) |
|---|---|
| Framing the question, choosing the design, writing claims and narrative | Checking the spec is coherent and that produced artifacts satisfy it |

Gates never read live warehouses. They check declarations and hermetic artifacts
(`ANALYSIS-SPEC.yaml`, `DATA-PROFILE.yaml`, evidence files). `dsx profile`
computes profiles from local CSV when available; the gate still only reads the
written profile.

## Current state

- **v1.5.0** shipped: Phases 1–5 complete. Ten quality dimensions gated where
  decidable (DQ, evidence, coherence, viz/seals/smells, narrative/code, analytical
  logic / stats extensions including decision replay and repro_lock, plus scored
  CHART-REVIEW and ADR-authorised suppressions).
- **v2.0.0 DSX Validity Frame — SHIPPED 2026-08-28** (tag `v2.1.0`). All 11 phases
  (6, 7, 8, 9, 10, 11, 11.1, 11.1.1, 11.2, 11.3, 12) complete — 89 plans, 208 tasks.
  Every phase is verified and Nyquist-validated; cross-phase integration INTEGRATED;
  the milestone audit reached `passed` (75/75 requirements accounted, 0 unsatisfied,
  0 orphaned). The full validity-frame surface gates: `validity_frame:` and
  paradigm-aware `inference:` blocks in `ANALYSIS-SPEC.yaml`; the `DSX-VAL-*`
  (estimand, unit triad, dependence, identification, sampling frame, missingness,
  measurement), `DSX-INT-*` (interference/SUTVA, triggered-vs-eligible dilution,
  novelty/primacy), `DSX-PAR-*` (paradigm manifest + symmetric monitoring pair),
  `DSX-PRE-*` (pre-registered inference plan, declared-vs-executed branch
  reconciliation), `DSX-ADM-*` (frequentist procedure admissibility over
  `references/families.yaml`), the prescriptive-claim layer (`DSX-CLM-*`/
  `DSX-COH-040`), and reporting-completeness / missing-data discipline families.
  Phase 12 delivered the calibration corpus with a measured catch rate and
  false-positive rate and `dsx stats --paradigm`. Full detail archived under
  `.planning/milestones/v2.0.0-*`.
- **v2.2 Analytic Surface — SHIPPED 2026-08-29** (tag `v2.2.0`). All 4 phases
  (13, 14, 15, 16) complete — 20 plans. Every phase is verified (`threats_open: 0`)
  and human-signed-off; the milestone audit reached `passed` (23/23 requirements,
  10/10 cross-phase integration seams, Nyquist compliant, 0 unsatisfied/orphaned).
  Delivered: four operator-facing router skills (`dsx-cohort`, `dsx-funnel`,
  `dsx-root-cause`, `dsx-segment`) that point marketing work at existing gates
  instead of restating them; a compounding-learnings search step and a portable
  `DATA-DICTIONARY.md` for onboarding; CUPED as a declared, gated variance
  adjustment (`DSX-EXP-070`, CRITICAL, post-treatment-covariate guard) and a
  changing-denominator BI check (`DSX-MET-021`, HIGH), both under full D-05
  primary-source citation discipline; and off-gate-path re-run verification via
  the new `dsx-reproduce` skill (`DSX-REP-060`/`061`, both HIGH). Package version
  is still 2.0.0 (v2.2 is additive, not a breaking contract change — see Version
  rationale below). The finding catalogue now holds **260 codes**, grown
  additively from 256 with the frozen Phase-12 snapshot unmutated. Full detail
  archived under `.planning/milestones/v2.2-*`.
- **v2.3 Test Catalog — SHIPPED 2026-09-02** (tag `v2.3.0`). All 4 phases
  (17, 18, 19, 20) complete — 11 plans. Every phase is verified (`threats_open: 0`
  across 54 threats, all seven HIGH) and human-signed-off; the milestone audit
  reached `passed` (22/22 requirements, 5/5 cross-phase integration seams,
  Nyquist compliant, 0 unsatisfied/orphaned). Delivered: the `recommend_test`
  decision table grew from ~15 to ~75 rows across 11 categories, backed by 15 new
  declaration-only gate checks (`DSX-STA-050`…`122`) under full D-05 citation
  discipline — every citation independently re-verified against primary sources
  before shipping (27 citations checked, 7 corrected). The finding catalogue now
  holds **275 codes**, grown additively from 260 with both frozen snapshots
  (Phase-12 at 256, v2.2's set) unmutated. Full detail archived under
  `.planning/milestones/v2.3-*`.

## Shipped Milestone: v2.0.0 DSX Validity Frame (shipped 2026-08-28)

**Goal (delivered):** Check the layer beneath every existing DSX check — that the estimand,
unit triad, dependence structure, interference risk, triggering, sampling frame,
missingness mechanism, measurement and declared inferential paradigm are coherent
enough for any DSX finding to mean anything.

**Why now:** The existing families (`DSX-EXP-*`, `DSX-STA-*`, `DSX-MET-*` …) all
assume a sound foundation. Class A failures — the ones recoverable only by
collecting new data — are largely uncovered today. Test choice is recoverable by
reanalysis; a wrong estimand is not.

**Operating context:** marketing data science, roughly 60% online controlled
experiments, under both frequentist and Bayesian paradigms, often on shared
paid-media budgets. The check set is weighted accordingly.

**Target features:**

- `validity_frame:` and paradigm-aware `inference:` blocks in `ANALYSIS-SPEC.yaml`
- Decision record (`5.5` schema) emitted by every step, plus non-blocking `dsx explain`
- `DSX-VAL-*` — estimand, unit triad, dependence, identification strength, sampling
  frame, missingness, measurement
- `DSX-INT-*` — interference/SUTVA, triggering and dilution, novelty and primacy
- `DSX-PAR-*` — paradigm manifest and the symmetric monitoring pair
- `DSX-PRE-*` — pre-registered inference plan, declared branch vs executed branch
- `DSX-ADM-*` — frequentist procedure admissibility over `references/families.yaml`
- Calibration corpus with measured catch rate and false-positive rate

**Version rationale:** v2.0.0 rather than v1.6.0 because `validity_frame:` becomes
required from plan (the `plan` gate point, at CRITICAL severity), so existing
specs without it begin to block — a breaking contract change.

## Shipped Milestone: v2.2 Analytic Surface (shipped 2026-08-29)

**Goal (delivered):** Close the operator-surface gaps that Claude Code data-science packs
cover with playbooks — cohort/funnel/root-cause skills, knowledge compounding,
CUPED as a declared variance adjustment, a CSV-first start, file-first scripts,
and off-gate re-run verification — without turning DSX into a prompt pack and
without computing statistics on the gate path.

**Why after v2.0.0:** Brief §3 ranks risk reduction first. The comparison packs
do not gate shared-budget interference, triggering dilution, or Bayesian
continuous monitoring. Folding their playbooks into Phases 7–12 would delay
that work. Entry condition was Phase 12 closed (`brief.md` §6.5).

**Delivered features:** Phases 13–16, archived at `.planning/milestones/v2.2-ROADMAP.md`.
All 23 requirements (REQ-P13-* … REQ-P16-*) satisfied — archived traceability at
`.planning/milestones/v2.2-REQUIREMENTS.md`. Comparison evidence:
`.planning/research/SURFACE.md`.

**Anti-features held (not built, by design):** Docker as a required runtime; MLflow
or Great Expectations on the gate path; notebooks as the shipped artifact;
Shapiro–Wilk auto-switch; SEM/HLM/IRT; bundled education datasets; a batch
path that skips the plan gate.

**What did not ship as originally worded:** REQ-P15-04 named two defects
(survivorship bias and changing denominator). A direct primary-source read
(not just bibliographic corroboration) found the candidate survivorship-bias
citation (Brown, Goetzmann, Ibbotson & Ross 1992) does not transfer to a
declaration-checkable rule — it is a narrower, fund-performance-persistence
result that never states a general "exclude non-survivors from the
denominator" criterion. Per the requirement's own stated escape clause ("a
code without a citation does not ship and remains in `brief.md` §6.5"), only
the changing-denominator half shipped (`DSX-MET-021`, HIGH); survivorship bias
stays an open, unpromoted item in `brief.md` §6.5. This was a loud, recorded
decision (HUMAN-QUEUE HQ-8/HQ-13), not a silent scope cut.

## Shipped Milestone: v2.3 Test Catalog (shipped 2026-09-02)

**Goal (delivered):** Expand the analyst-facing test-selection surface as close
to exhaustion as stays manageable and citable: the `recommend_test` decision
table grows ~15 → ~75 rows across 11 categories (correlation/association,
agreement/reliability, repeated measures, trend, categorical, resampling,
variance/scale, proportions, counts, post-hoc, power conventions), plus 15 new
declaration-only gate checks and the effect-size band growth — every row cited,
every check under full D-05 discipline.

**Why tests before charts:** both subjects write the same single-writer files
(finding-codes, spec template, shared skills) and D-06 makes range collisions
permanent, so the milestones run strictly sequentially; tests carry the heavier
D-05 read burden (27 citations vs v2.4's expected ~8–12) and began with
mandatory repairs (the Boschloo doc/code divergence; the missing `estimand_kind`
vocabulary), so they went first while the operator queue was fresh.

**Scope boundary held:** the gate did not become a per-test catalog.
`families.yaml` remains the admissibility ontology; what expanded is the
routing surface plus declaration-only checks. See
`.planning/research/V2.3-V2.4-SCOPE.md`.

**Delivered features:** Phases 17–20, archived at
`.planning/milestones/v2.3-ROADMAP.md`. All 22 requirements (REQ-P17-* …
REQ-P20-*) satisfied — archived traceability at
`.planning/milestones/v2.3-REQUIREMENTS.md`.

**The independent citation re-verification that mattered:** before shipping,
an interactive session re-verified all 27 citations against primary sources
(not just the loop's bibliographic corroboration) using parallel research
agents. Seven citations needed correction — the most consequential: a proposed
Krippendorff's-alpha worked-example fixture (0.743, with a claimed 0.734
"textbook typo") did not actually appear anywhere in the cited paper (Hayes &
Krippendorff 2007); the paper's own worked example gives α = 0.7598. Corrected
before the code shipped, not after. The other six were smaller: a kappa
companion-reporting citation reworded to the actual recommended statistics
(p_pos/p_neg, not "p_o and marginals"); a Zimmerman (2004) gate scoped to the
two-group case it actually studied, not generalized to k-group ANOVA; a
McCullagh & Nelder locator upgraded from an unconfirmed guess to a
well-supported specific section; a Lakens (2022) term corrected to his actual
wording; a Wilson (2015) DEPRECATED row stripped of an unsupported
replacement-test claim; a Maxwell & Delaney claim softened pending further
source access.

## Queued Milestone: v2.4 Visual Excellence

**Status:** Queued. Entry condition (D-13): v2.3 shipped.

**Goal:** The exhaustive-but-manageable chart catalog (~80 entries on the FT
Visual Vocabulary spine + Wilke's uncertainty family + rigour staples, three
citable axes per entry), the 5-layer question→chart selection heuristic
(Munzner → FT function → data signature → shortlist → Cleveland-McGill
tie-break), the license-audited publication style layer (dsx-urban default,
dsx-538, dsx-econ/dsx-bbc reimplemented from published doctrine), the SVG
determinism recipe, and a portfolio exemplar capstone that exercises both
milestones end-to-end. Phases 21–24; requirements REQ-P21-* … REQ-P24-* queued
in `.planning/REQUIREMENTS.md`. Pre-agreed contingency: split style/exemplar
off as v2.5 if v2.3's D-05 queue outruns the ceremony cadence.

**v3.0 (models) remains future scope** — nothing here touches it.

## Requirements

### Validated

- ✓ DQ assertions vs `DATA-PROFILE.yaml`, evidence resolution, question↔claim↔decision coherence — v1.1.0
- ✓ Chart-type matrix, figure seals, viz smells, takeaway heuristics, Gate A–D verifier protocol — v1.2.0
- ✓ Narrative discipline, forbidden-claim SSOT, SQL anti-patterns, entrypoint smell scan — v1.3.0
- ✓ Assumption checkoffs/waivers, TOST/CI/MDE, multiplicity family, repro_lock, decision replay — v1.4.0
- ✓ ANALYSIS-SPEC `suppressions[]` with authority, scored CHART-REVIEW.md — v1.5.0
- ✓ `validity_frame:`/`inference:` contract blocks, decision records + `dsx explain`, `DSX-PAR-001` paradigm manifest, `dsx/frame/` package with enforced D-03a boundary, mechanical D-05 citation enforcement, known-bad corpus — Phase 6 (REQ-P6-01 … REQ-P6-16)
- ✓ Symmetric monitoring pair `DSX-PAR-010`/`DSX-PAR-011` plus membership-free `DSX-PAR-002` (requiredness; `DSX-SPEC-085` owns vocabulary membership) — Phase 9 (REQ-P9-01 … REQ-P9-07)
- ✓ Interference adjudication `DSX-INT-010`/`-011` (unaddressed risk; channel-inadmissible mitigation, disjoint on the mitigation dimension alone), triggered-versus-eligible dilution `DSX-INT-030` (additive metrics only, ratio metrics explicitly out of scope), novelty/primacy `DSX-INT-040`, and the no-paradigm-read invariant — Phase 8 (REQ-P8-01 … REQ-P8-06)
- ✓ Validity-frame checks `DSX-VAL-*` — estimand completeness/falsifiability, unit triad, dependence method family, identification strength, sampling frame, missingness, measurement — Phase 7 (REQ-P7-01 … REQ-P7-09; REQ-P7-08 satisfied within its declared D-06 scope) — v2.0.0
- ✓ Pre-registered inference plan `DSX-PRE-*` — fallback-rule DSL, `declared_at` provenance, declared-vs-executed branch reconciliation blocking on branch identity alone — Phase 10 (REQ-P10-01 … REQ-P10-04) — v2.0.0
- ✓ Frequentist admissibility adjudicator `DSX-ADM-*` over `references/families.yaml` (14 cited families) — ranked admissible set, `no_admissible_procedure` escalation — Phase 11 (REQ-P11-01 … REQ-P11-06) — v2.0.0
- ✓ Generated-pipeline reality — widened entrypoint fit-scan, cleaning-stage fit boundary, score/selection provenance, imbalance disclosure — Phase 11.1 — v2.0.0
- ✓ Detection-code hardening — `ast.parse` primary path with text-scan fallback, closing false negatives and two false positives — Phase 11.1.1 — v2.0.0
- ✓ Prescriptive claim layer — `prescriptive` claim type + coherence ladder, causal-verb lexicon tiers, `decision.revisit_when` (`DSX-COH-040`), amendment counting on the locked plan, self-reported-fields view — Phase 11.2 (REQ-P11.2-01 … -07) — v2.0.0
- ✓ Reporting completeness and missing-data discipline — multiplicity over reported tests, examined-vs-reported gap, missingness method vocabulary + single-imputation denial, exclusion rules under the plan-time lock — Phase 11.3 (REQ-P11.3-01 … -07) — v2.0.0
- ✓ Calibration — full known-bad corpus with measured catch rate and false-positive rate, `dsx stats --paradigm`, gated-backlog re-evaluation — Phase 12 (REQ-P12-01 … REQ-P12-05) — v2.0.0
- ✓ Four router skills (`dsx-cohort`, `dsx-funnel`, `dsx-root-cause`, `dsx-segment`) filling `ANALYSIS-SPEC.yaml` fields against existing gates, a hypothesis register, What/So What/Now What narrative shape, advisory-only tier routing, and a `scripts/*.py` entrypoint preference — Phase 13 (REQ-P13-01 … REQ-P13-06) — v2.2
- ✓ Compounding-learnings search, `DATA-DICTIONARY.md` onboarding artifact, opt-in research-domain AI-assistance disclosure, CSV-first slash aliases, and a documented file-drop-hook skip — Phase 14 (REQ-P14-01 … REQ-P14-06) — v2.2
- ✓ CUPED as a closed-vocabulary variance adjustment with a post-treatment-covariate gate check (`DSX-EXP-070`), a changing-denominator BI check (`DSX-MET-021`), an optional APA research table, and a Shapiro–Wilk auto-switch prohibition — Phase 15 (REQ-P15-01 … REQ-P15-07; REQ-P15-04 satisfied as-worded via its own escape clause — see Shipped Milestone note below) — v2.2
- ✓ Off-gate-path reproduce verification (`dsx-reproduce` skill, `DSX-REP-060`/`061`), corpus `protocol_adherence` tagging, and a static no-entrypoint-execution guard — Phase 16 (REQ-P16-01 … REQ-P16-04) — v2.2
- ✓ Boschloo doc/code reconciliation, `estimand_kind` closed vocabulary (6 members), D-12a disposition table, and D-06 range pre-allocation — Phase 17 (REQ-P17-01 … REQ-P17-05) — v2.3
- ✓ Correlation/association routing (`recommend_association`) and agreement/reliability gates — scale/kind mismatch (`DSX-STA-050/051`), ICC/kappa declaration completeness (`DSX-STA-060/061/062`) — plus report-only effect-size conventions in `dsx/mathx.py` — Phase 18 (REQ-P18-01 … REQ-P18-06) — v2.3
- ✓ Repeated-measures/trend/categorical/resampling/post-hoc routing and ten declaration-only gates (`DSX-STA-070` … `122`) — unconditional Greenhouse-Geisser, declared dose scores/autocorrelation, resampling quadruples, post-hoc/omnibus matching, variance-test-as-precondition ban, observed-power ban, Wilson-not-Wald, declared exposure offsets — Phase 19 (REQ-P19-01 … REQ-P19-07; REQ-P19-03 verified zero-mint) — v2.3
- ✓ Calibration close — known-bad fixtures + FPR negative controls for the 15 new codes, a live HIGH verify/ship calibration stratum, category-complete no-autoswitch coverage, and a permanent doc/code agreement cross-check — Phase 20 (REQ-P20-01 … REQ-P20-04; zero-mint verified, catalogue stays 275) — v2.3

### Active

(None — all v2.0.0, v2.2, and v2.3 requirements shipped and validated. Full
requirement sets with final traceability are archived at
`.planning/milestones/v2.0.0-REQUIREMENTS.md`, `v2.2-REQUIREMENTS.md`, and
`v2.3-REQUIREMENTS.md`.) v2.4 Visual Excellence is queued (REQ-P21-* …
REQ-P24-* in `.planning/REQUIREMENTS.md` under **Queued**) and becomes Active
when started.

### Out of Scope

- Computing test statistics or posteriors inside the gate path — breaks D-01/D-02
- Bayesian procedure recommendation and admissibility — gated backlog, entry condition in brief §6.5
- Prior justification, prior sensitivity, convergence declarations — deferred under D-12a; their frequentist mirrors are not written
- Causal identification *strategy* checking — `DSX-CAU-*` owns this
- Survival, time-series and spatial estimation *methods* — temporal/spatial dependence are declared types; the methods are out
- Reading a data warehouse from a gate — breaks the determinism doctrine
- A catalogue of every named statistical test as a computing GATE — `families.yaml`
  stays the admissibility ontology (families, not tests), and no gate computes a
  statistic. v2.3 expanded the *routing surface* instead (`recommend_test` ~15→~75
  rows, one primary answer per declarable key) plus 15 declaration-only defect
  checks — a bounded, citable decision table, not "every named test" (Kanji
  enumerates ~100, Sheskin ~200; see `.planning/research/V2.3-V2.4-SCOPE.md` §1).
- The Unified Framework playbook's `r>0.3` heuristic as a CUPED admissibility rule — not admissible under D-05 (`SURFACE.md` §8); Phase 15 cites the WSDM primary source directly instead.
- Ratio-metric dilution (Deng & Hu 2015, Formula (3)) as a "changing-denominator" check — permanently out of scope for the declaration-only gate (no closed-form scalar, D-01/D-02); Phase 15's `DSX-MET-021` is scoped to a different defect (Simpson's-paradox-style allocation-rate shifts, Crook et al. 2009) and must not be confused with it.

## Context

- Seed brief: `brief.md` (committed at milestone start). Sections 4 (decisions),
  5 (contract), 6 (milestones), 6.5 (gated backlog) and 7 (citations) are binding
  inputs to planning and must not be re-litigated in discuss.
- Existing integration surface verified at v1.5.0:
  - Gate profiles are check-module tuples in `dsx/cli.py` (`GATE_PROFILES`), with
    thresholds CRITICAL at plan/execute and HIGH at verify/ship. New families must
    be registered there.
  - `DSX-EXP-060` already fires on undeclared interim looks under a fixed horizon.
  - `DSX-EXP-020/021` already reconciles `randomization_unit` vs `analysis_unit`.
  - `PEEKING_POLICIES` in `dsx/spec.py` already covers the stopping-rule concept.
  - `VARIANCE_ADJUSTMENTS` overlaps `dependence.method_family_required`. As of
    v2.2, the set is `{cluster_robust, delta_method, bootstrap_cluster,
    mixed_effects, cuped}` — CUPED landed in Phase 15 (REQ-P15-01).
  - `dsx explain` and `dsx stats` shipped in v2.0.0; `dsx-reproduce` (skill, not
    a subcommand) shipped in v2.2 Phase 16, re-running `reproducibility.entrypoint`
    off the gate path and writing `REPRO-REPORT.md`.
  - `dsx/frame/` package and `references/families.yaml` shipped in v2.0.0 (M2a/M4).
  - Analytic-surface comparison against five Claude Code packs: `.planning/research/SURFACE.md`
    (2026-08-26). That file does not authorise finding codes.
  - The capability now registers 14 skills (v2.2 added `dsx-cohort`, `dsx-funnel`,
    `dsx-root-cause`, `dsx-segment`, `dsx-reproduce`); the finding catalogue holds
    260 codes (v2.0.0 shipped 256; Phase 15 added `DSX-EXP-070`/`DSX-MET-021`,
    Phase 16 added `DSX-REP-060`/`061`).

## Constraints

- **Tech stack**: Python 3.9+, stdlib only on the gate path — D-01. A gate that breaks on a missing dependency is a gate that gets turned off.
- **Dependencies**: GSD Core >= 1.6. Extends the existing DSX package — no fork, no second installer, no patched upstream workflows.
- **Compatibility**: Exit codes remain the contract — `0` pass, `1` block, `2` could not run.
- **Compatibility**: Finding codes are never renumbered — D-06. A suppression written today stays valid.
- **Evidence**: No check ships without a primary-source citation in its docstring and a test against a published reference value — D-05. If velocity pressure arrives, cut checks, never this.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| D-03 Extend DSX in place, one install/contract/gate/test suite/catalogue | Highest-value checks are cross-cutting; a check spanning two contracts cannot live cleanly in either of two plugins | Delivered v2.0.0 — all `DSX-VAL/INT/PAR/PRE/ADM/CLM/COH` families ship in the one package, contract, gate profile set and catalogue (256 codes) |
| D-03a Keep an extractable boundary: `dsx/frame/` imports only `Report`/`Finding` from `dsx/checks/` | If in six months there are no upward imports, extraction is a `git filter-repo` | Delivered Phase 6 — `dsx/frame/` exists; `tests/test_frame_boundary.py` fails the suite on any upward import |
| D-04 Never block to teach — gates emit a decision record, `dsx explain` renders it | A gate that stops to explain is disabled on a deadline, losing guardrail and lesson both | Delivered Phase 6 — `dsx/decisions.py` emits, `dsx explain` renders, always exit 0; the gate-path write is a guarded side channel |
| D-05 Citation + published reference value per check | Prevents laundering model statistics knowledge into a blocking gate | Delivered Phase 6 — `check_d05` in `gen-finding-catalogue.py --check` fails the build on a missing `Citation:` line |
| D-10 An unsupported paradigm is never blocking on its own | Blocking on `paradigm: bayesian` makes typing `frequentist` the cheapest way past the gate | Delivered Phase 6 — `DSX-PAR-001` is INFO (10); every default `GATE_THRESHOLDS` value is 40 or 50 |
| D-11 Frame-layer checks never read `paradigm` | A prior does not save you from pseudo-replication; if a frame check branches on paradigm it is in the wrong layer | Delivered Phase 7 — AST-enforced import boundary; `applies_to_frequentist_admissibility` is the one predicate allowed to read declared paradigm, tested |
| D-12/D-12a Paradigm-specific checks ship in symmetric pairs, and symmetry is the scoping rule | Asymmetric enforcement is how a tool silently steers method choice | Delivered Phase 9 for the monitoring pair (`DSX-PAR-010`/`-011` at identical CRITICAL; `is_blank_text` as the single clearing predicate; committed symmetry audit). D-12a deferred codes (`DSX-PAR-020`/`-021`/`-030`) remain out of scope |
| D-13 Deferred checks carry an entry condition, not a wish | A trigger tied to a measured catch rate is falsifiable; a priority is not | Delivered Phase 12 — the §6.5 gated backlog was re-evaluated against the measured catch rate/FPR (carry 8, remove 1 as structurally unevaluable) |
| D-14 Reversing a D-table decision requires a reversal record; evidence-free reversal logs as `SELF-001` | "Here is what would change my mind" is stronger than "here is what I chose" | Delivered Phase 6 (template) + exercised — `REVERSALS.md` carries REV-001 and REV-002 (Phase 12 §6.5 relocate-not-delete) with all four template fields |
| **M-01** `DSX-PAR-010` ships as a distinct code, `DSX-EXP-060` untouched | Triggers are disjoint — undeclared looks under a fixed horizon vs a declared continuous design with no sequential method. Widening EXP-060 would silently broaden existing suppressions, against the spirit of D-06 | Delivered Phase 9 — pair ships in `dsx/frame/paradigm.py`; `dsx/checks/design.py` untouched |
| **M-02** No `inference.stopping_rule` field; `DSX-PAR-010/011` read the existing `design.peeking_policy` | One concept, one field. Avoids a permanent consistency check between two vocabularies for the same thing. Deviates from brief §5.2, which specified a new field | Delivered Phase 9 — both codes trigger on `peeking_policy: uncontrolled_continuous` |
| **Phase 9 D-08** `DSX-PAR-002` is presence/requiredness only; `DSX-SPEC-085` owns closed-vocabulary membership | Two codes for one defect would violate one-stable-fact-per-code. UAT 2026-08-13 accepted the split; ROADMAP SC 4 / REQ-P9-04 amended to name both codes | Delivered Phase 9 |
| **M-03** `PEEKING_POLICIES` gains a value for uncontrolled continuous monitoring | Consequence of M-02: the existing vocabulary has `always_valid` (disciplined) but no value for "peeking continuously with no correction" — precisely what `DSX-PAR-010` must fire on | Delivered Phase 6 — `uncontrolled_continuous` added (`dsx/spec.py:71`) |
| **M-04** Automated import test enforces the D-03a boundary from M1 | Enforces the boundary without scaffolding an empty `families.yaml`, which brief §6.6 warns accumulates speculative structure | Delivered Phase 6 — AST scanner proven against three deliberately violating sources |
| **M-05** `SELF-001` stays a convention for v2.0.0; `REVERSALS.md` template seeded in M1 | Enforcement is a planning-process concern, not a gate concern; a subcommand adjudicating planning docs is outside the gate path | Delivered Phase 6 — `REVERSALS.md` seeded with the four-field D-14 template; SELF-001 trigger stated. Human-validated (UAT 1) |
| **M-06** `validity_frame` sub-block requiredness is gated by `question_type` from M1 | Requiring the whole block for descriptive/BI work forces reflexive `none` answers — the exact incentive distortion D-10 exists to prevent. Far cheaper decided in M1 than retrofitted after M2a/M2b are written against the wrong requiredness | Delivered Phase 6 — REQ-P6-03 |
| **M-07** Existing `suppressions[]` with its authority requirement is the grandfather path for pre-v2.0.0 specs | Zero new code, and the ADR/SPEC authority requirement makes grandfathering deliberate and attributable rather than silent | Delivered Phase 6 — README states authority as a requirement (DSX-SPEC-070) and the "a frame that lies passes" known limit. Human-validated (UAT 2) |
| **M-08** D-05 citation enforcement is automated in M1 via `scripts/gen-finding-catalogue.py` | D-05 says "if velocity pressure arrives, cut checks, never this" — an unenforced constraint is the first thing velocity pressure removes. It was the only major constraint nothing checked | Delivered Phase 6 — see D-05 |
| **M-09** `dependence.method_family_required` reuses `VARIANCE_ADJUSTMENTS` | Same reasoning as M-02: one concept, one vocabulary. Consequence: the field holds a single member, so the brief's example `cluster_robust_or_mixed` is not expressible — carried as an open item for the M2a discuss rather than silently modelled as a disjunction | Delivered Phase 7 — the dependence check reads the reused vocabulary; resolved in M2a discuss |
| **v2.2-01** REQ-P15-04's survivorship-bias half ships unminted; only the changing-denominator half (`DSX-MET-021`) ships | A direct primary-source read of the candidate citation (Brown, Goetzmann, Ibbotson & Ross 1992) found it does not transfer to a declaration-checkable "denominator must exclude non-survivors" rule — it is a narrower, fund-performance-persistence-specific result. D-05 and brief §6.5: an honest non-promotion beats a stretched citation | Delivered Phase 15 — `DSX-MET-021` (HIGH) ships citing Crook, Frasca, Kohavi & Longbotham (2009) §6; survivorship bias stays an open item in `brief.md` §6.5. Decided via direct-read (not corroboration-only), recorded HUMAN-QUEUE HQ-8/HQ-13 |
| **v2.2-02** `DSX-REP-060`/`DSX-REP-061` mint in Phase 16, not Phase 15 | Keeps the `dsx-reproduce` skill and its enforcing gate check in one phase (no window where the skill exists but nothing enforces it). Phase 15's codes all carry D-05 statistical citations; these are engineering-hygiene checks (report missing / numbers don't overlap) with none — mixing the two would blur the citation discipline | Delivered Phase 16 — both HIGH, in `dsx/checks/repro.py`; catalogue moved 256→258 here, then 258→260 in Phase 15. Decided by Architect+Auditor persona round, unanimous, recorded HUMAN-QUEUE HQ-11 |
| **v2.3-01** Citation granularity: one human D-05 read per new gate CODE, one bibliographic citation per catalog ENTRY | A ~75-row decision table with a human read per row would put ~90 reads in front of one milestone, stalling the ceremony's one human-gated step; reads are only load-bearing for the codes that actually gate | Delivered Phases 18–19 — 15 new gate codes drew ~27 human reads (2 evidence packs, HQ-16/17), not 75+; row-level catalog citations confirmed at execute-time bibliography passes instead |
| **v2.3-02** All 15 new gate checks are declaration-only, keyed on DECLARED fields, never on inspecting data then choosing | The anti-two-stage doctrine (already shipped for Shapiro–Wilk) extends structurally: a routing key that reads "skew observed → pick test" recreates the exact banned pattern under a new name | Delivered Phases 18–19 — `inspect.signature` structural proofs + the no-autoswitch test suite extended to every new category; two new NEGATIVE gates (variance-test-as-precondition ban, observed-power ban) enforce the doctrine rather than merely avoiding violating it |
| **v2.3-03** Independent re-verification of all 27 D-05 citations against primary sources before shipping, not after | The Krippendorff-alpha citation (HQ-16 B4) would have shipped a fixture value (0.743) that appears nowhere in its cited paper — caught only by reading the actual paper, exactly the CUPED-author-misattribution failure mode from v2.2's HQ-8 | Delivered at S5-2 close-out — 7 of 27 citations corrected (1 wrong fixture value, 6 smaller wording/scope/locator fixes); corrections recorded in `HUMAN-QUEUE.md` HQ-16/17 before the codes' citations were considered in hand |

## Non-goals

- Patching gsd-core workflows
- Third-party Python deps inside the gate process
- Reading production databases from `dsx gate`

## Known limits

The gate checks declarations against declarations. **A frame that lies passes.**
The insurance against a bad question is still a human who knows the domain reading
the frame before the data is touched. What this changes is that the review becomes
cheap, structured and repeatable, so it actually happens. To be stated in the README.

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-09-02 — v2.3 Test Catalog milestone complete and shipped
(tag `v2.3.0`). v2.4 Visual Excellence is queued next.*
