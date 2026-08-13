---
phase: 10
slug: pre-registered-inference-plan-dsx-pre
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-13
---

# Phase 10 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `10-RESEARCH.md` §"Validation Architecture". The planner fills the
> per-task map once plans exist.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` — no third-party runner. Verified during research: no `pytest.ini`, `conftest.py`, `pyproject.toml` or `[tool.pytest]` exists |
| **Config file** | none — `scripts/check.sh:7` runs `python3 -m unittest discover -s tests -q` |
| **Quick run command** | `python -m unittest tests.test_frame_prereg -v` |
| **Full suite command** | `python -m unittest discover -s tests -q` (or `scripts/check.sh`, which also regenerates and checks the finding catalogue) |
| **Estimated runtime** | ~5 seconds quick, ~60 seconds full suite |

---

## Sampling Rate

- **After every task commit:** Run `python -m unittest tests.test_frame_prereg -v`
- **After every plan wave:** Run `python -m unittest discover -s tests -q` — this is the only
  thing that catches the harness blast radius against `tests/test_known_bad_corpus.py` and
  `tests/test_dsx.py`
- **Before `/gsd-verify-work`:** `scripts/check.sh` green, which also re-runs the good/bad fixture
  gate-contract loop where the decision-trail ordering assumption is exercised for real
- **Max feedback latency:** 60 seconds

---

## Per-Task Verification Map

Filled by the planner once PLAN.md files exist. The requirement-to-test mapping below is the
contract each task's `<verify>` block must satisfy.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | TBD | TBD | REQ-P10-01 | — | Unparseable rule raises `CheckError` → exit 2, never 0 | unit | `python -m unittest tests.test_frame_prereg.TestFallbackRuleParsing -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P10-02 | — | `declared_at` limit stated in remedy text and README; digest compared as recorded bytes | unit + doc-content assertion | `python -m unittest tests.test_frame_prereg.TestContentLockReconciliation -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P10-03 | — | Executed procedure differs from selected branch → exit 1, both branch labels in `detail` | unit + integration | `python -m unittest tests.test_frame_prereg -v` and `python -m unittest tests.test_known_bad_corpus -v` | ❌ W0 (unit) / ✅ (corpus) | ⬜ pending |
| TBD | TBD | TBD | REQ-P10-04 | — | Strictly-more-conservative substitute still blocks; check consults no merit ordering | unit, synthetic spec | `python -m unittest tests.test_frame_prereg.TestNoMeritConsultation -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | D-11 registration | — | `prereg` present in verify/ship, absent from plan/execute; every `DSX-PRE-*` code reachable from a profile | unit | `python -m unittest tests.test_frame_prereg.TestGateRegistration -v` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | D-13 guards | — | `_NOT_SHIPPED` / `_PARADIGM_INDEPENDENT` flip together; catalogue prefix + D-05 allow-list updated | existing tests | `python -m unittest tests.test_dsx -v`, `python -m unittest tests.test_gen_finding_catalogue -v` | ✅ | ⬜ pending |
| TBD | TBD | TBD | Harness blast radius | — | Existing corpus verify/ship calls do not regress to exit 2 | integration | `python -m unittest tests.test_known_bad_corpus -v` | ✅ needs modification | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_frame_prereg.py` — new file covering REQ-P10-01 … REQ-P10-04 plus the
      registration/reachability pair, modelled on `tests/test_frame_interference.py`
- [ ] `examples/known-bad/<slug>-ANALYSIS-SPEC.yaml` and its matching `-POSTMORTEM.md` (D-16), with
      `_TARGET_DEFECT_CODES["<slug>"] = {"verify": "DSX-PRE-030"}` and an
      `_EXPECTED_CAUGHT_DEFECTS["<slug>"]` entry
- [ ] A dedicated positive test in `tests/test_known_bad_corpus.py` for the new fixture's
      verify/ship behaviour — the generic corpus test does not cover non-`plan`/`execute` points
- [ ] **A fix to `tests/test_known_bad_corpus.py::_gate_findings()`** so verify/ship calls do not
      spuriously exit 2 for every existing fixture once `prereg` is registered. **Not optional** —
      without it the full suite goes red for reasons unrelated to any fixture's own defect, and the
      failure surfaces as a JSON decode error rather than a legible assertion
- [ ] Framework install: none — stdlib `unittest` is already the house framework

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The `declared_at` limit is stated honestly in the README rather than presented as a guarantee | REQ-P10-02 | A substring assertion proves the sentence exists, not that it reads as an honest limit to a human | Read `README.md` "## Known limits" and confirm the `declared_at` sentence names the self-declaration as unverifiable without implying the gate detects a lie |
| The `DSX-PRE-030` remedy explains why a better substituted procedure still blocks | REQ-P10-04 | Legibility to an operator under time pressure is a judgement, not a string match | Read the emitted finding on the new known-bad fixture and confirm an operator would not read the gate as broken |
| The citation locator flags are preserved, not "tidied" into confident locators | D-14 | Requires knowing the three flags exist and why | Confirm the docstring still says the article carries no numbered sections/tables/theorems and that φ comes from the 2013 working paper |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
