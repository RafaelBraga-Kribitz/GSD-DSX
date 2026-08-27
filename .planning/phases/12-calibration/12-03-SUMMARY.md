---
phase: 12-calibration
plan: 03
subsystem: known-bad-corpus-harness
status: complete
tags: [attribution-sidecar, falsifiability, anti-laundering, calibration, tdd, test-only]
requires: [dsx.loader.load, "tests/test_known_bad_corpus.py::_gate_findings", references/finding-codes.md, "examples/known-bad/*-ATTRIBUTION.yaml"]
provides: ["sidecar sibling-integrity validation (D-07)", "live tag falsifiability across four gate points (D-08)", "validated code union helper (catalogue ∪ §6.5 backlog)", "_SECTION_65_ITEM_IDS frozenset (nine ids)"]
affects: [tests/test_known_bad_corpus.py]
tech-stack:
  added: []
  patterns: [glob-discovery, dsx.loader-parse-no-pyyaml, allowlist-with-inline-reason, subset-sibling-check, live-gate-union-not-lifted-ledger, catalogue-enumeration-by-table-row-regex]
key-files:
  created: []
  modified: [tests/test_known_bad_corpus.py]
decisions: [D-01, D-03, D-06, D-07, D-08, D-18]
metrics:
  duration: ~20m
  completed: 2026-08-27
  tasks: 2
  files: 1
  commits: 2
requirements: [REQ-P12-02]
---

# Phase 12 Plan 03: Attribution Sidecar Validation Summary

Two new corpus-harness tests that make the §6.5 catch-attribution counts trustworthy: sidecar sibling-integrity (every `<slug>-ATTRIBUTION.yaml` names a real slug, an `absent_code` in the validated union of the 256-code catalogue plus the named §6.5 backlog codes, and one of nine real §6.5 item ids) and live falsifiability (each tag is confirmed against the CRITICAL union of a real `_gate_findings` run across plan/execute/verify/ship, so a miss cannot launder a firing code and a hypothetical code can never be credited as a catch). Test-only; zero codes minted, catalogue unchanged at 256.

## What Was Built (test-only, `tests/test_known_bad_corpus.py`)

- **`ATTRIBUTION_SUFFIX`** + **`_attribution_paths()`** — glob discovery of `*-ATTRIBUTION.yaml` by slug (D-06), no hardcoded slug list.
- **`_catalogue_codes()`** + `_CATALOGUE_ROW_RE` — enumerates the 256 shipped codes from `references/finding-codes.md` by table-row regex (`| `DSX-…` |`), the same generated artifact `scripts/gen-finding-catalogue.py --check` gates, so this reader cannot drift from what checks emit. Verified to return exactly 256.
- **`_SECTION_65_BACKLOG_CODES`** — allowlist-with-inline-reason set (mirroring `_INCIDENTAL_GAP_CODES`) of the four named-but-unshipped §6.5 codes: `DSX-PAR-020`, `-021`, `-022`, `-030`. Referencing an unbuilt backlog code is the miss-attribution point (D-07) and is not minting (D-18).
- **`_SECTION_65_ITEM_IDS`** — frozenset of exactly nine §6.5 item ids, one per `brief.md:369-379` row, in row order.
- **`test_attribution_sidecars_reference_valid_codes_and_items`** (D-07) — parses each sidecar via `dsx.loader.load` (no `import yaml`); asserts subset sibling-spec pairing (sidecars optional per D-03), `absent_code ∈ catalogue ∪ backlog`, `promotes_backlog_item ∈ _SECTION_65_ITEM_IDS`, required keys present, `kind` defaults to `miss`, and backlog∩catalogue = ∅.
- **`test_attribution_tags_are_falsifiable_against_live_gate`** (D-08) — reuses `self._gate_findings(spec_path, point)` verbatim over the four points, unions CRITICAL codes; `miss` ⇒ `absent_code` absent from union, `caught` ⇒ present. Never reads `_INCIDENTAL_GAP_CODES` / `_GOLDEN_SHIP_FINDINGS`.

## `_SECTION_65_ITEM_IDS` (nine) and provenance

Each id is `6.5-item-<N>-<slug>`, one per `brief.md:369-379` table row. Items 1 and 7 are load-bearing (used verbatim by the plan-12-01 sidecars); the other seven follow the same shape:

1. `6.5-item-1-prior-justification-and-sensitivity` — row 1 (`DSX-PAR-020/-021`) — **used by garden + operator sidecars**
2. `6.5-item-2-prior-predictive-check` — row 2 (`DSX-PAR-022`, REV-001)
3. `6.5-item-3-convergence-declarations` — row 3 (`DSX-PAR-030`)
4. `6.5-item-4-bayesian-admissibility` — row 4 (`DSX-ADM-*`, second axis)
5. `6.5-item-5-quiz-fading-mode` — row 5 (`dsx quiz`)
6. `6.5-item-6-ratio-metric-dilution` — row 6 (Deng & Hu 2015, REV-002 removal)
7. `6.5-item-7-feature-provenance` — row 7 — **used by retracted sidecar**
8. `6.5-item-8-magnitude-without-computed-effect` — row 8
9. `6.5-item-9-subgroup-harm-declaration` — row 9

## `_SECTION_65_BACKLOG_CODES` (four) and provenance

Named in §6.5 rows, confirmed NOT in the shipped catalogue (grep against `references/finding-codes.md` matched none of them):

- `DSX-PAR-020` — §6.5 item 1 prior justification (`brief.md:371`), unwritten
- `DSX-PAR-021` — §6.5 item 1 prior sensitivity (`brief.md:371`), unwritten
- `DSX-PAR-022` — §6.5 item 2 prior predictive check (`brief.md:372`, REV-001), writable but unshipped
- `DSX-PAR-030` — §6.5 item 3 convergence declarations (`brief.md:373`), unwritten

The wildcard family `DSX-ADM-*` (item 4) is deliberately not enumerated — it is a family, not a concrete code. The three shipped sidecars all name shipped catalogue codes (`DSX-EXP-051` HIGH, `DSX-VAL-080` HIGH, `DSX-REP-020` MEDIUM), so the backlog set is exercised as future-proofing, not by the current cases.

## Verification (verbatim)

`python -m unittest ...test_attribution_sidecars_reference_valid_codes_and_items -v` → `Ran 1 test in 0.004s` / `OK`.

`python -m unittest ...test_attribution_tags_are_falsifiable_against_live_gate -v` → `Ran 1 test in 0.720s` / `OK`.

`python -m unittest tests.test_known_bad_corpus` → `Ran 33 tests in 3.744s` / `OK` (both new tests plus all 31 existing).

### RED / negative-proof evidence (edit-and-revert, then restored)

- **Task 1** — set garden `absent_code: DSX-EXP-051 → DSX-XXX-999`: test FAILED (exit 1) with `names absent_code 'DSX-XXX-999' outside the validated union`. Reverted.
- **Task 2 Proof A** (caught branch / hypothetical never credited) — flip garden `kind: miss → caught`: test FAILED with `'DSX-EXP-051' not found in set() … a hypothetical/unshipped code can never be credited as a catch`. Reverted.
- **Task 2 Proof B** (miss branch bites) — temp sidecar for `weak-identification-mmm` with `absent_code: DSX-VAL-040, kind: miss` (a code that fires CRITICAL live): test FAILED with `'DSX-VAL-040' unexpectedly found in {'DSX-VAL-040', 'DSX-INT-030'} … a code that fires is a laundered catch, not a miss`. Temp sidecar removed.

## Deviations from Plan

None — plan executed exactly as written. TDD gate honored per task (test-only plan: each task is a `test(...)` commit, biting confirmed by negative proofs rather than a paired GREEN implementation, since the artifacts produced ARE tests).

## Structural note (not a deviation)

The plan's literal Task 2 miss-branch negative proof ("point a miss tag at one of the fixture's own target codes") cannot bite against the three shipped sidecar fixtures **as written**, because all three are genuine misses that fire ZERO CRITICAL findings across all four gate points (measured) — which is the D-08 invariant itself. The equivalent biting proof was therefore realized with a temporary sidecar on a catch fixture (`weak-identification-mmm`, which fires `DSX-VAL-040` CRITICAL at plan), demonstrated above as Proof B and removed after.

## Boundary compliance

- Only `tests/test_known_bad_corpus.py` modified. No edits to `dsx/`, `references/finding-codes.md`, `scripts/gen-finding-catalogue.py`, `GATE_PROFILES`, `dsx/checks/`, or any shared tracking file (STATE/ROADMAP/LOOP-LEDGER/HUMAN-QUEUE). No code minted; catalogue stays 256 (D-18).
- Not pushed — orchestrator pushes after re-gating the whole wave.

## Known Stubs

None.

## Self-Check: PASSED

- `tests/test_known_bad_corpus.py` present; both new tests and all 33 module tests pass.
- Commits `458dfad` and `219f4c4` present in `git log`.
- `git status --short` shows only `tests/test_known_bad_corpus.py` modified before commit; working tree clean after.
