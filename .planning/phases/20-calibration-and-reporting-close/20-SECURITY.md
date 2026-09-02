---
phase: 20
slug: calibration-and-reporting-close
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on (high) severity
threats_open: 0
asvs_level: 1
created: 2026-09-02
---

# Phase 20 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register origin: `register_authored_at_plan_time: true` (all four PLAN files — 20-A, 20-B,
> 20-C, 20-D — carried a parseable `<threat_model>` block). ASVS L1, `security_block_on: high`.
> **Phase 20 carries five HIGH threats** (T-20-A-01, T-20-A-02, T-20-B-01, T-20-D-01, T-20-D-02)
> — all self-reference / drift / false-pass tampering risks in a calibration-and-reporting close
> whose only surface is test/fixture code (production is byte-frozen). Every non-accepted
> mitigation was **re-run green by the orchestrator from a clean tree** (brief §5 "re-run,
> don't trust"), so the L1 short-circuit was taken with evidence rather than on faith.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| analyst-authored `ANALYSIS-SPEC.yaml` → dsx loader → `dsx/checks/stats.py` check | Phase 20 mints **zero** codes and adds **no** data path: it adds five PRESENT known-bad fixtures (declared correlation/agreement strings only), three valid good-corpus controls, and read-only calibration / cross-check / structural-guard test assertions over the fifteen Phase-18/19 codes. No value is read or computed, no I/O / auth / subprocess / new file-write path is introduced. Production `dsx/`, `scripts/`, `references/` are **byte-frozen** since the Phase-20 execute start (`git diff 0013ea3..HEAD -- dsx scripts references` empty). | analyst-authored YAML fixtures (non-sensitive; local) |
| the HIGH-tier catch declaration ↔ the live gate measurement (self-reference, D-09) | The load-bearing boundary: the HIGH verify/ship catch rate must be measured **live** from `self._gate_findings` filtered to HIGH, **never** lifted from the golden ledger `_GOLDEN_SHIP_FINDINGS` (which already records which of the fifteen fire — reading it as "what fired" is a tautological catch rate). | measured gate findings (in-test) |
| `report.add(...)` call sites ↔ generated `references/finding-codes.md` | Zero new `report.add` sites this phase; the `--check` gate + no-op regen + byte-frozen Phase-12 (256) snapshot + total exactly 275 is the boundary control (the D-01 zero-mint invariant). The fifteen codes are in `_D05_ALLOWLIST_CODES` by **exact string** (`DSX-STA-` is not an allowlisted prefix). | generated catalogue text |
| `references/test-selection.md` prose ↔ the routing engines (`recommend_test` / `recommend_*`) | The doc mirror must not drift from the engine (the Boschloo divergence class); the read-only `tests/test_doc_code_agreement.py` cross-check is the boundary control — strict cell-equality of the 15 decision rows + honest set-membership of the six mirror tables + a visible skip-list + an exhaustiveness net (no silent unparse), failing red at build/CI time. | routing-doctrine text |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-20-A-01 | Tampering (self-reference) | the HIGH stratum reading `_GOLDEN_SHIP_FINDINGS` (which already lists which of the fifteen fire) as "what fired" — a tautological catch rate | **high** | mitigate | The stratum derives its catch only from live `self._gate_findings` filtered to HIGH; `_GOLDEN_SHIP_FINDINGS` appears in `test_known_bad_corpus.py` only in prose comments documenting it is deliberately NOT read (lines 489, 729, 1576), never as an executable read in the HIGH readout (D-09). Re-run green in the 77-test Phase-20 suite | closed |
| T-20-A-02 | Tampering (null result wearing a coverage star) | reporting a re-run of the CRITICAL-only harness as "re-baselined to cover the fifteen" when it is provably invariant to them | **high** | mitigate | `_classify_target_defect` is severity-parameterised (default CRITICAL, every existing call byte-identical); the load-bearing HIGH verify/ship stratum (D-03) measures the fifteen where they actually fire as a separate, non-empty third readout beside the CRITICAL pair. `test_high_stratum_target_codes_fire_and_are_named` asserts each DSX-STA-05x fires live at verify/ship and is POSTMORTEM-named. Re-run green | closed |
| T-20-A-03 | Tampering (headline drift) | folding the HIGH catch into `_headline`, moving the (miss-rate, FPR) pair or the anchor/floor | medium | mitigate | The HIGH catch is reported BESIDE the pair; `_headline((2,5),(1,4),(3,10))==(0.25,0.3)` and `_ABSENT_PARTITION_FLOOR==3` are re-asserted unmoved and the pair is proven invariant to the stratum's presence (D-06). Re-run green | closed |
| T-20-A-04 | Tampering (false negative control) | a good-corpus control that never reaches a DSX-STA-05x branch (silent-not-clean) or a real false positive laundered as tempdir noise | medium | mitigate | Each of the three controls declares the VALID form that reaches its branch and stays silent (`frozenset()`); `test_fpr_noise_allowlist_is_disjoint_from_the_dsx_sta_family` structurally forbids a DSX-STA code in `_FPR_TEMPDIR_NOISE_CODES`; FPR denominator grew 12→15 (≥10 floor) (D-05). Re-run green | closed |
| T-20-A-05 | Tampering (spurious catch) | a new fixture firing DSX-STA-041 or a second Phase-18 code, misattributing the catch | low | mitigate | Each fixture omits `analysis.outcome_type` (no DSX-STA-041) and `inference.primary_procedure` (admissibility resolves `not_declared`, no spurious DSX-ADM/PRE/NAR) and declares only its one trigger; the audit asserts exactly one of the fifteen fires per fixture (clean singletons {050/051/060/061/062}). Re-run green | closed |
| T-20-A-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (`unittest`, `json`, `tempfile`, `pathlib`). No Package Legitimacy Audit owed. See Accepted Risks | closed |
| T-20-B-01 | Tampering (silent mint) | a `report.add` site or catalogue drift slipping into the terminal phase, moving the total off 275 | **high** | mitigate | `gen-finding-catalogue.py --check` green ("finding catalogue is current") at **275**; `test_phase20_zero_mint_close.py` asserts 275, the byte-frozen 256 Phase-12 snapshot, and the absent 123-onward reserve band (max code 122) — a mint would fail all three; production byte-frozen (`git diff 0013ea3..HEAD -- dsx scripts references` empty). Re-run green | closed |
| T-20-B-02 | Tampering (good fixture no longer silent) | the extension firing a new code or changing the finding set, breaking the negative-control guarantee | medium | mitigate | The good fixture is EXTENDED not replaced (D-08) with silent in-vocab new-family fields (`sphericity_correction: unconditional_gg` → DSX-STA-070 silent; `power_reporting_type: a_priori` → DSX-STA-111 silent; both in-vocab → DSX-STA-040 silent); the Task-1 gate asserts none of the fifteen fire and the four-code golden baseline is preserved (`test_causal_verb_golden` 6/6). Re-run green | closed |
| T-20-B-03 | Tampering (snapshot mutation) | the frozen Phase-12 snapshot being edited to absorb a change | medium | mitigate | `test_phase20_zero_mint_close.py` asserts `tests/fixtures/finding-codes-phase12.md` declares 256 and its code-set is a subset of the catalogue; the plan never edits it. Re-run green | closed |
| T-20-B-04 | Repudiation (uncited code laundered) | a milestone code missing from `_D05_ALLOWLIST_CODES`, shipping uncited under the non-allowlisted `DSX-STA-` prefix | low | mitigate | All fifteen (050/051/060/061/062/070/080/081/090/100/110/111/120/121/122) are in `_D05_ALLOWLIST_CODES` by **exact string** (structurally confirmed this audit) and `DSX-STA-` is not an allowlisted prefix. Re-run green | closed |
| T-20-B-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (`unittest`, `re`, `pathlib`, `importlib`). No Package Legitimacy Audit owed. See Accepted Risks | closed |
| T-20-C-01 | Tampering (data-then-pick) | a new-category `recommend_*` gaining a data/n/distribution parameter, reintroducing two-stage selection | low | mitigate | The dynamic `inspect.signature` enumeration fails red on any banned parameter across every `recommend_*` except `recommend_test` (REQ-P18-06 doctrine, category-complete). Re-run green | closed |
| T-20-C-02 | Tampering (silent scope loss) | the enumeration silently emptying (rename/refactor) so the proof passes vacuously | low | mitigate | The anti-vacuity assertion requires the enumerated set to be a superset of the eight known new-category names and to include `recommend_test`. Re-run green | closed |
| T-20-C-03 | Tampering (fallthrough displacement) | a new outcome branch appended after log_rank, or a new decision-table row after the time-to-event row, silently rerouting `time_to_event` | low | mitigate | Terminal-position assertions on both the code side (last `return _rec(` is log_rank) and the doc side (final decision-table outcome row is time-to-event). Re-run green | closed |
| T-20-C-04 | Tampering (normality autoswitch returns) | a normality-test CALL creeping onto the gate/skill decision surface | low | mitigate | The existing `DecisionSurfaceScanTest` over `dsx/` and `skills/` is preserved and re-run green (no `scipy.stats`/`shapiro`/`normaltest`/`anderson`/`kstest` call). Re-run green | closed |
| T-20-C-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (`unittest`, `inspect`, `re`, `pathlib`). No Package Legitimacy Audit owed. See Accepted Risks | closed |
| T-20-D-01 | Tampering (docs drift from behaviour) | a decision-table cell drifting from `recommend_test` (the Boschloo divergence class) | **high** | mitigate | Tier-1 strict cell-equality binds all 15 rows to `recommend_test` and asserts the Boschloo fallback in `['alternatives']`; a deliberately-wrong primary (welch_t vs engine welch_anova) FAILS the assertion (negative control confirms it is not a lenient pass). Doc/code repaired in lockstep in the same commit if surfaced (standing v2.3 rule) — none surfaced, both byte-frozen. Re-run green | closed |
| T-20-D-02 | Tampering (false pass) | the cross-check passing because a row silently failed to parse | **high** | mitigate | The 15-row anti-vacuity assertion (Tier 1) and the exhaustiveness net (all 57 pipe-delimited data rows accounted: 31 bound + 26 skip-listed, `bound==31`) make an unparsed row a hard failure. Re-run green | closed |
| T-20-D-03 | Tampering (over-strong claim) | asserting single-cell equality on a legitimately set-valued mirror table, over-blocking a valid Spearman-vs-Kendall choice | medium | mitigate | Tier 2 uses honest set-MEMBERSHIP against the engine's acceptable set — the same semantics the runtime gates use — never equality. Re-run green | closed |
| T-20-D-04 | Tampering (false authority) | a lenient normaliser mapping an unrelated doc token to a code token, masking a divergence | low | mitigate | Explicit enumerated normalisation maps (Groups/Paired/Distribution/Test-label); an unmapped token raises rather than silently passing. Re-run green | closed |
| T-20-D-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (`unittest`, `re`, `pathlib`). No Package Legitimacy Audit owed. See Accepted Risks | closed |

*Status: open · closed — below `high` threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-20-01 | T-20-A-SC / T-20-B-SC / T-20-C-SC / T-20-D-SC | Supply-chain (dependency-confusion / malicious install) is inapplicable: Phase 20 installs **zero** packages — Python stdlib `unittest`/`json`/`tempfile`/`pathlib`/`re`/`inspect`/`importlib` only, on the confirmed local Python 3.12.10. No package-legitimacy audit is owed. Low severity, below the `high` block threshold. | Phase 20 plan threat registers (persona round, S4-1/S4-2); operator approval pending (HUMAN-QUEUE HQ-25) | 2026-09-02 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-02 | 21 | 21 | 0 | orchestrator (secure-phase, State B, ASVS L1; **every non-accepted mitigation re-run green from a clean tree** — full suite **1462 OK** + 77 targeted Phase-20 tests (`test_known_bad_corpus` calibration harness + HIGH stratum, `test_causal_verb_golden`, `test_phase20_zero_mint_close`, `test_doc_code_agreement`, `test_no_shapiro_autoswitch`, `test_time_to_event_fallthrough`) + `gen-finding-catalogue.py --check` "current" at **275** + production byte-frozen (`git diff 0013ea3..HEAD -- dsx scripts references` empty) + the five HIGH mitigations confirmed structurally: HIGH catch via live `_gate_findings` never `_GOLDEN_SHIP_FINDINGS` (D-09), catalogue 275 + 256 snapshot frozen, fifteen codes in `_D05_ALLOWLIST_CODES` by exact string, doc/code cross-check `bound==31` exhaustiveness) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed (all five HIGH threats CLOSED with re-run evidence)
- [x] `status: verified` set in frontmatter (threat register verified by the orchestrator)

**Approval:** threat register verified 2026-09-02 (orchestrator, threats_open:0; all five HIGH threats re-run green, not trusted from the plan register). **Operator security sign-off PENDING — batched to HUMAN-QUEUE HQ-25, non-blocking until close-out S5-2 per LOOP-LEDGER S4-5.** The loop prepared and verified this register; the outward-facing security approval line is a human read (brief §4 item 4) and is not self-signed.
