---
phase: 22-catalog-spine-uncertainty-heuristic
plan: 02
wave: 2
status: complete
requirements:
  - REQ-P22-05
completed: 2026-09-03T03:37Z
---

# 22-02 SUMMARY — Mint DSX-VIZ-071 (the uncertainty-vocabulary gate)

Wave 2 of Phase 22. The single new gate code this phase introduces. TDD
RED→GREEN→prove, all gates re-run by the orchestrator on the final tree.

## What landed

**Task 1 (RED):**
- New `tests/test_uncertainty_vocabulary.py` — 3 gate-behaviour methods
  (non-member fires DSX-VIZ-071; a §5.6 member does not; an absent field is
  silent) plus the exact `# D-05: DSX-VIZ-071` test marker.
- Bumped `tests/test_finding_catalogue_invariant.py`: `_EXPECTED_TOTAL` 275→276,
  `DSX-VIZ-071` added to `_MINTED_CODES`, count method renamed to
  `test_finding_catalogue_stays_at_276_codes`, docstrings/messages updated to name
  DSX-VIZ-071 as the sole additive mint; snapshot stays byte-frozen at 256; all
  regexes left CRLF-safe (untouched).
- RED-confirmed: non-member returned 0≠1; set-identity `removed=['DSX-VIZ-071']`;
  count 275≠276. No assertion softened.

**Task 2 (GREEN):**
- `dsx/checks/viz.py` — added `_check_uncertainty_vocabulary(visual, label, where,
  report)` beside `_check_uncertainty`; reads `visual.get("uncertainty_mark")`,
  returns early if blank, else emits DSX-VIZ-071 (MEDIUM) when the normalized mark
  is not in `set(RELATIONSHIP_CHARTS["uncertainty"])` — pure membership, no
  threshold. Docstring carries the `Citation:` (Wilke §5.6 + §16.2) and `Structural
  criterion:` lines on their own lines (so `_resolve_docstrings` binds them).
  `report.add` kept inside the function. Wired the call into `check()`'s per-visual
  block next to `_check_uncertainty`. DSX-VIZ-070 unchanged (complementary).
- `scripts/gen-finding-catalogue.py` — `DSX-VIZ-071` added to `_D05_ALLOWLIST_CODES`
  by EXACT string (not the `DSX-VIZ-` prefix, which would drag the ~20 legacy
  uncited VIZ codes into enforcement), with a comment recording why.
- Regenerated `references/finding-codes.md` via `--write`: Total line reads 276,
  the DSX-VIZ-071 row present under the Visualization group.

**Task 3 (prove):**
- Two sibling lockstep count-pins that hardcode the *live* catalogue total needed
  the same 275→276 bump (they explicitly track `_EXPECTED_TOTAL`): 
  `tests/test_p19_categorical_rows.py` (`_EXPECTED_TOTAL` + method rename) and
  `tests/test_phase20_zero_mint_close.py` (the count-declares assertion + method
  rename + docstrings). Their real zero-mint tells (absent DSX-STA-06x decade;
  untouched DSX-STA 123+ reserve band; snapshot subset) are unchanged. This ripple
  was not in 22-02's `files_modified` list but is the direct, necessary consequence
  of the legitimate mint — recorded loudly here rather than silently.

## Gate evidence (orchestrator-run, final tree)

- DSX-VIZ-071 gate + set-identity: `python -m unittest
  tests.test_uncertainty_vocabulary tests.test_finding_catalogue_invariant` = 5 OK.
- D-05 enforced for the new code: `python scripts/gen-finding-catalogue.py --check`
  → exit 0, "finding catalogue is current" (Citation:/Structural criterion:
  docstring lines + `# D-05: DSX-VIZ-071` marker + exact-string allowlist all
  present).
- Catalogue: `**Total: 276 codes.**`; DSX-VIZ-071 row present.
- **Additive-only proof:** the set-identity invariant passes → added={DSX-VIZ-071},
  removed={}, nothing dropped. 275→276.
- Full suite (per-wave gate): `python -m unittest discover -s tests` = **1481 OK**
  (1478 + 3 new gate tests), 41.0s, clean tree.

## Decision recorded loudly (HQ-30 veto window; silence = accept)

**DSX-VIZ-072 is NOT minted.** The ten §5.6 marks are deliberately paradigm-
symmetric (that symmetry IS REQ-P22-02's D-12a-clean property), so there is no
clean mark→paradigm partition to gate — a paradigm-mismatch check would
manufacture a false constraint. Phase 22's blocking-code footprint is exactly one:
DSX-VIZ-071.

## Notes

- DSX-VIZ-071 answers *selection* ("which uncertainty mark?"); DSX-VIZ-070 answers
  *presence* ("is uncertainty shown at all?"). Neither subsumes the other; both
  retained.
- The 7 pre-existing declared-twice VAL/COH/PAR/SPEC warnings on `--check` are
  unrelated (no VIZ code), unchanged by this wave.
- REQ-P22-05 (gate extended, D-05 citation carried the enforced way, additive-only
  mint proven) delivered. Waves 3-4 (catalog + heuristic) remain in S2-3.
