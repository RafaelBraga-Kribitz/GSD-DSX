---
phase: 7
slug: validity-frame-checks-dsx-val
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-12
---

# Phase 7 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `07-RESEARCH.md` § Validation Architecture. Task IDs land when PLAN.md files exist.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python standard-library `unittest` — verified: no `pytest.ini`, `tox.ini` or `Makefile` in the repository root |
| **Config file** | none |
| **Quick run command** | `python3 -m unittest tests.test_dsx -v` |
| **Full suite command** | `python3 -m unittest discover -s tests -v` |
| **Estimated runtime** | fast — no slow/integration split exists in this repository |

**Second, non-negotiable gate command:** `python3 scripts/gen-finding-catalogue.py --check`.
It enforces D-05 mechanically and must be green from the moment the first
`report.add("DSX-VAL-...")` exists. Treat it as part of the suite, not as a release step.

---

## Sampling Rate

- **After every task commit:** targeted `python3 -m unittest tests.test_dsx -v -k <relevant>`,
  plus `python3 scripts/gen-finding-catalogue.py --check` once any `DSX-VAL-*` code is emitted
- **After every plan wave:** `python3 -m unittest discover -s tests -v` (full suite)
- **Before `/gsd-verify-work`:** full suite green, `--check` green, and the known-bad corpus test
  conflict explicitly resolved (see below)
- **Max feedback latency:** under 30 seconds — the suite is pure standard library with no I/O

---

## Per-Task Verification Map

Task IDs are assigned when PLAN.md files are written. The requirement-level map below is the
binding contract each task must trace to.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | TBD | TBD | REQ-P7-01 | — | N/A | unit | `python3 -m unittest tests.test_dsx -v -k estimand` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P7-02 | — | N/A | unit | `python3 -m unittest tests.test_dsx -v -k design_effect` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P7-03 | — | N/A | gate-level | `python3 -m unittest tests.test_dsx -v -k units` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P7-04 | — | N/A | unit | `python3 -m unittest tests.test_dsx -v -k dependence` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P7-05 | — | N/A | unit + build check | `python3 scripts/gen-finding-catalogue.py --check` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P7-06 | — | N/A | unit | `python3 -m unittest tests.test_dsx -v -k sampling_frame` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P7-07 | — | N/A | unit | `python3 -m unittest tests.test_dsx -v -k missingness` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P7-08 | — | N/A | unit | `python3 -m unittest tests.test_dsx -v -k measurement` | ❌ W0 | ⬜ pending |
| TBD | TBD | TBD | REQ-P7-09 | — | N/A | abstract-syntax-tree boundary | `python3 -m unittest tests.test_frame_boundary -v` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

**Regression assertions that must stay green throughout** — these already exist and must not be
weakened to make new work pass:

| Existing test | What it protects |
|---|---|
| `tests/test_dsx.py` D-08 exit-code pair | good fixture passes every gate, bad fixture blocked by every gate |
| `tests/test_dsx.py:1390-1393` | `dsx init` output clears `dsx gate plan` |
| `tests/test_dsx.py:1239-1244` | the template still fails at ship as a scaffold |
| `tests/test_dsx.py:2585-2607` | every `_NOT_SHIPPED` prefix resolves to no shipped code |
| `tests/test_frame_boundary.py` | no `dsx/frame/*` module imports `dsx.checks` |
| `tests/test_known_bad_corpus.py:193-200` | every corpus fixture clears plan and execute |
| existing `DSX-EXP-020/021` fixtures | `dsx gate` output on them is unchanged (REQ-P7-03) |

---

## Wave 0 Requirements

- [ ] New test class or module for `dsx/frame/val.py` unit tests, mirroring the
      `DSX-SPEC-080/081/082` tests at `tests/test_dsx.py:390-474`
- [ ] `mathx.design_effect()` reference-value test in the existing `TestMath` class
      (`tests/test_dsx.py:33`) — asserting **1.576** (intraclass correlation coefficient 0.02,
      average cluster size 29.8, Cochrane Handbook §23.1.4.1). **Not 3.45**, which is unpublished.
- [ ] The REQ-P7-09 no-paradigm-read test — a new method on
      `tests/test_frame_boundary.py::TestFrameImportBoundary` or a sibling class
- [ ] `# D-05: DSX-VAL-0NN` marker comments in `tests/` for all nine codes
- [ ] **Resolution of the known-bad corpus test conflict** — a test-suite design gap, not a fixture
      gap, and it needs its own task (see below)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The `weak-identification-mmm` fixture encodes a real, published, D-05-admissible case | REQ-P7-05 / ROADMAP SC 1 | Which published case to encode is a sourcing judgement; vendor blogs and Medium posts are inadmissible in either direction | Confirm the fixture's post-mortem cites a primary source, and that the source actually describes weak identification in a marketing-mix model |
| The two project-defined partitions are disclosed as project-defined | REQ-P7-01, REQ-P7-05 | A docstring claiming published authority for a project convention is the exact D-05 failure mode; no test can judge the honesty of prose | Read the `DSX-VAL-010` and `DSX-VAL-041` docstrings and confirm each states the partition is project-defined |
| Unverified citation locators are labelled unverified, not invented | D-05 | Same reason — a plausible-looking locator passes every mechanical check | Confirm the Kish section number and the Gelman/Simpson/Betancourt typeset-version caveat are both flagged, per the `dsx/frame/paradigm.py:66-72` precedent |

---

## Blocking design conflict carried from research

`ROADMAP.md:212-213` requires `examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml` to
**exit 1 at `dsx gate plan`**. `tests/test_known_bad_corpus.py:193-200` globs
`examples/known-bad/*-ANALYSIS-SPEC.yaml` and asserts **every** match clears plan and execute, with
no allow-list escape hatch at that level. Dropping the new fixture into that directory breaks the
test as written.

This must be resolved by an explicit task with a stated decision, not silently. It is listed here
so it cannot be missed at sign-off.

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 30s
- [ ] `python3 scripts/gen-finding-catalogue.py --check` green
- [ ] Known-bad corpus test conflict resolved by an explicit, recorded decision
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
