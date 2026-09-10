# Phase 28: Evidence case — magnitude no test computed - Research

**Researched:** 2026-09-07
**Domain:** dsx claims-discipline check (`dsx/checks/claims.py`, `DSX-CLM-*`) + D-13 measure-first
corpus-fixture mint (conditional on a live miss) + finding-catalogue/harness wiring
**Confidence:** HIGH — every locator below was read live this session (`Read`/`Grep` against the
working tree, CPython 3.12.10 real interpreter confirmed present, no gate re-run performed). Where
a CONTEXT.md-claimed locator did not match the live line range exactly, it is flagged loudly in
`## Discrepancies`, never silently "corrected."

> Scope: this is the S4-2 *plan-input* research. `28-CONTEXT.md`'s design (D-28-00..05) is FROZEN
> and is NOT re-opened here. This file verifies the code locators the plan will touch, maps the
> six research targets the orchestrator specified, and hands the planner an implementation-ready
> map. **The live miss is UNMEASURED as of this research** (D-13) — nothing here assumes an
> outcome; the plan-decomposition section is written to be correct under EITHER measured verdict.

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions (FROZEN — do not re-open)

- **D-28-00 (D-13 correction):** the scope's literal "magnitude in no test" case is CAUGHT by
  existing `DSX-CLM-033` (union-membership). The only honest live-miss seam is the
  **collision/mislabel construction**: the claim's own numbers (27/18) are the REAL reported
  numbers of *other* metrics' tests, so `DSX-CLM-033` clears on its full logic while no test
  computed the claimed metric (churn). The literal-wording case is preserved as the NO-MINT
  control shape.
- **D-28-01 (corpus fixture shape):** descriptive/observational churn fixture; two `results.tests[]`
  entries on OTHER metrics (`revenue_per_user`, `activation_rate`), each fully reporting
  effect+CI+`effect_size_kind`; one `association`-typed claim on churn (27% vs 18%, `base_n`
  declared) whose literals collide with tests A/B; **no `claims[].supported_by` declared** →
  `DSX-CLM-034` (if minted) stays silent on this fixture, an honest MISS (attribution, not
  detection — Phase-27 precedent).
- **D-28-02 (pass/fail rule):** measured at all four gate points from a fresh tempdir, `claims`
  registers only at verify/ship, threshold HIGH. CAUGHT ⇒ no-mint close. LIVE MISS ⇒ all four
  points pass on the merits (after subtracting documented, swap-still-fires incidental codes).
  A table of existing checks that MUST clear honestly is pre-registered (see `## Per-Target
  Findings` §2 below for the verified locators).
- **D-28-03 (rounding tolerance):** `claims[].rounding` = significant figures, default 2, applying
  the same ×100 percent/proportion scale bridge `DSX-CLM-033` already uses. `rounding` may only
  tighten, never loosen, relative to `DSX-CLM-033`'s rel-5%/abs-5e-4 window.
- **D-28-04 (reserved code):** `DSX-CLM-034`, next-free-in-family in the `03x`
  evidence-pointer/overlap tier (030 no-pointer, 031 unresolved, 032 anchor-absent, 033
  CRITICAL numeric-overlap). RESERVED, not minted, until S4-3 confirms a live miss.
- **D-28-05 (D-05 citation honesty):** Wilkinson & TFSI (1999) is the MOTIVATING PRINCIPLE
  (mandates reporting effect sizes/intervals), NOT the mechanism. The check enforces a
  declaration-level traceability corollary (`DSX-REP-061` mould — text/declared-number overlap,
  never a recomputation). The docstring must say this plainly and must record the bounded-catch
  honesty: the check catches via the **stray** number, not metric-identity.
- **Guardrails (non-negotiable):** FREEZE-BEFORE-MEASURE; NOTHING MINTED PRE-MEASUREMENT; HARD
  STOP AT THE MINT BOUNDARY; HONEST MEASUREMENT (fresh tempdir, unmodified gate, verbatim
  recording, swap-still-fires counterfactual applied by literal code).

### Claude's Discretion (plan inputs recorded, not over-frozen)

- `claims[].supported_by` — recommended a **string** = the `metric` value of the
  `results.tests[]` entry the claim rests on (list tolerated → union of numbers). Additive,
  opt-in, absent → silent.
- `claims[].rounding` — int significant figures, default 2.
- Severity — the round **leans HIGH** (030–032 traceability tier, non-overlapping with 033's
  CRITICAL). S4-2 (this plan) finalises against REQ-P28-02's exact text and the live measurement.
- Harness wiring names — fixture slug `magnitude-without-computed-effect`; empty
  `_EXPECTED_CAUGHT_DEFECTS`/`_EXPECTED_VAL_CODES` entries; golden ship set measured live; spec
  count 43→44; catalogue total 277→278 — **all conditional on a confirmed live miss.**

### Deferred Ideas (OUT OF SCOPE)

- Re-opening the D-28-00 case-shape shift (scope's literal wording → collision construction).
- Re-litigating the rounding-tolerance-vs-DSX-CLM-033-tolerance reconciliation beyond confirming
  non-double-coding on the shipped fixture (D-28-03 already settles the direction; only the
  live measurement, not argument, may adjust it).
- Any change to `dsx/checks/dq.py`, `dsx/checks/viz.py`, or the chart corpus (out of scope per
  REQUIREMENTS.md `## Out of Scope`).
- Manufacturing a corpus miss to justify a mint (forbidden by D-13; explicit `## Out of Scope`
  entry in REQUIREMENTS.md).
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description (`.planning/REQUIREMENTS.md:95-112`) | Research support |
|----|-----|-----|
| REQ-P28-01 | A known-bad corpus case whose `claims[].text` asserts a magnitude no `results.tests[]` entry computed, while every existing claims/narrative/stats check passes at default threshold (`DSX-CLM-070` cleared by declared base, `DSX-STA-012` cleared by effect sizes). Measured live before any check is designed. | `## Per-Target Findings` §2–3 (existing-checks-clear table verified; four-point measurement protocol verified); `## Recommended Plan Decomposition` Wave 1 |
| REQ-P28-02 | If live miss: `claims[].supported_by` cross-reference + a check that every numeric literal in the claim text appears among the cited test's reported numbers within a declared rounding tolerance (`DSX-REP-061` mould, never recomputation); D-05 citation (Wilkinson & TFSI 1999); D-06 next-free `DSX-CLM-*` number. If caught, recorded, nothing minted. | `## Per-Target Findings` §1 (DSX-REP-061 mould verified), §2 (vocabulary slot verified), §5 (D-05 gate mechanics + placement risk); `## Recommended Plan Decomposition` Wave 1 (conditional) |
| REQ-P28-03 | Corpus harness entries complete; brief §6.5 item 8 row rewritten with measured evidence. | `## Per-Target Findings` §4 (every harness map/count locator verified); `## Recommended Plan Decomposition` Wave 2 (conditional) |
</phase_requirements>

---

## Summary

`28-CONTEXT.md`'s design is frozen and — on live-code verification this session — **every
load-bearing locator checks out**. `DSX-CLM-033`'s union-membership mechanic (`claims.py:343-401`),
its bare-integer exclusion (`:404-436`), its ×100 scale bridge (`:360-368`, exact) and its
rel-5%/abs-5e-4 tolerance (`:439-443`, exact) are all confirmed exactly as described, so D-28-00's
central claim — the literal item-8 case is already caught, only the collision construction is a
genuine live-miss seam — is sound. `DSX-REP-061` (`dsx/checks/repro.py:285-388`, fire site
`:372-386`) is confirmed as the correct mould: a declaration-gated, opt-in check that parses a
committed artifact's declared numbers and compares them against `results.tests` with a numeric
tolerance, never re-running anything — the right shape to imitate for `DSX-CLM-034`, though its own
tolerance (`math.isclose(rel_tol=1e-2)`) is NOT sig-figs; the sig-figs comparator must be written
fresh per REQ-P28-02's binding text. The `claims[].` schema slot (`templates/ANALYSIS-SPEC.yaml:
299-308`) is exactly where `supported_by`/`rounding` belong, following the existing
`base_n`/`from_value`/`to_value` commented-optional-key convention. `_SECTION_65_ITEM_IDS`'s item-8
string is confirmed **exact** at `tests/test_known_bad_corpus.py:853` — this is the single most
load-bearing harness locator and it is dead-on. `_D05_ALLOWLIST_CODES` (`scripts/gen-finding-
catalogue.py:183-211`) confirms the exact-code-not-prefix precedent already used four times for
other pre-existing families (`DSX-ML-*`, `DSX-VIZ-*`, `DSX-STA-*`, `DSX-CODE-*`) — and confirms
**no `DSX-CLM-*` code has ever carried a D-05 citation before**: `DSX-CLM-034` would be the first,
so the exact-code (never prefix) discipline is doubly important here. The catalogue's live total is
confirmed **277** and the spec count **43** (post-Phase-27), matching CONTEXT's stated pre-mint
baseline exactly, so the 277→278 / 43→44 pins are correctly anticipated.

**One structural risk not present in Phase 27, flagged for the plan-checker (see
`## Recommended Plan Decomposition`):** Phase 27 measured its live miss in a pre-plan spike
(S3-1/S3-3, before any PLAN.md existed), so its plans were written unconditionally against an
already-known verdict. Phase 28's own frozen roadmap (`28-CONTEXT.md` §5, `.planning/STATE.md`)
places the measurement at **S4-3 (execute)**, i.e. *after* this plan is authored (S4-2) — meaning
**S4-2 must write a plan whose first task performs the D-13 measurement and whose later tasks are
explicitly conditional on that task's recorded verdict.** This is a real authoring risk (an
ambiguous conditional reads as "mint by default"), addressed concretely below.

**A handful of CONTEXT locators are off by a small margin (never load-bearing, never contradicting
the design) — see `## Discrepancies`.** None require re-opening a frozen decision; all are line-
range imprecision the plan should cite correctly.

---

## Per-Target Findings

### 1. `DSX-REP-061` — the mould, verified

`dsx/checks/repro.py:285-388` (`_check_reproduce_report`), fire site `:372-386`. Mechanic, read
verbatim:

- **Opt-in / declaration-gated:** silent unless `reproducibility.reproduce_report` is declared
  (`:305-307`) AND `results.tests` is non-empty (`:309-311`) — mirrors exactly the
  `claims[].supported_by`-gated silence D-28-01 requires for `DSX-CLM-034`.
- **Never recomputes:** it locates a committed markdown file (mirrors `_check_code_pointer`'s
  entrypoint-resolution idiom, `:313-320`), parses the FIRST fenced ` ```yaml ` block with a
  CRLF-safe regex (`:337-345` — consistent with this repo's CRLF-checkout rule), and reads a
  **declared** number off it. No pandas, no re-run, no execution (docstring `:285-304`, explicit:
  "The gate re-runs nothing... never executes the entrypoint").
- **Honest opt-out branch:** `status: skipped|unable` short-circuits the comparison (`:347-352`)
  — the direct precedent for D-28-01's "fixture declares no `supported_by` → stays silent" design
  (same shape: an absent/opted-out declaration means no finding, never a lie-detector).
- **Tolerance is NOT sig-figs:** `math.isclose(report_value, spec_value, rel_tol=1e-2, abs_tol=1e-9)`
  (`:367-370`) — a flat 1% relative tolerance, not significant-figures rounding. **This is the one
  place DSX-CLM-034 must diverge from the DSX-REP-061 mould**, because REQ-P28-02's text is
  binding on `rounding` = sig-figs (D-28-03) — the *mechanic* (declaration → text/number overlap,
  never a recompute) is what DSX-CLM-034 borrows from DSX-REP-061; the *tolerance function* is
  new, sig-figs-based, plus D-28-03's ×100 scale bridge reuse from `DSX-CLM-033`.
- **Confirms the "never a recomputation" honesty claim in D-28-05** is achievable and precedented
  — DSX-REP-061 is proof this repo already ships exactly this class of check.

### 2. Additive claims-schema keys — location and read idiom

`templates/ANALYSIS-SPEC.yaml:299-308` — the `claims:` block, read in full:

```yaml
claims:
  - text: "<the claim exactly as it will appear>"
    type: descriptive              # descriptive | association | predictive | causal | prescriptive
    evidence: "RESULTS.md#anchor"
    population: "<who this applies to>"
    # ci: [lower, upper]
    # identification: <overrides design.identification for this claim>
    # base_n: null                 # absolute base when text has a relative %
    # from_value: null             # optional pair for "up X% from A to B"
    # to_value: null
```

`supported_by`/`rounding` slot in as two more commented-optional lines after `# to_value: null`,
exactly matching the existing convention (`base_n`/`from_value`/`to_value` are all optional,
commented, additive). **Confirmed no schema-shape validator enumerates allowed claim keys**:
`dsx/spec.py:1285-1319` (`_validate_claims_shape`) checks only `text` (blank → `DSX-SPEC-060`) and
`type` (missing/unrecognised → `DSX-SPEC-061`/`062`); it does not reject unknown keys. This is the
exact same finding Phase 27's research made for `model.feature_provenance[]` against
`_validate_model_shape` (`dsx/spec.py:1254-1282`) — **no `dsx/spec.py` change is required** for the
new fields to validate silently on every existing spec.

**Read idiom for the new check:** `dsx/checks/claims.py`'s per-claim loop already resolves `tests`
(`claims.py:73-74`, `results.tests`) and iterates `claims` with `text`/`ctype`/`where` bound per
claim (`:76-88`). A new `_check_supported_by_traceability(claim, text, tests, where, report)` call
added to that loop reads `claim.get("supported_by")` (string or list, per D-28-01's discretion
note) and `claim.get("rounding", 2)`, resolves the union of numbers from the *named* test(s) only
(NOT the union-over-all-tests `DSX-CLM-033` uses — this is the whole point of the "per-cited-test,
declaration-gated" distinction the Architect persona made in `28-CONTEXT.md`'s §4 round), and
compares using a sig-figs comparator plus the same ×100 bridge `_check_numeric_overlap` uses
(`claims.py:360-368`).

**Placement warning for the plan (load-bearing for the D-05 gate, verified this session — see §5
below): do NOT add the `report.add("DSX-CLM-034", ...)` call inside the existing
`_check_numeric_overlap` function.** Write a brand-new function. Reason verified in §5.

### 3. The four-point measurement protocol

`tests/test_known_bad_corpus.py::_gate_findings` (`:996-1052+`), verified in full:

- Runs one real `dsx gate <point>` per call via `cli.main(argv)` inside a fresh
  `tempfile.TemporaryDirectory()` (`:1042`), with `--phase-dir` pointed at that tempdir so no
  `DECISIONS.jsonl` trail write lands under `examples/` — directly answers the orchestrator's
  "stray `DECISIONS.jsonl` false-fails two explain tests" hazard note: **the harness itself already
  avoids this by construction; a plan-time measurement spike must copy this same fresh-tempdir
  discipline, never running `dsx gate` against the repo root or a fixture's own directory.**
- `_seed_entrypoint(tmp, spec_path)` runs unconditionally before every gate point (`:1043`) — seeds
  the fixture's declared `reproducibility.entrypoint` file into the tempdir so `code`/`repro`
  checks (registered at execute/verify/ship, `dsx/cli.py:120-130`) can resolve it. **This means the
  D-28-01 fixture needs a real, committed entrypoint file even though it declares no `model:`
  block** — the entrypoint just needs to exist and be readable text (never executed); a minimal
  descriptive-stats script is sufficient, mirroring the narrative-only synthetic-CSV pattern Phase
  27 used (`27-RESEARCH.md §A`).
- `seed_plan_header(tmp, spec_path)` runs only for `point in ("verify", "ship")` (`:1044-1045`) —
  the `prereg` check's decision-trail precondition.
- `claims` is registered in `GATE_PROFILES["verify"]` and `GATE_PROFILES["ship"]` only
  (`dsx/cli.py:122,127` — see `## Discrepancies` for the exact line numbers vs. CONTEXT's cited
  `:123,128`); **absent from `plan`/`execute`** (`:116-120`). `GATE_THRESHOLDS["verify"]` and
  `["ship"]` are both `"HIGH"` (`dsx/cli.py:138-139`, exact match). This confirms: `DSX-CLM-034` (any
  severity ≥ HIGH) can only ever fire at verify/ship, never plan/execute — consistent with D-28-02's
  table, which lists `claims`-family checks only at those two points.
- The swap-still-fires counterfactual (D-28-02) is "applied by literal code, never narrative" —
  Phase 27's own spike script (`spike/feature-origin-leak-MEASURE.py`, referenced in
  `27-MEASUREMENT.md:73-85`) is the precedent artifact shape: a small script that runs
  `_gate_findings`-equivalent logic twice (once on the real fixture, once on a hand-edited swap
  variant) and diffs the CRITICAL/HIGH sets. Phase 28's plan should mirror this exactly: run the
  real fixture (27/18 collision) and a swap variant (27/18 replaced by churn's genuinely-reported
  numbers, if the fixture declared any — or, since the fixture as designed declares NO churn test
  at all, the swap is "the same claim text but with a `supported_by`-adjacent number that WOULD
  reconcile" as the counter-check) at all four points and confirm identical residual-code sets.

### 4. Harness wiring — every locator, verified

All locators below were read live this session (not assumed from CONTEXT):

| Map/constant | File:line (verified) | Current state | Edit required (if LIVE MISS) |
|---|---|---|---|
| `_EXPECTED_CAUGHT_DEFECTS` | `tests/test_known_bad_corpus.py:432` | dict, keyed by slug | add `"magnitude-without-computed-effect": frozenset()` (a MISS catches nothing) |
| `_TARGET_DEFECT_CODES` | `tests/test_known_bad_corpus.py:185` (declared) | subset-of-disk map | **no entry** — misses are absent from this map (Phase-27 precedent, `27-RESEARCH.md §C1`) |
| `_INCIDENTAL_GAP_CODES` | `tests/test_known_bad_corpus.py:65` | allowlist-with-inline-reason | edit only if the measured residual codes are NOT already documented there — must be re-measured, not assumed |
| `_SECTION_65_BACKLOG_CODES` | `tests/test_known_bad_corpus.py:832-837` | `{DSX-PAR-020, -021, -022, -030}` — confirmed does NOT contain any `DSX-CLM-*` or `DSX-ML-*` code | **no edit** — `DSX-CLM-034` ships to the catalogue if minted; adding it here would fail the disjointness assertion (`:1619-1624`) |
| `_SECTION_65_ITEM_IDS` | `tests/test_known_bad_corpus.py:845-855` | frozenset of 9 strings, exactly nine (`:855`) | **no edit** — item 8's string `"6.5-item-8-magnitude-without-computed-effect"` is at **exact line 853**, confirmed verbatim |
| `_EXPECTED_VAL_CODES` | `tests/test_frame_val.py:1363` | dict keyed by spec filename | add `"magnitude-without-computed-effect-ANALYSIS-SPEC.yaml": set()` — must be measured live, not guessed (this fixture has no causal `design.identification`, so `val`/`interference` checks likely clear trivially, but confirm) |
| `_GOLDEN_SHIP_FINDINGS` | `tests/test_causal_verb_golden.py:82` | dict keyed by repo-relative path | add the measured ship-residual frozenset for the promoted fixture path |
| Spec count | `tests/test_dsx.py:583` | `self.assertEqual(len(paths), 43, ...)` — confirmed live at **43** | 43 → 44 |
| `_EXPECTED_TOTAL` | `tests/test_finding_catalogue_invariant.py:40` | confirmed live at **277** | 277 → 278 |
| Phase-20 total pin | `tests/test_phase20_zero_mint_close.py:100` | confirmed live at **277** | 277 → 278 |
| Catalogue Total line | `references/finding-codes.md:16` | confirmed live `**Total: 277 codes.**` | regenerated automatically via `--write`, never hand-edited |
| `_D05_ALLOWLIST_CODES` | `scripts/gen-finding-catalogue.py:183-211` | frozenset, exact-code entries only; confirmed contains `"DSX-ML-034"` at `:209` (Phase 27 landed) and **zero** `DSX-CLM-*` entries | add `"DSX-CLM-034"` by exact code, with an inline comment following the four precedent-comment blocks already in this file (`:100-137,147-182,194-201,202-209`) |

**ATTRIBUTION sidecar falsifiability, verified mechanic (`tests/test_known_bad_corpus.py:1725-
1781`):** for `kind: "miss"`, the test asserts `absent_code` fires **nowhere CRITICAL** across all
four gate points (`:1766-1773`) — it checks only the CRITICAL union, never HIGH. This means: **even
if `DSX-CLM-034` ships at HIGH** (the round's severity recommendation), the falsifiability test
still passes as designed, because the fixture's declared absence of `supported_by` keeps the check
silent at *every* severity, not just CRITICAL — the severity choice (HIGH vs CRITICAL) is
orthogonal to whether this specific gate test passes. This directly resolves one of D-28-03's open
plan-gate carries: severity HIGH does not weaken the falsifiability guarantee.

**Fixture slug collision check:** confirmed `examples/known-bad/chart-takeaway-without-magnitude-*`
exists (a different, viz-domain fixture: a chart takeaway that doesn't name a magnitude — unrelated
check family, unrelated defect). The proposed slug `magnitude-without-computed-effect` is
textually and semantically distinct; no collision.

**Entrypoint/code-check surface:** `GATE_PROFILES["execute"]` includes `"code"`
(`dsx/cli.py:120`) and `"verify"`/`"ship"` also include `"code"` (`:123,128`) — the promoted
fixture's entrypoint will be scanned by `dsx/checks/code.py` at three of the four gate points. Since
the D-28-01 fixture has no `model:` block and no leakage-relevant code idiom, this scan should clear
trivially (no fit/cleaning/scaler idiom to misjudge), but the plan must still author a real,
syntactically-plausible entrypoint file — an empty or trivially-static script is fine (never
executed, only read as text, per the same idiom `27-RESEARCH.md §A` documents).

### 5. D-05 gate mechanics — placement risk (load-bearing for the plan)

`scripts/gen-finding-catalogue.py:336-423`, verified:

- `_resolve_docstrings` (`:336-375`) maps **each individual `report.add(code, ...)` call site** to
  its nearest enclosing `FunctionDef`'s docstring (`:356-374`) — not to the module, not to the
  check family. Two different codes emitted by the SAME function share that function's ONE
  docstring.
- `check_d05` (`:393-423`) only gates codes in `_D05_ALLOWLIST_PREFIXES` or named exactly in
  `_D05_ALLOWLIST_CODES` (`:403-407`) — confirmed **zero pre-existing `DSX-CLM-*` code** is in
  either allowlist (grepped the full 211-line block; only `DSX-SPEC-*`, `DSX-CODE-*`, `DSX-ML-*`,
  `DSX-COH-040`, `DSX-EXP-070`, `DSX-MET-021`, `DSX-STA-*`, `DSX-VIZ-071` appear). **`DSX-CLM-034`
  would be the FIRST-ever cited code in the `DSX-CLM` family.**
- **Risk if `DSX-CLM-034`'s `report.add` call is placed inside the EXISTING `_check_numeric_overlap`
  function** (`claims.py:343-401`, which already emits `DSX-CLM-033`): `_resolve_docstrings` would
  bind `DSX-CLM-034` to `_check_numeric_overlap`'s docstring, which today is a bare one-liner
  (`"""Claim numbers must overlap results.tests effects/CIs when tests exist."""`, `:346`) with no
  `Citation:`/`Structural criterion:` line. The D-05 gate would fail for `DSX-CLM-034` (not for
  `DSX-CLM-033` — 033 is not allowlisted, so it is unaffected) unless the plan amends that
  function's docstring. **The precedent this project has used four separate times (`DSX-VIZ-071`,
  `DSX-ML-034`, `DSX-COH-040`, `DSX-EXP-070`/`DSX-MET-021`) is always to write a brand-new function**
  so the citation obligation attaches only to the new code, never retrofitting a legacy/uncited
  sibling's shared function. **Recommendation for the plan: write `DSX-CLM-034`'s check as a new
  function (e.g. `_check_supported_by_traceability`), NOT as a branch inside
  `_check_numeric_overlap`.** This is a discretionary implementation choice (S4-2's to make), but
  it is the only choice consistent with every prior mint in this codebase and avoids inventing a
  docstring-sharing edge case with no precedent.
- `_TEST_MARKER_RE = re.compile(r"#\s*D-05:\s*(DSX-[A-Z]+-\d{3})")` (`:217`) — the test-marker regex
  requires exactly three digits after the family; `DSX-CLM-034` matches (`\d{3}` = `034`).
  Confirmed no formatting risk.
- `_CITATION_RE`/`_REFVALUE_RE` (`:213-216`) require a line matching `^\s*Citation:\s*\S` and
  `^\s*(?:Reference value|Structural criterion):\s*\S` — the plan must use exactly one of
  `Reference value:` or `Structural criterion:`; per D-28-05's honesty framing (a structural
  criterion, not a recomputed reference value), `Structural criterion:` is the correct choice,
  mirroring `_check_feature_provenance`'s own docstring shape from Phase 27
  (`27-RESEARCH.md §D`, confirmed pattern).

### 6. `node install.mjs --check` obligation + byte-freeze invariant

`install.mjs:38-47` (`CAPABILITY_PAYLOAD`), confirmed: the installer syncs `dsx/`, `references/`,
`templates/`, and `examples/` into the overlay; it does **not** sync `tests/` or `scripts/`. Since
a live-miss mint touches `dsx/checks/claims.py` (source), `references/finding-codes.md`
(regenerated), `templates/ANALYSIS-SPEC.yaml` (new commented-optional keys), and
`examples/known-bad/*` (new fixture files), **all four synced directories change** — `node
install.mjs` (or `--force`) then `node install.mjs --check` is required at phase end, exactly as
Phase 27 required. If the measured verdict is CAUGHT, none of `dsx/`/`references/`/`templates/`
change (only `examples/` gains nothing new, since a no-mint close does not promote the fixture
either — see `## Recommended Plan Decomposition`), so the installer obligation may be a no-op in
that branch; the plan should still run `--check` to confirm.

**`dsx/checks/dq.py` byte-freeze:** no direct byte-diff test was found in `tests/test_known_bad_
corpus.py`; the invariant is enforced structurally by `tests/test_gate_path_hermetic.py:134-141`
(asserts `dsx/checks/dq.py` is among the resolved gate-module roots and its import closure excludes
the profiler, `:155-169`) plus the project convention of a plan-time `git diff --stat -- dsx/checks/
dq.py` verification step (the mechanism Phase 27's plan used, `27-01-PLAN.md` `<verify>` block).
**Confirmed: nothing in this phase's design touches `dq.py` at all** — the mint lives entirely in
`claims.py`, `templates/ANALYSIS-SPEC.yaml`, `scripts/gen-finding-catalogue.py`, and the harness/
examples tree. The plan should still carry the `git diff --stat -- dsx/checks/dq.py` empty-output
verification step as a belt-and-braces check, mirroring Phase 27.

---

## REQ-by-REQ Implementation Notes

**REQ-P28-01** (measure live before any check is designed): satisfied by a plan task that (a)
authors the frozen D-28-01 fixture text (spec + minimal entrypoint, not yet promoted into
`examples/`), (b) runs `_gate_findings`-equivalent logic at all four points from a fresh tempdir
(mirroring `tests/test_known_bad_corpus.py:996-1052`), (c) records the verbatim table plus the
swap-still-fires counterfactual, (d) writes `28-MEASUREMENT.md` with an explicit VERDICT line. The
existing-checks-clear table in `28-CONTEXT.md` (D-28-02) is now locator-verified — see §4 above and
the confirmed line numbers there — so the measurement task can cite exact locators when recording
which checks cleared and why.

**REQ-P28-02** (conditional mint): satisfied only if the measurement is a LIVE MISS. The check
belongs in `dsx/checks/claims.py` as a **new function** (§5 above), dispatched from the existing
per-claim loop (`claims.py:76-88`), reading `claim.get("supported_by")` (silent if absent) and
`claim.get("rounding", 2)`, resolving the union of numbers from ONLY the named test(s) (not
`_check_numeric_overlap`'s all-tests union), comparing with a sig-figs comparator plus the ×100
scale bridge. `supported_by`/`rounding` slot into `templates/ANALYSIS-SPEC.yaml:299-308` as two more
commented-optional keys; no `dsx/spec.py` change needed (§2). D-05 citation is Wilkinson & TFSI
(1999) as motivating principle only, `DSX-REP-061`'s mould as the mechanism precedent (§1),
docstring must use `Structural criterion:` not `Reference value:` and must state the bounded-catch
honesty (catches via the stray number, not metric-identity — D-28-05). D-06 number is `DSX-CLM-034`
(confirmed free, §4 table). If the measurement is CAUGHT, this requirement's own text is satisfied
by recording which code caught it (predicted: `DSX-CLM-033`) and minting nothing.

**REQ-P28-03** (harness complete + brief rewritten): the four harness maps and three count pins
in §4's table, all locator-verified, are the exhaustive edit list for a LIVE MISS outcome. For a
CAUGHT outcome, the harness edit surface shrinks to: no new fixture promotion, no catalogue/count
pin moves — only the brief.md §6.5 item 8 row rewrite recording the measured CAUGHT verdict and the
catching code.

---

## Recommended Plan Decomposition

**Structural difference from Phase 27, stated plainly:** Phase 27 measured its live miss in a
pre-plan spike (S3-1, before any `27-01-PLAN.md` existed), so its two plans (mint the check, then
promote the fixture + wire the harness) were written unconditionally against an already-known
verdict. Phase 28's own roadmap (`28-CONTEXT.md` §5) places the D-13 measurement at **S4-3
(execute)** — after this research and the S4-2 plan are authored. **The plan(s) produced from this
research must therefore encode the measurement as their own first task, with every later task
explicitly conditional on that task's recorded verdict.** This is the single highest-risk authoring
point for S4-2; an ambiguously-worded conditional would read as "mint by default," which would
violate guardrail 2 (NOTHING MINTED PRE-MEASUREMENT) the moment an executor runs the plan
mechanically without checking the branch.

**Recommended: two plans, mirroring Phase 27's wave split, with the measurement embedded as Plan
28-01's Task 1 and every subsequent task explicitly gated on its recorded verdict.**

### Plan 28-01 (Wave 1, standalone, TDD, requirements: REQ-P28-01, REQ-P28-02)

- **Task 1 — MEASURE (the D-13 act, not a RED/GREEN test task):** author the frozen fixture text
  (spec + minimal static entrypoint, not yet committed under `examples/known-bad/` — keep it under
  the phase directory or a throwaway path until the verdict is known, mirroring Phase 27's
  `spike/` convention). Run the four-point protocol from a fresh tempdir, mirroring
  `tests/test_known_bad_corpus.py::_gate_findings` exactly (never against the repo root). Apply the
  swap-still-fires counterfactual. Write `28-MEASUREMENT.md` with the verbatim table and an explicit
  `VERDICT: LIVE MISS` or `VERDICT: CAUGHT` line, first, before any other content. **This task's
  `<done>` block must state in plain language: "If VERDICT is CAUGHT, stop here — do not perform any
  task below; instead perform the closure task (Task 4/branch B). If VERDICT is LIVE MISS, proceed
  to Task 2."**
- **Task 2 (CONDITIONAL — LIVE MISS only) — RED:** failing unit test for the new check
  (`_check_supported_by_traceability` or the plan's chosen name) in a new
  `tests/test_claims_supported_by.py` (no existing file claims this name — confirmed via directory
  listing), carrying the `# D-05: DSX-CLM-034` marker and the Wilkinson-as-principle honesty phrase
  in a comment, mirroring `27-01-PLAN.md` Task 1's shape exactly.
- **Task 3 (CONDITIONAL — LIVE MISS only) — GREEN:** implement the check in `dsx/checks/claims.py`
  as a brand-new function (§5), dispatch it from the per-claim loop, add `supported_by`/`rounding`
  to `templates/ANALYSIS-SPEC.yaml:299-308`, write the D-05 docstring (`Structural criterion:` line,
  bounded-catch honesty, Wilkinson-as-principle-not-mechanism), allowlist `DSX-CLM-034` in
  `_D05_ALLOWLIST_CODES` with an inline comment following the four existing precedent blocks, and
  regenerate the catalogue (`--write`, 277→278).
- **Task 4 — CLOSURE (branches on Task 1's verdict):**
  - *If CAUGHT:* write the no-mint record (which code caught it, verified against the swap
    counterfactual) and rewrite `brief.md` §6.5 item 8 row stating the measured CAUGHT verdict.
    REQ-P28-01/02/03 are all satisfied by this branch; **Plan 28-02 below is not executed.**
  - *If LIVE MISS:* this task is a short verification-only step (confirm Tasks 2/3 landed cleanly,
    full suite green) and the phase proceeds to Plan 28-02.

### Plan 28-02 (Wave 2, depends_on: [28-01], executed ONLY if Plan 28-01 measured LIVE MISS;
requirements: REQ-P28-01, REQ-P28-03)

- Promote the measured fixture into `examples/known-bad/` under the corpus slug
  `magnitude-without-computed-effect`; author the POSTMORTEM (reproducing the four-point table
  verbatim) and the ATTRIBUTION sidecar (`absent_code: DSX-CLM-034`,
  `promotes_backlog_item: "6.5-item-8-magnitude-without-computed-effect"` — the exact string
  confirmed at `tests/test_known_bad_corpus.py:853`, `kind: miss`, `protocol_adherence: skipped`).
- Wire all four harness maps + the three count pins from §4's table (spec count 43→44 already
  reflects Plan 28-01's mint; this plan's own edit is the `_EXPECTED_CAUGHT_DEFECTS`/
  `_EXPECTED_VAL_CODES`/`_GOLDEN_SHIP_FINDINGS` entries plus the spec-count bump, all **measured
  live on the promoted fixture, never guessed** — mirroring Phase 27's explicit "if the measured
  sets differ, stop, do not silently overwrite" instruction).
- Rewrite `brief.md` §6.5 item 8 row with the measured LIVE MISS evidence and `DSX-CLM-034`.
- `node install.mjs` then `node install.mjs --check`.

**Plan-checker instruction (carry into the plan's own front matter or a note to the plan-checker):
verify Task 1's conditional language in Plan 28-01 is unambiguous** — this is the WR-01-class risk
Phase 27's own code review caught for a different ambiguity (`27-01-PLAN.md` objective references
"WR-01 fixed" per the commit log `746ec57`). An executor reading Task 4 must not be able to run
Tasks 2/3's mint work if Task 1 recorded CAUGHT.

Each `PLAN.md` must carry the `<threat_model>` block (security capability active per
`.planning/config.json` `security_enforcement: true`, ASVS L1, `block_on: high`) — see
`## Security Domain` below for the applicable threat classes, closely mirroring Phase 27's own
`<threat_model>` register (docstring-honesty repudiation risk, catalogue-count-pin tampering,
D-05-allowlist exact-code tampering, dq.py byte-freeze).

**Single-writer reminder for the plan:** `REQUIREMENTS.md`/`STATE.md`/`ROADMAP.md` are
orchestrator-only; neither Plan 28-01 nor 28-02 may schedule a subagent task that edits them.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python `unittest` (stdlib), CPython 3.12.10 real interpreter, confirmed present at `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe` |
| Config file | none — discovery via `python -m unittest` |
| Quick run | `python312 -m unittest tests.test_known_bad_corpus tests.test_claims_supported_by -q` (name of the new test module is the plan's choice; substitute accordingly) |
| Full suite | `python312 -m unittest discover -s tests -q` + `python312 scripts/gen-finding-catalogue.py --check` + `node install.mjs --check` |

> Run from a clean tree — a stray `DECISIONS.jsonl` at the repo root false-fails two explain tests
> (project hazard note, confirmed relevant since `_gate_findings`'s fresh-tempdir discipline is the
> mitigation already built into the harness — a plan-time measurement spike must reuse that same
> discipline, never writing a trail file into the repo root).

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|--------------------|--------------|
| REQ-P28-01 | Four-point measurement recorded, verbatim, from a fresh tempdir; swap-still-fires counterfactual applied | measurement (not a unit test — a recorded artifact) | ad hoc script mirroring `_gate_findings`, output captured in `28-MEASUREMENT.md` | ❌ Wave 1 Task 1 (new artifact, no existing test asserts it — this is the D-13 act itself) |
| REQ-P28-02 | `DSX-CLM-034` fires HIGH (or the plan's finalised severity) when `supported_by` is declared and the cited test's numbers do not cover the claim's literal within `rounding` sig-figs; silent when `supported_by` is absent; D-05 gate passes | unit + build | new `tests/test_claims_supported_by.py` (or plan's chosen name) with `# D-05: DSX-CLM-034`; `python312 scripts/gen-finding-catalogue.py --check` | ❌ Wave 1 Task 2 (new unit test) — CONDITIONAL on LIVE MISS |
| REQ-P28-03 | All harness maps + counts consistent; golden ship set measured; catalogue 278 | corpus + invariant | `tests.test_causal_verb_golden`, `tests.test_frame_val`, `tests.test_finding_catalogue_invariant`, `tests.test_phase20_zero_mint_close`, `tests.test_dsx`, `tests.test_known_bad_corpus` | ✅ (edits to existing maps/pins) — CONDITIONAL on LIVE MISS |

### Sampling Rate

- **Per task commit:** `python312 -m unittest tests.test_known_bad_corpus tests.test_claims_supported_by -q`
- **Per wave merge:** full `discover` + `gen-finding-catalogue.py --check`
- **Phase gate:** full suite green + `node install.mjs --check` before `/gsd-verify-work`, on both
  branches (CAUGHT and LIVE MISS produce different file sets, but both must leave the suite green).

### Wave 0 Gaps

- [ ] `28-MEASUREMENT.md` — new (REQ-P28-01), produced by Plan 28-01 Task 1, not pre-existing.
- [ ] `tests/test_claims_supported_by.py` (name discretionary) — new unit test carrying
  `# D-05: DSX-CLM-034` (REQ-P28-02), CONDITIONAL on LIVE MISS.
- [ ] `examples/known-bad/magnitude-without-computed-effect-POSTMORTEM.md` +
  `-ATTRIBUTION.yaml` — new (REQ-P28-01/03), CONDITIONAL on LIVE MISS, produced by Plan 28-02.

---

## Security Domain

`security_enforcement: true`, `security_asvs_level: 1`, `security_block_on: "high"` (confirmed in
`.planning/config.json`). This phase touches no network/auth/session surface — it is a pure
declaration-reading static check plus test/doc/catalogue wiring. Applicable ASVS categories, per
the actual change surface:

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-------------------|
| V2 Authentication | No | N/A — no auth surface touched |
| V3 Session Management | No | N/A |
| V4 Access Control | No | N/A |
| V5 Input Validation | Yes | The new check reads `claim.get("supported_by")`/`claim.get("rounding")` off a parsed YAML dict via the existing `normalize()`/`as_number()`/`get()` helpers (`dsx/spec.py`) — never a raw string eval, never a hand-rolled parser (D-01: stdlib-gate-path). Untrusted spec content is data, never code (the entrypoint is read as text, never executed, per the standing gate-path rule). |
| V6 Cryptography | No | N/A — no secrets/crypto touched |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|-----------------------|
| D-05 citation over-claiming (docstring asserts a first-hand read that never happened) | Repudiation | Docstring + `# D-05:` marker must state Wilkinson & TFSI (1999) as motivating principle only, never claim the check enforces the literal "report an effect size" rule (D-28-05); grep-verified in acceptance criteria, mirroring Phase 27's T-27-03 mitigation shape. |
| Catalogue count-pin drift (one pin moves, others don't) | Tampering | Move `references/finding-codes.md` Total, `_EXPECTED_TOTAL`, and the Phase-20 pin together (277→278); all three confirmed at the same live value (277) this session, so no pre-existing drift exists to inherit. |
| `_D05_ALLOWLIST_CODES` prefix-vs-exact-code tampering | Tampering | Add `"DSX-CLM-034"` as an exact code, never a `"DSX-CLM-"` prefix — confirmed zero pre-existing `DSX-CLM-*` codes carry a citation; a prefix add would retroactively obligate ~15 legacy CLM codes and fail the build red. |
| `dsx/checks/dq.py` byte-freeze violation | Tampering | Confirmed nothing in this design touches `dq.py`; `git diff --stat -- dsx/checks/dq.py` empty is a plan verification step. |
| Ambiguous plan-conditional executed as "mint by default" on a CAUGHT verdict | Tampering (of the design intent) / Repudiation (of D-13) | Plan 28-01's Task 1 `<done>` block must state the branch explicitly (see `## Recommended Plan Decomposition`); this is the phase's own novel risk, not present in Phase 27's precedent. |

---

## Discrepancies

Loud, per instruction — none of these re-open a frozen decision; all are line-range imprecision in
`28-CONTEXT.md`'s citations, verified against the live tree this session:

1. **`dsx/pct_base.py:56-72`** (D-28-02's table, `DSX-CLM-070` row) — the function actually named,
   `claim_supplies_base`, starts at **line 50**, not 56. Lines 56-72 mostly cover
   `relative_percent_without_base` (60-68) and `normalize_ws` (71-72), a sibling function, not the
   one the table's "clears honestly because" column describes. Not load-bearing — the described
   behavior (`base_n` declared → `claim_supplies_base` True) is correct; only the line anchor is off
   by ~6 lines.
2. **`dsx/cli.py:123,128`** (D-28-02, "`claims` registers only at verify and ship") — the literal
   `"claims"` tuple element sits at **lines 122 and 127**, not 123/128 (`GATE_PROFILES["verify"]`
   opens at `:121`, its `"claims"` entry is on the immediately-following line `:122`; `["ship"]`
   opens at `:126`, `"claims"` on `:127`). Off by one line in each case; the semantic claim (verify
   + ship only) is correct and confirmed.
3. **`claims.py:523-546,667-675`** (D-28-02, `DSX-STA-002/003, 020/021` row) — `523-546` correctly
   covers `_check_reporting_contract`'s `DSX-STA-002/003` fire sites (actually
   `dsx/checks/stats.py`, not `claims.py` — the table's file column already says `stats.py`
   elsewhere in context, this citation is consistent). `667-675`, however, only spans
   `_check_null_acceptance`'s opening guard clauses; the actual `DSX-STA-021` fire site is at
   `stats.py:710` and `DSX-STA-020`'s is at `:726` — both outside the cited range. Not load-bearing
   (the described clearing condition is correct), but a plan citing this locator for its own
   verification step should use `stats.py:667-728` instead.
4. **`_SECTION_65_ITEM_IDS` member at `tests/test_known_bad_corpus.py:853`** — confirmed **exactly
   correct**, called out here for completeness since it is the single most load-bearing locator in
   the whole design (the sidecar's `promotes_backlog_item` string) and it checks out precisely,
   with zero discrepancy.
5. **Catalogue/spec-count baseline** — CONTEXT states "live catalogue re-measured this firing... Total:
   277" and "spec count 43 → 44" — both confirmed **exactly correct** against the live tree
   (`references/finding-codes.md:16`, `tests/test_dsx.py:583`, `tests/test_finding_catalogue_
   invariant.py:40`, `tests/test_phase20_zero_mint_close.py:100`, all read this session).

No discrepancy found that contradicts or requires re-opening D-28-00 through D-28-05. All are
citation-precision notes for the plan to use corrected locators in its own `<read_first>`/`<verify>`
blocks.

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|-----------------|
| A1 | The D-28-01 fixture needs a real (if trivial) committed entrypoint file, even though it declares no `model:` block | §3, §4 | Low — confirmed via `_seed_entrypoint`'s unconditional-per-gate-point behavior (`tests/test_known_bad_corpus.py:1043`) and `DSX-REP-030/031`'s hard requirement for a resolvable `reproducibility.entrypoint`; if wrong, `repro` fires HIGH at verify/ship and the "every existing check clears honestly" REQ-P28-01 condition fails — must be measured, not assumed, at Plan 28-01 Task 1 |
| A2 | `DSX-CLM-034` should be a brand-new function in `claims.py`, not a branch inside `_check_numeric_overlap` | §5 | Medium if ignored — placing it inside the existing function would obligate a docstring rewrite of a function shared with the uncited `DSX-CLM-033`; while not technically forbidden (033 stays unaffected since it's not allowlisted), it breaks the four-times-repeated project precedent and invites confusion for a future maintainer. Plan-checker should confirm the chosen placement either way, live |
| A3 | The new positive-firing unit test file should be named `tests/test_claims_supported_by.py` | Recommended Plan Decomposition | Low — purely a naming choice; confirmed no existing file claims this name, but the plan author may prefer a different name (e.g. `test_clm_034.py`) consistent with this project's inconsistent-but-descriptive test-file naming (`test_ml_feature_provenance.py`, `test_uncertainty_vocabulary.py`) |
| A4 | Severity for `DSX-CLM-034` should be HIGH per the persona round's lean | §4 (falsifiability note) | Low — confirmed the falsifiability test's `kind: miss` assertion checks only the CRITICAL union, so HIGH vs CRITICAL is orthogonal to that specific gate passing; the actual severity choice remains S4-2's to finalise against REQ-P28-02's exact text, per `28-CONTEXT.md`'s own note that this is not yet fully settled |

**If this table is empty:** not applicable — see rows above; all are recommendations subordinate to
the frozen design, not assumptions about the design itself.

---

## Open Questions

1. **Will the measured verdict be CAUGHT or LIVE MISS?**
   - What we know: the persona round predicts LIVE MISS under the collision construction (both
     personas independently), but explicitly labels this a prediction, not a substitute for
     measurement (D-13).
   - What's unclear: nothing about the mechanism is unclear (every locator checks out); only the
     live gate's actual behavior on the specific fixture text is unmeasured.
   - Recommendation: Plan 28-01 Task 1 performs the measurement as its literal first act, before
     any mint code is written, exactly as D-13 requires.

2. **Exact fire-site wording for `_check_supported_by_traceability`'s two branches (list vs single
   string `supported_by`).**
   - What we know: D-28-01's discretion note recommends a string with list tolerated (union of
     those tests' numbers).
   - What's unclear: whether the plan should implement list-tolerance in the first mint or defer it
     (REQ-P28-02's text names a single "the `results.tests[]` entry a claim rests on" — singular).
   - Recommendation: implement the single-string case first (satisfies REQ-P28-02's literal text);
     list-tolerance can be added additively without a new code if the plan-checker flags it as
     in-scope, but is not required to satisfy the requirement as written.

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| CPython 3.12 (real interpreter) | All test/measurement commands | ✓ | 3.12.10, confirmed at `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe` | — (do not use a bare `python3`/`python312` shim; confirmed hazard per project memory) |
| Node.js | `node install.mjs [--check]` | assumed ✓ (not probed this session — no `node --version` run; project's `install.mjs` is invoked routinely in prior phases per `27-RESEARCH.md`) | unconfirmed this session | none — required; the plan should re-confirm at execute time |

**Missing dependencies with no fallback:** none identified this session.

---

## Sources

### Primary (HIGH confidence — read live this session)

- `dsx/checks/claims.py` (full file) — `DSX-CLM-*` dispatch, `_check_numeric_overlap`,
  `_extract_claim_magnitudes`, `_close_enough`, all other CLM checks
- `dsx/checks/repro.py` (full file) — `DSX-REP-060/061`, the `_check_reproduce_report` mould
- `dsx/checks/stats.py:490-728` — `DSX-STA-001..021` reporting-contract and effect-size checks
- `dsx/checks/narrative.py:55-99` — `DSX-NAR-020/040`
- `dsx/pct_base.py:40-73` — `claim_supplies_base`, `relative_percent_without_base`
- `dsx/mathx.py` (grep) — `EFFECT_SIZE_KINDS`
- `dsx/cli.py:100-149` — `GATE_PROFILES`, `GATE_THRESHOLDS`
- `dsx/spec.py:1254-1339` — `_validate_model_shape`, `_validate_claims_shape`
- `templates/ANALYSIS-SPEC.yaml:270-319` — `claims:` schema block
- `tests/test_known_bad_corpus.py:65-1781` (multiple ranges) — `_gate_findings`,
  `_SECTION_65_BACKLOG_CODES`, `_SECTION_65_ITEM_IDS`, falsifiability test
- `tests/test_frame_val.py`, `tests/test_causal_verb_golden.py`, `tests/test_dsx.py:583`,
  `tests/test_finding_catalogue_invariant.py:40`, `tests/test_phase20_zero_mint_close.py:100`
- `scripts/gen-finding-catalogue.py` (full file) — `_D05_ALLOWLIST_CODES`, `check_d05`,
  `_resolve_docstrings`, `_collect_test_markers`
- `references/finding-codes.md:1-20,163` — live totals, `DSX-ML-034` row
- `install.mjs:1-60` — `CAPABILITY_PAYLOAD`
- `tests/test_gate_path_hermetic.py:130-169` — `dq.py` structural invariants
- `.planning/phases/27-evidence-case-feature-origin-only-leak/{27-CONTEXT.md,27-RESEARCH.md,
  27-01-PLAN.md,27-02-PLAN.md,27-MEASUREMENT.md}` — the mirrored precedent phase
- `.planning/phases/28-evidence-case-magnitude-no-test-computed/28-CONTEXT.md` — the frozen design
  this research verifies against
- `.planning/REQUIREMENTS.md:93-113`, `.planning/STATE.md`, `.planning/config.json` — requirements
  text, project state, workflow toggles

### Secondary (MEDIUM confidence)

- None — this research performed no web lookups; the entire domain is this repo's own code and its
  own frozen prior-phase artifacts, all read live.

### Tertiary (LOW confidence)

- Node.js availability (Environment Availability table) — not directly probed this session,
  carried forward from the fact that `install.mjs` was invoked successfully in the immediately
  preceding Phase 27.

---

## Metadata

**Confidence breakdown:**
- Standard stack / mechanism (DSX-REP-061 mould, claims schema slot, D-05 gate mechanics): HIGH —
  every locator read live, cross-checked against the AST-extraction/docstring-resolution logic
  itself, not merely against comments describing it.
- Harness wiring: HIGH — every map/constant/count-pin locator read live; the single most
  load-bearing string (`_SECTION_65_ITEM_IDS` item 8) confirmed exact.
- Plan decomposition (measurement-embedded-in-plan structure): MEDIUM — the mechanism (a
  conditional first task) is sound and grounded in this project's own precedent for conditional
  executor instructions (Phase 27's "if the measured sets differ... stop" pattern), but this is a
  genuinely new structural shape not previously exercised in this exact form (measurement AFTER
  planning, not before) — the plan-checker should scrutinize the conditional wording specifically.
- Pitfalls / discrepancies: HIGH — every discrepancy listed was independently re-derived from the
  live file, not inferred from CONTEXT's prose.

**Research date:** 2026-09-07
**Valid until:** next mutation of `dsx/checks/claims.py`, `scripts/gen-finding-catalogue.py`, or
`tests/test_known_bad_corpus.py` — treat as valid through S4-3 execution; re-verify locators if any
other phase lands between S4-2 planning and S4-3 execution.
