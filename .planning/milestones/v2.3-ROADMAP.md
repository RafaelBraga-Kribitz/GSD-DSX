# Roadmap: gsd-dsx

**Active:** v2.3 Test Catalog — Phases 17–20 (opened 2026-08-29)
**Queued:** v2.4 Visual Excellence — Phases 21–24 (entry condition: v2.3 shipped)
**Shipped:** v2.2 Analytic Surface — Phases 13–16 (2026-08-29); v2.0.0 DSX Validity Frame — Phases 6–12 (2026-08-28); v1.1.0–v1.5.0 — Phases 1–5

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

Full phase detail archived at `.planning/milestones/v2.0.0-ROADMAP.md`.

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

Full phase detail archived at `.planning/milestones/v2.2-ROADMAP.md` and
`.planning/milestones/v2.2-phases/`. Milestone audit `passed`
(`.planning/milestones/v2.2-MILESTONE-AUDIT.md`): 23/23 requirements, 4/4
phases verified, 10/10 cross-phase integration seams, Nyquist compliant, 0
unsatisfied/orphaned. Finding catalogue grew 256 → 260 (additive; the frozen
Phase-12 snapshot at 256 was never mutated).

- [x] Phase 13: Task playbooks that fill the spec (skill-only) — 5/5 plans — completed 2026-08-28
- [x] Phase 14: Compounding and data onboarding — 5/5 plans — completed 2026-08-28
- [x] Phase 15: CUPED and BI declaration checks (`DSX-EXP-070`, `DSX-MET-021`) — 6/6 plans — completed 2026-08-29
- [x] Phase 16: Re-run verification off the gate path (`DSX-REP-060`, `DSX-REP-061`) — 4/4 plans — completed 2026-08-29

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

**v2.0.0 totals:** 11 phases, 89 plans, 208 tasks. Milestone audit `passed` (`.planning/milestones/v2.0.0-MILESTONE-AUDIT.md`); all 11 phases verified and Nyquist-validated; cross-phase integration INTEGRATED.

**v2.2 totals:** 4 phases, 20 plans. Milestone audit `passed` (`.planning/milestones/v2.2-MILESTONE-AUDIT.md`); all 4 phases verified and Nyquist-validated; cross-phase integration INTEGRATED (10/10 seams).

## Queued milestone — v2.3 Test Catalog (Phases 17–20) — ACTIVE since 2026-08-29

**Status:** Active — opened 2026-08-29 by operator direction; driven by the
autonomous ceremony on branch `gsd/v2.3.0-test-catalog`. Ships as tag `v2.3.0`.
**Scope source:** `.planning/research/V2.3-V2.4-SCOPE.md` (research provenance,
per-row citations, doctrine dispositions, critique register). Requirements
REQ-P17-01 … REQ-P20-04 in `.planning/REQUIREMENTS.md`. This scope was researched
and written 2026-08-29 with full goals, success criteria and ordering constraints —
**this milestone does not need a fresh scoping round; it needs execution.**

**Scope boundary (do not re-litigate):** the gate does NOT become a per-test
catalog — `families.yaml` stays the admissibility ontology and no gate computes a
statistic. What expands is the routing surface: the `recommend_test` decision
table (~15 → ~75 rows, one primary answer per declarable key) plus 8±1
declaration-only defect checks. Every new gate check needs D-05 (citation +
published reference value) and a D-12a disposition recorded at Phase 17.

### Phase 17: Foundation — repairs and spec vocabulary

**Goal**: Fix the inherited defects every later row would compound (Boschloo
doc/code divergence; missing `estimand_kind` vocabulary; unguarded
`recommend_test` fallthrough; unverified catalogue count), and settle the D-12a
dispositions before any check is written.
**Requirements**: REQ-P17-01 … REQ-P17-05. **Zero new codes** (set-identity diff).
**Ordering**: hard-blocks Phases 18–19 (they read `estimand_kind` and the
pre-allocated ranges).

### Phase 18: Correlation, association and agreement

**Goal**: Decision-table rows for correlation (Pearson/Spearman/Kendall/
point-biserial/phi, keyed on declared estimand kind) and agreement/reliability
(kappa family, Krippendorff alpha, ICC triple, Bland-Altman), with two new
declaration-only gates (scale/kind match; agreement declaration completeness) and
the effect-size band growth in mathx (bands as conventions, never thresholds).
**Requirements**: REQ-P18-01 … REQ-P18-06.

### Phase 19: Repeated measures, trend, categorical, resampling, post-hoc

**Goal**: The bulk of the row expansion (RM/always-GG, trend with declared dose
scores and autocorrelation handling, N-1 chi-square/CMH/FFH honesty, resampling
quadruple, post-hoc family matching, Wilson-not-Wald, exposure offsets) plus the
negative gates (two-stage sphericity ban; variance-test-as-precondition ban;
observed-power ban). Deprecated methods ship as first-class routing-off rows.
**Requirements**: REQ-P19-01 … REQ-P19-07.

### Phase 20: Calibration and reporting close

**Goal**: Known-bad fixtures per new code, catch-rate/FPR re-baseline, D-08
fixture silence, no-autoswitch coverage over every new category, and the
doc/code agreement test that makes the Boschloo divergence class structurally
impossible.
**Requirements**: REQ-P20-01 … REQ-P20-04.

## Queued milestone — v2.4 Visual Excellence (Phases 21–24)

**Status:** Queued. Entry condition (D-13): v2.3 shipped. Requirements
REQ-P21-* … REQ-P24-* in `.planning/REQUIREMENTS.md` under **Queued**. Full
research in `.planning/research/V2.3-V2.4-SCOPE.md` §3: viz vocabulary
reconciliation first (Phase 21), then the ~80-entry chart catalog + uncertainty
family + 5-layer selection heuristic (Phase 22), the license-audited style/snippet
layer with the SVG determinism recipe (Phase 23), and the portfolio exemplar
capstone + viz calibration (Phase 24). Pre-agreed contingency: if v2.3's D-05
queue materially outruns the ceremony cadence, split Phase 23–24 off as v2.5.

## Next

v2.0.0 and v2.2 are shipped and archived (`.planning/milestones/v2.0.0-*`,
`v2.2-*`). v2.3 is active under the autonomous ceremony. Two dormant seeds still
carry forward (deepen `dsx-explore-data` into a reusable EDA protocol; grow
DATA-PROFILE into hermetic EDA artifacts) — see `.planning/STATE.md` Deferred
Items; both are natural v2.4/v2.5 candidates given the EDA-adjacent chart work.
