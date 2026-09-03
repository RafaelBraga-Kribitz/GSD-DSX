# Phase 23: Style and snippet layer — Research

**Researched:** 2026-09-03
**Domain:** matplotlib style-sheet tooling, font/license vendoring, SVG determinism, WCAG contrast, finding-code catalogue mechanics
**Confidence:** HIGH

## Summary

Phase 23 is **non-analytical**: it ships no metric, model, experiment, or statistical
claim, so the dsx analytical-research contract (decision rule / power arithmetic /
identification strategy) is **Not Applicable** here. What this research verifies instead
is tooling provenance — the exact bytes, licenses, and mechanics the plan will pin.

Everything load-bearing was read directly off the installed toolchain rather than
recalled from training data: matplotlib 3.11.1's bundled `fivethirtyeight.mplstyle`
(quoted verbatim below), its `LICENSE` file (Matplotlib License, BSD-compatible,
requires only a retained copyright notice + a brief summary of changes on redistribution
— vendoring a style sheet verbatim is explicitly permitted), the `svg.hashsalt` /
`svg.fonttype` / SVG-metadata-`Date` mechanics read straight out of
`matplotlib/backends/backend_svg.py`, and `font_manager.FontManager.addfont()`'s real
signature. matplotlib 3.11.1 is also the current PyPI release (`pip index versions
matplotlib` — INSTALLED and LATEST both 3.11.1), so no version-currency gap exists. No
new PyPI packages are installed this phase — matplotlib is a pre-existing analyst-side
dependency, and the vendored Lato `.ttf` + OFL text are static assets, not packages — so
the Package Legitimacy Gate is scoped accordingly (see below).

The two mechanics CONTEXT.md asserts but does not derive — how `svg.hashsalt` affects
element ids, and how `metadata={'Date': None}` actually suppresses the timestamp — are
now **directly verified against the installed source**, not assumed: `_make_id()` salts
a SHA-256 of element content with `rcParams['svg.hashsalt']` (`None` → a fresh
`uuid.uuid4()` every process, hence non-deterministic ids); `_write_metadata()` only
auto-stamps `Date` via `datetime.today().isoformat()` when the `'Date'` key is **absent**
from the metadata dict — passing `metadata={'Date': None}` sets the key present-but-None,
which short-circuits both the auto-stamp branch and the element-emission branch, so no
`<dc:date>` is written at all. This is the precise mechanism GA-3 requires; the plan can
cite it with confidence.

**Primary recommendation:** Pin the four `.mplstyle` files and `dsx_plotstyle.py` exactly
against the verified rcParams/API surfaces below; treat the WCAG-AA contrast test and the
double-render determinism test as two independent, off-gate-path `unittest` modules
(mirroring `test_gate_path_hermetic.py`'s existing AST-only, `report.add`-free pattern);
prove zero-mint with the same set-identity mechanism `test_finding_catalogue_invariant.py`
already uses for 275→276 (this phase does the analogous 276→276).

## Architectural Responsibility Map

This project has no browser/frontend/CDN tiers — it is a Python CLI + gate-check
architecture. The relevant tiers are: **Gate path** (`dsx/`, stdlib-only, hermetic),
**Analyst-side tooling** (`templates/`, matplotlib-dependent, off the gate path),
**Repo-integrity tests** (`tests/`, off the gate path, no `report.add`), and
**Documentation/references** (`references/`, `styles/`).

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| `.mplstyle` style-sheet definitions (REQ-P23-01) | Documentation/references (`styles/`) | — | Static config loaded by name/path via `plt.style.use`; not Python code, never imported by `dsx/` |
| Vendored Lato font + OFL text | Documentation/references (`styles/fonts/`) | — | Static binary asset, license-audited, never imported by `dsx/` |
| `dsx_plotstyle.py` helper (REQ-P23-02) | Analyst-side tooling (`templates/`) | — | matplotlib-only, imported by analysts at readout time, never by a `GATE_PROFILES` module |
| SVG determinism recipe (REQ-P23-03) | Analyst-side tooling (`templates/dsx_plotstyle.py`) | Repo-integrity test | Recipe lives in the helper; its *proof* is an off-gate-path test |
| Seal *verification* (existing, unchanged) | Gate path (`dsx/checks/figures.py`) | — | Already ships; stdlib `hashlib` only; Phase 23 changes nothing here |
| Snippet catalog (REQ-P23-04) | Documentation/references | — | Markdown/code-fenced examples that import the helper and cite finding codes; not executable gate logic |
| WCAG-AA palette verification (REQ-P23-05) | Repo-integrity test | Documentation/references (palette hexes live in `styles/*.mplstyle`) | Contrast check is a build-time property test, not a `report.add` gate code (D-P23-04) |
| Hermeticity guard extension (D-P23-03) | Gate path guard (`tests/test_gate_path_hermetic.py`) | — | Structural AST-closure test; adds `"matplotlib"` to `FORBIDDEN` |

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**GA-1 — style-file set & per-file license/attribution headers (REQ-P23-01):** exactly
four files in `styles/` — `dsx-538.mplstyle` (fork, Matplotlib License), `dsx-urban.mplstyle`
(Apache-2.0 palette + vendored OFL Lato, **house default**), `dsx-econ.mplstyle` and
`dsx-bbc.mplstyle` (**reimplemented from doctrine, no port, no PDF, no proprietary font**);
one vendored OFL font (Lato) is the deterministic house face every style resolves to; each
file carries a header (source, license, "reimplemented / not affiliated" where apt).

**GA-2 — `dsx_plotstyle.py` public signatures (REQ-P23-02):** three keyword-explicit
functions — `finalise_figure(fig, *, title, source, subtitle=None, note=None) -> Figure`
(mandatory `source`, no default), `direct_label(ax, *, ...) -> list[Text]`,
`save_deterministic(fig, path, *, metadata=None, **savefig_kwargs) -> Path` (writes the
deterministic SVG; sealing stays with `dsx seal`). Exact bodies pinned at plan (S3-2).

**GA-3 — determinism recipe's exact rcParams (REQ-P23-03):** `svg.fonttype: path` +
fixed `svg.hashsalt` + `metadata={'Date': None}` + vendored OFL font registered via
`font_manager.addfont` before `font.family` resolves to it + pinned matplotlib version
recorded in `FIGURE-MANIFEST.yaml`; proven by an off-gate-path double-render
hash-equality test (`skipIf` matplotlib absent).

**D-P23-03 — hermeticity hardening (REQ-P23-03):** add `"matplotlib"` to
`test_gate_path_hermetic.FORBIDDEN` — a cheap structural guard that turns a future
"render inline on the gate path" regression red; safe because no gate module imports
matplotlib today.

**D-P23-04 — zero new codes this phase (REQ-P23-04/05, D-06):** the snippet catalog
*routes* to existing codes, the determinism test is off the gate path (no `report.add`),
and the palette gate defers behind a D-13 entry condition — so Phase 23 mints **zero**
codes, proven by a set-identity diff `276 → 276` at S3-4.

**Binding inputs (fixed upstream, not re-opened):**
- `dsx-538` = fork of matplotlib's bundled `fivethirtyeight` style → Matplotlib License
  (BSD-compatible, PSF-derived); vendorable verbatim.
- `dsx-urban` = Urban Institute data-viz guide → Apache-2.0; Lato = SIL OFL 1.1, genuinely
  vendorable — **house default**.
- `dsx-econ` = reimplemented from published Economist doctrine only; the 2017 Economist
  styleguide PDF is unlicensed — cite, never embed/copy; proprietary face never vendored.
- `dsx-bbc` = reimplemented from the BBC cookbook's prose; `bbplot` is GPL-2.0 — never
  port its code; proprietary Reith face never vendored.
- Milestone D-constraints: D-01 stdlib gate path / D-02 declarations only / D-06 additive
  codes only against live baseline (now 276). D-13 entry-condition discipline governs any
  deferred palette gate (REQ-P23-05).
- Faceting already shipped (Phase 22, REQ-P22-03) — Phase 23 does not touch it.

### Claude's Discretion

Pinned at plan (S3-2), not settled at discuss — this research supplies the verified
mechanics so the plan can pin exact values with citations:
- The exact `.mplstyle` rcParams and header wording for all four files.
- `direct_label`'s keyword set (which series, colour inheritance, offset).
- The fixed `svg.hashsalt` value (CONTEXT.md suggests e.g. `"dsx"`).
- The snippet catalog's exact chart-type list and code routing.
- The exact Lato weights vendored (minimum Regular + Bold recommended — see below).

### Deferred Ideas (OUT OF SCOPE)

- No new gate check for palettes this phase (D-13 defer — WCAG-AA verification ships as
  a repo-integrity test, not an enforcing `report.add` code).
- No change to `dsx/checks/figures.py`'s stdlib seal *verification* (DSX-FIG-010/011/020
  already exist, Phase 12).
- No proprietary font, no GPL port, no PDF embed.
- A second vendored OFL family for closer aesthetic fidelity to `dsx-econ`/`dsx-bbc` —
  explicitly deferred ("one font family = one determinism surface to prove").
- License-audit confirmation itself is owed at S3-2 plan-review, not at research or
  discuss — the six-point checklist in 23-CONTEXT.md GA-1 runs there and files a
  non-blocking HUMAN-QUEUE line, mirroring the Phase 22 security sign-offs.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P23-01 | `styles/*.mplstyle` set (dsx-538/dsx-urban/dsx-econ/dsx-bbc), per-file license headers, license audit as plan-review item | matplotlib LICENSE text quoted below (confirms verbatim-fork permission); full `fivethirtyeight.mplstyle` quoted for faithful forking; SIL OFL 1.1 text + Lato provenance verified; header-wording template provided |
| REQ-P23-02 | `templates/dsx_plotstyle.py` helper — `finalise_figure()`, `direct_label()`, `save_deterministic()` | Verified `savefig(metadata=...)` contract, `font_manager.addfont()` signature, existing `templates/FIGURE-MANIFEST.yaml` shape to extend with `matplotlib_version` |
| REQ-P23-03 | Determinism recipe + off-gate-path double-render test + `test_gate_path_hermetic` stays true | `svg.hashsalt`/`svg.fonttype`/`metadata={'Date': None}` mechanics verified against installed `backend_svg.py` source; `test_gate_path_hermetic.py` FORBIDDEN-set/closure-walk read in full, confirms matplotlib-add is safe |
| REQ-P23-04 | Per-chart-type snippet catalog routing to finding codes, no threshold restatement | Full `dsx/checks/viz.py` finding-code inventory extracted (DSX-VIZ-010…080), `references/chart-catalog.md`/`chart-selection.md` read, `skills/dsx-visualize/SKILL.md` read for cross-reference shape |
| REQ-P23-05 | WCAG-AA contrast-verified palettes with per-palette citations, palette gate D-13-deferred | WCAG 2.2 relative-luminance + contrast-ratio formula and AA thresholds verified via W3C source; confirmed no existing WCAG/contrast code in repo (net-new territory) |
</phase_requirements>

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| matplotlib | 3.11.1 (installed and current — `pip index versions matplotlib` shows INSTALLED=LATEST=3.11.1) [VERIFIED: pip registry] | Figure rendering, style sheets, SVG backend, font management | Already the project's analyst-side charting dependency (Phase 22 confirmed installed); no alternative under consideration — GA-2/GA-3 are matplotlib-API-specific |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `matplotlib.font_manager` | bundled with matplotlib 3.11.1 | Register the vendored Lato `.ttf` at runtime via `fontManager.addfont(path)` | Always, before any `font.family`-dependent draw call |
| Python stdlib `hashlib` | stdlib | `dsx seal` remains the single hashing authority (GA-2) — `save_deterministic` must NOT hash | Already used by `dsx/checks/figures.py::file_sha256` |
| Python stdlib `unittest` (`skipIf`) | stdlib | Off-gate-path determinism test; skip cleanly when matplotlib is absent | New pattern for this repo — no prior `skipIf` test exists (verified: `grep skipIf tests/` = no matches) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| matplotlib SVG `svg.fonttype: path` | `svg.fonttype: svgfont` (embed real glyphs as SVG `<font>`) | `path` is what the bundled `fivethirtyeight.mplstyle` already uses and is the only setting that removes font-name dependency entirely — GA-3 already locks this, not a live choice |
| Vendoring one OFL font (Lato) | Vendoring per-style fonts (Overpass Mono for `dsx-538`, IBM Plex for `dsx-econ`, Ubuntu-family for `dsx-bbc`) | Explicitly deferred in CONTEXT.md — "one font family = one determinism surface to prove"; not a live choice this phase |
| `save_deterministic` computing and returning the seal | `save_deterministic` calling `hashlib` itself | Rejected in CONTEXT.md (GA-2) — would create a second hasher that could diverge from `dsx seal`; not a live choice |

**Installation:**
```bash
# No new pip installs this phase — matplotlib is already a project dependency.
# The only new artifacts are static: styles/*.mplstyle and styles/fonts/Lato-*.ttf + OFL.txt.
```

**Version verification:** `pip index versions matplotlib` → `INSTALLED: 3.11.1`,
`LATEST: 3.11.1` [VERIFIED: pip registry, checked 2026-09-03]. Training-data staleness is
not a concern here — the installed version is the current release.

## Package Legitimacy Audit

**No new external packages are installed this phase.** `styles/*.mplstyle` are plain-text
config files (not Python packages); the vendored Lato `.ttf` + `OFL.txt` are static font
assets fetched from an official source (see below), not a package-manager dependency;
`templates/dsx_plotstyle.py` imports only `matplotlib` (already installed) and the Python
stdlib. The Package Legitimacy Gate protocol (`gsd-tools query package-legitimacy check`)
therefore has no `pip install` targets to audit this phase — recorded here so the planner
does not skip the section, only its subject.

| Package | Registry | Age | Downloads | Source Repo | Verdict | Disposition |
|---------|----------|-----|-----------|-------------|---------|-------------|
| matplotlib | PyPI | ~20 yrs (since 2003) | very high (top-50 PyPI package) | github.com/matplotlib/matplotlib | OK | Pre-existing dependency, not newly installed this phase |

**Packages removed due to [SLOP] verdict:** none — no new packages proposed.
**Packages flagged as suspicious [SUS]:** none.

**Non-package asset provenance (the actual load-bearing legitimacy question this phase
answers — see the License-audit checklist in 23-CONTEXT.md GA-1, owed as a plan-review
gate at S3-2, not settled here):**

| Asset | Source | License | Fetch mechanism (plan must pin) |
|-------|--------|---------|----------------------------------|
| `fivethirtyeight.mplstyle` fork basis | Bundled with the installed matplotlib 3.11.1 at `<site-packages>/matplotlib/mpl-data/stylelib/fivethirtyeight.mplstyle` | Matplotlib License (BSD-compatible) [VERIFIED: read from installed `matplotlib-3.11.1.dist-info/LICENSE`] | Copy verbatim from the local install — no network fetch needed, avoids a third-party download entirely |
| Lato `.ttf` | Official: `https://www.latofonts.com/` or `github.com/latofonts/lato-source`; also served via Google Fonts | SIL OFL 1.1 [CITED: github.com/latofonts/lato-source/blob/master/LICENSE.txt, choosealicense.com/licenses/ofl-1.1] | Plan must pin the exact download URL and checksum at S3-2 — not resolved here (D-05-style at-locator confirmation owed at the license-audit gate) |
| Urban Institute palette hexes | Urban Institute Data Visualization Style Guide (public web guide) | Apache-2.0 [ASSUMED — carried from Scope §3.3 research, 2026-08-29; at-locator re-confirmation owed at S3-2 per GA-1's checklist item 2] | Vendor only the hex values + rcParams, never guide prose |

## Verified Mechanics (read directly from installed matplotlib 3.11.1 source)

### 1. The bundled `fivethirtyeight.mplstyle` — quoted in full for a faithful fork

Read from `<site-packages>/matplotlib/mpl-data/stylelib/fivethirtyeight.mplstyle`
[VERIFIED: installed matplotlib 3.11.1 package]:

```ini
#Author: Cameron Davidson-Pilon, replicated styles from FiveThirtyEight.com
# See https://www.dataorigami.net/blogs/fivethirtyeight-mpl

lines.linewidth: 4
lines.solid_capstyle: butt

legend.fancybox: true

axes.prop_cycle: cycler('color', ['008fd5', 'fc4f30', 'e5ae38', '6d904f', '8b8b8b', '810f7c'])
axes.facecolor: f0f0f0
axes.labelsize: large
axes.axisbelow: true
axes.grid: true
axes.edgecolor: f0f0f0
axes.linewidth: 3.0
axes.titlesize: x-large

patch.edgecolor: f0f0f0
patch.linewidth: 0.5

svg.fonttype: path

grid.linestyle: -
grid.linewidth: 1.0
grid.color: cbcbcb

xtick.major.size: 0
xtick.minor.size: 0
ytick.major.size: 0
ytick.minor.size: 0

font.size: 14.0

figure.subplot.left: 0.08
figure.subplot.right: 0.95
figure.subplot.bottom: 0.07
figure.facecolor: f0f0f0
```

Notable: **`svg.fonttype: path` is already set** in the upstream file — matplotlib's own
fivethirtyeight style already uses the exact setting GA-3 requires, which is a useful
credibility anchor for the fork. `dsx-538.mplstyle` should retain this line and add the
`svg.hashsalt` + font-family override on top (the upstream file does not set
`font.family`, so overriding it to the vendored Lato does not fight an existing value).

### 2. matplotlib LICENSE — verbatim-vendoring permission

Read from `matplotlib-3.11.1.dist-info/LICENSE` [VERIFIED: installed package]. Section 2
of the "License agreement for matplotlib versions 1.3.0 and later" grants: *"a
nonexclusive, royalty-free, world-wide license to reproduce, analyze, test, perform
and/or display publicly, prepare derivative works, distribute, and otherwise use
matplotlib alone or in any derivative version, provided... MDT's License Agreement and
MDT's notice of copyright ... are retained."* Section 3 adds: *"In the event Licensee
prepares a derivative work ... Licensee hereby agrees to include ... a brief summary of
the changes made to matplotlib."* This is exactly what GA-1's license-audit checklist
item 1 needs to confirm: **verbatim vendoring of a bundled `.mplstyle` file is explicitly
permitted**, conditioned only on (a) retaining the MDT copyright notice and (b) stating a
brief summary of changes — both satisfiable inside the per-file header block GA-1 already
mandates. No separate LICENSE file needs bundling for this one asset beyond the header
attribution (contrast the Lato `.ttf`, which does need its own bundled `OFL.txt` per SIL
OFL 1.1 condition 2 — see below).

The same LICENSE file's third-party-bundled-software section also documents that
matplotlib itself bundles OFL-1.1 fonts (AMS Fonts, Last Resort, STIX) and an
Apache-2.0-licensed ColorBrewer color-scheme table (`lib/matplotlib/_cm.py`) — useful
precedent if the plan wants a second citable source for colourblind-safe categorical
palettes beyond Urban Institute (ColorBrewer is Apache-2.0, ColorBrewer's ties back to
Cynthia Brewer / Penn State, ColorBrewer palettes are already redistributed inside the
installed matplotlib under this license).

### 3. `svg.hashsalt` — verified element-id determinism mechanism

Read from `matplotlib/backends/backend_svg.py` (`RendererSVG._make_id`)
[VERIFIED: installed matplotlib 3.11.1 source]:

```python
def _make_id(self, type, content):
    salt = mpl.rcParams['svg.hashsalt']
    if salt is None:
        salt = str(uuid.uuid4())
    m = hashlib.sha256()
    m.update(salt.encode('utf8'))
    m.update(str(content).encode('utf8'))
    return f'{type}{m.hexdigest()[:10]}'
```

Confirms CONTEXT.md's claim exactly: the default `svg.hashsalt` is `None`
[VERIFIED: `matplotlib.rcParamsDefault['svg.hashsalt']` → `None`], which reseeds every
element/clip-path id from a fresh `uuid.uuid4()` **per process** — so the same figure
rendered twice in two different Python processes gets two different sets of SVG element
ids, breaking a byte-for-byte hash comparison even though the visible pixels are
identical. Setting a fixed string (e.g. `svg.hashsalt: "dsx"`) makes `_make_id` a pure
function of `(type, content)`, so ids are stable across renders **and across processes**.
matplotlib's own docstring for `_get_clippath_id` independently confirms this: *"This
allows plots that include custom clip paths to produce identical SVG output on each
render, provided that the `svg.hashsalt` config setting and the `SOURCE_DATE_EPOCH`
build-time environment variable are set to fixed values."* — the plan should be aware
`SOURCE_DATE_EPOCH` is the second half of that sentence (relevant to the Date-stripping
mechanism below, not to hashsalt itself).

### 4. `metadata={'Date': None}` — verified timestamp-suppression mechanism

Read from `matplotlib/backends/backend_svg.py` (`RendererSVG._write_metadata`)
[VERIFIED: installed matplotlib 3.11.1 source]. The relevant branch:

```python
date = metadata.get('Date', None)
if date is not None:
    ...  # format and emit <dc:date>
elif 'Date' not in metadata:
    # Do not add `Date` if the user explicitly set `Date` to `None`
    # Get source date from SOURCE_DATE_EPOCH, if set.
    date = os.getenv("SOURCE_DATE_EPOCH")
    if date:
        ...
        metadata['Date'] = date.replace(tzinfo=UTC).isoformat()
    else:
        metadata['Date'] = datetime.datetime.today().isoformat()
```

This is the precise mechanism, and it resolves an ambiguity CONTEXT.md's prose glosses
over: matplotlib does **not** unconditionally stamp a `Date` — it only does so when the
`'Date'` key is **absent** from the `metadata` dict passed to `savefig`/`print_svg`. The
default `savefig(...)` call (no `metadata` kwarg, or `metadata=None`) normalizes to an
**empty** dict internally, so `'Date' not in metadata` is `True` → falls to the
`SOURCE_DATE_EPOCH`-or-`datetime.today()` branch → **this is the guaranteed per-render
difference GA-3 closes.** Passing `metadata={'Date': None}` explicitly sets the key
present-with-value-`None`: the first `if date is not None` is `False` (skip emission) and
the `elif 'Date' not in metadata` is also `False` (key *is* present) — so **no `<dc:date>`
element is written at all**, and no auto-stamp branch ever fires. This is exactly GA-3's
`save_deterministic(..., metadata={'Date': None}, ...)` contract; the plan can cite this
mechanism verbatim.

The matplotlib docstring for `print_svg`'s `metadata` parameter independently confirms:
*"Values have been predefined for 'Creator', 'Date', 'Format', and 'Type'. They can be
removed by setting them to `None`."* — matching this exactly.

### 5. `font_manager.fontManager.addfont(path)` — verified signature and ordering

Read from the installed `matplotlib.font_manager` module [VERIFIED: installed matplotlib
3.11.1 source]:

```python
def addfont(self, path):
    """
    Cache the properties of the font at *path* to make it available to the
    `FontManager`. The type of font is inferred from the path suffix.
    """
```

`fontManager` is the module-level singleton `FontManager` instance
(`matplotlib.font_manager.fontManager`), so the call is
`matplotlib.font_manager.fontManager.addfont(<path-to-.ttf>)`. Internally it appends a
`ttfFontProperty` entry to `self.ttflist` and — critically —
**`self._findfont_cached.cache_clear()`** at the end, invalidating matplotlib's font
lookup cache. This means the *strict* ordering requirement is not "addfont must run
before any matplotlib import" but rather: **call `addfont()` before the first
`draw()`/`savefig()` that needs the font resolved**, and specifically before
`plt.style.use(...)` is applied for a style whose `font.family`/`font.sans-serif` already
names the vendored family — otherwise matplotlib logs a `findfont: Font family 'Lato' not
found` warning and silently falls back to DejaVu Sans for that render (the cache-clear
protects *subsequent* renders, not one already in flight). Recommended sequence for
`dsx_plotstyle.py` / the determinism test:

```python
from matplotlib import font_manager
import matplotlib.pyplot as plt

font_manager.fontManager.addfont("styles/fonts/Lato-Regular.ttf")  # 1. register first
plt.style.use("styles/dsx-urban.mplstyle")                          # 2. style resolves font.family to it
fig, ax = plt.subplots()                                            # 3. draw
...
```

### 6. `templates/FIGURE-MANIFEST.yaml` — existing shape to extend

Full current content [VERIFIED: read `templates/FIGURE-MANIFEST.yaml`]:

```yaml
manifest_version: 1
run_id: "<shared readout id>"
figures:
  - chart_id: <stable_id>
    path: figures/<name>.svg
    generator: analysis/charts.py
```

REQ-P23-03 requires a `matplotlib_version` field recorded alongside `svg_sha256`. Two
placements are consistent with the file's existing shape:
- **Per-figure** (inside each `figures[]` row, next to `svg_sha256` if that key is added
  here too) — correct if different figures in one manifest could legitimately be rendered
  at different pinned matplotlib versions (unlikely in one readout, but future-proof).
  Note `svg_sha256` today actually lives on `spec.visuals[]`, not on this manifest (see
  `dsx/checks/figures.py::_check_manifest` — it cross-references `chart_id` between the
  two, it does not read `svg_sha256` off the manifest file).
- **Manifest-level** (a top-level `matplotlib_version:` key alongside `manifest_version`)
  — simpler, matches the "one manifest, one render environment" reality of a single
  readout, and mirrors `manifest_version`'s own top-level placement. **Recommended.**

`dsx/checks/figures.py` reads `figures` (list) and each entry's `path`/`chart_id`/
`generator` — it does not currently read or validate any `matplotlib_version` key, so
adding one is additive and requires no change to the existing gate-path checker (D-P23-04
zero-mint holds).

## Architecture Patterns

### System Architecture Diagram

```
                     ┌─────────────────────────────┐
                     │  styles/*.mplstyle (4 files) │
                     │  + styles/fonts/Lato-*.ttf    │
                     │  (REQ-P23-01, off gate path)  │
                     └───────────────┬───────────────┘
                                     │ plt.style.use(...)
                                     ▼
   Analyst code  ──imports──▶  templates/dsx_plotstyle.py  (REQ-P23-02)
   (readout script)              │        │         │
                                  │        │         │
                    finalise_figure   direct_label   save_deterministic
                    (title/source/    (label series   (apply GA-3 recipe,
                     subtitle/note)    at line ends)    write SVG bytes,
                                  │        │            NOT hash)
                                  └────────┴────────┐
                                                     ▼
                                          figures/<name>.svg  (on disk)
                                                     │
                                       `dsx seal figures/<name>.svg`
                                       (stdlib hashlib — single hasher)
                                                     │
                                                     ▼
                              spec.visuals[].svg_sha256  (pasted by analyst)
                              FIGURE-MANIFEST.yaml (+ matplotlib_version)
                                                     │
                          ══════════ gate path (dsx/, hermetic) ══════════
                                                     ▼
                              dsx/checks/figures.py  (UNCHANGED this phase)
                              DSX-FIG-010 seal mismatch (CRITICAL)
                              DSX-FIG-011 artifact w/o seal (HIGH)
                              DSX-FIG-020 renderer:glyph w/o seal (HIGH)

   ══════════ off-gate-path repo-integrity tests (no report.add) ══════════
   tests/test_*_determinism.py        tests/test_*_wcag_contrast.py
   (skipIf matplotlib absent;         (stdlib-only; asserts styles/*.mplstyle
    double-render save_deterministic   palette hexes meet 4.5:1 / 3:1 AA)
    → svg_sha256 equal)

   tests/test_gate_path_hermetic.py   (D-P23-03: "matplotlib" added to
                                        FORBIDDEN; walks dsx/ AST closure —
                                        styles/ and templates/ are outside
                                        it by construction)

   references/<snippet-catalog>.md    (REQ-P23-04: per-chart-type examples
                                        importing dsx_plotstyle, routing to
                                        DSX-VIZ-*/DSX-FIG-* codes by name —
                                        never restating a threshold value)
```

### Recommended Project Structure

```
styles/
├── dsx-538.mplstyle          # fork of matplotlib's fivethirtyeight, Matplotlib License
├── dsx-urban.mplstyle        # Apache-2.0 palette + Lato, HOUSE DEFAULT
├── dsx-econ.mplstyle         # reimplemented from doctrine, cite-only
├── dsx-bbc.mplstyle          # reimplemented from doctrine, cite-only
└── fonts/
    ├── Lato-Regular.ttf      # vendored, SIL OFL 1.1
    ├── Lato-Bold.ttf         # vendored, SIL OFL 1.1
    └── OFL.txt               # SIL OFL 1.1 license text (required alongside the .ttf)

templates/
├── dsx_plotstyle.py          # finalise_figure / direct_label / save_deterministic
└── FIGURE-MANIFEST.yaml      # extended with a matplotlib_version: field

references/
└── snippet-catalog.md        # per-chart-type snippets, routes to DSX-VIZ-*/DSX-FIG-*
                               # (exact filename pinned at plan — see Open Questions)

tests/
├── test_dsx_plotstyle_determinism.py   # skipIf matplotlib absent; double-render hash-eq
├── test_style_wcag_contrast.py         # stdlib-only; palette hex AA check
└── test_gate_path_hermetic.py          # FORBIDDEN += "matplotlib" (D-P23-03)
```

### Pattern 1: Off-gate-path `skipIf` test module (new to this repo, modeled on `test_gate_path_hermetic.py`'s existing conventions)

**What:** A `unittest.TestCase` that imports matplotlib lazily inside the test body (or
guards the whole module with `@unittest.skipIf(matplotlib absent, ...)`), so a
matplotlib-free CI environment collects and skips cleanly rather than erroring at import
time.

**When to use:** Both REQ-P23-03's determinism test and REQ-P23-05's WCAG contrast test —
though the WCAG test reads only the plain-text `.mplstyle` files (regex/`configparser`-style
key extraction) and needs **no matplotlib import at all**, so it does not need `skipIf` —
only the determinism test, which must actually call `savefig`, needs the guard.

**Example:**
```python
# Source: pattern derived from tests/test_gate_path_hermetic.py's existing module
# docstring conventions (CRLF discipline, "no report.add", explicit Run: line) +
# stdlib unittest.skipIf documented behavior (Python docs, unittest module).
from __future__ import annotations

import unittest

try:
    import matplotlib
    _MPL_AVAILABLE = True
except ImportError:
    _MPL_AVAILABLE = False


@unittest.skipIf(not _MPL_AVAILABLE, "matplotlib not installed — analyst-side only")
class TestDeterministicSVG(unittest.TestCase):
    def test_double_render_hash_equality(self):
        from templates.dsx_plotstyle import save_deterministic
        import matplotlib.pyplot as plt

        def render(path):
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3], [1, 4, 9])
            return save_deterministic(fig, path, metadata={'Date': None})

        p1 = render("figures/_det_test_1.svg")
        p2 = render("figures/_det_test_2.svg")
        # dsx seal stays the single hashing authority (GA-2) — this test uses
        # the SAME hashlib.sha256 file_sha256() dsx/checks/figures.py already
        # exports, not a second hasher of its own.
        from dsx.checks.figures import file_sha256
        self.assertEqual(file_sha256(p1), file_sha256(p2))
```

### Pattern 2: Snippet-catalog routing, never restating a threshold

**What:** Each per-chart-type entry shows a minimal `dsx_plotstyle`-based code snippet,
then names the finding code(s) that govern its correctness — by code, not by re-deriving
the rule.

**When to use:** REQ-P23-04, every entry.

**Example:**
```markdown
<!-- Source: pattern derived from dsx/checks/viz.py's live report.add() call sites
     (DSX-VIZ-020/060/061/062) and skills/dsx-visualize/SKILL.md's existing
     "Audit." step, which already routes to `dsx check viz` rather than
     restating hard_rules inline. -->

## Bar chart (Magnitude)

\`\`\`python
from templates.dsx_plotstyle import finalise_figure, save_deterministic
fig, ax = plt.subplots()
ax.bar(categories, values)
ax.set_ylim(bottom=0)  # zero baseline — DSX-VIZ-020 (CRITICAL if violated)
finalise_figure(fig, title="<the takeaway sentence>", source="<dataset, period>")
save_deterministic(fig, "figures/revenue-by-region.svg", metadata={'Date': None})
\`\`\`

Gate-enforced: DSX-VIZ-020 (zero baseline), DSX-VIZ-060/063/064 (takeaway title),
DSX-VIZ-061 (units), DSX-VIZ-062 (source note), DSX-FIG-011 (seal present).
See `references/chart-catalog.md` for the full Magnitude-function row set.
```

### Anti-Patterns to Avoid

- **Restating a threshold inside the snippet catalog.** E.g. writing "must be ≤5 slices"
  in prose next to a pie-chart snippet instead of citing `DSX-VIZ-040` — creates a second
  source of truth that can drift from `dsx/checks/viz.py`'s actual `MAX_PIE_SLICES`
  constant. D-P23-04 forbids this explicitly.
- **Calling `addfont()` after `plt.style.use()` and after a figure has already drawn.**
  The font substitution warning is silent-by-default (`findfont` logs at `WARNING` level,
  easy to miss in a notebook), so a wrong-font render can ship without visible error.
- **Letting `save_deterministic` compute or return a sha256.** GA-2 explicitly rejected
  this — it would create a second hasher that could silently diverge from `dsx seal`.
- **Setting `metadata=None` (or omitting `metadata` entirely) and assuming that's
  equivalent to stripping the date.** Verified above: omitting `metadata['Date']` triggers
  the `datetime.today()` auto-stamp branch — the *opposite* of the desired effect. Must be
  `metadata={'Date': None}` explicitly (or a dict that includes that key set to `None`).

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| SVG element/id determinism | A custom post-processing pass that regex-strips `id=` attributes from rendered SVG | `rcParams['svg.hashsalt']` set to a fixed string | matplotlib's own `_make_id()` already produces deterministic ids for free once the rcParam is set — a regex post-processor is fragile against future SVG structure changes and duplicates logic matplotlib maintains |
| SVG metadata timestamp removal | Parsing and deleting `<dc:date>` from the written SVG file after the fact | `savefig(..., metadata={'Date': None})` | Verified above: the backend supports this natively; a post-process step is an unnecessary second pass over the file and risks corrupting other Dublin-Core metadata elements |
| WCAG contrast-ratio computation | A third-party contrast-checking library (e.g. `wcag-contrast-ratio` PyPI package) | The ~15-line stdlib formula (relative luminance + ratio, both pure arithmetic on 0–255 RGB tuples) | D-01 (stdlib gate path) applies in spirit even though this is a repo-integrity test, not a gate check; the formula is short, stable (WCAG 2.x, unchanged since 2008), and a dependency for 15 lines of arithmetic is not justified |
| Finding-code catalogue diffing | A hand-written list of "codes added this phase" checked by eye | The same `_ROW_RE`/set-identity pattern `test_finding_catalogue_invariant.py` already uses (`current_set == expected_set`, `expected_set = snapshot ∪ _MINTED_CODES`) | Proven pattern from Phase 21/22; a fresh implementation risks missing the CRLF-safe, non-line-anchored regex discipline the existing one already encodes |

**Key insight:** Every "don't hand-roll" here is really "don't re-derive what matplotlib
or the existing test infrastructure already provides deterministically" — the phase's
entire job is *wiring together* verified upstream mechanics, not inventing new ones.

## Common Pitfalls

### Pitfall 1: Windows font-fallback silently breaking determinism

**What goes wrong:** On a machine without Lato installed at the OS level, matplotlib's
`findfont()` silently substitutes a fallback (commonly DejaVu Sans on most installs), and
the render *looks* fine but is geometrically different from a render on a machine that
does have Lato — breaking the hash even with `svg.fonttype: path` set, if `addfont()`
was never called.

**Why it happens:** `svg.fonttype: path` only removes the *font-name* dependency from
the SVG output (glyphs become vector paths) — it does nothing to guarantee *which* font's
glyph outlines get baked in. That's `font_manager.addfont()`'s job, and it must run
before the font is resolved.

**How to avoid:** Always call `font_manager.fontManager.addfont(<vendored .ttf path>)`
before `plt.style.use(...)` / before any draw call in `save_deterministic`'s code path —
CONTEXT.md's GA-3 already states this ordering; this research confirms *why* via the
`_findfont_cached.cache_clear()` mechanic (Pitfall exists precisely because the cache is
only cleared going forward, not retroactively for renders already in flight).

**Warning signs:** A `findfont: Font family 'Lato' not found` log line (WARNING level,
easy to miss); the double-render determinism test failing intermittently depending on
which machine/CI runner executes it.

### Pitfall 2: Confusing `metadata=None` with `metadata={'Date': None}`

**What goes wrong:** A developer assumes "no metadata passed = no metadata written,"
calls `save_deterministic(fig, path)` with no `metadata` kwarg, and gets a fresh
`datetime.today().isoformat()` stamped into the SVG every render — the exact bug GA-3
exists to prevent.

**Why it happens:** matplotlib's `savefig`/`print_svg` treats an *absent* `'Date'` key
as "please auto-stamp," and a *present-but-None* `'Date'` key as "please omit" — an
inversion of the intuitive default. Verified directly from `_write_metadata`'s source
(see Verified Mechanics §4 above).

**How to avoid:** `save_deterministic`'s implementation must construct
`{'Date': None, **(metadata or {})}` (or equivalent) so the caller cannot accidentally
omit the key — GA-2's signature (`metadata=None, **savefig_kwargs`) leaves this the
helper's responsibility, not the analyst's.

**Warning signs:** The determinism test intermittently fails only when run at a different
wall-clock second than the previous run (a strong tell that `Date` is leaking through).

### Pitfall 3: A pre-existing family's finding codes carry no D-05 citation — do not add one under `DSX-VIZ-`/`DSX-FIG-` casually

**What goes wrong:** If the plan mistakenly decides the snippet catalog needs a *new*
finding code (e.g. "DSX-VIZ-090 for missing style-sheet header") to make routing
"cleaner," it silently violates D-P23-04's zero-mint constraint and breaks the
276→276 set-identity test.

**Why it happens:** `scripts/gen-finding-catalogue.py`'s `_D05_ALLOWLIST_PREFIXES`/
`_D05_ALLOWLIST_CODES` machinery makes minting a *new* code inside an existing family
(`DSX-VIZ-*`, `DSX-FIG-*`) look easy — but D-P23-04 is explicit that this phase mints
zero codes, full stop.

**How to avoid:** Every snippet-catalog "rule" must map to a code that **already exists**
in the current inventory (verified list below); if a chart type genuinely has no
governing code yet, the snippet documents the pattern without a code citation rather than
minting one.

**Warning signs:** `tests/test_finding_catalogue_invariant.py`'s
`test_code_set_is_phase12_snapshot_plus_the_sanctioned_mints` failing with a non-empty
`added=[...]` list; `scripts/gen-finding-catalogue.py --check` exiting 1.

**Live `DSX-VIZ-*`/`DSX-FIG-*` codes available for snippet routing** [VERIFIED: read in
full from `dsx/checks/viz.py` and `dsx/checks/figures.py`]:

| Code | Severity | What it checks |
|------|----------|-----------------|
| DSX-VIZ-010/011 | MEDIUM | Relationship declared / recognised |
| DSX-VIZ-012/013/014 | — | Relationship↔mark and data-signature↔mark admissibility |
| DSX-VIZ-020 | CRITICAL | Truncated y-axis on a length-encoded chart (bar/area) |
| DSX-VIZ-021 | LOW | Baseline not declared |
| DSX-VIZ-030 | HIGH | Dual y-axes |
| DSX-VIZ-040 | MEDIUM | Too many pie/donut/waffle/treemap slices (`MAX_PIE_SLICES`) |
| DSX-VIZ-050 | MEDIUM | Too many categorical colours (`MAX_CATEGORICAL_COLORS`) |
| DSX-VIZ-051 | HIGH | Red/green as sole distinction |
| DSX-VIZ-052 | MEDIUM | Rainbow scale on a continuous variable |
| DSX-VIZ-060/063/064 | MEDIUM/HIGH/MEDIUM | Missing/weak takeaway title |
| DSX-VIZ-061 | HIGH | Units not declared |
| DSX-VIZ-062 | LOW | No source note — **directly mirrors `finalise_figure`'s mandatory `source` kwarg** |
| DSX-VIZ-070 | HIGH | No uncertainty shown alongside an estimate |
| DSX-VIZ-071 | MEDIUM | Uncertainty mark not a recognised Wilke §5.6 member |
| DSX-VIZ-080 | LOW | Categories not ordered meaningfully |
| DSX-FIG-010 | CRITICAL | `svg_sha256` mismatch |
| DSX-FIG-011 | HIGH | `artifact_path` without `svg_sha256` |
| DSX-FIG-020 | HIGH | `renderer: glyph` without `svg_sha256` |
| DSX-FIG-030 | HIGH | Duplicate `chart_id` |
| DSX-FIG-040/041 | HIGH/MEDIUM | Manifest coverage / orphan entries |

Related `DSX-SMELL-*` codes also available (in `dsx/checks/smells.py`):
`DSX-SMELL-002/007/009/010/011/013` — declaration-based plot-construction smells the
snippet catalog can also route to where relevant.

## Code Examples

### `finalise_figure` — mandatory-source enforcement via signature (GA-2)

```python
# Source: GA-2 (23-CONTEXT.md), signature only — body pinned at plan (S3-2)
def finalise_figure(
    fig: "matplotlib.figure.Figure",
    *,
    title: str,
    source: str,           # required keyword, NO default — omitting it is a TypeError
    subtitle: str | None = None,
    note: str | None = None,
) -> "matplotlib.figure.Figure":
    ...
    return fig
```

### `save_deterministic` — the full recipe wired together (GA-3)

```python
# Source: GA-2/GA-3 (23-CONTEXT.md) + verified mechanics above — body pinned at plan
from pathlib import Path
import matplotlib.pyplot as plt

_HASHSALT = "dsx"  # exact value pinned at plan (S3-2)

def save_deterministic(
    fig: "matplotlib.figure.Figure",
    path: "str | Path",
    *,
    metadata: dict | None = None,
    **savefig_kwargs,
) -> Path:
    import matplotlib as mpl
    mpl.rcParams["svg.hashsalt"] = _HASHSALT
    mpl.rcParams["svg.fonttype"] = "path"
    merged_metadata = {"Date": None, **(metadata or {})}
    out = Path(path)
    fig.savefig(out, format="svg", metadata=merged_metadata, **savefig_kwargs)
    return out
    # NOTE: does NOT call hashlib / dsx seal — GA-2, single-hasher rule.
```

### Font registration at module import time (recommended location: `dsx_plotstyle.py` top level or a `register_fonts()` helper called once)

```python
# Source: verified font_manager.addfont API (see Verified Mechanics §5)
from pathlib import Path
from matplotlib import font_manager

_FONT_DIR = Path(__file__).resolve().parent.parent / "styles" / "fonts"

def register_fonts() -> None:
    for ttf in sorted(_FONT_DIR.glob("Lato-*.ttf")):
        font_manager.fontManager.addfont(str(ttf))
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|---------------|--------|
| Embedding font glyphs by name (`svg.fonttype: none`, the matplotlib default before 3.x styling conventions) | `svg.fonttype: path` for hermetic, font-independent SVG | Already matplotlib's own `fivethirtyeight.mplstyle` convention (predates this phase) | No behavior to migrate — this phase adopts what upstream already models |
| Non-deterministic build artifacts (random ids, wall-clock timestamps) accepted as "normal" in visualization pipelines | Reproducible-builds discipline (`SOURCE_DATE_EPOCH`, fixed salts) applied to chart rendering | matplotlib's `_get_clippath_id` docstring explicitly references the `reproducible-builds.org` `SOURCE_DATE_EPOCH` spec | This phase is matplotlib's reproducible-builds story applied to a DSX-specific gate/seal use case, not a novel technique |

**Deprecated/outdated:** None identified — matplotlib 3.11.1 is current, and the
determinism mechanisms used (`svg.hashsalt`, `svg.fonttype`, metadata stripping,
`font_manager.addfont`) are stable, long-standing matplotlib APIs, not recent additions
subject to near-term deprecation.

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Urban Institute data-viz guide is Apache-2.0-licensed and its palette hexes are freely vendorable | Package Legitimacy Audit, GA-1 (carried from CONTEXT.md, itself carried from 2026-08-29 Scope §3.3 research) | If the license has changed or was misidentified, `dsx-urban.mplstyle` (the house default) would need re-licensing or a different palette source; this is exactly why GA-1's checklist item 2 requires at-locator re-confirmation at S3-2 before shipping |
| A2 | The official Lato distribution URL/repo (`latofonts.com`, `github.com/latofonts/lato-source`) is the canonical, unmodified OFL 1.1 source | Verified Mechanics §Package Legitimacy Audit table | A modified or third-party-repackaged `.ttf` could carry a stripped or altered license notice; the plan must pin an exact URL + checksum, not just "a Lato ttf from somewhere" |
| A3 | Minimum Lato weights to vendor are Regular + Bold | Standard Stack / Claude's Discretion | If `dsx_plotstyle.py`'s title/label styling needs Italic or Light weights, additional `.ttf` files (and OFL bundling) would be needed — low risk, easy to extend later since OFL permits it |

**If this table is empty:** N/A — three assumptions recorded above, each already flagged
for at-locator confirmation at the S3-2 license-audit gate per GA-1's own checklist, so
no *additional* user confirmation is needed beyond what CONTEXT.md already scheduled.

## Open Questions

1. **Exact `svg.hashsalt` string value.**
   - What we know: CONTEXT.md suggests `"dsx"` as an example; any fixed non-`None` string
     works mechanically (verified above — `_make_id` treats it as an opaque salt string).
   - What's unclear: Whether the plan wants a more specific/versioned salt (e.g.
     `"dsx-v1"`) to allow a deliberate future re-salt if a hash-breaking bug is found.
   - Recommendation: Pin `"dsx"` at plan (S3-2) unless there's a reason to version it;
     changing the salt later is itself a determinism-breaking event that would need its
     own migration note, so simplicity favors an unversioned string now.

2. **Snippet catalog file location and name.**
   - What we know: It must "point at Phase 22's `references/chart-catalog.md`" (per
     23-CONTEXT.md) and live somewhere the `dsx-visualize` skill's `<references>` block
     can `@`-reference it (that block currently lists `chart-catalog.md`,
     `chart-selection.md`, `data-input-types.md`, `viz-smells.md`).
   - What's unclear: Whether it should be a fifth file in `references/` (matching the
     existing four) or live under `templates/` alongside `dsx_plotstyle.py` (since it
     imports the helper). `references/` is the stronger fit — it is documentation, not
     an importable module, and the existing `dsx-visualize` skill already wires
     `references/` files into its `<references>` block.
   - Recommendation: `references/chart-snippets.md` (or similar), added to
     `skills/dsx-visualize/SKILL.md`'s `<references>` block at plan time.

3. **Which chart types get a snippet entry — all 60 admissible marks, or a curated subset?**
   - What we know: REQ-P23-04 says "per-chart-type," and `references/chart-catalog.md`
     enumerates 60 `dsx_admissible` marks across 11 function categories.
   - What's unclear: Whether "per-chart-type" means per-mark (60 entries) or per-function
     (11 entries, one representative mark each) — the latter is far more tractable and
     matches the catalog's own function-axis organization.
   - Recommendation: Per-function (≥11 entries, one worked example per function category
     including Uncertainty), each optionally showing 1-2 sibling marks inline rather than
     a full 60-entry enumeration — pin the exact scope at plan (S3-2), since this
     materially affects plan sizing.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| matplotlib | `dsx_plotstyle.py`, determinism test | ✓ | 3.11.1 (current PyPI release) | `skipIf` guard on the determinism test; the helper itself has no fallback (it is matplotlib-only by design, GA-2) |
| Lato `.ttf` source (network fetch) | Vendoring the font asset (REQ-P23-01) | not yet vendored — `**/*.ttf` and `**/*.otf` globs both return zero matches in the live tree [VERIFIED] | — | None needed — this is exactly what the phase ships; not a runtime dependency once vendored |
| `pip`/PyPI registry access | Confirming matplotlib version currency | ✓ (`pip index versions matplotlib` succeeded) | — | — |

**Missing dependencies with no fallback:** none — the one "missing" item (vendored Lato)
is the phase's own deliverable, not an external blocker.

**Missing dependencies with fallback:** matplotlib absence is handled by the mandated
`skipIf` guard on the determinism test (GA-3) — a matplotlib-free CI stays green by
design, this is not a gap but a documented, deliberate skip.

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | Python stdlib `unittest` [VERIFIED: every existing test in `tests/` uses `unittest.TestCase`, e.g. `tests/test_gate_path_hermetic.py`, `tests/test_finding_catalogue_invariant.py`] |
| Config file | none — no `pytest.ini`/`unittest.cfg` found; tests run via `python -m unittest tests.<module> -v` (the convention every existing test module's docstring documents) |
| Quick run command | `python -m unittest tests.test_dsx_plotstyle_determinism -v` (or the WCAG contrast test module name pinned at plan) |
| Full suite command | `python -m unittest discover -s tests -v` (matches the "FULL SUITE 1495 OK" pattern referenced in STATE.md for prior phases) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P23-01 | Each `.mplstyle` carries a license/attribution header (source, license, vendoring rule) | unit (repo-integrity, stdlib text read) | `python -m unittest tests.test_style_headers -v` | ❌ Wave 0 |
| REQ-P23-01 | License-audit six-point checklist confirmed | manual (human read at S3-2 plan-review, filed to HUMAN-QUEUE non-blocking — NOT an automated test) | — | N/A — manual gate, not a test file |
| REQ-P23-02 | `finalise_figure`/`direct_label`/`save_deterministic` exist with the exact keyword-only signatures GA-2 pins | unit | `python -m unittest tests.test_dsx_plotstyle_api -v` | ❌ Wave 0 |
| REQ-P23-02 | `finalise_figure(fig, title=..., subtitle=..., note=...)` without `source=` raises `TypeError` | unit (mandatory-kwarg enforcement) | same module as above, one test method | ❌ Wave 0 |
| REQ-P23-03 | Double-render `save_deterministic` produces byte-identical `svg_sha256` | unit, `skipIf` matplotlib absent | `python -m unittest tests.test_dsx_plotstyle_determinism -v` | ❌ Wave 0 |
| REQ-P23-03 | `test_gate_path_hermetic` still passes with `"matplotlib"` added to `FORBIDDEN` | unit (existing test, edited) | `python -m unittest tests.test_gate_path_hermetic -v` | ✅ exists, edit only |
| REQ-P23-04 | Every snippet-catalog entry's cited code exists in `references/finding-codes.md` | unit (routing↔catalogue cross-check, mirrors `test_selection_heuristic_docs`'s doc/code agreement pattern from Phase 22) | `python -m unittest tests.test_snippet_catalog_routing -v` | ❌ Wave 0 |
| REQ-P23-04 | No snippet entry restates a numeric threshold that also appears in `dsx/checks/viz.py` (`MAX_PIE_SLICES`, `MAX_CATEGORICAL_COLORS`, etc.) | unit (regex/value-scan guard) | same module as above | ❌ Wave 0 |
| REQ-P23-05 | All four `.mplstyle` palette hexes meet WCAG AA (4.5:1 text / 3:1 graphical) against their declared background | unit, stdlib-only relative-luminance formula | `python -m unittest tests.test_style_wcag_contrast -v` | ❌ Wave 0 |
| REQ-P23-05 (D-P23-04) | Finding catalogue set-identity stays `276 → 276` (no mint) | unit (existing pattern, extended) | `python -m unittest tests.test_finding_catalogue_invariant -v` + `python scripts/gen-finding-catalogue.py --check` | ✅ exists — extend `_MINTED_CODES`/`_EXPECTED_TOTAL` only if any code is (unexpectedly) touched; expected: **no edit needed** since zero-mint |

### Sampling Rate

- **Per task commit:** the specific new test module(s) touched by that task
  (`python -m unittest tests.test_<module> -v`).
- **Per wave merge:** `python -m unittest discover -s tests -v` (full suite) +
  `python scripts/gen-finding-catalogue.py --check` (catches any accidental mint).
- **Phase gate:** Full suite green, `gen-finding-catalogue.py --check` exit 0, before
  `/gsd-verify-work`.

### Wave 0 Gaps

- [ ] `tests/test_style_headers.py` — covers REQ-P23-01 (header presence/shape)
- [ ] `tests/test_dsx_plotstyle_api.py` — covers REQ-P23-02 (signatures, mandatory `source`)
- [ ] `tests/test_dsx_plotstyle_determinism.py` — covers REQ-P23-03 (double-render hash-eq, `skipIf`)
- [ ] `tests/test_snippet_catalog_routing.py` — covers REQ-P23-04 (code-citation cross-check)
- [ ] `tests/test_style_wcag_contrast.py` — covers REQ-P23-05 (AA contrast, stdlib-only)
- [ ] Framework install: none — stdlib `unittest` is already the project convention, no new install needed
- [ ] Fixture: `styles/fonts/Lato-*.ttf` + `OFL.txt` must exist on disk before
      `test_dsx_plotstyle_determinism.py` can pass (not a test-framework gap, but a
      build-order dependency the plan must sequence: vendor font → write helper → write
      determinism test, not the reverse)

## Security Domain

`security_enforcement: true` in `.planning/config.json`, so this section is required —
but Phase 23's threat surface is narrow and mostly non-applicable, since it ships no
authentication, session, network, or user-input-handling code. Recorded honestly rather
than padded.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No auth surface — style files and a plotting helper |
| V3 Session Management | no | No session surface |
| V4 Access Control | no | No access-control surface |
| V5 Input Validation | marginal | `dsx_plotstyle.py`'s functions take in-process Python objects (a `Figure`, an `Axes`), not untrusted external input; no validation gap identified |
| V6 Cryptography | yes, narrowly | `dsx seal` (unchanged, pre-existing) uses stdlib `hashlib.sha256` — a non-cryptographic-strength use case (content-integrity seal, not a security secret), already correctly implemented pre-Phase-23; `save_deterministic` explicitly must NOT hash (GA-2), so no new crypto surface is introduced |

### Known Threat Patterns for this stack

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Supply-chain: a modified/malicious `.ttf` masquerading as the official Lato distribution | Tampering | Pin an exact download URL + checksum for the vendored `.ttf` at plan time (Assumption A2); the license-audit gate (S3-2) is the natural place to also record the checksum |
| A future contributor "just renders inline on the gate path" for convenience, silently pulling matplotlib (and its large native-code surface: FreeType, HarfBuzz, Qhull — all visible in the LICENSE bundle) into the hermetic `dsx/` closure | Elevation of Privilege (of the render path into the trust boundary) | D-P23-03: add `"matplotlib"` to `test_gate_path_hermetic.FORBIDDEN` — turns this red structurally, verified safe today (no gate module currently imports matplotlib) |
| A GPL-2.0 (`bbplot`) or unlicensed-PDF (Economist styleguide) source contaminating a vendored/shipped asset via careless "reference implementation" copying | Tampering (of license provenance) | GA-1's reimplement-from-doctrine posture + the six-point license-audit checklist, filed to HUMAN-QUEUE non-blocking at S3-2 (mirrors the Phase 22 security sign-off pattern, HQ-29/HQ-31) |

## Sources

### Primary (HIGH confidence)
- Installed matplotlib 3.11.1 source (`matplotlib/backends/backend_svg.py`,
  `matplotlib/font_manager.py`) — `svg.hashsalt`/`_make_id`, `_write_metadata`/Date
  handling, `FontManager.addfont` signature, all read and quoted directly.
- `<site-packages>/matplotlib/mpl-data/stylelib/fivethirtyeight.mplstyle` — full contents
  quoted verbatim.
- `matplotlib-3.11.1.dist-info/LICENSE` — Matplotlib License text + bundled
  third-party-license manifest (OFL fonts, ColorBrewer Apache-2.0, etc.) read in full.
- `dsx/checks/figures.py`, `dsx/checks/viz.py`, `dsx/checks/smells.py`,
  `tests/test_gate_path_hermetic.py`, `tests/test_finding_catalogue_invariant.py`,
  `scripts/gen-finding-catalogue.py`, `templates/FIGURE-MANIFEST.yaml`,
  `references/chart-catalog.md`, `references/chart-selection.md`,
  `skills/dsx-visualize/SKILL.md` — all read in full from the live tree.
- `pip index versions matplotlib` — confirms installed 3.11.1 is current PyPI release.

### Secondary (MEDIUM confidence)
- W3C, "Understanding Success Criterion 1.4.3: Contrast (Minimum)" —
  <https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html> — relative
  luminance formula and 4.5:1/3:1 AA thresholds.
- `github.com/latofonts/lato-source/blob/master/LICENSE.txt` and
  <https://choosealicense.com/licenses/ofl-1.1/> — Lato's SIL OFL 1.1 licensing.

### Tertiary (LOW confidence)
- None — the Urban Institute Apache-2.0 palette claim (Assumption A1) is carried forward
  from prior-session Scope §3.3 research, not independently re-verified this session;
  flagged in the Assumptions Log for the S3-2 at-locator re-confirmation GA-1 already
  schedules.

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — matplotlib is a pre-existing, version-current dependency; no new
  package decisions to make.
- Architecture: HIGH — every mechanic (hashsalt, metadata, addfont, gate-path hermeticity,
  finding-catalogue set-identity) was verified against live source, not recalled.
- Pitfalls: HIGH — both major pitfalls (font-fallback ordering, metadata-Date inversion)
  were derived directly from reading the matplotlib source, not inferred.
- License facts for vendored assets (matplotlib fork, Lato): HIGH (read directly).
- License fact for Urban Institute palette: MEDIUM (carried, flagged for S3-2 re-confirmation).

**Research date:** 2026-09-03
**Valid until:** 2026-10-03 (30 days — matplotlib's determinism APIs are stable and
long-standing; the one time-sensitive fact, "3.11.1 is current," should be re-checked if
planning is materially delayed past that window).
