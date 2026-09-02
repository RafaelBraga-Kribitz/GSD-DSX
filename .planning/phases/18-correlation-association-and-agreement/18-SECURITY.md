---
phase: 18
slug: correlation-association-and-agreement
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on (high) severity
threats_open: 0
asvs_level: 1
created: 2026-09-02
---

# Phase 18 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register origin: `register_authored_at_plan_time: true` (both PLAN files — 18-A and 18-B —
> carried a parseable `<threat_model>` block). ASVS L1, `security_block_on: high`. Every
> non-accepted mitigation was re-run green by the orchestrator (brief §5 "re-run, don't trust"),
> so the L1 short-circuit was taken with evidence rather than on faith.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| analyst-authored `ANALYSIS-SPEC.yaml` → dsx loader → `dsx/checks/stats.py` check | The single external input surface. Phase 18 **adds** five declaration-only closed-vocabulary / structural membership guards on the `analysis:` block (DSX-STA-050/051/060/061/062) and weakens none. No data is read, no computation is performed on values, no network / auth / subprocess / new file-write path is introduced. | analyst-authored YAML spec (non-sensitive; local) |
| `report.add(...)` call sites ↔ generated `references/finding-codes.md` | Documentation-of-enforcement boundary; kept honest by `scripts/gen-finding-catalogue.py` and its `--check` gate (regeneration, never hand-edit). The five new codes are added to `_D05_ALLOWLIST_CODES` by exact name. | generated catalogue text |
| `mathx` report-only convention band tables → DSX-STA-012 recognition branch / `templates/APA-TABLE-research.md` | Report-only surface. The registry is consulted for RECOGNITION only; it must never route into the blocking DSX-STA-011 band path, and is wired only into the ungated APA template (which mints no finding code). | convention band labels (report-only) |
| `references/test-selection.md` ↔ `dsx/checks/stats.py` routing table | Doc/code agreement surface; the `recommend_association` routing and the catalog-only pointer rows are mirrored in the doc in the same commit as the code (D-08 lockstep). | routing-doctrine text |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-18-A-01 | Tampering | a closed-vocabulary gate (050/051/060/062, operand_scale) implemented as substring/fuzzy match, letting a malformed or adjacent value silently pass | low | mitigate | Exact `normalize(value)`-equality membership for every field except `weights`; DSX-STA-040 reuse for `operand_scale` recognition. `test_correlation_scale_kind_gate` + `test_agreement_completeness_gate` assert non-firing on valid members and firing on out-of-vocab — re-run green (in the 52-test Phase-18 suite) | closed |
| T-18-A-02 | Tampering | type-confused membership on the weighted-kappa `weights` field (`normalize()`/`str()` on a matrix silently matching nothing yet raising nothing) | low | mitigate | Explicit `isinstance` branch before any `normalize` (Pitfall-5): a recognised string OR a non-empty explicit matrix passes, anything else fires DSX-STA-061; a nested-list fixture proves no false positive. `test_agreement_completeness_gate` re-run green | closed |
| T-18-A-03 | Repudiation | a new code ships with no verifiable citation because the `DSX-STA-` family prefix is not in the D-05 allowlist | low | mitigate | The five codes are added by **exact name** to `_D05_ALLOWLIST_CODES`; `scripts/gen-finding-catalogue.py --check` enforces the `Citation:`/structural-criterion/`# D-05` marker discipline — re-run **exit 0** ("finding catalogue is current") | closed |
| T-18-A-04 | Tampering | regenerated `references/finding-codes.md` committed out of sync with the `report.add` sites | low | mitigate | `finding-codes.md` is regenerated (never hand-edited) via `gen-finding-catalogue.py --write` and committed in the same commit as the `report.add` sites; `--check` is the drift gate — re-run exit 0 at Total **265** | closed |
| T-18-A-05 | Tampering (false authority) | a fabricated/approximated citation locator for the D-07 not-in-hand item (the P18-03 doctrinal scale citation) | low | mitigate | The DSX-STA-050 block rests on the internal Phase-17 `estimand_kind`/scale definitions; the external doctrinal citation ships as a named, **presence-only** disposition with explicit catalog-only language — no invented page/section locator. Confirmed in `references/test-selection.md` (dCor / partial / ICC-Koo-Li / Kendall's-W all catalog-only, "no numeric boundary shipped") and in `18-VERIFICATION.md` P18-03 | closed |
| T-18-A-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (`unittest`, `inspect`, `re`). No Package Legitimacy Audit owed. See Accepted Risks. | closed |
| T-18-B-01 | Tampering (of the validation contract) | a convention band mistakenly made blocking by widening `EFFECT_SIZE_KINDS` or by feeding `label_convention_band` into DSX-STA-011 | low | mitigate | `EFFECT_SIZE_KINDS` stays exactly `{d,h,r}` (firewall test asserts equality); bands live on a separate report-only surface and `label_convention_band` is never called by the blocking guard; bands wired only into the ungated template. `test_effect_size_kinds_is_exactly_d_h_r` + `test_interpret_effect_still_rejects_a_report_only_kind` re-run green | closed |
| T-18-B-02 | Tampering (false authority) | pinning an unconfirmed boundary (ICC/Koo-Li, Kendall's W) as if cited, or a level-free Krippendorff pin | low | mitigate | Only `0.7598@ordinal` (with its level) and the Landis-Koch bands are pinned; ICC/Koo-Li and Kendall's W ship as named catalog-only entries with no numeric boundary (Kendall's W carries a "no band citation exists" note); tests assert presence only, never numeric equality, for catalog-only items. `test_effect_size_kind` re-run green | closed |
| T-18-B-03 | Tampering | the report-only recognition set drifting from the DSX-STA-012 branch that consults it | low | mitigate | The seam oracle asserts `effect_size_kind: kappa` fires neither 011 nor 012 and yields a `report.ok` — drift between the registry and the consuming branch turns it red post-merge. `test_report_only_kappa_fires_neither_011_nor_012_and_reports_ok` re-run green (RUNS, not skipped) | closed |
| T-18-B-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only. No Package Legitimacy Audit owed. See Accepted Risks. | closed |

*Status: open · closed — below `high` threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-18-01 | T-18-A-SC, T-18-B-SC | Supply-chain (dependency-confusion / malicious install) is inapplicable: Phase 18 installs **zero** packages — Python stdlib `unittest`/`inspect`/`re` only, on the confirmed local python3 3.14.6. No package-legitimacy audit is owed. Low severity, below the `high` block threshold. | Phase 18 plan threat registers (persona round, S2-1/S2-2); operator approval pending (HUMAN-QUEUE HQ-21) | 2026-09-02 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-02 | 10 | 10 | 0 | orchestrator (secure-phase, State B, ASVS L1; every non-accepted mitigation gate re-run green — full suite 1367 OK + 52 targeted Phase-18 tests + `gen-finding-catalogue.py --check` exit 0 at 265 + firewall + seam oracle) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter (threat register verified by the orchestrator)

**Approval:** threat register verified 2026-09-02 (orchestrator, threats_open:0). **Operator security sign-off PENDING — batched to HUMAN-QUEUE HQ-21, non-blocking until close-out S5-2 per LOOP-LEDGER S2-5.** The loop prepared and verified this register; the outward-facing security approval line is a human read (brief §4 item 4) and is not self-signed.
