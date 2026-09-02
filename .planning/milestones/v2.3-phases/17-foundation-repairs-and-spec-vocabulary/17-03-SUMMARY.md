# 17-03 SUMMARY — estimand_kind vocabulary + shared DSX-STA-040 guard

**Plan:** 17-03 (Wave 2, depends_on 17-01) · **Requirements:** REQ-P17-02, REQ-P17-05
**Executed:** 2026-09-01, inline on `gsd/v2.3.0-test-catalog` as orchestrator (NOT the
framework subagent-wave path — branch-safety anti-pattern, HUMAN-QUEUE standing note).
**Status:** COMPLETE. This closes S1-3 (all three Phase-17 plans executed).

## What was built

- **`estimand_kind` closed 6-member vocabulary (D-01)** in `dsx/spec.py`: a name→description
  dict `ESTIMAND_KINDS` = `{linear_association, monotone_association, nominal_association,
  agreement, method_comparison, ordered_trend}`, placed beside `ESTIMAND_TYPES` with an
  orthogonality comment (kind = association/agreement FORM for test routing;
  validity_frame.estimand.type = causal QUANTITY for admissibility; disjoint, never a shared
  read site). Registered in `_VOCABULARIES` under the **singular** dump key `estimand_kind`
  (matches the analysis field name and the 17-VALIDATION oracle).
- **DSX-STA-040 widened, zero new codes (REQ-P17-05)** in `dsx/checks/stats.py`: the old
  single hardcoded outcome_type membership test became a single-call-site `(field, vocab)`
  membership loop over `outcome_type` (OUTCOME_TYPES) and `estimand_kind` (ESTIMAND_KINDS,
  imported from `..spec` — D-03a allowed direction). The loop runs **independently of** the
  declared-test early return, so a mis-slotted routing value is always a loud DSX-STA-040
  (D-01), never a silent no-op (the Pitfall-2 tightening). Pure normalized-equality
  membership; no n_groups/paired coupling.
- **Fixtures + template extended (D-08)**: `estimand_kind: linear_association` on both
  canonical ANALYSIS-SPECs (a valid member — inert; the bad fixture's pinned finding set is
  unchanged) and `estimand_kind: null` + six-member allowed-values comment on the template.
- **Catalogue regenerated**: `references/finding-codes.md` rebuilt (DSX-STA-040 row text now
  templated over both guarded fields); `tests/fixtures/finding-codes-phase12.md` byte-frozen.

## Gate evidence (all re-run by the orchestrator)

- Task 1 RED: `test_estimand_kind_vocab` failed on `ImportError: cannot import name
  'ESTIMAND_KINDS'` + the guard/Pitfall-2 assertions (commit f684e8e).
- Task 2 GREEN: `python -m unittest tests.test_estimand_kind_vocab tests.test_finding_catalogue_invariant`
  → **8 tests OK** (6 vocab assertions + catalogue 260 by set identity). D-03a import boundary
  intact (full suite has no import-boundary failure). Commit d7ca5ce.
- Task 3: `python scripts/gen-finding-catalogue.py --check` → **exit 0** ("finding catalogue
  is current"); the pre-existing "declared twice" generator warnings do NOT include
  DSX-STA-040 (single call site, no duplicate-text warning). `test_finding_catalogue_invariant`,
  `test_good_fixture_phase15`, `test_causal_verb_golden` → **11 tests OK**. Commit 929a364.
- Merge gate: `python -m unittest discover -s tests -q` from a clean tree → **1323 tests, OK**.

## Deviation — Wave-1 lockstep gap repaired (one repair attempt, brief §5)

The S1-3 full-suite merge gate surfaced a REGRESSION the Wave-1 (17-01) firing missed by not
running the full suite after the Boschloo change: `tests/test_dsx.py`'s REQ-P11-05 pinned
golden snapshot `_BASELINE_TWO_PROPORTION_NO_SPEC` still asserted `fisher_exact (any expected
cell < 5)` and carried a **now-false** provenance comment ("stats.py byte-identical to v1.4.0
/ recommend_test never changed"). The REQ-P17-01 reconciliation (commit 99622fe) deliberately
changed that alternative to `boschloo_exact`. Fixed the snapshot value, comment, and docstring
to the reconciled reality (doc test-selection.md:10 and code stats.py:75 both name Boschloo;
`git log v1.4.0..HEAD -- dsx/checks/stats.py` confirms stats.py did change). Committed as a
17-01 fix (06d4cf6), not folded into 17-03. This is REQ-P17-01's intended effect, not a new
defect. No new finding code.

## Files

- `dsx/spec.py`, `dsx/checks/stats.py`, `examples/good-ANALYSIS-SPEC.yaml`,
  `examples/bad-ANALYSIS-SPEC.yaml`, `templates/ANALYSIS-SPEC.yaml`,
  `references/finding-codes.md`, `tests/test_estimand_kind_vocab.py`,
  `tests/test_dsx.py` (17-01 lockstep repair).

## Commits

f684e8e (RED) · d7ca5ce (GREEN) · 06d4cf6 (17-01 baseline repair) · 929a364 (Task 3).
