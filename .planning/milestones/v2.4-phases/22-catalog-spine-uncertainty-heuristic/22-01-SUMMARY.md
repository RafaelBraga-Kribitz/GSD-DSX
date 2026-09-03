---
phase: 22-catalog-spine-uncertainty-heuristic
plan: 01
wave: 1
status: complete
requirements:
  - REQ-P22-02
  - REQ-P22-03
completed: 2026-09-03T03:28Z
---

# 22-01 SUMMARY — Uncertainty vocabulary spine + refusal doctrine + facet routing

Wave 1 of Phase 22. The vocabulary spine the rest of the phase stands on. TDD
RED→GREEN→GREEN, all gates re-run by the orchestrator on the final tree.

## What landed

**Task 1 (RED):** extended `tests/test_viz_vocabulary_invariant.py` with a new
class `TestUncertaintyFamilyAndFacet` (7 methods) plus two frozensets
(`UNCERTAINTY_MARKS_D2` cross-check, `SEVEN_BANNED_TYPES`). RED-confirmed for the
documented reasons: no `uncertainty` key, len 10≠11, ten marks unhomed,
gauge/word_cloud absent, radar still PROVISIONAL, DSX-SMELL-007 remedy silent on
faceting. The facet_by-orthogonality guard passed as designed (standing guard).
No assertion softened.

**Task 2 (GREEN):**
- `dsx/checks/viz.py` — added the 11th `RELATIONSHIP_CHARTS["uncertainty"]` key: a
  ten-id tuple, `error_bars` first (default). Comment records D-2 (Wilke §5.6) and
  the §16.2 frequentist/Bayesian symmetry that makes it D-12a-clean by
  construction. `_check_relationship_match` needed no body change (mechanical over
  the dict).
- `dsx/spec.py` — added the same ten ids to `CHART_CAPABILITIES["interval-range"]`
  (the honest data-signature home; no new input-type id, GA-2).
- `python scripts/gen-input-types.py` regenerated `dsx/data/input_types.json` —
  verified IT040 (an interval-range id with no EXTRA_MARKS entry) now admits all
  ten marks, proving the id path was refreshed, not just the live dict (Pitfall 1).
- Gate: `TestEveryMarkHasAHome` + `tests.test_input_types` = 23 OK.

**Task 3 (GREEN):**
- `dsx/checks/viz.py` `BANNED_TYPES` → seven complete `{reason, code, citation}`
  records. Added `gauge` (Few 2006 grounds — wasted space / no context / unlabelled
  scale; arbitrary-maximum attributed to DSX's own reasoning, not Few, per HQ-27
  T3-GAUGE) and `word_cloud` (Jacob Harris 2011, editorial rationale). Swapped
  `radar`'s PROVISIONAL placeholder for the signed **Duan et al. 2023
  (J Clin Epidemiol 156:85-94)**. All seven `code == DSX-VIZ-001` (zero new code).
- `dsx/checks/smells.py` — DSX-SMELL-007 remedy now also routes to `facet_by`
  (small multiples), kept orthogonal to the mark (REQ-P22-03).

## Gate evidence (orchestrator-run, final tree)

- Full invariant module: `python -m unittest tests.test_viz_vocabulary_invariant
  tests.test_finding_catalogue_invariant` = **18 OK** (uncertainty key, 11
  relationships, ten marks capability-homed, seven complete refusal records
  code=DSX-VIZ-001, radar=Duan/no-PROVISIONAL, facet_by orthogonal, SMELL-007
  routes to facet_by).
- Zero mint held: catalogue invariant green at 275; `python
  scripts/gen-finding-catalogue.py --check` → exit 0, "finding catalogue is
  current". (7 pre-existing declared-twice VAL/COH/PAR/SPEC warnings, none a VIZ
  code, unrelated to this wave.)
- Input-type id path: `gen-input-types.py` wrote 40 input types; IT040 admits all
  ten uncertainty marks.
- Full suite (per-wave gate): `python -m unittest discover -s tests` = **1478 OK**
  (1471 baseline + 7 new invariant methods), 40.7s, clean tree
  (DECISIONS.jsonl swept per standing note).

## Notes

- Zero finding codes minted — DSX-VIZ-071 is Wave 2's work (22-02), which reads
  `set(RELATIONSHIP_CHARTS["uncertainty"])` from this wave as its source of truth.
- No parallel `UNCERTAINTY_MARKS` dict in production (Research Pattern 1): the
  tuple is the single authority; the test's `UNCERTAINTY_MARKS_D2` is a labelled
  cross-check only.
- REQ-P22-02 (uncertainty family, 11th-key shape, D-12a-clean) and REQ-P22-03
  (facet_by orthogonal, smells route to it, no new code) delivered.
