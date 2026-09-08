# Requirements

**Current milestone:** v2.6 Exploration Depth and Backlog Evidence (Phases 25–30) — see below.
**Shipped:** v1.1.0–v1.5.0 (Phases 1–5, archived); v2.0.0 DSX Validity Frame
(Phases 6–12, `.planning/milestones/v2.0.0-REQUIREMENTS.md`); v2.2 Analytic Surface
(Phases 13–16, `v2.2-REQUIREMENTS.md`); v2.3 Test Catalog (Phases 17–20,
`v2.3-REQUIREMENTS.md`); v2.4 Visual Excellence (Phases 21–24,
`v2.4-REQUIREMENTS.md`); v2.4.1 and v2.5.0 shipped interactively 2026-09-06
(`.planning/MILESTONES.md`).

**Scope source:** `.planning/research/V2.6-SCOPE.md` (2026-09-06) — live-tree facts,
per-phase content, D-05 citation candidates (all UNVERIFIED until the human read),
ordering, contingency, and the critique register these requirements answer. Opened
by operator direction (HUMAN-QUEUE HQ-39). Binding constraints: D-01 (stdlib gate
path), D-02 (declarations only — the profiler is a producer, not a gate), D-05
(citation + structural criterion per minted check), D-06 (additive codes only; live
catalogue re-verified at 276 before this milestone opened), D-13 (evidence phases
measure first; a case the gate already catches closes the phase with no mint).

---

## Phase 25 — Hermetic profile depth (SEED-002)

- [x] REQ-P25-01 `dsx profile` computes, stdlib-only, into `DATA-PROFILE.yaml` —
  additively, with every existing key and value byte-stable — the trust-core
  numbers the explore protocol currently asks the agent to compute: per numeric
  column `min`, `q1`, `median`, `q3`, `max`, `mean`, `sd`, `n_zero`, `n_negative`;
  per categorical column `share_top1`, `share_top10`, `rare_share`, `n_singleton`;
  on the time column `rows_per_day {min, median, max}`, `first_period_ratio`,
  `last_period_ratio`, `share_at_hour_00`; on a declared `--unit` column
  `rows_per_unit {p50, p95, max}` and `largest_unit_share`; on a declared
  `--target` column a weekly base-rate table with `overall`, `weekly_range` and the
  skill's ±20 % `verdict`.

- [x] REQ-P25-02 Every statistic is a declared definition with a cited source — the
  quantile method named by the Hyndman & Fan (1996) type that
  `statistics.quantiles` actually implements, verified at plan time, never assumed
  — and a reference-value test on a hand-computed fixture CSV; two runs on the same
  extract are byte-identical; the committed example profiles regenerate identically
  on every pre-existing key.

- [x] REQ-P25-03 `templates/DATA-PROFILE.yaml`, `references/data-quality-assertions.md`
  and `skills/dsx-explore-data/SKILL.md` steps 1a, 3a, 4a, 4b, 4e and 4f say
  "copied from the profile" wherever the profiler now supplies the number, and the
  agent computes only what the profiler does not produce (null cross-tabs, outlier
  taxonomy, impossible pairs, robust metric recomputes — named exclusions);
  `dsx/checks/dq.py`, the `data[].assertions` vocabulary and the gate profiles are
  byte-unchanged; zero new codes (set-identity 276 → 276, re-measured); installed
  copies re-synced and `node install.mjs --check` passes.

## Phase 26 — Per-skill read contracts (SEED-001 E-26)

- [x] REQ-P26-01 Each of `dsx-scope-analysis`, `dsx-define-metrics`,
  `dsx-design-experiment`, `dsx-build-model` and `dsx-narrate` gains one
  named-input read step at its head stating the `EDA.md` front-matter keys and the
  `DATA-PROFILE.yaml` keys it reads, what each changes in its output, and the
  recorded fallback when the artifact is absent (`eda_artifact: none`), mirroring
  the executor fragment's existing rule.

- [x] REQ-P26-02 An off-gate-path repo-integrity test asserts that every front-matter
  key a skill's read step names exists in `templates/EDA.md`'s front-matter block,
  and every profile key it names exists in `templates/DATA-PROFILE.yaml`
  (CRLF-tolerant), so a renamed key fails the suite instead of silently orphaning a
  read step.

- [x] REQ-P26-03 Skill-only: `dsx/` byte-identical for the phase, zero new codes;
  installed copies re-synced and `node install.mjs --check` passes.

## Phase 27 — Evidence case: a leak attributable only through feature origin (§6.5 item 7)

- [x] REQ-P27-01 A known-bad corpus case — spec, entrypoint, postmortem, ATTRIBUTION
  sidecar — whose leak is attributable only through feature origin: no feature
  name matches `LEAKAGE_PATTERNS`, the leaking column arrives pre-joined so no fit
  or cleaning idiom is visible to the entrypoint scan, and no declaration
  contradicts another. Measured live at all four gate points before any check is
  designed; the measurement is recorded in the postmortem as the entry-condition
  test.

- [x] REQ-P27-02 If the case is a live miss: an optional `model.feature_provenance[]`
  declaration (`{feature, source, available_at, derived_from}`) and a
  declaration-only check that a feature declared available after the prediction
  moment fires CRITICAL and an `unknown` availability without a waiver fires HIGH;
  D-05 citation confirmed at its locator by the human read (candidate: Kaufman et
  al. 2012, ACM TKDD 6(4), the legitimacy condition); D-06 next free `DSX-ML-*`
  number from a re-measured catalogue. If the case is caught by an existing code,
  the postmortem and §6.5 record which, and nothing is minted — that outcome
  satisfies this requirement.

- [x] REQ-P27-03 Corpus harness entries complete (target maps, golden ship ledger,
  validity-frame map, spec count, sidecar with a reserved `absent_code` when
  needed); brief §6.5 item 7 row rewritten with the measured evidence.

## Phase 28 — Evidence case: a magnitude no reported test computed (§6.5 item 8)

- [x] REQ-P28-01 A known-bad corpus case whose `claims[].text` asserts a magnitude
  that no `results.tests[]` entry computed (the reported tests, with effect sizes
  and intervals, cover other metrics), while every existing claims, narrative and
  stats check passes at the default threshold — `DSX-CLM-070` cleared by a declared
  base, `DSX-STA-012` cleared by effect sizes on the reported tests. Measured live
  before any check is designed.

- [x] REQ-P28-02 If the case is a live miss: a declaration-level cross-reference
  `claims[].supported_by` naming the `results.tests[]` entry a claim rests on, and a
  check that every numeric literal in the claim text appears among that test's
  reported numbers (`effect`, `ci`, `from_value`/`to_value`, `base_n`) within a
  declared rounding tolerance — the `DSX-REP-061` named-numbers-overlap precedent,
  never a recomputation; D-05 citation confirmed at its locator (candidates:
  Wilkinson & TFSI 1999; APA JARS–Quant 2018); D-06 next free `DSX-CLM-*` number. If
  caught by an existing code, recorded, nothing minted.

- [x] REQ-P28-03 Corpus harness entries complete; brief §6.5 item 8 row rewritten
  with the measured evidence.

## Phase 29 — Evidence case: subgroup harm under a prescriptive recommendation (§6.5 item 9)

- [x] REQ-P29-01 A known-bad corpus case: a prescriptive recommendation with a
  positive overall effect and declared `results.segments[]` in which one minority
  segment's effect opposes the recommendation's direction, with n above a declared
  floor and no disposition declared — fewer than half the segments oppose, so
  `DSX-MET-030`/`031` structurally do not fire. Measured live before any check is
  designed.

- [x] REQ-P29-02 A primary source with operationalisable criteria confirmed at its
  locator by the human read (candidate: Gail & Simon 1985, Biometrics 41(2), the
  qualitative-interaction definition — enforced as a declaration, never computed),
  and one documented public case where an average benefit masked subgroup harm,
  found by phase research with a primary source; if either cannot be found, that is
  recorded and the item stays on the backlog with the half-met condition stated.

- [x] REQ-P29-03 If REQ-P29-01 is a live miss and REQ-P29-02's source is confirmed:
  an optional `decision.subgroup_harm[]` declaration (`{segment, effect, ci, n,
  disposition: accept | exclude | mitigate, rationale}`) required for a prescriptive
  question whenever a declared segment opposes the recommendation direction at the
  declared floor, with a declaration-only check (missing row CRITICAL; `accept`
  without rationale HIGH); D-06 next free `DSX-COH-*` number; harness entries
  complete; brief §6.5 item 9 row rewritten. Otherwise recorded, nothing minted.

## Phase 30 — Calibration re-baseline (terminal)

- [ ] REQ-P30-01 Catch rate, FPR and every stratum re-measured live with the three
  evidence cases classified — PRESENT with their new code, or ABSENT with an
  attribution sidecar promoting the item — the miss-partition floor still met;
  brief §6.5 rows 7–9 and the deferred table in
  `docs/literature/the-ai-data-scientist.md` updated with each item's outcome.

- [ ] REQ-P30-02 Milestone audit prerequisites: catalogue current
  (`gen-finding-catalogue.py --check` exit 0), all frozen snapshots unmutated,
  doc/code agreement tests green, `node install.mjs --check` passes,
  `scripts/check.sh` green, full suite green on the real interpreter.

- [ ] REQ-P30-03 Zero new codes in this phase (set-identity diff against the
  post-Phase-29 catalogue).

## Out of Scope

| Feature | Reason |
|---------|--------|
| New `data[].assertions` keys or `DSX-DQ-*` codes reading the new profile keys | A gate reading the numbers is a separate D-06 decision; this milestone keeps the profiler a producer (D-01/D-02) |
| SEED-001 E-27 … E-31 | Entry conditions unchanged and unmet |
| §6.5 items 1–6 | Entry conditions unchanged; paradigm-paired items wait for their mirrors (D-12a) |
| Any change to `dsx/checks/viz.py` or the chart corpus | Closed in v2.5.0 |
| Package version bump | Stays 2.0.0 by the precedent of every release since v2.2; `repro_lock.dsx_version` is gate-read |
| Manufacturing a corpus miss to justify a mint | Forbidden by the brief's D-13 rule; a caught case closes its phase with no mint |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| REQ-P25-01 | Phase 25 | Met — verified S1-4 (25-VERIFICATION.md, passed) |
| REQ-P25-02 | Phase 25 | Met — verified S1-4 (25-VERIFICATION.md, passed) |
| REQ-P25-03 | Phase 25 | Met — verified S1-4 (25-VERIFICATION.md, passed) |
| REQ-P26-01 | Phase 26 | Met — verified S2-4 (26-VERIFICATION.md, passed) |
| REQ-P26-02 | Phase 26 | Met — verified S2-4 (26-VERIFICATION.md, passed) |
| REQ-P26-03 | Phase 26 | Met — verified S2-4 (26-VERIFICATION.md, passed) |
| REQ-P27-01 | Phase 27 | Met |
| REQ-P27-02 | Phase 27 | Met |
| REQ-P27-03 | Phase 27 | Met |
| REQ-P28-01 | Phase 28 | Met |
| REQ-P28-02 | Phase 28 | Met |
| REQ-P28-03 | Phase 28 | Met |
| REQ-P29-01 | Phase 29 | Met |
| REQ-P29-02 | Phase 29 | Met |
| REQ-P29-03 | Phase 29 | Met |
| REQ-P30-01 | Phase 30 | Pending |
| REQ-P30-02 | Phase 30 | Pending |
| REQ-P30-03 | Phase 30 | Pending |

**Coverage:**
- v2.6 requirements: 18 total
- Mapped to phases: 18
- Unmapped: 0

---
*Requirements defined: 2026-09-06*
*Last updated: 2026-09-06 at milestone open*
