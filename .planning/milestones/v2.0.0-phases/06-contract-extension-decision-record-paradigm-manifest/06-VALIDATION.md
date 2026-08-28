---
phase: 6
slug: contract-extension-decision-record-paradigm-manifest
# status lifecycle: draft (seeded by plan-phase) → validated (set by validate-phase §6)
# audit-milestone §5.5 distinguishes NOT-VALIDATED (draft) from PARTIAL (validated + nyquist_compliant: false) (#2117)
status: validated
nyquist_compliant: true
wave_0_complete: true
created: 2026-08-07
validated: 2026-08-24
---

# Phase 6 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.
> Seeded by `/gsd-plan-phase 6` from `06-RESEARCH.md` § Validation Architecture.

---

> **Retroactive Nyquist audit (loop S0-8, 2026-08-24).** This phase shipped
> `passed` (06-VERIFICATION.md), but two requirements — REQ-P6-14 and REQ-P6-15 —
> were pure *documentation* requirements that had **no automated verification** at
> all: the only check on `.planning/REVERSALS.md` and the README migration/known-limit
> prose was a human copyability/clarity read (06-UAT, complete 2026-08-10). That
> made them the milestone's last real Nyquist gap. This audit closed it by
> generating **content-presence regression tests** (`tests/test_phase6_doc_presence.py`,
> 14 tests) that pin the required structural content — the D-14 reversal template's
> five fields, the `SELF-001` definition, the `suppressions[]` migration path with
> its `authority` requirement, and the "a frame that lies passes" caveat — so a
> future edit that deletes any of it fails the suite.
>
> **On the presence-vs-quality split:** the *presence* of the documented content is
> now mechanically guarded; the *quality* of the prose (is the template usable, is
> the caveat stated plainly and not softened) remains a human judgement, and it was
> already made and recorded in 06-UAT (2026-08-10). Nyquist compliance is about
> whether each requirement's implemented, mechanically-checkable behavior has
> automated verification — it now does for all 16 REQ-P6 — not about relocating a
> completed human judgement into code.

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | `unittest` (Python 3.9+ stdlib) — the only test runner used anywhere in this codebase |
| **Config file** | none — no `pytest.ini` / `setup.cfg` / `pyproject.toml` test config exists; tests are discovered by directory convention |
| **Quick run command** | `python3 -m unittest discover -s tests` |
| **Full suite command** | `python3 -m unittest discover -s tests -v` |
| **Estimated runtime** | ~0.25 seconds (160 tests, measured during research) |

**Note:** the suite is fast enough that there is no meaningful quick-vs-full distinction. Run the
full suite every time; there is no subset worth maintaining.

---

## Sampling Rate

- **After every task commit:** `python3 -m unittest discover -s tests`
- **After every plan wave:** `python3 -m unittest discover -s tests -v` **plus**
  `python3 scripts/gen-finding-catalogue.py --check`
- **Before `/gsd-verify-work`:** full suite green, catalogue current, and all six gate
  invocations behaving:
  - `dsx gate {plan,execute,verify,ship} --spec examples/good-ANALYSIS-SPEC.yaml` → exit `0`
  - `dsx gate plan --spec examples/bad-ANALYSIS-SPEC.yaml` → exit `1`
  - `dsx gate ship --spec examples/bad-ANALYSIS-SPEC.yaml` → exit `1`
- **Max feedback latency:** 1 second

---

## Per-Task Verification Map

> Task IDs are assigned by the plans. This table is seeded at requirement granularity; the
> `Task ID` column is completed once `*-PLAN.md` files exist, and `Status` is maintained during
> execution.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01/T1 | 06-01 | 1 | REQ-P6-01 | T-6-04 | Parser agrees with PyYAML on the literal `none`; a declared value never silently becomes null | unit | `python3 -m unittest tests.test_dsx.TestLoader -v` | ❌ W0 (new method) | ⬜ pending |
| 06-05/T1,T3 · 06-06/T1 | 06-05, 06-06 | 2, 3 | REQ-P6-02 | T-6-11, T-6-12 | Malformed `validity_frame` degrades to a finding, never an exception (exit 1, not exit 2) | unit/integration | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` | ❌ W0 | ⬜ pending |
| 06-06/T1 | 06-06 | 3 | REQ-P6-03 | T-6-12 | Requiredness gating is data, not a branch; absence blocks from `plan` at CRITICAL | unit | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` | ❌ W0 | ⬜ pending |
| 06-05/T1 · 06-06/T2 | 06-05, 06-06 | 2, 3 | REQ-P6-04 | T-6-07 | A field removed by M-02 produces a redirect finding rather than silence | unit | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` | ❌ W0 | ⬜ pending |
| 06-01/T2 | 06-01 | 1 | REQ-P6-05 | T-6-18 | `DSX-EXP-060`'s trigger set is pinned by a parametrised disjointness test (M-01) | unit | `python3 -m unittest tests.test_dsx.TestDesign -v` | ❌ W0 | ⬜ pending |
| 06-01/T2 | 06-01 | 1 | REQ-P6-06 | — | N/A | unit | `python3 -m unittest tests.test_dsx.TestSpecStructure -v` | ❌ W0 | ⬜ pending |
| 06-02/T1,T2 · 06-09/T2 | 06-02, 06-09 | 1, 5 | REQ-P6-07 | T-6-02, T-6-05, T-6-19 | Tolerant reader: a truncated tail line is skipped, not fatal; fsync per record; a write failure never changes an exit code | unit | `python3 -m unittest tests.test_decisions -v` | ❌ W0 (new file) | ⬜ pending |
| 06-09/T1,T3 | 06-09 | 5 | REQ-P6-08 | T-6-02 | `dsx explain` exits `0` on empty, missing, corrupt and unknown-invocation `DECISIONS.jsonl`, and on a missing spec | integration | `python3 -m unittest tests.test_dsx.TestDecisionTrailCLI -v` | ❌ W0 | ⬜ pending |
| 06-07/T2,T3 | 06-07 | 4 | REQ-P6-09 | T-6-14, T-6-15 | INFO cannot flip the exit code at any of the four default `GATE_THRESHOLDS`; the manifest never names an unshipped family as applied | unit + integration | `python3 -m unittest tests.test_dsx.TestCLI -v` | ❌ W0 | ⬜ pending |
| 06-07/T1 | 06-07 | 4 | REQ-P6-10 | T-6-01 | `dsx/frame/*` never imports `dsx.checks.*` (D-03a blast-radius control), proven against three violating sources | unit (meta-test) | `python3 -m unittest tests.test_frame_boundary -v` | ❌ W0 (new file) | ⬜ pending |
| 06-03/T1,T2 | 06-03 | 1 | REQ-P6-11 | T-6-07, T-6-08 | Both halves of D-05 fail the build on a violating fixture; the allow-list is finite and visible | unit (meta-test) | `python3 -m unittest tests.test_gen_finding_catalogue -v` | ❌ W0 (new file) | ⬜ pending |
| 06-05/T1,T2 · 06-10/T2 | 06-05, 06-10 | 2, 6 | REQ-P6-12 | T-6-11 | The three D-08 tests and the `_run` harness stay byte-for-byte unedited | integration | `python3 -m unittest tests.test_dsx.TestCLI -v` | ✅ `tests/test_dsx.py:804-839` | ⬜ pending |
| 06-08/T1,T2,T3 | 06-08 | 4 | REQ-P6-13 | T-6-16, T-6-17 | Every post-mortem traces to a primary source; the Bayesian fixture names its formulation | integration | `python3 -m unittest tests.test_known_bad_corpus -v` | ❌ W0 (new file) | ⬜ pending |
| 06-04/T1 | 06-04 | 1 | REQ-P6-14 | T-6-10 | The D-14 template's five fields and the `SELF-001` definition stay present in `.planning/REVERSALS.md` | doc-presence (content regression) | `python3 -m unittest tests.test_phase6_doc_presence.TestReversalsDocPresence` | ✅ `tests/test_phase6_doc_presence.py` (S0-8) | ✅ green |
| 06-04/T2 | 06-04 | 1 | REQ-P6-15 | T-6-09 | The `suppressions[]` migration path with its `authority` requirement, and the "a frame that lies passes" caveat, stay documented in README.md | doc-presence (content regression) | `python3 -m unittest tests.test_phase6_doc_presence.TestReadmeSuppressionsMigration` | ✅ `tests/test_phase6_doc_presence.py` (S0-8) | ✅ green |
| 06-10/T1,T2 | 06-10 | 6 | REQ-P6-16 | T-6-20, T-6-21 | Every version declaration agrees; the catalogue's rendered rows equal its declared total | integration | `python3 scripts/gen-finding-catalogue.py --check` | ✅ exists | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_frame_boundary.py` — new file; covers REQ-P6-10. Neither the test nor
      `dsx/frame/` exists yet.
- [ ] `tests/test_decisions.py` — new file (or a `TestDecisions` class in `test_dsx.py`);
      covers REQ-P6-07.
- [ ] `tests/test_gen_finding_catalogue.py` — new file (or a `--self-test` mode in the script
      itself); covers REQ-P6-11.
- [ ] New test methods inside the existing `TestLoader` / `TestSpecStructure` / `TestCLI`
      classes in `tests/test_dsx.py` for REQ-P6-01/02/03/04/05/06/08/09/13. No new file — the
      existing 1606-line file's per-class organisation is the right home.
- [ ] No framework install needed — `unittest` is stdlib.

**Do not modify** `tests/test_dsx.py:804-839` (the two D-08 fixture tests). REQ-P6-12 requires
they stay green *unedited*; extending the fixtures is allowed, editing these assertions is not.

---

## Manual-Only Verifications

> **Presence is now automated (S0-8, 2026-08-24); only the *quality* reads below stay
> human.** `tests/test_phase6_doc_presence.py` mechanically pins that the required
> content still *exists*. The three REQ-P6-14/-15 rows below are the quality judgements
> a machine cannot make — all were completed in 06-UAT (2026-08-10), so they are
> recorded as done, not open.

| Behavior | Requirement | Why Manual | Status |
|----------|-------------|------------|--------|
| `.planning/REVERSALS.md`'s D-14 template is *usable* and `SELF-001` is *defined, not merely mentioned* | REQ-P6-14 | Whether the template is genuinely copy-and-usable is a judgement; its *presence* is now automated (`TestReversalsDocPresence`) | ✅ completed 06-UAT 2026-08-10 |
| The README `suppressions[]` migration section reads as a *requirement* and is discoverable from the pre-v2.0.0 upgrade path | REQ-P6-15 | Prose accuracy/discoverability need human judgement; the section's *presence* is now automated (`TestReadmeSuppressionsMigration`) | ✅ completed 06-UAT 2026-08-10 |
| The "a frame that lies passes" limit is stated *plainly, not buried or softened* | REQ-P6-15 | Tone/prominence of the central honesty caveat is a judgement; its *presence* is now automated (`TestReadmeSuppressionsMigration`) | ✅ completed 06-UAT 2026-08-10 |

REQ-P6-13's post-mortem *quality* read (structural parsing is automated separately in `tests.test_known_bad_corpus`):

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Each `examples/known-bad/*` fixture has a post-mortem that explains what went wrong | REQ-P6-13 | A post-mortem's usefulness is a judgement call; structural parsing is automated separately | Read each post-mortem; confirm it names the real-world failure, not a synthetic one |

---

## Validation Sign-Off

- [x] All tasks have `<automated>` verify or Wave 0 dependencies
- [x] Sampling continuity: no 3 consecutive tasks without automated verify
- [x] Wave 0 covers all MISSING references — REQ-P6-14/-15 filled 2026-08-24 (S0-8)
- [x] No watch-mode flags
- [x] Feedback latency < 1s
- [x] `nyquist_compliant: true` set in frontmatter

**Approval:** approved 2026-08-24 (retroactive audit, loop S0-8)

---

## Validation Audit 2026-08-24

| Metric | Count |
|--------|-------|
| Gaps found | 2 |
| Resolved | 2 |
| Escalated | 0 |

The two gaps were REQ-P6-14 (`.planning/REVERSALS.md` D-14 template + `SELF-001`) and
REQ-P6-15 (README `suppressions[]` migration path + "a frame that lies passes" limit) —
pure documentation requirements with **no automated verification** before this audit
(grep confirmed: zero tests referenced `REVERSALS.md`, `SELF-001`, or the frame-lies
caveat). Both resolved by generating `tests/test_phase6_doc_presence.py` (14
content-presence tests) via `gsd-nyquist-auditor` (haiku, adaptive profile), then
independently re-gated by the orchestrator. All other 14 REQ-P6 requirements'
implemented behaviors were already COVERED by committed automated tests (06 shipped
`passed`). Evidence: target `tests.test_phase6_doc_presence` 14 OK; full
`bash scripts/check.sh` → `all checks passed`, `Ran 1052 tests ... OK` (1038 baseline
+ 14 new), catalogue current, capability manifest conformant, gate contract + determinism
green. D-05/quality reads for REQ-P6-13/-14/-15 were completed in 06-UAT (2026-08-10);
this audit added the presence guard beneath them, it did not reopen them.
