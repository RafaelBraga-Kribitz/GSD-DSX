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
| 07-01-T2 | 07-01 | 1 | REQ-P7-01 | T-7-01, T-7-03 | word-list matching has no catastrophic backtracking; long-input timing test | unit | `python3 -m unittest tests.test_dsx -v -k estimand` | ❌ created by task | ⬜ pending |
| 07-03-T1 | 07-03 | 2 | REQ-P7-01 | T-7-01, T-7-05, T-7-07 | malformed sub-block degrades to no finding; decision record emitted; project-defined disclosure in docstring | unit | `python3 -m unittest tests.test_frame_val -v` | ❌ created by task | ⬜ pending |
| 07-01-T3 | 07-01 | 1 | REQ-P7-02 | T-7-07 | unverified Kish locator labelled, not invented | unit (numeric) | `python3 -m unittest tests.test_dsx -v -k design_effect` | ❌ created by task | ⬜ pending |
| 07-04-T1 | 07-04 | 3 | REQ-P7-02 | T-7-01, T-7-04 | illustrative number labelled as illustration, not as a figure computed from the author's spec | unit | `python3 -m unittest tests.test_frame_val -v -k units` | ❌ created by task | ⬜ pending |
| 07-04-T3 | 07-04 | 3 | REQ-P7-03 | T-7-06 | disjointness asserted by construction; design check pinned by content hash | unit + gate-level | `python3 -m unittest tests.test_frame_val -v` | ❌ created by task | ⬜ pending |
| 07-01-T1 | 07-01 | 1 | REQ-P7-04 | T-7-07 | two unverified locators labelled; Conley non-citation recorded | unit | `python3 -m unittest tests.test_dsx -v -k dependence` | ❌ created by task | ⬜ pending |
| 07-05-T1 | 07-05 | 4 | REQ-P7-04 | T-7-01, T-7-05 | malformed sub-block degrades to no finding; decision record emitted | unit | `python3 -m unittest tests.test_frame_val -v -k dependence` | ❌ created by task | ⬜ pending |
| 07-05-T2 | 07-05 | 4 | REQ-P7-05 | T-7-07, T-7-12, T-7-13 | project-defined partition disclosed in both comment and docstring; allow-list entry carries its cause | unit + build check | `python3 scripts/gen-finding-catalogue.py --check` | ✅ command exists | ⬜ pending |
| 07-05-T3 | 07-05 | 4 | REQ-P7-05 | — | N/A | gate-level | `python3 -m unittest tests.test_frame_val -v -k identification` | ❌ created by task | ⬜ pending |
| 07-07-T1 | 07-07 | 6 | REQ-P7-05 | T-7-07, T-7-16 | post-mortem source verified or escalated; corpus assertion narrowed by named exception with a positive counterpart | gate-level | `python3 -m unittest tests.test_known_bad_corpus -v` | ✅ exists, amended | ⬜ pending |
| 07-06-T1 | 07-06 | 5 | REQ-P7-06 | T-7-01 | malformed sub-block degrades to no finding | unit | `python3 -m unittest tests.test_frame_val -v -k sampling_frame` | ❌ created by task | ⬜ pending |
| 07-06-T2 | 07-06 | 5 | REQ-P7-07 | T-7-07, T-7-14 | pairing table stated as assembled, not as a printed table; rate field never read | unit | `python3 -m unittest tests.test_frame_val -v -k missingness` | ❌ created by task | ⬜ pending |
| 07-06-T1 | 07-06 | 5 | REQ-P7-08 | T-7-01 | blank construct demands nothing; second clause recorded as unadjudicated at the code | unit | `python3 -m unittest tests.test_frame_val -v -k measurement` | ❌ created by task | ⬜ pending |
| 07-03-T2 | 07-03 | 2 | REQ-P7-09 | — | detector proven to fire against synthetic violations, and a deliberate real violation run and reverted | abstract-syntax-tree and text boundary | `python3 -m unittest tests.test_frame_boundary -v` | ✅ exists, extended | ⬜ pending |
| 07-06-T3 | 07-06 | 5 | all nine (matrix) | T-7-15 | expected code sets measured and dated; an unrecognised fixture fails loudly | fixture matrix | `python3 -m unittest tests.test_frame_val -v` | ❌ created by task | ⬜ pending |
| 07-07-T2 | 07-07 | 6 | all nine (coverage) | T-7-06, T-7-17 | citation obligations asserted by parsing the module; no requirement checkbox changed | invariant scan | `python3 -m unittest tests.test_frame_val -v` | ❌ created by task | ⬜ pending |

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

- [ ] New test module `tests/test_frame_val.py` for `dsx/frame/val.py` unit tests, mirroring the
      `DSX-SPEC-080/081/082` tests at `tests/test_dsx.py:390-474` — created by plan 07-03, task 1.
      A dedicated module rather than a new class inside `tests/test_dsx.py`, so plans 07-01 and
      07-02 can run in the same wave without a shared-file conflict.
- [ ] `mathx.design_effect()` reference-value test in the existing `TestMath` class
      (`tests/test_dsx.py:33`) — asserting **1.576** (intraclass correlation coefficient 0.02,
      average cluster size 29.8, Cochrane Handbook §23.1.4.1). **Not 3.45**, which is unpublished.
      Created by plan 07-01, task 3.
- [ ] The REQ-P7-09 no-paradigm-read test — a sibling class
      `TestFrameParadigmReadBoundary` in `tests/test_frame_boundary.py`, created by plan 07-03,
      task 2. The existing scanner walks import statements only and cannot be extended to cover
      a string-literal read, so this is a second detector beside it, not an extension of it.
- [ ] `# D-05: DSX-VAL-0NN` marker comments in `tests/` for all **ten** codes. Nine requirements,
      ten codes — decision D-02's own table lists `010`, `011`, `020`, `021`, `030`, `040`, `041`,
      `050`, `060` and `070`. Plan 07-07 task 2 asserts every emitted code has a marker.
- [ ] **Resolution of the known-bad corpus test conflict** — a test-suite design gap, not a fixture
      gap. Owned by plan 07-07, task 1, with the decision recorded in that plan (see below).

**One correction to the wave plan carried from research.** `07-RESEARCH.md` section 9 recommends
landing every fixture and template repair in a late wave, after all the checks exist. That leaves
the suite red between waves, because four regression assertions that must stay green break the
moment a check ships against an unrepaired file. The plans instead land each repair in the same
commit as the check that would otherwise break it: the template unit placeholders and the
interference fixture with `DSX-VAL-020` in plan 07-04, the template identification strength and the
corpus allow-list entry with `DSX-VAL-040`/`041` in plan 07-05, and the good fixture's implied
method with `DSX-VAL-060` in plan 07-06. Only the new fixture and its test conflict are genuinely
late, in plan 07-07, because they cannot be observed until every check exists.

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

**Resolved at planning, in plan 07-07 task 1, with the decision block recorded in that plan.** A
named exception dictionary in `tests/test_known_bad_corpus.py` maps a fixture file name to the
finding code expected to block it at the plan gate. The blanket assertion consults it: a listed
fixture must exit non-zero at `plan` naming that exact code, and must still exit zero at `execute`.
Glob discovery is untouched, every unlisted fixture is asserted exactly as today, and the lost
assertion is replaced by a stronger positive one rather than deleted. The exception is smaller than
it looks: the validity frame check is registered at `plan`, `verify` and `ship` but not at
`execute`, so half the corpus's positive guarantee holds for the new fixture with no special
handling at all. The fixture's target code goes into `_TARGET_CODE_FAMILIES` as one exact code
string rather than the family prefix, which is what keeps the `DSX-VAL-041` allow-list entry from
plan 07-05 legal under `test_incidental_allowlist_names_no_target_family_code`.

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
