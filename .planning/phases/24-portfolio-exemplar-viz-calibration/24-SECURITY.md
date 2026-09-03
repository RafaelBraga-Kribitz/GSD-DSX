---
phase: 24
slug: portfolio-exemplar-viz-calibration
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-09-03
---

# Phase 24 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| (none introduced) | This phase adds a **portfolio exemplar** and **calibration corpus fixtures**, neither of which introduces a new runtime input path. `examples/analysis/charts.py` is the sole matplotlib importer and is deliberately **off the gate path** (analyst-side render tool, never imported by any `dsx/` module). The bad-chart fixtures under `examples/known-bad/` are static YAML/Markdown parsed by the same hermetic gate that already parses every other spec. The corpus harness extensions in `tests/test_known_bad_corpus.py` and the tightened assertion in `tests/test_selection_heuristic_docs.py` are stdlib-only off-gate-path repo-integrity tests. | None. No network input at runtime, no untrusted parse, no auth/session, no new file/process I/O on the gate path. The only "inputs" are the repo's own static YAML specs / SVG bytes / Markdown, edited by a developer under review. The re-sealed SVGs are checksum-pinned in `examples/good-ANALYSIS-SPEC.yaml` (`.gitattributes` stores them byte-exact so `dsx seal` survives a fresh/cross-platform checkout). `matplotlib` is a pre-existing analyst-side dependency, deliberately kept OUT of the `dsx/` import closure (`test_gate_path_hermetic.FORBIDDEN`). |

---

## Threat Register

Register authored at plan time across the three `24-0N-PLAN.md` STRIDE models
(`register_authored_at_plan_time: true`). Thirteen threats total; every mitigation
re-run GREEN by the orchestrator on the clean final tree `ef13b27` — not trusted
from the 24-01/24-02/24-03 execute or the S4-4 review reports.

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-24-01-01 | Tampering | `spec.visuals[].svg_sha256` vs re-rendered SVG bytes (a stale seal shipping) | critical | mitigate | All THREE SVGs re-sealed via `dsx seal` after the style-layer re-render (24-01 Task 2); `.gitattributes` `examples/figures/*.svg binary` stores the sealed bytes byte-exact so the seal survives checkout (fix `11e2df7`). Re-run 2026-09-03: full `dsx gate ship --spec examples/good-ANALYSIS-SPEC.yaml` on a swept trail = **CRITICAL=0**; `DSX-FIG-010`/`DSX-FIG-011` (the CRITICAL stale-seal guards) do **not** fire. | closed |
| T-24-01-02 | Tampering | matplotlib on the gate path | high | mitigate | `charts.py` is the sole matplotlib importer and is not a gate module; `matplotlib` stays in `tests/test_gate_path_hermetic.FORBIDDEN`. Re-run 2026-09-03: `tests/test_gate_path_hermetic.py` GREEN (matplotlib FORBIDDEN, walked `dsx/` AST closure clean). | closed |
| T-24-01-03 | Information disclosure | `good-NARRATIVE.md` / `good-REPRO-REPORT.md` overstating the verified effect | medium | mitigate | Narrative and repro lead number pinned to `results.tests[0]` (effect 0.024, CI 1.0–3.8pp); `DSX-REP-061` (HIGH) gates a lead-number disagreement. Re-run 2026-09-03: `dsx gate ship` **HIGH=0**; `DSX-REP-06x` do **not** fire (narrative/repro/charts.py/results all reconcile). | closed |
| T-24-01-04 | Tampering | accidental finding-code mint via exemplar edits | high | mitigate | Exemplar routes only to EXISTING codes (`DSX-VIZ-071`/`DSX-FIG-*`/`DSX-REP-*`). Re-run 2026-09-03: `git diff --stat 08a65bf..ef13b27 -- dsx/ scripts/gen-finding-catalogue.py references/finding-codes.md` EMPTY → zero mint by construction; set-identity 276→276. | closed |
| T-24-02-01 | Tampering | Fixture trips MORE than its target defect (stray HIGH) | high | mitigate | Each fixture is a copy of a proven-clean good-corpus spec with exactly one bad `visuals[]` entry; the recipe was MEASURED through the real corpus harness (not estimated). `test_ship_gate_findings_are_all_documented_incidental_corpus_gaps` gates any stray HIGH. Re-run 2026-09-03: covered inside `tests.test_known_bad_corpus` GREEN. | closed |
| T-24-02-02 | Repudiation | MEDIUM catch-rate folded into the headline to inflate apparent coverage | high | mitigate | MEDIUM stratum reported BESIDE the headline; `--block-on MEDIUM` threaded through `_gate_findings` (default `None` → CRITICAL/HIGH strata byte-identical); headline-invariance assertion proves (miss-rate, FPR) unchanged by added caught fixtures. Re-run 2026-09-03: GREEN. | closed |
| T-24-02-03 | Spoofing | `DSX-VIZ-071` mislabeled as a `kind: miss` ABSENT case to force a catch | medium | mitigate | Explicitly forbidden (24-02 Task 2); the ABSENT partition checks CRITICAL-tier absence only — a firing MEDIUM is not a miss; `DSX-VIZ-071` severity unchanged. Re-run 2026-09-03: GREEN. | closed |
| T-24-02-04 | Tampering | accidental finding-code mint / `DSX-VIZ-071` severity change | high | mitigate | Fixtures route only to EXISTING `DSX-VIZ-001` (banned) / `DSX-VIZ-071` (uncertainty-mark-misuse); no gate-code edit. Re-run 2026-09-03: `gen-finding-catalogue.py --check` exit 0 @276; `git diff dsx/` EMPTY. | closed |
| T-24-02-05 | Tampering | matplotlib imported into an off-gate-path corpus test | high | mitigate | Corpus tests stay stdlib-only (Risk P7); `test_gate_path_hermetic` keeps matplotlib FORBIDDEN. Re-run 2026-09-03: GREEN (module + hermetic guard). | closed |
| T-24-03-01 | Tampering | accidental finding-code mint from 24-01/24-02 (D-06 violation) | high | mitigate | 24-03 Task 1 runs `gen-finding-catalogue.py --check` (exit 0) + CRLF-safe unique count == 276 + `Total:`-line agreement on the FINAL tree; set-identity 276→276 asserted. Re-run 2026-09-03: exit 0 @276; unique DSX-code count == 276 == the `**Total: 276 codes.**` line; `test_finding_catalogue_invariant` GREEN (added={} removed={}). | closed |
| T-24-03-02 | Tampering | snapshot/count pins silently mutated to force a pass | high | mitigate | 24-03 Task 1 verifies `test_viz_vocabulary_invariant` + `test_chart_catalog_invariant` green WITHOUT mutation; a red pin is reported for gap closure, never patched. Re-run 2026-09-03: both modules GREEN; no pin mutated. | closed |
| T-24-03-03 | Tampering | `test_doc_code_agreement.py`'s deliberate one-directionality "fixed" | medium | mitigate | Explicitly forbidden (24-03 Task 1 + Task 2); the one-directionality is documented-by-design (module docstring) and was left UNTOUCHED. Re-run 2026-09-03: `tests/test_doc_code_agreement.py` GREEN, one-directionality intact. | closed |
| T-24-03-04 | Spoofing | chart-selection doc drifts from the live vocabulary undetected | medium | mitigate | RECOMMENDED close (plan-checker's call): `test_selection_heuristic_docs.py` now imports `RELATIONSHIP_CHARTS` and asserts `set(RELATIONSHIP_CHARTS) == set(_RELATIONSHIPS)` both directions — a live 12th key or a rename fails HERE directly, not only transitively via the `len==11` pin. Re-run 2026-09-03: `tests/test_selection_heuristic_docs.py` GREEN (7 OK, incl. the both-directions method). | closed |

*Status: all thirteen `closed`*
*Severity: critical > high > medium > low — only OPEN threats at or above `workflow.security_block_on` (high) count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

One threat (T-24-01-01) is `critical` severity and several are `high`, but **every threat is CLOSED** — `threats_open: 0`, so nothing blocks under the ASVS level-1 block-on-`high` policy. The critical seal-integrity risk is discharged by the re-seal + byte-exact SVG storage, proven by `dsx gate ship` exiting 0 with `CRITICAL=0` (`DSX-FIG-010` silent).
**Package legitimacy gate: N/A** — this phase installs no npm/pip/cargo packages (matplotlib is a pre-existing analyst-side dependency), so no `T-24-SC` supply-chain threat and no legitimacy checkpoint apply.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|

No accepted risks — all thirteen threats closed by mitigation (in-tree tests + the re-seal + the D-05 zero-mint build gate + the full exemplar gate sequence), not by risk acceptance.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-03 | 13 | 13 | 0 | autonomous loop firing (secure-phase orchestrator, opus/high) — State B create; ASVS-L1 short-circuit (`threats_open: 0`, register authored at plan time across the three `24-0N-PLAN.md` STRIDE models, `register_authored_at_plan_time: true`); every mitigation re-run GREEN by the orchestrator on the clean final tree `ef13b27` rather than trusted from the 24-01/24-02/24-03 execute or S4-4 review reports. Evidence: seven mitigation modules (`tests.test_known_bad_corpus` + `tests.test_gate_path_hermetic` + `tests.test_selection_heuristic_docs` + `tests.test_doc_code_agreement` + `tests.test_viz_vocabulary_invariant` + `tests.test_chart_catalog_invariant` + `tests.test_finding_catalogue_invariant`) = **90 tests OK**; D-05 zero-mint gate `scripts/gen-finding-catalogue.py --check` exit 0 @**276** (unique DSX-code count == 276 == the `Total:` line; 9 pre-existing declared-twice warnings unchanged — this phase edits none of the mint surfaces, `git diff dsx/` EMPTY across the phase); the exemplar acceptance ran as the full `dsx gate plan→execute→verify→ship` sequence on a swept `examples/DECISIONS.jsonl` (the trail-sensitive acceptance from the S4-4 methodology note): plan/execute PASS (blocking at CRITICAL, CRITICAL=0 HIGH=0 MEDIUM=0), verify/ship PASS (blocking at HIGH, **CRITICAL=0 HIGH=0** MEDIUM=3 = 3× pre-existing `DSX-STA-011` on the untouched `results.tests` block, INFO=1) — `DSX-FIG-010`/`DSX-REP-06x` silent; full suite **1508 OK / 45.5s** from a clean tree (stray `DECISIONS.jsonl` swept per standing note). |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer) — all thirteen `mitigate`
- [x] Accepted risks documented in Accepted Risks Log — none; all closed by mitigation
- [x] `threats_open: 0` confirmed — all thirteen CLOSED with live GREEN test/gate evidence
- [x] `status: verified` set in frontmatter — machine audit complete and clean

**Approval:** verified (technical) 2026-09-03 — gate **SECURED**, `threats_open: 0`, 13/13 threats CLOSED by orchestrator re-gate on the clean final tree `ef13b27` (not trusted from the 24-01/24-02/24-03 or S4-4 reports): seven mitigation modules = 90 tests OK; `gen-finding-catalogue.py --check` exit 0 @276 (zero mint, set-identity 276→276, `git diff dsx/` EMPTY across the phase — T-24-01-04/02-04/03-01); the exemplar plan→execute→verify→ship sequence all exit 0 on a swept trail with CRITICAL=0 HIGH=0 (re-seal T-24-01-01 + repro lead-number T-24-01-03 both discharged, MEDIUM=3 = pre-existing `DSX-STA-011`); `matplotlib` in `test_gate_path_hermetic.FORBIDDEN` GREEN (T-24-01-02/02-05); full suite 1508 OK / 45.5s. **Human sign-off is BATCHED to HUMAN-QUEUE (HQ-36), non-blocking until S5-2**, mirroring the Phase 21 (HQ-29), Phase 22 (HQ-31), and Phase 23 (HQ-34) precedents. Phase 24 adds no user-facing runtime behavior beyond the exemplar/fixtures (all gated), so its UAT IS the automated invariant/gate set (`nyquist_compliant: true`, 3/3 requirements COVERED — see `24-VALIDATION.md`).
