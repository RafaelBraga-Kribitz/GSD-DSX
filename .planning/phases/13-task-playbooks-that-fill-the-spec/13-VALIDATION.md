---
phase: 13
slug: task-playbooks-that-fill-the-spec
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-28
validated: 2026-08-28
---

# Phase 13 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> **State B run** (no prior VALIDATION.md): reconstructed from the five plans + SUMMARY files.
> Phase 13 is skill-only (prose playbooks), so the "behaviours" are the *structural invariants*
> each requirement promises. Rather than leave those as manual reads, the deterministic checks
> S1-4 ran by hand were **crystallised into a standing test** (`tests/test_phase13_playbooks.py`,
> 8 tests) alongside the pre-existing catalogue invariant — so all six requirements have green
> automated verification. Gap analysis: **0 gaps** → no `gsd-nyquist-auditor` spawned. Every
> command below was re-run by the orchestrator this firing (brief §5).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (no pytest / no third-party test framework in the repo) |
| **Config file** | none — `python -m unittest discover -s tests -q` (see `scripts/check.sh`) |
| **Quick run command** | `python -m unittest tests.test_phase13_playbooks tests.test_finding_catalogue_invariant -v` |
| **Full suite command** | `python -m unittest discover -s tests -q` (1230 tests as of 2026-08-28) |
| **Phase gate** | `sh scripts/check.sh` (full suite + `gen-finding-catalogue.py --check` + capability manifest + gate-contract good/bad/missing exit codes + determinism) |
| **Estimated runtime** | ~54 seconds (full suite: `Ran 1230 tests in ~54s`) |

---

## Sampling Rate

- **After every task commit:** Run `python -m unittest tests.test_phase13_playbooks -v`, plus `python scripts/gen-finding-catalogue.py --check` whenever a skill's cited codes or the catalogue change.
- **After every plan wave:** Run `python -m unittest discover -s tests -q` (full suite).
- **Before `/gsd-verify-work`:** `sh scripts/check.sh` must be green.
- **Max feedback latency:** ~54 seconds.

---

## Per-Task Verification Map

*State B reconstruction: every requirement maps to a named test that runs green.*

| Requirement | Observable behaviour | Test Type | Named passing test(s) | Status |
|-------------|----------------------|-----------|-----------------------|--------|
| REQ-P13-01 | The four router skills exist, are registered in `capability.json` (13 skills), and every `DSX-*` code they cite exists in the catalogue (route-and-cite, not restate) | unit | `tests.test_phase13_playbooks.TestPhase13Playbooks.test_req01_four_router_skills_exist_and_registered`, `…test_req01_cited_codes_all_exist_in_catalogue`, `…test_req02_router_skills_route_and_cite_no_parallel_advice` | ✅ green |
| REQ-P13-02 | `dsx-explore-data` writes a hypothesis register that routes an untested belief to `assumptions[]` (`DSX-COH-030/031`) and a promoted test to `design.multiplicity.family[]` (no new spec field) | unit | `tests.test_phase13_playbooks.TestPhase13Playbooks.test_req02_explore_data_hypothesis_register` | ✅ green |
| REQ-P13-03 | `dsx-narrate` carries the explicit **What / So What / Now What** shape over the existing 5-part structure, citing `DSX-COH-040` + `DSX-CLM-080` | unit | `tests.test_phase13_playbooks.TestPhase13Playbooks.test_req03_narrate_what_so_what_now_what` | ✅ green |
| REQ-P13-04 | `dsx-scope-analysis` routes lookup → Tier 0, ad-hoc → Tier 1, full pipeline → Tier 2, cites `docs/gsd-tiers.md`, emits `gsd-tier.ps1`, and stays **advisory** (no config mutation) | unit | `tests.test_phase13_playbooks.TestPhase13Playbooks.test_req04_scope_tier_routing_matches_doc`, `…test_req04_scope_routing_is_advisory_not_mutating` | ✅ green |
| REQ-P13-05 | The executor fragment prefers a `scripts/*.py` entrypoint over a notebook for `reproducibility.entrypoint`, citing `DSX-REP-040` (ordering fidelity, not leakage) | unit | `tests.test_phase13_playbooks.TestPhase13Playbooks.test_req05_executor_prefers_py_entrypoint` | ✅ green |
| REQ-P13-06 | No new `DSX-*` code ships: distinct-code SET identical to the frozen Phase-12 snapshot AND exactly 256 (mint-one/drop-one swap named, not just counted) | unit + build gate | `tests.test_finding_catalogue_invariant.TestCatalogueInvariant.test_code_set_is_set_identical_to_phase12_snapshot`, `…test_finding_catalogue_stays_at_256_codes`; `python scripts/gen-finding-catalogue.py --check` (exit 0) | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

The one new Wave-0 dependency (`tests/test_phase13_playbooks.py`) was created during this validation
run to crystallise the deterministic structural checks; `tests/fixtures/finding-codes-phase12.md`
was created in execution (13-05). Both are present in the tree; `wave_0_complete: true`.

- [x] `tests/test_phase13_playbooks.py` — structural coverage for REQ-P13-01..05 (8 tests; CRLF-safe)
- [x] `tests/fixtures/finding-codes-phase12.md` — frozen Phase-12 catalogue snapshot for the set-identity diff (REQ-P13-06)

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Semantic fidelity: that `dsx-scope-analysis`'s tier→`dsx.enforce`/`mode` mapping is *substantively identical* to `docs/gsd-tiers.md` (not merely that both mention Tier 0/1/2) | REQ-P13-04 | The automated test asserts the routing tokens + helper emission + doc citation; whether the prose *semantics* match the authority doc is a read, not an assertion | Hand-verified at S1-4 (VERIFICATION.md): tier table matches the doc's `enforce` off/on/on + `mode=interactive` @ Tier 2. Re-read on any edit to either file. |
| Prose quality: that each router playbook actually *guides* an analyst to fill the right spec fields (beyond citing the right codes) | REQ-P13-01 | Usefulness of guidance prose is a judgement no unit test makes | Hand-verified at S1-4 (21/21 cited codes real; router discipline clean). |

*These manual-only items do **not** reduce Nyquist compliance: the underlying deterministic
behaviours for REQ-P13-01/04 are covered by green automated tests above. Only the semantic/prose
*fidelity* — a read no test can perform — is manual, exactly as with the D-05 reads in earlier
phases. `nyquist_compliant: true` stands.*

---

## Validation Audit 2026-08-28

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

State B reconstruction: all 6 requirements classified **COVERED** — each maps to a named test that
runs green. **No `gsd-nyquist-auditor` spawned and no gap-filling tests generated (0 gaps).** The
single new test module (`tests/test_phase13_playbooks.py`) was authored to crystallise the phase's
deterministic invariants, not to fill a gap the auditor found. Independent re-gate this firing:

- New module `tests.test_phase13_playbooks` → **Ran 8 tests … OK**.
- Catalogue invariant `tests.test_finding_catalogue_invariant` → **Ran 2 tests … OK** (set-identity + 256).
- Full corpus gate `sh scripts/check.sh` → **all checks passed** (`Ran 1230 tests … OK`, catalogue current at 256, capability manifest conformant, gate contract good/bad/missing, determinism identical).

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (none — 0 gaps)
- [x] No watch-mode flags
- [x] Feedback latency < 54s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-08-28 — `nyquist_compliant: true`, 0 gaps, 6/6 requirements COVERED by green automated tests; independent re-gate green (`Ran 1230 tests … OK`).
