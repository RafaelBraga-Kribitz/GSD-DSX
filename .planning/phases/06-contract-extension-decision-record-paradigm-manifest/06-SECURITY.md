---
phase: 06
slug: contract-extension-decision-record-paradigm-manifest
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
security_block_on: high
register_authored_at_plan_time: true
created: 2026-08-10
---

# Phase 06 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

Register built from the `<threat_model>` blocks of all 13 Phase 6 plans (State B —
no prior SECURITY.md). Every plan carried a parseable threat model, so this is a
**verify-mitigations** audit, not a retroactive STRIDE reconstruction.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| operator-authored `ANALYSIS-SPEC.yaml` → `dsx.loader.load()` | The primary untrusted-input boundary; parsed by the bundled stdlib parser, never executed | Untrusted YAML text |
| operator-authored `ANALYSIS-SPEC.yaml` → `validate_structure()` | Malformed or hostile shapes must degrade to a finding, never raise | Untrusted structured data |
| operator-authored `inference.paradigm` → `dsx/frame/paradigm.py` | A declared value read to select an applicability set; never used to skip a check | Untrusted string |
| `DECISIONS.jsonl` on disk → `read_all()` | Bytes that may be crash-truncated, hand-edited, corrupted at the filesystem level, or written by anyone with write access to the analysis directory | Untrusted JSONL |
| `read_all()` → `cmd_explain` | A read-only render path documented as never blocking | Parsed records |
| `read_all()` → `next_invocation_id()` → `_write_decision_trail` → `cmd_gate` | The read-before-write inside the gate path — the route by which trail state could reach a gate verdict | Parsed records |
| gate process → filesystem | The first write path in this codebase; target is the already-resolved spec root | Append-only audit records |
| `dsx/frame/` ↔ `dsx/checks/` | The D-03a module boundary — a blast-radius control on future package extraction | Import edges |
| repository source text → `ast.parse` in build scripts | Static analysis only; never executes the scanned module | Repository-controlled source |
| finding-code strings → `check_d05` coverage decision | The string match deciding whether a code is subject to D-05 citation enforcement | Repository-controlled identifiers |
| committed fixture specs → `dsx.loader.load()` | Repository-controlled input; the corpus's trust property is provenance, not hostility | Committed YAML |
| committed corpus prose / `dsx/spec.py` comments → a future phase author | Text asserting guarantees the code may not perform | Committed documentation |
| published version number → a user deciding whether to upgrade | The only signal read before pulling a breaking contract change | Release metadata |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-6-01 | Tampering | the D-03a module boundary | high | mitigate | `tests/test_frame_boundary.py` — `test_real_frame_modules_import_nothing_from_checks` plus a scanner self-test on violating/permitted sources | closed |
| T-6-02 | Denial of Service | `dsx.decisions.read_all` | medium | mitigate | Per-line `try/except json.JSONDecodeError: continue` (`dsx/decisions.py:153`) | closed |
| T-6-02b | Denial of Service | `cmd_explain` | medium | mitigate | Outer `except Exception` returning 0 (`dsx/cli.py:520`); `read_all` cannot raise for any on-disk state | closed |
| T-6-03 | Tampering / Information Disclosure | `decisions_path()` write target | low | accept | `--spec`/`--phase-dir` resolve operator-supplied paths by design; local single-user CLI | closed |
| T-6-04 | Tampering | `dsx/loader.py::_NULL`, `none`-valued frame fields | medium | mitigate | Parser-agreement test against PyYAML, six-case regression test, audited `== "none"` comparison sites | closed |
| T-6-05 | Repudiation | `dsx.decisions.append` / trail completeness | medium | mitigate | `flush()` + `os.fsync(fh.fileno())` per record (`dsx/decisions.py:119`); append-only two-invocation test | closed |
| T-6-06 | Availability | unbounded `DECISIONS.jsonl` growth | low | accept | Out of scope per `06-CONTEXT.md`; no REQ-P6-* requires rotation | closed |
| T-6-07 | Spoofing | D-05 citation markers | medium | mitigate | `_CITATION_RE` + `check_d05` (`scripts/gen-finding-catalogue.py:70,250`) reject a missing `Citation:` line | closed |
| T-6-08 | Tampering | `_D05_ALLOWLIST_PREFIXES` | high | mitigate | Literal tuple inside the script (`scripts/gen-finding-catalogue.py:58`), asserted by two tests | closed |
| T-6-09 | Repudiation | `suppressions[]` documented as a migration path | medium | mitigate | README states the authority requirement as a requirement (DSX-SPEC-070); human-validated in UAT test 2 | closed |
| T-6-10 | Repudiation | `SELF-001` convention | low | accept | Evidence-free reversal is undetectable in v2.0.0 by design (M-05: planning-process concern) | closed |
| T-6-11 | Tampering | the two canonical D-08 fixtures | high | mitigate | `test_good_fixture_passes_every_gate`, `test_bad_fixture_blocks_at_plan`, `test_bad_fixture_blocks_at_ship` — all passing | closed |
| T-6-12 | Denial of Service | `_validate_validity_frame_shape` | medium | mitigate | Non-dict `validity_frame` degrades to `DSX-SPEC-080` rather than raising (`dsx/spec.py:731`) | closed |
| T-6-13 | Tampering | the D-13 boundary | medium | mitigate | Decision records emitted from `dsx/frame/`, not an existing v1.5.0 check module | closed |
| T-6-14 | Spoofing | `DSX-PAR-001` manifest content | high | mitigate | `dsx/frame/paradigm.py` + registration asserted at all four default gate thresholds (`tests/test_dsx.py:1395`) | closed |
| T-6-15 | Elevation of Privilege | INFO severity flipping a gate exit code | low | accept | `Severity.INFO` is 10; every default `GATE_THRESHOLDS` value is 40 or 50 | closed |
| T-6-16 | Spoofing | post-mortem provenance | high | mitigate | 13 provenance tests in `tests/test_known_bad_corpus.py`; unverifiable locators flagged, not invented. Human-validated in UAT test 3 | closed |
| T-6-17 | Tampering | the Bayesian fixture's formulation | high | mitigate | `test_no_corpus_file_misattributes_the_prior_averaged_bound`, `test_no_planning_document_misattributes_the_prior_averaged_bound`, `test_bayesian_postmortem_states_the_deng_bound_and_its_value`. Human-validated in UAT test 4 | closed |
| T-6-18 | Tampering | `DSX-EXP-060` double-firing | medium | mitigate | Single-emission assertion in the corpus gate tests | closed |
| T-6-19 | Denial of Service | the gate-path trail write | high | mitigate | `_write_decision_trail` wrapped in `try/except Exception` (`dsx/cli.py:315`); the write is a side channel that cannot change `cmd_gate`'s exit code | closed |
| T-6-19b | Denial of Service | `_write_decision_trail` → `cmd_gate` exit code | high | mitigate | `read_all` uses `errors="replace"` + `except OSError` (`dsx/decisions.py:143-144`); call-site guard widened to `Exception`; control-comparison regression tests assert corrupted-trail exit == no-trail exit | closed |
| T-6-20 | Spoofing | version declarations across four manifests | medium | mitigate | Verified live: `dsx/__init__.py`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `capabilities/dsx/capability.json` and both `repro_lock.dsx_version` fixtures all read `2.0.0` | closed |
| T-6-21 | Repudiation | the finding catalogue | medium | mitigate | `--check` mode in `scripts/gen-finding-catalogue.py:286` fails on a stale catalogue | closed |
| T-6-22 | Tampering | `DECISIONS.jsonl` content | low | accept | Reader treats content strictly as data (`json.loads`, never `eval`); trail is change-detection, not a security control | closed |
| T-6-23 | Repudiation | concurrent invocation-id allocation | medium | accept | Racing `dsx gate` processes can collide on one identifier. Accepted for this milestone; documented at function, module and README level. Advisory-lock remedy deferred | closed |
| T-6-24 | Information Disclosure | the widened exception guards | low | mitigate | Tests assert degraded *output* (surviving invocation id reaches `dsx explain` stdout), not exit codes alone; caught exception surfaced on stderr under `--verbose` | closed |
| T-6-25 | Repudiation | committed corpus documentation | medium | mitigate | Corpus guarantees stated as falsifiable and machine-checked rather than asserted in prose | closed |
| T-6-26 | Tampering | the retired over-claims | low | mitigate | `test_no_corpus_file_repeats_a_retired_gate_overclaim` | closed |
| T-6-27 | Denial of Service | the new gate-driving tests | low | accept | Test-suite runtime cost only; suite completes in 6.4s | closed |
| T-6-28 | Tampering | test artifacts written into `examples/` | low | mitigate | `--phase-dir` points writes at a temp directory, leaving fixtures clean | closed |
| T-6-29 | Tampering | `check_d05`'s coverage boundary | medium | mitigate | Hyphen-terminated family prefixes plus an explicit `_D05_ALLOWLIST_CODES` frozenset (`scripts/gen-finding-catalogue.py:57,66`) — no bare numeric-string prefix matching | closed |
| T-6-30 | Repudiation | committed comments in `dsx/spec.py` | low | mitigate | Comments corrected to state what the code actually enforces | closed |
| T-6-31 | Tampering | minting a finding code inside a cleanup | medium | mitigate | Catalogue `--check` gate forces any new code through citation enforcement | closed |
| T-6-32 | Denial of Service | the collapsed test helper | low | accept | A wrong collapse breaks the D-03a boundary proof loudly rather than degrading it silently | closed |
| T-6-SC | Tampering | package-manager installs (npm/pip/cargo) | low | accept | Zero third-party installs ship in this phase (D-01, stdlib-only). `06-RESEARCH.md` Package Legitimacy Audit records the gate as not applicable; asserted by `import dsx` succeeding with PyYAML absent | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` (high) count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-06-01 | T-6-03 | `--spec`/`--phase-dir` resolve arbitrary operator-supplied paths by design; a local single-user CLI has no privilege boundary to cross | Phase 6 plan author (06-02, 06-09) | 2026-08-10 |
| AR-06-02 | T-6-06 | Trail rotation is explicitly out of scope per `06-CONTEXT.md`; no REQ-P6-* requires it | Phase 6 plan author (06-02) | 2026-08-10 |
| AR-06-03 | T-6-10 | An evidence-free reversal is undetectable in v2.0.0 by design — M-05 makes enforcement a planning-process concern, not a gate concern | Phase 6 plan author (06-04) | 2026-08-10 |
| AR-06-04 | T-6-15 | `Severity.INFO` (10) cannot reach any default `GATE_THRESHOLDS` value (40/50), so the manifest is structurally unable to block | Phase 6 plan author (06-07) | 2026-08-10 |
| AR-06-05 | T-6-22 | The trail reader treats content strictly as data; the trail is change-detection, not a security control, matching `frame_digest`'s recorded disposition | Phase 6 plan author (06-11) | 2026-08-10 |
| AR-06-06 | T-6-23 | Concurrent-invocation id collision is real but unexercised by this milestone's single-process suite; the advisory-lock remedy is deferred with recorded reasoning and documented at three levels | Phase 6 plan author (06-11) | 2026-08-10 |
| AR-06-07 | T-6-27 | Cost is test-suite runtime only; the full suite completes in 6.4s | Phase 6 plan author (06-12) | 2026-08-10 |
| AR-06-08 | T-6-32 | A wrong collapse breaks the D-03a boundary proof loudly rather than degrading it silently | Phase 6 plan author (06-13) | 2026-08-10 |
| AR-06-09 | T-6-SC | Zero third-party installs ship in this phase (D-01, stdlib-only gate path); no `[ASSUMED]`/`[SUS]` package exists to gate on | Phase 6 plan author (all 13 plans) | 2026-08-10 |

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-10 | 35 | 35 | 0 | /gsd-secure-phase 06 (orchestrator, ASVS L1) |
| 2026-08-10 | 35 | 35 | 0 | /gsd-secure-phase 06 re-verification (State A audit, ASVS L1) |

**Verification depth.** ASVS L1 (grep depth) per `workflow.security_asvs_level: 1`.
All 8 high-severity threats were confirmed against named implementation sites and
named passing tests, not against plan prose alone. Full suite re-run during this
audit: **306 passed, 239 subtests passed in 6.40s.**

**Re-verification (State A audit).** The register was re-derived from the 13 plan
`<threat_model>` blocks and matched this file exactly — 35 threat IDs, no additions,
no orphans. Closure evidence was re-checked against the live tree rather than
against this file's own claims:

- **T-6-01** `tests/test_frame_boundary.py:93` — `test_real_frame_modules_import_nothing_from_checks` present
- **T-6-08 / T-6-29** `scripts/gen-finding-catalogue.py:58,66` — `_D05_ALLOWLIST_PREFIXES = ("DSX-PAR-",)` and the five-code `_D05_ALLOWLIST_CODES` frozenset both literal in-script
- **T-6-11** `tests/test_dsx.py:1192,1198,1204` — all three fixture-gate tests present
- **T-6-14** `dsx/frame/paradigm.py` present; `DSX-PAR-001` asserted at `tests/test_dsx.py:1395`
- **T-6-16** `tests/test_known_bad_corpus.py` — 13 test functions, matching the claimed count
- **T-6-17** `tests/test_known_bad_corpus.py:270,292,310` — all three bound-attribution guards present
- **T-6-19** `dsx/cli.py` — `_write_decision_trail` body ends in `except Exception`, stderr only under `--verbose`
- **T-6-19b** `dsx/decisions.py:142-144` — `errors="replace"` + `except OSError: return []`
- **T-6-02 / T-6-02b** tolerant per-line `except json.JSONDecodeError: continue`; `cmd_explain` outer `except Exception` returning 0
- **T-6-05** `dsx/decisions.py:118-119` — `flush()` + `os.fsync(fh.fileno())`
- **T-6-20** `2.0.0` confirmed in `dsx/__init__.py:9`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `capabilities/dsx/capability.json`

Gates re-run at re-verification time: full suite **306 passed, 239 subtests passed
in 6.22s** (identical counts, timing variance only), and
`python scripts/gen-finding-catalogue.py --check` → exit 0, "finding catalogue is
current". No open threat at or above the `high` block threshold. Summaries still
carry no `## Threat Flags` sections, so the register remains plan-sourced.

**Register origin.** All 13 plans carried a `<threat_model>` block, so
`register_authored_at_plan_time: true` and the audit verified mitigations rather
than reconstructing a register. Summaries carried no `## Threat Flags` sections;
the register is sourced entirely from the plans.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-08-10
