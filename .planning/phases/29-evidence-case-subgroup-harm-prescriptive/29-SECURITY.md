---
phase: 29
slug: evidence-case-subgroup-harm-prescriptive
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
security_block_on: high
register_authored_at_plan_time: true
created: 2026-09-08
---

# Phase 29 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register built from the two PLAN `<threat_model>` blocks (29-01 mint, 29-02
> TARGET fixture + harness); every mitigation re-verified against the implementation
> by the orchestrator (loop S5-5, ASVS L1 grep-depth) on real Python 3.12.10 — not
> trusted from a subagent report.
> Phase 29 mints one code (`DSX-COH-041`, subgroup-harm disposition obligation) under a
> human-confirmed D-05 citation (Gail & Simon 1985, read at its locator, HQ-40 row 40e)
> and promotes the corpus's FIRST `kind: target` fixture — the load-bearing inverse of
> the Phase-27/28 permanent misses (D-29-00): the newly-minted code is PRESENT and fires
> CRITICAL at plan/verify/ship. The attack surface is D-05 over-claiming (laundering
> Gail & Simon's *motivating definition* into an *asserted likelihood-ratio mechanic*),
> catalogue/count tampering, a frozen case widened to manufacture a miss, a fixture that
> silently gains a `decision.subgroup_harm[]` row (flipping the honest TARGET into a
> silenced case), and the new `kind: target` vocabulary mis-routing a code — not general
> runtime input handling. `dsx/checks/dq.py` and `dsx/cli.py` stay byte-frozen
> (profiler-is-a-producer rule; the mint lives in the existing coherence family dispatch).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| measured verdict → mint decision | Task 1's recorded VERDICT is the sole gate on whether any code is minted; an ambiguous conditional read as "mint by default" would mint on a CAUGHT verdict and violate D-13. | `29-MEASUREMENT.md` verdict |
| minted code → finding catalogue | A new `report.add` call-site becomes a catalogue row via AST extraction; a non-deterministic or over-claiming emission corrupts the committed catalogue. | `report.add` code/severity |
| docstring / `# D-05:` marker → D-05 honesty record | The Citation text is the durable provenance claim; over-claiming that Gail & Simon (1985) authorises the enforcement mechanic launders a motivating definition into an asserted likelihood-ratio test the code never runs. | citation prose |
| frozen case → mint decision | The four-segment shape (3 positive + 1 minority opposing above floor) and its numbers are frozen (D-29-02); shaving segment D to a trivial n/effect to force a miss would manufacture the gap D-13 forbids. | ANALYSIS-SPEC bytes |
| promoted fixture → corpus harness | A fixture that silently gains a `decision.subgroup_harm[]` disposition row converts the honest TARGET into a silenced case and defeats the requirement's point (`kind: target`, DSX-COH-041 must fire). | ANALYSIS-SPEC bytes |
| kind vocabulary → completeness/falsifiability tests | `("miss", "caught", "target")` is a closed vocabulary; a mis-placed code or a fourth kind would route the `kind`-switches (schema, falsifiability, ABSENT-partition guard) incorrectly. | slug→kind map |
| ATTRIBUTION sidecar → §6.5 backlog id set | An id that does not match the frozen `_SECTION_65_ITEM_IDS` fails the sidecar gate; a shipped `absent_code` placed in `_SECTION_65_BACKLOG_CODES` fails the disjointness gate. | sidecar id strings |
| source tree → installed overlay | An un-synced overlay means the shipped package disagrees with the repo; `install --check` is the boundary check. | source file bytes |
| untrusted spec content → static check | `decision.get("subgroup_harm_floor")` / `results.get("segments")` are read off a parsed YAML dict; the entrypoint is read as text and never executed (V5 input validation, standing gate-path rule). | ANALYSIS-SPEC bytes |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-29-01 | Tampering (of design intent) / Repudiation (of D-13) | plan conditional executed as "mint by default" on a CAUGHT verdict | high | mitigate | `29-MEASUREMENT.md` first line is **`VERDICT: LIVE MISS`** (independently re-run by the orchestrator: the DEFECT fixture exits 0 at validate/plan/execute/verify/ship, CRITICAL=[] HIGH=[]; the D→+0.06 swap counterfactual toggles nothing, so no existing code was a latent catch). The mint is the conditional LIVE-MISS branch; a CAUGHT verdict is a no-mint terminal. | closed |
| T-29-02 | Repudiation (D-05 over-claim) | `DSX-COH-041` docstring + `# D-05:` marker | high | mitigate | Docstring (`dsx/checks/coherence.py:229-236`) + marker (`tests/test_subgroup_harm_disposition.py:10`) cite Gail & Simon (1985) as the **MOTIVATING DEFINITION only** and disclaim the likelihood-ratio mechanic ("does NOT cite Gail & Simon as authority for the enforcement path (D-02)"; test comment: "NOT the Gail & Simon mechanic … must not be read as detecting hidden, mis-signed defects"). Source read at its locator + operator-CONFIRMED (HQ-40 40e). | closed |
| T-29-03 | Tampering (count pin) | catalogue count pins (278→279) | high | mitigate | `references/finding-codes.md` **Total 279**; the invariant, phase-20 and p19 pins move in lockstep; drift red-fails the invariant test. `gen-finding-catalogue.py --check` → exit 0, "finding catalogue is current". | closed |
| T-29-04 | Tampering (retrofit uncited docstring) | D-05 docstring placement | high | mitigate | `DSX-COH-041` lives in a **brand-new function** `_check_subgroup_harm_disposition` (`dsx/checks/coherence.py:223`), separate from the uncited legacy coherence checks; the Citation obligation does not retrofit an uncited legacy docstring. | closed |
| T-29-05 | Tampering (allowlist form) | `_D05_ALLOWLIST_CODES` entry | high | mitigate | `DSX-COH-041` added as an **exact code** (`scripts/gen-finding-catalogue.py:228`), never a `DSX-COH-` prefix; a prefix add would obligate the uncited legacy COH family and fail the build red. | closed |
| T-29-06 | Tampering (scope creep) | `dsx/checks/dq.py` + `dsx/cli.py` + wave-1 catalogue byte-freeze | medium | mitigate | `git diff --stat 4945a62..HEAD -- dsx/checks/dq.py dsx/cli.py` **empty** (byte-frozen); the mint lives in `dsx/checks/coherence.py`, registered through the existing coherence family dispatch with no `cli.py` edit. | closed |
| T-29-07 | Tampering (scope creep) | `dsx/checks/dq.py` byte-freeze | medium | mitigate | Covered by the empty diff above — only `coherence.py` was edited for the mint; `dq.py` byte-frozen (profiler-is-a-producer rule). | closed |
| T-29-08 | Tampering (TARGET→silenced) | promoted ANALYSIS-SPEC | high | mitigate | Fixture declares `decision.subgroup_harm_floor: 500` and **DELIBERATELY OMITS** the `decision.subgroup_harm[]` disposition list (grep of the spec confirms no disposition row), so the missing-row CRITICAL fires — an honest TARGET; the falsifiability `kind`-switch runs the live gate and requires `DSX-COH-041` fire CRITICAL, and the golden-set test re-measures the ship set — either flips red if a disposition row is added. | closed |
| T-29-09 | Spoofing (backlog id) | ATTRIBUTION `promotes_backlog_item` | high | mitigate | Sidecar names `absent_code: DSX-COH-041`, `promotes_backlog_item: "6.5-item-9-subgroup-harm-declaration"`, `kind: target` (the corpus's FIRST); the id is a frozen member of `_SECTION_65_ITEM_IDS`; membership gate fails on any other string. | closed |
| T-29-10 | Tampering (kind vocab/placement) | `kind` vocabulary + `_TARGET_DEFECT_CODES` | high | mitigate | The closed vocabulary is extended to `("miss", "caught", "target")` (`tests/test_known_bad_corpus.py:1810`); `DSX-COH-041` is wired in `_TARGET_DEFECT_CODES` at plan/verify/ship (`:223,:336`) with `_EXPECTED_CAUGHT_DEFECTS[slug]=frozenset()`; the schema and critical-threshold tests fail on a wrong kind or a mis-placed code. | closed |
| T-29-11 | Tampering (spec-count pin) | `tests/test_dsx.py` spec count | high | mitigate | `self.assertEqual(len(paths), 45, …)` (`tests/test_dsx.py:593`) — moved 44→45 exactly when the fixture landed; count assert red-fails on drift. | closed |
| T-29-12 | Tampering (vacuous pin) | golden ship set | high | mitigate | Ship set **re-measured live** (`_GOLDEN_SHIP_FINDINGS[slug] = frozenset({DSX-COH-041})`, PRESENT — it fires live at plan/verify/ship, re-measured by the per-fixture golden test, not statically guessed); a set that dropped `DSX-COH-041` (fixture stopped being a catch) or carried an undocumented incidental fails the equality re-measure. | closed |
| T-29-13 | Information disclosure (drift) | installed overlay | medium | mitigate | `node install.mjs` re-sync THEN `node install.mjs --check` → self-test **passed** (5 gates, 6/6 agents, 14/14 skills). | closed |
| T-29-14 | Tampering (partition floor) | ABSENT-partition floor | high | mitigate | `_ABSENT_PARTITION_FLOOR = 3` (`tests/test_known_bad_corpus.py:1032`) **untouched**; the `kind: target` sidecar is excluded from the miss partition by `!= "miss"` (`:1959`), so the floor stays 3 and the standing assertions verify it. | closed |
| T-29-SC | Supply chain | package installs | low | accept | No npm/pip/cargo installs. The promoted `-entrypoint.py` is **read as text** by the code scan and never executed; no Package Legitimacy Gate applies. | closed |

*Status: open · closed — below the high threshold is non-blocking*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-29-01 | T-29-SC | Phase introduces zero external packages; the promoted `-entrypoint.py` is read as text by the corpus scan and never executed, so its imports never reach an install surface for a legitimacy gate to run against. | loop orchestrator (re-gate); operator sign-off batched to HUMAN-QUEUE (S7-2) | 2026-09-08 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-08 | 15 | 15 | 0 | orchestrator (loop S5-5, ASVS L1 grep-depth re-gate) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-09-08 — gate **SECURED**, `threats_open: 0`, 15/15 threats CLOSED by orchestrator re-gate on real Python 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`). Register authored at plan time (2/2 PLAN `<threat_model>` blocks; `T-29-06` and `T-29-SC` shared across both, deduplicated) + ASVS L1 → the auditor short-circuit applies (L1 grep-depth sufficient); each mitigation was re-confirmed against the implementation and re-run this firing (`29-MEASUREMENT.md` VERDICT LIVE MISS for T-29-01; structural greps at their locators for T-29-02/04/05/09/10/14; `dq.py`+`cli.py` empty diff `4945a62..HEAD` for T-29-06/07; `gen-finding-catalogue.py --check` current + Total 279 for T-29-03; fixture `dsx validate` PASS CRITICAL=0 + no `subgroup_harm[]` row for T-29-08; live golden re-measure + full suite for T-29-12; spec count 45 for T-29-11; `install.mjs --check` self-test passed for T-29-13; full suite **1627 OK**) rather than trusted from a report. The load-bearing HIGH threats are T-29-02 (D-05 over-claim): the docstring and marker record Gail & Simon (1985) as the motivating definition only and never claim it authorises the enforcement mechanic; and T-29-08 (TARGET honesty): the fixture omits the disposition row so DSX-COH-041 fires as designed. **Human sign-off + UAT batched to HUMAN-QUEUE as HQ-45 (non-blocking until S7-2 per LOOP-LEDGER S5-5)** — the loop verifies the threat mitigations but does not sign the approval line (brief §4.4).
