---
phase: 23-style-snippet-layer
plan: 02
wave: 2
status: complete
requirements:
  - REQ-P23-02
  - REQ-P23-03
completed: 2026-09-03
---

# 23-02 SUMMARY — dsx_plotstyle.py (GA-2 helper) + GA-3 SVG-determinism recipe

Wave 2 of Phase 23 (S3-3). Executed **inline by the orchestrator** (persona-lite,
S1-3/S2-3/23-01 precedent: the plan left no irreversible design judgment — the double-render
hash-equality test is the oracle; every gate is re-run by the orchestrator on the final
tree; STATE is single-writer, so no subagent touches it). TDD RED→GREEN. Consumes Wave 1's
vendored Lato + `dsx-urban.mplstyle`.

## What shipped

- **`templates/dsx_plotstyle.py`** — the analyst-side, matplotlib-only figure-finalisation
  helper (in `templates/`, OFF the `dsx/` gate closure). Three GA-2 keyword-explicit
  functions plus `register_fonts()`:
  - `finalise_figure(fig, *, title, source, subtitle=None, note=None) -> Figure` — **`source`
    is a mandatory keyword with no default**; omitting it is a `TypeError` at call binding
    (makes "every figure cites its source" a signature property, mirroring DSX-VIZ-062).
  - `direct_label(ax, *, labels=None, color_from_line=True, x_offset=6.0, fontsize=None)
    -> list[Text]` — labels each line at its terminal point via `transforms.offset_copy`;
    skips matplotlib's internal `_child*` labels; colour inherited from the line.
  - `save_deterministic(fig, path, *, metadata=None, **savefig_kwargs) -> Path` — applies the
    GA-3 recipe and **writes only; it does NOT hash** (`dsx seal`/stdlib `hashlib` stays the
    single hashing authority — the file imports no `hashlib` and touches nothing in
    `dsx.checks`).
  - `register_fonts()` — `font_manager.fontManager.addfont` for each `styles/fonts/Lato-*.ttf`,
    **called once at module import** so Lato resolves before any `plt.style.use`/draw
    (Pitfall 1: the findfont cache clears forward-only).
- **`templates/FIGURE-MANIFEST.yaml`** — top-level `matplotlib_version: "3.11.1"` added
  directly under `manifest_version: 1` (the reproducibility contract field, REQ-P23-03).
  Additive: `dsx/checks/figures.py` never reads the key, so it mints nothing.
- **`tests/test_dsx_plotstyle_api.py`** (5 methods) — loads the helper by file path
  (`templates/` has no `__init__.py`); asserts the keyword-only signatures, `source` having
  no default, and the missing-source `TypeError`; `@skipIf` matplotlib absent.
- **`tests/test_dsx_plotstyle_determinism.py`** (1 method) — double-renders one figure through
  `save_deterministic` into a `TemporaryDirectory` and asserts byte-identical bytes under
  `dsx.checks.figures.file_sha256` (the same hasher `dsx seal` uses, not a second one);
  `@skipIf` matplotlib absent; off every `GATE_PROFILES` path; no `report.add`.
- **`tests/test_gate_path_hermetic.py`** (edit) — `FORBIDDEN += "matplotlib"` (D-P23-03);
  docstring/comment updated to record the guard and why it is safe today.

## GA-3 recipe (verified against installed matplotlib 3.11.1, 23-RESEARCH §3/§4/§5)

`save_deterministic` sets `svg.hashsalt='dsx'` (element ids become a pure function of content,
not a per-process `uuid4` — `_make_id`), `svg.fonttype='path'` (glyphs baked as vector paths),
and merges `metadata={'Date': None, **(metadata or {})}` so the per-render `datetime.today()`
timestamp is suppressed (`_write_metadata` only auto-stamps when `'Date'` is *absent*; the
helper owns the default so a caller cannot re-stamp — Pitfall 2). Lato registered before the
style resolves `font.family` (Pitfall 1). The double-render test is the machine proof this
holds.

## Gates (orchestrator-run, clean tree)

- `tests.test_dsx_plotstyle_api` + `tests.test_dsx_plotstyle_determinism` — **6 OK** (GREEN;
  RED first confirmed — 6 errors for `FileNotFoundError` on the absent helper, no assertion
  softened).
- `tests.test_gate_path_hermetic` — **2 OK** with `"matplotlib"` in FORBIDDEN (no gate module
  imports it; the render helper is in `templates/`, outside the walked `dsx/` AST closure).
- Manifest field check — `manifest_version` + `matplotlib_version: "3.11.1"` both present.
- `python scripts/gen-finding-catalogue.py --check` — **exit 0, catalogue current @276**
  (zero mint; the 9 pre-existing "declared twice" warnings unchanged).
- **Full suite (clean tree): 1505 OK, 41.6s** (1499→1505, +6 = the two new modules).

## Single-hasher rule (GA-2) — verified

`grep` of `templates/dsx_plotstyle.py` for `hashlib`/`dsx.checks`/`import dsx` returns matches
**only inside docstring prose** — no import, no call. `save_deterministic` writes the SVG and
returns the `Path`; hashing stays entirely with `dsx seal`.

## Zero mint

No `report.add` anywhere in this plan; both new test modules sit off `GATE_PROFILES` and the
helper lives outside the `dsx/` closure (D-P23-04). Catalogue stays **276** (set-identity
276→276, `gen --check` exit 0).

## Boundary

Wave 2 of 3. Wave 3 (`references/chart-snippets.md` route-to-codes snippet catalog + the
`skills/dsx-visualize/SKILL.md` `<references>` wiring, plus its zero-mint routing test)
remains — **the S3-3 checkbox stays UNCHECKED** until Wave 3 lands. Wave 3 is a separate
substantial documentation unit for a fresh firing.
