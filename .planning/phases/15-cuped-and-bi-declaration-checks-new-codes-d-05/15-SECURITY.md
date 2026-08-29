---
phase: 15
slug: cuped-and-bi-declaration-checks-new-codes-d-05
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: 2026-08-29
---

# Phase 15 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> **State B run** (no prior SECURITY.md): the 23-entry register was consolidated from the
> `<threat_model>` blocks of all six 15-0x plans (`register_authored_at_plan_time: true`);
> each of the six plans declared `T-15-SC` identically, deduped here to one supply-chain
> accept (22 distinct threats + 1 accept). No SUMMARY carried a `## Threat Flags` section
> (grep-confirmed), so nothing was added outside the plan-time register. `asvs_level: 1`
> (config `security_asvs_level: 1`) + `register_authored_at_plan_time: true` +
> `threats_open: 0` → the workflow's L1 short-circuit applies (no auditor spawn; grep/AST
> depth is sufficient at Level 1). Every mitigation was **re-gated directly by the
> orchestrator** with real commands (brief §5 — never trusted from a report). Phase 15 mints
> two always-run declaration-only checks — `DSX-EXP-070` (CRITICAL: a CUPED covariate that is
> not pre-experiment) and `DSX-MET-021` (HIGH: a metric pooled across buckets sampled at
> different rates with no reweighting) — adds the `cuped` variance-adjustment vocabulary
> keystone, ships an optional APA research-table template, guarantees no normality-test
> auto-switch on the decision surface, and rebaselines the catalogue additively (258 → 260,
> Phase-12 snapshot unmutated). There is **no untrusted input and no executable surface on any
> deterministic gate path** — both checks read the already-loaded spec dict and compute
> nothing, opening no data file and importing no tabular library — so ASVS L1 injection / auth
> / session vectors are all N/A. The residual STRIDE surface is Tampering / Spoofing — a
> future "simplification" pulling the CUPED variance arithmetic (in `dsx/mathx.py`, off the
> gate path) onto the check, a code minted or downgraded so a bad declaration no longer exits
> 1, a survivorship code invented despite its citation not transferring (answered HQ-8), or
> `DSX-MET-021` double-reporting with its sibling `DSX-MET-020` on one defect.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| `spec.design.cuped.covariate_timing` → `dsx/checks/design.py::_check_cuped` | The check reads one declared timing string against the closed `CUPED_COVARIATE_TIMINGS` vocabulary and emits at most one finding; it computes no θ/ρ/variance and **never imports** `cuped_theta`/`cuped_variance_reduction` (D-01/D-02). | in-repo spec dict (internal) |
| `dsx/mathx.py` CUPED arithmetic → tests only | `cuped_theta` / `cuped_variance_reduction` are pure scalar identities (the WSDM ρ²=0.25 worked value) exercised **only** by tests; no gate check imports them — the diluted-effect / DSX-INT-030 purity boundary. | test-only pure functions (no gate read) |
| `spec.results.cohort_comparisons` → `dsx/checks/metrics.py::_check_cohort_denominator_shift` | The check reads declared per-bucket sampling rate / treatment share and a `reweighted` flag, compares a spread to a scalar tolerance with stdlib arithmetic, and emits at most one finding per entry. It reads a **disjoint** surface from the sibling `DSX-MET-020` (which reads `results.period_comparisons`); writes nothing, runs nothing (D-01). | in-repo spec dict (internal) |
| `report.add` sites → generator → `references/finding-codes.md` | The generator walks `dsx/**.py` `report.add` sites (including 15-02/15-04's two new codes) and rewrites the catalogue; `--check` re-derives currency and the D-05/families gates; the two exact codes are allowlisted into `_D05_ALLOWLIST_CODES` (not by prefix). | generated markdown (internal) |
| `_SNAPSHOT_TOTAL` + `_MINTED_CODES` → invariant | The two-leg invariant pins count 260 AND set-identity vs the frozen Phase-12 snapshot ∪ {REP-060, REP-061, EXP-070, MET-021}; the byte-frozen 256 snapshot anchor makes any drift name itself. | test-only fixture (no gate read) |

---

## Threat Register

*Consolidated from the six plans' `<threat_model>` blocks; phase-unique IDs assigned by the
plan authors, plan of origin in the component column. `block_on = high`, so only OPEN threats at
high+ count toward `threats_open`. Re-gate range: gate-path diff `a75fc9e..HEAD` (the S4-2
baseline through the landed phase); the six feature commits are 6ccb155 / e6c1ee8 / 0ffeb7f /
2173030 / 47b5e41 / 4704722.*

| Threat ID | Category | Component (plan) | Severity | Disposition | Mitigation | Status |
|-----------|----------|------------------|----------|-------------|------------|--------|
| T-15-01 | Tampering | A parallel CUPED-timing set forked from the vocabulary, letting the dump and the 15-04 check drift (15-01) | medium | mitigate | M-09 single-source: `CUPED_COVARIATE_TIMINGS` is one `spec.py` constant registered once in `_VOCABULARIES` and imported by the check. Re-gate: `tests.test_cuped_vocab` **4 OK** (equality on the constant AND the `dsx vocab` dump); `test_phase15_bi_checks.test_req01_covariate_timing_vocab_is_two_valued`. | closed |
| T-15-02 | Tampering | A silent finding-code mint or gate-threshold edit riding the vocabulary change (15-01) | high | mitigate | D-01: 15-01 adds no `report.add` and no `GATE_THRESHOLDS`/`GATE_PROFILES` entry. Re-gate: `git diff a75fc9e..HEAD -- dsx/spec.py` is additive vocab only; `gen-finding-catalogue.py --check` **exit 0**; the catalogue delta is exactly the two sanctioned mints (invariant set-identity). | closed |
| T-15-03 | Tampering | Replacing (not extending) `VARIANCE_ADJUSTMENTS`, dropping a legacy member and loosening an existing gate (15-01) | high | mitigate | REQ-P15-01: the four legacy members survive and the set is exactly five. Re-gate: `tests.test_cuped_vocab.test_four_legacy_variance_adjustments_round_trip`; `test_phase15_bi_checks.test_req01_cuped_is_a_legal_variance_adjustment` (`{cluster_robust,delta_method,bootstrap_cluster,mixed_effects} ⊆` set, `len == 5`). | closed |
| T-15-10 | Tampering | `DSX-MET-021` double-reporting with `DSX-MET-020` on one defect, over-blocking legitimate cohort comparisons (15-02) | high | mitigate | trap #1: the two read disjoint surfaces. Re-gate: `tests.test_cohort_denominator.test_met020_and_met021_are_disjoint` (a period-drift spec fires MET-020 not MET-021; a cohort mix-shift spec fires MET-021 not MET-020); `test_phase15_bi_checks.test_req04_met020_and_met021_read_disjoint_surfaces`. | closed |
| T-15-11 | Tampering | The check pulling pandas/scipy or summing per-unit data, re-implementing ratio-metric dilution / INT-030 (15-02) | high | mitigate | trap #5/#6/D-01: the check reads declared shares only. Re-gate: `grep -E '^\s*(import\|from)\s+(pandas\|scipy\|numpy\|csv\|subprocess\|runpy\|os\|shutil)' dsx/checks/metrics.py` → **none**; `test_phase15_bi_checks.test_req04_cohort_check_is_declaration_only`; the body references `cohort_comparisons` (4×), not summation. | closed |
| T-15-12 | Spoofing | A truthy-but-not-boolean `reweighted` value (a string, `1`) silently clearing the finding (15-02) | medium | mitigate | D-03: the fire condition is `reweighted is not True` (identity to Python `True`). Re-gate: `tests.test_cohort_denominator.test_met021_silent_when_reweighted_true` pins the boolean path; the firing tests use non-`True` values. | closed |
| T-15-13 | Tampering | A silently minted survivorship code riding along, overstating REQ-P15-04 as fully satisfied (15-02) | high | mitigate | D-05: only `DSX-MET-021` ships; survivorship stays a `brief.md` §6.5 non-promotion (Brown 1992 does-not-transfer, answered HQ-8). Re-gate: `tests.test_cohort_denominator.test_only_met021_reachable_from_cohort_check`; `test_phase15_bi_checks.test_req04_survivorship_code_not_minted` (`survivorship` absent from the catalogue); no plan edits `REQUIREMENTS.md`. | closed |
| T-15-20 | Tampering | The APA template read as relaxing the marketing-domain ship contract (dropping NAR/FIG/CLM evidence) (15-03) | medium | mitigate | REQ-P15-05: the header states the template is optional + research-domain and that NAR/FIG/CLM stay required; no gate code is edited. Re-gate: `tests.test_apa_template` **3 OK** (domain + optional framing asserted). | closed |
| T-15-21 | Tampering | A future skill or gate quietly adding a Shapiro-Wilk auto-switch that flips the recommended test (15-03) | high | mitigate | D-07: the decision surface names no normality-test auto-switch. Re-gate: `tests.test_no_shapiro_autoswitch` **4 OK** — greps `dsx/` + `skills/` for normality-test calls (0) and pins `test-selection.md`'s fixed independence→variance→normality order + unconditional Welch. | closed |
| T-15-22 | Tampering | A vacuous decision-surface scan (empty or mis-scoped walk) passing green while proving nothing (15-03) | medium | mitigate | anti-vacuity: the scan asserts a non-empty named file set including a `dsx/` module and a `skills/` file; scoping excludes `tests/`/`references/`. Re-gate: `tests.test_no_shapiro_autoswitch` non-empty-named-set assertion green. | closed |
| T-15-40 | Tampering | The CUPED math creeping onto the gate path (`design.py` importing `cuped_theta` to "verify" the reduction) (15-04) | critical | mitigate | D-01/D-02 / trap #5: the check reads `covariate_timing` only. Re-gate: `grep` for `cuped_theta`/`cuped_variance_reduction` in `dsx/checks/design.py` → **none** (`tests.test_cuped.GateCheckPurityTest`; `test_phase15_bi_checks.test_req02_cuped_check_is_declaration_only`); forbidden-import grep on `design.py` → none. | closed |
| T-15-41 | Tampering | A typo or absent `covariate_timing` being cheaper than an honest `post_treatment`, letting a mislabelled CUPED slip the gate (15-04) | high | mitigate | D-02 / trap #11: the fire covers every non-`pre_experiment` value. Re-gate: `tests.test_cuped` fires on `post_treatment`, `absent`, and `unrecognised` timing; silent on `pre_experiment` and non-cuped. | closed |
| T-15-42 | Spoofing | A false-positive on a valid covariate via a fuzzy third timing state (15-04) | medium | mitigate | D-02: `CUPED_COVARIATE_TIMINGS` is exactly two-valued (15-01); `pre_experiment` is the only ok path. Re-gate: `tests.test_cuped.test_exp070_silent_on_pre_experiment`; `tests.test_cuped_vocab.test_cuped_covariate_timings_is_exactly_two_valued`. | closed |
| T-15-43 | Tampering | Downgrading below CRITICAL (or a `GATE_THRESHOLDS` edit) so a post-treatment CUPED no longer exits 1 at plan (15-04) | high | mitigate | REQ-P15-02 / trap #8: the `report.add` severity arg is the constant `CRITICAL`. Re-gate: `tests.test_cuped.GatePlanExitTest` proves `dsx gate plan` exit **0 → 1** over the real good fixture via `run_checks`; the catalogue severity cell reads **CRITICAL** (`test_phase15_bi_checks.test_req02_exp070_registered_critical`). | closed |
| T-15-44 | Tampering | Citing the Unified playbook snippet instead of the WSDM primary source (15-04) | medium | mitigate | REQ-P15-02 / D-05: the check + mathx docstrings cite Deng et al. 2013 WSDM (confirmed at locator, answered HQ-8). Re-gate: `grep -c Deng dsx/checks/design.py` → **1**; `test_phase15_bi_checks.test_req02_cuped_check_cites_wsdm_primary_source`. | closed |
| T-15-50 | Tampering | A new thin field landing inside `validity_frame`, changing `frame_digest` and moving a downstream check (15-05) | high | mitigate | D-04: the new keys live under `results`/`metrics`/`design`, never `validity_frame`. Re-gate: `tests.test_good_fixture_phase15` placement test (new keys absent from `validity_frame`; `frame_digest` unchanged). | closed |
| T-15-51 | Tampering | The new checks firing on the good fixture, breaking the D-08 clean-at-every-threshold contract (15-05) | high | mitigate | trap #2: the fixture declares equal sampling rate / `reweighted: true` and `pre_experiment` CUPED timing. Re-gate: `tests.test_good_fixture_phase15` **3 OK** — `DSX-MET-021`/`DSX-EXP-070` absent and exit 0 at all four gate points. | closed |
| T-15-52 | Tampering | Replacing rather than extending the good fixture, dropping a field and loosening a passing gate (15-05) | high | mitigate | D-08: additions only. Re-gate: `tests.test_good_fixture_phase15` round-trip (new keys present) with the causal-verb golden suite still green (existing finding set unchanged). | closed |
| T-15-60 | Tampering | Adding `DSX-EXP-`/`DSX-MET-` to `_D05_ALLOWLIST_PREFIXES`, dragging legacy uncited family members into D-05 enforcement (15-06) | high | mitigate | D-09: only the two **exact** codes are allowlisted. Re-gate: `_D05_ALLOWLIST_PREFIXES` byte-unchanged over the phase; `gen-finding-catalogue.py --check` **exit 0** (no red D-05 obligation on legacy EXP/MET members). | closed |
| T-15-61 | Tampering | Hand-editing `references/finding-codes.md` or a cardinality-preserving mint/drop slipping the count (15-06) | high | mitigate | trap #10 / D-08: the file is generator-produced (`--check` exit 0) and the invariant's set-identity leg compares against snapshot ∪ {REP-060, REP-061, EXP-070, MET-021}. Re-gate: `tests.test_finding_catalogue_invariant` **2 OK**. | closed |
| T-15-62 | Tampering | Mutating the byte-frozen Phase-12 snapshot to 260 to "make the leg pass", erasing the additive-mint audit (15-06) | high | mitigate | D-08 / trap #3: `_SNAPSHOT_TOTAL` stays 256 and the snapshot-length leg anchors to it. Re-gate: `git diff --stat a75fc9e..HEAD -- tests/fixtures/finding-codes-phase12.md` → **empty** (byte-unchanged). | closed |
| T-15-63 | Tampering | A stale invariant (method names/prose still say 258/256) masking the real 260 baseline (15-06) | medium | mitigate | D-08 internal-consistency: names + prose updated to 260. Re-gate: `tests.test_finding_catalogue_invariant.test_finding_catalogue_stays_at_260_codes` + `…_is_phase12_snapshot_plus_the_phase15_and_phase16_mints` both green. | closed |
| T-15-SC | Tampering | npm/pip/cargo installs (all six plans) | n/a | accept | No package installs occur; the deliverables are two stdlib checks, two pure stdlib identities, a vocabulary constant, a template, a fixture extension, a catalogue regen, and stdlib-only tests. | closed |

*Status: open · closed — 23 entries, 22 threats + 1 supply-chain accept; 1 critical + 14 high + 7 medium, all closed.*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on (`high`) count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-15-SC | T-15-SC | Vocabulary/check/template/fixture/test phase; no dependency manifest changed in the phase diff; both new checks, both new identities, and every new test are stdlib-only. Design-time disposition recorded identically in all six plan `<threat_model>` blocks; not a fresh mitigate→accept. | brief D-01 (standing) | 2026-08-29 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-08-29 | 23 | 23 | 0 | orchestrator direct re-gate (L1 short-circuit; no auditor spawn — declaration-only check phase, asvs_level 1) |

**Independent re-gate evidence (orchestrator, brief §5 — real commands, not a report):**
- **Gate-path purity (T-15-11/40, D-01):** `git diff --stat a75fc9e..HEAD -- dsx/ scripts/` → `dsx/checks/design.py` (+62), `dsx/checks/metrics.py` (+73), `dsx/mathx.py` (+35), `dsx/spec.py` (+15), `scripts/gen-finding-catalogue.py` (+11, the build-time allowlist — not a runtime gate). A `grep -E '^\s*(import|from)\s+(pandas|scipy|numpy|csv|subprocess|runpy|os|shutil)\b'` over the four runtime modules returns **none**; `design.py` names neither `cuped_theta` nor `cuped_variance_reduction` (the mathx CUPED arithmetic stays off the gate path).
- **CUPED gate-flip + severity (T-15-40/41/42/43, REQ-P15-02):** `python -m unittest tests.test_cuped` → **8 OK** — `DSX-EXP-070` fires on `post_treatment`/absent/unrecognised timing, silent on `pre_experiment`/non-cuped; `GatePlanExitTest` proves `dsx gate plan` exit **0 → 1** over the real good fixture via `run_checks`; the catalogue severity cell reads **CRITICAL**. WSDM ρ²=0.25 worked value proven; `design.py` cites Deng et al. 2013.
- **Changing-denominator disjointness (T-15-10/11/12/13, REQ-P15-04):** `python -m unittest tests.test_cohort_denominator` → **7 OK** — `DSX-MET-021` fires on unreweighted rate / treatment-share spread, silent when `reweighted is True` or rates equal, respects declared tolerance, and is **disjoint from `DSX-MET-020` in both directions** (period_comparisons vs cohort_comparisons); only MET-021 reachable from the cohort check; `metrics.py` cites Crook et al. 2009 KDD §6.
- **Good-fixture silence (T-15-50/51/52, REQ-P15-03, D-04/D-08):** `python -m unittest tests.test_good_fixture_phase15` → **3 OK** — the extended fixture is silent (EXP-070/MET-021 absent, exit 0) at all four gate points; new keys absent from `validity_frame` (`frame_digest` unchanged); causal-verb golden green.
- **No normality auto-switch (T-15-21/22, REQ-P15-06, D-07):** `python -m unittest tests.test_no_shapiro_autoswitch` → **4 OK** — 0 normality-test calls on the `dsx/`+`skills/` decision surface; non-empty named scan set (anti-vacuity).
- **APA template (T-15-20, REQ-P15-05):** `python -m unittest tests.test_apa_template` → **3 OK** — `templates/APA-TABLE-research.md` present, optional + research-domain, NAR/FIG/CLM contract intact.
- **Zero-drift / additive catalogue (T-15-02/60/61/62/63, REQ-P15-07, D-08/D-09):** `python -m unittest tests.test_finding_catalogue_invariant` → **2 OK** (count **260** AND set-identity `current == snapshot ∪ {DSX-REP-060, DSX-REP-061, DSX-EXP-070, DSX-MET-021}`); `python scripts/gen-finding-catalogue.py --check` → **exit 0**. Both new codes present at the decided severity (EXP-070 CRITICAL, MET-021 HIGH); `_SNAPSHOT_TOTAL` stays 256; the frozen `tests/fixtures/finding-codes-phase12.md` anchor is byte-unchanged (`git diff a75fc9e..HEAD` empty); `_D05_ALLOWLIST_PREFIXES` byte-unchanged (two exact codes only).
- **Phase-scoped coverage anchor:** `python -m unittest tests.test_phase15_bi_checks` → **20 OK** (crystallised this firing — REQ-P15-01..07 structural regression guard).
- **Citation authenticity (D-05):** both shipping codes cite HQ-8-confirmed primary sources (Deng et al. 2013 WSDM; Crook et al. 2009 KDD §6). The survivorship-bias code is **not** minted (Brown 1992 does-not-transfer, answered HQ-8; `brief.md` §6.5). **No new D-05 read owed by Phase 15** — HQ-8 is answered.
- **Full gate** `sh scripts/check.sh` → **all checks passed** (`Ran 1312 tests … OK`, catalogue current at 260, capability manifest conformant — 14 skills, gate contract good/bad/missing, determinism identical). The `declared twice` warnings are the pre-existing S0-2 shipped-tree noise — both gates exit 0.

**Environmental note (not a threat; recorded for S5-1/S5-4):** two pre-existing `explain`
tests (`test_dsx…test_explain_missing_spec_exits_zero_not_two`,
`test_explain_self_reported…test_returns_zero_when_spec_cannot_be_loaded`) run `dsx explain`
from the repo-root CWD without isolating it, so a stray **gitignored** `DECISIONS.jsonl`
runtime ledger (auto-written by any repo-root `dsx gate`/`explain`, `.gitignore:7`) makes them
read a real decision trail and false-fail. On a clean checkout — the state the committed tree
ships as — both pass; proven this firing by moving the four gitignored ledgers aside (tests
green) and by `scripts/check.sh` (which runs the suite before its own gate steps regenerate the
ledger). Not a Phase-15 defect and not on any gate path. See HUMAN-QUEUE standing notes.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified (technical) 2026-08-29 — gate **SECURED**, `threats_open: 0`, 23/23 closed by orchestrator re-gate. **Human sign-off is a D-05/§4-category-4 operator item and is NOT yet granted** — queued to `HUMAN-QUEUE.md` (HQ-14) as the batched Phase 15 end-of-phase security + UAT round. Per brief §4 this is non-blocking until close-out (S5-2); the technical gate for ledger unit S4-5 is met. The D-06 numbering veto for the two new codes is tracked separately as HQ-13 (same drain).
