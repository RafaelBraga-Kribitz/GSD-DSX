---
phase: 22
slug: catalog-spine-uncertainty-heuristic
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-09-03
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

> Seed only — the authoritative Per-Task map is filled at S2-5 (`/gsd-validate-phase 22`)
> against the finalized PLAN.md task IDs. Requirement→surface mapping (from
> `22-RESEARCH.md` §Validation Architecture):
>
> - **REQ-P22-01** (merged catalog) → repo-integrity test: catalog↔vocabulary conformance
>   (every DSX-admissible mark ↔ exactly one catalog row; row-band `75 ≤ total ≤ 90`);
>   citation authenticity is manual-only, already tracked under HQ-27 (not duplicated).
> - **REQ-P22-02** (uncertainty family) → automated gate test `DSX-VIZ-071` + Phase-21
>   every-mark-has-a-home invariant extended to the 11th `"uncertainty"` relationship key.
> - **REQ-P22-03** (faceting) → automated: `facet_by` declaration + smell-remedy routing to
>   the existing overplotting/density check (no new code).
> - **REQ-P22-04** (5-layer heuristic) → repo-integrity test on the route-and-cite edits to
>   `question-taxonomy.md` / `chart-selection.md`; the corrected D-1 perceptual line asserted.
> - **REQ-P22-05** (perceptual tie-break) → repo-integrity structural-criterion test
>   `rank(a) <= rank(b)` over the catalog rank data (D-1, pure ordering assertion, no
>   computation, OFF the gate path).

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| (filled at S2-5) | — | — | REQ-P22-01..05 | — | — | — | — | — | ⬜ pending |

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

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 40s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
