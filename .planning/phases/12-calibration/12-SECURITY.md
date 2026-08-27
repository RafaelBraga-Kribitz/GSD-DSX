---
phase: 12
slug: calibration
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
status: verified
threats_open: 0
asvs_level: 1
register_authored_at_plan_time: true
created: 2026-08-27
---

# Phase 12 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Terminal calibration/measurement phase — mints ZERO finding codes (D-18); no product-code
> surface added beyond a read-only `dsx stats --paradigm` reader plus corpus/test data.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| fixture author → harness | Hand-authored `<slug>-ATTRIBUTION.yaml` sidecars and postmortem prose become machine-countable §6.5 evidence | attribution tags, absent-code claims |
| on-disk `DECISIONS.jsonl` trails → reported split | Any trail `dsx stats --paradigm` reads becomes measured operator history | frame paradigm records |
| CLI flag surface → gate semantics | A block flag on an always-pass reader would be a lie in help text | argparse contract |
| corpus composition → headline number | A present-heavy corpus could inflate a single catch-rate to ~100% for free | measured miss-rate/FPR |
| own-target map ↔ friction | Relabelling a code incidental→own shrinks reported over-blocking without fixing it | friction RAW/NET |
| measured numbers → backlog disposition | A disposition not grounded in the measured number is narrative judgement, the thing §6.5 replaces | §6.5 carry/remove |
| reversal record → project decision log | A laundered reversal corrupts the discipline that makes "here is what would change it" honest | REV-002 |

---

## Threat Register

Consolidated from all seven plans' `<threat_model>` blocks (`register_authored_at_plan_time: true`),
deduped by `threat_id` (T-12-01 severity taken as the max across plans = high). ASVS L1, block_on `high`.
Verified SECURED by `gsd-security-auditor` (opus) and independently re-gated by the orchestrator (§5) — see audit trail.

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-12-01 | Tampering | golden / lifted-or-stale number | high | mitigate | Calibration numbers computed live via `_gate_findings` + `_classify_target_defect`; golden `_GOLDEN_SHIP_FINDINGS` measured via fresh-tempdir `_ship_findings` (`tests/test_causal_verb_golden.py:217,262`); `_INCIDENTAL_GAP_CODES`/`_GOLDEN_SHIP_FINDINGS` ledgers explicitly NOT read as source (`tests/test_known_bad_corpus.py:1444-1445,1504-1506,1632`) | closed |
| T-12-02 | Tampering | coverage predicate / manufacturing a case | high | mitigate | `test_corpus_includes_full_coverage_classes` (`tests/test_known_bad_corpus.py:862`) asserts class-PRESENCE over glob-discovered slugs, no hardcoded slug list / no count; D-02 source-before-count | closed |
| T-12-03 | Tampering | `cmd_stats` source selection | high | mitigate | D-13 hard-exclude of `examples`/`templates` by resolved+case-folded path COMPONENT (`dsx/cli.py:670-672` `trail.resolve().parts`, CR-01 absolute, fails SAFE); pinned by `test_never_sources_the_known_bad_floor`, `test_root_pointed_at_the_floor_still_excludes_it`, `test_excluded_component_match_is_case_folded` (`tests/test_cli_stats.py`) | closed |
| T-12-03b | Tampering | raw-record inflation | high | mitigate | Dedup by distinct `frame_digest` (`dsx/decisions.py:120`; `dsx/cli.py:709-745`); `test_dedup_is_by_distinct_frame_digest` asserts Bayesian share = 1/(N+1) | closed |
| T-12-04 | Tampering | incidental→own relabel to shrink friction | high | mitigate | `test_target_defect_codes_fire_and_are_named` (`:1689`): every `_TARGET_DEFECT_CODES` entry fires blocking-at-threshold live AND is named in the fixture's postmortem/attribution | closed |
| T-12-05 | Repudiation | miss/caught laundering | high | mitigate | `test_attribution_tags_are_falsifiable_against_live_gate` (`:1438`): `kind="miss"` absent_code fires NOWHERE CRITICAL across all four gate points; hypothetical codes never credited | closed |
| T-12-06 | Repudiation | REV-002 laundering the determinism doctrine as new evidence | high | mitigate | `.planning/REVERSALS.md:82-106` — REV-002 "New evidence" = the systematic REQ-P12-05 re-evaluation event, explicitly NOT the D-01/D-02 doctrine restated; SELF-001-safe (D-17) | closed |
| T-12-07 | Tampering | sidecar naming a hallucinated/misspelled code | high | mitigate | `test_attribution_sidecars_reference_valid_codes_and_items` (`:1363`): `absent_code ∈ catalogue ∪ §6.5-backlog` validated at schema time before any live check; backlog disjoint from catalogue | closed |
| T-12-08 | Elevation of Privilege | `cmd_stats` masquerading as a gate | medium | mitigate | Readout `cmd_stats` (`dsx/cli.py:678`) returns 0 by construction; `p_stats` (`:1009-1026`) omits `add_common` so carries no `--block-on`; NOT registered in CHECKS/GATE_PROFILES (`:1017` comment; the `"stats"` key there is the separate statistical `stats.check`, not this reader); `test_block_on_flag_is_rejected` (argparse exit 2), `test_always_exits_zero` | closed |
| T-12-09 | Tampering | FPR denominator honesty / noise inflation | high | mitigate | Tempdir-noise codes `_FPR_TEMPDIR_NOISE_CODES` (DQ-001/CLM-031/FIG-001/NAR-010, `tests/test_known_bad_corpus.py:658-663`) excluded from FPR; `test_false_positive_findings_excludes_documented_tempdir_noise` | closed |
| T-12-10 | Tampering | control spec authenticity | medium | mitigate | Each good-corpus control spec passes `dsx validate` with no CRITICAL/HIGH on its own merits; golden good-corpus sets all `frozenset()` (`tests/test_causal_verb_golden.py:117-128`); 12 clean specs on disk | closed |
| T-12-11 | Tampering | headline gaming via easy catches | high | mitigate | Headline = (miss-rate, FPR) with floored ABSENT partition `_ABSENT_PARTITION_FLOOR=3` + synthetic + live invariance (`test_headline_is_invariant_to_adding_a_target_present_case`) | closed |
| T-12-12 | Tampering | silent code mint breaking D-18 | high | mitigate | `test_finding_catalogue_stays_at_256_codes` (declared + enumerated both = 256) + `scripts/gen-finding-catalogue.py --check`; `references/finding-codes.md:16` "Total: 256 codes"; GATE_PROFILES/CHECKS unchanged | closed |
| T-12-13 | Tampering | item-6 row softened/deleted rather than relocated | high | mitigate | `test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker` (`:1284`) keeps 3 pinned substrings after relocation to §6.5 "Removed / permanently out of scope (D-14)" | closed |
| T-12-SC | Tampering | npm/pip/cargo installs | low | accept | Zero new third-party packages this phase (D-01 hermeticity); `git diff 297bdd2 HEAD` over pyproject/setup/requirements/Pipfile/poetry.lock empty — no install surface | closed — accepted-risk (AR-12-SC) |

*Status: open · closed · open — below `high` threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` (high) count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

**Count:** 15 distinct threats — 14 mitigate (all CLOSED, mitigation present at file:line + pinned test) + 1 accept (T-12-SC, CLOSED via accepted-risk). **threats_open: 0.**

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-12-SC | T-12-SC | Phase 12 introduces zero new third-party packages (D-01 hermeticity; 12-RESEARCH Package Legitimacy Audit). No install surface, so no supply-chain attack surface to mitigate. Design-time plan decision, not a fresh redisposition. | Persona round (S3-1, Auditor `dsx-ml-integrity-auditor`), pending human sign-off (HQ-6) | 2026-08-27 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-27 | 15 | 15 | 0 | `gsd-security-auditor` (opus) verdict SECURED; orchestrator independently re-gated the HIGH blockers (§5) |

**Independent re-gate evidence (orchestrator, never trusted the subagent — brief §5):**
- T-12-03: `dsx/cli.py:670-672` `excluded = {"examples","templates"}` matched against `{part.lower() for part in trail.resolve().parts}` (resolved + case-folded, CR-01 hardened absolute, fails SAFE) — read first-hand.
- T-12-03b: `dsx/decisions.py:120` `frame_digest` grouping anchor — read first-hand; `test_dedup_is_by_distinct_frame_digest` green.
- T-12-08: `dsx/cli.py:1013-1017` comment + `p_stats` deliberately omits `add_common`; the `"stats"` in CHECKS (`:67`) / GATE_PROFILES (`:122,127`) is the pre-existing `stats.check`, a distinct component — read first-hand; `test_block_on_flag_is_rejected`/`test_always_exits_zero` green.
- T-12-12/D-18: `references/finding-codes.md:16` "Total: 256 codes" — read first-hand; catalogue-invariant test green + `check.sh` catalogue current.
- T-12-06: `.planning/REVERSALS.md:82` REV-002 (D-14) + SELF-001 convention `:40-49` — read first-hand.
- Requirement/mitigation pin tests: 52 green in the three requirement modules; full suite `Ran 1221 tests … OK`; `bash scripts/check.sh` → all checks passed.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer) — 14 mitigate + 1 accept
- [x] Accepted risks documented in Accepted Risks Log (AR-12-SC)
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-08-27 (technical gate). Per brief §4 category 4 the **human phase security sign-off line** is owed at the Phase-12 UAT/ship round (HQ-6) — non-blocking for downstream gates; the AR-12-SC accept disposition is also in that veto window. Answer e.g. `HQ-6 security: approved`.
