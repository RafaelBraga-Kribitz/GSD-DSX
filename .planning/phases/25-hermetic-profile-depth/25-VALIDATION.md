---
phase: 25
slug: hermetic-profile-depth
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-09-06
---

# Phase 25 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `unittest` (Python stdlib — tests are `unittest.TestCase` classes; no pytest config exists) |
| **Config file** | none — `scripts/check.sh` is the gate (`python3 -m unittest discover -s tests -q`) |
| **Quick run command** | `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe -m unittest discover -s tests -q` |
| **Full suite command** | `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe -m unittest discover -s tests -q` (== `scripts/check.sh`) |
| **Estimated runtime** | ~{N} seconds |

> Real interpreter only — a bare `python3` on this machine can resolve to a package-less stub (Python 3.14.6) that reports the matplotlib determinism test as *skipped* (HUMAN-QUEUE standing note). The gate is stdlib `unittest`, NOT pytest (verified 2026-09-06: no `pyproject.toml`/`pytest.ini`/`setup.cfg`; `scripts/check.sh` runs `unittest discover`).

---

## Sampling Rate

- **After every task commit:** Run the quick run command above
- **After every plan wave:** Run the full suite command above
- **Before `/gsd-verify-work`:** Full suite must be green
- **Max feedback latency:** {N} seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| {N}-01-01 | 01 | 1 | REQ-{XX} | T-{N}-01 / — | {expected secure behavior or "N/A"} | unit | `{command}` | ✅ / ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

> Draft scaffold — completed by `/gsd-validate-phase 25` (S1-5) against the finalized PLAN.md task IDs.

---

## Wave 0 Requirements

- [ ] `{tests/test_file.py}` — stubs for REQ-{XX}
- [ ] `{tests/conftest.py}` — shared fixtures
- [ ] `{framework install}` — if no framework detected

*If none: "Existing infrastructure covers all phase requirements."*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| {behavior} | REQ-{XX} | {reason} | {steps} |

*If none: "All phase behaviors have automated verification."*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < {N}s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** {pending / approved YYYY-MM-DD}
