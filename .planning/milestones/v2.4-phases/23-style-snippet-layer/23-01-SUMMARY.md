---
phase: 23-style-snippet-layer
plan: 01
wave: 1
status: complete
requirements:
  - REQ-P23-01
  - REQ-P23-05
completed: 2026-09-03
---

# 23-01 SUMMARY — styles/*.mplstyle set + vendored Lato + WCAG-AA palettes

Wave 1 of Phase 23 (S3-3). Executed **inline by the orchestrator** (persona-lite,
S1-3/S2-3 precedent: the plan left no irreversible design judgment — the WCAG contrast
test is the oracle; every gate is re-run by the orchestrator; STATE is single-writer, so
no subagent touches it). TDD RED→GREEN.

## What shipped

- **`styles/dsx-538.mplstyle`** — fork of matplotlib's bundled `fivethirtyeight` style
  (Matplotlib License, BSD-compatible). Structural keys retained verbatim (linewidth 4,
  butt caps, fancybox, grid, tick sizes 0, axes.linewidth 3.0, figure.subplot.*, facecolor
  `f0f0f0`); `font.family`→Lato, `svg.hashsalt: dsx` added; palette adjusted for WCAG-AA.
- **`styles/dsx-urban.mplstyle`** — **HOUSE DEFAULT**. Urban Institute palette (Apache-2.0,
  hexes + rcParams only, no guide prose); white panel; brand blue `1696d2` + magenta
  `ec008b` retained, lighter hues darkened for AA.
- **`styles/dsx-econ.mplstyle`** — reimplemented from published Economist Graphic Detail
  doctrine only (signature red `e3120b` + dark blues on an ecru `fbf7f0` panel); nothing
  vendored; no Econ-Sans/Milo font, no styleguide-PDF text.
- **`styles/dsx-bbc.mplstyle`** — reimplemented from the BBC R Cookbook's prose (blue
  `1380a1`, dark red `990000`, green `588300`); nothing vendored; no `bbplot` GPL code, no
  Reith font.
- **`styles/fonts/Lato-Regular.ttf`, `Lato-Bold.ttf`, `OFL.txt`** — one vendored OFL house
  face, from the pinned canonical Google Fonts OFL source, all four styles resolve to it.
- **`tests/test_style_headers.py`** (2 methods) — per-file header presence/shape, stdlib
  text read, CRLF-safe.
- **`tests/test_style_wcag_contrast.py`** (2 methods) — stdlib relative-luminance + contrast
  formula; series ≥3:1 vs `axes.facecolor`, text ≥4.5:1 vs `figure.facecolor`.

Every style pins `font.family: sans-serif` / `font.sans-serif: Lato, DejaVu Sans` /
`svg.fonttype: path` / `svg.hashsalt: dsx` — **determinism-ready for Plan 02**. Verified all
four load clean under matplotlib 3.11.1 with `warnings→error` (no invalid rcParam), Lato
resolves, `svg.hashsalt=dsx`.

## Vendored-font checksums (T-23-01 license-audit evidence)

Source (pinned, canonical, unmodified upstream): `https://github.com/google/fonts/raw/main/ofl/lato/`

| Asset | Size (bytes) | SHA-256 |
|-------|-------------:|---------|
| `Lato-Regular.ttf` | 656568 | `d636e4683231f931eda222d588e944d082bfd3bdba02f928bee461c0f185b251` |
| `Lato-Bold.ttf` | 656544 | `8a0aace75d33794eece4b28187bfc1df0bbd2888b5d8a56e01788c8d65d16be1` |
| `OFL.txt` | 4407 | (SIL OFL 1.1; `Copyright (c) 2010-2014 by tyPoland Lukasz Dziedzic … Reserved Font Name "Lato"`) |

`OFL.txt` at-locator sanity-confirmed: carries `SIL Open Font License, Version 1.1` and the
Lato copyright/reserved-name line — the genuine Lato distribution, not a repackage.

## Six-point license-audit checklist (REQ-P23-01 plan-review artifact)

1. **matplotlib LICENSE permits verbatim vendoring of `fivethirtyeight`** — VERIFIED
   (23-RESEARCH §2: §2/§3 grant reproduce/derive/distribute, conditioned on retaining the
   MDT copyright + a brief change summary; both are in the dsx-538 header). *Vendored, load-bearing.*
2. **Urban Institute source Apache-2.0 assumption — CORRECTED 2026-09-03 (HQ-33
   at-locator read, interactive session).** The Scope §3.3 Apache-2.0 assumption does
   NOT hold: an independent fetch of the actual repo found its own README states
   "Copyright 2016 Urban Institute. Code released under the GNU General Public License
   v3.0" — the Apache-2.0 reading came from GitHub's detector picking up unmodified
   Jekyll-theme boilerplate whose copyright line names an unrelated party ("Iron Summit
   Media Strategies, LLC"), not Urban Institute. Separately, only 2 of the 6 vendored
   hexes (`1696d2`, `ec008b`) are genuinely Urban's own published palette (confirmed
   against `urbnthemes::palette_urbn` and the style guide's own `variables.less`); 3
   more (`1b7837`, `b35806`, `762a83`) are ColorBrewer's PRGn/PuOr diverging-palette
   stops, mislabeled here as "Urban shade equivalents." **Resolution:** kept all 6
   colors (bare hex values are not independently copyrightable in most jurisdictions
   regardless of license terms) but corrected `styles/dsx-urban.mplstyle`'s header to
   state Urban's real position (GPL-3.0, moot given only facts are vendored) and to
   attribute the 3 ColorBrewer hexes correctly. *Vendored, load-bearing — corrected,
   not merely confirmed.*
3. **Lato is SIL OFL 1.1; `OFL.txt` bundled alongside the `.ttf`** — VERIFIED at-locator this
   firing (OFL.txt preamble + checksums above). *Vendored, load-bearing.*
4. **dsx-econ embeds no Economist-PDF text and no proprietary font; rcParams our own
   derivation** — CONFIRMED by construction (only rcParams authored; header states it).
5. **dsx-bbc has no `bbplot` GPL-2 line and no proprietary Reith font; behaviour re-derived
   from the cookbook's prose** — CONFIRMED by construction (only rcParams authored; header
   states it).
6. **Every `.mplstyle` carries its header block** — VERIFIED (test_style_headers green).

**Loud execution decision (within plan latitude, rigour > convenience):** Task 1's header
spec requires a `Source:` line carrying a URL for **all four** files, while Task 3's per-file
text gave dsx-econ/dsx-bbc source lines with no URL. The test is the REQ-P23-01 oracle, so
all four carry a real public-provenance URL. For econ/bbc these are **cite-only doctrine
URLs** (Economist Graphic Detail; BBC R Cookbook) — nothing is vendored from them, so per
the CONTEXT GA-1 Auditor robustness note they cannot contaminate; the load-bearing at-locator
confirmations are the three **vendored** assets (mpl fork, Urban hexes, Lato .ttf).

## Gates (orchestrator-run, final tree)

- `tests.test_style_headers` + `tests.test_style_wcag_contrast` — **4 OK** (GREEN; RED first
  confirmed for file-absence before the styles existed).
- All four styles parse clean under matplotlib 3.11.1 (`warnings→error`).
- `python scripts/gen-finding-catalogue.py --check` — **exit 0, catalogue current @276**
  (zero mint; the 9 pre-existing "declared twice" warnings unchanged).
- **Full suite (clean tree): 1499 OK, 41.6s** (1495→1499, +4 = the two new modules).

## Zero mint

No `report.add` anywhere in this plan; the WCAG check is a repo-integrity test, not a gate
code (D-P23-04). Catalogue stays **276**.

## Boundary

Wave 1 of 3. Waves 2 (`dsx_plotstyle.py` + determinism + hermeticity) and 3 (snippet catalog
+ zero-mint proof) remain — **the S3-3 checkbox stays UNCHECKED** until all three land.
