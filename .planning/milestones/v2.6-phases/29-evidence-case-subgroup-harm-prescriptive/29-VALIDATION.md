---
phase: 29
slug: evidence-case-subgroup-harm-prescriptive
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-08
validated: 2026-09-08T00:00:00Z
---

# Phase 29 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> No planner-seeded VALIDATION.md existed (the crashed 12:38Z S5-5 firing wrote
> `29-SECURITY.md` but not this file); this contract is authored by validate-phase
> (S5-5) directly from the FROZEN `29-CONTEXT.md` decisions, the two plans' task
> structure, and `29-VERIFICATION.md`'s requirement verdicts. validate-phase (S5-5)
> sets `status: validated`.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python `unittest` (stdlib), CPython 3.12.10 real interpreter `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe` |
| **Config file** | none — discovery via `python -m unittest` |
| **Quick run command** | `python312 -m unittest tests.test_subgroup_harm_disposition tests.test_known_bad_corpus -q` |
| **Full suite command** | `python312 -m unittest discover -s tests -q` + `python312 scripts/gen-finding-catalogue.py --check` + `node install.mjs --check` |
| **Estimated runtime** | ~76 seconds (full suite last green 1627 OK @ this phase) |

---

## Sampling Rate

- **After every task commit:** Run `python312 -m unittest tests.test_subgroup_harm_disposition -q`
- **After every plan wave:** Run full `discover` + `gen-finding-catalogue.py --check`
- **Before `/gsd-verify-work`:** Full suite green + `node install.mjs --check`
- **Max feedback latency:** ~76 seconds

---

## Per-Task Verification Map

*Derived from the two plans (S5-2) by validate-phase (S5-5). Requirements →
behaviours (from `29-CONTEXT.md` D-29-00..05 and `29-VERIFICATION.md`):*

- **REQ-P29-01** — Four-segment prescriptive fixture present (3 positive + 1 minority
  opposing at n=1000 above the declared `decision.subgroup_harm_floor: 500`, no
  `decision.subgroup_harm[]` disposition); a shape `DSX-MET-030/031` structurally
  cannot fire on (1-of-4 opposing); measured LIVE MISS at all four gate points before
  any check was designed → corpus test `tests.test_known_bad_corpus` + `29-MEASUREMENT.md`
  (`VERDICT: LIVE MISS`).
- **REQ-P29-02** — `DSX-COH-041` cites Gail & Simon (1985) as the MOTIVATING DEFINITION
  only (never the likelihood-ratio mechanic, D-02); one documented public case found with
  a primary source (Obermeyer et al. 2019, abstract+metadata grade) → new unit test
  `tests/test_subgroup_harm_disposition.py` carrying `# D-05: DSX-COH-041` (lines 10/81)
  + `gen-finding-catalogue.py --check` (allowlist) + `29-RESEARCH.md`.
- **REQ-P29-03** — `_check_subgroup_harm_disposition` (`DSX-COH-041`) fires CRITICAL on a
  missing/invalid disposition row, HIGH on accept-with-blank-rationale (one code, two
  severities); the promoted fixture is the corpus's FIRST `kind: target` (DSX-COH-041
  PRESENT/firing, D-29-00 inverse of the 27/28 misses); all harness maps + counts
  consistent; catalogue 278→279; spec count 44→45; brief §6.5 item 9 rewritten →
  `tests.test_subgroup_harm_disposition`, `tests.test_known_bad_corpus`,
  `tests.test_finding_catalogue_invariant`, `tests.test_dsx`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 29-01-T1 | 29-01 | 1 | REQ-P29-01 | T-29-01 | D-13 measure-first: recorded VERDICT gates the mint | measurement | `python312 spike/…-MEASURE` → `29-MEASUREMENT.md` `VERDICT: LIVE MISS` | ✅ shipped | ✅ green |
| 29-01-T2 | 29-01 | 1 | REQ-P29-02, REQ-P29-03 | T-29-02 | D-05 marker honest (Gail & Simon motivating definition only) | unit (RED→GREEN) | `python312 -m unittest tests.test_subgroup_harm_disposition` | ✅ exists | ✅ green |
| 29-01-T3 | 29-01 | 1 | REQ-P29-03 | T-29-03, T-29-04, T-29-05, T-29-06, T-29-07 | separate new function; one deterministic catalogue row; four count pins move together; dq.py+cli.py byte-frozen | unit + invariant + build | `python312 scripts/gen-finding-catalogue.py --check && python312 -m unittest tests.test_finding_catalogue_invariant -q` | ✅ | ✅ green |
| 29-01-T4 | 29-01 | 1 | REQ-P29-01 | T-29-01 | verdict-branch closure (LIVE MISS → mint; CAUGHT → no-mint terminal) | record | `29-MEASUREMENT.md` verdict first line | ✅ shipped | ✅ green |
| 29-02-T1 | 29-02 | 2 | REQ-P29-01 | T-29-08 | fixture stays an honest TARGET (no `subgroup_harm[]` disposition row) | validate | `python312 -m dsx.cli validate --spec examples/known-bad/subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml` | ✅ shipped | ✅ green |
| 29-02-T2 | 29-02 | 2 | REQ-P29-01, REQ-P29-02 | T-29-09 | sidecar falsifiable; corpus's FIRST `kind: target`; harness-frozen backlog id | corpus | `python312 -m unittest tests.test_known_bad_corpus -q` | ✅ shipped | ✅ green |
| 29-02-T3 | 29-02 | 2 | REQ-P29-03 | T-29-10, T-29-11, T-29-12, T-29-13, T-29-14 | maps consistent; `kind` vocab `("miss","caught","target")`; DSX-COH-041 out of backlog; spec count 45; golden re-measured live; partition floor 3 untouched; overlay synced | corpus + invariant + build | `python312 -m unittest discover -s tests -q && python312 scripts/gen-finding-catalogue.py --check && node install.mjs --check` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `examples/known-bad/subgroup-harm-without-disposition-POSTMORTEM.md` — shipped (REQ-P29-01)
- [x] `examples/known-bad/subgroup-harm-without-disposition-ATTRIBUTION.yaml` — shipped, corpus's FIRST `kind: target` (REQ-P29-01/03)
- [x] `tests/test_subgroup_harm_disposition.py` — shipped unit test carrying `# D-05: DSX-COH-041` (REQ-P29-02)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| *(none expected)* | | | |

*Phase 29 has no user-facing runtime behaviour beyond the declaration-only check and
the corpus TARGET fixture; its acceptance test IS the automated invariant set.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 76s
- [x] `nyquist_compliant: true` set in frontmatter

## Requirement Coverage (validate-phase S5-5)

State A (all references shipped). 3/3 requirements COVERED by named `unittest`
tests, 0 MISSING → `nyquist_compliant: true`. Re-run by the orchestrator on real
Python 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`;
not trusted from a subagent report):

| Requirement | Covering test(s) | Verdict |
|-------------|------------------|---------|
| REQ-P29-01 | `tests.test_known_bad_corpus` (TARGET fixture present + `dsx validate` PASS CRITICAL=0 + four-point measurement, TARGET polarity) + `29-MEASUREMENT.md` (`VERDICT: LIVE MISS`) | COVERED |
| REQ-P29-02 | `tests/test_subgroup_harm_disposition.py` (`# D-05: DSX-COH-041` at lines 10/81) + `gen-finding-catalogue.py --check` (DSX-COH-041 in `_D05_ALLOWLIST_CODES` by exact code, `gen-finding-catalogue.py:228`) + `29-RESEARCH.md` (Obermeyer et al. 2019 documented case) | COVERED |
| REQ-P29-03 | `_check_subgroup_harm_disposition` (`dsx/checks/coherence.py:223`) + `tests/test_subgroup_harm_disposition.py` + `tests.test_known_bad_corpus` (`_TARGET_DEFECT_CODES`, golden set, `kind:target` vocab, backlog disjointness), `tests.test_finding_catalogue_invariant` (279), `tests.test_dsx` (spec count 45) | COVERED |

- Phase modules re-run (`tests.test_subgroup_harm_disposition` + `tests.test_known_bad_corpus`): **72 tests OK**.
- Fixture `dsx validate --spec …subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml`: **PASS, CRITICAL=0** (honest TARGET at the validate point — `DSX-COH-041` fires at plan/verify/ship, correctly silent at validate; `subgroup_harm[]` disposition row deliberately omitted, only `subgroup_harm_floor: 500` declared).
- Catalogue `gen-finding-catalogue.py --check`: **exit 0, "finding catalogue is current"**, Total **279** (the declared-twice warnings are the by-design two-severity dedup pattern, non-failing).
- `dsx/checks/dq.py` + `dsx/cli.py`: **byte-frozen** across the phase (empty diff `4945a62..HEAD`).
- Full suite (`unittest discover -s tests -q`): **1627 tests OK** (76.1s).
- `node install.mjs --check`: self-test **passed** (6/6 agents, 14/14 skills, 5 gates).
- Manual-only verifications: none (Phase 29 has no user-facing runtime behaviour
  beyond the declaration-only check and the corpus TARGET fixture; its acceptance
  test IS the automated invariant set).

**Approval:** validated (technical) 2026-09-08 — `nyquist_compliant: true`, 0 gaps,
3/3 requirements COVERED by named tests, phase modules 72/72 green and full suite
1627 OK on real 3.12.10. UAT round batched to HUMAN-QUEUE as **HQ-45** (non-blocking
until S7-2 per LOOP-LEDGER S5-5).

## Operator UAT sign-off — 2026-09-10 (HQ-45)

**UAT accepted by the operator** (interactive session, 2026-09-10; batched here from LOOP-LEDGER S5-5). Acceptance = the automated invariant set above, plus the session's hands-on run: the promoted fixture was run through `dsx audit`: `DSX-COH-041` fires CRITICAL with a precise, actionable message — the check does exactly what the requirement asked. Full suite re-run on real Python 3.12.10 before signing: **1629 tests OK**; `gen-finding-catalogue.py --check` current at 279; `node install.mjs --check` self-test passed (6/6 agents, 14/14 skills, 5 gates). Caveat recorded honestly: the hands-on runs used generated data and the project's own fixtures; the first real portfolio dataset is the live acceptance of the user-facing surface.
