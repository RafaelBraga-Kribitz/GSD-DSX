---
phase: 12
slug: calibration
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-27
validated: 2026-08-27
---

# Phase 12 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded from `12-RESEARCH.md` `## Validation Architecture` (line 718). Finalized at `/gsd-validate-phase 12` (S3-5).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | Python `unittest` (stdlib) |
| **Config file** | none — `tests/` discovered by `unittest discover` |
| **Quick run command** | `python -m unittest tests.test_known_bad_corpus -q` |
| **Full suite command** | `bash scripts/check.sh` (full suite + catalogue `--check` + manifest + gate contract + determinism) |
| **Estimated runtime** | ~45 seconds (full suite ~1199 tests today) |

---

## Sampling Rate

- **After every task commit:** Run the quick run command for the touched module.
- **After every plan wave:** Run `bash scripts/check.sh`.
- **Before `/gsd-verify-work`:** Full suite must be green.
- **Max feedback latency:** ~45 seconds.

---

## Per-Task Verification Map

> Seeded scaffold — validate-phase (S3-5) maps each executed task's requirement to its named passing
> test. The RESEARCH `## Validation Architecture` section carries the per-requirement test shapes:
> REQ-P12-01 per-class coverage predicates; REQ-P12-02 sidecar sibling-integrity + falsifiability
> tests; REQ-P12-03 stratified (present/absent) rate + live-computed friction (raw AND net) + the
> good-control FPR denominator; REQ-P12-04 `dsx stats --paradigm` synthetic-trail guard + negative
> known-bad-source assertion; REQ-P12-05 §6.5 disposition + REV-002 pinned-substring preservation;
> D-18 catalogue-invariant (256) test.

Validate-phase (S3-5) gap analysis: **0 gaps — all 5 requirements COVERED**, each mapped to a named
green test. No `gsd-nyquist-auditor` spawned, no generated tests (workflow §3 skip-to-§6; mirrors
11.2/11.3). Independently re-gated first-hand (§5): the three requirement modules ran verbosely →
`Ran 52 tests … OK`.

| Req | Plan(s) | Wave | Secure Behavior | Named Test(s) | Automated Command | Status |
|-----|---------|------|-----------------|---------------|-------------------|--------|
| REQ-P12-01 | 12-01 | 1 | Corpus at full size across the 3 missing coverage classes, class-presence predicate (no hardcoded slug list), source-before-count | `test_corpus_includes_full_coverage_classes` (`tests/test_known_bad_corpus.py:862`) | `python -m unittest tests.test_known_bad_corpus` | ✅ COVERED |
| REQ-P12-02 | 12-01, 12-03, 12-06 | 1–4 | Every miss/promotion case carries a union-validated, live-falsifiable `<slug>-ATTRIBUTION.yaml` sidecar; per-family friction RAW+NET; catalogue stays 256 | `test_attribution_sidecars_reference_valid_codes_and_items` (`:1363`), `test_attribution_tags_are_falsifiable_against_live_gate` (`:1438`), `test_net_is_raw_minus_own_and_both_are_surfaced` (`:1935`), `test_relabeling_incidental_to_own_shrinks_net_but_not_raw` (`:1957`), `test_friction_uses_the_same_live_findings_as_golden` (`:1627`), `test_finding_catalogue_stays_at_256_codes` | `python -m unittest tests.test_known_bad_corpus tests.test_finding_catalogue_invariant` | ✅ COVERED |
| REQ-P12-03 | 12-04, 12-05 | 2–3 | Stratified catch-rate + FPR, headline (miss-rate, FPR), floored ABSENT partition + invariance; ≥10-spec good-side FPR control corpus; tempdir-noise excluded | `test_stratified_catch_rate_and_fpr_report` (`:1496`), `test_headline_is_invariant_to_adding_a_target_present_case` (`:1915`), `test_false_positive_findings_excludes_documented_tempdir_noise` (`:1880`) | `python -m unittest tests.test_known_bad_corpus` | ✅ COVERED |
| REQ-P12-04 | 12-02 | 1 | `dsx stats --paradigm` exits 0, distinct-frame dedup, D-13 fixture-floor exclusion (CR-01 hardened absolute), `--block-on` rejected | `test_always_exits_zero`, `test_dedup_is_by_distinct_frame_digest`, `test_never_sources_the_known_bad_floor`, `test_root_pointed_at_the_floor_still_excludes_it`, `test_excluded_component_match_is_case_folded`, `test_block_on_flag_is_rejected` (`tests/test_cli_stats.py`) | `python -m unittest tests.test_cli_stats` | ✅ COVERED |
| REQ-P12-05 | 12-07 | 5 | §6.5 carry-8/remove-1; item-6 ratio-metric relocated (not deleted) with pinned substrings intact; REV-002 filed, SELF-001-safe | `test_brief_states_the_ratio_metric_dilution_entry_condition_as_a_falsifiable_blocker` (`:1284`) | `python -m unittest tests.test_known_bad_corpus` | ✅ COVERED |

*Status: ⬜ pending · ✅ COVERED (green) · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- Existing infrastructure (`tests/test_known_bad_corpus.py`, `tests/test_causal_verb_golden.py`,
  `unittest`) covers the measurement substrate; new test files are added per-plan (RED before GREEN
  under TDD mode). No framework install needed.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| D-05 primary-source citation authenticity for new corpus cases (retracted papers, p-hacking cases) | REQ-P12-01 | Verbatim quote-at-locator is a human read (project D-05 bar), not automatable | Assembled as an evidence pack at the Phase-12 UAT/ship round (pre-registered per CONTEXT `<deferred>`); does not reduce nyquist compliance |

*Automated verification covers every machine-checkable behavior; only the D-05 source reads are manual (mirrors 11.2/11.3).*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies — all 5 requirements COVERED by named green tests
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references — 0 MISSING (existing `unittest` infrastructure; no new framework)
- [x] No watch-mode flags
- [x] Feedback latency < 60s — quick module run ~11s, full suite ~55s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-08-27 (S3-5). The single Manual-Only item (D-05 primary-source citation
authenticity for the 3 new corpus cases) is a human source read, NOT a coverage gap — it does not
reduce compliance (mirrors 11.2/11.3). Tracked in HQ-6, drained at the Phase-12 UAT/ship round.

---

## Validation Audit 2026-08-27

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

All 5 requirements (REQ-P12-01..05) classified COVERED in gap analysis — each has an existing named
passing test. Per workflow §3, 0 gaps → skip auditor, `nyquist_compliant: true`. Independently
re-gated first-hand (§5, never trusted a summary): the three requirement modules ran verbosely →
`Ran 52 tests … OK`; full suite `Ran 1221 tests … OK`; `bash scripts/check.sh` → all checks passed
(catalogue current 256, D-18 zero minted, manifest conformant, gate contract good/bad/missing,
determinism identical). No test files generated; nothing to commit beyond this document.
