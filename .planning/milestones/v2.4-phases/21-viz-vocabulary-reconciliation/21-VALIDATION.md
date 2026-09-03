---
phase: 21
slug: viz-vocabulary-reconciliation
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-03
---

# Phase 21 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | stdlib `unittest` (existing — `tests/` dir; siblings `test_finding_catalogue_invariant.py` / `test_gen_finding_catalogue.py` / `test_phase20_zero_mint_close.py`) |
| **Config file** | none — `unittest` discovery, no config file required |
| **Quick run command** | `python -m unittest tests.test_viz_vocabulary_invariant` |
| **Full suite command** | `python -m unittest discover -s tests` |
| **Estimated runtime** | ~40s full suite (1471 tests, measured 2026-09-02); ~5s quick (55 tests across the three invariant modules) |

---

## Sampling Rate

- **After every task commit:** Run `python -m unittest tests.test_viz_vocabulary_invariant`
- **After every plan wave:** Run `python -m unittest discover -s tests`
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** ~40s (measured full suite)

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 21-01-01 | 01 | 1 | REQ-P21-01 / REQ-P21-02 | T-21-01 / T-21-02 | Repo-integrity invariant authored (every non-banned mark has a capability home + a relationship home or a frozen `CAPABILITY_ONLY` allowlist entry; every banned type carries a complete `{reason, code, citation}` refusal record) | unit | `python -m unittest tests.test_viz_vocabulary_invariant` | ✅ | ✅ green |
| 21-01-02 | 01 | 1 | REQ-P21-01 | T-21-01 | 12 orphan marks homed one-family-each in `CHART_CAPABILITIES` / `RELATIONSHIP_CHARTS`; `dsx/data/input_types.json` regenerated so the IT-id gate path admits them | unit | `python -m unittest tests.test_viz_vocabulary_invariant.TestEveryMarkHasAHome tests.test_input_types` | ✅ | ✅ green |
| 21-01-03 | 01 | 1 | REQ-P21-02 / REQ-P21-03 | T-21-02 / T-21-03 | `BANNED_TYPES` promoted to `{reason, code, citation}` records (code = DSX-VIZ-001, `_check_banned` reads `["reason"]`); finding-code catalogue holds 275→275 (zero mint, set-identity) | unit | `python -m unittest tests.test_viz_vocabulary_invariant.TestRefusalEntryCompleteness tests.test_finding_catalogue_invariant tests.test_gen_finding_catalogue` | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

*Existing infrastructure covers all phase requirements.* stdlib `unittest` needs no install; the one new module (`tests/test_viz_vocabulary_invariant.py`) was authored inside Wave 1 Task 1 as the TDD RED test, not as a Wave 0 dependency. No shared fixtures or framework install were required.

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Refusal-citation **authenticity** (does each cited source actually support the ban) | REQ-P21-02 | D-05 primary-source read — a program can assert the `citation` field is non-empty (automated, `TestRefusalEntryCompleteness`) but cannot confirm the source text says what is claimed | Confirm each of the five banned-type citations at its locator per HUMAN-QUEUE HQ-27 Tier-3; the `radar` row is the least-certain (provisional doctrine fit, no exact pre-mapped source) — resolve or resource at S5-2. Non-blocking for Phase 21. |

*Note: the refusal-record structural completeness and code identity ARE automated; only the source-text authenticity is a human read.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies — all three tasks have automated commands
- [x] Sampling continuity: no 3 consecutive tasks without automated verify — 3/3 automated
- [x] Wave 0 covers all MISSING references — no MISSING references (0 gaps)
- [x] No watch-mode flags — all commands single-shot
- [x] Feedback latency < 60s — measured 40s full suite / 5s quick
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-09-02 (autonomous loop firing, validate-phase orchestrator) — State A gap analysis: all 3 requirements COVERED with green automated tests, re-run by the orchestrator (55 invariant/catalogue tests OK; full suite 1471 OK) rather than trusted from the S1-4 report. 0 gaps → no auditor spawn.

---

## Validation Audit 2026-09-02

| Metric | Count |
|--------|-------|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

All three requirements (REQ-P21-01/02/03) classified COVERED at gap analysis: each has an automated unit test that targets the behavior and runs green. No MISSING (no test generation needed), no PARTIAL (no failing/incomplete tests). The single Manual-Only entry is a D-05 citation-authenticity read (batched to HQ-27), not a test-coverage gap.
