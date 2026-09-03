# 23-REVIEW — Phase 23 code review

**Reviewer:** autonomous ceremony orchestrator (opus / high, brief §3 code-review routing).
**Date:** 2026-09-03. **Unit:** S3-4 (code review + fixes).
**Verdict: PASS — zero code fixes.**

**Scope:** the three Phase-23 execute commits `d2f1f1e` (23-01) · `55c9659` (23-02) ·
`e22d2c1` (23-03). Scope was isolated at the wave boundary (`git diff 281ae31 e22d2c1`,
code only) so the review does **not** re-litigate the two interactive-session commits that
sit between the S3-2 close and Wave 1 — `202a9d2` (a HUMAN-QUEUE standing note) and
`281ae31` (the missed **D-4** `dual_axis_line` citation correction to `dsx/checks/viz.py`
+ `references/chart-catalog.md`, already reviewed and signed under HQ-30/HQ-31). **The three
waves themselves touched no gate code** — verified: `git diff 281ae31 e22d2c1 -- dsx/checks/`
is empty. 17 files changed, +1344 / −5:

| File | Change | Verdict |
|---|---|---|
| `styles/dsx-538.mplstyle` | new (fivethirtyeight fork, Matplotlib License) | PASS |
| `styles/dsx-urban.mplstyle` | new (Apache-2.0 palette, **house default**) | PASS |
| `styles/dsx-econ.mplstyle` | new (reimplemented from doctrine) | PASS |
| `styles/dsx-bbc.mplstyle` | new (reimplemented from doctrine) | PASS |
| `styles/fonts/Lato-Regular.ttf` `Lato-Bold.ttf` `OFL.txt` | vendored (SIL OFL 1.1) | PASS |
| `templates/dsx_plotstyle.py` | new analyst-side helper (matplotlib-only, off gate path) | PASS |
| `templates/FIGURE-MANIFEST.yaml` | +4 (`matplotlib_version: '3.11.1'`, additive) | PASS |
| `references/chart-snippets.md` | new (route-to-code snippet catalog) | PASS |
| `skills/dsx-visualize/SKILL.md` | +1 (`@references/chart-snippets.md` wiring) | PASS |
| `tests/test_style_headers.py` `test_style_wcag_contrast.py` `test_dsx_plotstyle_api.py` `test_dsx_plotstyle_determinism.py` `test_snippet_catalog_routing.py` | new (5 repo-integrity modules) | PASS |
| `tests/test_gate_path_hermetic.py` | +21 (`matplotlib` → `FORBIDDEN`, D-P23-03) | PASS |

Every changed source hunk and every new test module was read in full. The review targets the
four risks this phase actually carries.

## Risk 1 — gate-path contamination (a render/analyst dependency reaching the hermetic `dsx/` closure)

This is the phase's defining risk: it introduces matplotlib, a large native surface
(FreeType, HarfBuzz, Qhull). **Closed by construction and structurally pinned.**

- `templates/dsx_plotstyle.py` lives in `templates/`, **outside** the `dsx/` AST closure the
  hermetic guard walks, and is imported by no `GATE_PROFILES` module. Confirmed by the guard
  itself: `test_gate_path_hermetic` re-run GREEN with `matplotlib` now in `FORBIDDEN` — no gate
  module's import closure pulls it in.
- The determinism proof `test_dsx_plotstyle_determinism.py` carries **no `report.add`**, sits
  outside every gate closure, mints no code, and writes only into a `TemporaryDirectory` — never
  into `./figures`, so it cannot trip `DSX-FIG-040` manifest coverage. Its `@skipIf` on
  matplotlib means a matplotlib-free CI skips rather than errors at import.
- `save_deterministic` **writes only, never hashes** — imports no `hashlib`, calls nothing in
  `dsx.checks.figures`. `dsx seal` (stdlib `hashlib`) stays the single hashing authority (GA-2).
  Confirmed: `grep hashlib templates/dsx_plotstyle.py` returns nothing.

## Risk 2 — false-pass in the five new Markdown/signature invariants (oracles that look like proofs but pass vacuously)

Each new invariant carries an explicit non-vacuity anchor, so it cannot pass on an empty or
absent input:

- `test_style_headers` — `assertEqual(checked, 4)` / `assertEqual(checked, 2)`: exactly the four
  style files (and both reimplemented ones) must be reached; a deleted/renamed file fails rather
  than being skipped.
- `test_style_wcag_contrast` — `assertGreaterEqual(len(cycle), 3)` per file **and**
  `assertEqual(checked, 4)`: the arithmetic is the ~15-line stdlib WCAG 2.x formula (no
  third-party dep), and a file whose palette failed to parse fails loudly.
- `test_snippet_catalog_routing` — `cited` must be non-empty (a catalog routing to nothing cannot
  pass), and the forbidden-threshold regexes are **built from the live `MAX_PIE_SLICES` /
  `MAX_CATEGORICAL_COLORS` integers imported from `dsx.checks.viz`** — never transcribed, so the
  guard tracks `viz.py` rather than a stale copy.
- `test_dsx_plotstyle_api` — asserts `source` has **no default** (`Parameter.empty`) and that
  omitting it raises `TypeError` at call binding, not merely that the parameter name exists.
- `test_dsx_plotstyle_determinism` — reuses the **canonical** `dsx.checks.figures.file_sha256`,
  not a second hand-rolled hasher, so the oracle and `dsx seal` agree by construction.

## Risk 3 — determinism-recipe correctness (the load-bearing REQ-P23-03 claim)

The recipe's two real non-determinism sources are (a) SVG element ids seeded per-process by
`uuid4` in `RendererSVG._make_id`, and (b) the per-render `datetime.today()` timestamp in
`_write_metadata`. `save_deterministic` neutralises **both**: it pins `svg.hashsalt='dsx'`
(ids become a pure function of content) and merges `metadata={'Date': None}` (present-but-`None`
suppresses the auto-stamp; the helper owns the default so a caller cannot re-stamp — Pitfall 2).
`svg.fonttype='path'` bakes glyphs as vector paths, removing the font-name dependency. The
double-render oracle re-runs `savefig` twice and asserts byte-equality under `file_sha256` —
GREEN, so a re-render is byte-identical. Font registration precedes style resolution
(`register_fonts()` at import, before any `plt.style.use` — Pitfall 1: the findfont cache clears
forward-only).

## Risk 4 — license / provenance integrity of the three vendored (load-bearing) assets

- **matplotlib `fivethirtyeight` fork (`dsx-538`)** — Matplotlib License §2/§3 permit verbatim
  vendoring of a bundled style sheet, conditioned on retaining the MDT copyright and a brief
  change summary. Both are present (header `# License:` + `# Changes:` lines). VERIFIED by the
  loop (HQ-33 item 1).
- **Urban Institute palette (`dsx-urban`, Apache-2.0)** — palette hexes + rcParams only, no guide
  prose. Carried from Scope §3.3; the one item still owed an at-locator human read (HQ-33 item 2,
  non-blocking until S5-2).
- **Lato `.ttf` (SIL OFL 1.1)** — checksums re-verified this unit: Regular
  `d636e468…5b251`, Bold `8a0aace7…d16be1`; `OFL.txt` carries the SIL OFL 1.1 text and the
  `Reserved Font Name "Lato"` line (genuine, not a repackage). VERIFIED at-locator (HQ-33 item 3).
- The two cite-only styles (`dsx-econ`, `dsx-bbc`) **vendor nothing** — reimplemented from
  published doctrine, no Economist-PDF text, no `bbplot` GPL code, no proprietary font — and so
  cannot contaminate under any license. Their headers carry the three required disclaimer phrases
  (`test_style_headers::test_reimplemented_styles_carry_the_doctrine_disclaimer` GREEN).

## Observations (recorded, not defects — no fix applied)

- **OBS-1** `save_deterministic` hard-codes `format="svg"`; a caller who *also* passes `format=`
  inside `**savefig_kwargs` gets a duplicate-keyword `TypeError`. This is intentional — it is an
  SVG-only deterministic writer — and it fails loudly, so it is a documented shape, not a latent
  bug.
- **OBS-2** the determinism oracle double-renders the *same* `Figure` object. That validly catches
  **both** non-determinism sources (the element-id salt fires on every `savefig`; the timestamp
  differs between the two calls). A second, independently-constructed figure would be an even
  stronger cross-construction proof, but REQ-P23-03 is about re-render byte-equality, which this
  proves. No change owed.
- **OBS-3** the `dsx-538` header reads "forked verbatim" then documents a WCAG-AA palette
  adjustment. The two are reconciled honestly by the explicit `# Changes:` line (which is exactly
  what Matplotlib License §3 requires) and the `# Palette:` line naming the upstream hues that
  fell below 3:1. Honest provenance, no fix.

## Zero fixes

No finding rose above an observation. Nothing on the gate path changed; the vocabulary the gate
admits is unchanged (zero mint @276, confirmed by `gen-finding-catalogue.py --check` exit 0 and
`test_finding_catalogue_invariant` set-identity 276→276). No fix commit was needed.
