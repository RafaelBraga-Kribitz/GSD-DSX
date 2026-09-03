# Roadmap: gsd-dsx

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

<details>
<summary>✅ v2.3 Test Catalog (Phases 17–20) — SHIPPED 2026-09-02</summary>

Full phase detail archived at `.planning/milestones/v2.3-ROADMAP.md` and
`.planning/milestones/v2.3-phases/`. Milestone audit `passed`
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

Full phase detail archived at `.planning/milestones/v2.4-ROADMAP.md` and
`.planning/milestones/v2.4-phases/`. Milestone audit `passed`
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

## Next

v2.0.0, v2.2, v2.3, and v2.4 are shipped and archived (`.planning/milestones/v2.0.0-*`,
`v2.2-*`, `v2.3-*`, `v2.4-*`). Two dormant seeds still carry forward (deepen
`dsx-explore-data` into a reusable EDA protocol; grow DATA-PROFILE into
hermetic EDA artifacts) — see `.planning/STATE.md` Deferred Items; both are
natural v2.5 candidates given the EDA-adjacent chart work v2.4 just shipped.

Start the next milestone with `/gsd-new-milestone`.
