---
phase: 22-catalog-spine-uncertainty-heuristic
plan: 03
type: execute
wave: 3
status: complete
requirements:
  - REQ-P22-01
  - REQ-P22-05
completed: 2026-09-03T04:33Z
---

# 22-03 SUMMARY — merged chart catalog + conformance/tie-break invariant

Wave 3 of the S2-3 execute unit. Ships the milestone's centre-of-gravity artifact:
`references/chart-catalog.md`, the merged citable chart catalog, plus the two
off-gate-path repo-integrity tests that keep it honest.

## What shipped

- **`references/chart-catalog.md`** (new) — **81 rows** (60 dsx_admissible + 14
  reference_only + 7 refusal), band 75–90, target ~80. Each row carries three axes
  (function = attributed FT nine-category axis with our own description; data_signature
  = a DSX input-type shape; perceptual_channel = a D-1 six-rank channel) + a per-row
  citation, and a `dsx_admissible | reference_only | refusal` flag. A human-readable
  intro + Markdown table + a single fenced ```json payload (perceptual_ranks map +
  rows array) parsed by the invariant test with the input-type-inventory.md idiom
  (`re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)`).
- **`tests/test_chart_catalog_invariant.py`** (new) — stdlib unittest, 8 clauses, all
  green: band; three-axes+citation shape; catalog↔vocabulary conformance both
  directions; seven-refusal drift guard vs live BANNED_TYPES; reference-only isolation;
  D-1 perceptual tie-break structural criterion; citation traceability; non-vacuity.

## How correctness is guaranteed (not asserted)

- The 60 dsx_admissible rows were **generated from the live `_mark_universe()`**, not
  hand-transcribed — the conformance clause set-equals the admissible rows to
  `_mark_universe()` (imported by path from `tests/test_viz_vocabulary_invariant.py`,
  the single source of truth), both directions, no duplicate.
- The 7 refusal rows are exactly the live `BANNED_TYPES` keys; each `banning_code`
  reads `BANNED_TYPES[bt]["code"]` (DSX-VIZ-001) live, so a stale catalog turns the
  test red at commit (drift guard, T-22-07).
- The 14 reference_only names are all outside `_mark_universe()` — the catalog never
  widens what the gate admits (T-22-09).

## D-1 perceptual_ranks (six ranks WITH TIES, HQ-27 D-1)

`position_common=1 · position_nonaligned=2 · {length, direction, angle}=3 · area=4 ·
{volume, curvature}=5 · {shading, colour_saturation}=6`. The tie-break test asserts
`rank(a) <= rank(b)` throughout and `rank(length) == rank(angle)` both ways — never a
strict `<` across a tied pair. `density` is absent (not in the 1984 paper). Pure
ordering assertion, off the gate path, no computation (REQ-P22-05, GA-3).

## Decision recorded loudly (persona-lite, within plan latitude)

**Reference-only rows sourced to FT categories / Wilke chapters, not DVC-with-URL.**
Plan 22-03 Task 1 permits FT / Wilke-ch.5 / DVC sourcing and requires any *DVC-attested*
row to carry a **build-time-resolved** URL (never name-generated — the `treemap.html`
trap, HQ-27 T2-4). This firing cannot resolve/verify live DVC URLs, and the brief's
standard is "prefer the smaller, provable claim." So all 14 reference-only rows are
cited to an FT function category (D-3) or a Wilke chapter (T2-2) — no per-method URL
asserted — and the Ribecca-lineage independence caveat (GC + DVC + FT are one lineage,
not three authorities) is stated in the intro, never claimed as triangulation per row.
This is fully within the plan's stated source set and strictly more provable than
guessing URLs. Rigour > reliability. No off-limits citation (Abela / Few's Graph
Selection Matrix / the 8 HQ-27 unverified items) appears — enforced by clause (g).

## Gates (all orchestrator-run on the final post-build tree)

- `python -m unittest tests.test_chart_catalog_invariant -v` → **8 OK**.
- Plan Task-2 verify one-liner → `rows 81 ok; length==angle tie; no density`.
- Full suite `python -m unittest discover -s tests` → **1489 OK** (1481 → 1489, +8;
  clean tree, stray DECISIONS.jsonl cleared per standing note). Same 3 pre-existing
  "declared twice" warnings, unchanged.

## Not done here (boundary)

- Catalog is a **reference doc, not a gate check** — it routes to codes, never
  re-implements a threshold. Zero new finding code minted this wave (mint stays at 276
  from Wave 2's DSX-VIZ-071).
- The temp deterministic generator (`_build_catalog.py`) was run once and **deleted**;
  only the `.md` artifact ships.
- **Wave 4 (22-04)** — the 5-layer heuristic route-and-cite + the chart-selection.md
  perceptual-line correction + SKILL.md 10→11 relationships — remains. S2-3 checkbox
  stays UNCHECKED until Wave 4 lands.
