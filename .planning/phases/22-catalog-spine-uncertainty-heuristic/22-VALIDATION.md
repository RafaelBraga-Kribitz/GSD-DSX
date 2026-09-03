---
phase: 22
slug: catalog-spine-uncertainty-heuristic
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-03
validated: 2026-09-03
---

# Phase 22 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (stdlib `unittest` discover — gate path is stdlib-only, no pandas/scipy/numpy) |
| **Config file** | none — existing `tests/` infrastructure covers all phase requirements |
| **Quick run command** | `python -m unittest tests.test_viz_vocabulary_invariant tests.test_finding_catalogue_invariant -v` |
| **Full suite command** | `python -m unittest discover -s tests` |
| **Estimated runtime** | ~40 seconds (baseline 1471 tests measured this milestone) |

---

## Sampling Rate

- **After every task commit:** Run the quick run command
- **After every plan wave:** Run the full suite command
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** ~40 seconds

---

## Per-Task Verification Map

> Filled at S2-5 (`/gsd-validate-phase 22`) against the finalized four-plan / four-wave
> task set (12 `type="auto"` tasks). Every row's automated command was RE-RUN GREEN by
> the orchestrator this firing (six mitigation modules = 79 tests OK; `gen --check` exit
> 0 @276; full suite 1495 OK / 41.6s). No `⚠️ flaky` or `❌ red` rows → no
> `gsd-nyquist-auditor` spawn required.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 22-01-T1 | 22-01 | 1 | REQ-P22-02 | T-22-02 | 11th `"uncertainty"` key = Wilke's ten §5.6 marks; `BANNED_TYPES` completed to 7 `{reason,code=DSX-VIZ-001,citation}` records (radar→Duan 2023, gauge/word_cloud from signed HQ-27) | automated | `python -m unittest tests.test_viz_vocabulary_invariant` | ✅ | ✅ green |
| 22-01-T2 | 22-01 | 1 | REQ-P22-02 | T-22-01 | Ten uncertainty marks homed into `CHART_CAPABILITIES['interval-range']`; `input_types.json` regenerated (IT040 admits all ten) | automated | `python -m unittest tests.test_viz_vocabulary_invariant` | ✅ | ✅ green |
| 22-01-T3 | 22-01 | 1 | REQ-P22-03 | T-22-03 | `facet_by` orthogonal declaration; `DSX-SMELL-007` remedy routes to it; absent from every chart-type map (no new code) | automated | `python -m unittest tests.test_viz_vocabulary_invariant` | ✅ | ✅ green |
| 22-02-T1 | 22-02 | 2 | REQ-P22-05 | T-22-05 | `DSX-VIZ-071` minted in `_check_uncertainty_vocabulary`, wired into `check()`; membership vs `RELATIONSHIP_CHARTS['uncertainty']`, no computed threshold | automated | `python -m unittest tests.test_uncertainty_vocabulary` | ✅ | ✅ green |
| 22-02-T2 | 22-02 | 2 | REQ-P22-05 | T-22-05 | `_D05_ALLOWLIST_CODES` exact-string entry + `Citation:`/`Structural criterion:` docstring lines; `finding-codes.md` regenerated | automated | `python scripts/gen-finding-catalogue.py --check` | ✅ | ✅ green |
| 22-02-T3 | 22-02 | 2 | REQ-P22-05 | T-22-04, T-22-06 | Set-identity 275→276 (`added={DSX-VIZ-071}`, `removed={}`); DSX-VIZ-072 NOT minted; sibling lockstep pins (p19, phase20) keep zero-mint tells | automated | `python -m unittest tests.test_finding_catalogue_invariant` | ✅ | ✅ green |
| 22-03-T1 | 22-03 | 3 | REQ-P22-01 | T-22-08 | `references/chart-catalog.md` authored (81 rows: 60 admissible generated from `_mark_universe()` + 14 reference-only + 7 refusal), three axes + per-row citation, fenced json payload | automated | `python -m unittest tests.test_chart_catalog_invariant` | ✅ | ✅ green |
| 22-03-T2 | 22-03 | 3 | REQ-P22-01 | T-22-07, T-22-09 | Catalog↔vocab conformance both directions (set-equal `_mark_universe()`); reference-only isolation (14 rows outside the universe → no gate widening); band 75≤total≤90 | automated | `python -m unittest tests.test_chart_catalog_invariant` | ✅ | ✅ green |
| 22-03-T3 | 22-03 | 3 | REQ-P22-05 | T-22-10 | Perceptual tie-break structural criterion: `rank(a) <= rank(b)`, `length==angle` tied both ways, `density` absent — pure ordering, off gate path (D-1) | automated | `python -m unittest tests.test_chart_catalog_invariant` | ✅ | ✅ green |
| 22-04-T1 | 22-04 | 4 | REQ-P22-04 | T-22-10 | `chart-selection.md` L2-L5 route-and-cite edits; superseded 7-item strict chain rewritten to D-1 six-rank-with-ties form (Pitfall 3) | automated | `python -m unittest tests.test_selection_heuristic_docs` | ✅ | ✅ green |
| 22-04-T2 | 22-04 | 4 | REQ-P22-04 | T-22-11 | `question-taxonomy.md` L1 question→task pointer (Munzner ch.3); `skills/dsx-visualize/SKILL.md` step-1 relationship list 10→11; citations HQ-27-signed only (no Abela/Few) | automated | `python -m unittest tests.test_selection_heuristic_docs` | ✅ | ✅ green |
| 22-04-T3 | 22-04 | 4 | REQ-P22-04 | T-22-12 | No-parallel-tree guard (name-pattern regex): no new decision-tree file under `references/`; forbidden-token guard; edits are pointers into existing files | automated | `python -m unittest tests.test_selection_heuristic_docs` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements* — the two new off-gate-path
repo-integrity tests (perceptual tie-break; catalog↔vocabulary conformance) extend the
existing `tests/test_viz_vocabulary_invariant.py` family; the additive-mint proof extends
the existing `tests/test_finding_catalogue_invariant.py`.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Per-citation authenticity at the locator | REQ-P22-01, -02, -05 | D-05 human read | Already tracked under HQ-27 (signed evidence pack); do NOT duplicate here |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies — all 12 `type="auto"`, each with a re-run-GREEN command
- [x] Sampling continuity: no 3 consecutive tasks without automated verify — every task carries an automated command
- [x] Wave 0 covers all MISSING references — no MISSING references (existing `tests/` infrastructure covers all 5 requirements; `wave_0_complete: true`)
- [x] No watch-mode flags — all commands are single-shot `unittest` / `--check`
- [x] Feedback latency < 40s — quick run < 5s; full suite 41.6s measured
- [x] `nyquist_compliant: true` set in frontmatter — all 5 requirements COVERED with live GREEN tests; 0 MISSING / 0 PARTIAL → no `gsd-nyquist-auditor` spawn

**Approval:** validated 2026-09-03 — autonomous loop firing (validate-phase orchestrator, opus/high). Nyquist gap analysis: REQ-P22-01..05 each COVERED by a green automated repo-integrity/gate test (Per-Task map above), 0 MISSING, 0 PARTIAL. The one residual human read — per-citation *authenticity* at the locator (D-05) — is tracked under HQ-27 (signed evidence pack), not duplicated here.
