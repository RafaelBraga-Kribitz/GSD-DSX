---
phase: 7
slug: validity-frame-checks-dsx-val
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-12
validated: 2026-08-24
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> **Reconciled retroactively 2026-08-24** (loop S0-8 / audit `not_validated_phases`): shipped as
> the unfilled plan-phase scaffold. The phase executed and passed (07-VERIFICATION.md `passed`;
> 8/9 REQ-P7 MET, 1/9 PARTIAL by the deliberate D-06 scope decision on REQ-P7-08). This audit maps
> each requirement's *implemented behavior* to its committed automated tests and finds **zero
> coverage gaps** — no `gsd-nyquist-auditor` run and no generated tests.
>
> **On `nyquist_compliant: true` despite REQ-P7-08 being PARTIAL:** Nyquist compliance is about
> whether each requirement's *implemented behavior* has automated verification, not about whether
> the requirement is fully MET. REQ-P7-08's implemented first clause (`DSX-VAL-070` blocks a blank
> operationalisation) is automated-tested; its second clause is deliberately unimplemented (D-06,
> 07-CONTEXT.md), so there is no behavior to test. All shipped behavior is covered → compliant.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` |
| **Config file** | none — discovery-based |
| **Quick run command** | `python3 -m unittest tests.test_frame_val` |
| **Full suite command** | `python3 -m unittest discover -s tests -q` (or `sh scripts/check.sh`) |
| **Estimated runtime** | `tests.test_frame_val` + `TestFrameParadigmReadBoundary` ~1.2s (99 tests); full suite ~47s (1038 tests) — measured 2026-08-24 |

---

## Sampling Rate

- **After every task commit:** `python3 -m unittest tests.test_frame_val`
- **After every plan wave:** `python3 -m unittest discover -s tests -q`
- **Before `/gsd-verify-work`:** Full suite green (`sh scripts/check.sh`)
- **Max feedback latency:** ~47s (full suite)

---

## Per-Requirement Verification Map

Granularity per requirement (retroactive-audit level); each plan is traced to its requirement IDs
in 07-VERIFICATION.md. Threat coverage verified separately in `07-SECURITY.md` (`verified`,
`threats_open: 0`).

| Requirement | Plans | Wave(s) | Covering tests | Automated Command | Status |
|-------------|-------|---------|----------------|-------------------|--------|
| REQ-P7-01 | 07-01, 07-03 | 1, 2 | `_check_estimand_completeness` (`DSX-VAL-010`), `_check_estimand_falsifiability` (`DSX-VAL-011`) — `tests.test_frame_val` | `python3 -m unittest tests.test_frame_val` | ✅ green |
| REQ-P7-02 | 07-01, 07-02, 07-04, 07-08 | 1, 3 | `_check_unit_triad` (`DSX-VAL-020`), `TestKishCitationCoherence` (3/3), worked DEFF value 1.576 asserted | `python3 -m unittest tests.test_frame_val` | ✅ green |
| REQ-P7-03 | 07-04 | 3 | `DSX-VAL-020`/`DSX-EXP-021` disjointness (`observation` vs `assignment`) — `tests.test_frame_val` | `python3 -m unittest tests.test_frame_val` | ✅ green |
| REQ-P7-04 | 07-01, 07-05 | 1, 4 | `_check_dependence` (`DSX-VAL-030`); `DEPENDENCE_ADMISSIBLE_METHODS` ⊆ `VARIANCE_ADJUSTMENTS` | `python3 -m unittest tests.test_frame_val` | ✅ green |
| REQ-P7-05 | 07-02, 07-05, 07-07 | 1, 4, 6 | `DSX-VAL-040`/`DSX-VAL-041` + committed `weak-identification-mmm` fixture (Chan & Perry 2017 citation = supplementary D-05 human check, 07-UAT test 6 pass — not the sole verification) | `python3 -m unittest tests.test_frame_val` | ✅ green |
| REQ-P7-06 | 07-06 | 5 | `_check_sampling_frame` (`DSX-VAL-050`) presence/consistency (D-06) | `python3 -m unittest tests.test_frame_val` | ✅ green |
| REQ-P7-07 | 07-06 | 5 | `_check_missingness` (`DSX-VAL-060`); dedicated test proves `missingness.rate` is never read | `python3 -m unittest tests.test_frame_val` | ✅ green |
| REQ-P7-08 | 07-06 | 5 | **Implemented clause covered:** `_check_measurement` (`DSX-VAL-070`) blocks a blank operationalisation. Second clause deliberately unimplemented (D-06) — no behavior to test. Requirement is `Partial` in REQUIREMENTS.md by design. | `python3 -m unittest tests.test_frame_val` | ✅ green (implemented clause) |
| REQ-P7-09 | 07-03 | 2 | `TestFrameParadigmReadBoundary` (7/7) — no `DSX-VAL-*` check reads `inference.paradigm` (D-11) | `python3 -m unittest tests.test_frame_boundary.TestFrameParadigmReadBoundary` | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

Live confirmation 2026-08-24: `python3 -m unittest tests.test_frame_val tests.test_frame_boundary.TestFrameParadigmReadBoundary` → **99 tests, OK** (part of full suite 1038 OK).

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. Plans 07-03, 07-04, 07-06 are `tdd`; all
`DSX-VAL-*` behaviors landed with committed regression tests. No scaffolding or framework install
was needed.

---

## Manual-Only Verifications

All phase *behaviors* have automated verification (the map above). The phase's human checks were
**supplementary D-05 citation-authenticity reads**, not the requirements' sole verification, and
were all completed in `07-UAT.md` (`status: complete`, 38/38 pass, 0 issues):

| Behavior | Requirement | Why Manual | Resolution |
|----------|-------------|------------|------------|
| Kish (1965) DEFF citation coherence across the four sites | REQ-P7-02 | D-05 human source read | 07-UAT pass; also machine-guarded by `TestKishCitationCoherence` |
| Chan & Perry (2017) citation admissibility | REQ-P7-05 | D-05 human source read | 07-UAT test 6 pass |
| Gelman, Simpson & Betancourt (2017) citation | REQ-P7-05 | D-05 human source read | 07-UAT pass |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references — none MISSING (0 gaps)
- [x] No watch-mode flags
- [x] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-08-24 (retroactive audit, loop S0-8)

---

## Validation Audit 2026-08-24

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

All 9 REQ-P7 requirements' implemented behaviors classified COVERED (REQ-P7-08's implemented first
clause covered; second clause out of scope by D-06). No `gsd-nyquist-auditor` run required (0 gaps).
Evidence: `tests.test_frame_val` + `TestFrameParadigmReadBoundary` 99 OK; full suite 1038 OK
(2026-08-24). D-05 citation reads were completed in 07-UAT (supplementary, not coverage gaps).
