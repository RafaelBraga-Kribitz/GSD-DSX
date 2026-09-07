---
phase: 26
slug: per-skill-read-contracts
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-09-07
validated: 2026-09-07T09:00:00Z
---

# Phase 26 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> **Draft** — seeded by plan-phase (S2-2) from 26-RESEARCH.md `## Validation Architecture`.
> The Per-Task Verification Map is finalized at validate-phase (S2-5) once PLAN.md task IDs exist.
> Skill-doc + one off-gate-path test only; `dsx/` byte-identical; zero new codes (276 → 276).

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `unittest` (Python 3.12 stdlib) — no pytest in this repo |
| **Config file** | none — `scripts/check.sh` runs `unittest discover -s tests -q` |
| **Quick run command** | `"C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe" -m unittest tests.test_skill_read_contracts -v` |
| **Full suite command** | `"C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe" -m unittest discover -s tests -q` |
| **Estimated runtime** | ~60 seconds (full suite; the new file reads 7 small files, negligible on its own) |

---

## Sampling Rate

- **After every task commit:** Run `python -m unittest tests.test_skill_read_contracts -v`
- **After every plan wave:** Run the full suite (`unittest discover -s tests -q`)
- **Before `/gsd-verify-work`:** Full suite green AND `scripts/gen-finding-catalogue.py --check` exit 0 AND `node install.mjs && node install.mjs --check` exit 0 AND `git diff --stat -- dsx/` empty
- **Max feedback latency:** ~60 seconds

---

## Per-Task Verification Map

> Finalized at validate-phase (S2-5) from the executed plans (26-01…26-04).
> Every requirement is COVERED by a named `unittest` test that exists and passes on
> real Python 3.12.10; 0 MISSING → `nyquist_compliant: true`.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 26-01 (3 skills) + 26-02 (2 skills) | 26-01/02 | 1 | REQ-P26-01 | T-26-02/06 | Each of 5 skills carries one head `<inputs>` block naming its keys + `eda_artifact: none` fallback | unit | `test_every_skill_carries_at_least_one_key_region` (checked==5) + `test_when_absent_names_eda_artifact_none` | ✅ | ✅ pass |
| 26-03 (guard) | 26-03 | 2 | REQ-P26-02 | T-26-01/02/05/06 | Every named key resolves live; renamed key fails; CRLF-tolerant; non-vacuous; Also-consult zero backticks | unit | `test_skill_keys_are_members_of_live_templates` + `test_negative_control_orphan_key_is_rejected` + `test_anchor_non_vacuity` + `test_parse_is_deterministic_and_order_independent` + `test_also_consult_line_has_zero_backticks` | ✅ | ✅ pass |
| 26-04 (close) | 26-04 | 3 | REQ-P26-03 | T-26-03/04/07 | `dsx/` byte-identical; 276→276; installed copies re-synced | unit + smoke | `tests.test_finding_catalogue_invariant` + `gen-finding-catalogue.py --check` + `git diff --stat 818fb7c..HEAD -- dsx/` empty + `node install.mjs && --check` | ✅ | ✅ pass |

**Draft requirement → behavior → test coverage (from 26-RESEARCH.md):**

| Req ID | Behavior | Test / assertion |
|--------|----------|------------------|
| REQ-P26-01 | Each of the 5 skills carries exactly one `<inputs>…</inputs>` block at the correct insertion point with ≥1 key region | `test_every_skill_carries_at_least_one_key_region` (per-skill presence, `checked == 5`) |
| REQ-P26-01 | Each `When absent:` line names the `eda_artifact: none` tier | per-skill assertion the fallback line exists and contains `eda_artifact: none` |
| REQ-P26-02 | Every named EDA front-matter key exists in `templates/EDA.md` live key set (dotted path, `[]` for list-of-map) | per-skill/per-region set-membership vs `parse_eda_keys()` |
| REQ-P26-02 | Every named DATA-PROFILE key exists in `templates/DATA-PROFILE.yaml` live-plus-uncommented key set | per-skill/per-region set-membership vs `parse_profile_keys()` (uncomment `#` example lines first) |
| REQ-P26-02 | A renamed/fabricated key FAILS the suite (anti-silent-orphan) | `test_negative_control_orphan_key_is_rejected` (`grain.__orphan__`, `columns[].__orphan__`) |
| REQ-P26-02 | Parser did not degenerate to empty/over-broad (anti-vacuity) | `test_anchor_non_vacuity` (`len(eda_keys) >= 30`, known keys present, `columns[].null_rate` present only after uncomment) |
| REQ-P26-02 | CRLF-tolerant across both templates (EDA.md CRLF, DATA-PROFILE.yaml bare-LF, verified live) | every parse test splits on `\r?\n`; both templates parse with nonzero key count |
| REQ-P26-03 | `dsx/` byte-identical for the phase | `git diff --stat -- dsx/` empty (smoke) |
| REQ-P26-03 | Zero new finding codes (276 → 276) | `scripts/gen-finding-catalogue.py --check` exit 0 + `tests/test_finding_catalogue_invariant.py` (`_EXPECTED_TOTAL = 276`) |
| REQ-P26-03 | Installed copies re-synced and `--check` passes | `node install.mjs && node install.mjs --check` (NOT `--check` alone) |

---

## Wave 0 Requirements

- [x] `tests/test_skill_read_contracts.py` — entire test file is new; covers REQ-P26-01 and REQ-P26-02 in full (the guard: line-oriented stdlib parser, dotted-path set-membership, negative control, anti-vacuity, CRLF tolerance). **Landed 26-03 (`3d60f63` GREEN); 7 tests OK on real 3.12.10.**
- [x] No shared fixtures needed — reads `templates/EDA.md`, `templates/DATA-PROFILE.yaml`, and the five `skills/*/SKILL.md` directly via `Path(__file__).resolve().parents[1]`, matching every existing repo-integrity test
- [x] No framework install needed — `unittest` is stdlib

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| — | — | — | — |

*All phase behaviors have automated verification (static repo-integrity test + git/catalogue/installer smoke checks). No user-facing runtime behavior.*

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references
- [x] No watch-mode flags
- [x] Feedback latency < 60s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** validated 2026-09-07 (loop S2-5, orchestrator) — 3/3 requirements
(REQ-P26-01/02/03) COVERED by named `unittest` tests that exist and pass on real
Python 3.12.10; 0 MISSING, `nyquist_compliant: true`. Phase module
`tests.test_skill_read_contracts` re-run this firing = **7 tests OK**; the full suite
is **1590 OK**. Phase 26 has no user-facing runtime behaviour beyond agent-facing
skill prose and the static repo-integrity guard, so its acceptance test IS the
automated invariant set (no manual UAT step owed). Operator UAT confirmation batched
to HUMAN-QUEUE as HQ-42, non-blocking until S7-2.
