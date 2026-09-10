---
phase: 27
slug: evidence-case-feature-origin-only-leak
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-07
validated: 2026-09-07T00:00:00Z
---

# Phase 27 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `27-RESEARCH.md` `## Validation Architecture`; the planner fills the
> Per-Task Verification Map, validate-phase (S3-5) sets `status: validated`.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python `unittest` (stdlib), CPython 3.12.10 real interpreter `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe` |
| **Config file** | none — discovery via `python -m unittest` |
| **Quick run command** | `python312 -m unittest tests.test_known_bad_corpus tests.test_causal_verb_golden -q` |
| **Full suite command** | `python312 -m unittest discover -s tests -q` + `python312 scripts/gen-finding-catalogue.py --check` + `node install.mjs --check` |
| **Estimated runtime** | ~65 seconds (full suite last green 1590 OK @ Phase 26) |

---

## Sampling Rate

- **After every task commit:** Run `python312 -m unittest tests.test_known_bad_corpus -q`
- **After every plan wave:** Run full `discover` + `gen-finding-catalogue.py --check`
- **Before `/gsd-verify-work`:** Full suite green + `node install.mjs --check`
- **Max feedback latency:** ~65 seconds

---

## Per-Task Verification Map

*Filled by the planner (S3-2). Requirements → behaviours (from `27-RESEARCH.md`
Validation Architecture):*

- **REQ-P27-01** — Fixture pair present, validates, postmortem names a code, sidecar
  falsifiable → corpus test `tests.test_known_bad_corpus`.
- **REQ-P27-02** — `DSX-ML-034` fires CRITICAL on `after_prediction`, HIGH on
  `unknown`; silent when block absent; D-05 gate satisfied → new unit test
  `tests/test_ml_feature_provenance.py` carrying `# D-05: DSX-ML-034` +
  `gen-finding-catalogue.py --check`.
- **REQ-P27-03** — All harness maps + counts consistent; golden ship set pinned;
  catalogue 277 → `tests.test_causal_verb_golden`, `tests.test_frame_val`,
  `tests.test_finding_catalogue_invariant`, `tests.test_phase20_zero_mint_close`,
  `tests.test_dsx`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 27-01-T1 | 27-01 | 1 | REQ-P27-02 | T-27-03 | D-05 marker/docstring stay honest (secondary-corroborated, paywalled) | unit (RED) | `python312 -m unittest tests.test_ml_feature_provenance` (expect non-zero) | ✅ shipped | ✅ green |
| 27-01-T2 | 27-01 | 1 | REQ-P27-02 | T-27-09 | check silent when block absent; dq.py byte-frozen | unit + suite | `python312 -m unittest tests.test_ml_feature_provenance -q && python312 -m unittest discover -s tests -q` | ✅ ml.py exists | ✅ green |
| 27-01-T3 | 27-01 | 1 | REQ-P27-02 | T-27-04, T-27-02a, T-27-08 | one deterministic catalogue row; count pins move together | build + invariant | `python312 scripts/gen-finding-catalogue.py --check && python312 -m unittest tests.test_finding_catalogue_invariant tests.test_phase20_zero_mint_close -q` | ✅ | ✅ green |
| 27-02-T1 | 27-02 | 2 | REQ-P27-01 | T-27-01 | fixture stays a MISS (no feature_provenance block) | validate | `python312 -m dsx.cli validate --spec examples/known-bad/feature-origin-only-leak-ANALYSIS-SPEC.yaml` | ✅ shipped | ✅ green |
| 27-02-T2 | 27-02 | 2 | REQ-P27-01, REQ-P27-03 | T-27-07 | sidecar falsifiable; harness-valid backlog id | corpus | `python312 -m unittest tests.test_known_bad_corpus -q` | ✅ shipped | ✅ green |
| 27-02-T3 | 27-02 | 2 | REQ-P27-03 | T-27-06, T-27-02b, T-27-10, T-27-11 | maps consistent; DSX-ML-034 out of backlog; overlay synced | corpus + invariant + build | `python312 -m unittest discover -s tests -q && python312 scripts/gen-finding-catalogue.py --check && node install.mjs --check` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `examples/known-bad/feature-origin-only-leak-POSTMORTEM.md` — shipped (REQ-P27-01)
- [x] `examples/known-bad/feature-origin-only-leak-ATTRIBUTION.yaml` — shipped (REQ-P27-01/03)
- [x] `tests/test_ml_feature_provenance.py` — shipped unit test carrying `# D-05: DSX-ML-034` (REQ-P27-02)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| *(none expected)* | | | |

*Phase 27 has no user-facing runtime behaviour beyond the declaration-only check and
the corpus fixture; its acceptance test IS the automated invariant set.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 65s
- [x] `nyquist_compliant: true` set in frontmatter

## Requirement Coverage (validate-phase S3-5)

State A (all references shipped). 3/3 requirements COVERED by named `unittest`
tests, 0 MISSING → `nyquist_compliant: true`. Re-run by the orchestrator on real
Python 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`):

| Requirement | Covering test(s) | Verdict |
|-------------|------------------|---------|
| REQ-P27-01 | `tests.test_known_bad_corpus` (fixture present + validates PASS + sidecar falsifiable) | COVERED |
| REQ-P27-02 | `tests/test_ml_feature_provenance.py` (9 tests, `# D-05: DSX-ML-034`) + `gen-finding-catalogue.py --check` | COVERED |
| REQ-P27-03 | `tests.test_causal_verb_golden`, `tests.test_frame_val`, `tests.test_finding_catalogue_invariant`, `tests.test_phase20_zero_mint_close`, `tests.test_dsx` | COVERED |

- Phase module re-run (`tests.test_ml_feature_provenance` + `tests.test_known_bad_corpus`): **60 tests OK**.
- Golden ship set re-measure (`tests.test_causal_verb_golden`): **6 tests OK**.
- Full suite (`unittest discover -s tests -q`): **1599 tests OK** (64.2s).
- Manual-only verifications: none (Phase 27 has no user-facing runtime behaviour
  beyond the declaration-only check and the corpus fixture; its acceptance test IS
  the automated invariant set).

**Approval:** validated (technical) 2026-09-07 — `nyquist_compliant: true`, 0 gaps,
3/3 requirements COVERED by named tests, phase module 60/60 green on real 3.12.10.
UAT round batched to HUMAN-QUEUE as **HQ-43** (non-blocking until S7-2 per
LOOP-LEDGER S3-5).

## Operator UAT sign-off — 2026-09-10 (HQ-43)

**UAT accepted by the operator** (interactive session, 2026-09-10; batched here from LOOP-LEDGER S3-5). Acceptance = the automated invariant set above, plus the session's hands-on run: the promoted fixture was run through `dsx audit`: the minted code stays silent on the honest miss and the incidental findings equal the recorded golden set; the D-05 citation is now a first-hand read. Full suite re-run on real Python 3.12.10 before signing: **1629 tests OK**; `gen-finding-catalogue.py --check` current at 279; `node install.mjs --check` self-test passed (6/6 agents, 14/14 skills, 5 gates). Caveat recorded honestly: the hands-on runs used generated data and the project's own fixtures; the first real portfolio dataset is the live acceptance of the user-facing surface.
