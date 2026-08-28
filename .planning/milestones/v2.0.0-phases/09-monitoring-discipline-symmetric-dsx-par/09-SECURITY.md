---
phase: 09
slug: monitoring-discipline-symmetric-dsx-par
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
security_block_on: high
register_authored_at_plan_time: true
created: 2026-08-13
---

# Phase 09 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

Register built from the `<threat_model>` blocks of all 7 Phase 9 plans (State B —
no prior SECURITY.md). Every plan carried a parseable threat model, so this is a
**verify-mitigations** audit, not a retroactive STRIDE reconstruction. ASVS L1
grep-depth: mitigations located in the shipped code and tests; the 526-test
suite was already green at verification.

Plan-local IDs collided across 09-05 and 09-06 (`T-9-13`, `T-9-14`, `T-9-15`).
Those rows are disambiguated with a plan suffix. Repeated `T-9-SC` rows are
collapsed to one accepted risk. `T-9-01` / `T-9-02` / `T-9-07` were restated
across successive plans; the strongest (latest) mitigation is recorded.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| operator-authored `ANALYSIS-SPEC.yaml` → `dsx/frame/paradigm.py` | Untrusted YAML decides CRITICAL monitoring findings and a HIGH requiredness finding | Untrusted structured data |
| `inference:` free-text clearing fields → gate verdict | A value that looks declared while carrying no content is a gate bypass | Untrusted scalars |
| `dsx/spec.py` shared helpers → every check family | Editing `is_blank` would retype 138 call sites | Shared predicate |
| finding severity → process exit code | `GATE_THRESHOLDS` turns severity into an exit code | Repository-controlled enum |
| `tests/` → `dsx/` | A simulation under `tests/` must never become reachable from the gate path | Import edges |
| published literature → committed docstring / emitted `detail=` | A locator is a claim about a source; a wrong one carries the tool's authority | Citation text |
| `references/paradigm-symmetry.md` → reader's belief about the tool | The audit is what an external reader trusts about cheapest dishonest paths | Committed documentation |
| finding-code ownership (`DSX-SPEC-085` vs `DSX-PAR-002`) | Membership vs requiredness; a boundary crossing emits two codes for one defect | Finding codes |
| `suppressions[]` → blocking set | An operator can remove a finding with a written authority pointer | Operator-authored YAML |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-9-01 | Tampering | `inference.decision_threshold` and other free-text clearing declarations | high | mitigate | Gate path applies `is_blank` / `is_blank_text` only — no parse, eval, or arithmetic. `test_arbitrary_decision_threshold_string_produces_identical_finding_text` | closed |
| T-9-02 | Denial of Service | malformed / nested `inference:` and `design:` values | medium | mitigate | Reads go through existing `get`, `is_blank`/`is_blank_text`, `normalize` — none raise on a missing or oddly shaped key | closed |
| T-9-03 | Spoofing | Armitage citation locator | high | mitigate | Docstring names verified bibliographic fields only and states the full text is subscriber-only; no table or page claimed (`dsx/mathx.py`, `dsx/frame/paradigm.py`) | closed |
| T-9-04 | Elevation of Privilege | a `tests/` module becoming reachable from the gate path | high | mitigate | `tests/test_par_monitoring_simulation.py::test_no_module_under_dsx_imports_from_tests` AST-scans `dsx/` | closed |
| T-9-05 | Tampering | non-reproducible simulation output | medium | mitigate | `random.Random(<literal>)` plus a determinism test that reruns the same seed | closed |
| T-9-06 | Tampering | asymmetric severity between `DSX-PAR-010` and `DSX-PAR-011` | high | mitigate | Both `report.add` at `CRITICAL`; undeclared case yields both codes; suite asserts severity | closed |
| T-9-07 | Tampering | `references/paradigm-symmetry.md` drifting from live clearing conditions | high | mitigate | `test_paradigm_symmetry_audit_enumerates_both_halves` derives required substrings from `_MONITORING_DISCIPLINE` at runtime | closed |
| T-9-08 | Elevation of Privilege | undeclared-paradigm escape past `dsx gate plan` | high | mitigate | Blank/absent paradigm selects every `_MONITORING_DISCIPLINE` row; exit-code tests pin two CRITICAL findings | closed |
| T-9-09 | Repudiation | suppressing a genuine `DSX-PAR-010`/`-011` via `suppressions[]` | medium | accept | Existing authority requirement (reason + pointer; unknown code → exit 2). Intended M-07 grandfather path. See accepted-risks log | closed |
| T-9-10 | Information Disclosure | operator free text in `DECISIONS.jsonl` | low | accept | Trail is operator-controlled and contains only operator-authored text. See accepted-risks log | closed |
| T-9-11 | Repudiation | corpus docs claiming a shipped defect is still unadjudicated | high | mitigate | Catch-attribution and bound-value tests in `tests/test_known_bad_corpus.py` | closed |
| T-9-12 | Tampering | line-ending-sensitive guards on a CRLF checkout | medium | mitigate | Content matching is whitespace-normalized with no line anchors | closed |
| T-9-13 | Tampering | per-member / per-paradigm path ranking one justification above another | high | mitigate | Remedy iterates live `PARADIGM_JUSTIFICATIONS` in sorted order; 14-case parametrised test in `TestPhase9ParadigmJustification` | closed |
| T-9-13b | Elevation of Privilege | `_blank_clearing_declarations` cleared by bare `0`/`False`/containers | high | mitigate | `is_blank_text`; 48-case matrix at verification; type-domain tests in `TestPhase9MonitoringDiscipline` | closed |
| T-9-14 | Repudiation | `DSX-PAR-002` double-firing with `DSX-SPEC-085` | high | mitigate | Membership-free check (D-08). Canonical bad fixture pinned at three `DSX-SPEC-085` and zero `DSX-PAR-002`. UAT 2026-08-13 accepted the split | closed |
| T-9-14b | Tampering | tightening `is_blank` itself (138 call sites) | high | mitigate | New separately-named `is_blank_text`; `is_blank` body left byte-identical; positive test that `is_blank(0)` is still `False` | closed |
| T-9-15 | Information Disclosure | operator free text echoed into the decision trail (09-05) | low | accept | Record `counterfactual` names field names, not values. See accepted-risks log | closed |
| T-9-15b | Repudiation | audit cheapest-path claim factually wrong while reading as authoritative | high | mitigate | Audit rewritten ("What does not clear either half"); runtime enumeration test kept | closed |
| T-9-16 | Tampering | line-anchored assertions over a CRLF checkout (09-06) | medium | mitigate | Same whitespace-normalized matching as T-9-12 | closed |
| T-9-17 | Spoofing | `DSX-PAR-011` emitted `detail=` locator error | high | mitigate | `test_dsx_par_011_detail_attributes_the_bound_without_a_locator_error` asserts on the live emitted string | closed |
| T-9-18 | Repudiation | Bayesian known-bad fixture comment repeating the locator error | high | mitigate | Fixture Formulation note rewritten; `_RETIRED_LOCATOR_ERRORS` corpus-wide negative guard | closed |
| T-9-19 | Tampering | correction by deletion rather than rewording | high | mitigate | Positive-content test keeps `Theorem 1`, `1/(K+1)` and `1/20 = 0.05` present | closed |
| T-9-20 | Tampering | line-wrap / CRLF fragility in the 09-07 guards | medium | mitigate | Whitespace-normalized matching; 09-07 SUMMARY records the guard catching a wrap that would have broken `1/20 = 0.05` | closed |
| T-9-SC | Tampering | npm/pip/cargo installs | low | accept | Phase installs no packages; stdlib-only gate path. See accepted-risks log | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `security_block_on: high` count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-9-01 | T-9-09 | Suppressing a genuine PAR-010/011 finding requires `suppressions[]` authority (reason + pointer); unknown codes exit 2. This is the M-07 grandfather path, not a silent bypass | plan 09-03 | 2026-08-13 |
| AR-9-02 | T-9-10, T-9-15 | Decision-trail content is operator-authored text written to an operator-controlled directory; no new sink | plans 09-03, 09-05 | 2026-08-13 |
| AR-9-03 | T-9-SC | No third-party installs; D-01 stdlib-only gate path | every 09-* plan | 2026-08-13 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-13 | 24 | 24 | 0 | Cursor Grok 4.6 (L1 grep-depth at UAT close) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-08-13
