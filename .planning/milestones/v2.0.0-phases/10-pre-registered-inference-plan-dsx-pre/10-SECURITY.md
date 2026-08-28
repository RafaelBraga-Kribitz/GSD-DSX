---
phase: 10
slug: pre-registered-inference-plan-dsx-pre
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-08-24
verified: 2026-08-24
---

# Phase 10 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.

First-time security audit (State B: no SECURITY.md previously existed). The register was
built from the `<threat_model>` block in each of the six executed plans
(`10-01-PLAN.md` … `10-06-PLAN.md`, all authored at plan time —
`register_authored_at_plan_time: true`), consolidated by the orchestrator, then
independently verified by `gsd-security-auditor` (opus) against the live tree and the
test suite rather than taken on the plans' word, and re-gated a second time by the
orchestrator. Several threat IDs (T-10-03, -10, -13, -14, -SC) were declared in more than
one plan for the same guarantee treated from a different angle — consolidated below into a
single row each, with both treatments named.

The load-bearing new element of this phase is trust boundary 2: `DECISIONS.jsonl`, a file
that was previously written and never read, becomes a gate **input** that can stop a run.
That is why Phase 10 warranted its own security pass even though the earlier phases were
already secured.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| operator-authored YAML → gate parser | `inference.fallback_rule`, `inference.primary_procedure`, `analysis.test` and `inference.declared_at` are all free text written by the operator and read by the gate. `fallback_rule` is parsed by a regular expression; `declared_at` is a self-declaration the tool cannot verify (the exact limit REQ-P10-02 exists to name). This is the only externally-authored input on the gate path. | Spec YAML fields (untrusted text) |
| on-disk `DECISIONS.jsonl` → gate input | **New in this phase.** A file previously written and never read becomes an input that can stop a gate run. It is operator-writable and carries no spec identity, so a shared trail root can mix specifications. | Invocation-header records, `frame_digest` bytes |
| command-line invocation → check scope | Which command was run now determines whether a stateful precondition (the content lock) applies. `cmd_gate` at verify/ship reconciles the trail; read-only `cmd_audit` must not, or it becomes a requirement no command sequence can satisfy. | `gate_invocation` flag, gate point |
| finding text (`detail` / `remedy`) → operator | The emitted explanation is the only account an operator gets for a blocked run. A misleading remedy causes the gate to be read as broken and worked around. | Finding prose |
| documentation (`README`) and citation record (`brief.md` §7) → operator / future work | A limit described as a guarantee transfers unearned confidence; a confident-looking citation locator launders into every later phase that reads it. | Coverage claims, citation locators |
| committed fixture → corpus test suite | The fixture is the executable evidence for REQ-P10-04. If it silently stops encoding its defect, the requirement's only committed proof disappears without anything going red. | Known-bad fixture spec |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-10-01 | Repudiation | `_check_content_lock` ordering (operator may re-run `dsx gate plan` after seeing results) | medium | accept | Documented limit, not enforced: blocking a re-run would also block legitimate refinement before execution. Named in the DSX-PRE-020 remedy (`dsx/frame/prereg.py:588-591`) and README (`:500-504`); `TestDocumentedLimits` test 7 pins the remedy text. | closed (accepted) |
| T-10-02 | Denial of Service | `_parse_fallback_rule` / `_CONDITION_RE` | high | mitigate | `_CONDITION_RE` fully anchored `^…$` with no nested quantifier (no catastrophic-backtracking exposure) at `prereg.py:35-39`; `match is None` → `CheckError` (controlled exit 2) at `:92-96`; arrow-with-no-branch → `CheckError` at `:99-103`; never a raw traceback. `TestFallbackRuleParsing` tests 7-10 pass. | closed |
| T-10-03 | Tampering | pre-registration guarantee vs. an unknown/undeclared fact (`_resolve_branch`/`PREREG_FACTS`; `_check_rule_resolves`) | high | mitigate | Two treatments of one guarantee: the fact namespace is a closed registry `_PREREG_FACTS_NORMALIZED` built from `PREREG_FACTS` (`prereg.py:133-135`, resolve at `:168-204`), and an unknown/undeclared fact emits **DSX-PRE-010 at CRITICAL** (`:247-258`) rather than resolving silently. `TestBranchResolution` 5-7 + `TestRuleResolutionFindings` 1-2 pass. | closed |
| T-10-04 | Spoofing | `InvocationHeader` record shape (a shared trail root mixes specs) | medium | mitigate | Reconciliation compares set membership of the current `frame_digest` (`current_digest not in recorded`, `prereg.py:568`) rather than picking a header by order — order-independent, removes the cross-spec false positive without changing a shipped record shape. `TestContentLockReconciliation` test 5 passes. | closed |
| T-10-06 | Repudiation | `_D05_ALLOWLIST_PREFIXES` (citation obligation silently unenforced) | high | mitigate | `"DSX-PRE-"` present in the inclusion tuple (`scripts/gen-finding-catalogue.py:76`); inclusion enforced via `startswith(_D05_ALLOWLIST_PREFIXES)` at `:327`; `--check` exits 0; the family is genuinely inspected, not skipped. Live `# D-05:` markers in tests. | closed |
| T-10-07 | Spoofing | `report.add` title arguments | low | mitigate | Code and severity are literal string constants at every call site, so the catalogue extractor records what actually fires. `gen-finding-catalogue.py --check` exit 0, catalogue current. | closed |
| T-10-08 | Denial of Service | `check()` on malformed (non-dict) input | medium | mitigate | Non-dict guards at every level return an empty report / unresolved rather than raising (`prereg.py:640`, `:168-173`, `:320-324`), matching the shipped `interference.check` habit. `TestMalformedShapesDegradeGracefully` (4 tests) pass. | closed |
| T-10-09 | Denial of Service | trail read on corrupt/truncated input | medium | mitigate | `_recorded_plan_digests` relies on `read_all` (which never raises for any on-disk state) and adds no try/except, so a corrupt trail degrades to the documented missing-header path (`prereg.py:390-424`) rather than a traceback. `TestMissingPlanHeader` test 7 passes. | closed |
| T-10-10 | Elevation of Privilege | (a) missing plan-time header vs. the M-07 grandfather route; (b) trail precondition on read-only commands | high | mitigate | (a) `_has_grandfather_suppression` (`prereg.py:427-452`) is checked **before** the `CheckError` raise (`:542-543`) — the route is runtime-functional, not just named: a real DSX-PRE-020 suppression with reason+authority lets `dsx gate verify` proceed (`TestMissingPlanHeader` test_6/test_10, `TestAdHocCommandScope` test_6), while missing reason/authority/unknown-code do NOT unlock (test_11-14). Fixes REVIEW CR-01 (route once inert, `d8ff23e`). (b) `cmd_audit` never passes `gate_invocation=True` (`cli.py:272-278`); only `cmd_gate` does (`:318`); `reconcile_trail = gate_invocation and gate_point in {verify,ship}` (`:185`). `TestAdHocCommandScope` 1-6 pass. | closed |
| T-10-11 | Denial of Service | `GATE_PROFILES` registration vs. the existing corpus | high | mitigate | `prereg` registered in `GATE_PROFILES["verify"]` (`cli.py:122`) and `["ship"]` (`:127`), absent from `plan`/`execute` (confirmed live: `prereg` ∈ verify,ship only). Harness `_gate_findings` guards `json.loads` (`except json.JSONDecodeError` → readable failure, `test_known_bad_corpus.py:546-552`) so a plain-text exit-2 message is legible; registration + harness repair landed together. Corpus suite 30/30 green — no fixture breaks with a decode error. | closed |
| T-10-12 | Repudiation | `_write_decision_trail` docstring drift | low | mitigate | Docstring narrowed to scope the write-path-only side-channel invariant and acknowledge the Phase-10 read side can block (`cli.py:345-356`) — the comment no longer contradicts behaviour. | closed |
| T-10-13 | Tampering | corpus incidental-gap allow-list `_INCIDENTAL_GAP_CODES` | high | mitigate | No `DSX-PRE-*` code is in the allow-list (`test_known_bad_corpus.py:64-80`; grep count 0); the target code lives in `_TARGET_DEFECT_CODES` (`:168`). `test_incidental_allowlist_names_no_slugs_own_target_code` (`:797`) forbids a target code being laundered into the allow-list and is not weakened. | closed |
| T-10-14 | Repudiation | citation locators in `brief.md` §7 and source docstrings | high | mitigate | Only sources verified during discussion are cited, at the verified locators; the Gelman & Loken "no numbered sections / OCR-symbol" locator warnings and the Nosek per-sentence-page scope warning are written into `brief.md:498-516` and the `prereg.py` docstrings (`:10-17`, `:215-223`, `:510-525`) so they cannot be tidied away without failing a test. `TestDocumentedLimits` test 8 passes. Citation authenticity itself was read during the phase (10-VERIFICATION.md: "Human Verification Required: None"). | closed |
| T-10-15 | Spoofing | committed fixture ceasing to encode its defect | medium | mitigate | `test_post_hoc_procedure_switch_fixture_blocks_verify_and_ship_naming_pre_030` (`test_known_bad_corpus.py:668`) asserts exit 1 + DSX-PRE-030 at CRITICAL at verify/ship, and the absence of any DSX-PRE code at plan/execute (`:710-717`) — both the positive and negative half are pinned. | closed |
| T-10-16 | Spoofing | README limit prose (a limit read as a guarantee) | high | mitigate | Each of the four limits is stated as what is NOT checked — `declared_at` self-declaration the tool "cannot verify" (`README.md:479-486`), `analysis.test` plan-time scaffolding (`:488-493`), content-lock ordering not enforced (`:495-504`), missing-lock exit-2 (`:506-511`); no sentence implies the gate can detect a false `pre_data` claim. `TestDocumentedLimits` tests 2-4 pin the sentences. The honest-tone judgment was carried by the phase verification pass (no human item outstanding). | closed |
| T-10-17 | Tampering | registry / documentation drift | low | mitigate | `test_5_every_prereg_fact_is_named_in_the_readme` iterates `PREREG_FACTS` rather than hard-coding the three names (`test_frame_prereg.py:1268`), so a registry member added without documentation fails a test. | closed |
| T-10-SC | Tampering | package-manager installs | low | accept | No package manager runs anywhere in the phase (grep across the 19-file phase dir clean — no pip/npm/cargo/poetry/conda). Brief D-01 restricts the gate path to the standard library; `prereg.py` imports only `operator`, `re`, `dataclasses` + internal modules. | closed (accepted) |

*Status: open · closed · open — below `high` threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` (`high`) count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

**`threats_open: 0`** — all 8 high-severity `mitigate` threats (T-10-02, -03, -06, -10, -11, -13, -14, -16) are verified present at the correct boundary with their named tests passing; the two `accept` dispositions (T-10-01, T-10-SC) are design-time acceptances documented in the plans. No open threat remains at or above the `high` block threshold.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-10-01 | T-10-01 | An operator can re-run `dsx gate plan` after seeing results and register the edited frame, clearing the content-lock check. Blocking this would also block legitimate refinement before execution, so it is documented as a known limit in the DSX-PRE-020 remedy and README rather than enforced — the honest treatment already given to `declared_at: post_data`. | Phase 10 plan 03 (design-time) | 2026-08-20 |
| AR-10-02 | T-10-SC | No package-manager install step exists anywhere in this phase's six plans; the gate path is standard-library only (`operator`, `re`, `dataclasses`), per brief D-01. | Phase 10 plans 01-06 (design-time) | 2026-08-20 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-24 | 17 | 17 (15 mitigate verified + 2 accept) | 0 | `gsd-security-auditor` (opus), first-time audit — register consolidated from six plan-time threat models, each mitigation verified present at its boundary with the named test executed (`tests.test_frame_prereg` 90/90, `tests.test_known_bad_corpus` 30/30, `tests.test_gen_finding_catalogue` 40/40, `gen-finding-catalogue.py --check` exit 0). Orchestrator independently re-ran the gate: prereg 90/90, corpus 30/30, `--check` exit 0, `"DSX-PRE-"` ∈ `_D05_ALLOWLIST_PREFIXES`, 0 DSX-PRE in `_INCIDENTAL_GAP_CODES`, `prereg` ∈ GATE_PROFILES verify+ship only. Verdict: SECURED. |

**Process note:** none of the six SUMMARY.md files carries a `## Threat Flags` section, so the executor's threat-flag channel did not fire this phase; the auditor swept the implementation directly. (Same process gap the 11.1.1 audit recorded — worth a template fix, not a phase-10 blocker.)

**Path reconciliation:** the plan threat models refer to the citation record as `brief.md` §7; that file lives at the repo root (`brief.md`), not `references/brief.md`. Verified present at the root.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer) — 17/17 (15 mitigate, 2 accept)
- [x] Accepted risks documented in Accepted Risks Log — AR-10-01, AR-10-02
- [x] `threats_open: 0` confirmed — re-audit 2026-08-24 (0 blocking threats; all 8 high `mitigate` verified closed)
- [x] `status: verified` set in frontmatter — set 2026-08-24 after the audit + orchestrator gate re-run

**Approval:** security audit PASSED 2026-08-24 — 17/17 threats closed/accepted, `threats_open: 0`, verified by `gsd-security-auditor` (opus) and independently re-gated by the orchestrator. This phase carries **no open risk-acceptance decision requiring a fresh human sign-off**: both `accept` dispositions (T-10-01, T-10-SC) were made at plan time by the plans and reconciled in `10-VERIFICATION.md`, which recorded "Human Verification Required: None". Nothing here is escalated to HUMAN-QUEUE.
