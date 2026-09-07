---
phase: 26
slug: per-skill-read-contracts
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
security_block_on: high
register_authored_at_plan_time: true
created: 2026-09-07
---

# Phase 26 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register built from the four PLAN `<threat_model>` blocks (26-01…26-04);
> every mitigation re-verified against the implementation by the orchestrator
> (loop S2-5, ASVS L1 grep-depth) — not trusted from a subagent report.
> Phase 26 is skill-only: `dsx/` byte-identical, zero new codes, one off-gate-path
> static repo-integrity test; the attack surface is drift and false read contracts,
> not runtime input handling.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| template key set → skill read step | A skill's `<inputs>` block names an `EDA.md`/`DATA-PROFILE.yaml` key; if the key is not a real template key the read step silently orphans. Enforced by the off-gate-path guard, not at edit time. | backtick-wrapped key strings |
| repo-committed files → static guard | The guard's only input is the repo's own committed templates and skills, resolved via `Path(__file__).resolve().parents[1]` — no user path, no network, no untrusted bytes (same trust model as every existing `tests/` repo-integrity test). | repo file bytes |
| line-ending convention → line split | `EDA.md` is CRLF, `DATA-PROFILE.yaml` is bare-LF; a wrong split silently yields an empty key set (vacuous pass). | template line bytes |
| skill prose → prose-only reference | The joins matrix (define-metrics) and the wide-categorical policy recommendation (build-model) are EDA prose, not front-matter keys; naming either as a backtick key would create a false read contract. | Also-consult prose line |
| repo `skills/` → host overlay (install.mjs) | Installer copies the five edited skills into the runtime overlay; the only concern is drift between repo and installed copy, adjudicated by `--check`. | source file bytes |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-26-01 | Tampering (vacuous pass) | `parse_eda_keys` / `parse_profile_keys` line splitting | high | mitigate | Split on `\r?\n` so both CRLF and bare-LF templates parse; anti-vacuity anchors (`len(eda) >= 30`, `columns[].null_rate` present only after the uncomment step, DATA-PROFILE non-empty) fail immediately on a mis-split empty parse. `test_anchor_non_vacuity` + `test_parse_is_deterministic_and_order_independent` green. | closed |
| T-26-02 | Tampering (orphaned read key) | `<inputs>` blocks + key-set membership matcher | high | mitigate | Full dotted-path set-membership fails loudly (skill+region+key) when a named key is absent; the negative control proves discrimination. `test_skill_keys_are_members_of_live_templates` + `test_negative_control_orphan_key_is_rejected` green; the code review's exhaustive leaf+parent+placeholder rename probe confirmed every rename leaves zero surviving referenced keys. | closed |
| T-26-03 | Tampering (silent drift) | installed overlay vs repo (`install.mjs`) | medium | mitigate | `node install.mjs` re-sync THEN `node install.mjs --check` (never `--check` alone; the v2.5.0 real gate) → self-test **passed** (5 gates, 6/6 agents, 14/14 skills); the five edited skills are among the synced skills. | closed |
| T-26-04 | Tampering (scope creep) | `dsx/`, `templates/`, finding catalogue | high | mitigate | `git diff --stat 818fb7c..HEAD -- dsx/ templates/` **empty** (byte-identical for the phase); `scripts/gen-finding-catalogue.py --check` → "finding catalogue is current"; `tests/test_finding_catalogue_invariant.py` green; catalogue **276 → 276** (276 rows counted). Zero new codes. | closed |
| T-26-05 | Tampering (leaf collision) | intermediate map-header dotted-path matching | medium | mitigate | Leaf-only matching rejected (D-26-04); the parser records every intermediate dotted path and matches full paths, so a parent rename cannot be masked by a same-named leaf elsewhere (`overall` under both `base_rate` and `target`; five `verdict` leaves). Covered by the membership + negative-control tests. | closed |
| T-26-06 | Tampering (false read contract) | Also-consult prose line | medium | mitigate | The joins-matrix / policy-recommendation references are written as zero-backtick prose; `test_also_consult_line_has_zero_backticks` asserts zero backticks on the Also-consult line in `dsx-define-metrics` and `dsx-build-model`, so prose can never be mistaken for a machine-parsed key. | closed |
| T-26-07 | Tampering (regression) | full test suite on the real interpreter | medium | mitigate | `python -m unittest discover -s tests -q` on real Python **3.12.10** (not the `python3` stub) → **Ran 1590 tests, OK**; the two `explain` tests did not false-fail (clean tree); the guard is included. | closed |
| T-26-SC | Tampering (supply chain) | package installs | low | accept | Zero external packages introduced this phase; the guard imports stdlib only (`re`/`unittest`/`pathlib`/`__future__`) with no `import yaml`, and `node install.mjs` runs the existing unmodified installer against repo-local content only — no npm/pip/cargo install surface for a legitimacy gate to run against. | closed |

*Status: open · closed — below the high threshold is non-blocking*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-26-01 | T-26-SC | Phase introduces zero external packages; the guard is stdlib-only (no `import yaml`) and the installer copies existing repo files only, no registry fetch — there is no install surface for a legitimacy gate to run against. | loop orchestrator (re-gate); operator sign-off batched to HUMAN-QUEUE (S7-2) | 2026-09-07 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-07 | 8 | 8 | 0 | orchestrator (loop S2-5, ASVS L1 grep-depth re-gate) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-09-07 — gate **SECURED**, `threats_open: 0`, 8/8 threats CLOSED by orchestrator re-gate on real Python 3.12.10. Register authored at plan time + ASVS L1 → the auditor short-circuit applies (L1 grep-depth sufficient); each mitigation was re-confirmed against the implementation and re-run this firing (guard 7 OK, catalogue invariant 2 OK + `--check` current, full suite 1590 OK, `install.mjs --check` self-test passed, `dsx/`+`templates/` diff empty) rather than trusted from a report. **Human sign-off + UAT batched to HUMAN-QUEUE as HQ-42 (non-blocking until S7-2 per LOOP-LEDGER S2-5)** — the loop verifies the threat mitigations but does not sign the approval line (brief §4.4).
