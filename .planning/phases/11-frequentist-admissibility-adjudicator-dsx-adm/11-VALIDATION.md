---
phase: 11
slug: frequentist-admissibility-adjudicator-dsx-adm
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-20
---

# Phase 11 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `unittest` (Python standard library) — Python 3.12.10 installed |
| **Config file** | none — no `pytest.ini` or `pyproject.toml` test config in the repository root |
| **Quick run command** | `python -m unittest tests.test_frame_boundary` |
| **Full suite command** | `python -m unittest discover -s tests` |
| **Estimated runtime** | quick ~0.2 s · full ~18 s |

**Measured baseline, 2026-08-20, before any Phase 11 work:**

```
$ python -m unittest tests.test_frame_boundary
Ran 8 tests in 0.043s
OK                                          (wall clock 183 ms)

$ python -m unittest discover -s tests
warning: DSX-VAL-060 declared twice with different text
Ran 640 tests in 17.933s
OK                                          (wall clock 18.3 s)

$ python scripts/gen-finding-catalogue.py --check
warning: DSX-SPEC-070 declared twice with different text
warning: DSX-SPEC-070 declared twice with different text
warning: DSX-VAL-021 declared twice with different text
warning: DSX-VAL-060 declared twice with different text
finding catalogue is current                 (exit 0)
```

The four duplicate-declaration warnings are **pre-existing** and unrelated to this phase. They are
recorded here so that a warning appearing during Phase 11 can be told apart from one that was
already there.

---

## Sampling Rate

- **After every task commit:** `python -m unittest tests.test_frame_boundary`
- **After every plan wave:** `python -m unittest discover -s tests`
- **Before `/gsd-verify-work`:** full suite green **and** `python scripts/gen-finding-catalogue.py --check` exit 0
- **Max feedback latency:** 1 s per task, 20 s per wave

The quick command targets the two boundary scanners deliberately. They catch the two failure modes
that are hardest to debug once buried — a stray `dsx.checks` import inside `dsx/frame/` (D-03a) and
a stray `inference.paradigm` read (D-11) — and they cost under a fifth of a second.

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| *pending* | — | — | — | — | — | — | — | — | ⬜ pending |

*Seeded by plan-phase before PLAN.md files exist. The planner fills one row per task, mapping each
to the requirement rows below. Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

### Requirement → test map (from `11-RESEARCH.md`)

| Req ID | Behavior | Test Type | Automated Command | File Exists |
|--------|----------|-----------|-------------------|-------------|
| REQ-P11-01 | `families.yaml` parses identically through both loader paths (D-08) | unit | `python -m unittest tests.test_families_yaml` | ❌ Wave 0 |
| REQ-P11-01 | Every family entry traces to a committed fixture (SC 5, D-01) | integration | new test asserting each family `id` is exercised by at least one committed spec | ❌ Wave 0 |
| REQ-P11-02 | Alias resolution is exact-match, never fuzzy (D-18) | unit | new test asserting an unrecognised alias resolves through no distance or substring heuristic | ❌ Wave 0 |
| REQ-P11-03 | Ranked admissible set names assumptions bought and charged | unit | new test on the admissibility function's return shape | ❌ Wave 0 |
| REQ-P11-04 | Underdetermined frame → `DSX-ADM-020`, exit 1 at CRITICAL (D-16, D-21) | integration | new test constructing a spec with a blank required axis, asserting the code and the exit status at `plan` | ❌ Wave 0 |
| REQ-P11-05 | `cmd_recommend` output is additive — v1.5.0 behaviour byte-identical without `--spec` (D-04) | integration | new test comparing `dsx recommend-test proportion --groups 2` against the recorded v1.5.0 output | ❌ Wave 0 |
| REQ-P11-06 | An uncited family fails the build check (D-23, D-24, D-25) | unit | `python -m unittest tests.test_gen_finding_catalogue` — extend existing file | existing file, new cases |
| regression | Good fixture passes every gate; bad fixtures block at their gate points | regression | `python -m unittest tests.test_known_bad_corpus` | existing |
| regression | D-03a and D-11 boundary scanners pass against the new module, plus the new reverse-direction scanner (D-04a) | regression | `python -m unittest tests.test_frame_boundary` | existing, new case |

---

## Wave 0 Requirements

- [ ] `tests/test_families_yaml.py` — new file: dual-parser round-trip (D-08), citation presence
      at load time (D-24 run-time half), alias uniqueness within each `(estimand, dependence)` pair,
      and the assertion that no entry declares a Bayesian inference method (ROADMAP SC 5)
- [ ] `tests/test_frame_admissibility.py` — new file: the pure admissibility function's behaviour,
      `DSX-ADM-010` / `DSX-ADM-020` emission, byte-stable ranking (D-15), and
      `DecisionRecord.escalate` actually set to `True` on the refusal path (D-17)
- [ ] `tests/test_gen_finding_catalogue.py` — extend with cases for the new families-citation
      function (D-23); match the file's established style
- [ ] `tests/test_frame_boundary.py` — extend with the reverse-direction scanner (D-04a): assert no
      file under `dsx/checks/` imports `dsx.frame`

No framework install is needed — `unittest` is standard library and the suite already runs.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Each family's `citation:` names a real primary source that actually supports the family, and the `locator_status` is honest | REQ-P11-06, D-09 | A test can assert a citation string is non-blank and well-formed. It cannot assert the paper says what the entry claims. This is the D-05 judgement the project exists to protect. | For each family entry, open the cited source and confirm (a) the locator resolves, (b) the source supports this estimator family, (c) `locator_status` matches whether the chapter or page was actually confirmed. Mark unconfirmed locators `unverified` rather than guessing. |
| The four ranking orderings in D-13 are stated at the strength their sources support | REQ-P11-03, D-12 | Only a reader can tell a uniform domination from a hedged reliability ordering. The Lydersen result is uniform; the MacKinnon one is hedged by its own authors and fails with few treated clusters. | Read each `DSX-ADM-010` message against its cited source and confirm the message does not overstate. Confirm the Delacre 2022 Correction and the Pustejovsky & Tipton 2023 Corrigendum have been checked before any number from those two papers is used (D-26). |
| `references/test-selection.md`'s corrected Fisher rule reads correctly to a practitioner | D-27 | Correctness of the replacement wording is an editorial judgement, not a parse. | Read the amended row and confirm it no longer prescribes Fisher's exact as the small-cell fallback, and that the replacement carries its citation. |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 1 s per task, < 20 s per wave
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
