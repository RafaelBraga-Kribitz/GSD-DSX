# Roadmap: gsd-dsx

**Active:** v2.6 Exploration Depth and Backlog Evidence — Phases 25–30 (opened 2026-09-06)
**Shipped:** v2.4 Visual Excellence — Phases 21–24 (2026-09-03); v2.3 Test Catalog — Phases 17–20 (2026-09-02); v2.2 Analytic Surface — Phases 13–16 (2026-08-29); v2.0.0 DSX Validity Frame — Phases 6–12 (2026-08-28); v1.1.0–v1.5.0 — Phases 1–5

> **Milestone name vs. release tag.** The DSX Validity Frame is named **v2.0.0**
> throughout planning (its archives are `v2.0.0-ROADMAP.md`, `v2.0.0-REQUIREMENTS.md`,
> `v2.0.0-MILESTONE-AUDIT.md`), but it ships under the git tag **`v2.1.0`**. The
> `v2.0.0` tag was already published on origin (2026-08-10) against an earlier,
> partial merge of this same branch, and moving a published ref would silently break
> anyone who had already fetched it — so the completed milestone got the next free
> tag instead. The follow-on **Analytic Surface** milestone was correspondingly
> renamed from v2.1 to **v2.2** so it does not collide with that release tag. Its
> milestone name and release tag match: **v2.2.0**.

## Milestones

- ✅ **v1.1.0–v1.5.0** — Phases 1–5 (shipped incrementally; ten quality dimensions gated where decidable)
- ✅ **v2.0.0 DSX Validity Frame** — Phases 6–12 (shipped 2026-08-28, tag `v2.1.0`)
- ✅ **v2.2 Analytic Surface** — Phases 13–16 (shipped 2026-08-29, tag `v2.2.0`)
- ✅ **v2.3 Test Catalog** — Phases 17–20 (shipped 2026-09-02, tag `v2.3.0`)
- ✅ **v2.4 Visual Excellence** — Phases 21–24 (shipped 2026-09-03, tag `v2.4.0`)
- 🔄 **v2.6 Exploration Depth and Backlog Evidence** — Phases 25–30 (opened 2026-09-06; ships as tag `v2.6.0`)

## Phases

<details>
<summary>✅ v1.1.0–v1.5.0 (Phases 1–5) — SHIPPED</summary>

- [x] Phase 1: DQ + Evidence + Coherence (v1.1.0)
- [x] Phase 2: Viz proof + plot construction (v1.2.0)
- [x] Phase 3: Storytelling + code reality (v1.3.0)
- [x] Phase 4: Analytical logic depth + stats extensions (v1.4.0)
- [x] Phase 5: Chart review + suppressions (v1.5.0)

</details>

<details>
<summary>✅ v2.0.0 DSX Validity Frame (Phases 6–12) — SHIPPED 2026-08-28</summary>

Phase detail (plan counts, completion dates) is recorded above.
`.planning/milestones/v2.0.0-ROADMAP.md` is the milestone's pre-execution scoping
snapshot, not a post-completion archive.

- [x] Phase 6: Contract extension, decision record, paradigm manifest (M1) — 13/13 plans — completed 2026-08-10
- [x] Phase 7: Validity frame checks (`DSX-VAL-*`) (M2a) — 8/8 plans — completed 2026-08-20
- [x] Phase 8: Interference, triggering, stability (`DSX-INT-*`) (M2b) — 10/10 plans — completed 2026-08-14
- [x] Phase 9: Monitoring discipline, symmetric (`DSX-PAR-*`) (M2c) — 7/7 plans — completed 2026-08-13
- [x] Phase 10: Pre-registered inference plan (`DSX-PRE-*`) (M3) — 6/6 plans — completed 2026-08-20
- [x] Phase 11: Frequentist admissibility adjudicator (`DSX-ADM-*`) (M4) — 8/8 plans — completed 2026-08-28
- [x] Phase 11.1: Generated-pipeline reality (INSERTED) — 8/8 plans — completed 2026-08-21
- [x] Phase 11.1.1: Detection-code hardening (INSERTED) — 7/7 plans — completed 2026-08-22
- [x] Phase 11.2: Prescriptive claim layer (INSERTED) — 8/8 plans — completed 2026-08-26
- [x] Phase 11.3: Reporting completeness and missing-data discipline (INSERTED) — 7/7 plans — completed 2026-08-27
- [x] Phase 12: Calibration (M5, terminal) — 7/7 plans — completed 2026-08-27

</details>

<details>
<summary>✅ v2.2 Analytic Surface (Phases 13–16) — SHIPPED 2026-08-29</summary>

Phase detail (plan counts, completion dates) is recorded above.
`.planning/milestones/v2.2-ROADMAP.md` is the milestone's pre-execution scoping
snapshot (not a post-completion archive); `.planning/milestones/v2.2-phases/` holds
the individual phase plans. Milestone audit `passed`
(`.planning/milestones/v2.2-MILESTONE-AUDIT.md`): 23/23 requirements, 4/4
phases verified, 10/10 cross-phase integration seams, Nyquist compliant, 0
unsatisfied/orphaned. Finding catalogue grew 256 → 260 (additive; the frozen
Phase-12 snapshot at 256 was never mutated).

- [x] Phase 13: Task playbooks that fill the spec (skill-only) — 5/5 plans — completed 2026-08-28
- [x] Phase 14: Compounding and data onboarding — 5/5 plans — completed 2026-08-28
- [x] Phase 15: CUPED and BI declaration checks (`DSX-EXP-070`, `DSX-MET-021`) — 6/6 plans — completed 2026-08-29
- [x] Phase 16: Re-run verification off the gate path (`DSX-REP-060`, `DSX-REP-061`) — 4/4 plans — completed 2026-08-29

</details>

<details>
<summary>✅ v2.3 Test Catalog (Phases 17–20) — SHIPPED 2026-09-02</summary>

Phase detail (plan counts, completion dates) is recorded above.
`.planning/milestones/v2.3-ROADMAP.md` is the milestone's pre-execution scoping
snapshot (not a post-completion archive); `.planning/milestones/v2.3-phases/` holds
the individual phase plans. Milestone audit `passed`
(`.planning/milestones/v2.3-MILESTONE-AUDIT.md`): 22/22 requirements, 4/4
phases verified, 5/5 cross-phase integration seams, Nyquist compliant, 0
unsatisfied/orphaned. Finding catalogue grew 260 → 275 (additive; both frozen
snapshots — Phase-12 at 256, v2.2's set — never mutated). 27 D-05 citations
independently re-verified against primary sources at close-out; 7 corrected.

- [x] Phase 17: Foundation — repairs and spec vocabulary — 3/3 plans — completed 2026-09-01
- [x] Phase 18: Correlation, association and agreement (`DSX-STA-050`…`062`) — 2/2 plans — completed 2026-09-02
- [x] Phase 19: RM, trend, categorical, resampling, post-hoc (`DSX-STA-070`…`122`) — 2/2 plans — completed 2026-09-02
- [x] Phase 20: Calibration and reporting close — 4/4 plans — completed 2026-09-02

</details>

<details>
<summary>✅ v2.4 Visual Excellence (Phases 21–24) — SHIPPED 2026-09-03</summary>

Phase detail (plan counts, completion dates) is recorded above.
`.planning/milestones/v2.4-ROADMAP.md` is the milestone's pre-execution scoping
snapshot (not a post-completion archive); `.planning/milestones/v2.4-phases/` holds
the individual phase plans. Milestone audit `passed`
(`.planning/milestones/v2.4-MILESTONE-AUDIT.md`): 16/16 requirements, 4/4
phases verified, 5/5 cross-phase integration seams, Nyquist compliant, 0
unsatisfied/orphaned. Finding catalogue grew 275 → 276 (additive; all three
frozen snapshots — Phase-12 at 256, v2.2's, v2.3's — never mutated). 13 D-05
citations independently re-verified against primary sources at close-out; 7
corrected, including a perceptual-ranking claim unsupported by either cited
paper. A separate license-audit round caught a mislabeled style palette
(claimed Apache-2.0/Urban Institute; actually GPL-3.0-disputed with 3 of 6
colors being unattributed ColorBrewer stops) before ship.

- [x] Phase 21: Viz vocabulary reconciliation — 1/1 plan — completed 2026-09-03
- [x] Phase 22: Catalog spine, uncertainty family, selection heuristic — 4/4 plans — completed 2026-09-03
- [x] Phase 23: Style and snippet layer — 3/3 plans — completed 2026-09-03
- [x] Phase 24: Portfolio exemplar and viz calibration — 3/3 plans — completed 2026-09-03

</details>

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. DQ + Evidence + Coherence | v1.1.0 | — | Complete | v1.1.0 |
| 2. Viz proof + plot construction | v1.2.0 | — | Complete | v1.2.0 |
| 3. Storytelling + code reality | v1.3.0 | — | Complete | v1.3.0 |
| 4. Analytical logic depth + stats extensions | v1.4.0 | — | Complete | v1.4.0 |
| 5. Chart review + suppressions | v1.5.0 | — | Complete | v1.5.0 |
| 6. Contract extension, decision record, paradigm manifest | v2.0.0 | 13/13 | Complete | 2026-08-10 |
| 7. Validity frame checks (`DSX-VAL-*`) | v2.0.0 | 8/8 | Complete | 2026-08-20 |
| 8. Interference, triggering, stability (`DSX-INT-*`) | v2.0.0 | 10/10 | Complete | 2026-08-14 |
| 9. Monitoring discipline, symmetric (`DSX-PAR-*`) | v2.0.0 | 7/7 | Complete | 2026-08-13 |
| 10. Pre-registered inference plan (`DSX-PRE-*`) | v2.0.0 | 6/6 | Complete | 2026-08-20 |
| 11. Frequentist admissibility adjudicator (`DSX-ADM-*`) | v2.0.0 | 8/8 | Complete | 2026-08-28 |
| 11.1 Generated-pipeline reality | v2.0.0 | 8/8 | Complete | 2026-08-21 |
| 11.1.1 Detection-code hardening | v2.0.0 | 7/7 | Complete | 2026-08-22 |
| 11.2 Prescriptive claim layer | v2.0.0 | 8/8 | Complete | 2026-08-26 |
| 11.3 Reporting completeness | v2.0.0 | 7/7 | Complete | 2026-08-27 |
| 12. Calibration | v2.0.0 | 7/7 | Complete | 2026-08-27 |
| 13. Task playbooks that fill the spec | v2.2 | 5/5 | Complete | 2026-08-28 |
| 14. Compounding and data onboarding | v2.2 | 5/5 | Complete | 2026-08-28 |
| 15. CUPED and BI declaration checks | v2.2 | 6/6 | Complete | 2026-08-29 |
| 16. Re-run verification (off the gate path) | v2.2 | 4/4 | Complete | 2026-08-29 |
| 17. Foundation — repairs and spec vocabulary | v2.3 | 3/3 | Complete | 2026-09-01 |
| 18. Correlation, association and agreement | v2.3 | 2/2 | Complete | 2026-09-02 |
| 19. RM, trend, categorical, resampling, post-hoc | v2.3 | 2/2 | Complete | 2026-09-02 |
| 20. Calibration and reporting close | v2.3 | 4/4 | Complete | 2026-09-02 |
| 21. Viz vocabulary reconciliation | v2.4 | 1/1 | Complete | 2026-09-03 |
| 22. Catalog spine, uncertainty family, selection heuristic | v2.4 | 4/4 | Complete | 2026-09-03 |
| 23. Style and snippet layer | v2.4 | 3/3 | Complete | 2026-09-03 |
| 24. Portfolio exemplar and viz calibration | v2.4 | 3/3 | Complete | 2026-09-03 |

**v2.0.0 totals:** 11 phases, 89 plans, 208 tasks. Milestone audit `passed` (`.planning/milestones/v2.0.0-MILESTONE-AUDIT.md`); all 11 phases verified and Nyquist-validated; cross-phase integration INTEGRATED.

**v2.2 totals:** 4 phases, 20 plans. Milestone audit `passed` (`.planning/milestones/v2.2-MILESTONE-AUDIT.md`); all 4 phases verified and Nyquist-validated; cross-phase integration INTEGRATED (10/10 seams).

**v2.3 totals:** 4 phases, 11 plans. Milestone audit `passed` (`.planning/milestones/v2.3-MILESTONE-AUDIT.md`); all 4 phases verified and Nyquist-validated; cross-phase integration INTEGRATED (5/5 seams).

**v2.4 totals:** 4 phases, 11 plans. Milestone audit `passed` (`.planning/milestones/v2.4-MILESTONE-AUDIT.md`); all 4 phases verified and Nyquist-validated; cross-phase integration INTEGRATED (5/5 seams).

## Active milestone — v2.6 Exploration Depth and Backlog Evidence (Phases 25–30) — ACTIVE since 2026-09-06

**Status:** Active — opened 2026-09-06 by operator direction (HUMAN-QUEUE HQ-39);
driven by the autonomous ceremony on branch `gsd/v2.6.0-exploration-depth`. Ships
as tag `v2.6.0`. Requirements REQ-P25-01 … REQ-P30-03 in `.planning/REQUIREMENTS.md`.
Full scope in `.planning/research/V2.6-SCOPE.md` (2026-09-06), written against the
live tree at `d2f0140` — this milestone does not need a fresh scoping round; S0-2
re-verifies the scope before any planning.

**Scope boundary (do not re-litigate):** the profiler is a producer, never a gate
(D-01/D-02) — no gate reads a new profile key, the assertion vocabulary stays
frozen, Phases 25/26/30 mint zero codes. Phases 27–29 each build and MEASURE a
corpus case before any check is designed; a case the gate already catches closes
its phase with no mint (D-13). Every minted code carries D-05 with a human-read
citation. Pre-agreed contingency: split Phases 28–30 off as v2.7 if the D-05 queue
outruns the cadence.

- [ ] **Phase 25: Hermetic profile depth** - `dsx profile` produces the explore protocol's step 1–4 numbers, hash-bound and byte-stable
- [ ] **Phase 26: Per-skill read contracts** - five downstream skills read `EDA.md` front-matter and the profile
- [ ] **Phase 27: Evidence case — feature-origin-only leak** - §6.5 item 7 measured; provenance declaration if a live miss
- [ ] **Phase 28: Evidence case — magnitude no test computed** - §6.5 item 8 measured; claim-to-test overlap if a live miss
- [ ] **Phase 29: Evidence case — subgroup harm under a prescriptive recommendation** - §6.5 item 9 measured; disposition declaration if a live miss and source confirmed
- [ ] **Phase 30: Calibration re-baseline** - headline pair and strata re-measured with the new cases classified

### Phase 25: Hermetic profile depth

**Goal**: `dsx profile` computes, stdlib-only and hash-bound, the trust-core
numbers the explore protocol's steps 1a/3a/4a/4b/4e/4f currently ask the agent to
compute — five-number summaries, zeros and negatives, categorical shares, daily
volume and edge-period ratios, rows per unit, weekly base rate — additively and
with every existing key byte-stable, so `EDA.md` copies them and two runs carry
identical numbers by construction.
**Depends on**: Nothing (first phase)
**Requirements**: REQ-P25-01, REQ-P25-02, REQ-P25-03
**Success Criteria** (what must be TRUE):

  1. Running `dsx profile` on the committed example extracts regenerates every pre-existing key and value byte-identically and adds the new keys.
  2. Every new statistic has a declared, cited definition (the quantile type named by its Hyndman & Fan 1996 number, verified at plan) and a reference-value test on a hand-computed fixture.
  3. `dsx/checks/dq.py`, the assertion vocabulary and the gate profiles are byte-unchanged; catalogue 276 → 276.
  4. The explore skill, template and reference say "copied from the profile" where the profiler now supplies the number; `node install.mjs --check` passes.

**Plans**: 4 plans
**Wave 1**

- [ ] 25-01-PLAN.md — numeric & categorical column blocks (D-01/D-02), determinism + pre-existing-key golden (wave 1)

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 25-02-PLAN.md — time block (hour retention, rows_per_day, ISO-week edge ratios) + unit block (wave 2)

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 25-03-PLAN.md — target weekly base-rate block + `--unit`/`--target` CLI flags & validation D-03 (wave 3)

**Wave 4** *(blocked on Wave 3 completion)*

- [ ] 25-04-PLAN.md — doc ripple, DQ-gate-ignores-new-keys + example byte-invariance guards, installer re-sync, frozen/catalogue proofs (wave 4)

### Phase 26: Per-skill read contracts

**Goal**: The five skills that plan or narrate an analysis (`dsx-scope-analysis`,
`dsx-define-metrics`, `dsx-design-experiment`, `dsx-build-model`, `dsx-narrate`)
each gain one named-input read step consuming `EDA.md` front-matter and the
profile, with a repo-integrity test that every named key exists in the templates.
**Depends on**: Phase 25
**Requirements**: REQ-P26-01, REQ-P26-02, REQ-P26-03
**Success Criteria** (what must be TRUE):

  1. Each of the five skills opens with a read step naming its keys, their effect, and the absent-artifact fallback.
  2. A test fails the suite when a named key is absent from `templates/EDA.md` or `templates/DATA-PROFILE.yaml`.
  3. `git diff --stat -- dsx/` is empty for the phase; `node install.mjs --check` passes.

**Plans**: 4 plans

**Wave 1** *(parallel — disjoint skill files)*

- [ ] 26-01-PLAN.md — `<inputs>` read steps for dsx-scope-analysis, dsx-define-metrics, dsx-design-experiment (REQ-P26-01)
- [ ] 26-02-PLAN.md — `<inputs>` read steps for dsx-build-model, dsx-narrate (REQ-P26-01)

**Wave 2** *(blocked on Wave 1)*

- [ ] 26-03-PLAN.md — TDD repo-integrity guard `tests/test_skill_read_contracts.py`, RED→GREEN, negative control proves a renamed key fails (REQ-P26-02)

**Wave 3** *(blocked on Wave 2)*

- [ ] 26-04-PLAN.md — installer re-sync + byte-identity / catalogue 276→276 / full-suite close (REQ-P26-03)

### Phase 27: Evidence case — feature-origin-only leak

**Goal**: Build and measure the §6.5 item 7 corpus case (a leak with no name match,
no visible fit call, no contradicting declaration); if the gate misses it, ship an
optional `model.feature_provenance[]` declaration and its declaration-only check
under D-05; if the gate catches it, record which code and mint nothing.
**Depends on**: Phase 26
**Requirements**: REQ-P27-01, REQ-P27-02, REQ-P27-03
**Success Criteria** (what must be TRUE):

  1. The case is measured at all four gate points from a fresh temp directory before any check is designed, and the postmortem records the result.
  2. Either a live miss is closed by a minted, D-05-cited check whose fixture entries are complete, or the already-caught outcome is recorded with the codes and nothing is minted.
  3. Brief §6.5 item 7 states the measured evidence.

**Plans**: 2 (planned 2026-09-07; gsd-planner opus → plan-checker PASSED → orchestrator re-verified)

**Wave 1:**
- [ ] 27-01-PLAN.md — mint `DSX-ML-034` declaration-only feature-provenance check in `dsx/checks/ml.py` (CRITICAL `after_prediction` / HIGH `unknown`-no-waiver / silent when absent) + Kaufman D-05 docstring ("secondary-corroborated, primary PDF paywalled") + `_D05_ALLOWLIST_CODES` + catalogue 276→277 (REQ-P27-02, type: tdd)

**Wave 2** *(blocked on Wave 1 completion — sidecar `absent_code: DSX-ML-034` resolves only once the code ships to the catalogue)*:
- [ ] 27-02-PLAN.md — promote `spike/` fixture → committed corpus fixture `feature-origin-only-leak-*` (stays a MISS: no `feature_provenance` block) + POSTMORTEM + falsifiable ATTRIBUTION sidecar (`promotes_backlog_item: 6.5-item-7-feature-provenance`) + four harness maps + spec count 42→43 + brief §6.5 item 7 rewrite + installer re-sync (REQ-P27-01, REQ-P27-03, type: execute)

### Phase 28: Evidence case — magnitude no test computed

**Goal**: Build and measure the §6.5 item 8 corpus case (a claim magnitude no
reported test computed, with every existing claims check clearing); if missed,
ship `claims[].supported_by` and the claim-to-test number-overlap check under
D-05; if caught, record and mint nothing.
**Depends on**: Phase 27
**Requirements**: REQ-P28-01, REQ-P28-02, REQ-P28-03
**Success Criteria** (what must be TRUE):

  1. The case is measured live first and `DSX-CLM-070`/`DSX-STA-012` are shown to clear on it.
  2. Either the miss is closed by a minted, cited check (overlap, never recomputation) or the caught outcome is recorded.
  3. Brief §6.5 item 8 states the measured evidence.

**Plans**: 2 (authored 2026-09-07 by gsd-planner opus — 28-01 measure-live + conditional DSX-CLM-034 mint; 28-02 promote fixture + wire harness, live-miss branch. plan-checker gate PENDING — S4-2 stays unchecked until it passes)

### Phase 29: Evidence case — subgroup harm under a prescriptive recommendation

**Goal**: Build and measure the §6.5 item 9 corpus case (one harmed minority
segment under a positive average, below the Simpson thresholds), confirm a primary
source with an operationalisable criterion and a documented public failure case;
if all hold, ship `decision.subgroup_harm[]` and its check; otherwise record the
half-met condition and mint nothing.
**Depends on**: Phase 28
**Requirements**: REQ-P29-01, REQ-P29-02, REQ-P29-03
**Success Criteria** (what must be TRUE):

  1. The case is measured live and `DSX-MET-030`/`031` are shown not to fire on it.
  2. The primary source is confirmed at its locator by a human read, or the failure to confirm is recorded; the documented case is found with a source, or recorded as not found.
  3. Either the miss is closed by a minted, cited check or the outcome is recorded; brief §6.5 item 9 states the evidence.

**Plans**: TBD

### Phase 30: Calibration re-baseline

**Goal**: Re-measure the headline (miss-rate, FPR) pair and every stratum with the
three evidence cases classified, rewrite §6.5 rows 7–9 and the literature record
with the outcomes, and confirm every milestone-audit prerequisite.
**Depends on**: Phase 29
**Requirements**: REQ-P30-01, REQ-P30-02, REQ-P30-03
**Success Criteria** (what must be TRUE):

  1. The stratified report runs green with the new cases classified and the miss-partition floor met.
  2. Catalogue current, snapshots unmutated, doc/code agreement green, installer check green, `scripts/check.sh` green, full suite green on the real interpreter.
  3. Zero codes minted in this phase.

**Plans**: TBD

## Next

v2.0.0, v2.2, v2.3 and v2.4 are shipped and archived (`.planning/milestones/`);
v2.4.1 and v2.5.0 shipped interactively on 2026-09-06 (`.planning/MILESTONES.md`).
v2.6 is active under the autonomous ceremony. Still deferred with unchanged entry
conditions: SEED-001's E-27 … E-31 and brief §6.5 items 1–6.
