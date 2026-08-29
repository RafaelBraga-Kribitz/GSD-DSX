---
phase: 14
slug: compounding-and-data-onboarding
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-28
validated: 2026-08-28
---

# Phase 14 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> **State B run** (no prior VALIDATION.md): reconstructed from the five plans + SUMMARY files.
> Phase 14 is a doc/skill/template phase (compounding loop, data-onboarding artifact, opt-in
> disclosure, CSV-first aliases, documented-skip), so the "behaviours" are the *structural
> invariants* each requirement promises. Rather than leave those as manual reads, the
> deterministic checks S2-4 ran by hand were **crystallised into a standing test**
> (`tests/test_phase14_onboarding.py`, 11 tests) alongside the pre-existing catalogue
> invariant and the gate-path hermeticity guard — so all six requirements have green automated
> verification. Gap analysis: **0 gaps** → no `gsd-nyquist-auditor` spawned. Every command below
> was re-run by the orchestrator this firing (brief §5).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python stdlib `unittest` (no pytest / no third-party test framework in the repo) |
| **Config file** | none — `python -m unittest discover -s tests -q` (see `scripts/check.sh`) |
| **Quick run command** | `python -m unittest tests.test_phase14_onboarding tests.test_gate_path_hermetic tests.test_finding_catalogue_invariant -v` |
| **Full suite command** | `python -m unittest discover -s tests -q` (1243 tests as of 2026-08-28) |
| **Phase gate** | `sh scripts/check.sh` (full suite + `gen-finding-catalogue.py --check` + capability manifest + gate-contract good/bad/missing exit codes + determinism) |
| **Estimated runtime** | ~54 seconds (full suite: `Ran 1243 tests in ~54s`) |

---

## Sampling Rate

- **After every task commit:** Run `python -m unittest tests.test_phase14_onboarding -v`, plus `python scripts/gen-finding-catalogue.py --check` whenever a skill's cited codes or the catalogue change.
- **After every plan wave:** Run `python -m unittest discover -s tests -q` (full suite).
- **Before `/gsd-verify-work`:** `sh scripts/check.sh` must be green.
- **Max feedback latency:** ~54 seconds.

---

## Per-Task Verification Map

*State B reconstruction: every requirement maps to a named test that runs green.*

| Requirement | Observable behaviour | Test Type | Named passing test(s) | Status |
|-------------|----------------------|-----------|-----------------------|--------|
| REQ-P14-01 | `dsx-scope-analysis` searches `docs/dsx/learnings/` before framing; the schema `README.md` and at least one dated `YYYY-MM-DD-<slug>.md` exemplar exist; `gsd-extract-learnings` named as producer | unit | `tests.test_phase14_onboarding.TestPhase14Onboarding.test_req01_learnings_readme_and_dated_exemplar_exist`, `…test_req01_scope_analysis_searches_learnings_before_framing` | ✅ green |
| REQ-P14-02 | `templates/DATA-DICTIONARY.md` sits next to `DATA-PROFILE.yaml`, states the roster is **copied verbatim**, carries the closed `semantic_type` set; `dsx-explore-data` authors it | unit | `tests.test_phase14_onboarding.TestPhase14Onboarding.test_req02_data_dictionary_template_copies_profile`, `…test_req02_explore_data_authors_dictionary` | ✅ green |
| REQ-P14-03 | `dsx-narrate` offers the AI-assistance disclosure **only** on literal `dsx.domain == research` (opt-in/skippable), read via the documented `config-get`; the disclosure template exists | unit | `tests.test_phase14_onboarding.TestPhase14Onboarding.test_req03_disclosure_template_exists`, `…test_req03_narrate_disclosure_guarded_on_literal_research` | ✅ green |
| REQ-P14-04 | The operating guide carries the CSV-first alias table (CSV **as an argument**, no watched `data_storage/` folder); every DSX skill (13) carries a `Triggers:` clause; no `data_storage` in skills/shims | unit | `tests.test_phase14_onboarding.TestPhase14Onboarding.test_req04_operating_guide_alias_table_csv_as_argument`, `…test_req04_all_dsx_skills_carry_triggers`, `…test_req04_no_data_storage_in_skills_or_shims` | ✅ green |
| REQ-P14-05 | Documented-skip of the file-drop hook: the guide's "Why there is no file-drop hook" names `DSX-DQ-001` CRITICAL as the compensating control; the code exists in the catalogue; `hooks` stays `[]` | unit | `tests.test_phase14_onboarding.TestPhase14Onboarding.test_req05_documented_skip_names_dq001_and_keeps_hooks_empty` | ✅ green |
| REQ-P14-06 | No new `DSX-*` code ships (set-identical to Phase-12 snapshot AND exactly 256); the gate path stays stdlib-pure and profiler-free; `capability.json` `hooks == []`, no `aliases` key, `supported == ["*"]` | unit + build gate | `tests.test_phase14_onboarding.TestPhase14Onboarding.test_req06_capability_hooks_empty_no_aliases_key`; `tests.test_finding_catalogue_invariant` (set-identity + 256); `tests.test_gate_path_hermetic` (2); `python scripts/gen-finding-catalogue.py --check` (exit 0) | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

The one new Wave-0 dependency (`tests/test_phase14_onboarding.py`) was created during this validation
run to crystallise the deterministic structural checks; `tests/test_gate_path_hermetic.py` was created
in execution (14-05). Both are present in the tree; `wave_0_complete: true`.

- [x] `tests/test_phase14_onboarding.py` — structural coverage for REQ-P14-01..06 (11 tests; CRLF-safe)
- [x] `tests/test_gate_path_hermetic.py` — standing gate-path purity + dq-isolation guard (REQ-P14-06)

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Prose fidelity: that the compounding-loop step actually *guides* a later session to reuse a prior finding (beyond citing the README and grepping the keys) | REQ-P14-01 | Usefulness of guidance prose is a judgement no unit test makes | Hand-verified at S2-4 (VERIFICATION.md): the step greps the fixed keys, cites the README authority, records the empty case. Re-read on any edit. |
| Semantic fidelity: that the DATA-DICTIONARY roster copied by `dsx-explore-data` is *substantively identical* to `DATA-PROFILE.yaml` for a real dataset (not merely that the skill says "copy verbatim") | REQ-P14-02 | The automated test asserts the copy-verbatim discipline in the template + skill; whether a produced dictionary matches a produced profile is a per-run read | Hand-verified at S2-4: template + skill both carry the copy-verbatim rule under "never invent profile numbers". Re-verify per actual onboarding run. |

*These manual-only items do **not** reduce Nyquist compliance: the underlying deterministic
behaviours for REQ-P14-01/02 are covered by green automated tests above. Only the semantic/prose
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
single new test module (`tests/test_phase14_onboarding.py`) was authored to crystallise the phase's
deterministic invariants, not to fill a gap the auditor found. One test assertion was corrected during
authoring (an initial naive `assertNotIn("data_storage/", guide)` contradicted the 14-04 contract,
which *requires* the guide to document the folder's absence with the phrase "without a data_storage";
the guide is exempt and the check was rescoped to skills + shims). Independent re-gate this firing:

- New module `tests.test_phase14_onboarding` → **Ran 11 tests … OK**.
- Gate-path hermeticity `tests.test_gate_path_hermetic` → **Ran 2 tests … OK**.
- Catalogue invariant `tests.test_finding_catalogue_invariant` → **Ran 2 tests … OK** (set-identity + 256).
- Full corpus gate `sh scripts/check.sh` → **all checks passed** (`Ran 1243 tests … OK`, catalogue current at 256, capability manifest conformant, gate contract good/bad/missing, determinism identical).

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references (none — 0 gaps)
- [x] No watch-mode flags
- [x] Feedback latency < 54s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-08-28 — `nyquist_compliant: true`, 0 gaps, 6/6 requirements COVERED by green automated tests; independent re-gate green (`Ran 1243 tests … OK`).
