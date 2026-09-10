---
phase: 27
slug: evidence-case-feature-origin-only-leak
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
security_block_on: high
register_authored_at_plan_time: true
created: 2026-09-07
---

# Phase 27 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register built from the two PLAN `<threat_model>` blocks (27-01 mint, 27-02
> fixture + harness); every mitigation re-verified against the implementation by the
> orchestrator (loop S3-5, ASVS L1 grep-depth) on real Python 3.12.10 — not trusted
> from a subagent report.
> Phase 27 mints one code (`DSX-ML-034`, feature provenance) under a
> secondary-corroborated D-05 citation and promotes a corpus MISS fixture. The attack
> surface is provenance laundering (over-claiming a paywalled read), catalogue/count
> tampering, and a fixture that silently flips MISS→CATCH — not general runtime input
> handling. `dsx/checks/dq.py` stays byte-frozen (profiler-is-a-producer rule).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| minted code → finding catalogue | A new `report.add` call-site becomes a catalogue row via AST extraction; a non-deterministic or over-claiming emission corrupts the committed catalogue. | `report.add` code/severity |
| docstring / `# D-05:` marker → provenance record | The Citation text is the durable provenance claim; over-claiming a first-hand read launders a paywalled source into an asserted read. | citation prose |
| promoted fixture → corpus harness | A fixture that silently gains a `feature_provenance` block converts the MISS into a CATCH and defeats the requirement's whole point (`kind: miss`). | ANALYSIS-SPEC bytes |
| ATTRIBUTION sidecar → §6.5 backlog id set | An id that does not match the frozen `_SECTION_65_ITEM_IDS` fails the sidecar gate; a shipped `absent_code` placed in the backlog set fails the disjointness gate. | sidecar id strings |
| source tree → installed overlay | An un-synced overlay means the shipped package disagrees with the repo; `install --check` is the boundary check. | source file bytes |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-27-01 | Tampering (MISS→CATCH) | promoted ANALYSIS-SPEC | high | mitigate | Fixture declares **no** `model.feature_provenance` block (`grep -c feature_provenance` = **0**); `dsx validate` → **PASS, CRITICAL=0** (leak stays invisible = an honest miss); the falsifiability + golden-set tests re-measure the ship set and flip if a block is added. | closed |
| T-27-02a | Tampering (count pin) | catalogue count pins | high | mitigate | `references/finding-codes.md` **Total: 277**; `_EXPECTED_TOTAL = 277` (invariant test); phase-20 pin **277**. Moved in lockstep; drift red-fails the invariant + phase-20 tests. | closed |
| T-27-02b | Tampering (spec-count pin) | `tests/test_dsx.py` spec count | high | mitigate | `self.assertEqual(len(paths), 43, …)` (test_dsx.py:583) — moved 42→43 exactly when the fixture landed; count assert red-fails on drift. | closed |
| T-27-03 | Repudiation (provenance laundering) | `DSX-ML-034` docstring + `# D-05:` marker | high | mitigate | Docstring (`ml.py:551`) + marker (`tests/test_ml_feature_provenance.py:9`) state Kaufman/Rosset/Perlich/Stitelman (2012) TKDD 6(4) Art.15 is **secondary-corroborated, primary ACM PDF paywalled**; no first-hand read claim (grep for a read assertion = **0**), no invented page/section locator. **Update 2026-09-10 (interactive close-out):** the primary ACM PDF was obtained (operator-supplied) and read first-hand by the interactive session; the docstring and marker now record the read with locators (Sec. 3.1 p. 15:8; Sec. 3.2 eq. (3) p. 15:9), each verified against the PDF text at the source. The threat's shape inverts from "must not over-claim a read" to "the asserted locators must be verifiable" — they are. | closed |
| T-27-04 | Tampering (non-determinism) | catalogue regeneration (one code, two severities) | high | mitigate | `gen-finding-catalogue.py --check` → exit 0, "finding catalogue is current"; **exactly one** `DSX-ML-034` row, rendered **CRITICAL** (finding-codes.md:163); source order arranged so CRITICAL wins the dedupe. | closed |
| T-27-06 | Tampering (backlog leak) | `_SECTION_65_BACKLOG_CODES` | high | mitigate | Set = only `{PAR-020, PAR-021, PAR-022, PAR-030}` — **DSX-ML-034 absent**; the disjointness assertion red-fails if a shipped code is added. | closed |
| T-27-07 | Spoofing (backlog id) | ATTRIBUTION `promotes_backlog_item` | high | mitigate | Sidecar names `absent_code: DSX-ML-034`, `promotes_backlog_item: "6.5-item-7-feature-provenance"`, `kind: miss`; the id is a frozen member of `_SECTION_65_ITEM_IDS` (test_known_bad_corpus.py:852); membership gate fails on any other string. | closed |
| T-27-08 | Tampering (allowlist form) | `_D05_ALLOWLIST_CODES` entry | medium | mitigate | `DSX-ML-034` added as an **exact code** (gen-finding-catalogue.py:209), never a `DSX-ML-` prefix; a prefix add would fail the build red on the legacy family. | closed |
| T-27-09 | Tampering (scope creep) | `dsx/checks/dq.py` byte-freeze | medium | mitigate | Only `dsx/checks/ml.py` edited; `git diff --stat dd930af..HEAD -- dsx/checks/dq.py` **empty** (byte-frozen). | closed |
| T-27-10 | Tampering (vacuous pin) | golden ship set | high | mitigate | Ship set re-measured by the live per-fixture golden test rather than a guessed pin; `tests.test_causal_verb_golden` **6 OK** — a wrong set fails the equality re-measure. | closed |
| T-27-11 | Information disclosure (drift) | installed overlay | medium | mitigate | `node install.mjs` re-sync THEN `node install.mjs --check` → self-test **passed** (5 gates, 6/6 agents, 14/14 skills). | closed |
| T-27-SC | Supply chain | package installs | low | accept | No npm/pip/cargo installs. The promoted entrypoint imports pandas/lightgbm/sklearn but is **read as text** by the code scan and never executed; no Package Legitimacy Gate applies. | closed |

*Status: open · closed — below the high threshold is non-blocking*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-27-01 | T-27-SC | Phase introduces zero external packages; the promoted `-entrypoint.py` is read as text by the corpus scan and never executed, so its pandas/lightgbm/sklearn imports never reach an install surface for a legitimacy gate to run against. | loop orchestrator (re-gate); operator sign-off batched to HUMAN-QUEUE (S7-2) | 2026-09-07 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-07 | 12 | 12 | 0 | orchestrator (loop S3-5, ASVS L1 grep-depth re-gate) |
| 2026-09-10 | 12 | 12 | 0 | interactive session (operator-directed): T-27-03 re-gated after the first-hand Kaufman read — docstring/marker locators verified against the PDF; no other threat touched |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-09-07 — gate **SECURED**, `threats_open: 0`, 12/12 threats CLOSED by orchestrator re-gate on real Python 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`). Register authored at plan time + ASVS L1 → the auditor short-circuit applies (L1 grep-depth sufficient); each mitigation was re-confirmed against the implementation and re-run this firing (structural greps for T-27-01/02a/02b/03/06/07/08/09; `dsx validate` PASS CRITICAL=0; `gen-finding-catalogue.py --check` current + single CRITICAL row; golden `test_causal_verb_golden` 6 OK; full suite **1599 OK**; `install.mjs --check` self-test passed) rather than trusted from a report. The load-bearing HIGH threat is T-27-03 (provenance laundering): the docstring and marker honestly record the secondary corroboration and paywall, never claiming a first-hand ACM read. **Human sign-off + UAT batched to HUMAN-QUEUE as HQ-43 (non-blocking until S7-2 per LOOP-LEDGER S3-5)** — the loop verifies the threat mitigations but does not sign the approval line (brief §4.4).

**Operator approval — 2026-09-10 (HQ-43).** Approved by the operator (decision "Option A — sign all six", given in an interactive session; recorded by that session on the operator's behalf, 2026-09-10). Independent re-verification before signing, not trusted from the loop's report: T-27-03 re-gated after the D-05 UPGRADE of the same day: the Kaufman (2012) ACM PDF was obtained and read first-hand (Sec. 3.1 p. 15:8; Sec. 3.2 eq. (3) p. 15:9), and the docstring/marker now record that read with locators verified against the text (commit `da99ccf`). T-27-01 confirmed by auditing the fixture live: `DSX-ML-034` silent (no `feature_provenance` block = the honest miss) and the incidental set {DSX-CLM-031, DSX-COH-031, DSX-MET-040, DSX-NAR-001} equals the recorded golden ship set. Accepted risk R-27-01 stands. Full suite re-run on real Python 3.12.10 before signing: **1629 tests OK**; `gen-finding-catalogue.py --check` current at 279; `node install.mjs --check` self-test passed (6/6 agents, 14/14 skills, 5 gates).
