---
phase: 28
slug: evidence-case-magnitude-no-test-computed
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-07
validated: 2026-09-08T00:00:00Z
---

# Phase 28 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `28-RESEARCH.md` `## Validation Architecture`; the planner filled the
> Per-Task Verification Map, validate-phase (S4-5) sets `status: validated`.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python `unittest` (stdlib), CPython 3.12.10 real interpreter `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe` |
| **Config file** | none — discovery via `python -m unittest` |
| **Quick run command** | `python312 -m unittest tests.test_claims_supported_by tests.test_known_bad_corpus -q` |
| **Full suite command** | `python312 -m unittest discover -s tests -q` + `python312 scripts/gen-finding-catalogue.py --check` + `node install.mjs --check` |
| **Estimated runtime** | ~65 seconds (full suite last green 1615 OK @ this phase) |

---

## Sampling Rate

- **After every task commit:** Run `python312 -m unittest tests.test_claims_supported_by -q`
- **After every plan wave:** Run full `discover` + `gen-finding-catalogue.py --check`
- **Before `/gsd-verify-work`:** Full suite green + `node install.mjs --check`
- **Max feedback latency:** ~65 seconds

---

## Per-Task Verification Map

*Filled by the planner (S4-2). Requirements → behaviours (from `28-RESEARCH.md`
Validation Architecture):*

- **REQ-P28-01** — Collision fixture present, validates PASS, magnitude claim clears
  every existing check (`DSX-CLM-033` union-membership via the ×100 bridge,
  `DSX-CLM-070`, `DSX-STA-011/012`) while no reported test computed the claimed
  metric; measured LIVE MISS before any check was designed → corpus test
  `tests.test_known_bad_corpus` + `28-MEASUREMENT.md` (`VERDICT: LIVE MISS`).
- **REQ-P28-02** — `DSX-CLM-034` (`_check_supported_by_traceability`) fires HIGH when a
  claim magnitude does not trace to its cited test's reported numbers to
  `claims[].rounding` sig-figs; silent when `supported_by` absent; tolerance never
  looser than `DSX-CLM-033`; D-05 (Wilkinson & TFSI 1999, motivating principle) gate
  satisfied → new unit test `tests/test_claims_supported_by.py` carrying
  `# D-05: DSX-CLM-034` + `gen-finding-catalogue.py --check`.
- **REQ-P28-03** — All harness maps + counts consistent; DSX-COH-001 recorded as a
  point-scoped incidental (`_PER_FIXTURE_INCIDENTAL_CODES`, D-28-06); golden ship set
  re-measured live; catalogue 277→278; spec count 43→44; brief §6.5 item 8 rewritten →
  `tests.test_known_bad_corpus`, `tests.test_finding_catalogue_invariant`,
  `tests.test_dsx`, `tests.test_frame_interference`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 28-01-T1 | 28-01 | 1 | REQ-P28-01 | T-28-05 | D-13 measure-first: recorded VERDICT gates the mint | measurement | `python312 spike/…-MEASURE.py` → `28-MEASUREMENT.md` `VERDICT: LIVE MISS` | ✅ shipped | ✅ green |
| 28-01-T2 | 28-01 | 1 | REQ-P28-02 | T-28-01, T-28-07 | D-05 docstring/marker honest (Wilkinson motivating principle); tolerance ≤ -033 | unit (RED→GREEN) | `python312 -m unittest tests.test_claims_supported_by` | ✅ claims.py exists | ✅ green |
| 28-01-T3 | 28-01 | 1 | REQ-P28-02 | T-28-02, T-28-03, T-28-04, T-28-06 | separate new function; one deterministic catalogue row; count pins move together; dq.py byte-frozen | unit + invariant + build | `python312 scripts/gen-finding-catalogue.py --check && python312 -m unittest tests.test_finding_catalogue_invariant -q` | ✅ | ✅ green |
| 28-02-T1 | 28-02 | 2 | REQ-P28-01 | T-28-08 | fixture stays a MISS (no `supported_by`) | validate | `python312 -m dsx.cli validate --spec examples/known-bad/magnitude-without-computed-effect-ANALYSIS-SPEC.yaml` | ✅ shipped | ✅ green |
| 28-02-T2 | 28-02 | 2 | REQ-P28-01, REQ-P28-03 | T-28-09, T-28-12 | sidecar falsifiable; harness-frozen backlog id; golden set re-measured live | corpus | `python312 -m unittest tests.test_known_bad_corpus -q` | ✅ shipped | ✅ green |
| 28-02-T3 | 28-02 | 2 | REQ-P28-03 | T-28-10, T-28-11, T-28-13 | maps consistent; DSX-CLM-034 out of backlog; spec count 44; overlay synced | corpus + invariant + build | `python312 -m unittest discover -s tests -q && python312 scripts/gen-finding-catalogue.py --check && node install.mjs --check` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `examples/known-bad/magnitude-without-computed-effect-POSTMORTEM.md` — shipped (REQ-P28-01)
- [x] `examples/known-bad/magnitude-without-computed-effect-ATTRIBUTION.yaml` — shipped (REQ-P28-01/03)
- [x] `tests/test_claims_supported_by.py` — shipped unit test carrying `# D-05: DSX-CLM-034` (REQ-P28-02)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| *(none expected)* | | | |

*Phase 28 has no user-facing runtime behaviour beyond the declaration-only check and
the corpus fixture; its acceptance test IS the automated invariant set.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 65s
- [x] `nyquist_compliant: true` set in frontmatter

## Requirement Coverage (validate-phase S4-5)

State A (all references shipped). 3/3 requirements COVERED by named `unittest`
tests, 0 MISSING → `nyquist_compliant: true`. Re-run by the orchestrator on real
Python 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`;
not trusted from a subagent report):

| Requirement | Covering test(s) | Verdict |
|-------------|------------------|---------|
| REQ-P28-01 | `tests.test_known_bad_corpus` (collision fixture present + `dsx validate` PASS CRITICAL=0 + four-point measurement) + `28-MEASUREMENT.md` (`VERDICT: LIVE MISS`) | COVERED |
| REQ-P28-02 | `tests/test_claims_supported_by.py` (7 tests, `# D-05: DSX-CLM-034` at line 11) + `gen-finding-catalogue.py --check` (allowlist) | COVERED |
| REQ-P28-03 | `tests.test_known_bad_corpus` (harness maps + `_PER_FIXTURE_INCIDENTAL_CODES` + backlog disjointness + golden re-measure), `tests.test_finding_catalogue_invariant` (278), `tests.test_dsx` (spec count 44), `tests.test_frame_interference` (`_NON_CAUSAL_KNOWN_BAD`) | COVERED |

- Phase modules re-run (`tests.test_claims_supported_by` + `tests.test_known_bad_corpus`): **7 + 60 = 67 tests OK**.
- Fixture `dsx validate --spec …magnitude-without-computed-effect-ANALYSIS-SPEC.yaml`: **PASS, CRITICAL=0** (honest MISS — `DSX-CLM-034` silent, `supported_by` grep 0).
- Full suite (`unittest discover -s tests -q`): **1615 tests OK** (64.3s).
- Manual-only verifications: none (Phase 28 has no user-facing runtime behaviour
  beyond the declaration-only check and the corpus fixture; its acceptance test IS
  the automated invariant set).

**Approval:** validated (technical) 2026-09-08 — `nyquist_compliant: true`, 0 gaps,
3/3 requirements COVERED by named tests, phase modules 67/67 green on real 3.12.10.
UAT round batched to HUMAN-QUEUE as **HQ-44** (non-blocking until S7-2 per
LOOP-LEDGER S4-5).

## Operator UAT sign-off — 2026-09-10 (HQ-44)

**UAT accepted by the operator** (interactive session, 2026-09-10; batched here from LOOP-LEDGER S4-5). Acceptance = the automated invariant set above, plus the session's hands-on run: the promoted fixture was run through `dsx audit`: the minted code stays silent on the honest miss; the one CRITICAL is the documented incidental. Full suite re-run on real Python 3.12.10 before signing: **1629 tests OK**; `gen-finding-catalogue.py --check` current at 279; `node install.mjs --check` self-test passed (6/6 agents, 14/14 skills, 5 gates). Caveat recorded honestly: the hands-on runs used generated data and the project's own fixtures; the first real portfolio dataset is the live acceptance of the user-facing surface.
