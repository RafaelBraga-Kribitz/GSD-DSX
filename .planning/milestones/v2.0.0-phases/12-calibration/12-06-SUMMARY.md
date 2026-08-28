---
phase: 12-calibration
plan: 06
subsystem: testing
tags: [python, unittest, tdd, calibration, friction, finding-codes, crlf]

# Dependency graph
requires:
  - phase: 12-calibration (plan 12-05)
    provides: stratified catch-rate + FPR harness, _headline/_false_positive_findings helpers, _effective_target_map, live _gate_findings source
  - phase: 12-calibration (plans 08-02/09-01/11.1-08/11.2-08)
    provides: _TARGET_DEFECT_CODES / _EXPECTED_CAUGHT_DEFECTS per-fixture maps and _own_target_codes flattening
provides:
  - Per-family friction column computed live (raw + net) as a rate over non-target in-profile (fixture × gate-point) cells
  - Three D-11 friction guards (synthetic arithmetic, live-source, incidental→own relabel closure)
  - D-18 catalogue-invariant test pinning the finding-code catalogue at exactly 256
affects: [12-calibration verification, milestone audit, any future check-shipping phase that would change the catalogue count]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Two-proofs discipline: a pure filesystem-independent arithmetic proof beside a live-source proof, so a corpus that is degenerate/clean by construction cannot hide a broken helper"
    - "Friction reported RAW and NET (never net-only) so a relabel that shrinks net is visible against a relabel-stable raw"
    - "CRLF-tolerant catalogue parsing via whitespace-collapse + non-line-anchored row regex"

key-files:
  created:
    - tests/test_finding_catalogue_invariant.py
  modified:
    - tests/test_known_bad_corpus.py

key-decisions:
  - "Guard (c) asserts each own-target code fires as a BLOCKING finding at its mapped point per that point's gate threshold (CRITICAL at plan/execute; CRITICAL or HIGH at verify/ship), not a blanket CRITICAL — because DSX-ML-090 is HIGH by design and can never fire CRITICAL"
  - "Guard (c) naming allows a documented cross-fixture fallback: DSX-INT-030 is triggering-dilution's PRIMARY declared code, recorded as a secondary key on weak-identification-mmm, and is named in a corpus postmortem though not weak-identification-mmm's own"
  - "Catalogue-invariant test cross-checks the declared **Total: N** line AND the enumerated DSX-* rows, requiring both to equal 256"

patterns-established:
  - "Friction helpers (_friction, _friction_rate, _non_target_in_profile_cells) take their inputs as parameters so a synthetic proof exercises them without the filesystem or the gate"

requirements-completed: [REQ-P12-02]

coverage:
  - id: D1
    description: "Per-family friction column: live raw + net over-block, expressed as a rate over non-target in-profile cells, reported both ways (never net-only)"
    requirement: "REQ-P12-02"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#TestFrictionArithmetic (net_is_raw_minus_own_and_both_are_surfaced, relabeling_incidental_to_own_shrinks_net_but_not_raw, friction_rate_normalises_over_non_target_cells_and_floors_on_empty, non_target_in_profile_cells_counts_only_untargeted_cells)"
        status: pass
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_friction_uses_the_same_live_findings_as_golden"
        status: pass
    human_judgment: false
  - id: D2
    description: "Incidental→own relabel closure: every _TARGET_DEFECT_CODES entry fires blocking live at its mapped point and is named in a fixture postmortem/attribution"
    requirement: "REQ-P12-02"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py#TestKnownBadCorpus.test_target_defect_codes_fire_and_are_named"
        status: pass
    human_judgment: false
  - id: D3
    description: "D-18 catalogue invariant: the finding-code catalogue stays at exactly 256 codes; no code minted in Phase 12"
    requirement: "REQ-P12-02"
    verification:
      - kind: unit
        ref: "tests/test_finding_catalogue_invariant.py#TestCatalogueInvariant.test_finding_catalogue_stays_at_256_codes"
        status: pass
      - kind: other
        ref: "python scripts/gen-finding-catalogue.py --check"
        status: pass
    human_judgment: false

# Metrics
duration: 22min
completed: 2026-08-27
status: complete
---

# Phase 12 Plan 06: Friction Column + Catalogue Invariant Summary

**Live per-family friction column (raw + net over-block as a rate over non-target in-profile cells) guarded three ways — synthetic arithmetic, same-live-source-as-golden, and incidental→own relabel closure — plus a D-18 test pinning the finding-code catalogue at exactly 256.**

## Performance

- **Duration:** ~22 min
- **Started:** 2026-08-27
- **Completed:** 2026-08-27
- **Tasks:** 2
- **Files modified:** 2 (1 created, 1 modified)

## Accomplishments
- Added `_friction(blocking, own) -> (raw, net)`, `_friction_rate(total, cells)`, and `_non_target_in_profile_cells(effective, slugs, points)` — pure, parameterised friction helpers in the corpus harness.
- Added the three D-11 friction guards: `TestFrictionArithmetic` (filesystem-independent, net = raw − own, both surfaced, relabel shrinks net but not raw), `test_friction_uses_the_same_live_findings_as_golden` (consumes the same live `_gate_findings(slug, "ship")` set the golden test uses), and `test_target_defect_codes_fire_and_are_named` (every own-target code fires blocking live and is named in a postmortem/attribution).
- Created `tests/test_finding_catalogue_invariant.py` pinning the catalogue at 256 via both the declared Total line and the enumerated rows, CRLF-tolerant.
- Full `tests.test_known_bad_corpus` module green at 44 tests (was 38, +6); catalogue `--check` current at 256.

## Task Commits

Each task was committed atomically (TDD RED → GREEN):

1. **Task 1 (RED): failing friction column proofs** - `5206c2d` (test)
2. **Task 1 (GREEN): live per-family friction helper** - `2ce0404` (feat)
3. **Task 2: pin the finding-code catalogue at 256** - `6cede76` (test — invariant pin, no production code to add since the catalogue already holds at 256)

_Task 2 is a single `test(...)` commit: it pins an already-holding invariant, so there is no separate GREEN implementation step — the "code under test" (the generated catalogue) already exists at 256._

## Files Created/Modified
- `tests/test_known_bad_corpus.py` - Added three friction helpers and three D-11 guards (TestFrictionArithmetic class + two TestKnownBadCorpus methods).
- `tests/test_finding_catalogue_invariant.py` - New: TestCatalogueInvariant.test_finding_catalogue_stays_at_256_codes (D-18).

## Decisions Made
- **Friction denominator (non-target in-profile cells):** defined as (fixture × `_CRITICAL_THRESHOLD_POINTS`) cells where `_effective_target_map()` has no expected own-target code — the cells at which any block is over-blocking, matching the corpus's positive-direction test's cell space.
- **Catalogue test reads both signals:** the `**Total: N codes.**` line (whitespace-collapsed) and the enumerated `DSX-*` rows, requiring both to equal 256, so a stale Total line is caught as well as a minted/dropped code.

## Deviations from Plan

The plan's guard (c) wording says "every `_TARGET_DEFECT_CODES` entry fires **CRITICAL** live AND is named in **that slug's** POSTMORTEM.md or ATTRIBUTION.yaml." Two literal-wording deviations were necessary because the committed corpus makes the literal form impossible to satisfy without editing corpus files (which is prohibited — files_modified is test-only). Both were verified empirically before writing the test.

**1. [Rule 1 - Correctness] Guard (c) asserts "fires blocking at its mapped point per that point's gate threshold", not blanket CRITICAL**
- **Found during:** Task 1 (guard c design), confirmed by a live severity probe across all `_TARGET_DEFECT_CODES` entries.
- **Issue:** `full-frame-cleaning`'s own-target entry `DSX-ML-090` is severity **HIGH** by design (documented at length in the `_TARGET_DEFECT_CODES` comment: it is recorded under a "ship" collision-avoidance key precisely because `_classify_target_defect` only checks CRITICAL). A blanket "fires CRITICAL" assertion would fail on `DSX-ML-090`, which never fires CRITICAL anywhere.
- **Fix:** Guard (c) requires each mapped code to fire at a severity that **blocks its mapped gate point** — CRITICAL at `plan`/`execute`, CRITICAL or HIGH at `verify`/`ship` — exactly the gate thresholds `references/finding-codes.md` documents. This is strictly stronger for the threat it closes (the code must actually block the gate at the point it is credited), and is the only form consistent with a HIGH ship-key code.
- **Files modified:** tests/test_known_bad_corpus.py
- **Verification:** `test_target_defect_codes_fire_and_are_named` passes; full module green.
- **Committed in:** 5206c2d (RED) / passes at 2ce0404.

**2. [Rule 1 - Correctness] Guard (c) naming allows a documented cross-fixture fallback**
- **Found during:** Task 1 (guard c design), confirmed by a naming probe.
- **Issue:** `weak-identification-mmm`'s secondary "verify" key holds `DSX-INT-030`, which is **triggering-dilution's** own primary declared code (a second genuine defect weak-identification-mmm also encodes, per the map comment). `DSX-INT-030` is named in a corpus postmortem (triggering-dilution's) but NOT in weak-identification-mmm's own postmortem, and none of these fixtures has an ATTRIBUTION.yaml. A strict "that slug's own docs only" assertion would fail on this one entry, and the fix (adding text to a corpus postmortem) is out of scope.
- **Fix:** Guard (c) checks the slug's own POSTMORTEM.md/ATTRIBUTION.yaml first, and accepts a code that is named in **any** corpus postmortem/attribution as a documented fallback — the threat (a *silent* incidental→own relabel) is still closed, because the code must be publicly declared an intended defect somewhere in the corpus. Only `DSX-INT-030`/weak-identification-mmm uses the fallback today.
- **Files modified:** tests/test_known_bad_corpus.py
- **Verification:** `test_target_defect_codes_fire_and_are_named` passes.
- **Committed in:** 5206c2d (RED) / passes at 2ce0404.

---

**Total deviations:** 2 (both literal-wording adjustments to guard (c), each strictly threat-faithful and forced by the committed corpus + test-only scope). **Impact on plan:** No scope creep; the objective (friction RAW+NET as a live rate, three guards, catalogue pinned at 256) is met exactly. No production source, no tracking file, and no catalogue file was touched.

## Issues Encountered
- Initial severity probe showed `full-frame-cleaning`'s CODE codes as ABSENT because the probe did not seed the fixture's entrypoint into the fresh tempdir. Resolved by using `self._gate_findings` in the test, which calls `_seed_entrypoint` (and `seed_plan_header` for verify/ship) — the same live source the golden test uses.

## Orchestrator Handoff (tracking files NOT written by this subagent)
Per the parallel-subagent single-writer rule, this executor did **not** write STATE.md, ROADMAP.md, REQUIREMENTS.md, LOOP-LEDGER.md, or HUMAN-QUEUE.md. The orchestrator should serially:
- Mark **REQ-P12-02** complete.
- Advance the plan counter / progress for phase 12 plan 06.
- Record metrics (duration ~22 min, 2 tasks, 2 files).

## Next Phase Readiness
- Friction column and its three guards are live and green; the catalogue is pinned at 256.
- **Unpushed:** branch `gsd/v2.0.0-dsx-validity-frame` is **ahead 3** commits (5206c2d, 2ce0404, 6cede76) — not pushed, per single-writer wave discipline; orchestrator to push after the wave merges.

## Self-Check: PASSED

---
*Phase: 12-calibration*
*Completed: 2026-08-27*
