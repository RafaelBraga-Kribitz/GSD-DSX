# Phase 22: Catalog spine, uncertainty family, selection heuristic — Research

**Researched:** 2026-09-03
**Domain:** repo-internal reference-catalog authoring + gate-vocabulary extension (Python dict edits, Markdown reference docs, off-gate-path repo-integrity tests). Zero external packages, zero library research — this is a "read the live tree exactly" phase, same class as Phase 21.
**Confidence:** HIGH — every structural claim below is a direct read of the live tree (file + line span) or a runnable command executed during this research session, not training knowledge. All D-05 citation content is drawn from the **signed** HQ-27 pack; no new primary-source claims are made here.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions (binding, from the signed HQ-27 pack — D-1..D-4)

- **D-1 — perceptual rank axis.** Cleveland–McGill (1984) is **6 ranks over 10 tasks WITH TIES**, not a 7-item strict order (p.536 list, p.537 tie caveat; Heer & Bostock p.206 independently declines `length > angle`). Structural-criterion test asserts `rank(a) <= rank(b)`, **never** strict `<`, across tied members. Shipping form: rank1 `position_common` · rank2 `position_nonaligned` · rank3 `{length, direction/slope, angle}` · rank4 `area` · rank5 `{volume, curvature}` · rank6 `{shading, colour_saturation}`. `density` is absent from the 1984 paper.
- **D-2 — uncertainty vocabulary = Wilke's actual §5.6 ten marks**: error bars · graded error bars · 2D error bars · confidence strips · eyes · half-eyes · quantile dot plot · confidence band · graded confidence band · fitted draws. **"fan chart" and "gradient CI band" do NOT exist in Wilke and must not ship** — these were the SCOPE doc's (`.planning/research/V2.3-V2.4-SCOPE.md` §3.1/3.2) original (incorrect) naming; the scope doc is **superseded** on this point by the signed D-05 pack. "eye" (violin+error bar) ≠ "half-eye" (ridgeline+error bar). Frequentist/Bayesian paradigm symmetry is genuinely supported (Wilke §16.2).
- **D-3 — FT Visual Vocabulary is NOT MIT for its content.** Attribute the nine-category function axis (link ft.com/vocabulary); write all descriptions ourselves; never vendor the poster PDF or copy its blurbs; drop any "exhaustive" claim resting on the FT. Nine categories confirmed exactly: Deviation · Correlation · Ranking · Distribution · Change over Time · Magnitude · Part-to-whole · Spatial · Flow.
- **D-4 — `dual_axis_line` refusal** cites **"Muth 2018 (Datawrapper), as amended July 2026"**, records the amendment, scopes the reason string to a **general audience**. Already applied in `viz.py`'s `BANNED_TYPES`; the catalog refusal row must match verbatim.
- **Cross-cutting:** the "spine" sources are **one design lineage, not three independent authorities** (Ribecca authored both Graphic Continuum and DVC; FT credits Graphic Continuum). Never claim triangulation across FT/GC/DVC as independent corroboration. Genuine independence: Munzner's task taxonomy + Cleveland–McGill's encoding work.

### Claude's Discretion (GA-1/GA-2/GA-3, pinned at plan per CONTEXT.md)

- **GA-1 (REQ-P22-01):** catalog = 50 DSX-admissible + 10 uncertainty (frozen, 60) + 7 refusal rows + ~15 reference-only rows, target ~80, band 75–90 (plan-checker verifies `75 <= total <= 90`). Reference-only row **selection** (which spine types fill the FT function-coverage gaps) is not frozen — plan/execute discretion.
- **GA-2 (REQ-P22-02):** 11th `RELATIONSHIP_CHARTS` key `"uncertainty"`, not new input-type ids. `DSX-VIZ-070` retained as complementary verification surface (property-based), not replaced.
- **GA-3 (REQ-P22-05):** new gate codes = `DSX-VIZ-071` (+ `-072` contingently, decided at plan). Perceptual tie-break, faceting routing, catalog↔vocabulary conformance are **off-gate-path repo-integrity tests → zero code**.

### Deferred Ideas (OUT OF SCOPE)

- Promoting any `CAPABILITY_ONLY` mark to a relationship home beyond what GA-2 requires is not automatically in scope — only the uncertainty family's own homing need (see Pitfall 1 below) is required by this phase.
- The 8 items HQ-27 marks "still unverified" (Mackinlay 1986, R.L. Harris 1999 index, Tufte's verbatim chartjunk sentence, Few 2013 ed., GC primary count, FT stance on axis reuse, Munzner "cardinality", one Duan phrasing) — **must NOT be cited by any shipping row**.
- **Not in the signed HQ-27 pack at all (new finding, this research):** the SCOPE doc's L1/L2 heuristic-layer provenance names **Abela 2008** (pattern-origin credit) and **Few's Graph Selection Matrix** (L2 corroboration) — see Open Questions below. These were never submitted for HQ-27 verification and must not be shipped as citations without either (a) dropping them from the heuristic edit, or (b) a fresh, explicitly-flagged verification pass (out of scope for "no new primary-source read is owed to unblock the build").
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P22-01 | Merged chart catalog (~80, band 75–90), 3 axes + per-entry citation | Exact composition arithmetic verified (50+10+7+~15); `references/chart-catalog.md` confirmed absent; JSON-in-Markdown embedding pattern identified as the precedent to reuse (`references/input-type-inventory.md`) for a parseable rank/citation payload |
| REQ-P22-02 | Uncertainty family enters vocabulary as 11th relationship key, D-12a-clean | Exact `RELATIONSHIP_CHARTS` dict location (viz.py:17-29) and shape confirmed; **critical gap found**: the 10 Wilke marks have no existing capability home, which will break Phase 21's `test_every_mark_has_a_capability_home` invariant unless addressed (Pitfall 1) |
| REQ-P22-03 | `facet_by` orthogonal declaration, smells route to it | Confirmed zero existing scaffolding (`facet_by` appears nowhere in `dsx/`); closest existing smell to route to is `DSX-SMELL-007` (`_check_atoms_under_density`, smells.py:59-80) — no dedicated "overplotting" code exists today |
| REQ-P22-04 | 5-layer heuristic as route-and-cite edits, no parallel tree | Both target files read in full (38 + 63 lines); exact edit surface identified; `skills/dsx-visualize/SKILL.md` step 1 also enumerates all 10 relationships by name and **must be updated to 11** — a ripple point not named in CONTEXT.md's list |
| REQ-P22-05 | Gate extensions, D-05 citation per new code, perceptual tie-break as structural criterion | **Critical gap found**: `DSX-VIZ-*` is NOT in `gen-finding-catalogue.py`'s `_D05_ALLOWLIST_PREFIXES`, so the D-05 citation requirement is not machine-enforced unless `DSX-VIZ-071`(/`-072`) is added to `_D05_ALLOWLIST_CODES` by exact string (established Phase 18/19 precedent); **load-bearing gate identified**: `tests/test_finding_catalogue_invariant.py` hard-codes `_EXPECTED_TOTAL = 275` and `_MINTED_CODES` — this file WILL fail red the moment a new code is minted unless updated in the same plan |
</phase_requirements>

## Summary

Phase 22 is a pure repo-internal reference-authoring and vocabulary-extension phase — no new package, no new library, no external documentation lookup applies (config confirms all external search providers are disabled; none were needed). The live tree was read in full for every surface CONTEXT.md names, plus several it doesn't: `dsx/checks/viz.py` (460 lines), `dsx/spec.py`'s `DATA_INPUT_TYPES`/`CHART_CAPABILITIES` block, `scripts/gen-input-types.py`, `scripts/gen-finding-catalogue.py` (501 lines), `references/finding-codes.md`, `references/question-taxonomy.md`, `references/chart-selection.md`, `tests/test_viz_vocabulary_invariant.py`, `tests/test_finding_catalogue_invariant.py`, `tests/test_phase20_zero_mint_close.py`, `skills/dsx-visualize/SKILL.md`, and `references/input-type-inventory.md`. The full test suite (1471 tests) and the two vocabulary-invariant test modules were run and confirmed green before any change, establishing the exact baseline this phase must not regress.

Three findings materially change what the plan must scope beyond what CONTEXT.md already states, all with HIGH confidence because they are direct code reads:

1. **The 10 new uncertainty marks need a capability home, not just a relationship home.** GA-2 rejects new input-type ids, but Phase 21's `test_every_mark_has_a_capability_home` (the live, currently-green D-01 invariant) requires every mark named anywhere — including in a brand-new `RELATIONSHIP_CHARTS["uncertainty"]` tuple — to also appear in some `CHART_CAPABILITIES` or `EXTRA_MARKS` value, or the test goes red. GA-2's own text ("input_types.py narrowing") implicitly requires this too: `permitted()`'s relationship-narrowing step intersects against a capability-derived admissible set, which is empty for these 10 marks today. The natural, zero-new-family fix is adding the 10 marks to the existing `CHART_CAPABILITIES["interval-range"]` value (which already holds `box, violin, histogram, density, ecdf, strip, kde` — conceptually the same shape family) — no new coarse family, no new input-type id, consistent with GA-2's rejection of new IDs.
2. **`references/finding-codes.md`'s live gate test hard-codes the total and the exact code set.** `tests/test_finding_catalogue_invariant.py` asserts `_EXPECTED_TOTAL = 275` and `current_set == snapshot_set | _MINTED_CODES`. This is not optional bookkeeping — it is a currently-green, currently-enforced test that will fail the instant `DSX-VIZ-071` (or `-072`) is minted, unless this file is edited in the same plan to bump the total to 276 (or 277) and add the new code(s) to `_MINTED_CODES`. This is the actual mechanism behind "prove the additive-only set-identity diff," not a separate manual proof.
3. **D-05 citation enforcement for `DSX-VIZ-*` is currently OFF.** `gen-finding-catalogue.py`'s `_D05_ALLOWLIST_PREFIXES` does not include `"DSX-VIZ-"` (the family has 20 pre-existing, uncited legacy codes). The established, repeatedly-used precedent (Phase 15/18/19, all documented in-line in `gen-finding-catalogue.py`) is: never add the family prefix (it would retroactively fail-red on legacy codes); instead add the new code(s) by **exact string** to `_D05_ALLOWLIST_CODES`. This machine-enforces the docstring `Citation:`/`Structural criterion:` lines and the `# D-05: DSX-VIZ-071` test marker that REQ-P22-05 already requires as a matter of doctrine — it should be a plan task, not left as an unenforced convention.

**Primary recommendation:** scope the plan around six concrete edit targets — (1) create `references/chart-catalog.md` with a fenced JSON payload (mirroring `references/input-type-inventory.md`'s pattern) carrying the three axes + citation per row, so the two new repo-integrity tests (perceptual tie-break, catalog↔vocabulary conformance) have something machine-parseable to read rather than fragile Markdown-table regex; (2) add the 11th `"uncertainty"` key to `RELATIONSHIP_CHARTS` and home its 10 marks into `CHART_CAPABILITIES["interval-range"]`; (3) add `gauge`+`word_cloud` to `BANNED_TYPES` (reusing `DSX-VIZ-001`) and swap `radar`'s citation to Duan et al. 2023; (4) mint `DSX-VIZ-071` (contingently `-072`) in a **new** function in `viz.py` carrying `Citation:`/`Structural criterion:` docstring lines, add it to `_D05_ALLOWLIST_CODES`, and bump `test_finding_catalogue_invariant.py`'s pinned total + `_MINTED_CODES`; (5) add a `facet_by` declaration that routes its remedy string to `DSX-SMELL-007`'s existing detail (no new smell code); (6) edit `references/question-taxonomy.md`, `references/chart-selection.md` (which currently ships the **superseded** 7-item strict perceptual ordering — must be corrected to D-1's 6-rank-with-ties form) and `skills/dsx-visualize/SKILL.md` (which enumerates all 10 relationships by name in its `<method>` step 1 and must list an 11th).

## Architectural Responsibility Map

Single-tier Python library/CLI repo (no browser/server/DB tiers — this is the DSX gate tool itself, not an application built with it). Tiers below are this codebase's own module layers, matching Phase 21's precedent framing.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Chart-type recommendation (relationship → marks) | `dsx/checks/viz.py` (`RELATIONSHIP_CHARTS`) | `dsx/input_types.py` (`permitted()`) | Consumed by `_check_relationship_match` (DSX-VIZ-010/011/012) at verify/ship gates and by the CLI's `dsx charts` command |
| Data-shape admissibility (data_input_type → marks) | `dsx/spec.py` (`CHART_CAPABILITIES`) | `scripts/gen-input-types.py` (`EXTRA_MARKS`) → `dsx/data/input_types.json` | `_check_input_type_matrix` (DSX-VIZ-013/014) reads both the coarse-family path (live dict) and the IT-id path (generated JSON) — a change to one without regenerating the other is a real, previously-hit drift bug (Phase 21 research pitfall) |
| Refusal doctrine (banned marks) | `dsx/checks/viz.py` (`BANNED_TYPES`) | — | `_check_banned` (DSX-VIZ-001); reference-catalog refusal rows must be backed by an actual entry here or the catalog claims a ban the gate does not enforce (drift surface named explicitly in CONTEXT.md) |
| Reference catalog (human-facing, citable) | `references/chart-catalog.md` (new) | — | Explicitly **not** a gate check (CONTEXT.md: "The catalog is a reference artifact, not itself a gate check") — read by humans and by off-gate-path repo-integrity tests only |
| Selection heuristic (question → chart) | `references/question-taxonomy.md` + `references/chart-selection.md` | `skills/dsx-visualize/SKILL.md` | Route-and-cite edits only; the skill file is the agent-facing entry point and enumerates relationships by name, so it is a ripple point even though CONTEXT.md does not name it explicitly |
| Finding-catalogue integrity (code count, D-05 enforcement) | `scripts/gen-finding-catalogue.py` + `references/finding-codes.md` | `tests/test_finding_catalogue_invariant.py`, `tests/test_viz_vocabulary_invariant.py` | The catalogue-count gate is a **currently-green, currently-enforced** test, not aspirational documentation — it must be edited in-plan or the phase leaves the repo red |

## Standard Stack

Not applicable in the conventional sense — this phase installs no packages. The "stack" is the repo's own established Python stdlib idioms:

| Idiom | Where used | Why standard here |
|---|---|---|
| Plain `dict[str, tuple[str,...]]` / `dict[str, frozenset[str]]` for vocabularies | `RELATIONSHIP_CHARTS`, `CHART_CAPABILITIES`, `BANNED_TYPES` | House style (Phase 21 CONTEXT.md explicitly rejected a `NamedTuple`/dataclass alternative as "a new gate-adjacent type against the codebase's plain-dict house style") |
| `importlib.util.spec_from_file_location` to load hyphenated scripts without running `__main__` | `tests/test_phase20_zero_mint_close.py::_load_generator()`, `tests/test_viz_vocabulary_invariant.py::_load_gen_input_types()` | The only way to import `scripts/gen-*.py` (no `__init__.py`, hyphenated filenames) from a test; reused, not reinvented |
| Fenced ```` ```json ```` block embedded in a Markdown reference doc, parsed by a `re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)` | `references/input-type-inventory.md` → `scripts/gen-input-types.py` | Established pattern for "human-readable Markdown table + machine-parseable payload in the same file" — the direct precedent for `references/chart-catalog.md`'s three-axis rows |
| CRLF-safe, non-line-anchored regex (`\s*`, whitespace-collapse, never `^`/`$` alone) | `tests/test_finding_catalogue_invariant.py`, `scripts/gen-finding-catalogue.py` | Mandated by `./.claude/CLAUDE.md`: "This repo checks out CRLF on Windows... MUST tolerate `\r\n`" |

### Installation

None. `python --version` confirmed **3.12.10** installed and on PATH; stdlib-only per D-01/D-02 (gate path forbids pandas/scipy/numpy — confirmed no such import appears in `dsx/checks/viz.py` or `dsx/spec.py`).

## Package Legitimacy Audit

**Not applicable.** This phase installs zero external packages — every change is to existing repo-internal Python dicts, a new Markdown reference file, and repo-integrity test files. No `npm view` / `pip index versions` / package-legitimacy check was run because there is nothing to check.

## Architecture Patterns

### System Architecture Diagram

```
                    ┌─────────────────────────────────────┐
                    │  references/chart-catalog.md (NEW)   │
                    │  75-90 rows: function | data-sig |   │
                    │  perceptual-rank | citation          │
                    │  fenced ```json payload (parseable)  │
                    └───────────────┬───────────────────────┘
                                    │ read by (off gate path)
                    ┌───────────────▼───────────────────────┐
                    │  tests/ (repo-integrity, NOT dsx/checks)│
                    │  • perceptual tie-break: rank(a)<=rank(b)│
                    │  • catalog↔vocabulary conformance       │
                    └───────────────┬───────────────────────┘
                                    │ cross-checks against
        ┌───────────────────────────▼──────────────────────────────┐
        │  dsx/checks/viz.py  (LIVE, gate-enforced)                 │
        │  RELATIONSHIP_CHARTS: 10 keys → 11 (+ "uncertainty")      │
        │  BANNED_TYPES: 5 records → 7 (+ gauge, word_cloud)        │
        │  _check_relationship_match → DSX-VIZ-010/011/012          │
        │  _check_banned → DSX-VIZ-001                              │
        │  _check_uncertainty (unchanged, property-based) → DSX-VIZ-070│
        │  NEW: _check_uncertainty_vocabulary (name TBD at plan)    │
        │       → DSX-VIZ-071 (+072 contingent)                     │
        └───────────────┬─────────────────────┬─────────────────────┘
                         │                     │
          ┌──────────────▼─────────┐  ┌────────▼──────────────────────┐
          │ dsx/spec.py             │  │ scripts/gen-finding-catalogue.py│
          │ CHART_CAPABILITIES:     │  │ • extracts report.add() codes   │
          │ "interval-range" +=     │  │   via AST walk                  │
          │ 10 uncertainty marks    │  │ • _D05_ALLOWLIST_CODES +=       │
          │ (capability home fix,   │  │   "DSX-VIZ-071"(+"-072")        │
          │ see Pitfall 1)          │  │ • regenerates finding-codes.md  │
          └──────────────┬─────────┘  └────────┬─────────────────────┘
                         │                     │
          ┌──────────────▼─────────┐  ┌────────▼─────────────────────┐
          │ scripts/gen-input-      │  │ tests/                        │
          │ types.py → regenerates  │  │ test_finding_catalogue_       │
          │ dsx/data/input_types.json│ │ invariant.py: bump 275→276/277│
          └─────────────────────────┘  │ + _MINTED_CODES               │
                                        │ test_viz_vocabulary_          │
                                        │ invariant.py: re-run, stays   │
                                        │ green (capability home fixed) │
                                        └───────────────────────────────┘

    ┌────────────────────────────────────────────────────────────┐
    │ references/question-taxonomy.md + chart-selection.md        │
    │ 5-layer heuristic route-and-cite edits (L1..L5)              │
    │ chart-selection.md's perceptual-rank line MUST be corrected  │
    │ from the superseded 7-item strict order to D-1's 6-with-ties │
    └──────────────────────┬────────────────────────────────────┘
                            │ pointed to by
    ┌──────────────────────▼────────────────────────────────────┐
    │ skills/dsx-visualize/SKILL.md                               │
    │ <method> step 1 enumerates all relationships by name — must │
    │ list 11 (add "uncertainty"); <references> block should add  │
    │ @references/chart-catalog.md alongside chart-selection.md   │
    └───────────────────────────────────────────────────────────┘
```

### Recommended Edit Surface (files touched, by requirement)

```
references/
├── chart-catalog.md         # NEW — REQ-P22-01, three axes + citation, 75-90 rows
├── question-taxonomy.md     # EDIT — REQ-P22-04, L1 question→task layer pointer
├── chart-selection.md       # EDIT — REQ-P22-04 (L2-L5) + REQ-P22-05 (fix superseded
│                             #        7-item perceptual line to D-1's 6-with-ties)
└── finding-codes.md         # REGENERATED (not hand-edited) — REQ-P22-05, 275→276/277

dsx/
├── checks/viz.py            # EDIT — RELATIONSHIP_CHARTS (+uncertainty), BANNED_TYPES
│                             #        (+gauge,+word_cloud, radar citation swap), NEW
│                             #        function minting DSX-VIZ-071(/-072)
└── spec.py                  # EDIT — CHART_CAPABILITIES["interval-range"] += 10 marks
                              #        (capability-home fix, see Pitfall 1)

scripts/
├── gen-input-types.py       # RUN (not necessarily edited) — regenerate input_types.json
│                             #        if EXTRA_MARKS changes; verify no change needed if
│                             #        CHART_CAPABILITIES alone absorbs the 10 marks
└── gen-finding-catalogue.py # EDIT — _D05_ALLOWLIST_CODES += DSX-VIZ-071(/-072)

skills/dsx-visualize/
└── SKILL.md                 # EDIT — relationship list 10→11; add chart-catalog.md ref

tests/
├── test_finding_catalogue_invariant.py   # EDIT — 275→276/277, _MINTED_CODES
├── test_viz_vocabulary_invariant.py      # VERIFY stays green (or extend if the
│                                           #        uncertainty marks need CAPABILITY_ONLY
│                                           #        treatment — they should not, since D-1
│                                           #        gives them a relationship home directly)
└── test_XX_chart_catalog_invariant.py    # NEW — REQ-P22-01/05 repo-integrity:
                                            #        perceptual tie-break + catalog↔
                                            #        vocabulary conformance
```

### Pattern 1: Additive dict-value promotion, never a parallel structure

**What:** When a check needs richer metadata than a flat value provides (Phase 21's `BANNED_TYPES: dict[str,str]` → `dict[str,dict[str,str]]`), promote the value in place rather than adding a second lookup table.
**When to use:** Any time this phase is tempted to add a second dict tracking "which marks are uncertainty marks" alongside `RELATIONSHIP_CHARTS["uncertainty"]` — don't; the tuple itself is the source of truth, exactly as Phase 21's CONTEXT.md reasoned when it rejected a parallel `REFUSAL_ENTRIES` map ("a second invariant to police").
**Example (existing code, the precedent to follow):**
```python
# Source: dsx/checks/viz.py:45-72 (live)
BANNED_TYPES: dict[str, dict[str, str]] = {
    "3d_bar": {"reason": "...", "code": "DSX-VIZ-001", "citation": "..."},
    # ...
}
```

### Pattern 2: Fenced JSON-in-Markdown for a reference doc that a test must parse

**What:** A Markdown reference file carries both a human-readable table and a fenced ` ```json ` block with the same content in machine-parseable form; a generator or test regex-extracts the JSON block.
**When to use:** `references/chart-catalog.md` — the perceptual-rank tie-break test and the catalog↔vocabulary conformance test both need structured access to per-row function/data-signature/rank/citation fields. Parsing Markdown table cells with regex (the `finding-codes.md` approach) works for a flat code/severity/title triple but is fragile for three semantically distinct axes per row plus a citation string that may itself contain `|` characters.
**Example (the precedent to reuse verbatim):**
```python
# Source: scripts/gen-input-types.py:117-124 (live)
text = SOURCE.read_text(encoding="utf-8", errors="replace")
match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.S)
data = json.loads(match.group(1))
items = data["input_types"]
```

### Pattern 3: Exact-code D-05 allowlisting into a pre-existing, partially-uncited family

**What:** When a new finding code lives inside a large pre-existing family that has legacy uncited codes (`DSX-VIZ-*` has 20, none cited), add the new code by **exact string** to `_D05_ALLOWLIST_CODES`, never add the family prefix to `_D05_ALLOWLIST_PREFIXES`.
**When to use:** Minting `DSX-VIZ-071` (contingently `-072`).
**Example (the precedent — five prior phases have done exactly this):**
```python
# Source: scripts/gen-finding-catalogue.py:183-195 (live)
_D05_ALLOWLIST_CODES = frozenset({
    "DSX-SPEC-080", ..., "DSX-STA-120", "DSX-STA-121", "DSX-STA-122",
    # Phase 22 adds "DSX-VIZ-071" (+ "DSX-VIZ-072" if warranted) here.
})
```

### Anti-Patterns to Avoid

- **Hand-editing `references/finding-codes.md`.** It is generated (`python3 scripts/gen-finding-catalogue.py --write`) from live `report.add(...)` call sites. A hand edit will be immediately detected as stale by `--check` and by `test_finding_catalogue_invariant.py`.
- **Adding `"uncertainty"` as a new `data_input_type` / `CHART_CAPABILITIES` family.** GA-2 explicitly rejected this ("Rejected: new input-type ids"). The 10 marks need a capability home, but that home is an *existing* family (`interval-range`), not a new one.
- **Claiming a catalog refusal row for a type not in the live `BANNED_TYPES`.** CONTEXT.md names this explicitly as "the drift surface Phase 21's doctrine forbids" — every refusal row in `chart-catalog.md` must cross-reference an actual `BANNED_TYPES` key.
- **Citing Abela 2008 or Few's Graph Selection Matrix as if they were HQ-27-signed.** They appear in the SCOPE doc's L1/L2 provenance language but were never submitted to or verified by HQ-27. See Open Questions.
- **Re-deriving the perceptual channel ordering from memory instead of copying D-1's shipping form verbatim.** `references/chart-selection.md`'s current "Encoding accuracy" line (`position on a common scale → length → angle → area → colour saturation → volume`) is the exact **superseded 7-item strict order** HQ-27 corrected — it must be rewritten to the 6-rank-with-ties form, not merely left alone because it "looks right."

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Parsing the catalog's per-row structured data | A bespoke Markdown-table-cell regex parser | The fenced-JSON-block pattern (`re.search(r"```json\s*(\{.*?\})\s*```", ...)`) already used by `gen-input-types.py` | Table-cell regex breaks on citation strings containing `|`; the JSON pattern is proven CRLF-safe and already has a working precedent in this exact repo |
| Proving "additive-only mint" | A new, from-scratch verification script | `tests/test_finding_catalogue_invariant.py`'s existing set-identity idiom (`snapshot_set \| _MINTED_CODES == current_set`) | This is a live, running, currently-green test with exactly this job — editing its two constants is strictly less work and less risk than a parallel proof |
| Loading a hyphenated `scripts/*.py` module from a test | `importlib.import_module` tricks, `sys.path` manipulation, or copying the script's logic inline | `importlib.util.spec_from_file_location` + `module_from_spec` + `exec_module`, exactly as `test_phase20_zero_mint_close.py::_load_generator()` and `test_viz_vocabulary_invariant.py::_load_gen_input_types()` already do | Two independent precedents in this exact codebase; a third, slightly different implementation would be pure drift risk for zero benefit |

**Key insight:** every "don't hand-roll" item here is not a third-party library substitution (there are none to make) — it is "don't re-invent a pattern this exact repo has already built, tested, and run green three times." The risk in a phase like this is not choosing the wrong library; it is quietly diverging from an established in-repo idiom and creating a second, slightly different way of doing the same thing.

## Common Pitfalls

### Pitfall 1: The 10 new uncertainty marks have no capability home (will break the live D-01 invariant)

**What goes wrong:** Adding `RELATIONSHIP_CHARTS["uncertainty"] = (10 Wilke marks)` without also adding those 10 marks to some `CHART_CAPABILITIES` value causes `tests/test_viz_vocabulary_invariant.py::test_every_mark_has_a_capability_home` to fail — the mark universe (built from `RELATIONSHIP_CHARTS.values()` among other sources) will contain 10 marks that appear in no `CHART_CAPABILITIES`/`EXTRA_MARKS` value.
**Why it happens:** GA-2's decision text focuses on rejecting a *new data-input-type family* for these marks, which is correct, but doesn't by itself supply an existing family for them to join. The Phase-21 invariant (already shipped, already green, already gate-adjacent via a repo-integrity test) has an independent requirement that any new relationship-listed mark also be capability-homed.
**How to avoid:** Add the 10 marks to the existing `CHART_CAPABILITIES["interval-range"]` frozenset (it already models range/interval shapes: `box, violin, histogram, density, ecdf, strip, kde`) — no new coarse family, consistent with GA-2's rejection of new input-type ids, and it is the closest genuine data-signature fit (an uncertainty band, an error bar, and a box plot are all interval-shaped renderings of a distribution or estimate).
**Warning signs:** `python -m unittest tests.test_viz_vocabulary_invariant -v` going red on `test_every_mark_has_a_capability_home` with the 10 new mark names listed as orphans — run this command as the first verification step after adding the relationship key, before touching anything else.

### Pitfall 2: `references/finding-codes.md`'s pinned-total test is a silent trap

**What goes wrong:** A plan that mints `DSX-VIZ-071` and regenerates `finding-codes.md` (275→276) but does not also edit `tests/test_finding_catalogue_invariant.py`'s `_EXPECTED_TOTAL` and `_MINTED_CODES` will leave the full suite red — not because the new code is wrong, but because a pre-existing test literally asserts the old total.
**Why it happens:** The invariant test is not auto-derived from the catalogue file at test-collection time in a way that self-updates; its `_EXPECTED_TOTAL` and `_MINTED_CODES` are Python literals that must be hand-bumped every phase that mints, exactly as the file's own docstring documents happened for Phases 15/16/18/19.
**How to avoid:** Make "bump `test_finding_catalogue_invariant.py`" an explicit plan task in the same wave as the code mint, not a follow-up. `test_phase20_zero_mint_close.py` is a second, independent test asserting `max(present) == 122` for the `DSX-STA` family specifically — that one does **not** need touching (it's `DSX-STA`-scoped, not `DSX-VIZ`), but its existence is proof this pattern (hard-coded per-family high-water marks) recurs and should be checked for a `DSX-VIZ` analogue before assuming none exists. (Checked: none exists for `DSX-VIZ` today — this phase would be establishing the first one if it chooses to add a symmetrical Phase-22-close test, which is good practice but not required by any existing gate.)
**Warning signs:** `python -m unittest discover -s tests -q` reporting a failure in `test_finding_catalogue_stays_at_275_codes` or `test_code_set_is_phase12_snapshot_plus_the_sanctioned_mints` after the code mint — both currently read literal `275`/`_MINTED_CODES` and will not auto-adjust.

### Pitfall 3: `references/chart-selection.md` currently ships the citation HQ-27 corrected

**What goes wrong:** `references/chart-selection.md`'s "Encoding accuracy" section reads `position on a common scale → length → angle → area → colour saturation → volume` — this is precisely the 7-item strict ordering (with the false `length > angle` relation and the non-existent "density" term) that HQ-27's T1-1 finding corrected. If the plan only touches `references/question-taxonomy.md` and adds new content to `chart-selection.md` without also **fixing** this pre-existing line, the shipped repo ends up self-contradictory: a new, correct 6-rank-with-ties structural-criterion test alongside an old, incorrect prose sentence making the opposite claim.
**Why it happens:** This line predates HQ-27's verification pass and was written when the project still held the (now-corrected) 7-item belief; REQ-P22-05 is scoped as "gate extensions," which could be read as not touching this prose file, but REQ-P22-04 explicitly is "edits to ... chart-selection.md."
**How to avoid:** Treat the "Encoding accuracy" line as an in-scope Pitfall-3 fix within the REQ-P22-04 edit, not a separate ticket. Replace with D-1's shipping form verbatim (rank1 position_common · rank2 position_nonaligned · rank3 {length, direction/slope, angle} · rank4 area · rank5 {volume, curvature} · rank6 {shading, colour_saturation}), stated as ranks-with-ties, not a linear arrow chain.
**Warning signs:** Grep `references/*.md` for the literal string `"volume"` near `"colour saturation"` or `"angle"` immediately before `"area"` in a single arrow chain — both are tells of the pre-correction ordering.

### Pitfall 4: DVC URLs are not name-derivable — hand-typing them silently ships dead links

**What goes wrong:** The HQ-27 pack explicitly flags (T2-4) that the Data Visualisation Catalogue's URL pattern `datavizcatalogue.com/methods/{name}.html` is "NOT mechanically derivable from chart names (`treemap.html` has no underscore)." A plan or execute step that assumes `snake_case_name.html` for every DVC-cited reference-only row will ship some fraction of broken citation links.
**Why it happens:** Every other citation source in this phase (FT category names, Wilke mark names, Munzner chapter numbers) is either a fixed short list or a stable numeric/textual locator; DVC is the one source whose URL construction looks mechanical but isn't.
**How to avoid:** Resolve and store each DVC URL used in a reference-only row at build/execute time (visit or otherwise confirm the actual URL), never auto-generate from the display name, exactly as HQ-27 instructs.
**Warning signs:** Any reference-only row whose DVC URL was generated by a `.replace(" ", "_").lower()`-style transform without a corresponding manual confirmation note.

## Code Examples

Verified patterns from the live tree (all read directly during this session, line numbers current as of 2026-09-03):

### Existing relationship-match check (the function `_check_relationship_match` will keep working once `"uncertainty"` is added — no change needed to its logic)
```python
# Source: dsx/checks/viz.py:122-160 (live)
def _check_relationship_match(
    visual: dict, chart_type: str, label: str, where: str, report: Report
) -> None:
    relationship = normalize(visual.get("relationship", ""))
    ...
    admissible = RELATIONSHIP_CHARTS.get(relationship)
    if admissible is None:
        report.add(
            "DSX-VIZ-011", "MEDIUM",
            f"'{label}' declares unrecognised relationship {visual.get('relationship')!r}",
            detail="Allowed: " + ", ".join(sorted(RELATIONSHIP_CHARTS)),
            ...
        )
```
This function is entirely mechanical over the `RELATIONSHIP_CHARTS` dict — adding the 11th key is sufficient for `_check_relationship_match` to correctly admit/reject uncertainty marks. No code change to this function is required, only to the dict it reads.

### The banned-type refusal record shape to replicate for `gauge`/`word_cloud`
```python
# Source: dsx/checks/viz.py:61-71 (live) — radar and dual_axis_line, the two entries
# closest in citation-maturity to what gauge/word_cloud need
"radar": {
    "reason": "Radar area scales with the square of the value and depends on axis order.",
    "code": "DSX-VIZ-001",
    "citation": "Duan et al. 2023 (J Clin Epidemiol 156:85-94), Introduction — "
                "area-vs-axis-order and area-proportional-to-square-of-value criticisms",
},
```
(Citation text shown is the HQ-27-signed replacement for the current PROVISIONAL placeholder — REQ-P22 execute swaps this string per CONTEXT.md item 4.)

### The D-05 docstring convention a new `DSX-VIZ-071` function must carry
```python
# Source: pattern established across dsx/checks/design.py, dsx/frame/admissibility.py,
# dsx/checks/chart_review.py — every _D05_ALLOWLIST_CODES-covered function has both lines
def _check_uncertainty_vocabulary(...) -> None:
    """One sentence describing the check.

    Citation: Wilke, C.O. (2019), Fundamentals of Data Visualization, O'Reilly,
    ch.5 §5.6 (mark set) and ch.16 §16.2 (frequentist/Bayesian paradigm symmetry).
    Structural criterion: a declared uncertainty mark must be one of the ten
    named §5.6 members; no computed threshold.
    """
```
`scripts/gen-finding-catalogue.py::_resolve_docstrings()` walks up from each `report.add(...)` call to the nearest enclosing `FunctionDef` and reads its docstring for exactly these two regex-matched lines (`_CITATION_RE`, `_REFVALUE_RE`) — the docstring is not decorative, it is what `--check` parses.

## State of the Art

| Old (pre-HQ-27 / SCOPE-doc-era) claim | Corrected (HQ-27-signed) form | When changed | Impact |
|---|---|---|---|
| 7-item strict perceptual ordering, `length > angle`, includes "density" | 6 ranks WITH TIES; `length`/`direction`/`angle` tied at rank 3; "density" absent from the 1984 paper | HQ-27, 2026-09-03 (D-1) | `chart-selection.md`'s existing "Encoding accuracy" line must be rewritten (Pitfall 3); the new structural-criterion test must assert `<=`, never `<` |
| Uncertainty vocabulary = "fan chart, quantile dot plot, half-eye, gradient CI band" (SCOPE.md §3.1/3.2) | Wilke's actual §5.6 ten marks (see D-2 above); "fan chart" and "gradient CI band" do not exist in the source | HQ-27, 2026-09-03 (D-2) | Any code, docstring, or catalog row using the SCOPE doc's four original names is wrong and must use the ten-mark vocabulary instead |
| `radar`'s citation = "Tufte 1983 / Munzner 2014... PROVISIONAL" | Duan et al. 2023, J Clin Epidemiol 156:85-94 | HQ-27, 2026-09-03 | One-line string swap in `viz.py`'s `BANNED_TYPES["radar"]["citation"]` |
| "FT Visual Vocabulary is MIT-licensed" (repo-license read alone) | MIT covers only the software; content is FT-copyrighted, syndication-gated | HQ-27, 2026-09-03 (D-3) | Catalog must attribute + describe independently, never vendor the poster |
| DVC ≈ 77 chart methods | 60, verified twice | HQ-27, 2026-09-03 (T2-4) | Any "DVC has ~77 types" language elsewhere in the repo (SCOPE doc, ROADMAP) is stale relative to the signed count |
| FT = 72 named entries | 74 named / 66 distinct | HQ-27, 2026-09-03 (T2-1) | Same — use the corrected count in any prose the catalog ships |

**Deprecated/outdated:** the entire `.planning/research/V2.3-V2.4-SCOPE.md` §3.1/§3.2 uncertainty-family and perceptual-rank language is superseded by the signed HQ-27 pack; it remains useful for the L1-L5 heuristic-layer *structure* (which citations were NOT corrected — Munzner ch.2/3/6, Datawrapper cardinality) but must not be copied verbatim for the corrected items.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | The 10 uncertainty marks should be homed into `CHART_CAPABILITIES["interval-range"]` specifically (rather than a different existing family, or via a new `EXTRA_MARKS` entry on a specific IT id) | Architecture Patterns, Pitfall 1 | If the plan/execute chooses a different home, `test_every_mark_has_a_capability_home` still passes as long as *some* home is chosen — the specific family named here is a recommendation, not a structural requirement; the structural requirement (a home must exist) is HIGH confidence, the specific family choice is MEDIUM |
| A2 | A brand-new function (e.g. `_check_uncertainty_vocabulary`) is the right place to mint `DSX-VIZ-071`, rather than extending the existing `_check_uncertainty` | Code Examples, Common Pitfalls | `_check_uncertainty` (line 423) answers "did you show uncertainty at all" (property-based) — CONTEXT.md explicitly says this is "RETAINED complementary, not replaced," implying a distinct function for the new selection-surface check; if plan instead extends the same function, the D-05 docstring resolution (`_resolve_docstrings`) would attribute both codes to one function's docstring, which is legal but conflates two distinct citation obligations (Wilke §5.6 mark-membership vs. the existing uncertainty-property citation, which currently has none) |
| A3 | Reference-only row selection (which ~15 spine types fill FT function-coverage gaps) is genuinely plan/execute discretion and not something this research should pre-select | GA-1 discretion note | If the planner expected research to shortlist candidate reference-only rows, this gap would need filling before execute; CONTEXT.md marks this "not frozen here" and "execute (S2-3) work," so this research treats it as correctly out of scope |

**If this table is empty:** N/A — see rows above.

## Open Questions

1. **Are Abela 2008 and Few's Graph Selection Matrix citable for the L1/L2 heuristic layers?**
   - What we know: `.planning/research/V2.3-V2.4-SCOPE.md` §3.2 names them as the provenance for L1 ("pattern-origin credit") and L2 ("corroboration"). Neither appears anywhere in the signed HQ-27 pack (`.planning/v2.4-D05-EVIDENCE-PACK.md`) — not in the 13 dispositioned rows, not in the 8 "still unverified" items either. They were simply never submitted for HQ-27 verification.
   - What's unclear: whether "the S2-1 discuss applies HQ-27 as hard constraints" implicitly means anything *outside* HQ-27's scope needs its own separate verification, or whether these two sources are low-stakes enough (they're framed as "pattern-origin credit"/"corroboration," not load-bearing claims) to ship as unverified background attribution.
   - Recommendation: the plan should either (a) drop Abela/Few's Graph Selection Matrix from the L1/L2 edits entirely and cite only the HQ-27-signed Munzner ch.3 (task taxonomy, T2-6, confirmed) for L1 and the FT nine-category axis (T2-1, D-3-corrected) for L2, or (b) explicitly tag any Abela/Few's-Matrix reference as `[ASSUMED — not HQ-27-verified]` in the shipped Markdown so a future audit can find it. Given the phase's own "D-05 status" note ("No new primary-source read is owed to unblock the build... the 8 items HQ-27 lists as still unverified are not relied on by any shipping row"), option (a) is the safer default and the one this research recommends.

2. **Does `DSX-VIZ-072` get minted, and for what check?**
   - What we know: GA-3 reserves it "contingently, only if plan (S2-2) finds a second distinct uncertainty check is warranted (e.g. paradigm-mismatch detection)." No such check exists today; `_check_uncertainty` (070) and the proposed new mark-membership check (071) together cover "did you show uncertainty" and "is the mark a recognised member" — a hypothetical 072 would need to answer a third, different question (e.g. "does the declared mark match the declared paradigm, frequentist vs Bayesian").
   - What's unclear: whether a paradigm-mismatch check is decidable from a declared spec alone (D-01/D-02 requires declarations-only, no rendering) — e.g. would the visual need to declare both `uncertainty_mark` and `paradigm` fields for this to be checkable, and does `PARADIGMS`/`PARADIGM_JUSTIFICATIONS` (already in `dsx/spec.py:671-680`, from Phase 10's D-12 work) supply the paradigm vocabulary this check would key on?
   - Recommendation: this research found the necessary supporting vocabulary already exists (`dsx/spec.py`'s `PARADIGMS = {"frequentist", "bayesian"}`), so a 072 paradigm-consistency check is technically feasible if the plan wants it, but is not required by any requirement text verbatim — REQ-P22-02 only asks that the family be "D-12a-clean" (symmetric), which the 11th-key structure already achieves by construction per GA-2's own reasoning, without needing an enforcement code. Default to **not** minting `-072` unless the plan finds a concrete, checkable mismatch scenario worth gating.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | All checks, tests, generator scripts | ✓ | 3.12.10 | — |
| `python -m unittest` (stdlib) | Full suite, repo-integrity tests | ✓ | stdlib, no install needed | — |
| Bash / POSIX shell (for `scripts/check.sh`) | Full gate verification | ✓ (via Git Bash per repo shell environment) | — | PowerShell-native equivalent commands if `check.sh` itself is not run directly |
| pandas/scipy/numpy | **Explicitly forbidden on the gate path** (D-01/D-02) | N/A by design | — | N/A — confirmed absent from `dsx/checks/viz.py` and `dsx/spec.py` imports |

**Missing dependencies with no fallback:** none — this phase has no external dependency at all.
**Missing dependencies with fallback:** none applicable.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` |
| Config file | none — `python -m unittest discover -s tests -q` is the whole-suite invocation used by `scripts/check.sh` |
| Quick run command | `python -m unittest tests.test_viz_vocabulary_invariant tests.test_finding_catalogue_invariant -v` (the two directly-affected invariant modules; confirmed to run in <0.01s today) |
| Full suite command | `python -m unittest discover -s tests -q` (confirmed 1471 tests, ~41s, all green, pre-phase baseline established this session) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P22-01 | Catalog has 75-90 rows, 3 axes + citation per row, DSX-admissible vs reference-only flagged | repo-integrity | `python -m unittest tests.test_XX_chart_catalog_invariant -v` (new module reading the fenced JSON block) | ❌ Wave 0 |
| REQ-P22-01 | Every catalog refusal row's cited ban exists in live `BANNED_TYPES` (drift guard) | repo-integrity | same new module — a catalog↔vocabulary conformance check | ❌ Wave 0 |
| REQ-P22-02 | `"uncertainty"` is an 11th `RELATIONSHIP_CHARTS` key with exactly Wilke's 10 marks | unit (existing pattern) | `python -m unittest tests.test_viz_vocabulary_invariant -v` (extend `_mark_universe`/homing assertions, or add a targeted assertion) | ✅ extend existing |
| REQ-P22-02 | The 10 uncertainty marks have a capability home (Pitfall 1) | unit (existing) | `python -m unittest tests.test_viz_vocabulary_invariant.TestEveryMarkHasAHome.test_every_mark_has_a_capability_home -v` | ✅ existing, currently green, must stay green |
| REQ-P22-03 | `facet_by` declaration exists and its smell remedy routes to an existing check, mints no code | repo-integrity or unit | new assertion in `tests/test_viz_vocabulary_invariant.py` or a new small test module; also a `dsx check smells` smoke over a spec declaring `facet_by` | ❌ Wave 0 |
| REQ-P22-04 | `question-taxonomy.md`/`chart-selection.md` edits are route-and-cite (no parallel decision tree); `skills/dsx-visualize/SKILL.md` relationship list = 11 | repo-integrity (grep-based) or manual review | grep-count assertion (`grep -c` the relationship names) OR manual-only, justified: prose-quality judgment | manual-only justified — "no parallel decision tree" is a structural-prose judgment, not mechanically decidable |
| REQ-P22-05 | `DSX-VIZ-071`(/-072) carries `Citation:`/`Structural criterion:` docstring lines + `# D-05:` test marker | build gate (existing mechanism) | `python3 scripts/gen-finding-catalogue.py --check` (fails if `_D05_ALLOWLIST_CODES` doesn't include the new code, or the docstring/test-marker is missing) | ✅ existing mechanism, needs the new code added to the allowlist |
| REQ-P22-05 | Perceptual tie-break: `rank(a) <= rank(b)`, never `<`, over the catalog's rank data | repo-integrity | same new `test_XX_chart_catalog_invariant.py` module | ❌ Wave 0 |
| REQ-P22-05 | Catalogue total is additive-only (275→276 or 277) | build gate (existing, currently hard-coded) | `python -m unittest tests.test_finding_catalogue_invariant -v` (after editing `_EXPECTED_TOTAL`/`_MINTED_CODES`) + `python3 scripts/gen-finding-catalogue.py --check` | ✅ existing, must be edited (Pitfall 2), not just re-run |

### Sampling Rate

- **Per task commit:** `python -m unittest tests.test_viz_vocabulary_invariant tests.test_finding_catalogue_invariant -v` (sub-second; run after every `viz.py`/`spec.py`/`gen-finding-catalogue.py` edit)
- **Per wave merge:** `python -m unittest discover -s tests -q` (full 1471-test suite, ~41s) + `python3 scripts/gen-finding-catalogue.py --check` + `python3 scripts/gen-input-types.py` (regenerate and diff, confirm no unexpected change) + `sh scripts/check.sh` if Bash is available in the wave's environment
- **Phase gate:** Full suite green, `gen-finding-catalogue.py --check` exits 0, `gen-input-types.py` regeneration produces no unreviewed diff, before `/gsd-verify-work`

### Wave 0 Gaps

- [ ] `tests/test_XX_chart_catalog_invariant.py` (name TBD at plan) — new module covering REQ-P22-01 (band 75-90, three-axes-per-row shape, refusal-row↔`BANNED_TYPES` conformance) and REQ-P22-05 (perceptual tie-break `rank(a) <= rank(b)` structural criterion, non-vacuity guard mirroring `test_mark_universe_is_non_vacuous`'s pattern)
- [ ] `references/chart-catalog.md` itself — the fixture the above test reads; does not exist yet (REQ-P22-01's primary deliverable)
- [ ] A `facet_by`-declaring test fixture (either a new example spec or an inline dict in a new test) covering REQ-P22-03's smell-routing behavior
- [ ] No new framework install needed — `unittest` is stdlib and already the whole suite's framework

## Security Domain

`security_enforcement: true`, `security_asvs_level: 1` (`.planning/config.json`). This phase's surface is reference documentation and gate-vocabulary dict edits with no user input, no auth, no network, no data persistence beyond the repo's own Markdown/Python files — the ASVS categories that normally apply to application code (auth, session, access control, injection) are structurally inapplicable here, matching Phase 21's precedent (same domain shape, same conclusion).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No auth surface in this repo-internal reference/gate-vocabulary phase |
| V3 Session Management | no | Same |
| V4 Access Control | no | Same |
| V5 Input Validation | marginally yes | The new `DSX-VIZ-071` check validates a *declared* uncertainty-mark string against a closed vocabulary (the 10 Wilke names) — this is the same closed-membership-validation pattern every other `dsx/spec.py` vocabulary already uses (e.g. `PARADIGMS`, `ICC_MODELS`); no new pattern is introduced |
| V6 Cryptography | no | No cryptographic surface |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| A catalog row claims a refusal the live gate does not enforce (the "drift surface" CONTEXT.md names explicitly) | Tampering (of trust, not data) — a false authority claim | The catalog↔vocabulary conformance repo-integrity test (Wave 0 gap above); every refusal row's citation must resolve to a real `BANNED_TYPES` key |
| A shipped citation traces to one of HQ-27's 8 "still unverified" items, or to Abela 2008/Few's Graph Selection Matrix (never submitted to HQ-27 at all) | Repudiation-adjacent — an unverifiable claim presented as verified | Grep every new citation string in `chart-catalog.md`/`chart-selection.md`/`viz.py` docstrings against the HQ-27 pack's signed sources before shipping; treat any citation not traceable to a signed HQ-27 row as `[ASSUMED]` |

## Sources

### Primary (HIGH confidence — direct code/file reads and executed commands this session)

- `dsx/checks/viz.py` (full file, 460 lines) — `RELATIONSHIP_CHARTS`, `BANNED_TYPES`, `_check_relationship_match`, `_check_uncertainty`, all check function bodies
- `dsx/spec.py` (lines 260-680) — `DATA_INPUT_TYPES`, `CHART_CAPABILITIES`, `PARADIGMS`
- `scripts/gen-input-types.py` (full file) — `FAMILY`, `EXTRA_MARKS`, JSON-embedding pattern
- `scripts/gen-finding-catalogue.py` (full file, 501 lines) — `_D05_ALLOWLIST_PREFIXES`, `_D05_ALLOWLIST_CODES`, `_resolve_docstrings`, `check_d05`
- `references/finding-codes.md` (grep for `DSX-VIZ`, full-file code count) — confirmed 275 total, 20 VIZ codes
- `references/input-type-inventory.md` (lines 1-80) — the JSON-in-Markdown pattern precedent
- `references/question-taxonomy.md`, `references/chart-selection.md` (full files) — exact current content, including the superseded perceptual-ordering line
- `skills/dsx-visualize/SKILL.md` (full file) — relationship enumeration ripple point
- `dsx/checks/smells.py` (full file) — `DENSITY_MARKS`, `_check_atoms_under_density` (DSX-SMELL-007), confirmed no "overplotting" code exists
- `dsx/input_types.py` (full file) — `permitted()` narrowing logic
- `tests/test_viz_vocabulary_invariant.py` (full file) — live D-01/D-02 invariant, executed and confirmed green
- `tests/test_finding_catalogue_invariant.py` (full file) — live pinned-total/set-identity gate, executed and confirmed green
- `tests/test_phase20_zero_mint_close.py` (full file) — precedent pattern for a phase-close zero/N-mint proof
- `python -m unittest discover -s tests -q` — executed, 1471 tests, all green, this session
- `.planning/v2.4-D05-EVIDENCE-PACK.md` (full file) — the signed HQ-27 pack, source for all D-1..D-4 citation content
- `.planning/phases/22-catalog-spine-uncertainty-heuristic/22-CONTEXT.md` (full file) — GA-1/GA-2/GA-3, binding decisions
- `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, `.planning/config.json` (full reads)
- `.planning/HUMAN-QUEUE.md`, `.planning/LOOP-LEDGER.md` (grepped for HQ-30/S2-2 status)

### Secondary (MEDIUM confidence)

- `.planning/research/V2.3-V2.4-SCOPE.md` §3.1-3.2 — provides the 5-layer heuristic's L1-L5 structure and the original (partially-superseded) uncertainty/perceptual language; useful for structure, must be cross-checked against HQ-27 for content
- `.planning/phases/21-viz-vocabulary-reconciliation/21-RESEARCH.md` (partial read, first 120 lines) — precedent research format and precedent findings (EXTRA_MARKS regeneration gotcha, importlib idiom)
- `.planning/v2.4-SCOPE-RECHECK.md` — confirms REQ-P22-01..05 "still-valid, no artifact exists" pre-conditions

### Tertiary (LOW confidence)

- None — no web research was performed (config confirms all external search providers disabled; this phase has no library/framework surface requiring it).

## Metadata

**Confidence breakdown:**
- Standard stack / architecture: HIGH — every structural claim is a direct read of the live tree, cross-checked by running the actual test suite and the actual gate-check commands
- D-05 citation content: HIGH for everything traced to the signed HQ-27 pack; explicitly flagged LOW/Open-Question for Abela 2008 and Few's Graph Selection Matrix, which are outside HQ-27's scope entirely
- Pitfalls: HIGH — Pitfalls 1, 2, and 3 are each backed by either a currently-green test whose assertions were read in full, or a direct string comparison against the signed pack's corrected text
- Reference-only row selection (GA-1's ~15-row tunable remainder): correctly out of scope for this research per CONTEXT.md's own discretion note — not a confidence gap, a deliberate deferral to plan/execute

**Research date:** 2026-09-03
**Valid until:** the live tree (line numbers, test names, dict shapes) is only guaranteed current as of this commit; re-verify line numbers if `dsx/checks/viz.py` or `scripts/gen-finding-catalogue.py` are touched by any other phase before Phase 22 executes. The HQ-27 citation content itself does not expire on a calendar timescale (it is a signed, closed verification pack), but should not be treated as extensible to any citation not already in it.
