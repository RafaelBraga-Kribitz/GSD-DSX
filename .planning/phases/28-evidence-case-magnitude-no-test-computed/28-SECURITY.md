---
phase: 28
slug: evidence-case-magnitude-no-test-computed
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
security_block_on: high
register_authored_at_plan_time: true
created: 2026-09-08
---

# Phase 28 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register built from the two PLAN `<threat_model>` blocks (28-01 mint, 28-02
> fixture + harness); every mitigation re-verified against the implementation by the
> orchestrator (loop S4-5, ASVS L1 grep-depth) on real Python 3.12.10 — not trusted
> from a subagent report.
> Phase 28 mints one code (`DSX-CLM-034`, claim→cited-test traceability) under a
> human-confirmed D-05 citation (Wilkinson & TFSI 1999, read in full primary text —
> HQ-40 row 40c) and promotes a corpus MISS fixture built on the collision/mislabel
> construction. The attack surface is D-05 over-claiming (laundering a *motivating
> principle* into an *asserted mechanism*), catalogue/count tampering, a fixture that
> silently flips MISS→CATCH, and the new `_PER_FIXTURE_INCIDENTAL_CODES` map being
> abused to launder a missed target as an allowed incidental — not general runtime
> input handling. `dsx/checks/dq.py` stays byte-frozen (profiler-is-a-producer rule).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| measured verdict → mint decision | Task 1's recorded VERDICT is the sole gate on whether any code is minted; an ambiguous conditional read as "mint by default" would mint on a CAUGHT verdict and violate D-13. | `28-MEASUREMENT.md` verdict |
| minted code → finding catalogue | A new `report.add` call-site becomes a catalogue row via AST extraction; a non-deterministic or over-claiming emission corrupts the committed catalogue. | `report.add` code/severity |
| docstring / `# D-05:` marker → D-05 honesty record | The Citation text is the durable provenance claim; over-claiming that Wilkinson mandates the overlap mechanic launders a motivating principle into an asserted mechanism. | citation prose |
| promoted fixture → corpus harness | A fixture that silently gains a `claims[].supported_by` field converts the MISS into a CATCH and defeats the requirement's whole point (`kind: miss`). | ANALYSIS-SPEC bytes |
| per-fixture incidental map → completeness tests | `_PER_FIXTURE_INCIDENTAL_CODES` must stay strictly narrower than the global list (every entry another slug's declared target) and must never touch `_own_target_codes`/`_effective_target_map`, else a missed target could be laundered as an allowed incidental. | slug→code map |
| ATTRIBUTION sidecar → §6.5 backlog id set | An id that does not match the frozen `_SECTION_65_ITEM_IDS` fails the sidecar gate; a shipped `absent_code` placed in the backlog set fails the disjointness gate. | sidecar id strings |
| source tree → installed overlay | An un-synced overlay means the shipped package disagrees with the repo; `install --check` is the boundary check. | source file bytes |
| untrusted spec content → static check | `claim.get("supported_by")`/`claim.get("rounding")` are read off a parsed YAML dict; the entrypoint is read as text and never executed (V5 input validation, standing gate-path rule). | ANALYSIS-SPEC bytes |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-28-05 | Tampering / Repudiation (of D-13) | mint executed as "mint by default" on a CAUGHT verdict | high | mitigate | `28-MEASUREMENT.md` first line is **`VERDICT: LIVE MISS`** (independently re-run by the orchestrator: `DSX-CLM-033` silent at verify/ship via the ×100 bridge; honest-swap no-toggle; break-swap makes `DSX-CLM-033` fire). The mint is the conditional LIVE-MISS branch; a CAUGHT verdict is a no-mint terminal. | closed |
| T-28-01 | Repudiation (D-05 over-claim) | `DSX-CLM-034` docstring + `# D-05:` marker | high | mitigate | Docstring (`claims.py:482`) + marker (`tests/test_claims_supported_by.py:11`) cite Wilkinson & TFSI (1999) as the **MOTIVATING PRINCIPLE only** and disclaim any numeric-overlap mandate (bounded-catch honesty: a stray number, not metric identity); the citation was read in full primary text (HQ-40 40c). | closed |
| T-28-02 | Tampering (count pin) | catalogue count pins (277→278) | high | mitigate | `references/finding-codes.md` **Total 278**; `_EXPECTED_TOTAL = 278` (invariant), p19 pin **278**, phase-20 pin **278** — moved in lockstep; drift red-fails the invariant + phase-20 tests. `gen-finding-catalogue.py --check` → exit 0, "current". | closed |
| T-28-03 | Tampering (retrofit uncited docstring) | D-05 docstring placement | high | mitigate | `DSX-CLM-034` lives in a **brand-new function** `_check_supported_by_traceability` (`claims.py:477`), separate from the uncited `_check_numeric_overlap` (`claims.py:344`) shared with `DSX-CLM-033`; the `report.add("DSX-CLM-034", "HIGH")` is inside the new function (`claims.py:557`). | closed |
| T-28-04 | Tampering (allowlist form) | `_D05_ALLOWLIST_CODES` entry | high | mitigate | `DSX-CLM-034` added as an **exact code** (`gen-finding-catalogue.py:218`), never a `DSX-CLM-` prefix; a prefix add would obligate the uncited legacy CLM family and fail the build red. | closed |
| T-28-08 | Tampering (MISS→CATCH) | promoted ANALYSIS-SPEC | high | mitigate | Fixture declares **no** `claims[].supported_by` field (`grep supported_by` = **0**); `dsx validate` → **PASS, CRITICAL=0** (magnitude defect stays invisible = an honest miss); the falsifiability test (`test_known_bad_corpus.py:2620-2633`) runs the live gate and asserts `DSX-COH-001` fires while `DSX-CLM-034` does **not** — flips if a `supported_by` is added. | closed |
| T-28-09 | Spoofing (backlog id) | ATTRIBUTION `promotes_backlog_item` | high | mitigate | Sidecar names `absent_code: DSX-CLM-034`, `promotes_backlog_item: "6.5-item-8-magnitude-without-computed-effect"`, `kind: miss`; the id is a frozen member of `_SECTION_65_ITEM_IDS` (`test_known_bad_corpus.py:950`); membership gate fails on any other string. | closed |
| T-28-10 | Tampering (backlog leak) | `_SECTION_65_BACKLOG_CODES` | high | mitigate | `DSX-CLM-034` kept **out** of the backlog set (`test_known_bad_corpus.py:929`); the disjointness assertion (`:1724`, `set & catalogue == ∅`) red-fails if a shipped code is added. Green in the passing suite. | closed |
| T-28-11 | Tampering (spec-count pin) | `tests/test_dsx.py` spec count | high | mitigate | `self.assertEqual(len(paths), 44, …)` (`test_dsx.py:588`) — moved 43→44 exactly when the fixture landed; count assert red-fails on drift. | closed |
| T-28-12 | Tampering (vacuous pin) | golden ship set | high | mitigate | Ship set **re-measured live** (read from `_gate_findings`, never a static `_GOLDEN_SHIP_FINDINGS` pin — D-09); the per-fixture falsifiability test (`test_known_bad_corpus.py:2620-2633`) asserts `DSX-COH-001` CRITICAL at plan/verify/ship and `DSX-CLM-034` absent — a wrong set fails the equality re-measure. | closed |
| T-28-07 | Tampering (tolerance loosening) | significant-figures tolerance | medium | mitigate | The comparator is never looser than `DSX-CLM-033`'s rel-5%/abs-5e-4 window; the tie-boundary and rounding-may-tighten unit tests (`test_claims_supported_by.py:135, :198`) assert the direction. | closed |
| T-28-06 | Tampering (scope creep) | `dsx/checks/dq.py` byte-freeze | medium | mitigate | `git diff --stat caa9e4f..HEAD -- dsx/checks/dq.py` **empty** (byte-frozen); the mint lives in `dsx/checks/claims.py`. | closed |
| T-28-13 | Information disclosure (drift) | installed overlay | medium | mitigate | `node install.mjs` re-sync THEN `node install.mjs --check` → self-test **passed** (5 gates, 6/6 agents, 14/14 skills). | closed |
| T-28-SC | Supply chain | package installs | low | accept | No npm/pip/cargo installs. The promoted entrypoint is **read as text** by the code scan and never executed; no Package Legitimacy Gate applies. | closed |

*Status: open · closed — below the high threshold is non-blocking*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-28-01 | T-28-SC | Phase introduces zero external packages; the promoted `-entrypoint.py` is read as text by the corpus scan and never executed, so its imports never reach an install surface for a legitimacy gate to run against. | loop orchestrator (re-gate); operator sign-off batched to HUMAN-QUEUE (S7-2) | 2026-09-08 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-08 | 14 | 14 | 0 | orchestrator (loop S4-5, ASVS L1 grep-depth re-gate) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-09-08 — gate **SECURED**, `threats_open: 0`, 14/14 threats CLOSED by orchestrator re-gate on real Python 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`). Register authored at plan time (2/2 PLAN `<threat_model>` blocks; `T-28-06` and `T-28-SC` shared across both, deduplicated) + ASVS L1 → the auditor short-circuit applies (L1 grep-depth sufficient); each mitigation was re-confirmed against the implementation and re-run this firing (structural greps for T-28-01/02/03/04/09/10/11; `28-MEASUREMENT.md` VERDICT LIVE MISS for T-28-05; `dsx validate` PASS CRITICAL=0 + `supported_by` grep 0 for T-28-08; live falsifiability test for T-28-12; tolerance-direction tests for T-28-07; `dq.py` empty diff for T-28-06; `gen-finding-catalogue.py --check` current + single `DSX-CLM-034 | HIGH` row for T-28-02/04; full suite **1615 OK**; `install.mjs --check` self-test passed for T-28-13) rather than trusted from a report. The load-bearing HIGH threat is T-28-01 (D-05 over-claim): the docstring and marker record Wilkinson & TFSI (1999) as the motivating principle only and never claim it mandates the numeric-overlap mechanic. **Human sign-off + UAT batched to HUMAN-QUEUE as HQ-44 (non-blocking until S7-2 per LOOP-LEDGER S4-5)** — the loop verifies the threat mitigations but does not sign the approval line (brief §4.4).
