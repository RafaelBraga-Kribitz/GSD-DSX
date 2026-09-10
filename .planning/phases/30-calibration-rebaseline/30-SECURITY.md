---
phase: 30
slug: calibration-rebaseline
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
security_block_on: high
register_authored_at_plan_time: true
created: 2026-09-10
---

# Phase 30 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register built from the two PLAN `<threat_model>` blocks (30-01 measurement +
> readout; 30-02 doc re-baseline + audit battery + zero-mint); every mitigation
> re-verified against the implementation by the orchestrator (loop S6-5, ASVS L1
> grep-depth) on real Python 3.12.10 — not trusted from a subagent report.
> Phase 30 is the terminal calibration re-baseline: it **measures** the grown corpus
> (42 known-bad + 15 good-control) with the three v2.6 cases classified from the
> committed harness wiring (2 misses DSX-ML-034/DSX-CLM-034 + 1 target DSX-COH-041)
> and **mints zero codes** (set-identity 279 → 279). It designs nothing. The attack
> surface is therefore a *record-integrity* surface, not a runtime input surface:
> a readout number that does not equal a measured value; an FPR of 0/15 dressed up
> as a point estimate of a ~0 rate; a frozen gate module, fixture, or catalogue
> silently mutated to reshape the calibration; a stale doc claim (the "39 known-bad"
> that the corpus outgrew) left un-pinned; a `kind: target` case double-counted into
> the headline; a wrong interpreter/dirty tree hiding a skip. `dsx/` (incl. `dq.py`,
> `cli.py`, `viz.py`), `examples/` and `references/finding-codes.md` stay byte-frozen
> for the whole phase (profiler-is-a-producer + zero-mint rules).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| measured JSON → readout prose | Every headline/stratum number in `30-READOUT.md` must equal a value the read-only companion computed live; a hand-typed number that drifts from the measurement corrupts the durable calibration record. | companion JSON values |
| companion → gate path | The measurement companion `_measure_readout.py` runs read-only, off the gate path, tempdir-per-call; if it touched a tracked surface it would both perturb the calibration and violate the freeze. | file bytes under `dsx/`, `examples/`, `references/` |
| `kind: target` case → headline denominators | The corpus's first `kind: target` (DSX-COH-041) must be excluded from the PRESENT/ABSENT miss denominators; counting it into the headline would move a construction-invariant rate. | slug→kind map |
| readout FPR → external reader | 0/15 is a bounded observation, not a measured ~0 rate; reporting it as a point estimate would overstate calibration to a sceptical reader. | reported rate + interval text |
| doc claim → live corpus | `brief.md` §6.5 and the literature record assert corpus counts and item outcomes; a claim not pinned to the live corpus (the drift that let the doc read "39" while the corpus was 42) silently goes stale. | doc bytes vs live glob |
| agreement test → doc/live pins | `test_literature_corpus_count_agreement` asserts DOC == LIVE glob agreement; an over-pinned literal would false-pass on a stale number, an under-scoped regex would over-fire on line endings. | doc counts, glob counts |
| catalogue → zero-mint gate | `gen-finding-catalogue.py --check` is the authoritative set-identity boundary; any added/removed code fails REQ-P30-03. | DSX-* code set |
| source tree → installed overlay | An un-synced overlay means the shipped package disagrees with the repo; `install --check` is the boundary check. | source file bytes |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-30-01 | Tampering | `30-READOUT.md` numbers | high | mitigate | Every readout number equals a companion value; the durable reproducer `tests/test_known_bad_corpus.py::TestKnownBadCorpus::test_stratified_catch_rate_and_fpr_report` (re-run this unit: **OK, 7.7s**) independently asserts the partitions + floor; the headline pair **(miss 1.0 = 5/5, FPR 0.0 = 0/15)** and the ~0.181 bound are present in the readout. | closed |
| T-30-02 | Information disclosure (misleading record) | FPR reporting | high | mitigate | `30-READOUT.md` §3 states the one-sided **95% upper bound ≈ 0.181** (Clopper-Pearson `1 − 0.05^(1/15)`) and explicitly reads "0/15 is not evidence of a ~0 false-positive rate — it is a bounded observation"; the miss-rate carries the construction-invariant caveat and **NO confidence interval** (D-10 / F3), verbatim at readout `:58-59`, `:155-156`. | closed |
| T-30-03 | Tampering | `dsx/`, `examples/`, `references/finding-codes.md` (frozen) | critical | mitigate | Companion is read-only, off gate path, tempdir-per-call; whole-phase frozen-surface diff `git diff --stat e2ffd73..HEAD -- dsx/ examples/ references/finding-codes.md` is **empty** (byte-identical) — no reshape. | closed |
| T-30-04 | Spoofing (wrong interpreter) | measurement run | medium | mitigate | All steps run on the REAL interpreter (`python.exe` reported **Python 3.12.10**); the bare `python3` stub (3.14.6) is forbidden. The full suite ran with **no skips** and `scripts/check.sh` "determinism: identical input, identical output" ran (not skipped). | closed |
| T-30-05 | Tampering (silent drop/double-count) | `kind: target` handling | high | mitigate | The companion ABSENT loop excludes `kind: target` via the kind guard; `30-READOUT.md` §1 carries the **invariance proof** ("injecting a synthetic target-present case leaves the headline byte-identical", `:45-46`); the reproducer re-confirms an added catch cannot move the headline (**OK**). | closed |
| T-30-06 | Tampering (misleading record) | `brief.md` §6.5 backdrop | high | mitigate | The dated Phase-30 re-evaluation section names **DSX-ML-034, DSX-CLM-034, DSX-COH-041** (grep confirmed all three present) and the /15 FPR phrasing; the Phase-12 record is preserved as history (not overwritten). Numbers read from `30-READOUT.md`. | closed |
| T-30-07 | Tampering (stale claim) | literature doc row 15 + deferred table | high | mitigate | `docs/literature/the-ai-data-scientist.md`: "**42 known-bad**" present (grep=1), "**39 known-bad**" gone (grep=0); the new agreement test pins row-15 counts to the live globs so future drift fails a gate (**2 OK**). | closed |
| T-30-08 | Elevation (gap-test over/under-pinning) | `test_literature_corpus_count_agreement` | medium | mitigate | The test asserts DOC == LIVE agreement (no hardcoded number, so it cannot under-pin to a stale literal); a CRLF-tolerant regex avoids over-firing on line endings; it pins nothing beyond the row-15 counts (GA-4 "and no more"). Re-run: **2 OK**. | closed |
| T-30-09 | Tampering | catalogue / fixtures / `dq.py` / `viz.py` (frozen) | critical | mitigate | `gen-finding-catalogue.py --check` set-identity **279 → 279** (exit 0, "current"); the invariant test confirms the code SET equals the frozen Phase-12 snapshot **plus the sanctioned mints** and enumerates exactly 279 (**OK**); frozen-surface `git diff` **empty** (covers `dq.py`, `viz.py`, fixtures). | closed |
| T-30-10 | Spoofing (wrong interpreter / dirty tree) | audit battery | high | mitigate | Real 3.12.10 only; stray `DECISIONS.jsonl` deleted before the run (standing note); the full suite ran on the real interpreter so the matplotlib determinism test ran rather than skipped — **1629 tests OK, no skips**; `scripts/check.sh` "all checks passed". | closed |
| T-30-11 | Tampering (zero-mint violation) | finding catalogue | critical | mitigate | REQ-P30-03 set-identity **279 → 279, added={} removed={}**; the live count was **re-measured** this unit (279 rows, "Total: 279 codes."), not assumed; `--check` exit 0. | closed |

*Status: open · closed — below the high threshold is non-blocking*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-30-01 | (no SC threat declared) | Phase 30 introduces **zero external packages**: its only non-`.planning` edits are two doc rewrites (`brief.md`, `docs/literature/the-ai-data-scientist.md`) and one stdlib-only test (`tests/test_literature_corpus_count_agreement.py`). No package-legitimacy surface exists this phase, so neither PLAN `<threat_model>` declared a supply-chain threat and none is invented here. | loop orchestrator (re-gate); operator sign-off batched to HUMAN-QUEUE (S7-2) | 2026-09-10 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-10 | 11 | 11 | 0 | orchestrator (loop S6-5, ASVS L1 grep-depth re-gate) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-09-10 — gate **SECURED**, `threats_open: 0`, 11/11 threats CLOSED by orchestrator re-gate on real Python 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`). Register authored at plan time (2/2 PLAN `<threat_model>` blocks; T-30-01..05 from 30-01, T-30-06..11 from 30-02 — disjoint IDs, no dedup) + ASVS L1 → the auditor short-circuit applies (L1 grep-depth sufficient); each mitigation was re-run this firing rather than trusted from a report: reproducer `test_stratified_catch_rate_and_fpr_report` **OK 7.7s** (T-30-01/05); readout FPR-bound + no-interval text at `:58-59`/`:155-156` (T-30-02); whole-phase frozen-surface `git diff` **empty** for `dsx/`+`examples/`+`references/finding-codes.md` (T-30-03/09); real 3.12.10 + no-skip full suite + determinism ran (T-30-04/10); readout §1 invariance proof (T-30-05); `brief.md` names all three v2.6 codes (T-30-06); literature doc "42 known-bad" present / "39 known-bad" gone + agreement test **2 OK** (T-30-07/08); `gen-finding-catalogue.py --check` current + set-identity **279 → 279** + invariant test "code SET == frozen Phase-12 snapshot + sanctioned mints" + 279 rows (T-30-09/11); full suite **1629 OK**, `node install.mjs --check` self-test passed, `scripts/check.sh` all passed. The three CRITICAL threats (T-30-03 frozen-surface, T-30-09 catalogue/fixtures/`dq.py`/`viz.py` freeze, T-30-11 zero-mint) are all closed at the byte level. The load-bearing HIGH threats are T-30-01 (readout numbers equal measured values, reproduced live) and T-30-02 (FPR 0/15 reported as a bounded observation with its one-sided upper bound, never a ~0 point estimate). **Human sign-off + UAT batched to HUMAN-QUEUE as HQ-46 (non-blocking until S7-2 per LOOP-LEDGER S6-5)** — the loop verifies the threat mitigations but does not sign the approval line (brief §4.4).

**Operator approval — 2026-09-10 (HQ-46).** Approved by the operator (decision "Option A — sign all six", given in an interactive session; recorded by that session on the operator's behalf, 2026-09-10). Independent re-verification before signing, not trusted from the loop's report: T-30-01/05 confirmed by re-running the reproducer `test_stratified_catch_rate_and_fpr_report` (OK); T-30-09/11 by `gen-finding-catalogue.py --check` (current, 279, zero-mint); T-30-02 confirmed in `30-READOUT.md` (:58-59 no interval on the construction-invariant miss rate; :155-156 the one-sided 95% upper bound ~0.181 on FPR 0/15, stated as a bounded observation). Operator note recorded with the approval: fifteen good-control specs is a thin FPR denominator; growing that corpus is carried to SEED-003 as a v2.7 candidate, not a sign-off blocker. Full suite re-run on real Python 3.12.10 before signing: **1629 tests OK**; `gen-finding-catalogue.py --check` current at 279; `node install.mjs --check` self-test passed (6/6 agents, 14/14 skills, 5 gates).
