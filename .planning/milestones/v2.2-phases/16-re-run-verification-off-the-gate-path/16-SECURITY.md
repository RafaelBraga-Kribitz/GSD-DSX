---
phase: 16
slug: re-run-verification-off-the-gate-path
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-08-29
---

# Phase 16 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> **State B run** (no prior SECURITY.md): the 13-entry register was consolidated from the
> `<threat_model>` blocks of all four 16-0x plans (`register_authored_at_plan_time: true`);
> the four plans each declared `T-16-SC` identically, deduped here to one supply-chain
> accept. No SUMMARY carried a `## Threat Flags` section (grep-confirmed), so nothing was
> added outside the plan-time register. `asvs_level: 1` (config `security_asvs_level: 1`) +
> `register_authored_at_plan_time: true` + `threats_open: 0` → the workflow's L1
> short-circuit applies (no auditor spawn; grep/AST-depth is sufficient at Level 1). Every
> mitigation was **re-gated directly by the orchestrator** with real commands (brief §5 —
> never trusted from a report). Phase 16 splits reproduction across a trust boundary: the
> `dsx-reproduce` **skill** runs the analysis entrypoint in the agent runtime and writes
> `REPRO-REPORT.md`; the deterministic **gate** only reads the report's machine block and
> executes nothing. There is **no untrusted input and no executable surface on any
> deterministic gate path**, so ASVS L1 injection / auth / session vectors are all N/A. The
> residual STRIDE surface is Tampering / Elevation-of-Privilege — a future "simplification"
> pulling entrypoint execution or a data library onto the gate, a fabricated verdict being
> trusted, a silent catalogue mint/drop, or the additive `protocol_adherence` field leaking
> into the calibration numbers.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| spec + `REPRO-REPORT.md` → gate check | `dsx/checks/repro.py` reads the spec's `reproducibility.reproduce_report` opt-in string and the named report's fenced machine block via `Path.read_text` + stdlib `re`; it parses one number with `math.isclose`, opens no data file, imports no tabular library, and **never executes the declared entrypoint** (D-01). | in-repo markdown (internal) |
| `dsx-reproduce` skill runtime → entrypoint | The skill executes `reproducibility.entrypoint` via Bash in the agent runtime — the **only** sanctioned execution site. The gate never crosses this boundary; producing the report (execution) and checking it (declaration) sit on opposite sides of the purity boundary (D-01). | analysis entrypoint (agent runtime only) |
| skill → report → gate (verdict-agnostic) | The skill writes the numbers + a `status`; the gate re-derives overlap from the numbers alone and **ignores any PASS/FAIL verdict line** — a fabricated PASS with disagreeing numbers still emits `DSX-REP-061` (D-04). An honest `skipped`/`unable` short-circuits `061` without exiting 1 (D-11). | operator-authored report (numbers, not verdict) |
| corpus sidecar → test harness only | `protocol_adherence` lives on `*-ATTRIBUTION.yaml` sidecars read only by the corpus test at test time — never by a runtime gate — and is reported **beside** catch rate / FPR, never inside them (D-10). | test-only YAML (no gate read) |

---

## Threat Register

*Consolidated from the four plans' `<threat_model>` blocks; phase-unique IDs assigned by the
plan authors, plan of origin in the component column. `block_on = high`, so only OPEN threats at
high+ count toward `threats_open`. Re-gate ranges: gate-path diff `ec216b2..HEAD` (the S3-2
baseline through the landed phase); the four feature commits are 1195d97 / 71454f6 / e32f9e6 / 0bd6a75.*

| Threat ID | Category | Component (plan) | Severity | Disposition | Mitigation | Status |
|-----------|----------|------------------|----------|-------------|------------|--------|
| T-16-01 | Tampering | A future "simplification" shelling / runpy-ing the entrypoint from the check to "check it runs" (16-01) | critical | mitigate | D-01: the check is `Path`+`re`+`math` only. Re-gate: `grep` for `subprocess\|runpy\|os\|exec` in `dsx/checks/repro.py` → **none**; `test_no_entrypoint_execution` **3 OK** (AST scan) + `test_gate_path_hermetic` **2 OK**. | closed |
| T-16-02 | Tampering | Parsing the report with pandas/scipy/csv, pulling a data library onto the gate (16-01) | high | mitigate | D-01/D-04: the fenced block is parsed with stdlib `re` on `\r?\n`. Re-gate: `repro.py` imports are `math`/`re`/`pathlib` only; hermetic closure asserts `{pandas,scipy,numpy,csv}` absent → **2 OK**. | closed |
| T-16-03 | Tampering | Trusting a skill-authored PASS verdict so a non-reproducing analysis ships (16-01) | high | mitigate | D-04: the check reads only the numeric block + `status`. Re-gate: `test_verdict_pass_does_not_suppress_061` green (in `test_reproduce_report` **7 OK**) — a success verdict with disagreeing numbers still emits `DSX-REP-061`. | closed |
| T-16-04 | Tampering | A silent or cardinality-preserving catalogue mint/drop hiding the two new codes (16-01) | high | mitigate | D-08: `gen-finding-catalogue.py --check` **exit 0** at 258 + the two-leg invariant (count 258 AND set-identity vs snapshot ∪ {060,061}) → **2 OK**; the byte-frozen 256 snapshot anchor (`git diff ec216b2..HEAD -- tests/fixtures/finding-codes-phase12.md` **empty**) makes any drift name itself. | closed |
| T-16-05 | Denial of Service | A legitimately skipped reproduce (interpreter absent) firing `DSX-REP-061` and forcing exit 1 the ROADMAP forbids (16-01) | high | mitigate | D-11: the `skipped`/`unable` status short-circuits `061`. Re-gate: `test_061_short_circuits_on_skipped_status` green (in `test_reproduce_report` **7 OK**) — honest opt-out analogous to `DSX-REP-051`. | closed |
| T-16-10 | Elevation of Privilege | The reproduce execution creeping from the skill into a gate module (16-02) | critical | mitigate | D-01: execution stays in the skill (Bash, agent runtime); 16-02 edits no `dsx/` file. Re-gate: `git diff --stat ec216b2..HEAD -- dsx/` → **only `dsx/checks/repro.py`** (no execution primitive); AST scan + hermetic keep the gate execution-free. | closed |
| T-16-11 | Tampering | Template block schema drifting from the gate parser, so a valid report is misread (16-02) | medium | mitigate | D-04: the template's flat `metric: number` + `status` block is parsed by the same `\r?\n` extractor the 16-01 check uses. Re-gate: round-trip proven in `test_reproduce_report` **7 OK** (silent on overlap, fires on non-overlap using the template shape). | closed |
| T-16-12 | Spoofing | The skill fabricating a number or a PASS verdict to force a green gate (16-02) | high | mitigate | D-04/D-11: on failure the skill writes `status: skipped`/`unable` with no fabricated numbers; the gate trusts numbers, not the status/verdict. Re-gate: `test_verdict_pass_does_not_suppress_061` green — a fabricated PASS with bad numbers still fails `061`. | closed |
| T-16-20 | Tampering | `protocol_adherence` silently entering the catch-rate/FPR denominators or `_headline`, moving calibration (16-03) | high | mitigate | D-10: the field is a sidecar key, not a `_headline` parameter. Re-gate: `test_protocol_adherence_is_additive_and_ignored` green (in `test_known_bad_corpus` **45 OK**) — field absent from `_headline.__code__.co_varnames`; headline pair pinned `(0.25,0.3)`; anchor tests unedited. | closed |
| T-16-21 | Tampering | The field being placed on an `ANALYSIS-SPEC.yaml`, changing gate findings or tripping a schema check (16-03) | high | mitigate | D-10: the field goes on the sidecar only. Re-gate: `git diff --stat ec216b2..HEAD -- examples/known-bad/**ANALYSIS-SPEC.yaml` → **empty**; only the 3 `*-ATTRIBUTION.yaml` sidecars changed (0 fixture deletions); `test_known_bad_corpus` **45 OK** (per-fixture findings byte-unchanged). | closed |
| T-16-30 | Tampering | A future gate module shelling / runpy-ing the entrypoint — a stdlib execution primitive the import-based hermetic test cannot catch (16-04) | critical | mitigate | D-09: the static AST scan over `dsx/checks/` + `dsx/frame/` denylists `subprocess`/`os`/`runpy`/`exec`/`eval`/dynamic-compile-import and asserts the union empty. Re-gate: `test_no_entrypoint_execution` **3 OK** — the execution-detecting complement to the import hermetic test. | closed |
| T-16-31 | Tampering | A vacuous scanner (empty/mis-scoped walk, or a substring grep false-positiving on a docstring) passing green while proving nothing (16-04) | high | mitigate | D-09 anti-vacuity: the scanned set is asserted non-empty and to include `code.py` + `repro.py`; a positive control asserts `subprocess.run`/`runpy.run_path` flagged; a negative control asserts `ast.*`/`re.compile` not. Re-gate: `test_no_entrypoint_execution` **3 OK**. | closed |
| T-16-SC | Tampering | npm/pip/cargo installs (all four plans) | n/a | accept | No package installs occur; the deliverables are a skill markdown, a template, a JSON registration, YAML sidecar edits, and stdlib-only tests. | closed |

*Status: open · closed — 13 entries, 12 threats + 1 supply-chain accept; 3 critical + 8 high + 1 medium, all closed.*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on (`high`) count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-16-SC | T-16-SC | Skill/template/test/YAML phase; no dependency manifest changed in the phase diff; the check and every new test are stdlib-only. Design-time disposition recorded identically in all four plan `<threat_model>` blocks; not a fresh mitigate→accept. | brief D-01 (standing) | 2026-08-29 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-29 | 13 | 13 | 0 | orchestrator direct re-gate (L1 short-circuit; no auditor spawn — skill/template/test phase, asvs_level 1) |

**Independent re-gate evidence (orchestrator, brief §5 — real commands, not a report):**
- **Gate-path purity (T-16-01/02/10/30):** `git diff --stat ec216b2..HEAD -- dsx/ scripts/` → **only `dsx/checks/repro.py`** (+109), `scripts/` clean. `repro.py` imports are `math` / `re` / `pathlib.Path` + internal `..findings`/`..spec` only — a `grep` for `pandas|scipy|numpy|csv|subprocess|runpy|os|shutil` imports returns **none** (the lone `numpy` token in the file is a `DSX-REP-001` remedy *string*, not an import).
- **Entrypoint-execution guard (T-16-01/10/30/31, D-09):** `python -m unittest tests.test_no_entrypoint_execution` → **3 OK** — static AST scan over `dsx/checks` + `dsx/frame`; non-empty named set incl. `code.py` + `repro.py`; positive control flags `subprocess.run`/`runpy.run_path`/`os.system`/`exec`; negative control clears `ast.*`/`re.compile`.
- **Gate-path hermeticity (T-16-02):** `python -m unittest tests.test_gate_path_hermetic` → **2 OK** (no pandas/scipy/numpy/csv in the union closure of every gate root).
- **Verdict-agnostic + honest-skip (T-16-03/05/11/12, D-04/D-11):** `python -m unittest tests.test_reproduce_report` → **7 OK** — `060` strict-only; `061` fires on disagreement and is **not** suppressed by a PASS verdict; silent on absent/overlap/`skipped`; good-fixture back-compat.
- **Zero-mint / set-identity (T-16-04, D-08):** `python -m unittest tests.test_finding_catalogue_invariant` → **2 OK** (count 258 AND set-identity `current == snapshot ∪ {DSX-REP-060, DSX-REP-061}`); `python scripts/gen-finding-catalogue.py --check` → **exit 0**. Both codes are **HIGH** in `references/finding-codes.md`; the frozen `tests/fixtures/finding-codes-phase12.md` anchor is byte-unchanged over the phase.
- **Additive calibration (T-16-20/21, D-10):** `python -m unittest tests.test_known_bad_corpus` → **45 OK** incl. `test_protocol_adherence_is_additive_and_ignored`; the 3 remaining corpus cases carry `protocol_adherence` on their sidecars; `examples/known-bad/**ANALYSIS-SPEC.yaml` diff over the phase is **empty**.
- **Citation authenticity:** the two new codes (`DSX-REP-060`/`061`) are engineering-hygiene checks that cite no primary source (brief.md:389 assigns none — **no D-05 owed by Phase 16**); every code the phase's artifacts reference resolves in `references/finding-codes.md`.
- **Full gate** `sh scripts/check.sh` → **all checks passed** (`Ran 1263 tests … OK`, catalogue current at 258, capability manifest conformant — **14 skills**, gate contract good/bad/missing, determinism identical). The `declared twice` warnings are the pre-existing S0-2 shipped-tree noise — both gates exit 0.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-08-29 — gate **SECURED**, `threats_open: 0`, 13/13 closed by orchestrator re-gate. **Human sign-off granted 2026-08-29 (operator verdict recorded in HUMAN-QUEUE.md, item HQ-12):** the sign-off line above is approved as written, and the phase's UAT is confirmed. Phase 16 is now both technically verified and human-approved.
