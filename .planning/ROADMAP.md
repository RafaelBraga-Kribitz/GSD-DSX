# Roadmap: gsd-dsx

**Active:** v2.4 Visual Excellence — Phases 21–24 (opened 2026-09-02)
**Shipped:** v2.3 Test Catalog — Phases 17–20 (2026-09-02); v2.2 Analytic Surface — Phases 13–16 (2026-08-29); v2.0.0 DSX Validity Frame — Phases 6–12 (2026-08-28); v1.1.0–v1.5.0 — Phases 1–5

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

**v2.0.0 totals:** 11 phases, 89 plans, 208 tasks. Milestone audit `passed` (`.planning/milestones/v2.0.0-MILESTONE-AUDIT.md`); all 11 phases verified and Nyquist-validated; cross-phase integration INTEGRATED.

**v2.2 totals:** 4 phases, 20 plans. Milestone audit `passed` (`.planning/milestones/v2.2-MILESTONE-AUDIT.md`); all 4 phases verified and Nyquist-validated; cross-phase integration INTEGRATED (10/10 seams).

**v2.3 totals:** 4 phases, 11 plans. Milestone audit `passed` (`.planning/milestones/v2.3-MILESTONE-AUDIT.md`); all 4 phases verified and Nyquist-validated; cross-phase integration INTEGRATED (5/5 seams).

## Queued milestone — v2.4 Visual Excellence (Phases 21–24) — ACTIVE since 2026-09-02

**Status:** Active — opened 2026-09-02 by operator direction; driven by the
autonomous ceremony on branch `gsd/v2.4.0-visual-excellence`. Ships as tag
`v2.4.0`. Requirements REQ-P21-01 … REQ-P24-03 in `.planning/REQUIREMENTS.md`.
Full research in `.planning/research/V2.3-V2.4-SCOPE.md` §3 (2026-08-29) —
this milestone does not need a fresh scoping round; scope was re-verified
against the live tree at open (`dsx/checks/viz.py` untouched since before
v2.3; catalogue confirmed at 275).

**Scope boundary (do not re-litigate):** the ~80-entry chart catalog is
citable, not exhaustive-for-its-own-sake — union of five named taxonomies
(FT Visual Vocabulary spine, Wilke's uncertainty family, Graphic Continuum,
Data Visualisation Catalogue, Datawrapper) after synonym merge and principled
exclusions (3D, gauges, word clouds, dual-axis — each cross-referenced to its
banning code). The style layer is license-audited: dsx-538/dsx-urban forked or
built from permissively-licensed sources; dsx-econ/dsx-bbc reimplemented from
published doctrine only, never ported from GPL code or unlicensed PDFs.

### Phase 21: Viz vocabulary reconciliation

**Goal**: Fix the inherited inconsistency every later phase would compound —
several chart types (histogram, density, ecdf, strip, diverging_bar, waterfall,
dumbbell, bump, sankey, kde, population_pyramid, butterfly) sit in
`RELATIONSHIP_CHARTS` or smells sets but in no `CHART_CAPABILITIES` family,
guaranteeing `DSX-VIZ-013` friction once the catalog references them — and give
banned/excluded types first-class refusal entries instead of silent absence.
**Requirements**: REQ-P21-01 … REQ-P21-03. **Zero new codes** (set-identity diff).
**Ordering**: hard-blocks Phase 22 (the catalog spine is built on a reconciled
vocabulary).
**Plans**: 1 plan (1 wave) — 21-01-PLAN.md (home the 12 orphans + regenerate
input_types.json; enrich the five banned types to {reason,code,citation} refusal
records; prove 275 → 275). Planned 2026-09-03 (S1-2); plan-checker PASSED 12/12.

### Phase 22: Catalog spine, uncertainty family, selection heuristic

**Goal**: The ~80-entry merged chart catalog with three citable axes per entry,
the uncertainty function family (the one category every poster taxonomy lacks
and a rigour project most needs — D-12a-clean by construction), faceting as an
orthogonal declaration, and the 5-layer question→chart selection heuristic
route-and-cited into the existing taxonomy files.
**Requirements**: REQ-P22-01 … REQ-P22-05.

### Phase 23: Style and snippet layer

**Goal**: The license-audited `.mplstyle` set (dsx-urban as house default —
the only system whose real font is legally vendorable), the analyst-side
`dsx_plotstyle.py` helper, a proven SVG-determinism recipe for
`FIGURE-MANIFEST.yaml` seals, and a per-chart-type snippet catalog that routes
to finding codes rather than restating thresholds.
**Requirements**: REQ-P23-01 … REQ-P23-05.

### Phase 24: Portfolio exemplar and viz calibration

**Goal**: One end-to-end showcase analysis exercising both v2.3 and v2.4 —
the artifact a scrutinizing senior DS reads whole — plus known-bad chart
fixtures and a catch-rate/FPR re-baseline, matching the calibration discipline
Phase 12 and Phase 20 established.
**Requirements**: REQ-P24-01 … REQ-P24-03.

**Pre-agreed contingency:** if the D-05 queue materially outruns the ceremony
cadence, split Phase 23–24 off as v2.5 — the style layer needs almost no human
reads and should not be blocked behind the uncertainty-vocabulary reads.

## Next

v2.0.0, v2.2, and v2.3 are shipped and archived (`.planning/milestones/v2.0.0-*`,
`v2.2-*`, `v2.3-*`). v2.4 is active under the autonomous ceremony. Two dormant
seeds still carry forward (deepen `dsx-explore-data` into a reusable EDA
protocol; grow DATA-PROFILE into hermetic EDA artifacts) — see
`.planning/STATE.md` Deferred Items; both are natural v2.4/v2.5 candidates
given the EDA-adjacent chart work.
