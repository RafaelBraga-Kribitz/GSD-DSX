# Phase 24: Portfolio exemplar and viz calibration — Research

**Researched:** 2026-09-03
**Domain:** dsx gate framework (Python stdlib checks) — viz/figures/repro enforcement surfaces, known-bad corpus calibration harness, doc/code agreement tests
**Confidence:** HIGH (every claim below is `[VERIFIED: repo]` by direct file read; no web research — all ground truth is on disk)

## Summary

Phase 24 is calibration + integration, not new machinery. All three requirements resolve against code already on disk. The single most important structural fact: **the `dsx` gate reads the SPEC `visuals:` block, never the FIGURE-MANIFEST**, for every viz/uncertainty check. The FIGURE-MANIFEST is read only by `dsx/checks/figures.py` for coverage cross-checking, and the "seal" (`svg_sha256`) that `dsx seal` produces lands in **`spec.visuals[].svg_sha256`**, not in the manifest file. The requirement wording "SEAL the FIGURE-MANIFEST" is therefore slightly misleading and is clarified below.

Second key fact for REQ-P24-02: **`viz` and `figures` check families are registered at `verify` + `ship` only** (not `plan`/`execute`), and those gates block at **HIGH**. `DSX-VIZ-001` (banned type) is HIGH → catchable. But **`DSX-VIZ-071` is MEDIUM** → it fires but does not block at any default gate threshold, so it is invisible to the corpus's CRITICAL and HIGH catch-rate strata as they exist today. This is the phase's principal design landmine and is detailed in Risks.

REQ-P24-03 is verify-not-build for the bulk (catalogue @276 confirmed live, snapshots/count-pins unmutated). One narrow, defensible gap exists in the chart-selection surface's test; whether to close it is a plan-checker judgment call, framed precisely below.

**Primary recommendation:** Upgrade `examples/good-*` in place by adding a third `visuals:` entry (uncertainty), re-sealing all figures via `dsx seal` into `spec.visuals[].svg_sha256`, wiring `reproducibility.reproduce_report`; author 3 banned-type bad-chart fixtures registered in `_HIGH_TARGET_DEFECT_CODES`, and handle the `DSX-VIZ-071` MEDIUM fixture via a new MEDIUM stratum gated with `--block-on MEDIUM` (reuses existing `severity=` machinery). Mint zero codes; catalogue stays 276→276.

## User Constraints (from CONTEXT.md — 24-CONTEXT.md)

### Locked Decisions
- **GA-1 (a):** Upgrade the existing `examples/good-*` onboarding-activation exemplar **in place**. No net-new analytical question. Reuse proven-green statistics; add only the v2.4 presentation delta: (i) figures re-rendered through `dsx-urban` + `dsx_plotstyle` (`finalise_figure`/`direct_label`/`save_deterministic`); (ii) ONE uncertainty-family figure showing the real 95% CI (1.0–3.8pp) via `DSX-VIZ-071`/`RELATIONSHIP_CHARTS['uncertainty']`; (iii) sealed FIGURE-MANIFEST; (iv) strict What/So What/Now What NARRATIVE; (v) REPRO-REPORT proving deterministic re-render.
- **GA-2:** First bad-*chart*-choice fixtures mirroring `examples/known-bad/` convention (`-ANALYSIS-SPEC.yaml` + `-POSTMORTEM.md`); extend `tests/test_known_bad_corpus.py`; re-baseline stratified catch-rate/FPR. Minimal-honest set: 1× `DSX-VIZ-071`; 1× each `gauge` + `word_cloud` under `DSX-VIZ-001`; ≥1 pre-existing banned-type control (radar/3d_pie/dual_axis_line).
- **GA-3:** REQ-P24-03 largely verify-not-build. Close a doc/code-agreement gap ONLY if a genuine one is found; no speculative new selection-surface test.
- **D-06:** Phase 24 mints ZERO new finding codes → set-identity 276→276.
- **Standing:** `dsx seal` is the single hashing authority (`save_deterministic` writes only, never hashes). Double-render hash-equality determinism test stays OFF the gate path. Off-gate-path repo-integrity tests stay stdlib-only; no matplotlib on the gate path. Windows CRLF: any new line-start/end regex uses `\r?\n`.

### Claude's Discretion
- Exact fixture wiring, the catch-rate/FPR arithmetic (self-measuring), and the choice of banned-type control — all plan-level, verified by the plan-checker.

### Deferred Ideas (OUT OF SCOPE)
- Net-new exemplar / new analytical question (GA-1 rejected (b)). v2.5 phase-split (MOOT — proceeds inside v2.4).

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P24-01 | Upgrade `examples/good-*` → sealed, styled, uncertainty-figured, What/So What/Now What + REPRO-REPORT | Q1 (exact field path), Reuse anchors (seal/repro/style wiring) |
| REQ-P24-02 | First bad-chart fixtures + `test_known_bad_corpus.py` extension + catch-rate/FPR re-baseline | Q2 (enforcement surface + harness), Fixture recipe |
| REQ-P24-03 | Verify both doc/code agreement tests green + catalogue current + snapshots unmutated | Q3 (direction analysis + the one narrow gap) |

---

## Open Questions Resolved

### Q1 — REQ-P24-01 wiring: what field makes the uncertainty figure gate-visible to `DSX-VIZ-071`?

**Answer (decisive):** Add a **new entry to the SPEC `visuals:` list** in `examples/good-ANALYSIS-SPEC.yaml` carrying **`uncertainty_mark: <valid mark>`**. The concrete field path `DSX-VIZ-071` reads is **`spec.visuals[N].uncertainty_mark`**. The FIGURE-MANIFEST is NOT read by the viz check and plays no part in `DSX-VIZ-071` visibility.

Evidence:
- The viz check iterates the **spec** visuals only: `dsx/checks/viz.py:122-123` — `visuals = items(spec, "visuals")`; per-visual dispatch at `:127-142`.
- `_check_uncertainty_vocabulary` reads exactly one field: `dsx/checks/viz.py:494` — `raw = visual.get("uncertainty_mark")`. If blank it returns silently (`:495-496`); if present-but-not-a-member of `RELATIONSHIP_CHARTS["uncertainty"]` (`:498`) it emits `DSX-VIZ-071` MEDIUM (`:500-510`). A **valid** mark (e.g. `error_bars`) passes silently — which is what the good exemplar wants (happy-path exercise).
- The ten valid marks: `dsx/checks/viz.py:39-41` — `error_bars, graded_error_bars, error_bars_2d, confidence_strips, eye, half_eye, quantile_dot_plot, confidence_band, graded_confidence_band, fitted_draws`.

**Current state of `examples/good-ANALYSIS-SPEC.yaml`:** it already has a `visuals:` block with two entries (bar `:172-195`, line `:196-214`); **neither declares `uncertainty_mark`**. So the uncertainty figure is a **third `visuals[]` entry** to be added — not an edit to the existing two.

**Required fields on the new uncertainty visual (to be gate-clean at every threshold, since the good spec must pass all gates):**
- `relationship: uncertainty` + `type: error_bars` — admissible because `error_bars ∈ RELATIONSHIP_CHARTS["uncertainty"]` (`viz.py:174-198`, `_check_relationship_match`). Any non-uncertainty type here would trip `DSX-VIZ-012` HIGH.
- `uncertainty_mark: error_bars` — the `DSX-VIZ-071` field (`viz.py:494`).
- `shows_estimates: true` + `shows_uncertainty: true` — else `DSX-VIZ-070` HIGH fires (`viz.py:461-477`).
- `data_input_type:` — **must be one whose `CHART_CAPABILITIES` admits `error_bars`**, else `DSX-VIZ-013` HIGH (`viz.py:242-257`). **Plan must verify** the chosen id admits `error_bars` (grep `dsx/spec.py::CHART_CAPABILITIES` / `references/data-input-types.md`). Omitting it fires `DSX-VIZ-014` MEDIUM, which fails a `--block-on MEDIUM` gate — so declare a valid one.
- `units:` (non-blank → avoids `DSX-VIZ-061` HIGH, `viz.py:444-452`); `takeaway:` containing a digit/`pp`/comparison token (avoids `DSX-VIZ-063` HIGH / `DSX-VIZ-064` MEDIUM, `viz.py:386-442`); `source:` (avoids `DSX-VIZ-062` LOW).
- `artifact_path:` + **`svg_sha256:` (freshly sealed)** + `chart_id:` + `generator:` — see Reuse anchors for the figures-check requirements (`DSX-FIG-010` is CRITICAL on hash mismatch).

**Also required so the manifest coverage check stays green:** add a matching row to `examples/good-FIGURE-MANIFEST.yaml` `figures:` (chart_id/path/generator) — else `DSX-FIG-040` HIGH fires ("figure under figures/ with no manifest entry", `figures.py:218-237`). The manifest carries **no** `svg_sha256`; the seal lives in the spec.

### Q2 — REQ-P24-02 enforcement surface + corpus harness

**(a) Which surface, which artifact.** The corpus harness feeds the gate a **spec** and runs `dsx gate <point> --spec <path>`:
- `tests/test_known_bad_corpus.py:850-911` — `_gate_findings` runs `cli.main(["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"])` against a fresh `TemporaryDirectory()` and returns `(exit_code, findings)`.
- So a bad-chart fixture is a full **`<slug>-ANALYSIS-SPEC.yaml`** whose `visuals[]` block declares the chart defect. The gate reads `spec.visuals[]` exactly as in Q1.

**Which check point / severity (the load-bearing fact):**
- `viz` and `figures` are registered at **`verify` + `ship` only** — NOT `plan`/`execute`: `dsx/cli.py:115-131` (`GATE_PROFILES`).
- `verify`/`ship` block at **HIGH**; `plan`/`execute` block at **CRITICAL**: `dsx/cli.py:135-140` (`GATE_THRESHOLDS`).

**Exact field/severity per target defect:**

| Target | Spec field to set on `visuals[]` | Code | Severity | Blocks at verify/ship? |
|---|---|---|---|---|
| `gauge` refusal | `type: gauge` | `DSX-VIZ-001` | HIGH (`viz.py:153`) | **Yes** |
| `word_cloud` refusal | `type: word_cloud` | `DSX-VIZ-001` | HIGH | **Yes** |
| banned-type control | `type: radar` (or `3d_pie`) | `DSX-VIZ-001` | HIGH | **Yes** |
| uncertainty-mark misuse | `uncertainty_mark: <not-a-member>` (e.g. `gradient_band`) | `DSX-VIZ-071` | **MEDIUM** (`viz.py:502`) | **No** — MEDIUM < HIGH threshold |
| (alt banned via flag) | `dual_axis: true` | `DSX-VIZ-030` | HIGH (`viz.py:302`) | Yes |

`gauge`/`word_cloud` are live `BANNED_TYPES` keys (`viz.py:93-108`); both map to `DSX-VIZ-001` — a cross-reference, no new code (D-06 satisfied). The banned-type control is any of the pre-existing five (`3d_bar/3d_pie/3d_line/radar/dual_axis_line`, `viz.py:60-92`).

**(b) How the harness computes catch-rate / FPR, what counts as a catch, stratification, where expectations are declared:**
- Three per-fixture maps declare expected catches (a fixture absent from all maps defaults to "clears cleanly = exit 0"):
  - `_TARGET_DEFECT_CODES` (`:185-261`) and `_EXPECTED_CAUGHT_DEFECTS` (`:419-482`) — **CRITICAL**, plan/execute. Combined by `_effective_target_map()` (`:514-547`).
  - `_HIGH_TARGET_DEFECT_CODES` (`:505-511`) — **HIGH**, verify/ship: `{slug: {"verify": CODE, "ship": CODE}}`.
- A "catch" = `_classify_target_defect(slug, point, exit_code, findings, map, severity)` returns no problems (`:264-329`): it requires **`exit_code == 1`** AND every expected code present among findings at the given `severity` tier. Note the exit-code coupling — critical for the MEDIUM landmine (Risks P1).
- **PRESENT partition** (`test_stratified_catch_rate_and_fpr_report:1671-1690`): every `(slug, point)` cell in `_effective_target_map()`; caught iff `_classify_target_defect` clean.
- **HIGH stratum** (`:1759-1804`): iterates `_HIGH_TARGET_DEFECT_CODES` over `("verify","ship")`, re-derives catch LIVE via `_classify_target_defect(..., severity="HIGH")`; reports `high_catch_rate` **beside** the headline, asserted only to be within `[0,1]` (`:1802-1804`) — **no pinned baseline value**, so it self-rebaselines when fixtures are added.
- **ABSENT/miss partition** (`:1692-1714`): attribution sidecars with `kind: miss` whose `absent_code` fires nowhere **CRITICAL** across all four points (`:1707-1712` filters `severity=="CRITICAL"`). Floored at `_ABSENT_PARTITION_FLOOR = 3` (`:750`, `:1719-1729`).
- **FPR** (`:1656-1669`): rate of `examples/good-corpus/` specs (≥10, `:1658-1662`) that block at ship on a real (non-tempdir-noise) CRITICAL/HIGH finding. New known-bad fixtures do not touch this denominator.
- **Headline** = `(miss_rate over ABSENT, FPR)` (`_headline:771-784`); provably invariant to adding a caught PRESENT/HIGH case (`:1746-1753`, `:1806-1816`).

**Required test-extension points for each new fixture (hard requirements from live tests):**
1. `_EXPECTED_CAUGHT_DEFECTS`: add `slug → frozenset()` for **every** new fixture — equality test `test_expected_caught_defects_keys_match_the_corpus_on_disk` (`:1199-1211`) requires a key for every spec on disk.
2. `_HIGH_TARGET_DEFECT_CODES`: add `{"verify":"DSX-VIZ-001","ship":"DSX-VIZ-001"}` for gauge/word_cloud/banned-control. `test_high_stratum_target_codes_fire_and_are_named` (`:1818-1863`) then requires that code to (i) fire HIGH live at both points and (ii) be named in the fixture's POSTMORTEM, and to be disjoint from `_INCIDENTAL_GAP_CODES`.
3. `<slug>-POSTMORTEM.md` per fixture naming a `DSX-` code (`test_every_spec_has_a_sibling_postmortem_and_vice_versa:913`, `test_every_postmortem_names_a_catch_attribution_finding_code:982`).
4. Each fixture must pass `dsx validate` (`test_every_spec_passes_dsx_validate:972`) and must **exit 0 at plan+execute** (`test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points:993`) — i.e. no CRITICAL finding at plan/execute → base each fixture on a clean `examples/good-corpus/` spec + inject exactly one bad visual.
5. Every extra CRITICAL/HIGH finding at ship must be its own target code or in `_INCIDENTAL_GAP_CODES` (`test_ship_gate_findings_are_all_documented_incidental_corpus_gaps:1136-1177`) → keep `DSX-VIZ-001` the **only** HIGH finding per fixture (see Fixture recipe).

### Q3 — REQ-P24-03: do the two doc/code tests assert both directions, or only doc⊆code?

**`tests/test_doc_code_agreement.py`** (binds `references/test-selection.md` ↔ `dsx.checks.stats`):
- Tier 1 decision table — the **primary** cell is EQUALITY (both directions for that scalar): `:312-313` — `self.assertEqual(rec["test"], primary, ...)`. In-cell **alternatives are doc⊆code only**: `:314-317` — `for a in alts: self.assertIn(a, engine_alts, ...)`.
- Tier 2 six mirror tables — **doc⊆code only**: e.g. `:335-336` — `self.assertTrue(got <= engine, ...)` (identical `<=` shape at `:347-349`, `:359-361`, `:372-374`, `:384-386`, `:396-398`).
- Anti-false-pass net is **doc-side** exhaustiveness only: `test_skiplist_exhaustive:404-423` proves every DOC row is bound or skip-listed; it does not assert every engine acceptable-set member appears in the doc.
- **Verdict:** primary-cell equality + otherwise **doc⊆code**. There is no `code⊆doc` assertion for the set-valued tables. This one-directionality is **deliberate and documented** (module docstring `:20-23`: "honest SET-MEMBERSHIP … equality would be a false model" for legitimately set-valued rows). **Not a defect — do not "fix" it.**

**`tests/test_selection_heuristic_docs.py`** (nominally the `references/chart-selection.md` surface):
- This is a **prose/route-and-cite integrity** test, not a live doc↔code set-equality test. Its relationship-vocabulary check uses a **hardcoded tuple** `_RELATIONSHIPS` (`:32-44`), not the live dict: `test_skill_enumerates_eleven_relationships:64-70` — `missing = [r for r in _RELATIONSHIPS if r not in skill]`. It never imports `RELATIONSHIP_CHARTS` from `dsx/checks/viz.py`. So the chart-selection surface's relationship vocabulary is bound to a **constant mirror**, one-directional (constant⊆doc), not to code in either direction.
- The remaining assertions are citation-presence / forbidden-token / no-parallel-file / catalog-pointer guards (`:72-128`) — not doc↔code equality.

**The one genuine, narrow, permitted gap (plan-checker judgment):** `test_selection_heuristic_docs.py` does not bind the chart-selection relationship vocabulary to the **live** `RELATIONSHIP_CHARTS`; drift is caught only **transitively** by a *different* test — `tests/test_viz_vocabulary_invariant.py:231` pins `len(RELATIONSHIP_CHARTS) == 11` and `:223-227` pins the exact uncertainty set. If the plan-checker deems that transitive coverage sufficient, **REQ-P24-03 is pure verification**. If it wants the gap closed, the minimal, non-speculative close is: in `test_selection_heuristic_docs.py`, import `RELATIONSHIP_CHARTS` from `dsx.checks.viz` and assert `set(RELATIONSHIP_CHARTS)` equals the relationship names enumerated in `SKILL.md`/`chart-selection.md` **both directions** — a one-assertion tightening of the existing file, not a new surface (honours GA-3 "close exactly that gap and no more").

**Recommendation:** Treat REQ-P24-03 as verification of: (1) both tests green on the final tree; (2) `scripts/gen-finding-catalogue.py --check` exit 0 @276; (3) snapshot/count-pin tests unmutated (incl. `test_viz_vocabulary_invariant` len==11 / uncertainty-set pins, and `test_chart_catalog_invariant` BANNED_TYPES equality). Close the chart-selection live-dict binding **only if** the plan-checker calls it a real gap; otherwise do not touch either test. `test_doc_code_agreement`'s one-directionality must NOT be changed (documented-by-design).

---

## Ground-truth confirmations for the planner

- **Catalogue = 276 codes, confirmed live** `[VERIFIED: repo]`: `references/finding-codes.md` states `**Total: 276 codes.**`; a CRLF-safe unique `DSX-[A-Z]+-\d+` count over the same file also yields **276**. Zero-mint target 276→276 is current.
- **95% CI on the activation uplift = 1.0 to 3.8pp, confirmed** `[VERIFIED: repo]`: `examples/good-NARRATIVE.md:7` ("95% CI 1.0 to 3.8pp"); `examples/good-ANALYSIS-SPEC.yaml:287` (claim text); backed by `results.tests[0].ci: [0.0101, 0.0384]` (`:264`) and `effect: 0.024` (`:239`,`:260`). The uncertainty figure and REPRO-REPORT lead number are both anchored to these.
- **Branch is `gsd/v2.4.0-visual-excellence`** (correct, with the `.0`).

## Reuse anchors

| Need | Anchor | Notes |
|---|---|---|
| Exemplar spec (proven-green) | `examples/good-ANALYSIS-SPEC.yaml` | `visuals:` `:172-214` (2 entries); add 3rd. `results.tests` `:258-282`. `reproducibility:` `:216-228` (add `reproduce_report:`). `narrative:` `:230-233`. |
| Exemplar narrative | `examples/good-NARRATIVE.md` | Currently Answer/Limits/Method (`:5-21`) — rewrite to strict **What / So What / Now What**. |
| Manifest | `examples/good-FIGURE-MANIFEST.yaml` | 2 rows `:3-9`; add uncertainty row + `matplotlib_version` (per template). Recognised name in `figures.py:17-21` `MANIFEST_NAMES`. |
| Figures on disk | `examples/figures/activation_uplift.svg`, `daily_activation_trend.svg` | Re-render both + add uncertainty SVG; then re-seal all three. |
| Chart generators | `examples/analysis/charts.py` | Currently a 1-line stub (empty) — must be authored to render all 3 figures via the style layer. |
| Style layer | `templates/dsx_plotstyle.py` | `finalise_figure(fig, *, title, source, subtitle=None, note=None)` `:72-95` (source is **mandatory kw**); `direct_label(ax, *, ...)` `:98-140`; `save_deterministic(fig, path, *, metadata=None, **kw)` `:143-162` — **writes only, never hashes**. `register_fonts()` runs at import (`:69`). |
| House style | `styles/dsx-urban.mplstyle` | `axes.prop_cycle` `:8`; `svg.fonttype: path` `:30`; `svg.hashsalt: dsx` `:31`; Lato via `font.sans-serif` `:28`. Use `plt.style.use` on this. |
| Seal (single hashing authority) | `dsx/cli.py::cmd_seal:887-898` → `dsx/checks/figures.py::file_sha256:24-32` | `dsx seal <file>` prints `sha256:<hex>`; paste into `spec.visuals[N].svg_sha256`. `--json` emits `{path, svg_sha256}`. |
| Figures enforcement | `dsx/checks/figures.py` | `DSX-FIG-010` **CRITICAL** hash-mismatch `:120-129`; `DSX-FIG-011` HIGH (strict) artifact w/o seal `:105-114`; `DSX-FIG-001` HIGH missing artifact `:94-102`; `DSX-FIG-040` HIGH manifest coverage `:218-237`; `DSX-FIG-041` MEDIUM orphan `:244-252`. `strict=True` only at verify/ship. |
| Repro enforcement | `dsx/checks/repro.py` | Strict-only `_check_reproduce_report:285-388`: opt in via `reproducibility.reproduce_report: <path>`; `DSX-REP-060` HIGH if report missing `:322-335`; `DSX-REP-061` HIGH if lead number disagrees `:371-386`. Overlap is on `results.tests[0]` metric+effect (`:355-360`), `rel_tol=1e-2` (`:369`). |
| REPRO-REPORT template | `templates/REPRO-REPORT.md` | First ```yaml block is the only parsed part (`:22-29`); flat `key: value`; `status: reproduced` + `activation_rate: 0.024` already matches `results.tests[0].effect` (0.024). CRLF-safe parser (`repro.py:340` uses `\r?\n`). |
| Gate wiring | `dsx/cli.py` | `GATE_PROFILES:115-131` (viz/figures at verify+ship; repro at execute+verify+ship); `GATE_THRESHOLDS:135-140`; `--block-on` flag exists `:974`, consumed `:300`. |
| Corpus harness | `tests/test_known_bad_corpus.py` | `_gate_findings:850-911`; `_classify_target_defect:264-329` (severity-parametrised); maps `:185`,`:419`,`:505`; stratified test `:1627-1816`; HIGH-fire test `:1818-1863`. |

**Seal + repro wiring recipe (REQ-P24-01):**
1. Author `examples/analysis/charts.py` to build each figure, `plt.style.use("styles/dsx-urban.mplstyle")`, `finalise_figure(fig, title=<takeaway>, source=<provenance>)`, then `save_deterministic(fig, "examples/figures/<name>.svg")`.
2. For each of the 3 SVGs: `dsx seal examples/figures/<name>.svg` → paste `sha256:…` into the matching `spec.visuals[N].svg_sha256`. (Clarification: the requirement's "SEAL the FIGURE-MANIFEST" = seal each SVG and record the hash in the **spec** `visuals[].svg_sha256`; the manifest file itself carries no hash — verified by `DSX-FIG-010/011` against the spec field.)
3. Add `reproducibility.reproduce_report: good-REPRO-REPORT.md`; author `good-REPRO-REPORT.md` from the template with `status: reproduced` and `activation_rate: 0.024`.
4. Re-render is byte-deterministic (GA-3 recipe already inside `save_deterministic`), so re-running the generator reproduces the sealed bytes — that is the deterministic-re-render proof. Keep the double-render hash-equality assertion in `tests/` (skipIf matplotlib absent), off the gate path (`test_gate_path_hermetic.FORBIDDEN` now includes matplotlib).

## Fixture recipe (REQ-P24-02 — concrete per-fixture spec fields)

**Base:** copy a clean `examples/good-corpus/*-ANALYSIS-SPEC.yaml` (guarantees exit 0 at plan/execute and `dsx validate` pass), rename to `examples/known-bad/<slug>-ANALYSIS-SPEC.yaml`, then set exactly ONE `visuals[]` entry to the defect. Keep the visual otherwise complete so `DSX-VIZ-001` is the **only** HIGH finding: declare `units:`, a magnitude `takeaway:`, `source:`; **omit `artifact_path`/`svg_sha256`** (no file exists in the fresh tempdir → avoids `DSX-FIG-001` HIGH; figures.py `:90-91` skips when artifact blank); **omit `relationship:`** for banned-type fixtures (accept `DSX-VIZ-010` MEDIUM rather than trip `DSX-VIZ-012` HIGH from a type∉admissible mismatch). Then add the required map/POSTMORTEM entries.

| Fixture (suggested slug) | Defect field on the single bad `visuals[]` entry | Fires | Map entry |
|---|---|---|---|
| `chart-gauge-single-kpi` | `type: gauge` (no `relationship`, `artifact_path`) | `DSX-VIZ-001` HIGH | `_HIGH_TARGET_DEFECT_CODES["chart-gauge-single-kpi"] = {"verify":"DSX-VIZ-001","ship":"DSX-VIZ-001"}` |
| `chart-word-cloud-text` | `type: word_cloud` | `DSX-VIZ-001` HIGH | same shape, `DSX-VIZ-001` |
| `chart-radar-multimetric` (control) | `type: radar` (or `3d_pie`) | `DSX-VIZ-001` HIGH | same shape, `DSX-VIZ-001` |
| `chart-uncertainty-mark-misuse` | `relationship: uncertainty`, `type: error_bars`, `uncertainty_mark: gradient_band` (not a member), `shows_estimates: true`, `shows_uncertainty: true`, valid `data_input_type` admitting `error_bars`, `units`, `takeaway`, `source` | `DSX-VIZ-071` **MEDIUM** | see Risks P1 — needs MEDIUM handling, NOT `_HIGH_TARGET_DEFECT_CODES` |

For **all four**: add `slug → frozenset()` to `_EXPECTED_CAUGHT_DEFECTS`; author `<slug>-POSTMORTEM.md` naming the target `DSX-` code (and, for the 3 HIGH fixtures, containing the literal `DSX-VIZ-001`). Do **not** add any of these to `_INCIDENTAL_GAP_CODES`.

**Optional structural predicate** (REQ-P24-02 "extend `test_known_bad_corpus.py`"): mirror `test_corpus_includes_full_coverage_classes` (`:940`) with a `test_corpus_includes_a_chart_defect_class` asserting a chart-defect slug is present (glob-discovered, never a hardcoded list).

## Risks / pitfalls for the plan

**P1 — `DSX-VIZ-071` is MEDIUM; the corpus has no MEDIUM stratum (highest-risk item).** `viz.py:502` emits it at MEDIUM. `viz` runs only at verify/ship, which block at HIGH (`cli.py:135-140`), so a fixture whose only finding is `DSX-VIZ-071` **exits 0** at every default gate point. It therefore cannot register as a catch in the CRITICAL stratum (viz not in plan/execute) or the HIGH stratum (`test_high_stratum_target_codes_fire_and_are_named:1849-1856` requires the code to fire as a **HIGH** blocking finding — it won't). And `_classify_target_defect` (`:318`) requires `exit_code == 1`, which a non-blocking MEDIUM does not produce.
- **Recommended fix (honest, minimal, Phase-20-precedented):** add a **MEDIUM stratum** — a `_MEDIUM_TARGET_DEFECT_CODES = {"chart-uncertainty-mark-misuse": {"verify":"DSX-VIZ-071","ship":"DSX-VIZ-071"}}` map plus a readout in `test_stratified_catch_rate_and_fpr_report` that gates with **`--block-on MEDIUM`** so the fired MEDIUM causes `exit 1`, then classifies via the existing `_classify_target_defect(..., severity="MEDIUM")` (the `severity=` parameter already exists `:271`, `:285-290`). Requires threading a `block_on` argument into `_gate_findings` (`:850-911`) — the CLI already accepts `--block-on` (`cli.py:974`). Report the MEDIUM catch rate **beside** the headline, never folded in (mirror the HIGH stratum's D-06 invariance).
- **Do NOT** register `DSX-VIZ-071` as a `kind: miss` ABSENT case: it is not a structural miss (it fires; the ABSENT partition checks CRITICAL-tier absence, `:1707-1712`), and mislabeling it a miss would be exactly the dishonesty the corpus discipline forbids.
- **Do NOT** change `DSX-VIZ-071` to HIGH to force a catch — that is a behavior change / re-baseline of an existing code and risks D-06 posture; not sanctioned by the requirements.

**P2 — Re-render invalidates existing seals (CRITICAL failure if missed).** The two current `svg_sha256` values (`spec.visuals[].svg_sha256` `:180`,`:203`) hash the hand-made SVGs. Re-rendering through matplotlib changes the bytes; unless every figure is re-sealed, `DSX-FIG-010` fires **CRITICAL** at verify/ship. Re-seal all three (2 upgraded + 1 new) in the same change.

**P3 — `data_input_type` × `error_bars` admissibility.** The good exemplar must pass at every severity threshold; a `data_input_type` whose `CHART_CAPABILITIES` does not admit `error_bars` fires `DSX-VIZ-013` HIGH (`viz.py:242-257`). Plan must verify the chosen id (check `dsx/spec.py::CHART_CAPABILITIES` / `references/data-input-types.md`) before authoring.

**P4 — Bad-chart fixtures must be clean at plan+execute.** `test_every_spec_blocks_only_on_its_target_defect_at_critical_threshold_points` (`:993`) requires exit 0 there (viz not registered). Base each fixture on a clean good-corpus spec; do not reuse a statistically-defective known-bad spec.

**P5 — Extra HIGH findings must stay documented.** Any second HIGH finding at ship (e.g. `DSX-VIZ-012` if you leave `relationship` on a banned type, or `DSX-FIG-001` if you set `artifact_path`) trips `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` (`:1136`). Keep `DSX-VIZ-001` the only HIGH per fixture per the recipe, or add each extra to `_INCIDENTAL_GAP_CODES` with an inline reason.

**P6 — `_EXPECTED_CAUGHT_DEFECTS` equality is total.** Every new spec on disk must get a key (even `frozenset()`) or `test_expected_caught_defects_keys_match_the_corpus_on_disk` (`:1199`) goes red. Easy to forget for the MEDIUM fixture.

**P7 — CRLF + stdlib-only discipline.** Any new regex in tests/POSTMORTEMs must use `\r?\n` (repo is CRLF). New off-gate-path tests stay stdlib-only; never import matplotlib on the gate path (`test_gate_path_hermetic.FORBIDDEN`).

**P8 — Snapshot/count pins for REQ-P24-03.** Before asserting "verify-only," re-run `test_viz_vocabulary_invariant` (`len==11`, uncertainty set, `BANNED_TYPES==7`) and `test_chart_catalog_invariant` (BANNED_TYPES equality) — adding fixtures must not perturb these, and they are the real guards that catch RELATIONSHIP_CHARTS/BANNED_TYPES drift transitively.

**P9 — Commit branch trap.** Committing via `gsd-tools query commit` on this repo has a known trap that creates a stray `gsd/v2.4-visual-excellence` (missing `.0`). Current branch is correctly `gsd/v2.4.0-visual-excellence`; verify `git branch --show-current` after any tooling-driven commit and reconcile if it drifts.

## Assumptions Log

| # | Claim | Section | Risk if wrong |
|---|-------|---------|---------------|
| A1 | A `data_input_type` exists whose `CHART_CAPABILITIES` admits `error_bars` | Q1/P3 | If none, the uncertainty visual needs a different valid mark/type pairing; plan must grep to confirm before authoring |
| A2 | `type: gauge`/`word_cloud` pass `dsx validate` (free-string type at schema level) | Fixture recipe | If schema enums chart type, fixtures fail `test_every_spec_passes_dsx_validate`; verify with a one-off `dsx validate` on a draft |

*(Both are cheap to verify at plan time; neither is a compliance/security assumption.)*

## Sources

### Primary (HIGH confidence — direct repo reads)
- `dsx/checks/viz.py`, `dsx/checks/figures.py`, `dsx/checks/repro.py`, `dsx/cli.py`
- `tests/test_known_bad_corpus.py`, `tests/test_doc_code_agreement.py`, `tests/test_selection_heuristic_docs.py`, `tests/test_viz_vocabulary_invariant.py`, `tests/test_chart_catalog_invariant.py`
- `examples/good-ANALYSIS-SPEC.yaml`, `examples/good-FIGURE-MANIFEST.yaml`, `examples/good-NARRATIVE.md`, `examples/analysis/charts.py`
- `templates/dsx_plotstyle.py`, `templates/REPRO-REPORT.md`, `templates/FIGURE-MANIFEST.yaml`, `styles/dsx-urban.mplstyle`
- `references/finding-codes.md` (count = 276, verified live)
- `.planning/phases/24-portfolio-exemplar-viz-calibration/24-CONTEXT.md`

## Metadata

**Confidence breakdown:**
- REQ-P24-01 wiring (Q1): HIGH — exact field path and gate mechanics read directly.
- REQ-P24-02 surface + harness (Q2): HIGH — enforcement point, severities, and all map/test-extension points read directly; MEDIUM-stratum handling is a design recommendation (the mechanism exists; the exact wiring is a plan decision).
- REQ-P24-03 direction (Q3): HIGH on the facts (quoted assertions); the "gap or not" call is a bounded plan-checker judgment, framed both ways.

**Research date:** 2026-09-03
**Valid until:** stable until `dsx/checks/*` or the corpus harness change (repo-internal; no external dependencies).
