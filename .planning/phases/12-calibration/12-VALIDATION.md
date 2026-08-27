---
phase: 12
slug: calibration
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-08-27
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

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| TBD | — | — | REQ-P12-01..05 | — | measurement honesty (no lifted numbers; live `_gate_findings`) | unit | `bash scripts/check.sh` | ✅ | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

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

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
