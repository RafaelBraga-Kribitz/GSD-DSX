---
phase: 26
slug: per-skill-read-contracts
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-09-07
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

> Placeholder — task IDs (`26-NN-NN`) do not exist until the planner writes PLAN.md.
> validate-phase (S2-5) fills this from the executed plan. The requirement→behavior
> coverage below is the draft contract the map must satisfy.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 26-NN-NN | NN | N | REQ-P26-01 | — | N/A (agent-facing prose + static test) | unit | `python -m unittest tests.test_skill_read_contracts -v` | ❌ W0 | ⬜ pending |

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

- [ ] `tests/test_skill_read_contracts.py` — entire test file is new; covers REQ-P26-01 and REQ-P26-02 in full (the guard: line-oriented stdlib parser, dotted-path set-membership, negative control, anti-vacuity, CRLF tolerance)
- [ ] No shared fixtures needed — reads `templates/EDA.md`, `templates/DATA-PROFILE.yaml`, and the five `skills/*/SKILL.md` directly via `Path(__file__).resolve().parents[1]`, matching every existing repo-integrity test
- [ ] No framework install needed — `unittest` is stdlib

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| — | — | — | — |

*All phase behaviors have automated verification (static repo-integrity test + git/catalogue/installer smoke checks). No user-facing runtime behavior.*

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 60s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
