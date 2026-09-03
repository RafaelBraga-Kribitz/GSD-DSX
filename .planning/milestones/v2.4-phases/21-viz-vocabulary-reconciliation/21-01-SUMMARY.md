---
phase: 21-viz-vocabulary-reconciliation
plan: 01
type: tdd
status: executed
executed: 2026-09-02
requirements: [REQ-P21-01, REQ-P21-02, REQ-P21-03]
---

# Phase 21 · Plan 01 — Execution summary (S1-3)

Executed inline by the autonomous ceremony orchestrator (opus), 2026-09-02.
Rationale for inline vs delegated execution: the plan left zero design judgment
(D-01/D-02 decided, homing table plan-checker-verified); the orchestrator must
re-run every gate regardless (brief non-negotiable); CONTEXT.md required
single-firing completion without mid-unit compaction; STATE.md is
orchestrator-single-writer. Recorded loudly in LOOP-LEDGER Log.

## What was built

Three TDD tasks, RED → GREEN → GREEN:

**Task 1 (RED).** New repo-integrity test `tests/test_viz_vocabulary_invariant.py`
(off the gate path — `tests/` is never in `dsx.cli.GATE_PROFILES`' import closure).
Reads the live vocabulary objects directly; loads `EXTRA_MARKS` from the
hyphenated `scripts/gen-input-types.py` via `importlib.util.spec_from_file_location`
(the `test_phase20_zero_mint_close` precedent — exec_module is side-effect-free).
Two classes: `TestEveryMarkHasAHome` (D-01 clauses 1+2, allowlist-staleness guard,
two gate smokes) and `TestRefusalEntryCompleteness` (D-02 completeness, code
identity, `_check_banned` detail contract). RED confirmed with the exact orphan
lists: capability orphans `[bump, density, diverging_bar, dumbbell, ecdf,
histogram, kde, sankey, strip, waterfall]` (10); relationship orphans
`[butterfly, kde, population_pyramid]` (3). No assertion softened.

**Task 2 (GREEN, D-01).** Homed the 12 orphans, one family per mark (narrowest
home):
- `CHART_CAPABILITIES` (`dsx/spec.py`): interval-range += {histogram, density,
  ecdf, strip, kde}; categorical-value += {diverging_bar}; composition +=
  {waterfall}; categorical-multi += {dumbbell, bump}; matrix += {sankey}.
- `RELATIONSHIP_CHARTS` (`dsx/checks/viz.py`): distribution += {kde,
  population_pyramid}; comparison += {butterfly}.
- `population_pyramid`/`butterfly` NOT added to `CHART_CAPABILITIES` — already
  capability-homed via `EXTRA_MARKS["IT011"]` (Pitfall 2; corrects S0-2's
  "double orphan" label).
- Regenerated `dsx/data/input_types.json` via `python scripts/gen-input-types.py`
  (Pitfall 1: the IT-id gate path reads the static JSON, not the live dict).
  Diff = admissible-set additions only; verbatim-field test green.

**Task 3 (GREEN, D-02 + REQ-P21-03).** Promoted `BANNED_TYPES` from
`dict[str, str]` to `dict[str, {reason, code, citation}]` in place; `code =
DSX-VIZ-001` for all five (cross-ref to the existing code, not a new one);
`_check_banned` detail line changed to `["reason"]` (one call site, viz.py).
Citations point at HQ-27 Tier-3: 3d_* → Munzner ch.6 + Tufte 1983; dual_axis_line
→ Muth 2018 (see also DSX-VIZ-030); radar → provisional (no exact source — flagged
in HQ-27 for S5-2, Pitfall 5). HUMAN-QUEUE HQ-27 annotated with the per-mark
mapping and the radar gap.

## Gate evidence

| Gate | Command | Result |
|---|---|---|
| Task 1 RED | `unittest tests.test_viz_vocabulary_invariant` | non-zero: 9 failures + 6 errors, exact orphan lists |
| Task 2 GREEN | `gen-input-types.py && unittest TestEveryMarkHasAHome tests.test_input_types` | 22 OK (homing + both gate smokes + input-type suite) |
| Task 3 GREEN | `unittest test_viz_vocabulary_invariant test_finding_catalogue_invariant test_gen_finding_catalogue` | 54 OK |
| REQ-P21-03 (275 three ways) | Total line grep; CRLF-safe unique-code count; catalogue-invariant | 275 / 275 / green — zero mint |
| Phase suite | `unittest discover -s tests` | 1470 OK |

## Requirements

- **REQ-P21-01** (homing + invariant) — SATISFIED: both clauses green, allowlist
  frozen (14 marks), gate smokes prove DSX-VIZ-013 friction removed on both
  admissibility paths.
- **REQ-P21-02** (refusal entries) — SATISFIED: five complete {reason, code,
  citation} records; `_check_banned` still fires DSX-VIZ-001 with reason as detail.
- **REQ-P21-03** (zero new codes) — SATISFIED: catalogue 275 → 275, proven three
  ways; the `detail=` edit is mechanically unable to mint a code (generator
  `extract()` never reads `detail=`).

## Notes for S1-4 (code review + verification)

- The "declared twice with different text" warnings during the catalogue oracle
  are pre-existing (DSX-COH-030/PAR-002/SPEC-070/VAL-021/VAL-060 — non-VIZ,
  untouched here); tests pass regardless.
- radar citation is provisional — the one HQ-27 row to give closest attention at
  S5-2. Not a Phase 21 blocker (DSX-VIZ-001 already fires; reason strings shipped
  long ago).
- HQ-28 (D-01/D-02 veto window) remains open, non-blocking; silence = accept.
