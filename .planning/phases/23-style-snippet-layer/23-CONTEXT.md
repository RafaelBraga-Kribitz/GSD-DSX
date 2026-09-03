# Phase 23: Style and snippet layer — Context

**Milestone v2.4 Visual Excellence · S3-1 discuss · 2026-09-03 (autonomous firing).**
Phase 23 is the milestone's *tooling* layer: the license-audited `.mplstyle` set, the
analyst-side `dsx_plotstyle.py` helper, a proven SVG-determinism recipe that keeps
`FIGURE-MANIFEST.yaml` `svg_sha256` seals reproducible across re-render, and a
per-chart-type snippet catalog that routes to finding codes instead of restating
thresholds. It builds on Phase 22's catalog (the snippet catalog and heuristic point at
`references/chart-catalog.md`) and feeds Phase 24 (the exemplar's figures are produced by
this layer). Requirements: REQ-P23-01 … REQ-P23-05 (5).

Unlike Phase 22, Phase 23 carries a **light D-05 load** (brief §6): almost no
primary-source *reads* are owed. Its distinctive gate is the **license audit** — an
explicit plan-review item (REQ-P23-01), not a citation-authenticity read. This discuss
makes that audit a named checklist and settles the three design gray areas.

## Binding inputs (fixed upstream — recorded so execute/plan honour them, not re-opened)

- **Scope §3.3 license findings (from the 2026-08-29 research round)** are the binding
  provenance constraints, applied here as hard rules (their *at-locator* confirmation is
  the S3-2 license-audit gate, below):
  - `dsx-538` = fork of matplotlib's bundled `fivethirtyeight` style → **Matplotlib
    License** (BSD-compatible, PSF-derived); vendorable **verbatim**.
  - `dsx-urban` = Urban Institute data-viz guide → **Apache-2.0**; **Lato** font =
    **SIL OFL 1.1**, genuinely vendorable — **this is the house default** (the only one
    whose *real* font is legally vendorable).
  - `dsx-econ` = **reimplemented from published Economist doctrine only.** The 2017
    Economist styleguide PDF is **unlicensed** — **cite, never embed/copy**; the
    Economist's proprietary face (Econ Sans / Milo) is **never vendored**.
  - `dsx-bbc` = **reimplemented from the BBC cookbook's prose.** `bbplot` is **GPL-2.0** —
    **never port its code**; re-derive the `finalise_figure`-equivalent behaviour from the
    documented conventions; the BBC's proprietary Reith face is **never vendored**.
- **Milestone D-constraints (REQUIREMENTS.md preamble):** D-01 stdlib gate path / D-02
  declarations only / D-06 additive codes only against the re-measured live baseline (now
  **276** after Phase 22's DSX-VIZ-071). D-13 entry-condition discipline governs any
  deferred palette *gate* (REQ-P23-05).
- **Faceting is already shipped** as the orthogonal `facet_by` declaration in Phase 22
  (REQ-P22-03) — Phase 23 does not touch it.

## Phase Boundary

Ship (1) `styles/*.mplstyle` — four license-audited style files with per-file
license/attribution headers; (2) `templates/dsx_plotstyle.py` — the analyst-side,
matplotlib-only helper (`finalise_figure`, `direct_label`, `save_deterministic`), **off
the gate path**; (3) a **proven** SVG-determinism recipe (vendored OFL font via
`font_manager`, `svg.fonttype: path`, `svg.hashsalt`, metadata `Date` stripped, pinned
matplotlib version recorded in the manifest) verified by a **double-render hash-equality
test kept OFF the gate path** (`skipIf` matplotlib absent); (4) a per-chart-type snippet
catalog that imports the helper and routes to finding codes, never restating thresholds;
(5) WCAG-AA contrast-verified palettes with per-palette citations, any palette *gate*
deferred behind a D-13 entry condition.

**Out of boundary:** no new gate check for palettes this phase (D-13 defer); no change to
`dsx/checks/figures.py`'s stdlib seal *verification* (DSX-FIG-010/011/020 already exist,
Phase 12); no proprietary font, no GPL port, no PDF embed.

## Ground truth read this firing (assumptions mode)

Live tree read directly (not assumed):

- **matplotlib 3.11.1 is installed** locally (`import matplotlib` → 3.11.1). It is an
  **analyst-side** dependency, not a gate dependency — the determinism test and the helper
  import must be `skipIf` matplotlib absent so a matplotlib-free CI stays green.
- **No `styles/` directory exists** → REQ-P23-01 creates it. **No fonts are vendored**
  anywhere (`*.ttf`/`*.otf` search empty) → REQ-P23-03 vendors the OFL font.
- **`templates/` exists** (holds `ANALYSIS-SPEC.yaml`, `FIGURE-MANIFEST.yaml`,
  `REPRO-REPORT.md`, `DATA-PROFILE.yaml`, `EDA.md`, `FORBIDDEN-CLAIMS.yaml`, …) →
  `dsx_plotstyle.py` lands here (REQ-P23-02), alongside the manifest it feeds.
- **The seal *verification* is already on the gate path and hermetic.**
  `dsx/checks/figures.py` computes `svg_sha256` with **stdlib `hashlib` SHA-256 only** ("No
  Glyph/MCP dependency"), strict in verify/ship: `DSX-FIG-010` (seal mismatch, CRITICAL),
  `DSX-FIG-011` (artifact_path without seal, HIGH), `DSX-FIG-020` (renderer glyph without
  seal, HIGH). Phase 23 adds only the **render-side production** recipe that makes those
  seals reproducible; it changes nothing in `figures.py`. The canonical hasher stays
  `dsx seal` (single hashing authority) — see D-P23-02.
- **`test_gate_path_hermetic.py` (REQ-P14-06, D-01/D-03/D-07):** `FORBIDDEN = {"pandas",
  "scipy", "numpy", "csv"}`; it walks the AST import closure of only the `dsx/` gate roots
  resolved from `dsx.cli.GATE_PROFILES`. **matplotlib is not currently in `FORBIDDEN`.** The
  helper lives in `templates/`, outside `dsx/`, so it is **structurally never** in a gate
  module's closure — REQ-P23-03's "`test_gate_path_hermetic` stays true" holds by
  construction. See D-P23-03 for the cheap belt-and-suspenders strengthening.
- **Live catalogue = 276 codes** after Phase 22 (DSX-VIZ-071 minted, additive). Phase 23
  is designed to mint **zero** new codes (see D-P23-04).

## Persona round (LOOP-BRIEF §4)

**Architect** (`dsx-analysis-architect`) + **Auditor** (`gsd-security-auditor` /
`dsx-ml-integrity-auditor` lens) + **Advisor** (`gsd-advisor-researcher` lens, for the
license questions), all opus/high, run **inline** by the orchestrator against the
re-verified ground truth (S1-1/S2-1 precedent: a single artifact that must complete in one
firing without mid-unit compaction; tightly-scoped inline deliberation over blind-exploring
subagent spawns; no subagent touches a single-writer tracking file). **The Statistician is
NOT engaged** — Phase 23 is a style / tooling / licensing phase with no statistical content
(contrast Phase 22's uncertainty family). Tie-break **rigour > reliability > flexibility**.
The round converged on GA-1…GA-3 plus two cross-cutting decisions (D-P23-04 zero-mint,
D-P23-03 hermeticity hardening).

## Decisions (loud, vetoable — LOOP-BRIEF §4; veto window filed HQ-32, silence = accept)

<!-- Machine-readable decision index (format bridge for the context-coverage gate;
     decision CONTENT is in the authoritative ### bodies below). -->

- **GA-1 — style-file set & per-file license/attribution headers (REQ-P23-01):** exactly
  four files in `styles/` — `dsx-538.mplstyle` (fork, Matplotlib License), `dsx-urban.mplstyle`
  (Apache-2.0 palette + vendored OFL Lato, **house default**), `dsx-econ.mplstyle` and
  `dsx-bbc.mplstyle` (**reimplemented from doctrine, no port, no PDF, no proprietary font**);
  one vendored OFL font (Lato) is the deterministic house face every style resolves to; each
  file carries a header (source, license, "reimplemented / not affiliated" where apt).
- **GA-2 — `dsx_plotstyle.py` public signatures (REQ-P23-02):** three keyword-explicit
  functions — `finalise_figure(fig, *, title, source, subtitle=None, note=None) -> Figure`
  (mandatory `source`, no default), `direct_label(ax, *, ...) -> list[Text]`,
  `save_deterministic(fig, path, *, metadata=None, **savefig_kwargs) -> Path` (writes the
  deterministic SVG; sealing stays with `dsx seal`). Exact bodies pinned at plan (S3-2).
- **GA-3 — determinism recipe's exact rcParams (REQ-P23-03):** `svg.fonttype: path` +
  fixed `svg.hashsalt` + `metadata={'Date': None}` + vendored OFL font registered via
  `font_manager.addfont` before `font.family` resolves to it + pinned matplotlib version
  recorded in `FIGURE-MANIFEST.yaml`; proven by an off-gate-path double-render
  hash-equality test (`skipIf` matplotlib absent).
- **D-P23-03 — hermeticity hardening (REQ-P23-03):** add `"matplotlib"` to
  `test_gate_path_hermetic.FORBIDDEN` — a cheap structural guard that turns a future
  "render inline on the gate path" regression red; safe because no gate module imports
  matplotlib today.
- **D-P23-04 — zero new codes this phase (REQ-P23-04/05, D-06):** the snippet catalog
  *routes* to existing codes, the determinism test is off the gate path (no `report.add`),
  and the palette gate defers behind a D-13 entry condition — so Phase 23 mints **zero**
  code, proven by a set-identity diff `276 → 276` at S3-4 (Phase-21 precedent).

### GA-1 — the `.mplstyle` file set and per-file license/attribution headers (REQ-P23-01)

**Four files ship in a new top-level `styles/` directory** (matplotlib style sheets are
loaded by name/path via `plt.style.use`; keeping them out of `dsx/` also keeps them off the
gate path automatically):

| File | Provenance | License class | Vendoring rule | Load-bearing at ship? |
|---|---|---|---|---|
| `dsx-538.mplstyle` | fork of matplotlib's `fivethirtyeight` style sheet | Matplotlib License (BSD-compatible, PSF-derived) | fork **verbatim** OK; header credits matplotlib | **yes** — we vendor it |
| `dsx-urban.mplstyle` (**house default**) | Urban Institute data-viz guide + palette hexes | Apache-2.0 | vendor palette hexes + rcParams; header credits Urban | **yes** — we vendor palette |
| `dsx-econ.mplstyle` | reimplemented from published Economist doctrine | source PDF **unlicensed** | **cite, never embed**; our own rcParams; **no** proprietary font | no — nothing vendored |
| `dsx-bbc.mplstyle` | reimplemented from the BBC cookbook's prose | `bbplot` is **GPL-2.0** | **never port code**; our own rcParams; **no** proprietary font | no — nothing vendored |

**Font strategy (Architect + Advisor, decisive).** Vendor **exactly one** OFL family —
**Lato (SIL OFL 1.1)** — as the deterministic house face, registered via `font_manager`.
Every style's `font.family` / `font.sans-serif` resolves to it. `dsx-econ` / `dsx-bbc` use
the **same vendored OFL font as an open stand-in** for their proprietary faces (Econ
Sans / Reith), with a header note stating so — this keeps all four styles deterministic
without ever touching a proprietary or GPL asset. A second vendored OFL family for closer
aesthetic fidelity is a plan-level nicety, **deferred** (one font family = one determinism
surface to prove). Ship the OFL licence text alongside the vendored `.ttf`.

**Per-file header (each `.mplstyle` opens with a comment block):** source name + URL,
license (SPDX where clean), the vendoring rule applied, and for `dsx-econ`/`dsx-bbc` the
explicit line *"Reimplemented from published doctrine; not affiliated with or endorsed by
<publisher>; no source-PDF text, no GPL code, and no proprietary font are included."* The
**exact header wording** is pinned at plan (S3-2) and is the license-audit gate's artifact.

**Robustness note (Auditor, rigour tier — recorded because it reframes the risk).** The
*reimplement-from-doctrine* posture for `dsx-econ` and `dsx-bbc` is safe under **any**
license the source carries — so the exact license fact for those two is load-bearing only
for the **header wording**, not for shipping safety. The genuinely load-bearing license
facts are the three assets we **vendor**: the matplotlib style fork, the Urban palette
hexes, and the Lato `.ttf`. Those three get **at-locator confirmation before shipping**
(the S3-2 license-audit gate); the other two are cite-only and cannot contaminate.

**License-audit checklist (REQ-P23-01's explicit plan-review item — run at S3-2, evidence
presented then; a confirmation line is filed to HUMAN-QUEUE at that point, like the
security sign-offs, non-blocking until S5-2):**

1. Confirm matplotlib's LICENSE at the pinned version permits vendoring the
   `fivethirtyeight` style sheet verbatim. *(vendored — load-bearing.)*
2. Confirm the Urban Institute source's Apache-2.0 license and that the vendored artefact
   is the palette hexes / rcParams, not copied prose. *(vendored — load-bearing.)*
3. Confirm Lato ships under SIL OFL 1.1 and bundle the OFL license text with the `.ttf`.
   *(vendored — load-bearing.)*
4. Confirm `dsx-econ` embeds **no** Economist PDF text and **no** proprietary font; its
   rcParams are our own derivation from published doctrine (cited, not copied).
5. Confirm `dsx-bbc` contains **no** line derived from `bbplot`'s GPL-2 source and **no**
   proprietary Reith font; behaviour is re-derived from the cookbook's prose.
6. Confirm every `.mplstyle` carries its header block (source, license, vendoring rule).

### GA-2 — `dsx_plotstyle.py` public function signatures (REQ-P23-02)

**Chosen public surface (matplotlib-only, analyst-side, off the gate path, in
`templates/`):**

- **`finalise_figure(fig, *, title, source, subtitle=None, note=None) -> Figure`** —
  applies title-as-takeaway, optional subtitle, an optional footnote, and the **mandatory
  source line**. `source` is a **required keyword with no default**, so the
  "mandatory-source" doctrine is enforced by the signature (a call that omits it is a
  `TypeError`, not a silently source-less figure). Returns the mutated `Figure` for
  chaining.
- **`direct_label(ax, *, ...) -> list[Text]`** — direct labelling over legends: places
  series labels at line/point termini and returns the created `Text` artists. Exact keyword
  set (which series, colour inheritance, offset) pinned at plan.
- **`save_deterministic(fig, path, *, metadata=None, **savefig_kwargs) -> Path`** — writes
  the SVG with the full determinism recipe (GA-3) applied, and returns the written `Path`.
  **It does NOT compute the seal** — the seal stays the job of `dsx seal` (stdlib SHA-256,
  the single hashing authority on the gate path). This deliberately keeps **one** source of
  truth for the hash; the analyst runs `save_deterministic(...)` then `dsx seal <path>` and
  pastes the result into `FIGURE-MANIFEST.yaml`. (Rejected: returning the sha from
  `save_deterministic` — it would create a second hasher that could silently diverge from
  `dsx seal`. Rigour > convenience.)

**Why keyword-explicit and `~150` lines (Architect).** The helper is read by analysts as
documentation-by-signature; keyword-only params make each call self-describing and prevent
positional-arg mistakes in a figure-finalisation call that is easy to get subtly wrong.
Bodies are pinned at plan (plan-checker-verifiable), like Phase 22 pinned its per-row
catalog enumeration at plan.

### GA-3 — the determinism recipe's exact rcParams (REQ-P23-03)

**The recipe, each item with the failure mode it closes:**

- **`svg.fonttype: path`** — render glyphs as vector paths, so the SVG carries **no
  font-name dependency**; a machine lacking the font still produces byte-identical geometry.
  (Closes the "font substitution changes the file" break — Windows font fallback is the
  #1 hash-breaker per scope §3.3.)
- **`svg.hashsalt: '<fixed project salt>'`** (e.g. `"dsx"`) — matplotlib's default salt is
  `None`, which seeds element `id`/clip-path generation from a **per-process random**; a
  fixed salt makes those ids deterministic. (Closes the "same figure, different `id=`
  attributes" break.)
- **`metadata={'Date': None}`** passed to `savefig` — matplotlib embeds a `<dc:date>`
  creation timestamp in SVG metadata by default. Stripping it removes the one guaranteed
  per-render difference. (Closes the "timestamp in metadata" break.)
- **Vendored OFL font registered via `font_manager.fontManager.addfont(<vendored .ttf>)`**
  *before* rcParams set `font.family` to it — guarantees the same font is resolved on every
  machine regardless of system fonts. (Belt-and-braces with `svg.fonttype: path`.)
- **Pinned matplotlib version recorded in `FIGURE-MANIFEST.yaml`** (a `matplotlib_version`
  field alongside `svg_sha256`) — path-rendering geometry can shift between matplotlib
  releases, so the pinned version is the reproducibility **contract**: a seal is
  reproducible *at that version*. (Closes the "different matplotlib, different paths" break
  honestly — by recording the bound rather than pretending cross-version stability.)

**Proof (off the gate path).** A `tests/test_*_determinism.py` renders one representative
figure **twice** through `save_deterministic` and asserts the two `svg_sha256` values are
**equal**, `@unittest.skipIf` matplotlib is absent. It is a repo-integrity test (no
`report.add`, mints no code) and is **not** on any `GATE_PROFILES` path.

### D-P23-03 — hermeticity hardening (REQ-P23-03)

REQ-P23-03 requires `test_gate_path_hermetic` to **stay true**. It holds by construction
(the helper lives in `templates/`, outside the `dsx/` closure the test walks). **Decision:
also add `"matplotlib"` to `test_gate_path_hermetic.FORBIDDEN`.** This is a cheap,
strictly-strengthening structural guard: it turns a future "just render the chart inline on
the gate path" simplification **red** instead of letting it ship. It is safe today — no gate
module imports matplotlib (the gate path is stdlib-pure; `figures.py` uses `hashlib` only) —
verified against the live `FORBIDDEN`/closure walk. Recorded as a plan-level edit for S3-2.

### D-P23-04 — zero new codes this phase (REQ-P23-04/05, D-06)

Phase 23 is a **zero-mint** phase (Phase-21 precedent):

- **Snippet catalog (REQ-P23-04)** imports `dsx_plotstyle.py` and **routes** each snippet
  to the relevant existing finding code (e.g. `DSX-FIG-011` for the seal, `DSX-VIZ-*` for
  chart choice) — it **never restates a gate threshold**. No new code.
- **Determinism test (REQ-P23-03)** is off the gate path — no `report.add`. No new code.
- **Palette gate (REQ-P23-05)** is **deferred** behind a D-13 entry condition: the WCAG-AA
  contrast-verified palettes ship *in the style files* with per-palette citations, but no
  palette-**enforcing** gate code is minted this phase (a palette gate would need its own
  entry condition + calibration). Contrast verification is a repo-integrity property, not a
  `report.add` code.

The set-identity mint diff at S3-4 must therefore prove **`276 → 276`** (empty symmetric
difference), exactly as Phase 21 proved `275 → 275`.

## What Phase 23 execute (S3-3) is bound to

1. **Create `styles/`** with the four `.mplstyle` files (GA-1), each with its license
   header; **vendor one OFL font** (Lato) + its OFL license text; `dsx-urban` is the
   documented house default.
2. **Create `templates/dsx_plotstyle.py`** (GA-2) — `finalise_figure`, `direct_label`,
   `save_deterministic`; matplotlib-only; mandatory `source`; `save_deterministic` writes,
   `dsx seal` hashes.
3. **Implement the determinism recipe** (GA-3) and prove it with an off-gate-path
   double-render hash-equality test (`skipIf` matplotlib absent); record `matplotlib_version`
   in the manifest template.
4. **Add `"matplotlib"` to `test_gate_path_hermetic.FORBIDDEN`** (D-P23-03) and keep the
   test green.
5. **Author the per-chart-type snippet catalog** (REQ-P23-04) — imports the helper, routes
   to finding codes, restates no thresholds; points at Phase 22's `references/chart-catalog.md`.
6. **Ship WCAG-AA palettes** in the style files with per-palette citations (REQ-P23-05); the
   palette *gate* is a D-13-deferred entry condition, **no code minted**.
7. **Prove zero mint** — set-identity diff `276 → 276` at S3-4 (D-P23-04).

## Open questions / carried caveats

- **HQ-32 (veto window, non-blocking):** GA-1 (four-file set + one-OFL-font strategy + house
  default), GA-2 (three signatures + single-hasher decision), GA-3 (recipe), D-P23-03
  (matplotlib → FORBIDDEN), D-P23-04 (zero mint). Silence = accept; nothing blocks on it.
- **License-audit confirmation is owed at S3-2, not here.** The audit is REQ-P23-01's
  explicit plan-review item; the loop runs the six-point checklist above (at-locator
  confirmation for the three vendored assets) at plan-review and files a **non-blocking**
  confirmation line to HUMAN-QUEUE at that point — mirroring the security sign-offs
  (HQ-29/HQ-31), which were filed at secure-phase, not discuss. Not filed this firing.
- **Pinned at plan (S3-2), not here:** the exact `.mplstyle` rcParams and header wording;
  `direct_label`'s keyword set; the fixed `svg.hashsalt` value; the snippet catalog's exact
  chart-type list and code routing; the exact Lato weights vendored.
- **D-05 status:** Phase 23 relies on the scope §3.3 license findings (2026-08-29 research);
  the three vendored assets get at-locator confirmation at S3-2. No primary-source *paper*
  read is owed. The reimplement-from-doctrine posture makes the `dsx-econ`/`dsx-bbc` license
  facts non-load-bearing for shipping safety (D-P23-01 robustness note).
