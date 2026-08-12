---
phase: 8
slug: interference-triggering-stability-dsx-int
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-12
---

# Phase 8 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `08-RESEARCH.md` § Validation Architecture. Task IDs are filled once PLAN.md files exist.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python standard-library `unittest` — no pytest, no config file (confirmed directly; same finding as `07-RESEARCH.md`) |
| **Config file** | none |
| **Quick run command** | `python3 -m unittest tests.test_frame_interference -v` (new module, created in this phase) |
| **Full suite command** | `python3 -m unittest discover -s tests -v` |
| **Estimated runtime** | ~5 seconds quick, ~30 seconds full (no slow/integration split exists in this repo) |

**Second gate, not optional.** Any commit that adds a `report.add("DSX-INT-…")` call must also pass
`python3 scripts/gen-finding-catalogue.py --check`. That script enforces decision D-05 — the citation
marker, the reference value or structural criterion, and the linked `# D-05: <CODE>` test marker. It
is a build script, not the gate path, so it may read `tests/`.

---

## Sampling Rate

- **After every task commit:** targeted `python3 -m unittest tests.test_frame_interference -v -k <relevant>`, plus `python3 scripts/gen-finding-catalogue.py --check` once any `DSX-INT-*` code exists.
- **After every plan wave:** `python3 -m unittest discover -s tests -v`
- **Before `/gsd-verify-work`:** full suite green, catalogue check green, the known-bad corpus rewrite landed, and the `interference-shared-budget` second-code collision resolved.
- **Max feedback latency:** 30 seconds

---

## Per-Task Verification Map

Task IDs are assigned when PLAN.md files are written; the requirement→test mapping below is fixed now.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 08-03 T1 | 08-03 | 2 | REQ-P8-01 | T-8-01, T-8-08 | Malformed `interference` sub-block degrades to no finding, never a crash; the Kohavi citation claims only what was read | unit + gate-level (copy-mutate temp fixture) | `python3 -m unittest tests.test_frame_interference -v -k risk` | ❌ W0 | ⬜ pending |
| 08-03 T1 | 08-03 | 2 | REQ-P8-02 | T-8-08 | Cell-level admissibility is attributed to the structural criterion, not to the unread chapter | unit, table-driven over `_RISK_MITIGATION_MAP` | `python3 -m unittest tests.test_frame_interference -v -k mitigation` | ❌ W0 | ⬜ pending |
| 08-01 T1 · 08-04 T1 | 08-01, 08-04 | 1, 3 | REQ-P8-03 | T-8-03, T-8-04 | Dilution function raises on an out-of-range trigger rate rather than returning a plausible wrong number; the input pair is read, never back-solved | unit (`mathx`) + unit (`interference.check`) | `python3 -m unittest tests.test_dsx -v -k dilut` and `python3 -m unittest tests.test_frame_interference -v -k triggering` | ❌ W0 | ⬜ pending |
| 08-04 T1 · 08-04 T2 · 08-06 T1 | 08-04, 08-06 | 3, 5 | REQ-P8-04 | T-8-11 | The section 6.5 entry condition cannot be softened without a red test | unit + documentation-content test | `python3 -m unittest tests.test_frame_interference -v -k ratio_scope` and `python3 -m unittest tests.test_known_bad_corpus -v` | ❌ W0 | ⬜ pending |
| 08-05 T1 · 08-05 T2 | 08-05 | 4 | REQ-P8-05 | T-8-02, T-8-12, T-8-13 | Malformed `stability` sub-block degrades to no finding; severity alone selects the gate point and `GATE_THRESHOLDS` is provably unedited | unit + gate-level severity pinning (HIGH, not CRITICAL) | `python3 -m unittest tests.test_frame_interference -v -k stability` | ❌ W0 | ⬜ pending |
| 08-03 T2 | 08-03 | 2 | REQ-P8-06 | — | N/A | boundary scanner over `dsx/frame/*.py` | `python3 -m unittest tests.test_frame_boundary -v` | ✅ exists | ⬜ pending |
| 08-05 T2 | 08-05 | 4 | (cross-cutting) | T-8-01, T-8-02 | Twenty-five malformed shapes across four sub-blocks raise nothing and find nothing; no exception handler exists in the module | unit sweep + abstract-syntax-tree assertion | `python3 -m unittest tests.test_frame_interference -v -k malformed` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

**REQ-P8-06's ordering question is now resolved, in the direction that costs least.** This
document previously recorded that Phase 7 had not executed plan `07-03`, so the paradigm-read
scanner might not exist. That is no longer true. The planner verified directly on 2026-08-12:
`dsx/frame/val.py` is on disk, `dsx/cli.py` imports and registers `val` in `CHECKS` and in the
`plan`, `verify` and `ship` profiles, and `tests/test_frame_boundary.py` contains
`TestFrameParadigmReadBoundary` with a text detector, an abstract-syntax-tree detector, a
`FRAME_DIR.rglob("*.py")` scan and `paradigm.py` excluded by name. Commits `3633222`, `c7800ef`
and `27f495d` landed it. So `dsx/frame/interference.py` is covered by the glob automatically the
moment the file exists, with no scanner edit at all.

Plan `08-03` Task 2 is still written as check-then-branch — the executor confirms the class is
present rather than assuming it — but the expected branch adds only a named traceability test
asserting `interference.py` is inside the scan and clean under both detectors, plus a comment on
the exclusion set. The contingency branch, which writes the scanner in full in the shape
`07-03-PLAN.md` specified, remains in the plan in case the working tree is older than measured.

---

## Wave 0 Requirements

- [ ] `tests/test_frame_interference.py` — new module. Created by plan `08-03` Task 1 covering
      REQ-P8-01 and REQ-P8-02; extended by `08-04` Task 1 (REQ-P8-03, REQ-P8-04) and by `08-05`
      Tasks 1 and 2 (REQ-P8-05 and the malformed-shape sweep).
- [ ] A dilution function in `dsx/mathx.py` plus its reference-value test in the existing
      `TestMath` class — both new, both in plan `08-01` Task 1.
- [ ] The per-fixture rewrite of `tests/test_known_bad_corpus.py` — a **test-suite design gap
      shared with Phase 7**, not merely a fixture gap. Plan `08-02` Task 2, deliberately scheduled
      in wave 1 so it lands *before* the codes that break the old structure rather than beside
      them; plans `08-03` and `08-04` each add one map entry in the same commit as their code.
- [ ] `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` and its post-mortem — plan
      `08-02` Task 3.
- [x] The paradigm-read scanner in `tests/test_frame_boundary.py` — **already exists.** Phase 7's
      plan `07-03` landed `TestFrameParadigmReadBoundary` with the directory-glob design. Plan
      `08-03` Task 2 is still written as check-then-branch and adds a named traceability test for
      `interference.py` rather than new detection logic.
- [ ] Honest `stability` declarations on all three pre-existing corpus fixtures — plan `08-02`
      Task 1. Without this, `DSX-INT-040` would fire on three fixtures that exist to demonstrate
      other defects, and the family-prefix exclusion would make documenting it impossible.

No framework install is needed — `unittest` is standard library, consistent with the stdlib-only
constraint (D-01).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The risk→mitigation admissibility cells are defensible under the structural criterion | REQ-P8-02 | The criterion — a mitigation is admissible only where it operates on the same interference channel the risk names — is a judgement about meaning. A test can assert the map's keys match the vocabulary and that specific cells hold; it cannot assert the reasoning is sound. | Read each cell's one-line channel justification in `dsx/frame/interference.py` against the mitigation descriptions at `dsx/spec.py:211-218`. Confirm the docstring says the table is derived from the criterion and is not quoted from Kohavi Ch. 22. |
| The Kohavi Ch. 22 citation claims only what was verified | REQ-P8-01, REQ-P8-02 | The chapter's running text is unreachable (paywall plus HTTP 429). Only the technique names and page numbers were verified, from the publisher's index. | Confirm the docstring cites pp. 230-233 for the *existence and naming* of the technique set only, and that no cell-level admissibility claim is attributed to the book. |
| The `brief.md` §6.5 entry condition names the real blocker | REQ-P8-04 | Whether an entry condition is falsifiable is a human judgement. The automated half only asserts the row exists. | Confirm the row names the per-user-data requirement, not "obtained from primary source" — that premise was verified false, since the paper is freely public. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `python3 scripts/gen-finding-catalogue.py --check` green for all four new codes
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
