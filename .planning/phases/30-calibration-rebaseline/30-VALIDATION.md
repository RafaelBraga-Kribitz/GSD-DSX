---
phase: 30
slug: calibration-rebaseline
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-10
validated: 2026-09-10T00:00:00Z
---

# Phase 30 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> No planner-seeded VALIDATION.md existed; this contract is authored by validate-phase
> (S6-5) directly from the FROZEN `30-CONTEXT.md` decisions (GA-1..GA-4), the two plans'
> task structure (30-01 measurement + readout; 30-02 doc re-baseline + audit battery +
> zero-mint), and `30-VERIFICATION.md`'s requirement verdicts. validate-phase (S6-5)
> sets `status: validated`. Phase 30 **measures**; it designs nothing and mints nothing
> (set-identity 279 → 279), so its acceptance test IS the automated invariant set:
> the durable reproducer, the frozen catalogue/snapshot invariants, and the new doc↔live
> agreement test.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python `unittest` (stdlib), CPython 3.12.10 real interpreter `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe` |
| **Config file** | none — discovery via `python -m unittest` |
| **Quick run command** | `python312 -m unittest tests.test_literature_corpus_count_agreement tests.test_finding_catalogue_invariant -q` |
| **Full suite command** | `python312 -m unittest discover -s tests -q` + `python312 scripts/gen-finding-catalogue.py --check` + `node install.mjs --check` + `bash scripts/check.sh` |
| **Estimated runtime** | ~70 seconds (full suite last green 1629 OK @ this phase) |

---

## Sampling Rate

- **After every task commit:** Run `python312 -m unittest tests.test_literature_corpus_count_agreement -q`
- **After every plan wave:** Run full `discover` + `gen-finding-catalogue.py --check`
- **Before `/gsd-verify-work`:** Full suite green + `node install.mjs --check` + `scripts/check.sh`
- **Max feedback latency:** ~70 seconds

---

## Per-Task Verification Map

*Derived from the two plans (S6-2) by validate-phase (S6-5). Requirements →
behaviours (from `30-CONTEXT.md` GA-1..GA-4 and `30-VERIFICATION.md`):*

- **REQ-P30-01** — Catch rate, FPR and every stratum re-measured LIVE over the grown
  corpus (42 known-bad + 15 good-control) with the three v2.6 cases classified as the
  committed harness wiring forces (2 misses DSX-ML-034/DSX-CLM-034, 1 target DSX-COH-041);
  headline pair (miss 1.0 = 5/5, FPR 0.0 = 0/15); miss-partition floor 3 still met at 5;
  both stale doc records re-baselined → `tests.test_known_bad_corpus`
  (`test_stratified_catch_rate_and_fpr_report`, the durable reproducer) + `30-READOUT.md`.
- **REQ-P30-02** — Every milestone-audit prerequisite green on the real interpreter
  (catalogue current, frozen snapshots unmutated, doc/code agreement green,
  `node install.mjs --check` passes, `scripts/check.sh` green, full suite green); the one
  genuine gap (no test bound the literature row-15 counts to the live corpus) closed by the
  new off-gate-path agreement test → `tests.test_literature_corpus_count_agreement`,
  `tests.test_finding_catalogue_invariant`, `gen-finding-catalogue.py --check`,
  `node install.mjs --check`, `scripts/check.sh`.
- **REQ-P30-03** — Zero new codes: set-identity diff against the post-Phase-29 catalogue →
  `gen-finding-catalogue.py --check` (set-identity 279 → 279, added={} removed={}) +
  `tests.test_finding_catalogue_invariant` (code SET == frozen Phase-12 snapshot + the
  sanctioned mints; exactly 279).

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 30-01-T1 | 30-01 | 1 | REQ-P30-01 | T-30-03, T-30-04 | Read-only companion measures live, off gate path, tempdir-per-call; frozen surfaces stay byte-clean | measurement | `python312 .planning/phases/30-calibration-rebaseline/_measure_readout.py` → `30-READOUT.md` numbers | ✅ shipped | ✅ green |
| 30-01-T2 | 30-01 | 1 | REQ-P30-01 | T-30-01, T-30-05 | Durable reproducer independently asserts partitions + floor + target-present invariance | unit | `python312 -m unittest discover -s tests -p test_known_bad_corpus.py -k test_stratified_catch_rate_and_fpr_report` | ✅ shipped | ✅ green |
| 30-01-T3 | 30-01 | 1 | REQ-P30-01 | T-30-01, T-30-02 | Readout numbers equal measured values; FPR reported as a bounded observation with its one-sided upper bound, no interval on the construction-invariant miss-rate | record | grep `30-READOUT.md` for 5/5, 0/15, ≈0.181, construction-invariant caveat | ✅ shipped | ✅ green |
| 30-02-T1 | 30-02 | 2 | REQ-P30-01 | T-30-06 | `brief.md` §6.5 dated re-eval names the three v2.6 codes + /15 FPR; Phase-12 record preserved | record | `grep -oE 'DSX-(ML-034|CLM-034|COH-041)' brief.md` | ✅ shipped | ✅ green |
| 30-02-T2 | 30-02 | 2 | REQ-P30-01, REQ-P30-02 | T-30-07, T-30-08 | Literature row-15 39→42; deferred table flipped to satisfied with evidence; agreement test pins doc==live | record + unit | `python312 -m unittest tests.test_literature_corpus_count_agreement -q` | ✅ shipped | ✅ green |
| 30-02-T3 | 30-02 | 2 | REQ-P30-02, REQ-P30-03 | T-30-09, T-30-10, T-30-11 | Audit battery green; set-identity 279→279; frozen snapshots + `dq.py`/`viz.py`/fixtures byte-frozen; real interpreter | build + invariant | `python312 scripts/gen-finding-catalogue.py --check && python312 -m unittest tests.test_finding_catalogue_invariant -q && node install.mjs --check && bash scripts/check.sh` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [x] `tests/test_literature_corpus_count_agreement.py` — shipped, REQ-P30-02 gap-closing agreement test (doc row-15 == live glob)
- [x] `.planning/phases/30-calibration-rebaseline/_measure_readout.py` — shipped read-only measurement companion (off gate path)
- [x] `.planning/phases/30-calibration-rebaseline/30-READOUT.md` — shipped durable calibration record (headline pair + strata + FPR bound + adversarial review)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| *(none expected)* | | | |

*Phase 30 has no user-facing runtime behaviour beyond the declaration-only doc records and
the static agreement guard; its acceptance test IS the automated invariant set.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 70s
- [x] `nyquist_compliant: true` set in frontmatter

## Requirement Coverage (validate-phase S6-5)

State A (all references shipped). 3/3 requirements COVERED by named `unittest`
tests, 0 MISSING → `nyquist_compliant: true`. Re-run by the orchestrator on real
Python 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`;
not trusted from a subagent report):

| Requirement | Covering test(s) | Verdict |
|-------------|------------------|---------|
| REQ-P30-01 | `tests.test_known_bad_corpus::TestKnownBadCorpus::test_stratified_catch_rate_and_fpr_report` (stratified catch rate + FPR + ABSENT floor ≥ 3 + target-present invariance, re-run **OK 7.7s**) + `30-READOUT.md` (headline pair 5/5, 0/15; three cases classified) | COVERED |
| REQ-P30-02 | `tests.test_literature_corpus_count_agreement` (doc row-15 == live glob, **2 OK**) + `tests.test_finding_catalogue_invariant` (**2 OK**) + `gen-finding-catalogue.py --check` (exit 0) + `node install.mjs --check` (self-test passed) + `scripts/check.sh` ("all checks passed") + full suite | COVERED |
| REQ-P30-03 | `gen-finding-catalogue.py --check` (set-identity **279 → 279**, added={} removed={}) + `tests.test_finding_catalogue_invariant` (code SET == frozen Phase-12 snapshot + sanctioned mints; exactly 279) + whole-phase frozen-surface `git diff` empty | COVERED |

- Reproducer of record `test_stratified_catch_rate_and_fpr_report`: **OK** (7.7s) over the 42+15
  corpus (independent PRESENT/ABSENT denominators, 5-case ABSENT floor ≥ 3, target-present
  invariance proof).
- New REQ-P30-02 agreement test + catalogue invariant: **4 OK** (2 + 2).
- Catalogue `gen-finding-catalogue.py --check`: **exit 0, "finding catalogue is current"**, Total
  **279** (the declared-twice warnings are the by-design two-severity dedup pattern, non-failing);
  set-identity **279 → 279** (REQ-P30-03 zero-mint).
- Frozen surfaces (`dsx/` incl. `dq.py`/`cli.py`/`viz.py`, `examples/`, `references/finding-codes.md`):
  **byte-frozen** across the whole phase (empty diff `e2ffd73..HEAD`).
- Full suite (`unittest discover -s tests`): **1629 tests OK** (69.8s; no skips — the plotstyle
  determinism test ran, not skipped under a python3 stub).
- `node install.mjs --check`: self-test **passed** (6/6 agents, 14/14 skills, 5 gates).
- `scripts/check.sh`: **"all checks passed"** (catalogue current, manifest conformant, gate
  contract good-passes/bad-blocks/missing-errors, determinism identical output).
- Manual-only verifications: none (Phase 30 has no user-facing runtime behaviour beyond the
  doc records and the static agreement guard; its acceptance test IS the automated invariant set).

**Approval:** validated (technical) 2026-09-10 — `nyquist_compliant: true`, 0 gaps,
3/3 requirements COVERED by named tests, reproducer + agreement + invariant green and full suite
1629 OK on real 3.12.10. UAT round batched to HUMAN-QUEUE as **HQ-46** (non-blocking until S7-2
per LOOP-LEDGER S6-5).

## Operator UAT sign-off — 2026-09-10 (HQ-46)

**UAT accepted by the operator** (interactive session, 2026-09-10; batched here from LOOP-LEDGER S6-5). Acceptance = the automated invariant set above, plus the session's hands-on run: the stratified reproducer, the catalogue currency check and the literature agreement test were re-run green; the readout's numbers match the reproducer. Full suite re-run on real Python 3.12.10 before signing: **1629 tests OK**; `gen-finding-catalogue.py --check` current at 279; `node install.mjs --check` self-test passed (6/6 agents, 14/14 skills, 5 gates). Caveat recorded honestly: the hands-on runs used generated data and the project's own fixtures; the first real portfolio dataset is the live acceptance of the user-facing surface.
