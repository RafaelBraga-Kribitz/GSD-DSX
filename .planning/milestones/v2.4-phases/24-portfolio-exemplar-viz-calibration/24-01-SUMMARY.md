# 24-01 SUMMARY — Portfolio exemplar upgraded in place (REQ-P24-01)

**Plan:** 24-01 (Wave 1) · **Requirement:** REQ-P24-01 · **Status:** DONE
**Gate:** `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml` → **exit 0** (CRITICAL=0 HIGH=0 MEDIUM=3 INFO=1); full suite **1507 OK** from a clean tree.

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
`reproducibility.reproduce_report: examples/good-REPRO-REPORT.md` (repo-root-relative — see the regression note
below; opts into DSX-REP-060/061).

## Determinism (GA-3) — proven this run

Two consecutive `python examples/analysis/charts.py` renders produced **byte-identical** SVGs — `dsx seal`
returned identical `sha256:` digests both times for all three figures, and those digests match the sealed
`spec.visuals[].svg_sha256`. Recipe: `save_deterministic` fixes `svg.hashsalt`, bakes glyphs as paths
(`svg.fonttype: path`), suppresses the render timestamp (`metadata Date: None`); dsx-urban pins the same salt.

## Gate evidence (orchestrator-run, final tree)

- `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml` → **exit 0**,
  `gate:ship: PASS (blocking at HIGH) — CRITICAL=0 HIGH=0 MEDIUM=3 LOW=0 INFO=1` (no `--phase-dir` needed).
- **Full suite 1507 OK** from a clean tree (43.5s) — same count as Phase 23 close (24-01 adds no test module);
  every good-fixture-gating test in `test_dsx.py` / `test_good_fixture_phase15.py` / `test_reproduce_report.py` green.
- `python -m unittest tests.test_gate_path_hermetic` → **2 OK** (matplotlib stays in FORBIDDEN — charts.py off the gate path).
- `python scripts/gen-finding-catalogue.py --check` → **exit 0, "finding catalogue is current"** (zero mint; the 9
  pre-existing "declared twice" warnings unchanged — Phase 24 touched no `dsx/` code).
- Committed SVG index blobs seal EXACTLY to their spec values (1ab8459 / f44091c2 / 52023ee8) via the
  `.gitattributes` `examples/figures/*.svg binary` rule — the seal survives checkout on any platform.

## Honest notes (not folded into the pass claim)

- **3 pre-existing MEDIUM `DSX-STA-011`** fire on `results.tests[0..2]` (negligible standardized effect sizes
  h=0.052 / h=0.038 / d=0.031). Confirmed pre-existing by gating the pre-24-01 spec (08a65bf) — the same three
  fire there. They live in the untouched `results` block, do not block at HIGH, and my delta added **zero** new
  findings.
- **Regression caught and fixed within this plan (honest record).** My first pass set
  `reproducibility.reproduce_report: good-REPRO-REPORT.md` (spec-dir-relative, matching `narrative.path`). But
  unlike every other path field, the repro check resolves this against the GSD **phase dir / CWD**, not
  `resolve_root` — `dsx/cli.py` passes raw `phase_dir` (None when `--phase-dir` is omitted) to `repro.check`, and
  `repro.py` locates the report as it locates the entrypoint (CWD-relative fallback). The good-fixture-gating
  tests (`test_good_fixture_phase15.py`, `test_dsx.py`) call `run_checks(..., phase_dir=None, resolve_root=examples)`
  from repo-root CWD, so `good-REPRO-REPORT.md` did not resolve → **DSX-REP-060 HIGH → 16 tests flipped RED**. Fix:
  the exemplar is always gated from repo root, so the path is written **repo-root-relative**
  (`examples/good-REPRO-REPORT.md`); it now resolves under the CLI (`--spec examples/good-…yaml`, no `--phase-dir`)
  and under the test harness alike. This restored the full suite to **1507 OK** and removed the earlier
  `--phase-dir` workaround. No `dsx/` gate code touched (the phase_dir-vs-resolve_root asymmetry is a real
  latent inconsistency, but fixing it is out of 24-01's exemplar-only scope).
- Fixed one authoring bug during Task 1: direct color args need a `#` prefix (`#5c5859`, `#222222`); the
  `.mplstyle` prop_cycle hexes are bare because the cycler parses them, but `axhline(color=…)` does not.
- **Seal-durability fix (separate commit 11e2df7):** added `.gitattributes` marking `examples/figures/*.svg binary`
  so git stores the exact sealed CRLF bytes (matplotlib's Windows output). Without it, autocrlf normalised the
  committed blob (ci blob c9717f64 ≠ spec 52023ee8); on this machine it round-trips, but a fresh/cross-platform
  checkout would fire DSX-FIG-010. Verified the index blobs now seal to the recorded spec values exactly.

## Zero-mint (D-06)

276 → 276, added={} removed={}. `gen-finding-catalogue.py --check` exit 0. The holistic set-identity assertion
is 24-03 Task 1's job on the final tree; 24-01 touched no mint surface.

## Next

S4-3 remains OPEN (this is one of three plans under the checkbox). Remaining: **24-02** (first bad-chart
fixtures + MEDIUM-stratum harness re-baseline, Wave 1) and **24-03** (verify-not-build, Wave 2, depends on both).
