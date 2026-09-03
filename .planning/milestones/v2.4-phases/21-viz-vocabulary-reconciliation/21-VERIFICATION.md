---
phase: 21
unit: S1-4
verdict: PASSED
requirements_verified: [REQ-P21-01, REQ-P21-02, REQ-P21-03]
gate_rerun_by_orchestrator: true
full_suite: "Ran 1471 tests OK"
catalogue_total: 275
minted_codes: []
set_identity_baseline: 4b5c32d^
set_identity_symmetric_difference: empty
review_findings_fixed: [LOW-1, LOW-2]
---

# 21-VERIFICATION — Phase 21 goal-backward verification

**Verifier:** autonomous ceremony orchestrator (opus / high, brief §3 verification routing).
**Date:** 2026-09-02. **Unit:** S1-4 (verification `passed`).
**Method:** goal-backward against REQ-P21-01..03 — for each requirement, the delivered
artifact and the gate that proves it, **re-run by the orchestrator on the final post-fix tree**
(not trusted from the S1-3 subagent/inline report). All commands run from a clean tree (no
stray root `DECISIONS.jsonl` — the two `explain` tests pass in the full suite). The two LOW
findings from `21-REVIEW.md` (invariant-test anti-vacuity floor + allowlist-phantom guard) are
included in every rerun below.

## Phase goal

Reconcile the chart-type vocabulary so **every mark has a home and no ban is a silent
absence**, as the foundation the Phase-22 catalog spine is built on — while **minting zero new
codes** (catalogue stays 275). Concretely: a repo-integrity invariant proving every non-banned
mark is reachable through a capability family and (a relationship family OR an explicit frozen
allowlist); the 12 orphans homed one-family-each; the five `BANNED_TYPES` promoted to
first-class `{reason, code, citation}` refusal records; and a set-identity diff proving no code
was minted by the change.

## Requirement-by-requirement verdict

### REQ-P21-01 — every-mark-has-a-home invariant; the 12 orphans homed → **PASS**

- **Delivered:** `tests/test_viz_vocabulary_invariant.py` (off the gate path by construction —
  `tests/` is never in `dsx.cli.GATE_PROFILES`' import closure). Two directional homing clauses
  (`test_every_mark_has_a_capability_home`, `test_every_mark_has_a_relationship_home_or_is_allowlisted`)
  over a mark universe of 50 = union of `RELATIONSHIP_CHARTS ∪ CHART_CAPABILITIES ∪ EXTRA_MARKS`
  values `∪ LENGTH_ENCODED ∪ DENSITY_MARKS ∪ STACKED_MARKS`, minus `BANNED_TYPES`. Capability
  home defined gate-faithfully as `CHART_CAPABILITIES ∪ EXTRA_MARKS` (exactly what DSX-VIZ-013's
  `_check_input_type_matrix` admits from). The 10 capability orphans + 3 relationship orphans
  are homed one-family-each; `kde` (the one double orphan) homed in both surfaces;
  `population_pyramid`/`butterfly` left capability-homed via `EXTRA_MARKS[IT011]` and given only
  relationship homes (Pitfall 2). The frozen `CAPABILITY_ONLY` allowlist (14 marks) is guarded
  both directions: no entry may already have a relationship home, and (LOW-2 fix) every entry
  must be a real member of the universe.
- **Gate re-run:** `tests.test_viz_vocabulary_invariant` **9 OK**. The two gate smokes
  (`test_coarse_family_path_admits_a_homed_mark`, `test_input_type_id_path_admits_a_homed_mark`)
  positively prove the homing removed real DSX-VIZ-013 friction on both admissibility paths —
  the coarse-family path (live `CHART_CAPABILITIES`) and the IT040 id path (regenerated
  `dsx/data/input_types.json`) — so the homing is real, not decorative. Non-vacuity now
  explicitly guarded (`test_mark_universe_is_non_vacuous`, LOW-1 fix).

### REQ-P21-02 — banned/excluded types become first-class refusal entries with banning code + citation → **PASS**

- **Delivered:** `BANNED_TYPES` promoted in place from `dict[str, str]` to `dict[str,
  {reason, code, citation}]` (single registry — no parallel sub-map, so no drift surface,
  D-02). All five carry `code = "DSX-VIZ-001"` (a cross-reference to the existing code
  `_check_banned` already emits — not a new one) and a perception-doctrine `citation`
  (Munzner ch.6 / Tufte for the 3D marks, Muth 2018 for `dual_axis_line`; `radar` PROVISIONAL,
  flagged in HQ-27 for S5-2). `_check_banned`'s reader updated to `["reason"]` at its one call
  site; the `in` membership check needed no change.
- **Gate re-run:** `TestRefusalEntryCompleteness` green — every record has non-empty
  `reason`/`code`/`citation`; every code equals DSX-VIZ-001; and `viz.check` on a `radar` spec
  still fires exactly one DSX-VIZ-001 finding whose `detail` is the enriched `reason` string.
  Repo-wide grep confirms no second reader breaks on the shape change (21-REVIEW probe 1). The
  refusal-citation authenticity itself is a D-05 human read (HQ-27 Tier-3, batched to S5-2) —
  this requirement delivers the *routed-to-refusal, never silently absent* structure, which is
  met.

### REQ-P21-03 — zero new codes, by set-identity diff against the live 275-code baseline → **PASS**

- **Delivered:** the shape change touches only `detail=` text, which the AST-based catalogue
  generator never reads, so it is mechanically incapable of minting a code (plan-checker proved
  `gen-finding-catalogue.py::extract()` never reads `detail=`).
- **Gate re-run (set-identity, the requirement's named method):** the sorted unique code set
  extracted from `references/finding-codes.md` at the pre-Phase-21 baseline (`4b5c32d^`) and at
  HEAD are **both 275 and their symmetric difference is empty** — zero codes added, zero
  removed. `python scripts/gen-finding-catalogue.py --check` → "finding catalogue is current"
  @ **Total: 275 codes** (the three `declared twice` warnings for DSX-SPEC-070 / DSX-VAL-021 /
  DSX-VAL-060 are pre-existing legacy — they appear identically at the baseline, confirmed by
  the empty set diff, and concern codes Phase 21 never touched). `tests.test_finding_catalogue_invariant`
  + `tests.test_gen_finding_catalogue` → 46 OK.

## Orchestrator gate evidence (clean tree, final post-fix state, this unit)

- `python -m unittest tests.test_viz_vocabulary_invariant` → **Ran 9 tests OK**.
- `python -m unittest tests.test_finding_catalogue_invariant tests.test_gen_finding_catalogue`
  → **Ran 46 tests OK**.
- `python scripts/gen-finding-catalogue.py --check` → "finding catalogue is current" (exit 0),
  **Total: 275 codes**.
- Set-identity diff `finding-codes.md` codes at `4b5c32d^` vs HEAD → **275 == 275, symmetric
  difference empty (IDENTICAL)**.
- `python -m unittest discover -s tests` → **Ran 1471 tests OK** (the two `explain` tests
  passed → no stray root `DECISIONS.jsonl`; 1470 at S1-3 + 1 new anti-vacuity method = 1471).

## Verdict

**PASSED** — all three requirements delivered with re-run oracles; the vocabulary is homed
(50-mark universe, two directional clauses green), the five bans are complete first-class
refusal records, and the finding catalogue is proven byte-identical at 275 by set-identity
diff. Two LOW review findings fixed. Ready for S1-5 (`/gsd-secure-phase 21` +
`/gsd-validate-phase 21`; end-of-phase security sign-off + UAT batched to HUMAN-QUEUE,
non-blocking until S5-2).
