---
phase: 22
slug: catalog-spine-uncertainty-heuristic
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-09-03
---

# Phase 22 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| (none introduced) | This phase edits static, in-repo Python gate vocabularies (`RELATIONSHIP_CHARTS` 11th `"uncertainty"` key, `CHART_CAPABILITIES['interval-range']`, `BANNED_TYPES`), mints one gate code (`DSX-VIZ-071`) in `dsx/checks/viz.py`, regenerates two static generated artifacts (`dsx/data/input_types.json`, `references/finding-codes.md`), and adds/extends off-gate-path repo-integrity tests + reference-doc surfaces (`references/chart-catalog.md`, `chart-selection.md`, `question-taxonomy.md`, `skills/dsx-visualize/SKILL.md`). | None. No network input, no untrusted parse, no auth/session, no file/process I/O introduced. The only "input" is the repo's own static vocabularies and Markdown, edited by a developer under review. |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-22-01 | Tampering | A new uncertainty mark added to `RELATIONSHIP_CHARTS['uncertainty']` with no capability home | medium | mitigate | Phase-21 every-mark-has-a-home invariant, extended to the 11th key: the ten §5.6 marks are homed into `CHART_CAPABILITIES['interval-range']` (`tests/test_viz_vocabulary_invariant.py`). Re-run 2026-09-03: GREEN. | closed |
| T-22-02 | Repudiation | `gauge` / `word_cloud` / `radar` refusal citation traceable to no signed source (gauge attributing the arbitrary-maximum claim to Few) | medium | mitigate | `BANNED_TYPES` completed to seven `{reason, code=DSX-VIZ-001, citation}` records; `radar`'s PROVISIONAL replaced by Duan et al. 2023; `gauge`/`word_cloud` sourced from signed HQ-27 rows, arbitrary-max marked DSX's own reasoning (D-4/HQ-27). Refusal-record completeness re-run in `tests/test_viz_vocabulary_invariant.py`. Re-run 2026-09-03: GREEN. | closed |
| T-22-03 | Tampering | `facet_by` silently treated as a chart type (widening what the gate admits under cover of a "declaration") | low | mitigate | The facet_by-orthogonality assertion fails if `facet_by` appears in any `RELATIONSHIP_CHARTS` / `CHART_CAPABILITIES` / `BANNED_TYPES` value; REQ-P22-03 keeps it a declaration, `DSX-SMELL-007`'s remedy routes to it (no new code). Re-run 2026-09-03: GREEN. | closed |
| T-22-04 | Tampering | finding-code catalogue (a non-additive mint, a cardinality-preserving swap, or a silently dropped code alongside `DSX-VIZ-071`) | medium | mitigate | `tests/test_finding_catalogue_invariant.py` asserts both the count (`_EXPECTED_TOTAL` 276) and the exact set-identity (`added={DSX-VIZ-071}`, `removed={}`); a swap the count invariant would pass is caught by the set diff. Sibling lockstep pins (p19, phase20) bumped 275→276 keep their real zero-mint tells. Re-run 2026-09-03: GREEN. | closed |
| T-22-05 | Repudiation | `DSX-VIZ-071` shipping without an enforceable D-05 citation (an ungrounded gate code) | medium | mitigate | The exact-string `_D05_ALLOWLIST_CODES` entry turns the `Citation:` / `Structural criterion:` docstring lines and the `# D-05` marker into a build gate; `scripts/gen-finding-catalogue.py --check` fails red if any is missing; `tests/test_uncertainty_vocabulary.py` asserts DSX-VIZ-071 member/non-member/absent behavior. Re-run 2026-09-03: `gen --check` exit 0 @276; tests GREEN. | closed |
| T-22-06 | Tampering | `DSX-VIZ-072` minted with no distinct decidable trigger (a code duplicating DSX-VIZ-012/071 or manufacturing a false paradigm partition) | low | mitigate | The recorded decision does not mint DSX-VIZ-072 (the ten §5.6 marks are paradigm-symmetric → no mark→paradigm partition to gate); the set-identity invariant turns red if a 277th code appears, forcing any future mint through its own decided change. Re-run 2026-09-03: GREEN (total 276, not 277). | closed |
| T-22-07 | Tampering | A catalog refusal/admissible row drifting from the live `BANNED_TYPES` / `_mark_universe()` (the drift surface Phase 21's doctrine forbids) | medium | mitigate | The catalog↔vocabulary conformance clauses read live `BANNED_TYPES` and `_mark_universe()` and assert set-identity both directions; a stale catalog turns `tests/test_chart_catalog_invariant.py` red at commit (REQ-P22-01). Re-run 2026-09-03: GREEN. | closed |
| T-22-08 | Repudiation | A shipped citation tracing to an HQ-27 still-unverified item, or to Abela 2008 / Few's Graph Selection Matrix (never submitted), presented as verified; or a Ribecca-lineage triangulation claim | medium | mitigate | The citation-traceability negative guard (`tests/test_chart_catalog_invariant.py`) and the doc-conformance forbidden-token guard (`tests/test_selection_heuristic_docs.py`) fail on any forbidden token; lineage rows name the lineage, never triangulation. Re-run 2026-09-03: GREEN. | closed |
| T-22-09 | Tampering | A `reference_only` row silently widening what the gate admits (a documented type mistaken for an admissible one) | low | mitigate | The reference-only isolation clause asserts every `reference_only` mark is NOT in `_mark_universe()` (`tests/test_chart_catalog_invariant.py`); the gate reads the live dicts, never the catalog. Re-run 2026-09-03: GREEN. | closed |
| T-22-10 | Tampering | `chart-selection.md` continuing to ship the superseded 7-item strict perceptual ordering while the tie-break test asserts the corrected one (a self-contradicting repo) | medium | mitigate | The line was rewritten to D-1's six-rank-with-ties form; the doc-conformance test fails if the superseded chain or a stray `density` channel survives; the tie-break structural criterion (`rank(a) <= rank(b)`, `length==angle` both ways, `density` absent) holds in `tests/test_chart_catalog_invariant.py` + `tests/test_selection_heuristic_docs.py`. Re-run 2026-09-03: GREEN. | closed |
| T-22-11 | Repudiation | The heuristic citing Abela 2008 or Few's Graph Selection Matrix as if HQ-27-signed (never submitted), or claiming triangulation across the Ribecca lineage | medium | mitigate | Tasks cite only Munzner ch.3 + FT (from the signed HQ-27 set); the doc-conformance forbidden-token guard (`tests/test_selection_heuristic_docs.py`) fails on the forbidden tokens; lineage is named, not triangulated. Re-run 2026-09-03: GREEN. | closed |
| T-22-12 | Tampering | A parallel decision-tree document introduced alongside the two existing selection surfaces (two surfaces that drift) | low | mitigate | The edits are pointers into the existing files; the no-parallel-tree guard (name-pattern regex, `tests/test_selection_heuristic_docs.py`) asserts no new decision-tree file exists under `references/` (REQ-P22-04). Re-run 2026-09-03: GREEN. | closed |

*Status: all twelve `closed` — below the `high` blocking threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on (high) count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

No threat rises to `high`; nothing blocks under the ASVS level-1 block-on-`high` policy.
**Package legitimacy gate: N/A** — this phase installs no npm/pip/cargo packages, so no `T-22-SC` supply-chain threat and no legitimacy checkpoint apply.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|

No accepted risks — all twelve threats closed by mitigation (in-tree tests + the D-05 build gate), not by risk acceptance.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-03 | 12 | 12 | 0 | autonomous loop firing (secure-phase orchestrator, opus/high) — State B create; ASVS-L1 short-circuit (threats_open:0, register authored at plan time across the four 22-0N-PLAN.md threat models); every mitigation re-run GREEN by the orchestrator (six mitigation modules `tests.test_viz_vocabulary_invariant` + `tests.test_uncertainty_vocabulary` + `tests.test_finding_catalogue_invariant` + `tests.test_chart_catalog_invariant` + `tests.test_selection_heuristic_docs` + `tests.test_gen_finding_catalogue` = 79 tests OK; D-05 gate `scripts/gen-finding-catalogue.py --check` exit 0 @276; full suite 1495 OK / 41.6s) rather than trusted from the S2-3/S2-4 reports |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer) — all twelve `mitigate`
- [x] Accepted risks documented in Accepted Risks Log — none; all closed by mitigation
- [x] `threats_open: 0` confirmed — all twelve CLOSED with live GREEN test evidence
- [x] `status: verified` set in frontmatter — machine audit complete and clean

**Approval:** verified (technical) 2026-09-03 — gate **SECURED**, `threats_open: 0`, 12/12 threats CLOSED by orchestrator re-gate. **Human sign-off granted 2026-09-03 (operator verdict recorded in HUMAN-QUEUE.md, item HQ-31):** the sign-off line above is approved as written, and Phase 22's UAT is confirmed — the phase has no user-facing runtime behavior, so its acceptance test IS the automated invariant/gate set (`nyquist_compliant: true`, 5/5 requirements COVERED). Before signing, an interactive session **independently re-ran the six mitigation modules rather than trusting the report**: 79/79 tests green and `gen-finding-catalogue.py --check` exit 0 at catalogue **276** — matching this register's claims exactly. The D-05 per-citation authenticity reads behind this phase were discharged in **HQ-27** (13 citations verified against primary sources, 7 corrected); the four resulting decisions D-1…D-4 were verified as applied to the shipped tree at sign-off time. Phase 22 is now both technically verified and human-approved.
</content>
</invoke>
