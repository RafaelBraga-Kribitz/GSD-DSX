---
phase: 8
slug: interference-triggering-stability-dsx-int
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-12
validated: 2026-08-14
---

# Phase 8 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `08-RESEARCH.md` § Validation Architecture. Audited against the
> executed tree on 2026-08-14 — every command below was run, not inferred.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python standard-library `unittest` — no pytest, no config file (re-confirmed 2026-08-14: no `pytest.ini`, `pyproject.toml`, `setup.cfg` or `tox.ini` on disk) |
| **Config file** | none |
| **Interpreter** | `python` (3.12.10). **Not `python3`** — see the interpreter note below |
| **Quick run command** | `python -m unittest tests.test_frame_interference -v` (64 tests, ~2s) |
| **Full suite command** | `python -m unittest discover -s tests -v` |
| **Measured runtime** | 2s quick, 9.8s full — 543 tests, `OK`, 0 failures, 0 skips |

**Interpreter note (found during the 2026-08-14 audit).** On this machine `python3` resolves to
a *different* interpreter from `python`: `python3` is the Windows Store build at 3.14.6 with no
PyYAML installed, `python` is 3.12.10 with PyYAML present. Both run all 543 tests and both pass,
but under `python3` two PyYAML-differential loader tests
(`test_dsx.TestLoader.test_bare_none_matches_pyyaml` and
`test_bundled_parser_matches_pyyaml_when_available`) silently skip — the run reports
`OK (skipped=2)` rather than `OK`. Neither test is a Phase 8 requirement, so this is not a
Phase 8 coverage gap, but every command in this document has been rewritten to `python` so the
recorded sampling rate is the one that actually exercises the whole suite.
`scripts/check.sh` still calls `python3` at lines 7, 10 and 13 and so reports `OK (skipped=2)`;
it passes either way (`all checks passed`, verified 2026-08-14), but a run of `check.sh` alone
does not prove the two PyYAML-differential tests green.

**Second gate, not optional.** Any commit that adds a `report.add("DSX-INT-…")` call must also
pass `python scripts/gen-finding-catalogue.py --check`. That script enforces decision D-05 — the
citation marker, the reference value or structural criterion, and the linked `# D-05: <CODE>`
test marker. It is a build script, not the gate path, so it may read `tests/`.
**Verified 2026-08-14:** exit 0, "finding catalogue is current". All four `DSX-INT-*` codes
carry a D-05 marker — `DSX-INT-010` at `tests/test_frame_interference.py:97`, `DSX-INT-011` at
`:124`, `DSX-INT-030` at `:361` and `tests/test_dsx.py:152,163`, `DSX-INT-040` at `:834`.

---

## Sampling Rate

- **After every task commit:** targeted class-scoped run from the Per-Task Map below, plus
  `python scripts/gen-finding-catalogue.py --check` once any `DSX-INT-*` code exists.
- **After every plan wave:** `python -m unittest discover -s tests -v`
- **Before `/gsd-verify-work`:** full suite green, catalogue check green, the known-bad corpus
  rewrite landed, and the `interference-shared-budget` second-code collision resolved.
- **Max feedback latency:** 30 seconds — **measured 9.8s** for the full suite.

**Commands are class-scoped, not `-k`-scoped.** The seeded version of this document used `-k`
substring filters. The audit found they under-sample: `-k risk` selects 9 of the 64 interference
tests and misses `test_shared_budget_no_mitigation_blank_residual_produces_critical_int_010`,
the canonical positive test for `DSX-INT-010`; `-k triggering` selects 3 of
`TestTriggeringDilution`'s 19. Every row below now names the test class, so the quick command
cannot drift away from the requirement it claims to sample.

---

## Per-Task Verification Map

All statuses below were produced by running the command in the row on 2026-08-14, not by
reading a summary. Counts are the tests each command actually selects.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | Selects | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|---------|--------|
| 08-03 T1 · 08-07 T1/T2 · 08-08 T1 · 08-10 T1 | 08-03, 08-07, 08-08, 08-10 | 2, 6–9 | REQ-P8-01 | T-8-01, T-8-08 | Malformed `interference` sub-block degrades to no finding, never a crash; an out-of-vocabulary `risk` **or** `mitigation` is treated as absent rather than bypassing the check; the Kohavi citation claims only what was read | unit + gate-level (copy-mutate temp fixture) | `python -m unittest tests.test_frame_interference.TestInterferenceUnaddressed tests.test_frame_interference.TestInterferenceGateLevel -v` | 22 | ✅ green |
| 08-03 T1 · 08-07 T1 · 08-10 T1/T2 | 08-03, 08-07, 08-10 | 2, 6, 9 | REQ-P8-02 | T-8-08 | Cell-level admissibility is attributed to the structural criterion, not to the unread chapter; `DSX-INT-010` and `DSX-INT-011` are provably disjoint over the full risk × mitigation grid at both unit and gate level | unit, table-driven over `_RISK_MITIGATION_MAP` + 270-cell and 8-cell disjointness grids | `python -m unittest tests.test_frame_interference.TestRiskMitigationMap tests.test_frame_interference.TestInterferenceUnaddressed tests.test_frame_interference.TestInterferenceGateLevel -v` | 24 | ✅ green |
| 08-01 T1 · 08-04 T1 · 08-09 T1/T2 | 08-01, 08-04, 08-09 | 1, 3, 8 | REQ-P8-03 | T-8-03, T-8-04 | Dilution function raises on an out-of-range trigger rate rather than returning a plausible wrong number; an out-of-vocabulary `analysis_population` still fires `DSX-INT-030`; the `ANALYSIS_POPULATIONS` vocabulary is held by a contract test so a third member cannot silently widen what the code adjudicates | unit (`mathx`) + unit and gate-level (`interference.check`) | `python -m unittest tests.test_frame_interference.TestTriggeringDilution -v` and `python -m unittest tests.test_dsx.TestMath -k dilut -v` | 19 + 5 | ✅ green |
| 08-04 T1/T2 · 08-06 T1 · 08-07 T1 | 08-04, 08-06, 08-07 | 3, 5, 6 | REQ-P8-04 | T-8-11 | The section 6.5 entry condition cannot be softened without a red test; the scope-boundary test asserts the real additive/ratio partition and `diluted_effect`'s published reference pair rather than comparing two literals | unit + documentation-content test (`tests/test_known_bad_corpus.py:699-718`, pinning `brief.md` §6.5's "Formula (3)" per-user-data condition) | `python -m unittest tests.test_frame_interference.TestTriggeringDilution -k ratio_scope -v` and `python -m unittest tests.test_known_bad_corpus -v` | 2 + 22 | ✅ green |
| 08-05 T1/T2 | 08-05 | 4 | REQ-P8-05 | T-8-02, T-8-12, T-8-13 | Malformed `stability` sub-block degrades to no finding; severity alone selects the gate point and `GATE_THRESHOLDS` is provably unedited (`plan: CRITICAL`, `verify: HIGH` asserted at `tests/test_frame_interference.py:906-907`) | unit + gate-level severity pinning (HIGH, not CRITICAL) | `python -m unittest tests.test_frame_interference.TestStabilityAssessment -v` | 11 | ✅ green |
| 08-03 T2 | 08-03 | 2 | REQ-P8-06 | — | N/A | boundary scanner over `dsx/frame/*.py`, plus the named traceability test `test_interference_module_is_inside_the_paradigm_read_scan_and_clean` | `python -m unittest tests.test_frame_boundary -v` | 8 | ✅ green |
| 08-05 T2 | 08-05 | 4 | (cross-cutting) | T-8-01, T-8-02 | Twenty-five malformed shapes across four sub-blocks raise nothing and find nothing; no exception handler exists in the module | unit sweep + abstract-syntax-tree assertion | `python -m unittest tests.test_frame_interference.TestModuleHardenedAgainstMalformedShapes tests.test_frame_interference.TestMalformedShapesDegradeGracefully -v` | 6 | ✅ green |
| 08-03 T2 · 08-04 T1 | 08-03, 08-04 | 2, 3 | (cross-cutting) | — | Every `DSX-INT-*` code is reachable from a gate profile and `interference` is registered in `plan`/`verify`/`ship` but absent from `execute` | unit, registration contract | `python -m unittest tests.test_frame_interference.TestGateRegistration tests.test_frame_interference.TestNeedsCausalBlock -v` | 4 | ✅ green |
| 08-02 T1/T2/T3 · 08-06 T1 · 08-07 T3 | 08-02, 08-06, 08-07 | 1, 5, 6 | (corpus integrity) | — | A fixture's own encoded defect cannot be laundered into the incidental allow-list; `_TARGET_DEFECT_CODES` cannot name a fixture absent from disk; the `weak-identification-mmm` block at verify and ship is asserted, not prose | unit, corpus contract | `python -m unittest tests.test_known_bad_corpus -v` | 22 | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

**REQ-P8-06's ordering question resolved as recorded.** `dsx/frame/val.py` is on disk, `dsx/cli.py`
imports and registers `val` in `CHECKS` and in the `plan`, `verify` and `ship` profiles, and
`tests/test_frame_boundary.py` contains `TestFrameParadigmReadBoundary` with a text detector, an
abstract-syntax-tree detector, a `FRAME_DIR.rglob("*.py")` scan and `paradigm.py` excluded by
name. Plan `08-03` Task 2 took the expected branch: it added
`test_interference_module_is_inside_the_paradigm_read_scan_and_clean` (confirmed present at
`tests/test_frame_boundary.py:252`) rather than writing the scanner. The contingency branch was
not needed.

---

## Wave 0 Requirements

- [x] `tests/test_frame_interference.py` — 64 tests across 9 classes. Created by plan `08-03`
      Task 1 (REQ-P8-01, REQ-P8-02); extended by `08-04` Task 1 (REQ-P8-03, REQ-P8-04), `08-05`
      Tasks 1 and 2 (REQ-P8-05 and the malformed-shape sweep), and the gap-closure plans
      `08-07`, `08-08`, `08-09` and `08-10`.
- [x] A dilution function in `dsx/mathx.py` plus its reference-value test in the existing
      `TestMath` class — `diluted_effect` at `dsx/mathx.py:479`, five tests at
      `tests/test_dsx.py:153-188`.
- [x] The per-fixture rewrite of `tests/test_known_bad_corpus.py` — landed as the two-map D-15
      structure: `_TARGET_DEFECT_CODES` (point-scoped, line 134) and `_EXPECTED_CAUGHT_DEFECTS`
      (set-scoped, line 278), with `_INCIDENTAL_GAP_CODES` (line 61) guarded so a fixture's own
      target code can never be laundered into the allow-list.
- [x] `examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml` and its post-mortem — both on
      disk.
- [x] The paradigm-read scanner in `tests/test_frame_boundary.py` — already existed from Phase 7;
      plan `08-03` Task 2 added the named traceability test.
- [x] Honest `stability` declarations on all three pre-existing corpus fixtures — plan `08-02`
      Task 1. All five `examples/known-bad/*-ANALYSIS-SPEC.yaml` fixtures declare `stability`.

**`interference-shared-budget` second-code collision: resolved.**
`_TARGET_DEFECT_CODES["interference-shared-budget"] = {"plan": "DSX-INT-010"}` with
`_EXPECTED_CAUGHT_DEFECTS["interference-shared-budget"] = frozenset()`. The fixture's target
code is scoped to one gate point rather than excluded by family prefix, and
`test_incidental_allowlist_names_no_slugs_own_target_code` is green.

No framework install is needed — `unittest` is standard library, consistent with the stdlib-only
constraint (D-01). PyYAML is optional and only affects two differential loader tests outside
this phase.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| The risk→mitigation admissibility cells are defensible under the structural criterion | REQ-P8-02 | The criterion — a mitigation is admissible only where it operates on the same interference channel the risk names — is a judgement about meaning. A test can assert the map's keys match the vocabulary and that specific cells hold; it cannot assert the reasoning is sound. | Read each cell's one-line channel justification in `dsx/frame/interference.py` against the mitigation descriptions at `dsx/spec.py:211-218`. Confirm the docstring says the table is derived from the criterion and is not quoted from Kohavi Ch. 22. |
| The Kohavi Ch. 22 citation claims only what was verified | REQ-P8-01, REQ-P8-02 | The chapter's running text is unreachable (paywall plus HTTP 429). Only the technique names and page numbers were verified, from the publisher's index. | Confirm the docstring cites pp. 230-233 for the *existence and naming* of the technique set only, and that no cell-level admissibility claim is attributed to the book. |
| The `brief.md` §6.5 entry condition names the real blocker | REQ-P8-04 | Whether an entry condition is falsifiable is a human judgement. The automated half only asserts the row exists and contains "Formula (3)". | Confirm the row names the per-user-data requirement, not "obtained from primary source" — that premise was verified false, since the paper is freely public. |

---

## Audit Findings Outside the Validation Lane

Both were found while auditing coverage on 2026-08-14. Neither is a Phase 8 requirement gap, and
neither is fixed by generating a test — recorded here so they are not lost.

| Ref | Finding | Why no test was generated | Route |
|-----|---------|---------------------------|-------|
| `08-REVIEW.md` WR-01 | `DSX-INT-011`'s `remedy` string is self-contradictory when the risk is out-of-vocabulary: it renders as `Declare a mitigation admissible for 'shared_buget': (none admissible).` The two tests that drive this path assert the finding and its `where`, never the `remedy` text — so the message is genuinely uncovered. | Writing an assertion now would pin a string the review has already judged wrong. The remedy needs the empty-`admissible` branch first; the test belongs in the same commit as the fix. | `/gsd-code-review 08 --fix`, then extend `TestInterferenceUnaddressed` |
| `08-REVIEW.md` WR-02 | `dsx/frame/paradigm.py:219` — `as_number(get(spec, "design.alpha")) or 0.05` silently replaces an explicit `design.alpha: 0` with the default, because `0.0` is falsy. Affects `DSX-PAR-010`'s reference-value text only, never the fire/no-fire decision. Still unfixed in the working tree. | Phase 9 surface (`DSX-PAR-*`), not Phase 8. Fixing it changes finding text that Phase 9's own tests will pin. | Phase 9 / `/gsd-code-review --fix` |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies — 9/9 map rows green
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references — all six Wave 0 items confirmed on disk
- [x] No watch-mode flags — every command is a single-shot `unittest` invocation
- [x] Feedback latency < 30s — measured 9.8s full suite, ~2s quick
- [x] `python scripts/gen-finding-catalogue.py --check` green for all four new codes
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-08-14 — 6/6 requirements carry green automated verification.

---

## Validation Audit 2026-08-14

| Metric | Count |
|--------|-------|
| Requirements audited | 6 (REQ-P8-01 … REQ-P8-06) |
| COVERED | 6 |
| PARTIAL | 0 |
| MISSING | 0 |
| Gaps found | 3 (all documentation-accuracy, no test generation required) |
| Resolved | 3 |
| Escalated | 0 |
| Findings routed elsewhere | 2 (`08-REVIEW.md` WR-01, WR-02) |

**Gaps found and resolved in this audit:**

1. **Under-sampling quick commands.** Every `-k` substring filter in the seeded map selected a
   proper subset of the class that owns the requirement — `-k risk` missed the canonical
   `DSX-INT-010` positive test entirely. Replaced with class-scoped commands, each re-run and
   its selected-test count recorded in the map.
2. **Wrong interpreter recorded.** `python3` on this machine is a different build (3.14.6, no
   PyYAML) from `python` (3.12.10); the suite reports `OK (skipped=2)` under it. All commands
   rewritten to `python`, with the discrepancy documented under Test Infrastructure.
3. **Map predated the gap-closure waves.** Plans `08-07` through `08-10` added seven permanent
   tests (two out-of-vocabulary bypass regressions, two disjointness grids, a vocabulary
   contract test, an on-disk subset guard and a positive corpus gate assertion) that no map row
   named. Task IDs, waves and behaviors updated; two cross-cutting rows added for gate
   registration and corpus integrity.

**Evidence.** Full suite `python -m unittest discover -s tests`: 543 tests, `OK`, 0 failures,
0 skips, 9.8s. `python scripts/gen-finding-catalogue.py --check`: exit 0. Every command in the
Per-Task Verification Map executed individually; all green.
