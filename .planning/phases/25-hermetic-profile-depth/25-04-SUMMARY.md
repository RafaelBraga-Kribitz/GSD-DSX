---
phase: 25-hermetic-profile-depth
plan: 04
subsystem: docs
tags: [doc-ripple, profiler, hermetic, dq-gate, byte-invariant, installer, producer-only]

# Dependency graph
requires:
  - "25-01..25-03: profile_csv produces the full additive vocabulary (numeric, categorical, time, unit, target) reachable via `dsx profile --unit/--target`; dsx/checks/dq.py byte-frozen"
provides:
  - "templates/DATA-PROFILE.yaml: new keys documented as inert comments (numeric/categorical sub-maps, time additive keys, unit/target blocks) matching the existing commented-column style; scaffold parsed shape unchanged"
  - "references/data-quality-assertions.md: 'Producer-only depth keys (not gated)' subsection naming every additive key and stating no gate reads them this milestone"
  - "skills/dsx-explore-data/SKILL.md steps 1a/3a/4a/4b/4e/4f say 'copied from the profile' for the numbers the profiler now supplies; named exclusions (null cross-tabs, outlier taxonomy, impossible pairs, robust-metric recomputes, staleness) kept explicitly agent-computed"
  - "tests/test_profiler_hermetic.py::TestDocRipple, TestDQGateIgnoresNewKeys, TestExampleProfilesByteInvariant"
affects: [26]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Additive keys documented as YAML comments only — no live key added to the scaffold, so the loader parses the identical top-level/columns/time/sentinels_found shape as before the edit (columns stays empty, time stays the frozen 4-key block)."
    - "TestDocRipple is substring-based (CRLF-safe): asserts every additive key token appears in templates/DATA-PROFILE.yaml, 'copied from the profile' appears at least six times in SKILL.md (one per rippled step), 'staleness stays agent-computed' survives as the named-exclusion canary, and references marks the keys 'producer-only'."
    - "TestDQGateIgnoresNewKeys exercises the REAL dq.check(load(spec), tmp_dir) path — injects a full set of Phase-25 keys (columns.<col>.numeric/.categorical + top-level unit/target) into a temp copy of the good profile, appended after the existing keys, and proves the finding-code set and blocks(Severity.HIGH) verdict are identical to the stripped copy (the gate reads only its six .get() keys)."
    - "TestExampleProfilesByteInvariant pins sha256 over RAW bytes (CRLF included) of examples/{good,bad}-DATA-PROFILE.yaml to the current committed digests, so any future edit fails the suite (D-04 guard #4)."

key-files:
  created: []
  modified:
    - templates/DATA-PROFILE.yaml
    - references/data-quality-assertions.md
    - skills/dsx-explore-data/SKILL.md
    - tests/test_profiler_hermetic.py

key-decisions:
  - "D-04's REQ-P25-02 operationalization is RATIFIED at this plan gate: 'the committed example profiles regenerate identically' is realized as (4) example bytes invariant [TestExampleProfilesByteInvariant] + (3) producer invariance proven on the fixtures dsx profile can actually produce [25-01..25-03 golden/determinism tests]. Per 25-RESEARCH.md's reasoned PASS: the two example profiles are non-producer stand-ins (measured_export fake-hash / manual) with no source CSV, so literal regeneration is impossible; this operationalizes, it does not reword, the requirement."
  - "4b concentration: the profiler's categorical share_top1/share_top10 (level concentration) are marked 'copied from the profile', while the additive-measure concentration in 4b (top-1%/top-10% of the summed total, n_half, max_row_share, the summarisation decision) stays agent-computed — the profiler does not produce additive-measure row concentration. Documented truthfully rather than over-claiming."
  - "Named exclusions kept agent-side and marked as such: staleness (3a, needs wall-clock TODAY — the profiler emits only the hermetic input time.max), the robust half of 4a (trim10/mad_s/loc_gap/scale_ratio), and the untouched steps 2 (null cross-tabs), 4c (outlier taxonomy), 4d (impossible pairs)."

requirements-completed: [REQ-P25-01, REQ-P25-02, REQ-P25-03]

metrics:
  duration: 20min
  completed: 2026-09-07
  tasks: 3
  files-modified: 4

status: complete
---

# Phase 25 Plan 04: Doc ripple + whole-vocabulary guards + installer re-sync Summary

**The three documentation surfaces now say "copied from the profile" wherever `dsx profile` supplies the trust-core number (SKILL.md steps 1a/3a/4a/4b/4e/4f; templates/DATA-PROFILE.yaml new keys as inert comments; references/data-quality-assertions.md producer-only subsection), while the named exclusions stay explicitly agent-computed; three guard tests prove the DQ gate structurally ignores every new key and pin the example profiles byte-invariant; and the installer re-sync + `--check` gate passes with `dsx/checks/dq.py` byte-unchanged and the catalogue set-identity 276 → 276.**

## Performance
- **Duration:** ~20 min
- **Tasks:** 3/3 completed
- **Files modified:** 4 (`templates/DATA-PROFILE.yaml`, `references/data-quality-assertions.md`, `skills/dsx-explore-data/SKILL.md`, `tests/test_profiler_hermetic.py`)
- **Files created:** 0

## Task Commits
1. **Task 1 (doc ripple):** `e3a105c` — `docs(25-04): doc ripple -- profile depth keys 'copied from the profile'`
2. **Task 2 (whole-vocabulary guards):** `9f4c92f` — `test(25-04): whole-vocabulary guards -- DQ gate ignores new keys, example profiles byte-invariant`
3. **Task 3 (installer re-sync + frozen-file/catalogue proofs):** no commit — command-only; `install.mjs` writes the host overlay (outside the repo tree / gitignored), with no tracked-source edits, exactly as the plan specifies.

Branch: `gsd/v2.6.0-exploration-depth` (no branch created/switched; plain `git commit`; unpushed by design — the orchestrator re-verifies the gates and pushes).

## Verification (all on the real interpreter `C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`, 3.12.10)
- **Task 1:** `tests.test_profiler_hermetic.TestDocRipple` — 4 tests OK.
- **Task 2:** `tests.test_profiler_hermetic.TestDQGateIgnoresNewKeys tests.test_profiler_hermetic.TestExampleProfilesByteInvariant` — 2 tests OK. The DQ-gate test was additionally sanity-checked: the injected keys genuinely parse (user_id gains `numeric`+`categorical` alongside `null_rate`/`n_unique`/`dtype`; top-level `unit`/`target` present) and `dq.check` returns zero finding codes and no HIGH block either way.
- **Task 3:**
  - `node install.mjs` re-sync succeeded (7 payload entries, 6 agents, 14 skills, self-test passed); `node install.mjs --check` → **exit 0** (`self-test: passed`, `5 gates declared`).
  - `git diff --stat 83c4442..HEAD -- dsx/checks/dq.py` → **empty**; working-tree diff → **empty**.
  - `git diff --stat -- references/finding-codes.md` → **empty**.
  - `python.exe scripts/gen-finding-catalogue.py --check` → **exit 0** (`finding catalogue is current`). The `DSX-*** declared twice` warnings are pre-existing and unrelated (no gate module or `report.add(...)` site touched this phase).
  - `python.exe -m unittest tests.test_finding_catalogue_invariant -q` → 2 tests OK (set-identity **276 → 276**).
  - Full suite `python.exe -m unittest discover -s tests -q` → **1582 tests OK** (1576 25-03 baseline + 6 new). No failures, so no stray-`DECISIONS.jsonl` false-fail arose; the root `DECISIONS.jsonl` does not exist, and the gitignored strays under `examples/`/`templates/` did not affect the run.

## Pinned example-profile digests (raw bytes, CRLF included)
- `examples/good-DATA-PROFILE.yaml`: `3a2d220088a217f60523391f177d66561f2b7e051413855a60e639d30d3275d1`
- `examples/bad-DATA-PROFILE.yaml`: `723d2ba49c31190d33674c8015963dcd02edfb19b7bd0631c963d85b74c6c39a`

## D-04 ratification (REQ-P25-02)
D-04's operationalization of REQ-P25-02 ("the committed example profiles regenerate identically on every pre-existing key") as **(example bytes invariant) + (producer invariance proven on the fixtures `dsx profile` can actually produce)** is **ratified** here, per 25-RESEARCH.md's reasoned PASS. The literal text cannot be executed because the two example profiles are non-producer stand-ins (`measured_export` with a fabricated hash / `manual`) with no source CSV to regenerate from; the two-part split captures the requirement's intent using a mechanism that actually exists to test. `TestExampleProfilesByteInvariant` supplies the missing self-enforcing byte-diff assertion the research flagged as the one gap.

## Carried pending item (non-blocking)
- **HQ-40 row 40a (Hyndman & Fan type-number primary read):** remains a non-blocking pending item. The inclusive/type-7 mapping is triangulated from CPython's own source comment and R's documentation (both attribute the taxonomy to H&F 1996); the primary-paper Table 1 read is what HQ-40 40a exists to close. This phase mints no finding code and asserts a definition, not a label, so it is unaffected.

## Deviations from Plan
None. The three tasks executed exactly as written. One truthful clarification (not a deviation): in SKILL.md step 4b the profiler's categorical `share_top1`/`share_top10` (level concentration) are marked "copied from the profile", while the additive-measure concentration the step also computes (top-1%/top-10% of the summed total, `n_half`, the summarisation decision) is kept agent-computed, because the profiler does not produce additive-measure row concentration.

## Prohibitions honored
- Zero new finding codes; `dsx/checks/dq.py`, the `data[].assertions` vocabulary, and the gate profiles are byte-unchanged (git diff empty); catalogue set-identity 276 → 276.
- No gate reads a new profile key — the additive keys stay producer-only this milestone (proven by `TestDQGateIgnoresNewKeys`).
- The profiler is NOT asked to produce the named exclusions; the skill still asks the agent to compute exactly those (null cross-tabs, outlier taxonomy, impossible pairs, robust-metric recomputes, staleness).
- No edits to `.planning/REQUIREMENTS.md`, `.planning/STATE.md`, or `.planning/ROADMAP.md` (single-writer — orchestrator owns those).
- `examples/good-DATA-PROFILE.yaml` and `examples/bad-DATA-PROFILE.yaml` NOT edited (kept byte-invariant; digests pinned above).
- No non-stdlib import added anywhere. No branch created or switched; all commits on `gsd/v2.6.0-exploration-depth` via plain `git commit`; not pushed (orchestrator pushes after re-verifying gates).
- Operator-local untracked files (`.claude/*`, `.vscode/`, `graphify-out/`, `references/The AI Data Scientist.md`) left untouched — never staged.

## Known Stubs
None.

---
*Phase: 25-hermetic-profile-depth*
*Completed: 2026-09-07*

## Self-Check: PASSED

`templates/DATA-PROFILE.yaml`, `references/data-quality-assertions.md`, `skills/dsx-explore-data/SKILL.md`, `tests/test_profiler_hermetic.py`, and this SUMMARY confirmed present. Task commits `e3a105c` and `9f4c92f` confirmed in `git log`. `dsx/checks/dq.py` phase + working-tree diff confirmed empty. Full suite 1582 OK; `node install.mjs --check` exit 0; catalogue 276 → 276.
