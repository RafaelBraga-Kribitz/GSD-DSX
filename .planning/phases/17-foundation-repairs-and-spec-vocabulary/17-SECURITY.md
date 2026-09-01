---
phase: 17
slug: foundation-repairs-and-spec-vocabulary
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on (high) severity
threats_open: 0
asvs_level: 1
created: 2026-09-01
---

# Phase 17 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register origin: `register_authored_at_plan_time: true` (all three PLAN files carried a
> parseable `<threat_model>` block). ASVS L1, `security_block_on: high`. Every non-accepted
> mitigation was re-run green by the orchestrator (brief §5 "re-run, don't trust"), so the
> L1 short-circuit was taken with evidence rather than on faith.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| analyst-authored `ANALYSIS-SPEC.yaml` → dsx loader/parser → `dsx/spec.py` validate + `dsx/checks/stats.py` check | The single external input surface. Phase 17 **adds** one input-validation control (the `estimand_kind` membership guard) and weakens none. No network, auth, subprocess, or new file-write path is introduced. | analyst-authored YAML spec (non-sensitive; local) |
| generated `references/finding-codes.md` ↔ real `report.add(...)` call sites | Documentation-of-enforcement boundary; kept honest by `scripts/gen-finding-catalogue.py` and its `--check` gate. | generated catalogue text |
| `references/test-selection.md` ↔ `dsx/checks/stats.py` routing table | Doc/code agreement surface; bound for Boschloo by `test_boschloo_reconciliation` (Boschloo-specific down payment on REQ-P20-04). | routing-doctrine text |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-17-01-01 | Tampering | `test-selection.md` drifting from `stats.py` routing | low | mitigate | `test_boschloo_reconciliation` binds the doc's Boschloo name to the code's emitted two-proportion alternative — silent divergence turns it red | closed |
| T-17-01-02 | Tampering | `NONPARAMETRIC_TESTS` set — accidental replace-not-add dropping `fisher_exact` | low | mitigate | `test_boschloo_exact_added_without_dropping_fisher_exact` asserts `fisher_exact` remains a member alongside `boschloo_exact` | closed |
| T-17-01-SC | Tampering | npm/pip/cargo installs | low | accept | Zero packages installed (stdlib `unittest` only; python3 3.14.6). See Accepted Risks. | closed |
| T-17-02-01 | Tampering | `recommend_test` routing — a future outcome-type branch silently rerouting `time_to_event` | low | mitigate | `test_no_time_to_event_equality_guard_in_source` negative-scans the source for an equality guard on the literal; any future guard forces a reviewed contract change | closed |
| T-17-02-02 | Repudiation | a recorded decision (D-12a dispositions / D-06 ranges) silently absent | low | mitigate | Deterministic grep oracle confirms all nine D-12a gate dispositions + the D-06 range anchors (050–129, 130s reserve) present in committed `17-CONTEXT.md` | closed |
| T-17-02-SC | Tampering | npm/pip/cargo installs | low | accept | Zero packages installed (stdlib `unittest` + stdlib `inspect`/`re`). See Accepted Risks. | closed |
| T-17-03-01 | Tampering | `estimand_kind` guard implemented as substring/fuzzy match | low | mitigate | Exact `normalize(value) not-in vocab` equality only; `test_mis_slotted_value_fires_one_loud_finding` + `test_valid_member_fires_nothing` assert exactly one DSX-STA-040 on a bogus value and none on a valid one | closed |
| T-17-03-02 | Repudiation | the guard silently skipped when a sibling field is absent | low | mitigate | Membership loop runs INDEPENDENTLY of the declared-test early return (D-01); `test_outcome_type_membership_fires_without_a_declared_test` (Pitfall-2) green | closed |
| T-17-03-03 | Tampering | `references/finding-codes.md` committed out of sync with the widened DSX-STA-040 row | medium | mitigate | `scripts/gen-finding-catalogue.py --check` exit 0 = "finding catalogue is current"; DSX-STA-040 NOT among the pre-existing duplicate-text warnings (single call site) | closed |
| T-17-03-04 | Spoofing | a new finding code smuggled in under cover of the vocabulary work | medium | mitigate | Guard reuses DSX-STA-040 from a single call site; `test_finding_catalogue_stays_at_260_codes` + `test_code_set_is_phase12_snapshot...` assert the 260-code SET is unchanged (REQ-P17-05) | closed |
| T-17-03-SC | Tampering | npm/pip/cargo installs | low | accept | Zero packages installed (stdlib `unittest`; python3 3.14.6; no external dependency). See Accepted Risks. | closed |

*Status: open · closed · open — below `high` threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-17-01 | T-17-01-SC, T-17-02-SC, T-17-03-SC | Supply-chain (dependency-confusion / malicious install) is inapplicable: Phase 17 installs **zero** packages — stdlib `unittest`/`inspect`/`re` only, on the confirmed local python3 3.14.6. No package-legitimacy audit is owed. Low severity, below the `high` block threshold. | Phase 17 plan threat registers (persona round, S1-1); operator approval pending (HUMAN-QUEUE HQ-19) | 2026-09-01 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-01 | 11 | 11 | 0 | orchestrator (secure-phase, State B, ASVS L1; every mitigation gate re-run green — 13 targeted tests + catalogue `--check` exit 0) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter (threat register verified by the orchestrator)

**Approval:** threat register verified 2026-09-01 (orchestrator, threats_open:0). **Operator security sign-off PENDING — batched to HUMAN-QUEUE HQ-19, non-blocking until close-out S5-2 per LOOP-LEDGER S1-5.** The loop prepared and verified this register; the outward-facing security approval line is a human read (brief §4 item 4) and is not self-signed.
