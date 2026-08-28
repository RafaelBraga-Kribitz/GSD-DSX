---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 12
subsystem: known-bad-corpus-docs
tags: [gap-closure, known-bad-corpus, gate-behaviour, corpus-completeness, d-06, req-p6-13]

# Dependency graph
requires:
  - phase: 06-08
    provides: "the three examples/known-bad/ spec+post-mortem pairs and tests/test_known_bad_corpus.py this plan corrects and extends"
  - phase: 06-10
    provides: "06-VERIFICATION.md / 06-REVIEW.md's reproduced finding (CR-02 / Truth 5) that the corpus's committed gate-behaviour claim is false"
provides:
  - "A gate-level test suite (tests/test_known_bad_corpus.py) that drives dsx gate at all four points against every corpus fixture and asserts the corpus's real, measured guarantee — not just dsx validate"
  - "Corrected header/post-mortem prose across the three known-bad fixtures that states exactly what today's gates do and do not clear, and why"
  - "A retired-over-claim regression guard that fails if either false claim is reintroduced"
affects: [08, 09, 12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "_gate_findings() helper drives cli.main([\"gate\", point, \"--spec\", ..., \"--phase-dir\", tmp, \"--json\"]) against a fresh tempfile.TemporaryDirectory() per call, keeping the DECISIONS.jsonl trail write out of examples/ — the same --phase-dir-redirection convention 06-09 established, reused here for the first time in a test that drives the CLI at every gate point rather than just dsx validate"
    - "Incidental-gap allow-lists are measured, not asserted from memory: run the real CLI first, record the emitted codes and severities, then write the constant and its per-code cause comment from that output — never reproduce a prior review's partial transcript"

key-files:
  created: []
  modified:
    - tests/test_known_bad_corpus.py
    - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
    - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
    - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
    - examples/known-bad/interference-shared-budget-POSTMORTEM.md

key-decisions:
  - "Corrected the claim rather than repairing the fixtures (the review's remedy (b)) — 06-08 already decided and committed that dsx validate at CRITICAL, not dsx gate ship, is this corpus's acceptance bar, and ROADMAP Success Criterion 5 is written to that bar; repairing five unrelated spec sections across three fixtures would change what each fixture declares (the one thing a known-bad fixture must not do casually) and move the acceptance bar as a side effect of a documentation fix"
  - "Whitespace-normalized the retired-over-claim substring match (text.split() rejoined with single spaces) after discovering the interference post-mortem's actual committed retired sentence has a mid-phrase line-wrap (\"passes\\nevery gate\") that a literal, un-normalized substring check — and even `grep` without -z — would silently miss; without this fix Task 1's RED state at commit ec93c53 would have looked green on the one file that most needed to fail"
  - "_INCIDENTAL_GAP_CODES lists 8 measured codes, not the 5 illustrative causes named in the plan's action text — the frequentist fixture blocks additionally on DSX-EXP-007 (MDE exceeds decision.minimum_practical_effect) and the bayesian fixture additionally on DSX-REP-001 (stochastic method, no random_seed) and DSX-STA-041 (declared test outside the stats recommendation engine's acceptable set); the plan explicitly instructed measuring rather than reusing the review's interference-only transcript, and these three codes only appear on the other two fixtures"
  - "_TARGET_CODE_FAMILIES uses the prefix \"DSX-PAR-01\" rather than \"DSX-PAR-\" specifically so it does not also match the unrelated, already-shipped DSX-PAR-001 (INFO-severity paradigm manifest finding, REQ-P6-09) — DSX-PAR-001 is excluded from _INCIDENTAL_GAP_CODES anyway (it is INFO, not CRITICAL/HIGH), but the narrower prefix keeps the family boundary precise for any future incidental code that happens to start with DSX-PAR-00x"

patterns-established: []

requirements-completed: []

coverage:
  - id: G1
    description: "tests/test_known_bad_corpus.py gains _CRITICAL_THRESHOLD_POINTS, _INCIDENTAL_GAP_CODES, _TARGET_CODE_FAMILIES, _RETIRED_OVERCLAIMS module constants; _gate_findings() helper; and four new test methods (test_every_spec_passes_the_critical_threshold_gate_points, test_ship_gate_findings_are_all_documented_incidental_corpus_gaps, test_incidental_allowlist_names_no_target_family_code, test_no_corpus_file_repeats_a_retired_gate_overclaim) — the module now drives dsx gate at all four points against every fixture, closing the coverage gap CR-02 named (the module previously only ever ran dsx validate)"
    verification:
      - kind: unit
        ref: "python3 -m unittest tests.test_known_bad_corpus -v (10 tests, all pass)"
        status: pass
      - kind: other
        ref: "git diff --stat examples/ dsx/ scripts/ at the test(06-12) commit shows only tests/test_known_bad_corpus.py changed"
        status: pass
    human_judgment: false
  - id: G2
    description: "All three *-ANALYSIS-SPEC.yaml header comments and the interference POSTMORTEM.md's closing clause corrected to state the measured gate guarantee — structurally valid; dsx validate and both CRITICAL-threshold points (plan, execute) exit 0; verify/ship currently exit 1 on named, per-fixture corpus-completeness gaps; no code in this repository adjudicates the documented target defect today"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus.test_no_corpus_file_repeats_a_retired_gate_overclaim (RED at test(06-12), GREEN at docs(06-12))"
        status: pass
      - kind: other
        ref: "git diff -U0 examples/known-bad/ at the docs(06-12) commit — every changed line is inside a comment block (YAML) or prose (POSTMORTEM.md); no spec_version/validity_frame/inference/design/claims/metrics/assumptions line added, removed or altered"
        status: pass
    human_judgment: false
  - id: G3
    description: "The fixtures' encoded defects, declared field values and finding-code attributions are byte-for-byte unchanged"
    verification:
      - kind: other
        ref: "python3 -m dsx validate --spec <each fixture> exits 0 with zero findings at any severity, matching 06-08's original measurement"
        status: pass
    human_judgment: false

duration: ~35min
completed: 2026-08-08
status: complete
---

# Phase 6 Plan 12: Correct the known-bad corpus's gate-behaviour claim Summary

**Rewrote a false, committed claim that today's `dsx validate`/`gate` checks pass all three `examples/known-bad/` fixtures at every gate and severity threshold, and pinned the corrected claim with four new gate-driving tests measured directly against the real CLI.**

## Performance

- **Duration:** ~35 min
- **Completed:** 2026-08-08
- **Tasks:** 2
- **Files modified:** 5 (1 test module, 3 fixture headers, 1 post-mortem)

## Accomplishments

- `tests/test_known_bad_corpus.py` now drives the real `dsx gate` at all four points (`plan`, `execute`, `verify`, `ship`) against every corpus fixture, closing the coverage gap CR-02/Truth-5 named: the module previously only ever ran `dsx validate`.
- Measured, not guessed: `dsx gate {plan,execute,verify,ship} --json` was run in-process against all three committed fixtures before any assertion was written. The full measured table:

  | fixture | plan | execute | verify | ship | ship CRITICAL/HIGH codes |
  |---|---|---|---|---|---|
  | interference-shared-budget | exit=0 | exit=0 | exit=1 | exit=1 | DSX-CLM-031, DSX-COH-031, DSX-MET-040, DSX-NAR-001, DSX-REP-030 |
  | frequentist-uncontrolled-continuous | exit=0 | exit=0 | exit=1 | exit=1 | DSX-EXP-007, DSX-CLM-031, DSX-COH-031, DSX-MET-040, DSX-NAR-001, DSX-REP-030 |
  | bayesian-continuous-monitoring | exit=0 | exit=0 | exit=1 | exit=1 | DSX-STA-041, DSX-CLM-031, DSX-COH-031, DSX-MET-040, DSX-NAR-001, DSX-REP-001, DSX-REP-030 |

  Union across all three (`_INCIDENTAL_GAP_CODES`, 8 codes): `DSX-CLM-031`, `DSX-COH-031`, `DSX-EXP-007`, `DSX-MET-040`, `DSX-NAR-001`, `DSX-REP-001`, `DSX-REP-030`, `DSX-STA-041`. Every fixture's ship-point INFO/MEDIUM/LOW findings (`DSX-EXP-031`, `DSX-EXP-040`, `DSX-STA-042`, `DSX-REP-010`, `DSX-REP-011`, `DSX-PAR-001`) are below the allow-list's severity floor and excluded by construction.
- Four new tests pin this measurement mechanically:
  - `test_every_spec_passes_the_critical_threshold_gate_points` — the positive half of the claim ROADMAP Success Criterion 5 depends on: every fixture clears `plan` and `execute` (both CRITICAL-threshold).
  - `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` — every CRITICAL/HIGH finding at `ship` is a member of `_INCIDENTAL_GAP_CODES`; its docstring records that this test going RED after a later phase ships a new check (e.g. `DSX-INT-010`, `DSX-PAR-010`, `DSX-PAR-011`) is the intended signal, not a defect.
  - `test_incidental_allowlist_names_no_target_family_code` — no allow-listed code starts with `DSX-INT-` or `DSX-PAR-01`, the machine-checkable form of "no code in this repository catches the documented defect today."
  - `test_no_corpus_file_repeats_a_retired_gate_overclaim` — asserts neither retired substring (`"validate/gate checks pass it"`, `"passes every gate"`) appears anywhere under `examples/known-bad/`, matched against whitespace-normalized text (see Deviations — the postmortem's actual retired sentence has a mid-phrase line-wrap that a raw substring check would miss).
- All three fixture headers and the interference post-mortem's "Which absent code would have caught it" closing clause rewritten to state exactly what is true: structurally valid; `dsx validate` and both CRITICAL-threshold gate points exit 0; `dsx gate verify`/`dsx gate ship` currently exit 1 on the fixture's own named corpus-completeness gaps (per-fixture, not the interference fixture's list copy-pasted across all three); no code in this repository adjudicates the documented target defect today.
- Confirmed at the final commit: `git diff -U0 examples/known-bad/` touches only comment lines in the three YAML files and prose in the post-mortem — no `spec_version`, `validity_frame`, `inference`, `design`, `claims`, `metrics` or `assumptions` line was added, removed or altered. `dsx validate --spec <each fixture>` still exits 0 with zero findings at any severity, matching 06-08's original measurement exactly.
- Full suite: 274/274 passing (264 pre-existing + 10 in `test_known_bad_corpus`, up from 6). `python3 scripts/gen-finding-catalogue.py --check` exits 0 — no finding code added or touched. `git diff --stat dsx/ scripts/` is empty across both commits.

## Task Commits

1. **Task 1: Measure the corpus's real gate behaviour and pin it with tests** — `ec93c53` (test) — RED as designed: `test_no_corpus_file_repeats_a_retired_gate_overclaim` failed on 4 subTests (the 3 fixture headers plus the interference post-mortem) pending Task 2; the three other new tests and all five pre-existing tests passed unmodified against the fixtures as committed.
2. **Task 2: Rewrite the four false claims to state what the corpus actually guarantees** — `362ba6b` (docs) — GREEN: all 10 tests in the module pass, full suite 274/274.

## Files Created/Modified

- `tests/test_known_bad_corpus.py` — modified: 4 new module constants, `_gate_findings()` helper, 4 new test methods (6 → 10 tests total)
- `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` — modified: header comment block only
- `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` — modified: header comment block only
- `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` — modified: header comment block only (T-6-17 formulation note left untouched)
- `examples/known-bad/interference-shared-budget-POSTMORTEM.md` — modified: "Which absent code would have caught it" closing clause only

## Decisions Made

- **Corrected the claim, did not repair the fixtures.** The review offered two remedies; this plan takes only the documentation-correction one, per 06-08's already-committed decision that `dsx validate` (CRITICAL) is the corpus's acceptance bar, not `dsx gate ship`. See `key-decisions` in frontmatter for the full reasoning, restated from the plan's own action text.
- **Whitespace-normalized the retired-overclaim test.** The interference post-mortem's committed sentence wraps as `"...fixture passes\nevery gate at every severity..."` — a literal substring check for `"passes every gate"` (and even a default, non-`-z` `grep`) does not match text split by a newline. `test_no_corpus_file_repeats_a_retired_gate_overclaim` was fixed to compare against `" ".join(text.split())` before checking membership, so a cosmetic line-wrap can never hide a reintroduced claim. Caught during Task 1's own RED verification — see Deviations below.
- **Measured 8 incidental codes, not the plan's 5 illustrative ones.** The plan's action text names five example causes (no narrative path, no reproducibility entrypoint, unresolved evidence pointer, unwaived assumption, warehouse metric with no SQL). The actual measured union across all three fixtures also includes `DSX-EXP-007` (frequentist fixture's MDE exceeds its declared minimum practical effect) and `DSX-REP-001`/`DSX-STA-041` (bayesian fixture: no random seed for a stochastic method; declared test outside the stats recommendation engine's acceptable set for the outcome shape). All three are named-by-code in the corrected headers and comment-documented in the test module.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 — bug] Retired-overclaim substring check missed the post-mortem's actual retired sentence due to a mid-phrase line-wrap**
- **Found during:** Task 1, verifying the expected RED state before committing.
- **Issue:** `_RETIRED_OVERCLAIMS = ("validate/gate checks pass it", "passes every gate")` matched against raw `path.read_text()` correctly caught the three fixture headers (all three contain `"validate/gate checks pass it"` on one unbroken comment line) but did not flag `interference-shared-budget-POSTMORTEM.md`, whose committed sentence is `"...fixture passes\nevery gate at every severity..."` — the retired phrase is split across a markdown soft-wrap. An un-normalized substring check silently produced a false negative on the one file most central to the finding CR-02 named.
- **Fix:** Changed the comparison in `test_no_corpus_file_repeats_a_retired_gate_overclaim` to whitespace-normalize each file's text (`" ".join(text.read_text(...).split())`) before checking substring membership, and documented the reason in the test's docstring.
- **Files modified:** `tests/test_known_bad_corpus.py`
- **Commit:** `ec93c53` (folded into the Task 1 commit — caught before that commit landed, not as a follow-up fix)

**2. [Rule 1 — bug] A comment line-wrap in the bayesian fixture's corrected header split the literal string "dsx gate verify" across two lines**
- **Found during:** Task 2, running the plan's acceptance-criteria grep for `"dsx gate verify"` against all three headers before committing.
- **Issue:** The first draft of the bayesian header's corrected prose wrapped as `"...also blocks dsx gate\n# verify and dsx gate ship..."`, so a plain-text (non-normalized) grep for the contiguous phrase `"dsx gate verify"` — the exact form the plan's acceptance criteria and this corpus's other two headers use — found only 2 of the 3 fixtures.
- **Fix:** Re-wrapped the sentence so `"dsx gate verify"` stays on one line, matching the other two headers' phrasing exactly.
- **Files modified:** `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml`
- **Commit:** `362ba6b` (fixed before the Task 2 commit landed)

---

**Total deviations:** 2 auto-fixed (Rule 1), both caught by running this plan's own acceptance-criteria checks before committing rather than after. Zero impact on the committed result — both are corrected in the commits described above, not as separate follow-up commits.

## Issues Encountered

None beyond the two deviations above, both self-caught during verification.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phases 7, 8, 9 and 11 authors now have a mechanically enforced, true baseline to build regression tests against: every corpus fixture clears `plan`/`execute` today, and `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` will go RED the moment a new phase's code (e.g. `DSX-INT-010`, `DSX-PAR-010`, `DSX-PAR-011`) starts firing against its target fixture — which is the designed signal to move that code from `_INCIDENTAL_GAP_CODES` to "caught" in both the test module and the fixture's header/post-mortem prose.
- No blockers for parallel plans 06-11/06-13 — this plan touched only `tests/test_known_bad_corpus.py` and the four `examples/known-bad/` files named in its frontmatter; `git diff --stat dsx/ scripts/ tests/test_dsx.py tests/test_decisions.py tests/test_gen_finding_catalogue.py tests/test_frame_boundary.py` is empty across both commits.
- No new finding code minted, no check module touched, no third-party dependency introduced — `python3 scripts/gen-finding-catalogue.py --check` and the full 274-test suite both exit 0 at the final commit.

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*

## Self-Check: PASSED

- FOUND: tests/test_known_bad_corpus.py
- FOUND: examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/interference-shared-budget-POSTMORTEM.md
- FOUND: .planning/phases/06-contract-extension-decision-record-paradigm-manifest/06-12-SUMMARY.md
- FOUND commit: ec93c53 (test(06-12): pin the known-bad corpus's real gate behaviour)
- FOUND commit: 362ba6b (docs(06-12): state the known-bad corpus's real gate guarantee)
