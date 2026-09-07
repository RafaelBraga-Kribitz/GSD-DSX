---
phase: 25
slug: hermetic-profile-depth
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-06
validated: 2026-09-07
---

# Phase 25 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Audited by the orchestrator (loop S1-5): every requirement mapped to a named
> automated test, re-run green on the real interpreter — not trusted from a report.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `unittest` (Python stdlib — tests are `unittest.TestCase` classes; no pytest config exists) |
| **Config file** | none — `scripts/check.sh` is the gate (`python3 -m unittest discover -s tests -q`) |
| **Quick run command** | `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe -m unittest tests.test_profiler_hermetic` |
| **Full suite command** | `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe -m unittest discover -s tests -q` (== `scripts/check.sh`) |
| **Estimated runtime** | phase module ~0.2 s (51 tests); full suite ~62 s (1583 tests) |

> Real interpreter only — a bare `python3` on this machine can resolve to a package-less stub (Python 3.14.6) that reports the matplotlib determinism test as *skipped* (HUMAN-QUEUE standing note). The gate is stdlib `unittest`, NOT pytest (verified 2026-09-06: no `pyproject.toml`/`pytest.ini`/`setup.cfg`; `scripts/check.sh` runs `unittest discover`).

---

## Sampling Rate

- **After every task commit:** Run the quick run command above
- **After every plan wave:** Run the full suite command above
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** ~62 seconds (full suite)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| numeric/categorical blocks | 25-01 | 1 | REQ-P25-01, REQ-P25-02 | T-25-02 / T-25-04 | reference-value stats; deterministic tie-break | unit | `… -m unittest tests.test_profiler_hermetic.TestNumericBlock tests.test_profiler_hermetic.TestCategoricalBlock` | ✅ | ✅ green |
| determinism / byte-identity | 25-01 | 1 | REQ-P25-02 | T-25-04 | two runs byte-identical; explicit total-order sort | unit | `… -m unittest tests.test_profiler_hermetic.TestProfilerDeterminism` | ✅ | ✅ green |
| time-block depth | 25-02 | 2 | REQ-P25-01 | T-25-01 / T-25-04 | ISO-week edge ratios; locale-free bucketing | unit | `… -m unittest tests.test_profiler_hermetic.TestTimeBlock` | ✅ | ✅ green |
| unit block (`--unit`) | 25-02 | 2 | REQ-P25-01 | T-25-03 / T-25-04 | rows_per_unit p50/p95/max; unknown unit → CheckError | unit | `… -m unittest tests.test_profiler_hermetic.TestUnitBlock` | ✅ | ✅ green |
| target block + CLI flags | 25-03 | 3 | REQ-P25-01, REQ-P25-03 | T-25-05 / T-25-03 | binary `{0,1}` closed-set validation; `--target` requires `--time` | unit | `… -m unittest tests.test_profiler_hermetic.TestTargetBlock` | ✅ | ✅ green |
| doc ripple | 25-04 | 4 | REQ-P25-03 | — | template/reference/skill say "copied from the profile" | unit | `… -m unittest tests.test_profiler_hermetic.TestDocRipple` | ✅ | ✅ green |
| DQ gate ignores new keys | 25-04 | 4 | REQ-P25-03 | T-25-07 | identical verdict ± new profile keys; profiler stays a producer | unit | `… -m unittest tests.test_profiler_hermetic.TestDQGateIgnoresNewKeys` | ✅ | ✅ green |
| example profiles byte-invariant | 25-04 | 4 | REQ-P25-02, REQ-P25-03 | T-25-06 | pinned sha256 digests over CRLF bytes | unit | `… -m unittest tests.test_profiler_hermetic.TestExampleProfilesByteInvariant` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

> All 8 deliverable rows map to a named, existing `unittest.TestCase` class. Phase module re-run on real Python 3.12.10 at S1-5: **Ran 51 tests — OK**; full suite green at S1-4 (**1583 OK**). No requirement has a missing or partial test — `nyquist_compliant: true`.

---

## Wave 0 Requirements

Existing infrastructure covers all phase requirements. The phase is test-driven (RED→GREEN per plan): `tests/test_profiler_hermetic.py` and its 21 hand-computed fixtures under `tests/fixtures/profiler/` were authored inside the phase, plus the CLI tests in the existing `TestProfiler` module. No Wave 0 stub gap, no framework install needed (stdlib `unittest`).

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Security sign-off (SECURITY.md approval line) | (cross-cutting) | Human sign-off per brief §4.4 — the loop verifies mitigations but does not sign | Read `25-SECURITY.md`; confirm `threats_open: 0`, 8/8 CLOSED; approve the Approval line. Batched to HUMAN-QUEUE, non-blocking until S7-2. |
| H&F 1996 type-number citation authenticity (HQ-40 40a) | REQ-P25-02 | Primary-source read (D-05) — a definition, not a minted code | Confirm at the paper's Table 1 that `method="inclusive"` = type 7. Non-blocking: the quantile choice is pinned with a hand-computed reference value; only the citation's type-number authenticity awaits the read. |

*All automated phase behaviors have automated verification; the two rows above are human-read items (not test gaps), both non-blocking until S7-2.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (none — existing infrastructure covers all)
- [x] No watch-mode flags
- [x] Feedback latency < 62s (full suite)
- [x] `nyquist_compliant: true` set in frontmatter

## Validation Audit 2026-09-07

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

**Approval:** validated (technical) 2026-09-07 — Nyquist-compliant, 0 gaps: all 3 requirements COVERED by named automated tests, phase module re-run green (51/51) on real Python 3.12.10, full suite 1583 OK at S1-4. **UAT round batched to HUMAN-QUEUE (non-blocking until S7-2 per LOOP-LEDGER S1-5).**
