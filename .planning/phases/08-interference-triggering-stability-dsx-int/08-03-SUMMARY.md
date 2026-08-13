---
phase: 08-interference-triggering-stability-dsx-int
plan: 03
subsystem: gate-checks
tags: [dsx-frame, interference, sutva, admissibility-map, decision-record, catalogue]
status: complete

# Dependency graph
requires:
  - phase: 06-contract-extension-decision-record-paradigm-manifest
    provides: "validity_frame.interference sub-block/vocabulary, dsx/frame/ package, the D-03a import boundary, the paradigm-read boundary scanner (07-03), dsx.spec._validate_validity_frame_shape's causal-block condition"
  - phase: 07-validity-frame-checks-dsx-val
    provides: "dsx/frame/val.py as the two-code-per-module template, the finding-catalogue D-05 allow-list precedent (DSX-VAL-)"
  - plan: 08-02
    provides: "_TARGET_DEFECT_CODES + _classify_target_defect() in tests/test_known_bad_corpus.py, the point-scoped single-code map shape this plan adds its one entry to"
provides:
  - "dsx/frame/interference.py: DSX-INT-010 (risk declared, no mitigation, no real residual note) and DSX-INT-011 (mitigation inadmissible for the declared risk), both CRITICAL, both gated on dsx.spec.needs_causal_block"
  - "dsx.spec.needs_causal_block(spec): the causal-block condition extracted to a module-level function, shared by _validate_validity_frame_shape and the new interference checks so the two can never disagree (D-16)"
  - "_RISK_MITIGATION_MAP: a five-risk x six-mitigation admissibility matrix keyed by every dsx.spec.INTERFERENCE_RISKS member, argued cell-by-cell from the structural criterion"
  - "'interference' registered in CHECKS and in the plan/verify/ship gate profiles, absent from execute (D-03)"
  - "DSX-INT prefix group in the finding catalogue; 'DSX-INT-' in the D-05 citation-enforcement allow-list"
affects: [08-04-triggering-dilution-check, 08-05-stability-check, 08-06-phase-close-out]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Capability-matrix module constant (dict[str, frozenset[str]]) keyed by every vocabulary member, backed by a set-equality contract test — the _PARADIGM_CONDITIONAL/DEPENDENCE_ADMISSIBLE_METHODS idiom extended to a two-axis admissibility map"
    - "Shared gating condition extracted to a public dsx.spec function (needs_causal_block) rather than duplicated, so a shape validator and a semantic check can never drift apart on when a sub-block applies"
    - "Two disjoint-by-construction sibling codes (absence vs. presence of a declared value) proven disjoint by a single test rather than by suppression logic between them"

key-files:
  created:
    - dsx/frame/interference.py
    - tests/test_frame_interference.py
  modified:
    - dsx/spec.py
    - dsx/frame/paradigm.py
    - dsx/cli.py
    - scripts/gen-finding-catalogue.py
    - references/finding-codes.md
    - tests/test_frame_boundary.py
    - tests/test_known_bad_corpus.py
    - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
    - examples/known-bad/interference-shared-budget-POSTMORTEM.md

key-decisions:
  - "D-07's proposed five-cell mapping was reviewed and kept unchanged: cluster_randomisation admissible for marketplace/geo_spillover/social_graph/shared_inventory, inadmissible for shared_budget (the one cell ROADMAP success criterion 2 depends on); each cell's channel argument lives as an inline comment beside the cell it justifies"
  - "D-08 superseded as written: dsx.spec.is_placeholder_or_refusal() (Phase 7, 07-01) is reused for DSX-INT-010's residual_note check rather than adding a second is_placeholder() helper"
  - "Task 2 took Branch A (expected): tests/test_frame_boundary.py::TestFrameParadigmReadBoundary already existed from Phase 7's 07-03 (commits 3633222, c7800ef, 27f495d), so no new detector was written — only a named traceability test and an exclusion-set comment were added"
  - "Each of the two interference helpers appends exactly one DecisionRecord at its own judgment point (once a real, recognised risk is declared), whether or not its code fires — mirroring dsx/frame/paradigm.py's per-helper emission rather than val.py's outer-check emission, because the plan's action text specified this per-helper"

requirements-completed: [REQ-P8-01, REQ-P8-02, REQ-P8-06]

coverage:
  - id: D1
    description: "DSX-INT-010 fires on a declared interference risk with no mitigation and a blank/placeholder/refusal-token residual note; clears on a real residual note"
    requirement: REQ-P8-01
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestInterferenceUnaddressed (10 tests)"
        status: pass
      - kind: unit
        ref: "tests/test_frame_interference.py::TestInterferenceGateLevel (3 tests, copy-and-mutate against the committed fixture)"
        status: pass
    human_judgment: false
  - id: D2
    description: "DSX-INT-011 fires only when a declared mitigation is outside the admissible set for the declared risk; the two codes are proven disjoint (marketplace + cluster_randomisation fires nothing; shared_budget + cluster_randomisation fires DSX-INT-011 only)"
    requirement: REQ-P8-02
    verification:
      - kind: unit
        ref: "tests/test_frame_interference.py::TestInterferenceUnaddressed::test_inadmissible_mitigation_fires_int_011_not_int_010"
        status: pass
    human_judgment: false
  - id: D3
    description: "No code path in dsx/frame/interference.py reads the declared inference paradigm field, mechanically proven by the existing boundary scanner plus a new named traceability test, with the scanner shown to fail against a deliberate violation and the violation reverted"
    requirement: REQ-P8-06
    verification:
      - kind: unit
        ref: "tests/test_frame_boundary.py::TestFrameParadigmReadBoundary::test_interference_module_is_inside_the_paradigm_read_scan_and_clean"
        status: pass
    human_judgment: false
  - id: D4
    description: "Each of the five _RISK_MITIGATION_MAP cells is defensible under the structural criterion against each mitigation's own dsx/spec.py description"
    verification:
      - kind: human
        ref: "backstop must-have — argued in the module docstrings and inline cell comments; the Kohavi Chapter 22 citation claims only technique existence/naming, never a cell-level judgment"
        status: pass
    human_judgment: true

metrics:
  duration: 55min
  completed: 2026-08-13
---

# Phase 8 Plan 03: DSX-INT-010/011 interference gate module Summary

Shipped `dsx/frame/interference.py` with `DSX-INT-010` (a declared interference risk
with no mitigation and no honest residual note) and `DSX-INT-011` (a declared
mitigation that does not operate on the declared risk's channel), backed by a
five-risk admissibility map argued from the structural criterion, wired into the
plan/verify/ship gate profiles, and proven not to read the declared inference
paradigm.

## What was built

**Task 1 — the module, in one commit.** `dsx.spec.needs_causal_block(spec)` was
extracted out of `_validate_validity_frame_shape`'s local variable into a
module-level, publicly importable function (D-16), so the shape validator and the
new interference checks share one definition of "does this spec need the causal
`validity_frame` sub-blocks" and can never disagree. `dsx/frame/interference.py`
was created with `_RISK_MITIGATION_MAP` (a `dict[str, frozenset[str]]` keyed by
every `dsx.spec.INTERFERENCE_RISKS` member), two private check helpers
(`_check_interference_unaddressed` for DSX-INT-010, `_check_interference_mitigation_admissibility`
for DSX-INT-011), and a `check(spec)` dispatcher that returns an empty report when
`validity_frame` is absent or `needs_causal_block(spec)` is false. `dsx/cli.py`
registered `"interference"` in `CHECKS` and in the `plan`/`verify`/`ship` `GATE_PROFILES`
tuples, deliberately excluded from `execute` (D-03). `dsx/frame/paradigm.py`'s
`_NOT_SHIPPED` map dropped its now-false `"DSX-INT-"` entry.
`scripts/gen-finding-catalogue.py` gained a `DSX-INT` prefix group and
`"DSX-INT-"` in `_D05_ALLOWLIST_PREFIXES`; `references/finding-codes.md` was
regenerated. `tests/test_frame_interference.py` (new, 21 tests) covers all
fifteen behaviours the plan specified plus map-contract, registration,
malformed-shape and gate-level proofs. `tests/test_known_bad_corpus.py` gained
`"interference-shared-budget": {"plan": "DSX-INT-010"}` in `_TARGET_DEFECT_CODES`.

**Task 2 — the paradigm-read invariant, confirmed rather than written.**
`tests/test_frame_boundary.py::TestFrameParadigmReadBoundary` already existed
(Phase 7's 07-03, commits `3633222`, `c7800ef`, `27f495d`), scanning every file
under `dsx/frame/` by glob rather than a module list, so `interference.py` was
already covered the moment it existed. Branch A (expected) applied: no new
detector was written. Added a named test,
`test_interference_module_is_inside_the_paradigm_read_scan_and_clean`, proving
the file is in the glob's file list and clean under both detectors, plus a
comment on the exclusion set recording that the interference module is
deliberately *not* excluded (unlike `paradigm.py`, it adjudicates the frame
rather than describing what was declared). The deliberate-violation proof D-14
still owes was performed: a temporary `get(spec, "inference.paradigm")` read was
inserted into `dsx/frame/interference.py`, `python3 -m unittest tests.test_frame_boundary`
was run and observed to fail two tests with:

```
dsx\frame\interference.py (text): line 330: text contains 'inference.paradigm'
dsx\frame\interference.py (ast): line 330: call argument string literal 'inference.paradigm' names the inference block
```

The edit was reverted immediately after observing the failure; a byte-diff
against a pre-edit backup copy confirmed `dsx/frame/interference.py` was restored
exactly, and `git status --porcelain` showed it as untracked (`??`, unmodified
relative to Task 1's commit) throughout — no trace of the violation entered any
commit.

**Task 3 — fixture prose, rewritten to match the new gate reality.**
`examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml`'s header now
states the fixture blocks `dsx gate plan` with exit 1 naming `DSX-INT-010`, still
clears `dsx gate execute` (interference absent from that profile), still blocks
`verify`/`ship` on the five documented incidental gaps, and points at
`tests/test_known_bad_corpus.py`'s `_TARGET_DEFECT_CODES` map.
`examples/known-bad/interference-shared-budget-POSTMORTEM.md`'s "which absent code
would have caught it" section was retitled "which code catches it" and rewritten
in the present tense; the "why it was wrong" explanation was left untouched (it
was never about the gate). Only comment/prose lines changed — confirmed via
`git diff HEAD~1 -- <spec>` showing every changed line begins with `#`. Neither
retired over-claim phrase was reintroduced.

## Deviations from Plan

### Auto-fixed issues

None — the plan's guard-order, docstring content and map cells were followed as
written; no Rule 1/2/3 fix was needed.

### Noted, not a deviation from this plan's own scope

**Acceptance criteria referencing the two monitoring fixtures' plan-gate exit code
are stale relative to the merged tree, per the orchestrator's pre-flight context.**
The plan text (written before Wave 1 was merged onto the settled branch) says
`dsx gate plan` against `frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml`
and `bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` "exits 0". After the
orchestrator's merge brought in Phase 9 plan 09-01's shipped `DSX-PAR-010`/`DSX-PAR-011`,
both fixtures now correctly exit 1 at `plan` — but for their *own* target defect
(`DSX-PAR-010`/`DSX-PAR-011`, both already recorded in `_EXPECTED_CAUGHT_DEFECTS`
before this plan ran), never for `DSX-INT-010`/`DSX-INT-011`. Verified directly:
`dsx gate plan --json` against both fixtures shows no `DSX-INT-*` finding at all —
the substantive guarantee this plan owns (interference doesn't misfire on the
monitoring fixtures) holds; only the plan's literal "exits 0" wording is now
inaccurate for a reason entirely outside this plan's scope. The full
`tests/test_known_bad_corpus.py` suite (17 tests, including the merged
`_effective_target_map()` assertion) passes, which is the actual regression gate
for this claim.

## Self-Check: PASSED

- FOUND: dsx/frame/interference.py
- FOUND: tests/test_frame_interference.py
- FOUND: dsx/spec.py
- FOUND: dsx/frame/paradigm.py
- FOUND: dsx/cli.py
- FOUND: scripts/gen-finding-catalogue.py
- FOUND: references/finding-codes.md
- FOUND: tests/test_frame_boundary.py
- FOUND: tests/test_known_bad_corpus.py
- FOUND: examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/interference-shared-budget-POSTMORTEM.md
- FOUND commit d9fdae7 (Task 1) in `git log --oneline`
- FOUND commit 1cea641 (Task 2) in `git log --oneline`
- FOUND commit f62518a (Task 3) in `git log --oneline`
- `python3 -m unittest discover -s tests` — 486 tests, OK (skipped=2)
- `sh scripts/check.sh` — all checks passed
- Working tree clean after all three commits (`git status --porcelain` empty)
