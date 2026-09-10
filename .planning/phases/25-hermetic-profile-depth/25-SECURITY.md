---
phase: 25
slug: hermetic-profile-depth
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
security_block_on: high
register_authored_at_plan_time: true
created: 2026-09-07
---

# Phase 25 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register built from the four PLAN `<threat_model>` blocks (25-01…25-04);
> every mitigation re-verified against the implementation by the orchestrator
> (loop S1-5, ASVS L1 grep-depth) — not trusted from a subagent report.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| local CSV file → profile_csv | Untrusted extract bytes read and aggregated in a single pass; caller-supplied column-name args (`--pk`/`--time`/`--unit`/`--target`). No network, no auth, no eval. | untrusted CSV cell bytes; column-name strings |
| CLI args → cmd_profile → profile_csv | `--unit`/`--target` are caller-supplied header names; `--target` cell values validated as binary `{0,1}` before aggregation. | caller CLI strings; untrusted target cells |
| repo files → host overlay (install.mjs) | Installer copies `dsx/`, `templates/`, `references/` into the runtime overlay; the only concern is drift between repo and installed copy, adjudicated by `--check`. | source file bytes |
| profile file → dq.check | The DQ gate parses an arbitrary-nesting YAML profile with no schema; new profiler keys must be provably inert to the verdict (profiler is a producer, never a gate — D-01/D-02). | YAML profile keys |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-25-01 | Denial of Service (local) | profile_csv accumulators / bad flag | low | mitigate | New numeric/categorical accumulators grow inside the single existing pass, no second read, no unbounded per-row structure; missing file/header/bad flag → `CheckError` exit 2 (`dsx/profiler.py:172,191,220`). | closed |
| T-25-02 | Tampering (data integrity) | numeric parsing | medium | mitigate | Values parsed only via the ASCII `_INT_RE`/`_FLOAT_RE`-gated path — no locale-aware `float()` call site (`dsx/profiler.py:27-28,55-57,248`). | closed |
| T-25-03 | Tampering | `--unit`/`--target` column-name args | low | mitigate | Unknown header raises `CheckError` exit 2 matching `--pk`/`--time` (`dsx/profiler.py:216,222`); the name indexes a header dict, never eval or a filesystem path. | closed |
| T-25-04 | Information disclosure (determinism) | tie-break / container order | medium | mitigate | Explicit `sorted(counts.items(), key=lambda kv:(-kv[1],kv[0]))` for every top-N/rare/unit rank (`dsx/profiler.py:142,396`), ISO-week ordered by key (`:352`); never `Counter.most_common()` at ties; `isocalendar()` locale-free; determinism tests are the trip-wire. | closed |
| T-25-05 | Tampering (spec bypass) | binary target validation | medium | mitigate | Closed check against the literal set `{"0","1"}` (`dsx/profiler.py:412`); yes/no/true/false rejected (no truthy coercion); the error lists every offending value so it cannot be silently over-accepted (`:415`). | closed |
| T-25-06 | Tampering (silent drift) | installed overlay vs repo | medium | mitigate | `node install.mjs` re-sync + `node install.mjs --check` (the v2.5.0 real gate) → self-test **passed** (5 gates, 6/6 agents, 14/14 skills) proves installed copy matches repo after the `dsx/`/doc edits. | closed |
| T-25-07 | Elevation of privilege (scope creep) | new profile keys reaching a gate | high | mitigate | `dsx/checks/dq.py` reads only its six named keys via `.get()` — no arbitrary-key iteration over profile keys; `TestDQGateIgnoresNewKeys::test_gate_verdict_identical_with_and_without_new_keys` green; `dq.py` byte-unchanged for the phase (empty diff); catalogue **276 → 276**. The profiler stays a producer, never a gate. | closed |
| T-25-SC | Tampering (supply chain) | package installs | n/a | accept | Zero external packages introduced this phase (stdlib-only per D-01); no npm/pip/cargo install surface exists, so the legitimacy gate has no object to run against. | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| R-25-01 | T-25-SC | Phase introduces zero external packages (stdlib-only per D-01); the installer copies existing repo files only, no registry fetch — there is no install surface for a legitimacy gate to run against. | loop orchestrator (re-gate); operator sign-off batched to HUMAN-QUEUE (S7-2) | 2026-09-07 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-07 | 8 | 8 | 0 | orchestrator (loop S1-5, ASVS L1 grep-depth re-gate) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-09-07 — gate **SECURED**, `threats_open: 0`, 8/8 threats CLOSED by orchestrator re-gate. Register authored at plan time + ASVS L1 → the auditor short-circuit applies (L1 grep-depth sufficient); each mitigation was re-confirmed against the implementation at its locator rather than trusted from a report. **Human sign-off + UAT batched to HUMAN-QUEUE (non-blocking until S7-2 per LOOP-LEDGER S1-5)** — the loop verifies the threat mitigations but does not sign the approval line (brief §4.4).

**Operator approval — 2026-09-10 (HQ-41).** Approved by the operator (decision "Option A — sign all six", given in an interactive session; recorded by that session on the operator's behalf, 2026-09-10). Independent re-verification before signing, not trusted from the loop's report: T-25-07 spot-checked at its locator (`dsx/checks/dq.py` reads six named keys only, no iteration over profile keys; `TestDQGateIgnoresNewKeys` present in `tests/test_profiler_hermetic.py:520`); the accepted supply-chain risk R-25-01 stands (no install surface). Independent runs: `dsx profile` exercised with all four new flags on a generated 180-row CSV (target/unit/time/numeric blocks all present) and on `tests/fixtures/profiler/target_drifting.csv` (overall 0.5, weekly_range [0.25, 0.75], verdict drifting = the hand-computed expectation); two runs byte-identical. Full suite re-run on real Python 3.12.10 before signing: **1629 tests OK**; `gen-finding-catalogue.py --check` current at 279; `node install.mjs --check` self-test passed (6/6 agents, 14/14 skills, 5 gates).
