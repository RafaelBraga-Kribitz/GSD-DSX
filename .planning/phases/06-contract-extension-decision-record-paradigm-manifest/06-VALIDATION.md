---
phase: 6
slug: contract-extension-decision-record-paradigm-manifest
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-07
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded by `/gsd-plan-phase 6` from `06-RESEARCH.md` § Validation Architecture.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `unittest` (Python 3.9+ stdlib) — the only test runner used anywhere in this codebase |
| **Config file** | none — no `pytest.ini` / `setup.cfg` / `pyproject.toml` test config exists; tests are discovered by directory convention |
| **Quick run command** | `python3 -m unittest discover -s tests` |
| **Full suite command** | `python3 -m unittest discover -s tests -v` |
| **Estimated runtime** | ~0.25 seconds (160 tests, measured during research) |

**Note:** the suite is fast enough that there is no meaningful quick-vs-full distinction. Run the
full suite every time; there is no subset worth maintaining.

---

## Sampling Rate

- **After every task commit:** `python3 -m unittest discover -s tests`
- **After every plan wave:** `python3 -m unittest discover -s tests -v` **plus**
  `python3 scripts/gen-finding-catalogue.py --check`
- **Before `/gsd-verify-work`:** full suite green, catalogue current, and all six gate
  invocations behaving:
  - `dsx gate {plan,execute,verify,ship} --spec examples/good-ANALYSIS-SPEC.yaml` → exit `0`
  - `dsx gate plan --spec examples/bad-ANALYSIS-SPEC.yaml` → exit `1`
  - `dsx gate ship --spec examples/bad-ANALYSIS-SPEC.yaml` → exit `1`
- **Max feedback latency:** 1 second

---

## Per-Task Verification Map

> Task IDs are assigned by the plans. This table is seeded at requirement granularity; the
> `Task ID` column is completed once `*-PLAN.md` files exist, and `Status` is maintained during
> execution.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | TBD | TBD | REQ-P6-01 | — | N/A | unit | `python3 -m unittest tests.test_dsx.TestLoader -v` | ❌ W0 (new method) | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-02 | — | N/A | unit/integration | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-03 | — | N/A | unit | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-04 | — | N/A | unit | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-05 | — | N/A | unit | `python3 -m unittest tests.test_dsx.TestChecks -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-06 | — | N/A | unit | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-07 | T-6-02 | Tolerant reader: a truncated tail line is skipped, not fatal | unit | `python3 -m unittest tests.test_decisions -v` | ❌ W0 (new file) | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-08 | T-6-02 | `dsx explain` exits `0` on empty, missing, and corrupt `DECISIONS.jsonl` | integration | `python3 -m unittest tests.test_dsx.TestCLI -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-09 | — | INFO cannot flip the exit code at any of the four default `GATE_THRESHOLDS` | unit + integration | `python3 -m unittest tests.test_dsx.TestCLI -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-10 | T-6-01 | `dsx/frame/*` never imports `dsx.checks.*` (D-03a blast-radius control) | unit (meta-test) | `python3 -m unittest tests.test_frame_boundary -v` | ❌ W0 (new file) | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-11 | — | N/A | unit (meta-test) | `python3 -m unittest tests.test_gen_finding_catalogue -v` | ❌ W0 (new file) | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-12 | — | N/A | integration | `python3 -m unittest tests.test_dsx.TestCLI -v` | ✅ `tests/test_dsx.py:804-839` | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-13 | — | N/A | integration | `python3 -m unittest tests.test_dsx.TestCLI -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-14 | — | N/A | doc check | file-existence assertion on `.planning/REVERSALS.md` | N/A — docs | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-15 | — | N/A | doc check | manual review of README | N/A — docs | ⬜ pending |
| TBD | TBD | TBD | REQ-P6-16 | — | N/A | integration | `python3 scripts/gen-finding-catalogue.py --check` | ✅ exists | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_frame_boundary.py` — new file; covers REQ-P6-10. Neither the test nor
      `dsx/frame/` exists yet.
- [ ] `tests/test_decisions.py` — new file (or a `TestDecisions` class in `test_dsx.py`);
      covers REQ-P6-07.
- [ ] `tests/test_gen_finding_catalogue.py` — new file (or a `--self-test` mode in the script
      itself); covers REQ-P6-11.
- [ ] New test methods inside the existing `TestLoader` / `TestSpecStructure` / `TestCLI`
      classes in `tests/test_dsx.py` for REQ-P6-01/02/03/04/05/06/08/09/13. No new file — the
      existing 1606-line file's per-class organisation is the right home.
- [ ] No framework install needed — `unittest` is stdlib.

**Do not modify** `tests/test_dsx.py:804-839` (the two D-08 fixture tests). REQ-P6-12 requires
they stay green *unedited*; extending the fixtures is allowed, editing these assertions is not.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| `.planning/REVERSALS.md` carries a usable D-14 reversal template and the `SELF-001` convention | REQ-P6-14 | Documentation quality is not mechanically checkable beyond file existence | Read the file; confirm the template has every D-14 field and that `SELF-001` is defined, not merely mentioned |
| README documents the `suppressions[]` migration path with its authority requirement | REQ-P6-15 | Prose accuracy and completeness require human judgement | Read the README section; confirm it states the authority requirement and is discoverable from the pre-v2.0.0 upgrade path |
| README states the known limit that "a frame that lies passes" | REQ-P6-15 | Same | Confirm the limit is stated plainly, not buried or softened — it is the tool's central honesty caveat |
| Each `examples/known-bad/*` fixture has a post-mortem that explains what went wrong | REQ-P6-13 | A post-mortem's usefulness is a judgement call; structural parsing is automated separately | Read each post-mortem; confirm it names the real-world failure, not a synthetic one |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 1s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
