---
phase: 23
slug: style-snippet-layer
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-09-03
---

# Phase 23 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seed authored by plan-phase (S3-2) from `23-RESEARCH.md` §Validation Architecture.
> The Per-Task map is filled by the planner (task IDs do not exist until PLAN.md is written);
> the gap analysis + `nyquist_compliant` flip happen at validate-phase (S3-5).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (every module in `tests/` uses `unittest.TestCase`) |
| **Config file** | none — tests run via `python -m unittest`; no `pytest.ini`/`unittest.cfg` |
| **Quick run command** | `python -m unittest tests.test_<module> -v` (the specific new module a task touches) |
| **Full suite command** | `python -m unittest discover -s tests` |
| **Estimated runtime** | ~40 seconds (prior phases measured 40.4s / 41.6s full-suite) |

---

## Sampling Rate

- **After every task commit:** Run the specific new test module(s) that task touches (`python -m unittest tests.test_<module> -v`).
- **After every plan wave:** Run `python -m unittest discover -s tests` **plus** `python scripts/gen-finding-catalogue.py --check` (catches any accidental mint — D-P23-04 requires 276→276).
- **Before `/gsd-verify-work`:** Full suite green from a clean tree (sweep any stray root `DECISIONS.jsonl` first — standing note) and `gen-finding-catalogue.py --check` exit 0.
- **Max feedback latency:** ~40 seconds (full suite).

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 23-01-T1 (RED) | 23-01 | 1 | REQ-P23-01, REQ-P23-05 | T-23-03 | Header shape + WCAG-AA thresholds encoded before any style file | unit (stdlib text/luminance) | `python -m unittest tests.test_style_headers tests.test_style_wcag_contrast` | ❌ Wave 0 | ⬜ pending |
| 23-01-T2 (font vendor) | 23-01 | 1 | REQ-P23-01 | T-23-01 | Pinned canonical OFL URL + recorded `.ttf` SHA-256 | build-order fixture | inline `python -c` (2 Lato `.ttf` + OFL.txt present, checksums printed) | ❌ Wave 0 | ⬜ pending |
| 23-01-T3 (GREEN) | 23-01 | 1 | REQ-P23-01, REQ-P23-05 | T-23-03 | Four headered `.mplstyle` + WCAG-AA palettes; econ/bbc reimplemented-not-affiliated line | unit | `python -m unittest tests.test_style_headers tests.test_style_wcag_contrast -v` | ❌ Wave 0 | ⬜ pending |
| 23-02-T1 (RED) | 23-02 | 2 | REQ-P23-02, REQ-P23-03 | T-23-04, T-23-05 | Signatures + mandatory-`source` TypeError; double-render determinism | unit (`skipIf` mpl absent) | `python -m unittest tests.test_dsx_plotstyle_api tests.test_dsx_plotstyle_determinism` | ❌ Wave 0 | ⬜ pending |
| 23-02-T2 (GREEN) | 23-02 | 2 | REQ-P23-02, REQ-P23-03 | T-23-04, T-23-05 | GA-3 recipe; save_deterministic writes-only (no second hasher); `matplotlib_version` in manifest | unit | `python -m unittest tests.test_dsx_plotstyle_api tests.test_dsx_plotstyle_determinism -v` + manifest `python -c` | ❌ Wave 0 | ⬜ pending |
| 23-02-T3 (hermeticity) | 23-02 | 2 | REQ-P23-03 | T-23-02 | `"matplotlib"` in FORBIDDEN; gate path stays stdlib-pure | unit (edit existing) | `python -m unittest tests.test_gate_path_hermetic -v` | ✅ exists, edit only | ⬜ pending |
| 23-03-T1 (RED) | 23-03 | 3 | REQ-P23-04 | T-23-06, T-23-08 | Cited ⊆ defined; no live-threshold restatement (values read from viz.py) | unit | `python -m unittest tests.test_snippet_catalog_routing` | ❌ Wave 0 | ⬜ pending |
| 23-03-T2 (GREEN) | 23-03 | 3 | REQ-P23-04 | T-23-06 | Route by code name only; skill `<references>` wired | unit | `python -m unittest tests.test_snippet_catalog_routing -v` + sections/skill `python -c` | ❌ Wave 0 | ⬜ pending |
| 23-03-T3 (zero-mint prove) | 23-03 | 3 | REQ-P23-04 (D-P23-04) | T-23-07 | 276→276 set-identity; mint surfaces unedited | unit (existing) | `python -m unittest discover -s tests` + `python scripts/gen-finding-catalogue.py --check` | ✅ exists, no edit | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky. See `23-RESEARCH.md` §Validation Architecture "Phase Requirements → Test Map" for the seed mapping the planner expands.*

---

## Wave 0 Requirements

New test modules the plan must create (RED before GREEN; TDD mode is ON):

- [ ] `tests/test_style_headers.py` — REQ-P23-01 (per-file license/attribution header presence + shape, stdlib text read)
- [ ] `tests/test_dsx_plotstyle_api.py` — REQ-P23-02 (exact keyword-only signatures; `finalise_figure` without `source=` raises `TypeError`)
- [ ] `tests/test_dsx_plotstyle_determinism.py` — REQ-P23-03 (double-render `svg_sha256` byte-equality, `@unittest.skipIf` matplotlib absent, **off the gate path**)
- [ ] `tests/test_snippet_catalog_routing.py` — REQ-P23-04 (every cited code exists in `references/finding-codes.md`; no snippet restates a `dsx/checks/viz.py` numeric threshold)
- [ ] `tests/test_style_wcag_contrast.py` — REQ-P23-05 (palette hexes meet WCAG AA 4.5:1 text / 3:1 graphical; stdlib relative-luminance formula)
- [ ] `tests/test_gate_path_hermetic.py` — **edit only** (add `"matplotlib"` to `FORBIDDEN`, D-P23-03; the file already exists)
- [ ] `tests/test_finding_catalogue_invariant.py` — **no edit expected** (zero-mint 276→276 asserted via the existing set-identity pattern; touch only if a code is unexpectedly affected)
- [ ] Framework install: **none** — stdlib `unittest` is already the project convention
- [ ] Build-order fixture dependency: `styles/fonts/Lato-*.ttf` + `OFL.txt` must exist on disk before `test_dsx_plotstyle_determinism.py` can pass (plan must sequence vendor-font → write-helper → write-determinism-test)

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| License-audit six-point checklist: at-locator confirmation for the **three vendored assets** (matplotlib `fivethirtyeight.mplstyle` fork under Matplotlib License; Urban Institute palette under Apache-2.0; Lato under SIL OFL 1.1) + no-embed/no-port confirmation for `dsx-econ`/`dsx-bbc` | REQ-P23-01 | Provenance/license authenticity is a human read (D-05 class) — the loop prepares the evidence, it may not sign it. Filed to HUMAN-QUEUE non-blocking at S3-2, mirroring the security sign-offs (HQ-29/HQ-31); due by S5-2 | Confirm each vendored asset's license at its source locator; confirm no Economist-PDF text and no `bbplot` GPL line is embedded; confirm every `.mplstyle` carries its header block. Evidence pack presented at S3-2 plan-review. |

*All other Phase-23 behaviors have automated verification (the Wave 0 modules above).*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter (at validate-phase S3-5)

**Approval:** pending
