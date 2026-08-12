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
| TBD | TBD | TBD | REQ-P8-01 | T-8-01 | Malformed `interference` sub-block degrades to a finding, never a crash | unit + gate-level (copy-mutate temp fixture) | `python3 -m unittest tests.test_frame_interference -v -k risk` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P8-02 | — | N/A | unit, table-driven over the risk→mitigation map | `python3 -m unittest tests.test_frame_interference -v -k mitigation` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P8-03 | T-8-03 | Dilution function raises on an out-of-range trigger rate rather than returning a plausible wrong number | unit (`mathx`) + unit (`interference.check`) | `python3 -m unittest tests.test_dsx -v -k dilution` and `tests.test_frame_interference -v -k triggering` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P8-04 | — | N/A | unit + documentation-content test | `python3 -m unittest tests.test_frame_interference -v -k ratio_scope` plus a new corpus-module doc test | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P8-05 | T-8-02 | Malformed `stability` sub-block degrades to a finding | unit + gate-level severity pinning (HIGH, not CRITICAL) | `python3 -m unittest tests.test_frame_interference -v -k stability` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P8-06 | — | N/A | boundary scanner over `dsx/frame/*.py` | `python3 -m unittest tests.test_frame_boundary -v` | ⚠️ ordering-dependent | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

**REQ-P8-06 is ordering-dependent and must be planned as check-then-branch, not as an assumption.**
Phase 7's plan `07-03` Task 2 designs the paradigm-read scanner as a directory glob over every
`*.py` under `dsx/frame/` with `paradigm.py` excluded by name — so `interference.py` is covered
automatically the moment it exists, with no edit. But Phase 7 has **not** executed that plan:
`dsx/frame/val.py` does not exist and `val` is not registered in `dsx/cli.py` (both verified
directly). If Phase 8 executes first, it must write the scanner itself, in the glob shape Phase 7
specified, so Phase 7 inherits it rather than writing a second one.

---

## Wave 0 Requirements

- [ ] `tests/test_frame_interference.py` — new module; stubs for REQ-P8-01 … REQ-P8-05
- [ ] A dilution function in `dsx/mathx.py` plus its reference-value test in the existing `TestMath` class — both new
- [ ] The per-fixture rewrite of `tests/test_known_bad_corpus.py` — a **test-suite design gap shared with Phase 7**, not merely a fixture gap. Needs its own plan task.
- [ ] `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` and its post-mortem — confirmed absent; `examples/known-bad/` currently holds three pairs, none named `triggering-dilution`
- [ ] The paradigm-read scanner in `tests/test_frame_boundary.py` — may already exist depending on execution order; plan a check-then-branch task, never an assumption either way

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
