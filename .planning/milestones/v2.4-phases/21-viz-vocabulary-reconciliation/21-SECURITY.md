---
phase: 21
slug: viz-vocabulary-reconciliation
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-09-02
---

# Phase 21 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| (none introduced) | This phase edits static, in-repo Python vocabulary data structures (`CHART_CAPABILITIES`, `RELATIONSHIP_CHARTS`, `BANNED_TYPES`), regenerates one static generated artifact (`dsx/data/input_types.json`), and adds one off-gate-path test. | None. No network input, no untrusted parse, no auth/session, no file/process I/O introduced. The only "input" is the repo's own static vocabularies, edited by a developer under review. |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-21-01 | Tampering | `CHART_CAPABILITIES` / `RELATIONSHIP_CHARTS` (future mark added with no capability home, no relationship home, and no `CAPABILITY_ONLY` allowlist entry) | medium | mitigate | Every-mark-has-a-home invariant test (`tests/test_viz_vocabulary_invariant.py::TestEveryMarkHasAHome::test_every_mark_has_a_capability_home` + `::test_every_mark_has_a_relationship_home_or_is_allowlisted`) turns red at commit time on exactly this drift class — a test, not a runtime guard (D-01, REQ-P21-01). Re-run 2026-09-02: GREEN. | closed |
| T-21-02 | Repudiation | `BANNED_TYPES` refusal record shipping with an empty reason/code/citation (an unfounded ban with no traceable justification) | medium | mitigate | `TestRefusalEntryCompleteness::test_every_banned_type_has_a_complete_refusal_record` asserts all three fields non-empty for all five banned types; `::test_every_refusal_code_is_the_code_check_banned_emits` pins `code == "DSX-VIZ-001"`; `::test_check_banned_detail_is_the_reason_string` confirms the reader path (D-02, REQ-P21-02). Re-run 2026-09-02: GREEN. | closed |
| T-21-03 | Tampering | finding-code catalogue (a code silently minted or altered by the `BANNED_TYPES` value-type change str→dict) | low | mitigate | REQ-P21-03 set-identity: `gen-finding-catalogue.py::extract()` never reads `detail=`, so the dict-promotion cannot mint a code; `tests/test_finding_catalogue_invariant.py` + `tests/test_gen_finding_catalogue.py` confirm 275→275 (verified in 21-VERIFICATION.md: symmetric difference EMPTY). Re-run 2026-09-02: GREEN. | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on (high) count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

No threat rises to `high`; nothing blocks under the ASVS level-1 block-on-`high` policy.
**Package legitimacy gate: N/A** — this phase installs no npm/pip/cargo packages, so no `T-21-SC` supply-chain threat and no legitimacy checkpoint apply.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|

No accepted risks — all three threats closed by mitigation (in-tree tests), not by risk acceptance.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-02 | 3 | 3 | 0 | autonomous loop firing (secure-phase orchestrator, opus/high) — State B create; ASVS-L1 short-circuit (threats_open:0, register authored at plan time); all three mitigation modules re-run GREEN by the orchestrator (`tests.test_viz_vocabulary_invariant` + `tests.test_finding_catalogue_invariant` + `tests.test_gen_finding_catalogue` = 55 tests OK) rather than trusted from the S1-4 report |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer) — all three `mitigate`
- [x] Accepted risks documented in Accepted Risks Log — none; all closed by mitigation
- [x] `threats_open: 0` confirmed — all three CLOSED with live GREEN test evidence
- [x] `status: verified` set in frontmatter — machine audit complete and clean

**Approval:** verified (technical) 2026-09-02 — gate **SECURED**, `threats_open: 0`, 3/3 threats CLOSED by orchestrator re-gate. **Human sign-off granted 2026-09-03 (operator verdict recorded in HUMAN-QUEUE.md, item HQ-29):** the sign-off line above is approved as written, and Phase 21's UAT is confirmed — the phase has no user-facing runtime behavior, so its acceptance test IS the automated invariant set (`nyquist_compliant: true`, 3/3 requirements COVERED). Before signing, an interactive session **independently re-ran the mitigation modules rather than trusting the report**: `test_viz_vocabulary_invariant`, `test_finding_catalogue_invariant` and `test_gen_finding_catalogue` (the tests backing T-21-01/02/03) green as part of a 79-test run, and `gen-finding-catalogue.py --check` exit 0. The one residual human read (refusal-citation authenticity, including the then-provisional `radar` row) was discharged separately in **HQ-27**, which replaced that placeholder with a peer-reviewed source. Phase 21 is now both technically verified and human-approved.
