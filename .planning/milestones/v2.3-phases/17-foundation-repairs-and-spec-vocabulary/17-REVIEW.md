# 17-REVIEW — Phase 17 code review

**Reviewer:** autonomous ceremony orchestrator (opus / high, brief §3 code-review routing).
**Date:** 2026-09-01. **Unit:** S1-4 (code review + fixes).
**Scope:** the phase-17 source/test/fixture diff `6baa7ce..HEAD` — every line read in full.

## Files reviewed

| File | Change | Verdict |
|---|---|---|
| `dsx/checks/stats.py` | `boschloo_exact` → `NONPARAMETRIC_TESTS`; two-proportion small-cell alt fisher→boschloo; DSX-STA-040 widened to a single-call-site `_MEMBERSHIP_FIELDS` loop | PASS (1 fix applied, below) |
| `dsx/spec.py` | 6-member `ESTIMAND_KINDS` + `_VOCABULARIES` registration under singular key `estimand_kind` | PASS |
| `tests/test_boschloo_reconciliation.py` | new (3 tests) | PASS |
| `tests/test_estimand_kind_vocab.py` | new (6 tests) | PASS |
| `tests/test_time_to_event_fallthrough.py` | new (2 tests) | PASS |
| `tests/test_dsx.py` | REQ-P11-05 pinned baseline updated fisher→boschloo (+ comment/docstring) | PASS |
| `examples/{good,bad}-ANALYSIS-SPEC.yaml`, `templates/ANALYSIS-SPEC.yaml` | `estimand_kind` added (D-08 additive, not replaced) | PASS |
| `references/finding-codes.md` | DSX-STA-040 row text genericized in lockstep with the code | PASS |

## Findings

### F1 — `Any` used in an annotation without import (LOW, FIXED)

`dsx/checks/stats.py:22` annotated `_MEMBERSHIP_FIELDS: "tuple[tuple[str, Any], ...]"`
but the module did not import `Any` (spec.py imports it for the identical
`_VOCABULARIES` pattern). No **runtime** impact — the annotation is a quoted string
under `from __future__ import annotations`, never evaluated — but it is a latent
defect for any type-checker or `typing.get_type_hints(stats)` call, and an
inconsistency with the sibling module it mirrors.

**Fix applied this firing:** added `from typing import Any` to `dsx/checks/stats.py`.
Re-gated green afterward (full suite 1323 OK; `scripts/check.sh` all checks passed).

## Points examined and cleared (no finding)

- **No double-report of DSX-STA-040.** The membership loop reports an unrecognized
  `outcome_type`; the old outcome_type block below it was reduced to a bare `return`
  (comment: "Already reported by the membership loop above"), so exactly one finding
  fires per mis-slotted field. Confirmed by `test_mis_slotted_value_fires_one_loud_finding`.
- **Intended behavioural tightening, not a regression.** The guard now runs *before and
  independently of* the `if not declared or not outcome_type: return` early exit, so an
  unrecognized `outcome_type` is flagged even when no test is declared (Pitfall-2 / D-01).
  `estimand_kind` is a brand-new field, so no pre-existing spec regresses; absence is
  skipped via `is_blank` (D-10 non-blocking). Full suite green confirms no golden/snapshot
  expected the previously-silent path.
- **Single call site preserved (REQ-P17-05).** DSX-STA-040 is emitted from one loop;
  the catalogue duplicate-text warnings (VAL-060, CLM-020/021, COH-030, PAR-002,
  SPEC-070, VAL-021) are the pre-existing set — DSX-STA-040 is **not** among them.
- **fisher_exact retained** alongside boschloo_exact in `NONPARAMETRIC_TESTS`
  (`test_boschloo_exact_added_without_dropping_fisher_exact`); the 3-plus-group
  fisher_exact routing is untouched.
- **Doc/code lockstep** honoured: `finding-codes.md` DSX-STA-040 text and the code's
  message changed in the same phase; `references/test-selection.md` still names Boschloo
  (`test_doc_still_names_boschloo`).

**Verdict: PASS** — one LOW finding, fixed; no outstanding issues.
