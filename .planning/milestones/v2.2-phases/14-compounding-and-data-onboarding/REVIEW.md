# Phase 14 — Code Review (S2-4)

**Reviewer:** ceremony orchestrator, direct (opus/high, LOOP-BRIEF §3). Not spawned to
`gsd-code-reviewer`: the diff is a small, bounded doc/skill/template phase (24 content
files + 1 Python test, no `dsx/**.py`), and every load-bearing gate below was **re-run by
the orchestrator here** (brief §5), not trusted from a subagent report.
**Date:** 2026-08-28
**Diff under review:** `git diff 2236bb4..720ba10` (the five Phase-14 feature commits
`38801a0, 6ddee4c, 5e54297, 4d418b9, 720ba10`; 27 files, +756/−15).

## Verdict: **PASS — 0 blocking, 0 fixes applied.** 1 non-blocking observation.

This is a skill/doc/template phase whose entire correctness rests on two things: (a) it
mints no finding code and never touches the deterministic gate path, and (b) each of the
six requirements is delivered faithfully to the D-01..D-07 decisions. Both hold under
re-run gates.

## Load-bearing checks (all re-run this firing)

| # | Check | Command | Result |
|---|---|---|---|
| 1 | Gate-path purity — no `dsx/**.py` edits | `git diff --stat 2236bb4 720ba10 -- dsx/` | **empty** ✓ |
| 2 | `capability.json` untouched (hooks stays `[]`) | `git diff --stat … -- capabilities/dsx/capability.json` | **empty**; `hooks: []` / `supported: ["*"]` still at `:58`/`:13` ✓ |
| 3 | Zero-mint by count **and** set | `python -m unittest tests.test_finding_catalogue_invariant` | **2 OK** (256 count + set-identity `added=[] removed=[]`) ✓ |
| 4 | Catalogue current | `python scripts/gen-finding-catalogue.py --check` | **exit 0** (only the S0-2 known double-declare noise) ✓ |
| 5 | No `report.add` slipped into an off-gate CLI | `grep -c report.add dsx/cli.py` | **0** ✓ |
| 6 | Hermeticity guard actually guards | `python -m unittest tests.test_gate_path_hermetic` | **2 OK** (no pandas/scipy/numpy/csv in any `GATE_PROFILES` closure; profiler absent from `dq.py` closure) ✓ |
| 7 | Citation authenticity — only cited code exists | `grep -c DSX-DQ-001 references/finding-codes.md` | **1** (the sole `DSX-*` cited, in operating-guide §9) ✓ |
| 8 | REQ-P14-04 — no `data_storage/` folder | `grep -rn data_storage .claude/commands/ skills/` | **no match** ✓ |
| 9 | REQ-P14-04 — Triggers clause on all 13 DSX skills | `grep -rl "Triggers:" skills/*/SKILL.md` + per-skill scan | **13/13**, none missing ✓ |
| 10 | No data-lib in the new alias/fragment files | `grep -rn "pandas\|scipy" .claude/commands/ …/researcher.md` | **no match** ✓ |
| 11 | Full suite | `sh scripts/check.sh` | **all checks passed** — Ran **1232** tests OK; catalogue current; capability conformant (13 skills); gate contract; determinism ✓ |

## Requirement fidelity (spot-read against D-01..D-07)

- **REQ-P14-01 (D-02):** `docs/dsx/learnings/README.md` fixes the frontmatter schema
  (closed key set + order); the seed exemplar `2026-08-28-join-fanout-inflates-additive-metrics.md`
  carries that exact key set in order (`date` matches the filename date — no year skew),
  `domain: business_intelligence` is a real `dsx.domain` enum value, `question_type: diagnostic`
  is in the declared closed vocab, body is What/So What/Now What. The **search-before-framing**
  step is inserted as **step 0** of `dsx-scope-analysis` `<process>` (before Scaffold), greps the
  fixed keys, records `searched dated learnings: none found` on a miss (absence as a recorded
  result), and cites the README as schema authority; a one-line pointer is added to
  `fragments/researcher.md`'s "Has this been analysed before?" contract. Producer named =
  existing `gsd-extract-learnings` (referenced, not owned).
- **REQ-P14-02 (D-03):** `templates/DATA-DICTIONARY.md` mirrors the `EDA.md`
  written-then-ungated precedent; `dsx-explore-data` step 4 authors it next to
  `DATA-PROFILE.yaml`, copying `column/dtype/null_rate/unique_count/source_hash` **verbatim**
  and authoring only the semantics the CSV cannot carry. Explicitly "written and read but NOT
  gated"; the skill's closing gate note updated to "do not read `EDA.md` or `DATA-DICTIONARY.md`."
- **REQ-P14-03 (D-04):** `dsx-narrate` `<disclosure>` block reads `dsx.domain` via the
  documented `gsd-tools config-get` and offers the block **only on the literal `research`**
  value; for `auto`/`marketing_science`/every other value the path is byte-unchanged **by
  construction** (guard on the literal value; `auto` never infers it). `templates/DISCLOSURE-research.md`
  is GUIDE-LLM-**structured**, explicitly a template not a dependency (nothing installed/imported).
  Opt-in even under research; no `DSX-NAR` mint, no heading-scanner gate.
- **REQ-P14-04 (D-05):** operating-guide §9 alias table (all 13 skills) + Triggers clause on
  all 13 skill descriptions is the **portable** path (`supported:["*"]`); 2 `.claude/commands/*.md`
  shims ship as explicitly non-load-bearing Claude-Code-only sugar. CSV passed as an argument;
  no `data_storage/` folder; no `capability.json aliases` key. (Only 2 shims vs 13 documented
  aliases is by design — the convention + description triggers are the mechanism, not the shims.)
- **REQ-P14-05 (D-06):** documented-skip branch. Operating-guide "Why there is no file-drop
  hook" states all four honesty claims (no file-drop event in the portable floor; `FileChanged`
  is CC-family-only / runtime-gated / filename-matched / config-reload-only / unverified on a new
  CSV; `supported:["*"]` forbids a single-host silent-no-op hook; `dsx profile` stays
  analyst-invoked with the exact command) plus the `DSX-DQ-001` compensating control and the
  reversal condition. `capability.json hooks` stays `[]`.
- **REQ-P14-06 (D-07):** rows 3–6, 11 above. Zero mint by construction (no `dsx/` edit) and by
  proof (256 count + set-identity + `--check` exit 0), with a new standing hermeticity guard.

## Non-blocking observation (not fixed — deliberately)

- **N1 — `tests/test_gate_path_hermetic.py` closure walk does not traverse absolute dotted
  `import dsx.x` statements.** The walker adds a file to the frontier for `from dsx.x import …`
  (`ast.ImportFrom`) and relative imports, but a bare `import dsx.submodule` (`ast.Import`,
  dotted) only records its top-level name (`dsx`) without recursing into that submodule. Impact
  is negligible: every **third-party** forbidden import (`import pandas`, `import numpy`, …) *is*
  captured directly in the top-level-name set (the test's primary purpose), and the gate modules
  use `from`-imports, which the closure does follow. The only theoretical gap is a forbidden
  import reachable *solely* through an `import dsx.x` chain — an unusual form absent from the
  current gate path. This test is **optional hardening** (D-07 "planner's call"), it passes, and
  it protects the real regression it was written for. **Left as-is:** widening the walk risks
  introducing a bug in an off-requirement guard for no requirement gain (gold-plating). Recorded
  here so a future closure-completeness pass has the note.

## Fixes applied

None — nothing blocking or fix-worthy was found.
