# Phase 21: Viz vocabulary reconciliation — Research

**Researched:** 2026-09-03
**Domain:** repo-internal Python data-structure reconciliation (chart-mark vocabulary); zero external dependencies
**Confidence:** HIGH — every claim below is a direct read of the live tree (file + line span), not training knowledge. No web research was performed per task scope; this phase has no external/library surface to research.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**D-01 — the every-mark-has-a-home invariant's exact scope (REQ-P21-01).** The invariant is
two directional clauses over a precisely-bounded mark universe, implemented as **one
repo-integrity test off the gate path** (`tests/`, not `dsx/checks/`).

- **Mark universe** = union of marks named in `RELATIONSHIP_CHARTS` values,
  `CHART_CAPABILITIES` values, `EXTRA_MARKS` values, `LENGTH_ENCODED`, `DENSITY_MARKS`, and
  `STACKED_MARKS`, **minus `BANNED_TYPES`** (banned marks are exempt from homing; covered by
  REQ-P21-02's refusal invariant instead).
- **Capability home** = membership in some `CHART_CAPABILITIES` value **or** some
  `EXTRA_MARKS` value (gate-faithful: this is exactly what `_check_input_type_matrix` /
  DSX-VIZ-013 admits from).
- **Relationship home** = membership in some `RELATIONSHIP_CHARTS` value.
- **Clause 1 (capability-completeness, hard).** Every mark in the universe has a capability
  home. Homes the 9 relationship-listed capability-orphans + `kde`.
- **Clause 2 (relationship-completeness, hard, with an explicit exempt allowlist).** Every
  mark in the universe either has a relationship home **or** is on a frozen
  `CAPABILITY_ONLY` allowlist (the ~14 capability-only marks — not homed into
  `RELATIONSHIP_CHARTS` this phase; promotion is a Phase 22 decision).
- Do **not** touch `CHART_CAPABILITIES` for `population_pyramid`/`butterfly` — already
  capability-homed via `EXTRA_MARKS[IT011]`; their homing work is relationship-only.

**D-02 — refusal-entry representation (REQ-P21-02): enrich `BANNED_TYPES` in place.**
Promote `BANNED_TYPES` from `dict[str, str]` to `dict[str, dict[str, str]]`, each value a
record `{reason, code, citation}`. `reason` = the existing distortion string; `code` =
`"DSX-VIZ-001"` for all five (the code `_check_banned` emits); `citation` = the D-05
perception source (HQ-27 Tier-3, batched, non-blocking). `_check_banned` changes at exactly
one line (`detail=BANNED_TYPES[chart_type]["reason"]`); the `in` membership check is
unchanged (dict keys, unaffected by value-type promotion). Rejected alternatives: a parallel
`REFUSAL_ENTRIES` sub-map (drift surface — a second invariant to police) and a
`NamedTuple`/dataclass record (introduces a new gate-adjacent type against the codebase's
plain-dict house style; the invariant test carries the completeness guarantee instead).

**Zero new codes holds (REQ-P21-03).** The refusal entries cross-reference the existing
`DSX-VIZ-001`; `citation` is new metadata, not a new check.

### Claude's Discretion

The **homing guidance table** (which family/relationship each orphan lands in) is
"**proposed, plan-checker-verifiable, not frozen**" — the planner may choose the narrowest
correct home per mark, including picking between the two alternatives CONTEXT lists for
`waterfall` (composition vs categorical-value) and `bump` (categorical-multi vs
time-series). Any choice is valid provided: (a) the mark becomes gate-faithfully admissible
for a signature it genuinely fits, (b) no false negative is introduced, (c) zero new codes.
The exact citation string populated into each `BANNED_TYPES[...]["citation"]` field is also
discretionary in content (subject to HQ-27 Tier-3 sourcing — see Common Pitfall 5 below) as
long as the field is non-empty and the loop annotates HQ-27 with the per-mark mapping.

### Deferred Ideas (OUT OF SCOPE)

- **Carried to Phase 22:** whether any `CAPABILITY_ONLY` mark (`column`, `grouped_bar`, …)
  should be promoted to a relationship home — decided there with per-entry relationship
  citations, not pre-empted in Phase 21.
- **HQ-27 Tier-3** citation *signing* (operator confirms sourcing authenticity) — Phase 21
  builds the structure and populates the citation *pointers*; the sign-off is non-blocking
  for Phase 21 ship, drained at S5-2.
- **HQ-28** veto window on D-01/D-02 shape — non-blocking, silence = accept.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P21-01 | Every-mark-has-a-home invariant test; home the 12 orphans | Full mark-universe accounting (below) proves the 12-item orphan list is exact and complete; exact line targets given for every addition; test idiom + import mechanics (incl. the hyphenated-filename `importlib` trick for `EXTRA_MARKS`) documented with a working skeleton |
| REQ-P21-02 | Banned types → first-class refusal entries, code + citation | Exact one-line `_check_banned` edit identified and verified against the AST-based catalogue generator (confirms it is a zero-mint change mechanically, not by claim); repo-wide grep confirms no other `BANNED_TYPES` reader breaks; HQ-27 Tier-3 source table cross-referenced per banned type, with one gap flagged (`radar` has no explicit doctrine source in the prepared pack) |
| REQ-P21-03 | Zero new codes, set-identity diff vs 275 | Literal S0-2 diff commands reproduced; AST extraction mechanics of `scripts/gen-finding-catalogue.py::extract()` traced to prove the `detail=` kwarg is never read for code derivation, so the D-02 edit cannot mint or alter a code even mechanically |
</phase_requirements>

## Summary

This phase touches exactly four source files (`dsx/checks/viz.py`, `dsx/spec.py`,
`scripts/gen-input-types.py`, `dsx/checks/smells.py` — read-only for the last) plus one new
test file under `tests/`. There is no new package, no new check module, no new gate-registered
code path, and (verified mechanically via the finding-catalogue generator's AST extraction
logic) no possible new finding code. The work is: (1) add ~10 marks to existing
`CHART_CAPABILITIES` / `RELATIONSHIP_CHARTS` entries at named line spans, (2) promote
`BANNED_TYPES` values from `str` to a 3-field dict and change one `detail=` expression, (3)
write one `unittest.TestCase`-style repo-integrity test that reads these live structures and
asserts the two D-01 clauses plus refusal-record completeness, and (4) re-run the existing
275-code set-identity diff (already built, unchanged by this phase) to prove zero mint.

A full re-derivation of the mark universe (below) independently reproduces the CONTEXT's
12-orphan list, the ~14-item `CAPABILITY_ONLY` allowlist, and the population_pyramid/butterfly
correction exactly — the ground truth is internally consistent and plan-checker-verifiable.

One implementation subtlety not spelled out in CONTEXT: **`EXTRA_MARKS` (in
`scripts/gen-input-types.py`) only reaches the gate through the *generated* file
`dsx/data/input_types.json`, and that file is a static artifact — editing `EXTRA_MARKS` or
`CHART_CAPABILITIES` alone does not change gate behavior for visuals that declare an IT id
(e.g. `data_input_type: IT011`) until `python scripts/gen-input-types.py` is re-run and the
regenerated JSON is committed.** This must be an explicit task, not an assumed side effect.

**Primary recommendation:** implement the 10 dict edits, regenerate
`dsx/data/input_types.json`, write the invariant test using the exact structure-reading idiom
of `tests/test_input_types.py` (not the text-parsing idiom of
`tests/test_finding_catalogue_invariant.py` — these are live Python objects, not a generated
Markdown file), loading `EXTRA_MARKS` via `importlib.util.spec_from_file_location` (the same
trick `tests/test_phase20_zero_mint_close.py::_load_generator()` already uses for the
hyphenated `scripts/gen-finding-catalogue.py`), then re-run
`python3 -m unittest discover -s tests -v` and the three-way 275 diff.

## Architectural Responsibility Map

This is a single-tier Python library/CLI repo (no browser/server/DB tiers). Tiers below are
this codebase's own module layers.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Recommendation surface (relationship → marks) | `dsx/checks/viz.py` (`RELATIONSHIP_CHARTS`) | — | Consumed by `_check_relationship_match` (DSX-VIZ-010/011/012) and `dsx/input_types.py:100` |
| Admissibility surface (input shape → marks) | `dsx/spec.py` (`CHART_CAPABILITIES`) | `dsx/checks/viz.py` (`_check_input_type_matrix`) | The gate-enforced surface (DSX-VIZ-013); also consumed by `dsx/input_types.py:94`, `scripts/gen-input-types.py:143`, `dsx/spec.py:1647` (vocab dump), `tests/test_input_types.py:32` |
| Per-shape admissibility addenda | `scripts/gen-input-types.py` (`EXTRA_MARKS`) | `dsx/data/input_types.json` (generated artifact) | Only reachable through the generated JSON — a build step, not a live import |
| Refusal/ban surface | `dsx/checks/viz.py` (`BANNED_TYPES`, `_check_banned`) | — | Sole consumer of its own dict; 2 call sites, both in the same file |
| Repo-integrity verification | `tests/` (new invariant test + existing `test_finding_catalogue_invariant.py`) | — | Off the `dsx run` gate path by construction — `tests/` is never imported by `dsx.cli.GATE_PROFILES` |
| Citation/doctrine sourcing | `.planning/HUMAN-QUEUE.md` (HQ-27 Tier-3) + `.planning/v2.4-D05-EVIDENCE-PACK.md` | `BANNED_TYPES[...]["citation"]` (code) | Human-signed source of truth lives in planning docs; the code field only points at it |

## Standard Stack

**Not applicable.** This phase installs no packages and adds no dependency. Everything used
is already in the repo: Python stdlib (`unittest`, `re`, `pathlib`, `importlib.util`, `json`)
and the existing `dsx` package. No `pip install` / `npm install` step belongs in this phase's
plan.

**Version verification:** N/A — no packages to verify.

## Package Legitimacy Audit

**Not applicable — this phase installs no external packages.** Skip the Package Legitimacy
Gate entirely; there is nothing to check against a registry.

## Architecture Patterns

### System Architecture Diagram

```
                      ┌─────────────────────────────┐
                      │  references/input-type-      │
                      │  inventory.md  (source of     │
                      │  truth for IT001-IT040 prose) │
                      └───────────────┬───────────────┘
                                      │ read by
                                      ▼
   scripts/gen-input-types.py  ── FAMILY{} + EXTRA_MARKS{} ──┐
        │ imports (lazy, inside main())                       │
        ▼                                                      │
   dsx/spec.py :: CHART_CAPABILITIES{}  ◄── edited here (D-01) │
        │                                                      │
        │ admissible = CHART_CAPABILITIES[family] ∪ EXTRA_MARKS[it_id]
        ▼                                                      │
   dsx/data/input_types.json  (GENERATED — must be regenerated)◄
        │ loaded by
        ▼
   dsx/input_types.py :: input_type_record(it_id)["admissible"]
        │
        ▼
   dsx/checks/viz.py :: _check_input_type_matrix()  ──► DSX-VIZ-013
        ▲                                       ▲
        │ RELATIONSHIP_CHARTS{} ◄── edited here  │ CHART_CAPABILITIES.get(family)
        │ (D-01, relationship home)              │ (coarse-family path — reads
        │                                        │  CHART_CAPABILITIES directly,
   dsx/checks/viz.py :: BANNED_TYPES{} ◄── edited│  no regeneration needed)
        │ (D-02: str → {reason,code,citation})   │
        ▼                                        │
   dsx/checks/viz.py :: _check_banned()  ──► DSX-VIZ-001 (existing code, unchanged)
        │
        ▼
   tests/  (NEW invariant test, off gate path) ── reads all of the above live,
                                                    asserts D-01 clause 1+2 +
                                                    refusal-record completeness

   tests/test_finding_catalogue_invariant.py (UNCHANGED) ── reads
   references/finding-codes.md (UNCHANGED, generated from report.add() call sites,
   unaffected by the detail= kwarg edit) ── proves REQ-P21-03 (275 → 275)
```

The primary use case (an author declares `data_input_type: IT011` and `type: population_pyramid`)
traces: inventory → `FAMILY`/`EXTRA_MARKS` → generated JSON → `input_type_record()` →
`_check_input_type_matrix` → pass/fail. The **coarse-family path** (author declares
`data_input_type: categorical-multi` instead of `IT011`) traces a **shorter, different**
route straight to `CHART_CAPABILITIES` and never sees `EXTRA_MARKS` — see Pitfall 1.

### Recommended File-Change Set
```
dsx/spec.py                       # CHART_CAPABILITIES: add marks to 4-5 existing families (lines 296-325)
dsx/checks/viz.py                 # RELATIONSHIP_CHARTS: add kde/population_pyramid/butterfly (lines 17-28)
                                   # BANNED_TYPES: str -> {reason,code,citation} (lines 36-42)
                                   # _check_banned: one-line detail= change (line 86)
scripts/gen-input-types.py        # only if any orphan is homed via a NEW EXTRA_MARKS entry
                                   # rather than a base CHART_CAPABILITIES addition (lines 77-86)
dsx/data/input_types.json         # REGENERATE: python scripts/gen-input-types.py (any CHART_CAPABILITIES
                                   # or EXTRA_MARKS edit requires this or the IT-id gate path goes stale)
tests/test_viz_vocabulary_invariant.py   # NEW — every-mark-has-a-home + refusal-completeness (see below)
```
(Test filename is a naming *suggestion* following the existing `test_<subject>.py` convention
seen across `tests/`; not prescriptive.)

### The exact live structures (verified, with line spans)

| Structure | File:Lines | Shape | Current content |
|---|---|---|---|
| `RELATIONSHIP_CHARTS` | `dsx/checks/viz.py:17-28` | `dict[str, tuple[str,...]]`, 10 keys | comparison, trend, part_to_whole, distribution, correlation, deviation, ranking, flow, geographic, composition_over_time |
| `CHART_CAPABILITIES` | `dsx/spec.py:296-325` | `dict[str, frozenset[str]]`, 15 keys | bivariate-simple, bivariate-dual, trivariate, categorical-value, categorical-multi, time-series, interval-range, grouped-categorical, composition, hierarchical, matrix, event-time, single-value, geospatial, financial-ohlc |
| `EXTRA_MARKS` | `scripts/gen-input-types.py:77-86` | `dict[str, set[str]]`, 8 IT-id keys | IT011, IT014, IT036, IT017, IT022, IT024, IT037, IT028 |
| `BANNED_TYPES` | `dsx/checks/viz.py:36-42` | `dict[str, str]` (D-02 target: `dict[str, dict[str,str]]`) | 3d_bar, 3d_pie, 3d_line, radar, dual_axis_line |
| `LENGTH_ENCODED` | `dsx/checks/viz.py:32-34` | `set[str]`, 13 marks | bar, horizontal_bar, stacked_bar, area, stacked_area, waterfall, diverging_bar, column, histogram, waffle, funnel, stream, grouped_bar |
| `DENSITY_MARKS` | `dsx/checks/smells.py:12` | `set[str]`, 3 marks | density, kde, violin |
| `STACKED_MARKS` | `dsx/checks/smells.py:13` | `set[str]`, 3 marks | stacked_bar, stacked_area, stream |
| `_check_banned` (consumer) | `dsx/checks/viz.py:80-89` | function | line 81 `in` membership (unchanged), line 86 `detail=BANNED_TYPES[chart_type]` (→ `["reason"]`) |
| `_check_input_type_matrix` (consumer) | `dsx/checks/viz.py:133-191` | function | IT-id path uses generated JSON `admissible` (includes `EXTRA_MARKS`); coarse-family path uses `CHART_CAPABILITIES.get(dit)` directly (does **not** include `EXTRA_MARKS`) — line 173 |

### Full mark-universe accounting (independently re-derived, matches CONTEXT exactly)

Computed by set algebra directly from the tables above — this is the ground truth the
invariant test must reproduce programmatically, given here as a hand-check the plan-checker
can use.

- **Relationship-homed marks (33):** bar, horizontal_bar, dot_plot, bullet, line, area,
  sparkline, slope, stacked_bar, treemap, waffle, pie, histogram, box, violin, density, ecdf,
  strip, scatter, hexbin, heatmap, diverging_bar, waterfall, dumbbell, bump, sankey, chord,
  funnel, choropleth, symbol_map, cartogram, stacked_area, stream.
- **Base-capability-homed marks (38, from `CHART_CAPABILITIES` alone):** line, scatter, area,
  bar, column, horizontal_bar, grouped_bar, multi_line, bubble, heatmap, hexbin, pie, donut,
  waffle, dot_plot, bullet, stacked_bar, slope, stream, sparkline, box, violin, treemap,
  stacked_area, sunburst, icicle, circle_pack, chord, timeline, funnel, gantt, big_number,
  choropleth, symbol_map, cartogram, candlestick, ohlc_bar, column_range.
- **Capability-only-via-EXTRA_MARKS (2):** population_pyramid, butterfly (both only in
  `EXTRA_MARKS["IT011"]`).
- **Neither surface (1):** kde (only in `DENSITY_MARKS`, a property set, not a home).

**Relationship-set − capability-set = the 9 orphans:** histogram, density, ecdf, strip,
diverging_bar, waterfall, dumbbell, bump, sankey — exact match to CONTEXT/REQ-P21-01.

**Capability-set − relationship-set = the 14-item `CAPABILITY_ONLY` allowlist:** column,
grouped_bar, multi_line, bubble, donut, sunburst, icicle, circle_pack, timeline, gantt,
big_number, candlestick, ohlc_bar, column_range — exact match to CONTEXT's finding.

**9 + kde(both) + population_pyramid/butterfly(relationship-only) = 12** — exactly
REQ-P21-01's enumerated orphan list, with zero marks left unaccounted for and zero marks
double-counted. `BANNED_TYPES`' five keys (3d_bar, 3d_pie, 3d_line, radar, dual_axis_line)
appear in **none** of the six structures above — confirmed absent from the universe, matching
D-02's "silently absent" framing exactly.

### Homing guidance table, with exact target line spans

| Mark | Add to | File:Lines to edit | Alt considered |
|---|---|---|---|
| histogram, density, ecdf, strip | `CHART_CAPABILITIES["interval-range"]` | `dsx/spec.py:309` | — |
| diverging_bar | `CHART_CAPABILITIES["categorical-value"]` | `dsx/spec.py:300-302` | — |
| waterfall | `CHART_CAPABILITIES["composition"]` | `dsx/spec.py:313-315` | `categorical-value` (spec.py:300-302) |
| dumbbell | `CHART_CAPABILITIES["categorical-multi"]` | `dsx/spec.py:303-305` | — |
| bump | `CHART_CAPABILITIES["categorical-multi"]` | `dsx/spec.py:303-305` | `time-series` (spec.py:306-308) |
| sankey | `CHART_CAPABILITIES["matrix"]` | `dsx/spec.py:317` | — |
| kde | `RELATIONSHIP_CHARTS["distribution"]` **and** `CHART_CAPABILITIES["interval-range"]` | `dsx/checks/viz.py:21` and `dsx/spec.py:309` | — |
| population_pyramid | `RELATIONSHIP_CHARTS["distribution"]` | `dsx/checks/viz.py:21` | `comparison` (viz.py:18) |
| butterfly | `RELATIONSHIP_CHARTS["comparison"]` | `dsx/checks/viz.py:18` | — |

All nine capability additions land in an **existing base `CHART_CAPABILITIES` family**, not
a new `EXTRA_MARKS` entry — per the guidance ("prefer the narrowest home that removes the
friction ... base `CHART_CAPABILITIES` family for a broadly-admissible signature"), so no new
`EXTRA_MARKS` key is required by the proposed table. If the plan instead prefers an
`EXTRA_MARKS[specific-IT]` route for any of these (e.g. `waterfall` only for a specific IT id
rather than the whole `composition` family), that is within discretion but **must** be
followed by the `dsx/data/input_types.json` regeneration step (Pitfall 1).

### Pattern to copy: `EXTRA_MARKS` is only importable via `importlib.util`

`scripts/gen-input-types.py` has no `__init__.py` sibling and its filename contains hyphens
(`gen-input-types.py`), so `import scripts.gen_input_types` is not valid Python — there is no
such module. The only way to read its module-level `EXTRA_MARKS` dict from a test is the
`importlib.util.spec_from_file_location` pattern already used in
`tests/test_phase20_zero_mint_close.py:79-84` for the sibling script
`scripts/gen-finding-catalogue.py`:

```python
# Source: tests/test_phase20_zero_mint_close.py:79-84 (existing precedent, same
# hyphenated-filename problem, same script/ directory, same "load constants only,
# never call __main__" contract)
import importlib.util
import pathlib

_ROOT = pathlib.Path(__file__).resolve().parents[1]
_GEN_INPUT_TYPES = _ROOT / "scripts" / "gen-input-types.py"

def _load_gen_input_types():
    """Import scripts/gen-input-types.py without running its __main__ guard."""
    spec = importlib.util.spec_from_file_location("gen_input_types_mod", _GEN_INPUT_TYPES)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

EXTRA_MARKS = _load_gen_input_types().EXTRA_MARKS
```

`gen-input-types.py`'s module-level code only defines dicts/lists (`FAMILY`, `EXTRA_MARKS`,
`NARROWED`, `SHARED_SIGNATURE_GROUPS`) and a `main()` function; the `CHART_CAPABILITIES`
import happens *inside* `main()` (lazily, per its own docstring at line 132-134), so
`exec_module` alone is side-effect-free and does not require `dsx` to already be
importable — matching the precedent exactly.

### Pattern to copy: test idiom (structural, not text-parsing)

Use the `tests/test_input_types.py` idiom (import live Python objects, iterate with
`self.subTest`), **not** the `tests/test_finding_catalogue_invariant.py` idiom (regex over a
generated Markdown file). The new invariant reads Python dicts/sets directly — there is no
CRLF concern for this test (no line-anchored parsing of a text file), unlike the Markdown
catalogue tests. Skeleton:

```python
# Source: modeled on tests/test_input_types.py (import style) and
# tests/test_phase20_zero_mint_close.py (multi-clause oracle style, docstring
# citing REQ ids, "Run: python -m unittest ..." footer convention)
from __future__ import annotations

import unittest

from dsx.checks.smells import DENSITY_MARKS, STACKED_MARKS
from dsx.checks.viz import BANNED_TYPES, LENGTH_ENCODED, RELATIONSHIP_CHARTS
from dsx.spec import CHART_CAPABILITIES

# ... _load_gen_input_types() / EXTRA_MARKS as above ...

CAPABILITY_ONLY = frozenset({
    "column", "grouped_bar", "multi_line", "bubble", "donut", "sunburst",
    "icicle", "circle_pack", "timeline", "gantt", "big_number",
    "candlestick", "ohlc_bar", "column_range",
})  # frozen per D-01 clause 2; a mark added here without justification fails review


def _mark_universe() -> frozenset[str]:
    marks: set[str] = set()
    for group in RELATIONSHIP_CHARTS.values():
        marks.update(group)
    for group in CHART_CAPABILITIES.values():
        marks.update(group)
    for group in EXTRA_MARKS.values():
        marks.update(group)
    marks.update(LENGTH_ENCODED, DENSITY_MARKS, STACKED_MARKS)
    return frozenset(marks) - frozenset(BANNED_TYPES)


def _capability_homed() -> frozenset[str]:
    homed: set[str] = set()
    for group in CHART_CAPABILITIES.values():
        homed.update(group)
    for group in EXTRA_MARKS.values():
        homed.update(group)
    return frozenset(homed)


def _relationship_homed() -> frozenset[str]:
    homed: set[str] = set()
    for group in RELATIONSHIP_CHARTS.values():
        homed.update(group)
    return frozenset(homed)


class TestEveryMarkHasAHome(unittest.TestCase):
    def test_every_mark_has_a_capability_home(self):
        universe = _mark_universe()
        homed = _capability_homed()
        orphans = sorted(universe - homed)
        self.assertFalse(orphans, f"marks with no capability home: {orphans}")

    def test_every_mark_has_a_relationship_home_or_is_allowlisted(self):
        universe = _mark_universe()
        homed = _relationship_homed()
        unhomed = universe - homed
        not_allowlisted = sorted(unhomed - CAPABILITY_ONLY)
        self.assertFalse(
            not_allowlisted,
            f"marks with no relationship home and not on CAPABILITY_ONLY: {not_allowlisted}",
        )

    def test_capability_only_allowlist_is_exact_not_a_superset(self):
        # every allowlisted mark must actually lack a relationship home; an
        # allowlist entry that HAS a relationship home is stale, not loud.
        stale = sorted(CAPABILITY_ONLY & _relationship_homed())
        self.assertFalse(stale, f"CAPABILITY_ONLY entries that already have a relationship home: {stale}")


class TestRefusalEntryCompleteness(unittest.TestCase):
    def test_every_banned_type_has_a_complete_refusal_record(self):
        for mark, record in BANNED_TYPES.items():
            with self.subTest(mark):
                self.assertIsInstance(record, dict)
                for field in ("reason", "code", "citation"):
                    self.assertIn(field, record)
                    self.assertTrue(str(record[field]).strip(), f"{mark}.{field} is empty")

    def test_every_refusal_code_is_the_code_check_banned_emits(self):
        for mark, record in BANNED_TYPES.items():
            with self.subTest(mark):
                self.assertEqual(record["code"], "DSX-VIZ-001")


if __name__ == "__main__":
    unittest.main()
```

This is a **pattern to adapt**, not a literal file to paste — the plan should size it to
however many `.py` test methods the plan-checker wants, but the four assertions above are the
minimum that cover D-01 clause 1, D-01 clause 2 (+ allowlist staleness), and D-02's
completeness clause.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Loading a hyphenated-filename script's constants in a test | A `sys.path` hack, a file copy, or a rename of `gen-input-types.py` | `importlib.util.spec_from_file_location` (exact precedent: `tests/test_phase20_zero_mint_close.py:79-84`) | Already solved once in this repo for the sibling script; renaming `gen-input-types.py` would ripple into its own docstring-documented `python scripts/gen-input-types.py` run command and any doc references |
| A second registry for refusal citations | A parallel `REFUSAL_ENTRIES` dict keyed on the same marks | Enrich `BANNED_TYPES` in place (D-02, already decided) | Two synchronized maps is exactly the drift class REQ-P21-02 exists to prevent |
| Verifying the 275-code baseline | A new counting script or a hand count | `tests/test_finding_catalogue_invariant.py` (already exists, already asserts 275 two ways) + the S0-2 grep (`grep -oE '(DSX-[A-Z]+-[0-9]+\|SQL-[0-9]+)' references/finding-codes.md \| sort -u \| wc -l`) | The oracle already exists and is proven correct; this phase's job is to confirm it still reads 275 after the edits, not rebuild it |

**Key insight:** every tool this phase needs to prove its own correctness (the 275 diff, the
hyphenated-import trick, the `subTest`-per-item idiom) already exists in `tests/` as a working
precedent from an earlier phase. The plan should point at these, not reinvent them.

## Common Pitfalls

### Pitfall 1: Editing `CHART_CAPABILITIES`/`EXTRA_MARKS` without regenerating `dsx/data/input_types.json`
**What goes wrong:** A visual that declares `data_input_type: IT014` (an IT id) still gets a
DSX-VIZ-013 false positive for `histogram` even after `dsx/spec.py`'s `CHART_CAPABILITIES["interval-range"]`
is edited, because `_check_input_type_matrix`'s IT-id path (`dsx/checks/viz.py:154-156`) reads
`input_type_record(it_id)["admissible"]`, which comes from the **static, generated**
`dsx/data/input_types.json` — not from `CHART_CAPABILITIES` live.
**Why it happens:** `scripts/gen-input-types.py` computes `admissible = set(CHART_CAPABILITIES[family]) | EXTRA_MARKS.get(it_id, set())`
at generation time and writes it to JSON (`scripts/gen-input-types.py:143`); nothing
re-derives it at gate-check time.
**How to avoid:** after any `CHART_CAPABILITIES`/`EXTRA_MARKS` edit, run
`python scripts/gen-input-types.py` and commit the regenerated
`dsx/data/input_types.json`. Note the **coarse-family path** (`data_input_type: interval-range`,
no IT id) does *not* need regeneration — it reads `CHART_CAPABILITIES` directly
(`dsx/checks/viz.py:173`) — so the two paths can silently disagree if only one edit is made.
**Warning signs:** a manual/plan-checker smoke test that declares `data_input_type: IT014, type: histogram`
still fires DSX-VIZ-013 after the `CHART_CAPABILITIES` edit but passing the coarse family name
works.

### Pitfall 2: Treating `population_pyramid`/`butterfly` as needing a `CHART_CAPABILITIES` edit
**What goes wrong:** Adding them to a `CHART_CAPABILITIES` family would be redundant (they are
already reachable via `EXTRA_MARKS["IT011"]`) and risks over-widening a base family the way
D-01's rationale explicitly warns against.
**How to avoid:** touch `RELATIONSHIP_CHARTS` only for these two marks.

### Pitfall 3: Forgetting the `_MINTED_CODES`/allowlist style precedent does not apply here
**What goes wrong:** Phase 21's invariant test might be modeled too closely on
`test_finding_catalogue_invariant.py`'s CRLF-tolerant regex idiom, which is unnecessary
overhead — that idiom exists because that test parses a **generated Markdown file**. This
phase's invariant test reads **live Python dict/set objects**, so there is no line-anchoring
or CRLF concern to defend against.
**How to avoid:** use the `tests/test_input_types.py` idiom (direct object iteration), not the
regex-over-Markdown idiom, for the new test. (CRLF discipline from `.claude/CLAUDE.md` still
applies to any *other* file this phase edits/reads with a line-anchored regex — there are
none in this phase's scope.)

### Pitfall 4: Picking both alternatives for `waterfall`/`bump`
**What goes wrong:** CONTEXT lists an "alt" family for `waterfall` (categorical-value) and
`bump` (time-series). Adding to both the primary and the alt family is not wrong per se, but
it silently doubles the admissibility surface beyond what was reviewed in the persona round,
and the invariant test's "gate-faithful" framing means any addition is now gate behavior —
undocumented extra admissibility is an unscoped expansion of exactly the kind D-01 was
written to prevent for the 14-item allowlist.
**How to avoid:** pick one family per mark; if both are added, record the reason explicitly
(matching the rigor of the rest of D-01's rationale) rather than defaulting silently to both.

### Pitfall 5: The `radar` refusal citation has no doctrine source in the prepared HQ-27 Tier-3 pack
**What goes wrong:** `.planning/v2.4-D05-EVIDENCE-PACK.md` Tier 3 (lines 58-63) maps: Few
2006/2013 → gauges (not a `BANNED_TYPES` entry — gauges are excluded via `NARROWED` in
`gen-input-types.py`, a different mechanism), Harris 2011 → word clouds (also not a
`BANNED_TYPES` entry), Tufte 1983 → "chartjunk one-offs" (best generic fit for
`3d_bar`/`3d_pie`/`3d_line`), Muth 2018 → dual-axis (exact match: `dual_axis_line`). **No Tier-3
source is named for `radar`.** The closer fit is actually **Munzner 2014 ch.6** ("no
unjustified 3D," Tier 2 T2-6) for the three 3D bans, and Tufte/Munzner's general
proportional-encoding doctrine covers `radar`'s "area scales with the square of the value"
distortion (`viz.py`'s own existing `reason` string), but this exact source-to-mark mapping is
**not pre-resolved** in the evidence pack.
**How to avoid:** this phase should still populate `citation` for all five (non-empty is
required by the invariant test), but the plan must explicitly annotate HQ-27 (per CONTEXT's
"S1-3 must annotate HQ-27's Tier-3 batch with the specific banned-type → source mapping")
with the `radar` gap flagged for the operator to confirm or supply a better source at S5-2 —
do not silently reuse the Tufte citation for `radar` without flagging it as the least-precise
match of the five.
**Warning signs:** a citation field that is non-empty but was picked without noting the
mapping ambiguity in the HQ-27 annotation.

## Code Examples

### D-01: `CHART_CAPABILITIES` addition (one entry shown; repeat per homing table)
```python
# Source: dsx/spec.py:309 (live) — before
"interval-range": frozenset({"box", "violin", "dot_plot", "bar", "horizontal_bar", "bullet"}),
# after (adds histogram, density, ecdf, strip, kde)
"interval-range": frozenset({
    "box", "violin", "dot_plot", "bar", "horizontal_bar", "bullet",
    "histogram", "density", "ecdf", "strip", "kde",
}),
```

### D-01: `RELATIONSHIP_CHARTS` addition
```python
# Source: dsx/checks/viz.py:21 (live) — before
"distribution": ("histogram", "box", "violin", "density", "ecdf", "strip"),
# after (adds kde, population_pyramid)
"distribution": ("histogram", "box", "violin", "density", "ecdf", "strip", "kde", "population_pyramid"),
```
```python
# Source: dsx/checks/viz.py:18 (live) — before
"comparison": ("bar", "horizontal_bar", "dot_plot", "bullet"),
# after (adds butterfly)
"comparison": ("bar", "horizontal_bar", "dot_plot", "bullet", "butterfly"),
```

### D-02: `BANNED_TYPES` enrichment
```python
# Source: dsx/checks/viz.py:36-42 (live) — before
BANNED_TYPES = {
    "3d_bar": "3D bars distort length with perspective and occlude the back rows.",
    "3d_pie": "3D pie exaggerates the slices nearest the viewer.",
    "3d_line": "3D lines make position unreadable without adding information.",
    "radar": "Radar area scales with the square of the value and depends on axis order.",
    "dual_axis_line": "Two y-scales let any pair of series be made to look correlated.",
}
# after
BANNED_TYPES = {
    "3d_bar": {
        "reason": "3D bars distort length with perspective and occlude the back rows.",
        "code": "DSX-VIZ-001",
        "citation": "<Tufte 1983 / Munzner 2014 ch.6 — see Pitfall 5, HQ-27 Tier-3>",
    },
    # ... 3d_pie, 3d_line same citation family ...
    "radar": {
        "reason": "Radar area scales with the square of the value and depends on axis order.",
        "code": "DSX-VIZ-001",
        "citation": "<flag for HQ-27 — no exact Tier-3 source pre-mapped, see Pitfall 5>",
    },
    "dual_axis_line": {
        "reason": "Two y-scales let any pair of series be made to look correlated.",
        "code": "DSX-VIZ-001",
        "citation": "Muth 2018 (Datawrapper) — HQ-27 T3-4; see also DSX-VIZ-030 (_check_dual_axis)",
    },
}
```

### D-02: `_check_banned` one-line change
```python
# Source: dsx/checks/viz.py:80-89 (live) — before
def _check_banned(chart_type: str, label: str, where: str, report: Report) -> None:
    if chart_type in BANNED_TYPES:
        report.add(
            "DSX-VIZ-001",
            "HIGH",
            f"'{label}' uses {chart_type}, which distorts the data",
            detail=BANNED_TYPES[chart_type],
            remedy="Use a 2D length- or position-encoded chart instead.",
            where=f"{where}.type",
        )
# after — only the detail= line changes
            detail=BANNED_TYPES[chart_type]["reason"],
```
The `if chart_type in BANNED_TYPES:` membership check on line 81 needs **no change** — `in`
tests dict keys, which are unaffected by the value-type promotion.

## State of the Art

Not applicable — no external ecosystem to track. Internally: `dsx/checks/viz.py` last touched
at commit `edf862c` (2026-08-10), confirmed untouched since before v2.3
(`.planning/v2.4-SCOPE-RECHECK.md` Method section). No structural change to this vocabulary
has occurred since; Phase 21 is the first phase to edit it.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | `radar`'s refusal citation should point at Tufte 1983 / Munzner 2014 ch.6 as the closest available Tier-3-adjacent source, pending operator confirmation | Common Pitfall 5, Code Examples | Low — the `citation` field just needs to be non-empty and flagged for HQ-27 review; a wrong-but-flagged source is corrected at S5-2 sign-off, not blocking |
| A2 | The homing table's primary choice (not the "alt") for `waterfall` (composition) and `bump` (categorical-multi) is what the plan will implement | Homing guidance table | Low — both are explicitly within Claude's Discretion per CONTEXT; either choice satisfies D-01, this is a naming/precision risk only |
| A3 | The new test file will be named `tests/test_viz_vocabulary_invariant.py` | Recommended File-Change Set | None — explicitly noted as a suggestion, not prescriptive; any `test_*.py` name works with `unittest discover` |

**If this table is empty:** N/A — three low-risk naming/sourcing assumptions are logged above;
none affect REQ-P21-01/02/03 correctness.

## Open Questions

1. **Exact per-mark citation strings for the five `BANNED_TYPES` entries.**
   - What we know: HQ-27 Tier-3 maps Muth 2018 → `dual_axis_line` precisely; Tufte 1983 and
     Munzner 2014 ch.6 both plausibly cover the three 3D bans; nothing precisely names
     `radar`.
   - What's unclear: whether the operator wants a single shared citation for the three 3D
     bans plus `radar` (grouped under "no unjustified 3D / proportional-encoding doctrine") or
     four distinct citations.
   - Recommendation: populate `citation` non-empty for all five now (satisfies the invariant
     test and REQ-P21-02's "present and routed-to-refusal" requirement), explicitly flag the
     `radar` mapping as the least-certain in the HQ-27 annotation per CONTEXT's instruction,
     and let S5-2 sign-off correct it if needed — this is D-05's designed non-blocking path.

2. **Whether `waterfall`/`bump` need their "alt" family too, or just the primary.**
   - What we know: CONTEXT names one primary and one alt per mark, explicitly "proposed, not
     frozen."
   - What's unclear: no persona-round rationale distinguishes why the alt was rejected (unlike
     the fully-argued primary-vs-rejected pattern used for D-01/D-02 themselves).
   - Recommendation: default to the primary only (narrowest home, per D-01's own stated
     preference for "the narrowest home that removes the friction"); document if the plan
     diverges.

## Environment Availability

Skipped — this phase has no external tool/service/runtime dependency beyond the Python
interpreter and stdlib already required to run the existing `tests/` suite.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `unittest` (stdlib), repo-standard — confirmed via `README.md:431` (`python3 -m unittest discover -s tests -v # 121 tests`) and every existing test file in `tests/` |
| Config file | none — no `pytest.ini`/`setup.cfg`/`conftest.py` found in the repo (confirmed by search); tests are plain `unittest.TestCase` subclasses |
| Quick run command | `python3 -m unittest tests.test_viz_vocabulary_invariant -v` (new file, name per plan) |
| Full suite command | `python3 -m unittest discover -s tests -v` |

### Phase Requirements → Test Map
| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P21-01 | Every non-banned mark has a capability home (clause 1) | unit (repo-integrity) | `python3 -m unittest tests.test_viz_vocabulary_invariant.TestEveryMarkHasAHome.test_every_mark_has_a_capability_home -v` | ❌ Wave 0 — new file |
| REQ-P21-01 | Every non-banned mark has a relationship home or is on the frozen `CAPABILITY_ONLY` allowlist (clause 2) | unit (repo-integrity) | `python3 -m unittest tests.test_viz_vocabulary_invariant.TestEveryMarkHasAHome.test_every_mark_has_a_relationship_home_or_is_allowlisted -v` | ❌ Wave 0 — new file |
| REQ-P21-01 | `CAPABILITY_ONLY` allowlist has no stale entries (no allowlisted mark secretly already has a relationship home) | unit (repo-integrity) | `python3 -m unittest tests.test_viz_vocabulary_invariant.TestEveryMarkHasAHome.test_capability_only_allowlist_is_exact_not_a_superset -v` | ❌ Wave 0 — new file |
| REQ-P21-01 | `_check_input_type_matrix` no longer false-positives on the homed marks via IT id (e.g. `IT014`+`histogram`) | integration (gate smoke) | ad-hoc `viz.check({...})` call in the same test module, or a `Gate`-style class per `tests/test_input_types.py:95-131`'s pattern | ❌ Wave 0 — add alongside the invariant test |
| REQ-P21-02 | Every `BANNED_TYPES` record has non-empty `reason`/`code`/`citation` | unit (repo-integrity) | `python3 -m unittest tests.test_viz_vocabulary_invariant.TestRefusalEntryCompleteness.test_every_banned_type_has_a_complete_refusal_record -v` | ❌ Wave 0 — new file |
| REQ-P21-02 | Every refusal record's `code` equals `"DSX-VIZ-001"` (the code `_check_banned` actually emits) | unit (repo-integrity) | `python3 -m unittest tests.test_viz_vocabulary_invariant.TestRefusalEntryCompleteness.test_every_refusal_code_is_the_code_check_banned_emits -v` | ❌ Wave 0 — new file |
| REQ-P21-02 | `_check_banned` still fires `DSX-VIZ-001` with the enriched `reason` text as `detail` | unit (existing gate) | `python3 -m unittest tests.test_input_types.Gate -v` (or a new one-off spec against `viz.check`) is not sufficient — write a direct assertion in the new test module that `viz.check({...radar...}).findings[0].detail == BANNED_TYPES["radar"]["reason"]` | ❌ Wave 0 — add alongside |
| REQ-P21-03 | Catalogue set-identity: 275 → 275, zero new codes | unit (existing, unchanged) | `python3 -m unittest tests.test_finding_catalogue_invariant -v` (2 passed) | ✅ exists, unmodified |
| REQ-P21-03 | Declared Total line still reads 275 | doc grep | `grep -n "Total:" references/finding-codes.md` → `**Total: 275 codes.**` | ✅ exists |
| REQ-P21-03 | Unique-code count still 275 | doc grep | `grep -oE '(DSX-[A-Z]+-[0-9]+\|SQL-[0-9]+)' references/finding-codes.md \| sort -u \| wc -l` → `275` | ✅ exists (S0-2 literal command, reproduced verbatim) |

### Sampling Rate
- **Per task commit:** `python3 -m unittest tests.test_viz_vocabulary_invariant -v`
- **Per wave merge:** `python3 -m unittest discover -s tests -v` (full 121+1 suite)
- **Phase gate:** full suite green, plus the three REQ-P21-03 commands above, before
  `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/test_viz_vocabulary_invariant.py` — covers REQ-P21-01, REQ-P21-02 (new file, no
      existing test covers this vocabulary structure directly)
- [ ] No shared fixtures needed — the test reads live `dsx` module objects, no `conftest.py`
      or fixture file required
- [ ] Framework install: none — `unittest` is stdlib

*(No gap for REQ-P21-03 — existing test infrastructure (`test_finding_catalogue_invariant.py`)
already covers it and this phase does not need to modify it.)*

## Security Domain

### Applicable ASVS Categories

This phase edits static, gate-time-only vocabulary data structures in a Python library with
no network I/O, no user session, no auth, and no execution of untrusted input (the `dsx`
checks operate on a declared YAML/dict spec already loaded elsewhere; this phase does not
touch loading/parsing). Most ASVS categories do not apply.

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | N/A — no auth surface in this repo |
| V3 Session Management | no | N/A |
| V4 Access Control | no | N/A |
| V5 Input Validation | marginal | The gate's existing pattern (closed-vocabulary `dict`/`frozenset` membership checks, `report.add` on mismatch) is unchanged and reused — this phase only widens the *contents* of existing closed vocabularies, it does not change the validation *mechanism* |
| V6 Cryptography | no | N/A — no crypto in this phase |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Silent expansion of a security-relevant allowlist (here: chart-type admissibility, not an auth allowlist, but the same "loud not silent" discipline the repo already enforces via D-06/REQ-P21-03) | Tampering (of the vocabulary, not of a running system) | The invariant test itself is the mitigation — any future addition to `CHART_CAPABILITIES`/`RELATIONSHIP_CHARTS` without a corresponding home or allowlist entry turns the new test red, catching drift at commit time rather than silently passing review |
| A refusal entry with an empty `citation`/`reason`/`code` field shipping silently | Repudiation (an unfounded ban with no traceable justification) | `TestRefusalEntryCompleteness` asserts non-empty on all three fields for all five banned types — this is the concrete gate against exactly that failure mode |

No new attack surface is introduced; no new gate code is minted; the security posture of this
phase is fully captured by the two test classes above.

## Sources

### Primary (HIGH confidence — direct repo reads this session)
- `dsx/checks/viz.py` — full file read (431 lines); `RELATIONSHIP_CHARTS` (17-28), `LENGTH_ENCODED` (32-34), `BANNED_TYPES` (36-42), `_check_banned` (80-89), `_check_input_type_matrix` (133-191)
- `dsx/checks/smells.py` — full file read; `DENSITY_MARKS`/`STACKED_MARKS` (12-13)
- `dsx/spec.py` — `DATA_INPUT_TYPES` (275-293), `CHART_CAPABILITIES` (296-325), `_VOCABULARIES` list (695-734+, confirms `BANNED_TYPES` is not vocab-dumped), vocab-dump function (1630-1651)
- `dsx/input_types.py` — full lookup module read; `permitted()` (76-104), `canonical_id()` (43-54)
- `scripts/gen-input-types.py` — full file read (201 lines); `FAMILY` (32-73), `EXTRA_MARKS` (77-86), generation logic (112-196)
- `scripts/gen-finding-catalogue.py` — `_literal()`/`extract()` (204-234), confirming `detail=` kwargs are never read for code derivation
- `tests/test_finding_catalogue_invariant.py` — full file read (157 lines), the "off-gate-path repo-integrity test" idiom precedent named by CONTEXT
- `tests/test_input_types.py` — full file read (136 lines), the "structural object iteration" idiom to copy
- `tests/test_phase20_zero_mint_close.py` — full file read (156 lines), precedent for `importlib.util.spec_from_file_location` loading a hyphenated script and for multi-clause phase-close oracle style
- `tests/test_gate_path_hermetic.py` — partial read, confirms `tests/` is outside `dsx.cli.GATE_PROFILES`'s import closure by construction
- `references/finding-codes.md:16` — `**Total: 275 codes.**`, confirmed live
- `.planning/v2.4-SCOPE-RECHECK.md` — S0-2's independently re-verified premises (orphan list, `BANNED_TYPES` unchanged, 275 baseline, literal grep command)
- `.planning/HUMAN-QUEUE.md` (HQ-27, HQ-28) and `.planning/v2.4-D05-EVIDENCE-PACK.md` (Tier 1-3 tables) — citation-sourcing ground truth
- `.planning/phases/21-viz-vocabulary-reconciliation/21-CONTEXT.md` — authoritative D-01/D-02 decisions (this research does not re-litigate them)
- `dsx/data/input_types.json` — spot-read of `IT011`/`IT014`/`IT036`/`IT040` records, confirming the generated-artifact staleness risk (Pitfall 1)
- Repo-wide grep for `BANNED_TYPES`, `CHART_CAPABILITIES`, `RELATIONSHIP_CHARTS`, `EXTRA_MARKS` consumers — confirms the "exactly two call sites" and "no other reader" claims mechanically

No secondary or tertiary (web) sources — none used, per task scope.

## Metadata

**Confidence breakdown:**
- Standard stack: N/A — no external dependency
- Architecture: HIGH — every structure, line span, and consumer verified by direct read; the 12-orphan/14-allowlist accounting was independently re-derived by set algebra and matches CONTEXT exactly
- Pitfalls: HIGH for Pitfalls 1-4 (verified by tracing the actual code paths); MEDIUM for Pitfall 5 (citation-sourcing gap is a genuine open item, not a code-verifiable fact)

**Research date:** 2026-09-03
**Valid until:** stable — this research is pinned to a specific commit state of a file
untouched since 2026-08-10; re-verify only if `dsx/checks/viz.py`, `dsx/spec.py`, or
`scripts/gen-input-types.py` change before this phase executes.
