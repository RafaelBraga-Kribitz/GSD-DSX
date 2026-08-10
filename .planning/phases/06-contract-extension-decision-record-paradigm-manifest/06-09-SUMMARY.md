---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 09
subsystem: cli
tags: [argparse, jsonl, decision-record, audit-trail, fsync]

# Dependency graph
requires:
  - phase: 06-02
    provides: "dsx/decisions.py — schema, crash-safe append, tolerant reader, invocation identity, frame digest, decisions_path, report collection"
  - phase: 06-07
    provides: "dsx/frame/ package and DSX-PAR-001 registered at all four gate points; the cli.py state this plan edits"
provides:
  - "`dsx explain` subcommand — a pure read/render path over DECISIONS.jsonl that always exits 0"
  - "`add_common(include_block_on=...)` refactor so one subcommand can opt out of the block contract"
  - "Gate-path decision-trail emission: one invocation header plus sequentially-id'd records per run"
  - "DECISIONS.jsonl treated as a runtime artifact (gitignored), never a tracked file"
affects: [06-10, dsx-explain, decision-trail, audit]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Side-channel write: trail emission is wrapped so no failure mode can alter a gate verdict"
    - "Read/render separation: cmd_explain never imports Report, Severity, emit() or GATE_THRESHOLDS"

key-files:
  created: []
  modified:
    - dsx/cli.py
    - tests/test_dsx.py
    - .gitignore

key-decisions:
  - "`explain` carries no `--block-on` flag at all (D-04) — argparse rejects it with exit 2, rather than accepting and ignoring it, because a block flag on a command that always passes is a lie in the help text"
  - "`include_block_on` is keyword-only with default `True`, so all four pre-existing add_common call sites are unchanged by construction"
  - "A trail that cannot be written is a missing trail, not a failed gate — the write path is wrapped so an unwritable directory leaves every gate exit code untouched"

patterns-established:
  - "Invocation grouping: each gate run appends one header record, and explain defaults to rendering the most recent invocation only"
  - "Tolerant tail handling: a truncated or non-JSON final line is skipped, and the intact records before it still render"

requirements-completed: [REQ-P6-07, REQ-P6-08]

coverage:
  - id: D1
    description: "`dsx explain` subcommand renders a decision trail and exits 0 across every failure mode (missing spec, missing file, empty file, truncated tail line, unknown invocation id)"
    requirement: "REQ-P6-08"
    verification:
      - kind: integration
        ref: "tests/test_dsx.py#test_explain_missing_spec_exits_zero_not_two"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_explain_empty_trail_file_exits_zero"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_explain_truncated_tail_line_still_renders_intact_records"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_explain_unknown_invocation_id_exits_zero_and_reports_not_found"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_explain_no_args_from_dir_with_no_spec_exits_zero"
        status: pass
    human_judgment: false
  - id: D2
    description: "D-04 honored — `explain` accepts --spec/--phase-dir/--invocation/--json/--verbose and does NOT accept --block-on, while the other four subcommands keep it"
    requirement: "REQ-P6-08"
    verification:
      - kind: integration
        ref: "tests/test_dsx.py#test_explain_help_offers_no_block_on_flag"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_other_subcommands_still_accept_block_on"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_explain_json_is_parseable"
        status: pass
    human_judgment: false
  - id: D3
    description: "A `dsx gate` run appends one invocation header followed by sequentially-id'd decision records; a second run appends a new header leaving the first run intact"
    requirement: "REQ-P6-07"
    verification:
      - kind: integration
        ref: "tests/test_dsx.py#test_gate_writes_one_header_and_sequential_decision_records"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_second_gate_run_appends_new_header_leaving_first_run_intact"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_validate_check_audit_do_not_write_a_trail"
        status: pass
    human_judgment: false
  - id: D4
    description: "The trail is a side channel — a write failure never changes a gate's exit code, and adding the write left all four gate points' exit codes unchanged"
    requirement: "REQ-P6-07"
    verification:
      - kind: integration
        ref: "tests/test_dsx.py#test_unwritable_trail_directory_does_not_change_exit_code"
        status: pass
      - kind: integration
        ref: "tests/test_dsx.py#test_gate_every_point_still_exits_correctly_with_trail_write_added"
        status: pass
    human_judgment: false
  - id: D5
    description: "End-to-end round-trip: gate writes, explain reads back the same invocation id, selects between runs, survives a truncated tail, and names a record's counterfactual"
    requirement: "REQ-P6-08"
    verification:
      - kind: e2e
        ref: "tests/test_dsx.py#test_explain_names_the_invocation_id_the_gate_wrote"
        status: pass
      - kind: e2e
        ref: "tests/test_dsx.py#test_explain_renders_only_the_second_runs_records"
        status: pass
      - kind: e2e
        ref: "tests/test_dsx.py#test_explain_invocation_flag_selects_the_first_runs_records"
        status: pass
      - kind: e2e
        ref: "tests/test_dsx.py#test_truncated_tail_line_leaves_explain_at_exit_zero_with_survivors"
        status: pass
      - kind: e2e
        ref: "tests/test_dsx.py#test_rendered_text_names_the_counterfactual_of_at_least_one_record"
        status: pass
    human_judgment: false
  - id: D6
    description: "DECISIONS.jsonl is gitignored as a runtime artifact and never leaks into the tracked tree"
    verification:
      - kind: integration
        ref: "tests/test_dsx.py#test_decisions_jsonl_is_gitignored"
        status: pass
      - kind: other
        ref: "git status --porcelain examples/ | grep DECISIONS.jsonl → no match"
        status: pass
    human_judgment: false

# Metrics
duration: ~10min
completed: 2026-08-08
status: complete
---

# Phase 06 Plan 09: Decision Trail End to End Summary

**`dsx gate` writes a sequentially-id'd decision trail and `dsx explain` renders it, with the write wired as a side channel that no failure mode can turn into a gate verdict**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-08-08T01:26:56+02:00 (first task commit)
- **Completed:** 2026-08-08T01:32:42+02:00 (final task commit)
- **Tasks:** 3
- **Files modified:** 3 (+489 / −4)

## Accomplishments

- `dsx explain` subcommand: resolves a spec (or reports that it could not), reads `DECISIONS.jsonl` through the tolerant reader, and renders the most recent invocation's trail — exiting 0 on every failure mode the plan enumerated.
- `add_common` gained a keyword-only `include_block_on` parameter defaulting to `True`, so `explain` can be the one subcommand without a block flag while the four existing call sites are untouched by construction.
- The gate path now appends one invocation header (gate point, dsx version, digest of the `validity_frame:`/`inference:` blocks) followed by the records its checks produced, each carrying a sequential id and the run's invocation id.
- The write is wrapped so that an unwritable trail directory leaves every gate exit code exactly as it was — a trail that cannot be written is a missing trail, not a failed gate.
- 22 new tests pin all of it, including two-run invocation grouping, truncated-tail survival, and the D-04 help-text contract.

## Task Commits

Each task was committed atomically, RED before GREEN:

1. **Task 1: `add_common` refactor + `explain` subcommand** — `4967499` (test, RED) → `8a0c418` (feat, GREEN)
2. **Task 2: gate-path trail write** — `34df912` (test, RED) → `e4d9bf3` (feat, GREEN)
3. **Task 3: end-to-end round-trip and crash survival** — `2efbf25` (test)

Task 3 is a verification-only task — it adds e2e coverage over behavior Tasks 1–2 already landed, so it is a single `test(06-09)` commit with no paired implementation commit, matching the 06-05/06-06/06-08 precedent for test-only tasks.

**Plan metadata:** this SUMMARY (see Provenance below).

## Files Created/Modified

- `dsx/cli.py` (+147) — `cmd_explain`, `_render_decision_trail`, the `add_common(include_block_on=…)` refactor, and the gate-path trail write using the `resolve_root` value `cmd_gate` already computes
- `tests/test_dsx.py` (+345, 0 deletions) — 22 CLI-level tests across explain's failure modes, the gate write path, invocation grouping, and the e2e round-trip
- `.gitignore` (+1) — `DECISIONS.jsonl` ignored as a runtime artifact

## Decisions Made

- **`explain` rejects `--block-on` rather than ignoring it.** D-04 puts `explain` permanently outside the block contract. Accepting-and-ignoring the flag would leave a lie in the help text, so `include_block_on=False` removes it entirely and argparse exits 2 on use.
- **`include_block_on` is keyword-only with default `True`.** This makes "the four existing call sites keep working unchanged" a property of the signature rather than something to re-verify per call site.
- **Trail write is a side channel.** The mirror of D-04: if `explain` can never block, the write path must never be able to block either. Verified by forcing an unwritable directory and asserting the exit code is unmoved.

## Deviations from Plan

None — plan executed as written. No deviation rules fired; no auto-fixes were needed.

## Issues Encountered

**The executing agent was terminated mid-plan by a provider session limit.** It was cut off immediately after the final task commit, at the point of running the plan's `<verification>` block — so all three tasks' commits landed and the working tree was clean, but the SUMMARY and tracking updates were never written.

No work was lost and no partial state needed repair. See Provenance.

## Provenance

This SUMMARY was written by the execute-phase orchestrator during a `/gsd-resume-work` reconciliation, not by the executing agent, which was interrupted before it could write one. The orchestrator independently re-ran the plan's full `<verification>` block rather than trusting an agent self-report:

| Verification item | Result |
|---|---|
| `python -m unittest discover -s tests` | exit 0 — 270 tests, 0 failures |
| `python -m dsx explain --spec /nonexistent/spec.yaml` | exit 0 |
| `python -m dsx gate {plan,execute,verify,ship} --spec examples/good-ANALYSIS-SPEC.yaml` | all exit 0 |
| `python -m dsx gate plan --spec examples/bad-ANALYSIS-SPEC.yaml` | exit 1 |
| `python -m dsx gate ship --spec examples/bad-ANALYSIS-SPEC.yaml` | exit 1 |
| `python scripts/gen-finding-catalogue.py --check` | exit 0 |
| `git status --porcelain examples/` — untracked `DECISIONS.jsonl` | none leaked |
| `git diff --stat dsx/checks/` | no changes (D-13 preserved) |
| `git diff -U0 tests/test_dsx.py` — original 804–839 range | untouched (single pure-insertion hunk at 1481, 0 deleted lines) |

9/9 verification items pass. Contract truths were additionally spot-checked directly: `explain --block-on` exits 2 with 0 occurrences of `block-on` in its help; `add_common` carries `*, include_block_on: bool = True`; `cmd_gate` reaches `decisions_path`/`append` and `cmd_explain` reaches `read_all`/`_render_decision_trail`.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Plan 06-10 (the final plan in this phase) is unblocked: version bump to 2.0.0 across all declarations, catalogue regeneration, and the six-invocation closing phase gate.
- Test baseline for 06-10 to build on: **270 tests, 0 failures**; `gen-finding-catalogue.py --check` exits 0.
- **Carried concern (not introduced by this plan):** two citation locators remain unverified at sub-source granularity — the Deng, Lu & Chen (2016) section/theorem for `_validate_inference_shape` (from 06-06) and the Kohavi, Tang & Xu (2020) chapter for the shared-budget interference pattern (from 06-08). Author/year/title/venue match `brief.md` in both cases; only the sub-document locator is unconfirmed.
- **Carried concern (not introduced by this plan):** 06-08's two `<human-check>` reviews (interference post-mortem sourcing provenance; the Bayesian post-mortem's prior-averaged vs. point-null formulation) still await a human read-through.

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*
