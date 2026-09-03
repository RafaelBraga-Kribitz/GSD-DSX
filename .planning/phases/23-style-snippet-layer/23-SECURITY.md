---
phase: 23
slug: style-snippet-layer
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-09-03
---

# Phase 23 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| (none introduced) | This phase adds an **analyst-side** style/snippet layer that never touches the hermetic gate path: four `styles/*.mplstyle` (one `dsx-538` fork under the Matplotlib License, `dsx-urban` on the Apache-2.0 Urban palette as house default, `dsx-econ`/`dsx-bbc` reimplemented from published doctrine only), one vendored OFL font (`styles/fonts/Lato-*.ttf` + `OFL.txt`), the `templates/dsx_plotstyle.py` helper, `references/chart-snippets.md`, one field added to `templates/FIGURE-MANIFEST.yaml`, one `<references>` wire in `skills/dsx-visualize/SKILL.md`, and off-gate-path repo-integrity tests (`test_gate_path_hermetic.py` gains `"matplotlib"` in `FORBIDDEN`). | None. No network input at runtime, no untrusted parse, no auth/session, no new file/process I/O on the gate path. The only "inputs" are a static vendored font (checksum-pinned) and the repo's own static Markdown/rcParams, edited by a developer under review. `matplotlib` is a pre-existing analyst-side dependency, deliberately kept OUT of the `dsx/` import closure. |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-23-01 | Tampering | Vendored Lato `.ttf` — a modified/malicious font masquerading as the official Lato | medium | mitigate | Task 2 pinned the canonical Google Fonts OFL source and recorded each `.ttf` SHA-256; no unpinned mirror permitted. Re-verified 2026-09-03: `sha256sum` reproduces the recorded values EXACTLY (Regular `d636e468…5b251`, Bold `8a0aace7…d16be1`), and `OFL.txt` carries the SIL OFL 1.1 preamble + `Reserved Font Name "Lato"` (genuine, not a repackage). The at-locator license read is filed non-blocking as **HQ-33** (due by S5-2). | closed |
| T-23-02 | Elevation of Privilege | A future contributor "just renders inline on the gate path", silently pulling matplotlib (+ native code) into the hermetic `dsx/` closure | medium | mitigate | D-P23-03: `"matplotlib"` added to `tests/test_gate_path_hermetic.FORBIDDEN` — a structural AST-closure guard that turns the regression red; verified safe today (no gate module imports matplotlib; `figures.py` is `hashlib`-only). Re-run 2026-09-03: GREEN (2 OK). | closed |
| T-23-03 | Tampering (license provenance) | `dsx-econ` / `dsx-bbc` `.mplstyle` — GPL `bbplot` code or unlicensed Economist-PDF text contaminating a shipped asset via careless "reference implementation" copying | medium | mitigate | GA-1 reimplement-from-doctrine posture: rcParams are DSX's own derivation, no font/PDF/GPL bytes; the header carries the "reimplemented; not affiliated; no proprietary font" line, asserted by `tests/test_style_headers.py`. Robustness note: econ/bbc vendor nothing, so a license fact cannot contaminate — it is load-bearing only for header wording. Re-run 2026-09-03: GREEN. | closed |
| T-23-04 | Tampering | A second hasher: `save_deterministic` computing/returning its own sha256 that could silently diverge from `dsx seal` | medium | mitigate | GA-2: `save_deterministic` writes only and imports no `hashlib` (grep-confirmed docstring-prose-only hits); the determinism test reuses `dsx.checks.figures.file_sha256` (the same stdlib hasher `dsx seal` uses); the API test asserts the write-only signature. Re-run 2026-09-03: `tests/test_dsx_plotstyle_api.py` GREEN. | closed |
| T-23-05 | Tampering | A leaked per-render timestamp (`metadata=None` mistaken for date-stripping) silently breaking seal reproducibility | low | mitigate | `save_deterministic` owns the merge `{'Date': None, **(metadata or {})}` so a caller cannot omit the key (Pitfall 2); the double-render equality test would fail at a different wall-clock second if the date leaked. Re-run 2026-09-03: `tests/test_dsx_plotstyle_determinism.py::test_double_render_hash_equality` ran (NOT skipped — matplotlib 3.11.1 present) and passed. | closed |
| T-23-06 | Tampering | Snippet catalog restating a gate threshold (a second source of truth that drifts from `dsx/checks/viz.py`) | medium | mitigate | `tests/test_snippet_catalog_routing.py` builds its forbidden-restatement patterns from the LIVE `MAX_PIE_SLICES` / `MAX_CATEGORICAL_COLORS` constants (imported, never transcribed) and fails if any appears in the catalog; snippets route by code name only (D-P23-04). Re-run 2026-09-03: GREEN. | closed |
| T-23-07 | Tampering | A finding code silently minted or dropped while authoring the catalog (a cardinality-preserving swap the count alone would pass) | medium | mitigate | `tests/test_finding_catalogue_invariant.py`'s set-identity diff (`current_set == snapshot ∪ _MINTED_CODES`) + `scripts/gen-finding-catalogue.py --check` prove `added={}` `removed={}`; this phase edits none of the mint surfaces. Re-run 2026-09-03: `gen --check` exit 0 @**276**; set-identity GREEN (276→276). | closed |
| T-23-08 | Repudiation | A snippet citing a non-existent / mistyped finding code (an ungrounded route) | low | mitigate | The `cited ⊆ defined` assertion against `references/finding-codes.md` (CRLF-safe `_ROW_RE`) fails on any token that is not a real defined code. Re-run 2026-09-03: `tests/test_snippet_catalog_routing.py` GREEN. | closed |

*Status: all eight `closed` — below the `high` blocking threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on (high) count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

No threat rises to `high`; nothing blocks under the ASVS level-1 block-on-`high` policy.
**Package legitimacy gate: N/A** — this phase installs no npm/pip/cargo packages (matplotlib is a pre-existing analyst-side dependency; Lato is a static, checksum-pinned asset), so no `T-23-SC` supply-chain threat and no legitimacy checkpoint apply.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|

No accepted risks — all eight threats closed by mitigation (in-tree tests + the pinned-checksum font vendoring + the D-05 zero-mint build gate), not by risk acceptance.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-03 | 8 | 8 | 0 | autonomous loop firing (secure-phase orchestrator, opus/high) — State B create; ASVS-L1 short-circuit (threats_open:0, register authored at plan time across the three 23-0N-PLAN.md STRIDE models, `register_authored_at_plan_time: true`, none `high`); every mitigation re-run GREEN by the orchestrator (seven mitigation modules `tests.test_style_headers` + `tests.test_style_wcag_contrast` + `tests.test_dsx_plotstyle_api` + `tests.test_dsx_plotstyle_determinism` + `tests.test_gate_path_hermetic` + `tests.test_snippet_catalog_routing` + `tests.test_finding_catalogue_invariant` = 16 tests OK, incl. `test_double_render_hash_equality` NOT skipped; D-05 zero-mint gate `scripts/gen-finding-catalogue.py --check` exit 0 @276; Lato SHA-256 re-verified exact against the recorded values, OFL.txt SIL OFL 1.1 confirmed; full suite 1507 OK / 41.4s) rather than trusted from the S3-3/S3-4 reports |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer) — all eight `mitigate`
- [x] Accepted risks documented in Accepted Risks Log — none; all closed by mitigation
- [x] `threats_open: 0` confirmed — all eight CLOSED with live GREEN test/checksum evidence
- [x] `status: verified` set in frontmatter — machine audit complete and clean

**Approval:** verified (technical) 2026-09-03 — gate **SECURED**, `threats_open: 0`, 8/8 threats CLOSED by orchestrator re-gate on the clean final tree `f96bb1c` (not trusted from the S3-3/S3-4 wave reports): seven mitigation modules = 16 tests OK (incl. the off-gate-path double-render determinism oracle, run not skipped, T-23-05); `gen-finding-catalogue.py --check` exit 0 @276 (zero mint, T-23-07); Lato `.ttf` SHA-256 re-verified EXACT against the recorded values and OFL.txt SIL OFL 1.1 + reserved-name line confirmed (T-23-01); `matplotlib` in `test_gate_path_hermetic.FORBIDDEN` GREEN (T-23-02); full suite 1507 OK / 41.4s. **Human sign-off is BATCHED to HUMAN-QUEUE (HQ-34), non-blocking until S5-2**, mirroring the Phase 21 (HQ-29) and Phase 22 (HQ-31) precedents. The one residual human read behind this phase is the license-audit at-locator confirmation for the vendored Urban Apache-2.0 palette — tracked separately under **HQ-33** — not duplicated here. Phase 23 has no user-facing runtime behavior, so its UAT IS the automated invariant/gate set (`nyquist_compliant: true`, 5/5 requirements COVERED — see `23-VALIDATION.md`).
