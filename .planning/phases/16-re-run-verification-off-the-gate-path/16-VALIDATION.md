---
phase: 16
slug: re-run-verification-off-the-gate-path
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-29
validated: 2026-08-29
---

# Phase 16 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> **State B run** (no prior VALIDATION.md): reconstructed from the four plans + SUMMARY files.
> Phase 16 splits reproduction across a trust boundary — the `dsx-reproduce` skill *runs* the
> entrypoint and writes `REPRO-REPORT.md`; the deterministic gate only *reads* it and executes
> nothing. The gate side (what the check does with the produced report), the additive corpus
> field, and the no-execution guard are all deterministic and already carried dedicated tests
> (`test_reproduce_report` 7, `test_known_bad_corpus` 45, `test_no_entrypoint_execution` 3). The
> one requirement previously covered only by an S3-4 hand-read — REQ-P16-01, the skill's
> existence / registration / structural contract + the template — was **crystallised into a
> standing test** this firing (`tests/test_phase16_reproduce.py`, 9 tests: 5 for REQ-P16-01 plus
> 4 structural anchors the P16-02/03/04 behavioural tests depend on), following the S1-5 / S2-5
> precedent. Gap analysis: **0 gaps** → no `gsd-nyquist-auditor` spawned. Every command below was
> re-run by the orchestrator this firing (brief §5).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (no pytest / no third-party test framework in the repo) |
| **Config file** | none — `python -m unittest discover -s tests -q` (see `scripts/check.sh`) |
| **Quick run command** | `python -m unittest tests.test_phase16_reproduce tests.test_reproduce_report tests.test_no_entrypoint_execution tests.test_known_bad_corpus -v` |
| **Full suite command** | `python -m unittest discover -s tests -q` (1263 tests as of 2026-08-29) |
| **Phase gate** | `sh scripts/check.sh` (full suite + `gen-finding-catalogue.py --check` + capability manifest + gate-contract good/bad/missing exit codes + determinism) |
| **Estimated runtime** | ~54 seconds (full suite: `Ran 1263 tests in ~54s`) |

---

## Sampling Rate

- **After every task commit:** Run `python -m unittest tests.test_phase16_reproduce -v`, plus `python scripts/gen-finding-catalogue.py --check` whenever the catalogue or a cited code changes.
- **After every plan wave:** Run `python -m unittest discover -s tests -q` (full suite).
- **Before `/gsd-verify-work`:** `sh scripts/check.sh` must be green.
- **Max feedback latency:** ~54 seconds.

---

## Per-Task Verification Map

*State B reconstruction: every requirement maps to a named test that runs green.*

| Requirement | Observable behaviour | Test Type | Named passing test(s) | Status |
|-------------|----------------------|-----------|-----------------------|--------|
| REQ-P16-01 | `dsx-reproduce` exists + is capability-registered (14th DSX skill), re-runs `reproducibility.entrypoint` **OFF the gate path**, compares to `results.tests`, writes `REPRO-REPORT.md`, stamps the `reproducibility.reproduce_report` opt-in, and skips honestly (`skipped`/`unable`, no fabricated numbers); `templates/REPRO-REPORT.md` carries the fenced machine block + full status vocabulary | unit | `tests.test_phase16_reproduce.TestPhase16Reproduce.test_req01_skill_exists_and_capability_registered`, `…test_req01_skill_reruns_entrypoint_off_gate_path_and_writes_report`, `…test_req01_skill_opts_spec_in_and_skips_honestly`, `…test_req01_skill_carries_triggers_clause`, `…test_req01_template_has_machine_block_and_status_vocab` | ✅ green |
| REQ-P16-02 | `dsx gate verify/ship` emits `DSX-REP-060` (report missing) / `061` (numbers don't overlap); silent when absent or honestly skipped; verdict-agnostic; imports no pandas/scipy; executes no entrypoint. Both codes HIGH | unit | `tests.test_reproduce_report` (7 — 060 strict-only, 061 fires + not suppressed by PASS, silent on absent/overlap/skipped); anchors `tests.test_phase16_reproduce…test_req02_repro_check_is_stdlib_only`, `…test_req02_both_reproduce_codes_registered_high`; `tests.test_gate_path_hermetic` (2) | ✅ green |
| REQ-P16-03 | Remaining Phase-12 corpus cases carry `protocol_adherence`; the field is additive beside catch rate + FPR, never inside them; catch rate + FPR unchanged | unit | `tests.test_known_bad_corpus` (45, incl. `test_protocol_adherence_is_additive_and_ignored` — field not in `_headline.co_varnames`, headline pinned `(0.25,0.3)`); anchor `tests.test_phase16_reproduce…test_req03_remaining_corpus_cases_carry_protocol_adherence` | ✅ green |
| REQ-P16-04 | A non-vacuous test proves no `dsx/checks/` or `dsx/frame/` module executes the analysis entrypoint | unit | `tests.test_no_entrypoint_execution` (3 — static AST scan, non-empty named set incl. `code.py`+`repro.py`, positive control flags `subprocess.run`/`runpy.run_path`/`os.system`/`exec`, negative control clears `ast.*`/`re.compile`); anchor `tests.test_phase16_reproduce…test_req04_entrypoint_execution_guard_present` | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

The one new module (`tests/test_phase16_reproduce.py`) was created during this validation run to
crystallise REQ-P16-01's structural invariants and anchor the P16-02/03/04 facts. The behavioural
guards were created in execution (S3-3). All are present in the tree; `wave_0_complete: true`.

- [x] `tests/test_phase16_reproduce.py` — structural coverage for REQ-P16-01 + anchors for P16-02/03/04 (9 tests; CRLF-safe)
- [x] `tests/test_reproduce_report.py` — behavioural gate check for DSX-REP-060/061 (REQ-P16-02, 7 tests)
- [x] `tests/test_no_entrypoint_execution.py` — static no-execution AST guard (REQ-P16-04, 3 tests)
- [x] `tests/test_known_bad_corpus.py` — corpus suite incl. `protocol_adherence` additive assertion (REQ-P16-03, 45 tests)

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Runtime fidelity: that the `dsx-reproduce` skill, when actually invoked, *runs the entrypoint and reads back a real fresh number* (beyond the SKILL.md prose asserting it does) | REQ-P16-01 | The entrypoint execution happens in the agent runtime; whether a given run produces a truthful fresh number is per-run agent behaviour no unit test performs. The gate side (what the check does with the produced report) IS fully tested. | Hand-verified at S3-4 (VERIFICATION.md): the 7-step process runs the entrypoint OFF the gate path via Bash, captures numbers from the run's own output, and writes an honest `skipped`/`unable` on failure. Re-verify per actual reproduce run. |

*This manual-only item does **not** reduce Nyquist compliance: REQ-P16-01's deterministic structural
contract (skill exists + registered + names the entrypoint/results.tests/report/opt-in/honest-skip;
template machine block + status vocab) is covered by green automated tests above. Only the per-run
*runtime* fidelity — a read no test can perform — is manual, exactly as with the D-05 reads and the
prose-fidelity items in earlier phases. `nyquist_compliant: true` stands.*

---

## Validation Audit 2026-08-29

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

State B reconstruction: all 4 requirements classified **COVERED** — each maps to a named test that
runs green. **No `gsd-nyquist-auditor` spawned and no gap-filling tests generated (0 gaps).** The
single new test module (`tests/test_phase16_reproduce.py`) was authored to crystallise REQ-P16-01's
structural invariants and anchor the facts P16-02/03/04's behavioural tests depend on, not to fill a
gap the auditor found. Independent re-gate this firing:

- New module `tests.test_phase16_reproduce` → **Ran 9 tests … OK**.
- Gate check `tests.test_reproduce_report` → **Ran 7 tests … OK**; no-execution `tests.test_no_entrypoint_execution` → **Ran 3 tests … OK**; hermeticity `tests.test_gate_path_hermetic` → **Ran 2 tests … OK**.
- Corpus `tests.test_known_bad_corpus` → **Ran 45 tests … OK**; catalogue invariant `tests.test_finding_catalogue_invariant` → **Ran 2 tests … OK** (258 count + set-identity vs snapshot ∪ {060,061}).
- Full corpus gate `sh scripts/check.sh` → **all checks passed** (`Ran 1263 tests … OK`, catalogue current at 258, capability manifest conformant — 14 skills, gate contract good/bad/missing, determinism identical).

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (none — 0 gaps)
- [x] No watch-mode flags
- [x] Feedback latency < 54s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-08-29 — `nyquist_compliant: true`, 0 gaps, 4/4 requirements COVERED by green automated tests; independent re-gate green (`Ran 1263 tests … OK`).
