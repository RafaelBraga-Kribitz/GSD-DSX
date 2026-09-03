# 24-01 SUMMARY — Portfolio exemplar upgraded in place (REQ-P24-01)

**Plan:** 24-01 (Wave 1) · **Requirement:** REQ-P24-01 · **Status:** DONE
**Gate:** `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml --phase-dir examples` → **exit 0** (CRITICAL=0 HIGH=0 MEDIUM=3 INFO=1)

## What was built

GA-1(a): the existing `examples/good-*` onboarding-activation exemplar was upgraded **in place** into the
v2.4 capstone — no net-new analytical question, the proven-green statistics reused verbatim, only the
v2.4 presentation delta added.

**Task 1 — `examples/analysis/charts.py` + 3 figures through the style layer.** Authored the generator
(previously a 1-line stub) as the repo's sole matplotlib importer, NOT a gate module. Each figure:
`plt.style.use("styles/dsx-urban.mplstyle")` → build → `dsx_plotstyle.finalise_figure(fig, title=…, source=…)`
(mandatory `source` kw) → `save_deterministic(fig, …)` (writes only, never hashes — GA-2). Rendered:
`activation_uplift.svg` (point-estimate bar, re-render), `daily_activation_trend.svg` (trend, re-render,
direct-labelled), and the NEW `activation_uplift_ci.svg` (the uncertainty figure — the uplift with its real
95% CI as error bars). CI numbers anchored to `results.tests[0]` (effect 0.024, ci [0.0101, 0.0384] → 1.0–3.8pp);
no headline number invented. `helper` imported by path (templates/ is not a package; `register_fonts` runs at
import, registering Lato before `style.use` resolves `font.family` — Pitfall 1).

**Task 2 — 3rd uncertainty visual + re-seal all three + manifest.** Added the third `visuals[]` entry
(`relationship: uncertainty`, `type: error_bars`, `uncertainty_mark: error_bars` → DSX-VIZ-071 valid member,
silent; `data_input_type: interval-range` → admits error_bars per `dsx/spec.py` CHART_CAPABILITIES, so no
DSX-VIZ-013; `shows_estimates`/`shows_uncertainty` true → no DSX-VIZ-070; units + magnitude takeaway + source).
Re-sealed ALL THREE SVGs via `dsx seal` (the two pre-existing seals were stale after re-render — Risk P2):
- `activation_uplift.svg`      → `sha256:1ab8459fc501777167a628553baa3e38a6988be05ab6fc5403f4f4320e902f4f`
- `daily_activation_trend.svg` → `sha256:f44091c2080fb22f4bc6b2f3e186007097c5592adc1ded0ab597a1cee073f11e`
- `activation_uplift_ci.svg`   → `sha256:52023ee892b8dcd28c4468b5aec4562b59f9cc097c51fe6e05ed5857ec6c7ade`

Added the uncertainty row + `matplotlib_version: "3.11.1"` to `good-FIGURE-MANIFEST.yaml` (additive; figures.py
never reads it → zero mint). Manifest carries no `svg_sha256` — `dsx seal` stays the single hashing authority.

**Task 3 — narrative + repro report.** Rewrote `good-NARRATIVE.md` into strict **What / So What / Now What**,
keeping the three `claims[]` sentences verbatim (DSX-NAR-020 requires each claim present whitespace-normalised)
and not overstating the effect (2.4pp, 95% CI 1.0–3.8pp; h≈0.05 acknowledged; the case rests on the CI clearing
the +1.0pp floor, not on significance). Authored `good-REPRO-REPORT.md` from the template: `status: reproduced`,
`activation_rate: 0.024` (== `results.tests[0].effect`, within DSX-REP-061's rel_tol). Wired
`reproducibility.reproduce_report: good-REPRO-REPORT.md` (opts into DSX-REP-060/061).

## Determinism (GA-3) — proven this run

Two consecutive `python examples/analysis/charts.py` renders produced **byte-identical** SVGs — `dsx seal`
returned identical `sha256:` digests both times for all three figures, and those digests match the sealed
`spec.visuals[].svg_sha256`. Recipe: `save_deterministic` fixes `svg.hashsalt`, bakes glyphs as paths
(`svg.fonttype: path`), suppresses the render timestamp (`metadata Date: None`); dsx-urban pins the same salt.

## Gate evidence (orchestrator-run, final tree)

- `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml --phase-dir examples` → **exit 0**,
  `gate:ship: PASS (blocking at HIGH) — CRITICAL=0 HIGH=0 MEDIUM=3 LOW=0 INFO=1`.
- `python -m unittest tests.test_gate_path_hermetic` → **2 OK** (matplotlib stays in FORBIDDEN — charts.py off the gate path).
- `python scripts/gen-finding-catalogue.py --check` → **exit 0, "finding catalogue is current"** (zero mint; the 9
  pre-existing "declared twice" warnings unchanged — Phase 24 touched no `dsx/` code).
- Changed files == exactly the 8 in `files_modified`; no gate code touched.

## Honest notes (not folded into the pass claim)

- **3 pre-existing MEDIUM `DSX-STA-011`** fire on `results.tests[0..2]` (negligible standardized effect sizes
  h=0.052 / h=0.038 / d=0.031). These live in the untouched `results` block — NOT introduced by 24-01 — and do
  not block at HIGH. My visual/narrative/repro delta added **zero** new findings.
- **Deviation (recorded, minimal, honest): the gate is invoked with `--phase-dir examples`.** `dsx/cli.py`
  wires `repro.check(spec, phase_dir)` with the raw `phase_dir` (None when the flag is omitted), while every
  other check receives `resolve_root` (the spec's parent). By design (`repro.py:313`, "locate the report exactly
  as the entrypoint is located"), the repro module resolves `entrypoint`/`reproduce_report` against the GSD
  **phase directory**, not the generic resolve-root. Once `reproduce_report` is declared, the report only resolves
  when the phase directory is named — so the capstone is gated with `--phase-dir examples`, the phase-directory-aware
  form. This is strictly MORE rigorous (the repro checks actually run and validate), keeps the report path
  spec-dir-relative and consistent with every other path field, and touches no `dsx/` code. NOT patched in 24-01
  (out of scope — exemplar-only).
- Fixed one authoring bug during Task 1: direct color args need a `#` prefix (`#5c5859`, `#222222`); the
  `.mplstyle` prop_cycle hexes are bare because the cycler parses them, but `axhline(color=…)` does not.

## Zero-mint (D-06)

276 → 276, added={} removed={}. `gen-finding-catalogue.py --check` exit 0. The holistic set-identity assertion
is 24-03 Task 1's job on the final tree; 24-01 touched no mint surface.

## Next

S4-3 remains OPEN (this is one of three plans under the checkbox). Remaining: **24-02** (first bad-chart
fixtures + MEDIUM-stratum harness re-baseline, Wave 1) and **24-03** (verify-not-build, Wave 2, depends on both).
