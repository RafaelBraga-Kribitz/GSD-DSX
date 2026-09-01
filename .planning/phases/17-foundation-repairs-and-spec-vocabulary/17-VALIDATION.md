---
phase: 17
slug: foundation-repairs-and-spec-vocabulary
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-29
validated: 2026-09-01
---

# Phase 17 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `17-RESEARCH.md` § Validation Architecture (all locators re-verified
> against the live tree in S0-2 and again at research time). Task IDs are filled by
> the planner (S1-2) / refined by `/gsd-validate-phase 17` (S1-5).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (no `pytest` in this repo) |
| **Config file** | none — tests discovered by `unittest discover -s tests` |
| **Quick run command** | `python3 -m unittest tests.<module> -v` (e.g. `python3 -m unittest tests.test_boschloo_reconciliation -v`) |
| **Full suite command** | `python3 -m unittest discover -s tests -q` (the first step of `scripts/check.sh`) |
| **Estimated runtime** | ~20–40 seconds (full suite) |

---

## Sampling Rate

- **After every task commit:** Run the single new test module the task touched, PLUS `python3 -m unittest tests.test_finding_catalogue_invariant -v` on any task that touches a `report.add(...)` call site (cheapest early signal for an accidental code mint — REQ-P17-05).
- **After every plan wave:** Run `python3 -m unittest discover -s tests -q`.
- **Before `/gsd-verify-work`:** Full suite green + `scripts/check.sh` (exercises the good/bad fixture gate at all four gate points `plan`/`execute`/`verify`/`ship`).
- **Max feedback latency:** ~40 seconds.

> **Clean-tree caveat (HUMAN-QUEUE standing note):** run the full suite from a clean tree — a stray root `DECISIONS.jsonl` false-fails `test_dsx.py::test_explain_missing_spec_exits_zero_not_two` and `test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`. If exactly those two fail, remove the stray ledgers and re-run before treating it as real.

---

## Per-Task Verification Map

Seeded at requirement granularity from `17-RESEARCH.md` (planner assigns concrete Task IDs in PLAN.md; validate-phase refines).

| Task ID | Req | Behavior (test oracle) | Test Type | Automated Command | File Exists | Status |
|---------|-----|------------------------|-----------|-------------------|-------------|--------|
| 17-01 | REQ-P17-01 | `recommend_test("proportion", 2)` alternatives name `boschloo_exact`; `boschloo_exact ∈ NONPARAMETRIC_TESTS`; `references/test-selection.md` still names Boschloo (doc↔code pin) | unit | `python3 -m unittest tests.test_boschloo_reconciliation -v` | ✅ | ✅ green (3/3, re-run 2026-09-01) |
| 17-03 | REQ-P17-02 | `ESTIMAND_KINDS` has exactly 6 members; `describe_vocabulary()["estimand_kind"]` returns the same 6 | unit | `python3 -m unittest tests.test_estimand_kind_vocab -v` | ✅ | ✅ green (6/6, re-run 2026-09-01) |
| 17-03 | REQ-P17-02 | `analysis: {}` (no `estimand_kind`) → zero `estimand_kind` findings (absence non-blocking, D-10) | unit | same module | ✅ | ✅ green |
| 17-03 | REQ-P17-02 | `analysis: {estimand_kind: "not_a_real_kind"}` → exactly one loud finding naming `analysis.estimand_kind` (membership guard) | unit | same module | ✅ | ✅ green |
| 17-03 | REQ-P17-02 | `examples/good-ANALYSIS-SPEC.yaml` passes every gate threshold with the new `estimand_kind:` line (fixture EXTENDED, not replaced — D-08) | integration | `python3 -m unittest tests.test_good_fixture_phase15 tests.test_causal_verb_golden` (`test_every_fixture_ship_finding_set_equals_its_golden_baseline`) | ✅ | ✅ green (9/9, re-run 2026-09-01) |
| 17-02 | REQ-P17-03 | D-12a disposition table recorded for all 9 Phase 18/19 gates | manual-only (doc review) | N/A — `17-CONTEXT.md` D-02, committed | ✅ | ✅ complete (grep oracle re-confirmed 2026-09-01) |
| 17-02 | REQ-P17-04 | `recommend_test("time_to_event", …)` always returns `log_rank`; no `if outcome == "time_to_event"` guard in source (fallthrough pinned) | unit | `python3 -m unittest tests.test_time_to_event_fallthrough -v` | ✅ | ✅ green (2/2, re-run 2026-09-01) |
| 17-02 | REQ-P17-04 | D-06 range pre-allocation table present in committed `17-CONTEXT.md` | manual-only | N/A — `17-CONTEXT.md` D-03, committed | ✅ | ✅ complete (grep oracle re-confirmed 2026-09-01) |
| 17-03 | REQ-P17-05 | Live catalogue code set == frozen snapshot + same sanctioned-mint list (no add, no remove) → 260 → 260 | unit | `python3 -m unittest tests.test_finding_catalogue_invariant -v` | ✅ | ✅ green (2/2, re-run 2026-09-01) |
| 17-03 | REQ-P17-05 | `references/finding-codes.md` not stale vs AST-extracted code set | build script | `python3 scripts/gen-finding-catalogue.py --check` | ✅ | ✅ green (exit 0, re-run 2026-09-01) |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/test_boschloo_reconciliation.py` — REQ-P17-01 (exists, 3/3 green)
- [x] `tests/test_estimand_kind_vocab.py` — REQ-P17-02 (exists, 6/6 green: existence + absence-non-blocking + membership-guard)
- [x] `tests/test_time_to_event_fallthrough.py` — REQ-P17-04 (exists, 2/2 green: fallthrough half)
- [x] No framework install needed — stdlib `unittest` is the house convention (confirmed at research time)

*The set-identity (REQ-P17-05) and doc-staleness gates already exist (`tests/test_finding_catalogue_invariant.py`, `scripts/gen-finding-catalogue.py --check`) — verify they still pass unchanged rather than write new ones.*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| D-12a disposition table recorded for every Phase 18/19 gate | REQ-P17-03 | It is a recorded decision table, not runtime behavior | Confirm `17-CONTEXT.md` D-02 lists all 9 gates with dispositions (already committed) |
| D-06 range pre-allocation note committed | REQ-P17-04 (range half) | It is a committed planning note, not runtime behavior | Confirm `17-CONTEXT.md` D-03 range table (already committed) |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies (7 automated oracles + 2 manual-only recorded-decision items)
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (3 new test files — all exist and green)
- [x] No watch-mode flags
- [x] Feedback latency < 40s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** NYQUIST-COMPLIANT 2026-09-01 (orchestrator, State A audit). All 5 requirements
(REQ-P17-01…05) have automated verification: 7 automated test oracles re-run green
(13 targeted tests + 9 golden/good-fixture tests + catalogue `--check` exit 0) plus 2
manual-only recorded-decision items (D-12a table, D-06 ranges) re-confirmed by grep oracle.
Zero gaps → no auditor spawn required (workflow §3). nyquist_compliant: true.

---

## Validation Audit 2026-09-01

| Metric | Count |
|--------|-------|
| Requirements | 5 (REQ-P17-01…05) |
| COVERED (automated, green) | 5 |
| PARTIAL | 0 |
| MISSING | 0 |
| Manual-only (recorded decisions) | 2 (REQ-P17-03, REQ-P17-04 range half) |
| Gaps found | 0 |
| Resolved | 0 (none to resolve — all oracles pre-existing and green) |
| Escalated | 0 |

State A audit: every mapped oracle re-run by the orchestrator from a clean tree
(brief §5). No new test files generated — the seeded Wave-0 modules already exist and
pass. `nyquist_compliant: true`, `status: validated`.
