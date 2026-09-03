# 22-REVIEW — Phase 22 code review

**Reviewer:** autonomous ceremony orchestrator (opus / high, brief §3 code-review routing).
**Date:** 2026-09-03. **Unit:** S2-4 (code review + fixes).
**Scope:** the four Phase-22 execute commits `dc34a75` (22-01) · `f768822` (22-02) ·
`cd50e10` (22-03) · `217cf68` (22-04) — 23 files, +1927 / −56. Production/data changes:
`dsx/checks/viz.py`, `dsx/checks/smells.py`, `dsx/spec.py`, `dsx/data/input_types.json`,
`scripts/gen-finding-catalogue.py`, `references/finding-codes.md`. The rest is one new
reference artifact (`references/chart-catalog.md`), three route-and-cite doc edits
(`chart-selection.md`, `question-taxonomy.md`, `skills/dsx-visualize/SKILL.md`), four new/
extended test modules, and planning files. Every changed source hunk and every new test
module read in full. The review targets the three risks this phase actually carries:
**(1)** a live-vocabulary widening under cover of the new `uncertainty` key / `uncertainty_mark`
field (does the gate admit more than intended?); **(2)** false-pass risk in the four new
Markdown-reading invariants (oracles that look like proofs but pass vacuously); **(3)** the
count-pin ripple across three lockstep files (does bumping 275→276 quietly weaken a zero-mint
tell?).

## Files reviewed

| File | Change | Verdict |
|---|---|---|
| `dsx/checks/viz.py` | 11th `RELATIONSHIP_CHARTS` key `"uncertainty"` (10 Wilke §5.6 marks, D-2); new `_check_uncertainty_vocabulary` → **DSX-VIZ-071** wired into `check()`; `BANNED_TYPES` completed to 7 records (gauge/word_cloud added, radar PROVISIONAL→Duan 2023), all `code=DSX-VIZ-001` | PASS |
| `dsx/spec.py` | `CHART_CAPABILITIES["interval-range"]` gains the 10 uncertainty marks — keeps Phase-21 every-mark-has-a-home invariant green (GA-2, no new input-type id) | PASS |
| `dsx/checks/smells.py` | DSX-SMELL-007 remedy routes to `facet_by` (small multiples), kept orthogonal to the mark (REQ-P22-03) | PASS |
| `dsx/data/input_types.json` | regenerated from the homed `CHART_CAPABILITIES` (Pitfall 1) — IT040 now admits all ten uncertainty marks | PASS |
| `scripts/gen-finding-catalogue.py` | `_D05_ALLOWLIST_CODES` adds `DSX-VIZ-071` by **exact code** (not `DSX-VIZ-` prefix — would drag ~20 legacy uncited VIZ codes into enforcement red) | PASS |
| `references/finding-codes.md` | generated: Total 275→276, DSX-VIZ-071 row added (never hand-edited) | PASS |
| `references/chart-catalog.md` | new — 81 rows (60 dsx_admissible + 14 reference_only + 7 refusal), three axes + citation each, fenced-json payload with perceptual_ranks | PASS |
| `references/chart-selection.md`, `question-taxonomy.md`, `skills/dsx-visualize/SKILL.md` | 5-layer route-and-cite heuristic; perceptual line corrected to D-1 six-rank-with-ties; SKILL relationship list 10→11 | PASS |
| `tests/test_uncertainty_vocabulary.py` | new — DSX-VIZ-071 member/non-member/absent gate behaviour (`# D-05:` marker present) | PASS |
| `tests/test_chart_catalog_invariant.py` | new — band, three-axis shape, catalog↔vocab conformance (both directions), refusal drift guard, reference-only isolation, D-1 perceptual criterion, forbidden-citation guard, non-vacuity | PASS |
| `tests/test_selection_heuristic_docs.py` | new — 11-relationship enumeration, D-1 tie language + no superseded chain / no ranked density, catalog pointers, Munzner L1 cite, no-parallel-tree guard, no forbidden citations | PASS |
| `tests/test_viz_vocabulary_invariant.py`, `tests/test_finding_catalogue_invariant.py`, `tests/test_p19_categorical_rows.py`, `tests/test_phase20_zero_mint_close.py` | extended — 11th-key/facet-orthogonality assertions; count-pin 275→276 + set-identity `_MINTED_CODES ∪ {DSX-VIZ-071}` | PASS |

## Findings

**No code fixes required.** The three targeted risks are each closed by construction:

### Risk 1 — vocabulary widening → CLOSED (not a finding)

The new `_check_uncertainty_vocabulary` reads a **new optional field** `uncertainty_mark` and
is silent when it is blank (`is_blank(raw) → return`), so no existing spec changes behaviour;
it only *narrows* — it fires DSX-VIZ-071 (MEDIUM) when a declared mark is **not** one of the
ten `RELATIONSHIP_CHARTS["uncertainty"]` members (a membership lookup against the single source
of truth, never a computed threshold). The ten marks are homed into `CHART_CAPABILITIES
["interval-range"]`, which is the honest interval-shaped data signature and keeps Phase 21's
homing invariant green rather than opening a new admissibility surface. `facet_by` is proven
**absent** from every `RELATIONSHIP_CHARTS` / `CHART_CAPABILITIES` value and every `BANNED_TYPES`
key (`test_facet_by_is_orthogonal_not_a_chart_type`), so the "declaration, not a chart type"
claim is a runnable guard, not prose. The two new refusals (gauge, word_cloud) reuse the
existing `DSX-VIZ-001`, so the ban set grows without minting a code.

### Risk 2 — false-pass in the Markdown oracles → CLOSED (not a finding)

All four Markdown-reading invariants carry explicit non-vacuity anchors and derive their
"truth" from the **live code**, not a re-transcription: `test_chart_catalog_invariant` loads
`_mark_universe()` by path (single source of truth) and set-equals the dsx_admissible rows
against it in **both directions**, requires ≥60 rows + anchor marks present, reads the live
`BANNED_TYPES` for the refusal drift guard, and asserts the reference-only rows sit **outside**
the universe (so they can never widen the gate). `test_selection_heuristic_docs` collapses
whitespace before matching (CRLF/wrap-agnostic) and asserts both presence (11 relationships,
D-1 tie language, Cleveland & McGill 1984 / p.536–537) and absence (superseded `saturation →
volume` chain; `density` as a *ranked* channel — with a precise guard that still permits naming
density to say it is absent). None passes vacuously.

### Risk 3 — count-pin ripple weakening a zero-mint tell → CLOSED (not a finding)

Three files pin the live total in lockstep; all three were bumped 275→276 **and each keeps its
real invariant intact**: `test_finding_catalogue_invariant` adds `DSX-VIZ-071` to `_MINTED_CODES`
and proves the code SET equals `Phase-12 snapshot ∪ _MINTED_CODES` by symmetric-difference diff
(a cardinality-preserving mint-one/drop-one swap the count leg would miss is caught here);
`test_p19_categorical_rows` renames its method off the literal `275` and states the
categorical-minted-nothing proof is carried by rows-present + the absent DSX-STA-06x decade, not
the absolute total; `test_phase20_zero_mint_close` likewise re-anchors Phase 20's zero-mint tell
on the untouched DSX-STA reserve band + snapshot-subset, not the total. `DSX-VIZ-072` is
deliberately **not** minted (the ten §5.6 marks are paradigm-symmetric → no mark→paradigm
partition to gate; GA-3 / HQ-30).

## Observations (recorded, no action)

- **OBS-1 — illustrative prose in `viz.py:26` omits `error_bars_2d` from its frequentist/Bayesian
  bucketing.** The paradigm comment lists nine of the ten marks when illustrating D-12a symmetry;
  `error_bars_2d` (a frequentist 2-D mark) is in the tuple but not named in the prose. Cosmetic —
  the tuple is the source of truth and has all ten; no behaviour depends on the comment. Left as
  is (editing a docstring is not worth a churn commit against a clean gate).
- **OBS-2 — `references/finding-codes.md` emits 8 distinct `declared twice with different text`
  warnings** (DSX-CLM-020/021, DSX-COH-030, DSX-PAR-002, DSX-SPEC-070 ×3, DSX-VAL-021,
  DSX-VAL-060) under `gen --check`, which nonetheless exits 0 ("finding catalogue is current").
  These are **pre-existing** and structurally cannot be Phase-22-introduced: Phase 22 touched only
  viz/smells/spec among `dsx/` modules and none of those define CLM/COH/PAR/SPEC/VAL codes. Prior
  Log lines said "3" — that is the subset surfaced on the *suite's* stdout path
  (DSX-SPEC-070/DSX-VAL-021/DSX-VAL-060); the `--check` path surfaces all 8. Corrected here for
  the record; non-blocking, not this phase's to fix.

## Verdict

**PASS** — the production surface is clean; no fixes applied. The uncertainty vocabulary is a
narrowing membership gate on a new optional field, faceting is a proven-orthogonal declaration,
the catalog conforms to the live vocabulary by construction, and the single sanctioned mint
(DSX-VIZ-071) is additive by set-identity. Proceed to verification (same unit) then S2-5.
