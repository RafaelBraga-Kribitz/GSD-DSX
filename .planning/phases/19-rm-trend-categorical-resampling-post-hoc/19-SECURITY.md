---
phase: 19
slug: rm-trend-categorical-resampling-post-hoc
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on (high) severity
threats_open: 0
asvs_level: 1
created: 2026-09-02
---

# Phase 19 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register origin: `register_authored_at_plan_time: true` (both PLAN files — 19-A and 19-C —
> carried a parseable `<threat_model>` block). ASVS L1, `security_block_on: high`. **Unlike
> Phases 17–18 (all-low registers), Phase 19 carries two HIGH threats** (T-19-C-01 uncited
> code, T-19-C-02 citation laundering) — both are mitigated and **re-run green by the
> orchestrator from a clean tree** (brief §5 "re-run, don't trust"), so the L1 short-circuit
> was taken with evidence rather than on faith.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| analyst-authored `ANALYSIS-SPEC.yaml` → dsx loader → `dsx/checks/stats.py` check | The single external input surface. Phase 19 **adds** ten declaration-only closed-vocabulary / structural / `is_blank` guards on the `analysis:` block (DSX-STA-070/080/081/090/100/110/111/120/121/122) via seven per-family `_check_declared_*` helpers behind one `_check_declared_advanced_stats` dispatcher wired at both `check()` sites (stats.py:484, 501), plus seven **dataless** `recommend_*` routing functions and eight declared sub-vocabs + `POSTHOC_FAMILY_MAP`. No data is read, no computation is performed on values, no network / auth / subprocess / new file-write path is introduced. | analyst-authored YAML spec (non-sensitive; local) |
| `report.add(...)` call sites ↔ generated `references/finding-codes.md` | Documentation-of-enforcement boundary; kept honest by `scripts/gen-finding-catalogue.py` and its `--check` gate (regeneration, never hand-edit). The ten new codes are added to `_D05_ALLOWLIST_CODES` by exact name. | generated catalogue text |
| `references/test-selection.md` ↔ `dsx/checks/stats.py` routing table | Doc/code agreement surface; the seven `recommend_*` routings, the DEPRECATED routing-off rows (Yates / SNK / unprotected-LSD-k>3), the log-linear pointer row and the Fisher-Freeman-Halton footnote are mirrored in the doc in the same commit as the code (D-08 lockstep). Wave 1 keeps the catalogue at 265; Wave 2 mints the ten codes → 275. | routing-doctrine text |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-19-A-01 | Tampering | a closed-vocabulary recognition guard implemented as substring/fuzzy match, letting an adjacent value pass | low | mitigate | The six new scalar fields join `_MEMBERSHIP_FIELDS`, which uses exact `normalize(value)`-not-in-vocab equality only (no fuzzy/prefix match); the no-autoswitch routing modules assert the acceptable members. Re-run green in the 69-test Phase-19 gate+routing suite | closed |
| T-19-A-02 | Tampering (of the routing contract) | a `recommend_*` function silently returning a DEPRECATED procedure (Yates/SNK/unprotected-LSD/Vuong) as an acceptable default | low | mitigate | The acceptable SETs exclude every deprecated procedure by construction; the no-autoswitch modules assert `recommend_posthoc` never returns `snk` and `recommend_proportion_ci` never returns `wald`. `test_declared_rm_trend_routing` + `test_declared_resampling_posthoc_routing` re-run green | closed |
| T-19-A-03 | Tampering (data-then-pick) | a `recommend_*` function gaining a data/n/distribution parameter, reintroducing two-stage selection | low | mitigate | `inspect.signature` structural assertions in the two routing modules fail red on any data/n/distribution parameter (REQ-P18-06 anti-two-stage doctrine); a signature-inspecting test cannot silently rot. Re-run green | closed |
| T-19-A-04 | Tampering (false authority) | a fabricated numeric locator/boundary for a D-07 not-in-hand item printed into `test-selection.md` | low | mitigate | Every catalog-only / not-in-hand item ships as a named row with explicit confirm-at-source language and NO numeric boundary (Greenhouse-Geisser ε, Hamed-Rao lag, Davidson-MacKinnon B, Brown-Cai-DasGupta n, Campbell expected-count, Hayter α, McCullagh-Nelder §6.2). Confirmed in `references/test-selection.md` and `19-VERIFICATION.md` | closed |
| T-19-A-05 | Tampering (docs drift from behaviour) | `test-selection.md` rows drifting from the `recommend_*` acceptable sets | low | mitigate | Rows and `recommend_*` land in the same commit (doc/code lockstep, standing v2.3 rule); `finding-codes.md` regen (`--check`) confirms the catalogue stayed **265** at Wave 1. Re-run exit 0 | closed |
| T-19-C-01 | Repudiation | a new code ships uncited because the `DSX-STA-` family prefix is not in the D-05 allowlist | **high** | mitigate | All **ten** codes added by **exact name** to `_D05_ALLOWLIST_CODES`; `scripts/gen-finding-catalogue.py --check` enforces the `Citation:`/`Structural criterion:`/`# D-05` marker discipline per code — re-run **exit 0** ("finding catalogue is current") at Total **275**, ten codes each present once | closed |
| T-19-C-02 | Tampering (citation laundering) | a monolithic gate emitting all ten codes under one shared docstring, satisfying the D-05 gate while seven distinct citation obligations go unmet | **high** | mitigate | **Seven per-family helpers** (`_check_declared_rm_sphericity`/`_trend`/`_resampling`/`_posthoc`/`_variance_role`/`_power_reporting`/`_proportion_count`, stats.py:1078–1308), each with its own attributable `Citation:` docstring bound by `_resolve_docstrings` to its enclosing function; the `--check` per-code marker gate re-run exit 0 confirms every code resolves a distinct citation. Seven helpers + dispatcher confirmed present | closed |
| T-19-C-03 | Tampering | a closed-vocabulary gate implemented as substring/fuzzy match, or DSX-STA-081 written as membership instead of `is_blank` (false-blocking a declared `none`) | medium | mitigate | Exact `normalize(value)` equality/membership only; DSX-STA-081 keys on `is_blank` (Pitfall 5), proven silent on a declared `none`/`independent` by `test_trend_gate` (`is_blank(0)`/`(0.0)` = False adversarially cleared in 19-REVIEW). Re-run green | closed |
| T-19-C-04 | Tampering (over-block) | DSX-STA-070 firing on repeated-measures presence, or DSX-STA-110 firing on Levene presence without a role read, false-blocking a legitimate route | medium | mitigate | 070 keys on the declared two-stage token only; 110 keys on the declared role (`scale_estimand` exempt); both over-block guards asserted by `test_rm_sphericity_gate` / `test_variance_role_gate`. Re-run green | closed |
| T-19-C-05 | Tampering (docs drift from behaviour) | regenerated `finding-codes.md` committed out of sync with the ten `report.add` sites, or a stale invariant total | medium | mitigate | `finding-codes.md` regenerated via `--write` in the same commit as the `report.add` sites; the invariant triple moves as a set (265→275, +10, snapshot frozen 256); `--check` is the drift gate — re-run exit 0, `test_finding_catalogue_invariant` green at 275 | closed |
| T-19-C-06 | Tampering (false authority) | a fabricated numeric locator/boundary for a D-07 not-in-hand item printed into a gate docstring or a doc entry | low | mitigate | Gates check declared-field **PRESENCE only**; no numeric ships (Hamed-Rao lag, Brown-Cai-DasGupta n≤40, Campbell expected-count, McCullagh-Nelder §6.2, Hayter α, Greenhouse-Geisser ε, Davidson-MacKinnon B); catalog-only dispositions carry explicit not-in-hand language | closed |
| T-19-C-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (`unittest`, `ast`, `re`). No Package Legitimacy Audit owed. See Accepted Risks. | closed |

*Status: open · closed — below `high` threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-19-01 | T-19-C-SC | Supply-chain (dependency-confusion / malicious install) is inapplicable: Phase 19 installs **zero** packages — Python stdlib `unittest`/`ast`/`re` only, on the confirmed local python3 3.14.6. No package-legitimacy audit is owed. Low severity, below the `high` block threshold. | Phase 19 plan threat registers (persona round, S3-1/S3-2); operator approval pending (HUMAN-QUEUE HQ-23) | 2026-09-02 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-02 | 12 | 12 | 0 | orchestrator (secure-phase, State B, ASVS L1; **every non-accepted mitigation re-run green from a clean tree** — full suite **1442 OK** + 69 targeted Phase-19 gate/routing tests + `test_finding_catalogue_invariant` at 275 + `gen-finding-catalogue.py --check` exit 0 at 275 (ten codes each once) + golden ship-set/known-bad-corpus 51 OK proving bad fires all ten / good silent + the two HIGH mitigations confirmed structurally: seven per-family helpers at stats.py:1078–1308 and ten codes in `_D05_ALLOWLIST_CODES`) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed (both HIGH threats CLOSED with re-run evidence)
- [x] `status: verified` set in frontmatter (threat register verified by the orchestrator)

**Approval:** threat register verified 2026-09-02 (orchestrator, threats_open:0; the two HIGH threats re-run green, not trusted from the plan register). **Operator security sign-off PENDING — batched to HUMAN-QUEUE HQ-23, non-blocking until close-out S5-2 per LOOP-LEDGER S3-5.** The loop prepared and verified this register; the outward-facing security approval line is a human read (brief §4 item 4) and is not self-signed.
