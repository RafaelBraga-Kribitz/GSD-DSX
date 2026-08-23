---
phase: 11
slug: frequentist-admissibility-adjudicator-dsx-adm
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-20
validated: 2026-08-23
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
| **Estimated runtime** | quick ~0.1 s · full ~44 s |

**Measured, 2026-08-23, at validation time (post-phase):**

```
$ python -m unittest tests.test_frame_boundary
Ran 20 tests in 0.113s
OK

$ python -m unittest discover -s tests
Ran 1028 tests in 44.247s
OK

$ python scripts/gen-finding-catalogue.py --check
warning: DSX-COH-030 declared twice with different text
warning: DSX-PAR-002 declared twice with different text
warning: DSX-SPEC-070 declared twice with different text
warning: DSX-SPEC-070 declared twice with different text
warning: DSX-SPEC-070 declared twice with different text
warning: DSX-VAL-021 declared twice with different text
warning: DSX-VAL-060 declared twice with different text
finding catalogue is current                 (exit 0)
```

**Growth across the phase:** 640 tests at the pre-phase baseline → 1017 at phase close → 1028
after this validation pass filled two gaps (§ Validation Audit below). The boundary suite grew
8 → 10 (plan 11-03's reverse-direction scanner) → 20 (this pass's D-18 scanner).

**The seven duplicate-declaration warnings are pre-existing and unrelated to this phase.** The
baseline first recorded in this file listed only four. That was wrong — it came from a truncated
`tail -5` of the command output, not from the full run. The real count is **seven**, and the list
above is the complete, untruncated output. The error was caught by plan 11-01's executor, which
noticed the catalogue check printed warnings the plan's baseline did not name and logged the
discrepancy to `deferred-items.md` rather than assuming its own run was wrong. Confirmed unrelated
by `git diff abff1f3 HEAD -- scripts/gen-finding-catalogue.py` (script identical; a byte-count
difference between `git show` and the working tree is CRLF, not content).

**Any task asserting on this command must match on `exit 0` and the literal
`finding catalogue is current` line, never on a warning count.**

---

## Sampling Rate

- **After every task commit:** `python -m unittest tests.test_frame_boundary`
- **After every plan wave:** `python -m unittest discover -s tests`
- **Before `/gsd-verify-work`:** full suite green **and** `python scripts/gen-finding-catalogue.py --check` exit 0
- **Max feedback latency:** 1 s per task, 45 s per wave

The quick command targets the boundary scanners deliberately. They catch the failure modes that
are hardest to debug once buried — a stray `dsx.checks` import inside `dsx/frame/` (D-03a), the
reverse direction (D-04a), a stray `inference.paradigm` read (D-11), and now approximate alias
matching (D-18) — and they cost about a tenth of a second.

---

## Per-Task Verification Map

One row per plan deliverable, taken from each SUMMARY's `coverage:` block. Wave assignment is
derived from the `requires:` dependency graphs in the summaries themselves.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| D1 | 11-01 | 1 | REQ-P11-01 | T-11-01 | Amendment names amended-from value and D-02 reason | other | `python -m unittest discover -s tests` | ✅ | ✅ green |
| D2 | 11-01 | 1 | REQ-P11-01 | T-11-02 | Fisher's-exact fallback replaced by cited Boschloo | other | `python -m unittest discover -s tests` | ✅ | ✅ green ⚠️ human |
| D3 | 11-01 | 1 | REQ-P11-01 | T-11-02 | Two D-29 locators stated at supported strength | other | `python -m unittest discover -s tests` | ✅ | ✅ green ⚠️ human |
| D1 | 11-02 | 1 | REQ-P11-01 | T-11-05 | `ESTIMAND_TYPES` closed vocabulary, exact membership | unit | `python -m unittest tests.test_dsx.TestSpecStructure` | ✅ | ✅ green |
| D2 | 11-02 | 1 | REQ-P11-04 | T-11-05 | `estimand.type` optional by construction, no new branch | unit | `python -m unittest tests.test_dsx.TestSpecStructure` | ✅ | ✅ green |
| D3 | 11-02 | 1 | REQ-P11-01 | T-11-06 | All nine specs valid; no gate exit code moved | unit + integration | `python -m unittest tests.test_known_bad_corpus` | ✅ | ✅ green |
| D1 | 11-03 | 1 | REQ-P11-05 | T-11-09, T-11-12 | `dsx/checks/` imports nothing from `dsx.frame` (D-04a) | unit | `python -m unittest tests.test_frame_boundary` | ✅ | ✅ green |
| D2 | 11-03 | 1 | REQ-P11-04 | T-11-10 | Paradigm scoping widens to True on unrecognised value | unit | `python -m unittest tests.test_frame_paradigm` | ✅ | ✅ green |
| D1 | 11-04 | 2 | REQ-P11-01 | T-11-15, T-11-17 | Dual-parser byte-identical round-trip (D-08) | unit | `python -m unittest tests.test_families_yaml` | ✅ | ✅ green |
| D2 | 11-04 | 2 | REQ-P11-06 | T-11-13, T-11-14 | Every entry carries citation + honest `locator_status` | unit | `python -m unittest tests.test_families_yaml` | ✅ | ✅ green ⚠️ human |
| D3 | 11-04 | 2 | REQ-P11-02 | T-11-16 | Axis members valid; pair-scoped alias uniqueness | unit | `python -m unittest tests.test_families_yaml` | ✅ | ✅ green |
| D1 | 11-05 | 3 | REQ-P11-02 | T-11-20, T-11-30 | `load_ontology()` refuses, never degrades | unit | `python -m unittest tests.test_frame_admissibility` | ✅ | ✅ green |
| D2 | 11-05 | 3 | REQ-P11-02 | T-11-18 | Uncited family dropped at load (run-time half of D-24) | unit | `python -m unittest tests.test_frame_admissibility` | ✅ | ✅ green |
| D3 | 11-05 | 3 | REQ-P11-02 | T-11-19, T-11-21 | Exact-match, pair-scoped alias resolution (D-18) | unit | `python -m unittest tests.test_frame_admissibility` | ✅ | ✅ green |
| D4 | 11-05 | 3 | REQ-P11-02 | T-11-09 | Module imports no `dsx.checks`, reads no paradigm | unit | `python -m unittest tests.test_frame_boundary` | ✅ | ✅ green |
| D1 | 11-06 | 4 | REQ-P11-03 | T-11-26 | Byte-stable, permutation-invariant ranking (D-15) | unit | `python -m unittest tests.test_frame_admissibility.TestRankAdmissible` | ✅ | ✅ green |
| D2 | 11-06 | 4 | REQ-P11-03 | — | Pure JSON-serialisable shape naming bought/charged | unit | `python -m unittest tests.test_frame_admissibility.TestAdmissibleFamilies` | ✅ | ✅ green |
| D3 | 11-06 | 4 | REQ-P11-04 | T-11-22, T-11-23 | `DSX-ADM-010`/`020` via ordinary emit, never `CheckError` | unit | `python -m unittest tests.test_frame_admissibility.TestCheck` | ✅ | ✅ green ⚠️ human |
| D4 | 11-06 | 4 | REQ-P11-04 | T-11-24 | `escalate=True` on every refusal path, one record per call | unit | `python -m unittest tests.test_frame_admissibility.TestCheck` | ✅ | ✅ green |
| D5 | 11-06 | 4 | REQ-P11-04 | T-11-11, T-11-25 | `_NOT_SHIPPED` cleared in same commit as first `report.add` | unit | `python -m unittest tests.test_gen_finding_catalogue` | ✅ | ✅ green |
| D1 | 11-07 | 5 | REQ-P11-04 | T-11-27 | Registered at plan/verify/ship; scoping passed in, not derived | unit | `python -m unittest tests.test_dsx.TestAdmissibilityGateRegistration` | ✅ | ✅ green |
| D2 | 11-07 | 5 | REQ-P11-04 | T-11-23, T-11-27 | Blank axis exits 1 at `gate plan` with CRITICAL `DSX-ADM-020` | unit | `python -m unittest tests.test_dsx.TestAdmissibilityGateRegistration` | ✅ | ✅ green |
| D3 | 11-07 | 5 | REQ-P11-05 | T-11-29, T-11-31 | `recommend-test` additive; no-flag output unchanged | integration | `python -m unittest tests.test_dsx.TestAdmissibilityRecommendComposition` | ✅ | ✅ green |
| D4 | 11-07 | 5 | REQ-P11-05 | T-11-09 | `recommend_test()` unmoved; `stats.py` frame-free | unit | `python -m unittest tests.test_frame_boundary` | ✅ | ✅ green |
| D5 | 11-07 | 5 | REQ-P11-04 | T-11-06, T-11-28 | No corpus exit code moved; corpus file unedited | unit | `python -m unittest tests.test_known_bad_corpus` | ✅ | ✅ green |
| D1 | 11-08 | 5 | REQ-P11-06 | T-11-34, T-11-35 | Build gate reads via shipped loader; guarded `sys.path` insert | unit | `python -m unittest tests.test_gen_finding_catalogue.TestFamiliesCitationGate` | ✅ | ✅ green |
| D2 | 11-08 | 5 | REQ-P11-06 | T-11-32 | Every uncited entry reported, never a silent pass | unit | `python -m unittest tests.test_gen_finding_catalogue.TestFamiliesCitationGate` | ✅ | ✅ green |
| D3 | 11-08 | 5 | REQ-P11-06 | T-11-32 | `--check` exits 1 with `D-24:` naming the entry | unit | `python -m unittest tests.test_gen_finding_catalogue.TestFamiliesCitationGate` | ✅ | ✅ green |
| D4 | 11-08 | 5 | REQ-P11-06 | T-11-33 | D-05 enforcement live for `DSX-ADM-`, proven by removal | unit | `python -m unittest tests.test_gen_finding_catalogue.TestDsxAdmAllowlistEntry` | ✅ | ✅ green |
| D5 | 11-08 | 5 | REQ-P11-06 | — | No gate exit code moves; full suite green | unit + other | `python -m unittest discover -s tests` | ✅ | ✅ green |
| G1 | validate-phase | — | REQ-P11-02 | T-11-19 | No approximate-matching machinery in `admissibility.py` (D-18) | unit | `python -m unittest tests.test_frame_boundary.TestFrameApproximateMatchingBoundary` | ✅ | ✅ green |
| G2 | validate-phase | — | REQ-P11-05 | T-11-29 | `recommend-test` pinned to a recorded pre-phase baseline | integration | `python -m unittest tests.test_dsx.TestAdmissibilityRecommendComposition` | ✅ | ✅ green |

Status legend: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky. `⚠️ human` marks a row whose automated
half is green but which also carries an open human-judgement item — see Manual-Only below.

### Requirement → test map

| Req ID | Behavior | Test Type | Automated Command | File Exists |
|--------|----------|-----------|-------------------|-------------|
| REQ-P11-01 | `families.yaml` parses identically through both loader paths (D-08) | unit | `python -m unittest tests.test_families_yaml` | ✅ |
| REQ-P11-01 | Every family entry declares a resolving `traceability` value (SC 5, D-01) — see amendment note below | unit | `python -m unittest tests.test_families_yaml.TestFamiliesYamlTraceability` | ✅ |
| REQ-P11-02 | Alias resolution is exact-match, never fuzzy — behavioural (D-18) | unit | `python -m unittest tests.test_frame_admissibility.TestResolveDeclaredProcedure` | ✅ |
| REQ-P11-02 | Alias resolution is exact-match, never fuzzy — mechanical source scan (D-18) | unit | `python -m unittest tests.test_frame_boundary.TestFrameApproximateMatchingBoundary` | ✅ **new** |
| REQ-P11-03 | Ranked admissible set names assumptions bought and charged | unit | `python -m unittest tests.test_frame_admissibility.TestRankAdmissible` | ✅ |
| REQ-P11-04 | Underdetermined frame → `DSX-ADM-020`, exit 1 at CRITICAL (D-16, D-21) | integration | `python -m unittest tests.test_dsx.TestAdmissibilityGateRegistration` | ✅ |
| REQ-P11-05 | `cmd_recommend` output is additive; no-flag output is working-directory independent (D-04) | integration | `python -m unittest tests.test_dsx.TestAdmissibilityRecommendComposition` | ✅ |
| REQ-P11-05 | No-flag output pinned byte-for-byte to the recorded pre-phase baseline | integration | `python -m unittest tests.test_dsx.TestAdmissibilityRecommendComposition` | ✅ **new** |
| REQ-P11-06 | An uncited family fails the build check (D-23, D-24, D-25) | unit | `python -m unittest tests.test_gen_finding_catalogue` | ✅ |
| SC 5 | No ontology entry declares a Bayesian inference method | unit | `python -m unittest tests.test_families_yaml` | ✅ |
| regression | Good fixture passes every gate; bad fixtures block at their gate points | regression | `python -m unittest tests.test_known_bad_corpus` | ✅ |
| regression | D-03a, D-11 and D-04a boundary scanners pass against the new module | regression | `python -m unittest tests.test_frame_boundary` | ✅ |

**Amendment, 2026-08-23 — REQ-P11-01 row 2.** This row previously read *"Every family entry traces
to a committed fixture"*, specified as an integration test asserting each family `id` is exercised
by at least one committed spec. **That is not what shipped, and it could not have shipped:** the
roster holds 14 families against 9 committed specs, and two families
(`two_proportion_z_always_valid`, `ratio_of_means_delta_method`) exist to cover D-01 operating
contexts no fixture declares. Plan 11-04 built the honest weaker form instead —
`test_every_family_traceability_resolves` requires every family to declare a non-blank
`traceability` resolving to exactly one of three permitted forms, and fails loudly on any fourth
form. Measured distribution across the 14 entries: **4** `spec:<path>` (file existence asserted),
**8** `ranking_rule:<id>` (rule existence asserted), **2** `operating_context:<cluster>` (cluster
membership asserted). The row above now describes the shipped check. The original wording was a
planning-time overstatement, not a coverage gap.

---

## Manual-Only Verifications

These four are tracked live in [11-UAT.md](11-UAT.md), all `result: [pending]`. They are the
reason `nyquist_compliant: true` is a statement about *automated coverage of automatable
behaviour* — not a claim that the phase needs no human read.

| # | Behavior | Requirement | Threat Ref | Why Manual | Test Instructions |
|---|----------|-------------|------------|------------|-------------------|
| 1 | Each family's `citation:` names a real primary source that actually supports the family, and `locator_status` is honest | REQ-P11-06, D-09 | T-11-13, T-11-14 (residual accepted: AR-02, AR-03) | A test can assert a citation string is non-blank and well-formed. It cannot assert the paper says what the entry claims. This is the D-05 judgement the project exists to protect. | For each of the 14 family entries, open the cited source and confirm (a) the locator resolves, (b) the source supports this estimator family, (c) `locator_status` matches whether the chapter or page was actually confirmed. Mark unconfirmed locators `unverified` rather than guessing. Current split: 4 verified, 10 unverified. |
| 2 | The four ranking orderings in D-13 are stated at the strength their sources support | REQ-P11-03, D-12 | T-11-22 (residual accepted: AR-04) | Only a reader can tell a uniform domination from a hedged reliability ordering. The Lydersen result is uniform; the MacKinnon one is hedged by its own authors and fails with few treated clusters. | Read each `DSX-ADM-010` message against its cited source and confirm it does not overstate. Only `boschloo_over_fishers_exact` is tagged `uniform_domination`. Confirm the Delacre 2022 Correction and the Pustejovsky & Tipton 2023 Corrigendum have been checked before any number from those two papers is used (D-26). |
| 3 | `references/test-selection.md`'s corrected Fisher rule reads correctly to a practitioner | REQ-P11-01, D-27 | T-11-02 (residual accepted: AR-01) | Correctness of the replacement wording is an editorial judgement, not a parse. | Read the amended row and confirm it no longer prescribes Fisher's exact as the small-cell fallback, and that the replacement carries its Lydersen §9 citation. |
| 4 | `brief.md`'s two D-29 locators read at the strength the evidence supports | REQ-P11-01, D-29 | T-11-02 (residual accepted: AR-01) | 11-01-PLAN.md Task 3's own `<human-check>` requires this read; 11-01-SUMMARY.md records `human_judgment: true` without recording that the read was performed. | Confirm the Kohavi, Tang & Xu locator reads as verified (Ch. 22, pp. 226-234), and that the Cameron & Miller Section VI locator reads as manuscript-verified with the Section VIII-to-XI typeset-numbering caveat intact and unambiguous. |

Row 4 was absent from this table before 2026-08-23 despite being tracked in 11-UAT.md as test 4;
added by this validation pass.

---

## Validation Audit 2026-08-23

| Metric | Count |
|--------|-------|
| Requirement rows audited | 12 |
| COVERED at audit | 10 |
| Gaps found | 2 |
| Resolved | 2 |
| Escalated | 0 |
| Manual-only (unchanged, all open) | 4 |
| Documentation corrections | 2 |

**Gaps found and closed:**

- **G1 — REQ-P11-02 / D-18 had no mechanical scanner.** Behaviour was covered by
  `test_near_miss_variants_of_a_real_alias_are_unresolved` (a bare prefix and two edit-variants of
  `welch_t`, all asserted `unresolved`), but the "no approximate match anywhere in the module"
  guarantee existed only as prose in the module docstring. This project's convention is that a
  load-bearing prohibition gets a source scanner — D-03a/D-04a and D-11 both have one in
  `tests/test_frame_boundary.py`; D-18 did not. Added `_scan_source_for_approx_matching()` and
  `TestFrameApproximateMatchingBoundary` (10 tests) in that same file. The scanner detects difflib
  imports and attribute access, calls to `get_close_matches`/`SequenceMatcher`/`ratio`/
  `quick_ratio`/`real_quick_ratio`, and prefix/suffix matching via `startswith`/`endswith`. It
  deliberately does **not** flag the `in` operator: an AST walker cannot separate a legitimate
  alias-index lookup from a substring check without dataflow analysis, and a scanner that cries
  wolf on the module's own lookups would be deleted by the next maintainer. That direction stays
  covered behaviourally.
  **Proven to fire, not merely to pass:** temporarily appending
  `return alias.startswith(declared)` to `dsx/frame/admissibility.py` made the boundary suite exit
  1 with `line 991: calls 'startswith' (prefix/suffix matching is not exact match)`; reverting
  restored exit 0 with `git diff` clean. Three violating source strings and three permitted
  controls are committed as tests.

- **G2 — REQ-P11-05 was not pinned to a baseline.** The shipped
  `test_no_spec_output_is_byte_identical_regardless_of_working_directory` runs the command from two
  working directories and compares the runs *to each other*, then asserts the key list. That proves
  working-directory independence and key-shape stability but not value stability: an edit to
  `recommend_test()`'s `rationale` would change both runs together and still pass. Added
  `test_no_spec_proportion_groups_2_output_is_pinned_to_recorded_baseline` to the existing
  `TestAdmissibilityRecommendComposition`, asserting exact value equality *and* key insertion order
  against a literal recorded baseline. The baseline is trustworthy because
  `git diff v1.4.0 HEAD --stat -- dsx/checks/stats.py` is empty — `recommend_test()` has never
  changed, so today's output *is* the pre-phase output. (There is no `v1.5.0` tag in this
  repository; v1.4.0 is the nearest tagged ancestor and bounds the claim more tightly than v1.5.0
  would.)

**Documentation corrections:** REQ-P11-01 row 2 rewritten to describe the check that shipped (see
amendment note above); Manual-Only row 4 added to match 11-UAT.md.

**Constraints honoured:** no implementation file was modified — `git status --porcelain` after the
pass shows only `tests/test_dsx.py` and `tests/test_frame_boundary.py`. No existing test was
deleted, weakened, renamed or reordered. `tests/test_known_bad_corpus.py` untouched.

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references — all four Wave 0 files exist and are green:
      `tests/test_families_yaml.py` (28), `tests/test_frame_admissibility.py` (73),
      `tests/test_gen_finding_catalogue.py` (40), `tests/test_frame_boundary.py` (20)
- [x] No watch-mode flags
- [x] Feedback latency < 1 s per task (0.113 s), < 45 s per wave (44.2 s)
- [x] `nyquist_compliant: true` set in frontmatter
- [x] Full suite green at sign-off: 1028 tests, OK
- [x] `python scripts/gen-finding-catalogue.py --check` exit 0

**Approval:** validated 2026-08-23 by `/gsd-validate-phase 11`.

**Scope of this approval:** every automatable requirement behaviour in Phase 11 has automated
verification that has been run and observed green. The four Manual-Only items above remain open
and are *not* covered by this sign-off — they are citation-authenticity and wording-honesty reads
that no parser can perform, tracked in 11-UAT.md and carried as accepted residual risk AR-01
through AR-04 in 11-SECURITY.md.
