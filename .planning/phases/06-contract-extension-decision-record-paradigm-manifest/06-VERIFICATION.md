---
phase: 06-contract-extension-decision-record-paradigm-manifest
verified: 2026-08-08T07:36:57Z
status: gaps_found
score: 5/6 must-haves verified
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "dsx explain and the gate-path decision-trail write are a pure side channel that can never change a gate's exit code, and DECISIONS.jsonl 'survives a crashed run' without exception (SC3, REQ-P6-07, REQ-P6-08; PLAN 06-09 must-have: 'A failure to write DECISIONS.jsonl never changes a gate's exit code — the trail is a side channel, not part of the block contract')"
    status: failed
    reason: >
      dsx/decisions.py::read_all() calls Path.read_text(encoding='utf-8') with
      no error handling. A DECISIONS.jsonl containing one non-UTF-8 byte (e.g.
      a truncated multi-byte character, hand-edit, or disk-level corruption of
      an already-written byte) makes read_all() raise UnicodeDecodeError,
      which propagates uncaught through two call sites: (1) cmd_explain calls
      read_all() directly with no try/except — dsx explain, documented as "a
      pure reader ... never blocks, always returns 0", exits 2 instead; (2)
      cmd_gate's next_invocation_id() (called before append(), as part of
      writing the trail) also calls read_all() — the same corruption makes
      `dsx gate plan` exit 2 on a spec that would otherwise cleanly pass or
      block, directly violating the documented "the trail is a side channel
      ... no failure mode can turn into a gate verdict" invariant. Both were
      independently reproduced against the live CLI (not inferred from code
      reading): `dsx explain --phase-dir <corrupted>` -> exit 2;
      `dsx gate plan --spec examples/good-ANALYSIS-SPEC.yaml` with the same
      corrupted DECISIONS.jsonl alongside it -> exit 2 instead of 0. The
      narrower must-have this phase's tests do cover — "one whose final line
      is a truncated JSON fragment" — passes cleanly (test_read_all_skips_truncated_tail_line,
      test_truncated_tail_line_leaves_explain_at_exit_zero_with_survivors), and
      because append() writes via json.dumps(..., ensure_ascii=True) (default),
      a genuine process-kill-mid-write of a record dsx itself produced is
      always ASCII and therefore degrades to the already-handled
      JSONDecodeError path, not this one. The gap is real for any other source
      of invalid bytes in the file (hand-edit, filesystem-level corruption of
      a byte already committed to disk — the exact scenario the module's own
      docstring claims to guard against — or a future change to
      ensure_ascii). Given dsx explain's contract states zero carve-outs
      ("always returns 0"), this is a provable, present-day contract
      violation, not a theoretical one.
    artifacts:
      - path: "dsx/decisions.py"
        issue: "read_all() (line ~117) has no error handling around Path.read_text(encoding='utf-8'); only json.JSONDecodeError is caught, not UnicodeDecodeError"
      - path: "dsx/cli.py"
        issue: "cmd_explain (~line 413) calls read_all() with no try/except at all; _write_decision_trail's except OSError (~line 306) does not catch UnicodeDecodeError either"
    missing:
      - "read_all() must tolerate encoding errors the same way it already tolerates JSON-level corruption, e.g. Path.read_text(encoding='utf-8', errors='replace') so a corrupted line degrades to the existing JSONDecodeError skip path instead of raising"
      - "A regression test asserting dsx explain exits 0 and dsx gate <point> exits its correct pass/block code when DECISIONS.jsonl contains a non-UTF-8 byte (not just a truncated-but-valid-UTF-8 JSON tail)"
deferred: []
---

# Phase 6: Contract extension, decision record, paradigm manifest — Verification Report

**Phase Goal:** The v2.0.0 contract surface exists and is trustworthy to read — `validity_frame:` and `inference:` parse correctly, decision records accumulate and render, the paradigm manifest is defined the moment `paradigm` becomes declarable, and D-05/D-03a are enforced mechanically before any check family exists to violate them.

**Verified:** 2026-08-08T07:36:57Z
**Status:** gaps_found
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria)

| # | Truth (ROADMAP Success Criterion) | Status | Evidence |
|---|---|---|---|
| 1 | `_parse_yaml_subset` treats `none` as the string `"none"` (scalar and sequence), a full `validity_frame:`+`inference:` spec round-trips, every new closed vocabulary is dumped by `dsx vocab`, `dependence.method_family_required` is typed against `VARIANCE_ADJUSTMENTS`, `PEEKING_POLICIES` has a member for uncontrolled continuous monitoring distinct from `always_valid`, and `inference.stopping_rule` does not exist | ✓ VERIFIED | Reproduced directly: `_parse_yaml_subset("x: none\n","<t>")` → `{'x': 'none'}`; `_parse_yaml_subset("x: [none, clustered]\n","<t>")` → `{'x': ['none','clustered']}`. `PEEKING_POLICIES` keys = `{always_valid, fixed_horizon, sequential_obf, sequential_pocock, uncontrolled_continuous}` (5 distinct members). `VARIANCE_ADJUSTMENTS = {mixed_effects, delta_method, bootstrap_cluster, cluster_robust}`, reused (not duplicated) by `dependence.method_family_required` per `dsx/spec.py`. `dsx vocab` runs and emits `question_types`, `peeking_policies`, etc. `grep stopping_rule dsx/spec.py` shows it only appears as the *removed*-field redirect (`_INFERENCE_REMOVED_FIELD = "stopping_rule"`), never as a live field. |
| 2 | `dsx gate` exits 0 at all 4 points on extended `good-ANALYSIS-SPEC.yaml`, 1 at plan/ship on extended `bad-ANALYSIS-SPEC.yaml`, existing D-08 tests unchanged, a descriptive spec omitting `interference`/`triggering`/`stability` exits 0 while a causal spec omitting them blocks | ✓ VERIFIED | Reproduced directly: `good` → plan/execute/verify/ship all exit 0; `bad` → all four exit 1. `test_causal_spec_with_no_validity_frame_key_reports_one_critical_itemising_ten`, `test_descriptive_spec_with_no_validity_frame_key_names_only_six`, `test_descriptive_spec_with_only_six_always_required_produces_no_findings`, `test_descriptive_experiment_design_still_requires_interference` all pass (tests/test_dsx.py:390-457) and assert exactly this causal/descriptive split, including the design-kind override for experiments. |
| 3a | A `paradigm: bayesian` spec that is otherwise clean exits 0 at `dsx gate ship` with `DSX-PAR-001` printed naming applied/not-applied check families; INFO cannot flip the exit code at any of the four default `GATE_THRESHOLDS` | ✓ VERIFIED | Cloned `examples/` into a scratch dir, flipped `paradigm: frequentist` → `bayesian`, ran all four gate points: plan/execute/verify/ship all exit 0, `DSX-PAR-001` present at `[INFO]` severity in every report, naming `applied: DSX-SPEC-08` and 7 `not applied` families with phase attributions. None of the 4 default thresholds (`CRITICAL, CRITICAL, HIGH, HIGH`) is ever `INFO`, so `DSX-PAR-001` structurally cannot flip any default gate's exit code. |
| 3b | `dsx explain` exits 0 rendering the run's decision trail from an append-only `DECISIONS.jsonl` that survives a crashed run; the trail write is a side channel that can never change a gate's exit code | ✗ FAILED | See `gaps` in frontmatter. The specific, tested crash scenario (a truncated-but-still-ASCII/UTF-8 JSON tail line — the realistic shape of a kill mid-`append()`, since `append()` always writes `ensure_ascii=True` JSON) is genuinely handled and passes (`test_read_all_skips_truncated_tail_line`, `test_truncated_tail_line_leaves_explain_at_exit_zero_with_survivors`). But `read_all()` has zero handling for non-UTF-8 bytes (hand-edit, disk corruption of an already-committed byte, or any future `ensure_ascii=False`), and this is reachable from *both* `cmd_explain` (documented "always returns 0", no carve-out) and the gate-path's `next_invocation_id()`→`read_all()` call inside `_write_decision_trail`. Independently reproduced: `dsx explain --phase-dir <dir-with-corrupted-DECISIONS.jsonl>` exits 2; `dsx gate plan --spec examples/good-ANALYSIS-SPEC.yaml` with the same corrupted file present exits 2 instead of 0. This directly falsifies PLAN 06-09's own must-have truth that a trail failure "never changes a gate's exit code." |
| 4 | `scripts/gen-finding-catalogue.py --check` exits non-zero on a check whose docstring lacks a citation marker, and the D-03a AST boundary test fails when a `dsx/frame/*.py` module imports `dsx.checks.*`, each proven against a deliberately violating fixture | ✓ VERIFIED | `python3 scripts/gen-finding-catalogue.py --check` exits 0 on the real tree. `tests/test_gen_finding_catalogue.py::TestD05EnforcementFixture` (4 tests) proves the enforcement fires against `tests/fixtures/d05/bad_check.py`, a deliberately violating fixture, and stays silent on compliant code — all pass. `tests/test_frame_boundary.py::TestFrameImportBoundary` (2 tests) proves the scanner fires on a deliberately violating source and confirms the real `dsx/frame/` modules import nothing from `dsx.checks` — both pass. |
| 5 | ≥3 known-bad fixtures (≥1 interference, ≥1 Bayesian continuous-monitoring) committed with post-mortems and pass `dsx validate` structurally; `.planning/REVERSALS.md` with D-14 template + `SELF-001`; README documents `suppressions[]` migration + the "a frame that lies passes" limit; version 2.0.0; catalogue regenerated | ✓ VERIFIED (see WARNING below) | 3 pairs exist under `examples/known-bad/` (interference-shared-budget, frequentist-uncontrolled-continuous, bayesian-continuous-monitoring), each `dsx validate --spec ...` exits 0 (reproduced directly, all three). `.planning/REVERSALS.md` has a `## Template` section and defines `SELF-001` explicitly (not just names it). `README.md` documents `suppressions[]` with the `authority` requirement (lines ~143-151) and states "The gate checks declarations against declarations — a frame that lies passes." (line 311). `dsx --version` → `dsx 2.0.0`; `dsx/__init__.py::__version__ == "2.0.0"`. `scripts/gen-finding-catalogue.py --check` exits 0. **However:** the three fixtures' header comments and the interference post-mortem assert the specific, falsifiable claim "today's dsx validate/gate checks pass it" / "passes every gate at every severity threshold as of this phase" — this is false as committed. Reproduced directly: all three fixtures exit 1 at `dsx gate verify` and `dsx gate ship` today, on findings unrelated to the documented target defect (missing `narrative.path`, no `reproducibility.entrypoint`, unresolved evidence pointers, an unwaived assumption). ROADMAP SC5's literal text only requires passing `dsx validate` structurally, which holds — so this is a documentation-accuracy defect in committed prose, not a Success-Criterion failure, but it is false, present in the tracked repository, and could mislead Phase 7/8/9/11 authors about what the corpus guarantees today. See WARNING below. |

**Score:** 5/6 truths verified (3b failed)

### Required Artifacts

| Artifact | Expected | Status | Details |
|---|---|---|---|
| `dsx/loader.py` | `_NULL` no longer treats `"none"` as null | ✓ VERIFIED | Reproduced: `_parse_yaml_subset` returns the string `"none"`, not `None`, for scalar and sequence positions |
| `dsx/spec.py` | 10 new closed vocabularies, `_VOCABULARIES` registry, `PEEKING_POLICIES.uncontrolled_continuous` | ✓ VERIFIED | Confirmed present and exercised by tests |
| `dsx/decisions.py` | Decision-record schema, crash-safe append, tolerant reader, invocation identity, frame digest | ⚠️ VERIFIED WITH GAP | Schema/append/determinism/digest all confirmed correct; `read_all()` is tolerant of JSON corruption but not encoding corruption — see gap above |
| `dsx/frame/__init__.py`, `dsx/frame/paradigm.py` | Import-boundary package, `DSX-PAR-001` | ✓ VERIFIED | Present, wired into all four `GATE_PROFILES`, boundary test passes against real + fixture sources |
| `scripts/gen-finding-catalogue.py` | D-05 mechanical enforcement | ✓ VERIFIED | `--check` exits 0 on the real tree; proven to fail against a deliberately violating fixture |
| `tests/test_frame_boundary.py` | D-03a AST boundary test | ✓ VERIFIED | Present, passes, proven against a violating case |
| `.planning/REVERSALS.md` | D-14 template + `SELF-001` | ✓ VERIFIED | Both present |
| `README.md` | `suppressions[]` migration path + known limit | ✓ VERIFIED | Both present, reachable from migration heading |
| `examples/known-bad/*` | ≥3 spec+post-mortem pairs | ✓ VERIFIED (prose accuracy: see WARNING) | 3 pairs present, structurally valid, `dsx validate` passes; header/post-mortem prose overstates gate behavior |
| `dsx/__init__.py` | Version `2.0.0` | ✓ VERIFIED | Confirmed via `--version` and source |
| `references/finding-codes.md` | Regenerated catalogue | ✓ VERIFIED | `--check` confirms currency |

### Key Link Verification

| From | To | Via | Status | Details |
|---|---|---|---|---|
| `dsx/cli.py::cmd_gate` | `dsx/decisions.py::append` | writes invocation header + records per run | ✓ WIRED | Confirmed by reproduction: a gate run writes `DECISIONS.jsonl` |
| `dsx/cli.py::cmd_gate` | `dsx/decisions.py::next_invocation_id`→`read_all` | reads before writing to derive the next id | ⚠️ WIRED BUT UNSAFE | This read is the exact path that lets a corrupted trail hijack a gate's exit code (gap above) |
| `dsx/cli.py::cmd_explain` | `dsx/decisions.py::read_all` | pure read/render | ⚠️ WIRED BUT UNSAFE | No try/except around the call; same root cause |
| `dsx/cli.py::run_checks` | `dsx/frame/paradigm.py::check` | generic `CHECKS[name]` dispatch | ✓ WIRED | `DSX-PAR-001` present in all four gate profiles' output |
| `dsx/spec.py::validate_structure` | `_validate_validity_frame_shape` / `_validate_inference_shape` | added to existing call chain | ✓ WIRED | Confirmed via `DSX-SPEC-080/081/082` firing in tests and live reproduction |

### Requirements Coverage

| Requirement | Source Plan | Status | Evidence |
|---|---|---|---|
| REQ-P6-01 | 06-01 | ✓ SATISFIED | `_NULL` fix confirmed, PEEKING_POLICIES/VARIANCE_ADJUSTMENTS confirmed |
| REQ-P6-02 | 06-05, 06-06 | ✓ SATISFIED | `validity_frame:` block round-trips, extended fixtures confirmed |
| REQ-P6-03 | 06-06 | ✓ SATISFIED | Requiredness-by-question_type confirmed via direct test read + reproduction |
| REQ-P6-04 | 06-05, 06-06 | ✓ SATISFIED | `inference:` block present, `stopping_rule` absent, redirect confirmed |
| REQ-P6-05 | 06-01 | ✓ SATISFIED | `uncontrolled_continuous` member confirmed distinct from `always_valid` |
| REQ-P6-06 | 06-01 | ✓ SATISFIED | `_VOCABULARIES` + `dsx vocab` + `VARIANCE_ADJUSTMENTS` reuse confirmed |
| REQ-P6-07 | 06-02, 06-09 | ⚠️ PARTIALLY SATISFIED | Schema/emitter/append/reader exist and mostly work; the "survives a crash without changing exit code" half is falsified by the CR-01 gap |
| REQ-P6-08 | 06-09 | ⚠️ PARTIALLY SATISFIED | `dsx explain` renders correctly and exits 0 for every *tested* failure mode; the untested non-UTF-8 mode makes it exit 2, contradicting "never participating in the block contract" |
| REQ-P6-09 | 06-07 | ✓ SATISFIED | `DSX-PAR-001` INFO-only, non-blocking at default thresholds, confirmed live |
| REQ-P6-10 | 06-07 | ✓ SATISFIED | `dsx/frame/` boundary + AST test confirmed |
| REQ-P6-11 | 06-03 | ✓ SATISFIED | D-05 mechanical enforcement confirmed live and via fixture |
| REQ-P6-12 | 06-05, 06-10 | ✓ SATISFIED | Good/bad fixtures extended, D-08 gate behavior confirmed unchanged |
| REQ-P6-13 | 06-08 | ✓ SATISFIED (prose caveat) | 3 fixtures committed, `dsx validate` passes; see WARNING on prose accuracy |
| REQ-P6-14 | 06-04 | ✓ SATISFIED | `.planning/REVERSALS.md` confirmed |
| REQ-P6-15 | 06-04 | ✓ SATISFIED | README migration path + known limit confirmed |
| REQ-P6-16 | 06-10 | ✓ SATISFIED | Version 2.0.0 + catalogue regen confirmed |

No orphaned requirements: all 16 `REQ-P6-*` IDs are declared across the 10 phase plans and all 16 are listed in `.planning/REQUIREMENTS.md`'s Phase 6 section; the milestone traceability table shows 53/53 mapped, no orphans, no duplicates.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|---|---|---|---|---|
| `dsx/decisions.py` | ~117 | Missing `errors=` handling around `read_text(encoding="utf-8")` | 🛑 BLOCKER | Root cause of the failed truth above |
| `examples/known-bad/*-ANALYSIS-SPEC.yaml` (3 files), `examples/known-bad/interference-shared-budget-POSTMORTEM.md` | header comments / prose | False claim: "today's dsx validate/gate checks pass it" / "passes every gate at every severity threshold" | ⚠️ WARNING | Misleads future readers (Phase 7/8/9/11 authors) about the corpus's actual current guarantee; `tests/test_known_bad_corpus.py` only asserts `dsx validate`, never `dsx gate`, so nothing catches this claim being false |
| `dsx/spec.py:830-833` | `_INFERENCE_FIELDS` | Dead constant creating a false impression that all 6 `inference:` fields are membership-checked (only 3 are) | ⚠️ WARNING | Maintainability/documentation-accuracy, not a functional break |
| `dsx/decisions.py:128-135` | `next_invocation_id()` + `append()` | Non-atomic read-then-write; concurrent `dsx gate` runs can collide on invocation IDs | ⚠️ WARNING | Not exercised by this phase's single-process test suite; documented limitation, not a regression from a prior working state |
| `scripts/gen-finding-catalogue.py:51` | `_D05_ALLOWLIST_PREFIXES` | `"DSX-SPEC-08"` is a bare numeric-string prefix, not boundary-safe | ⚠️ WARNING | Works correctly for the current code set; risk is forward-looking |
| `tests/test_frame_boundary.py:38-54` | `_package_for` | Dead if/else (both arms identical) | ℹ️ INFO | Cosmetic |

These six findings match `.planning/phases/06-contract-extension-decision-record-paradigm-manifest/06-REVIEW.md` (already committed, `status: issues_found`, 2 critical/3 warning/1 info) — I independently reproduced both CRITICAL findings against the live CLI rather than trusting the review's prose, per verifier protocol; results agree exactly with the review's reproductions.

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|---|---|---|---|
| Loader treats `none` as string | `_parse_yaml_subset("x: [none, clustered]\n", "<t>")` | `{'x': ['none', 'clustered']}` | ✓ PASS |
| Good fixture passes all 4 gates | `dsx gate {plan,execute,verify,ship} --spec examples/good-ANALYSIS-SPEC.yaml` | all exit 0 | ✓ PASS |
| Bad fixture blocked at all 4 gates | `dsx gate {plan,execute,verify,ship} --spec examples/bad-ANALYSIS-SPEC.yaml` | all exit 1 | ✓ PASS |
| Bayesian spec passes gate ship with manifest | flipped `paradigm: bayesian` in a scratch copy of `examples/`, ran all 4 gate points | all exit 0, `DSX-PAR-001` present at INFO | ✓ PASS |
| Known-bad fixtures pass `dsx validate` | `dsx validate --spec <each of 3>` | all exit 0 | ✓ PASS |
| Known-bad fixtures pass `dsx gate` (per fixture-file claim) | `dsx gate {verify,ship} --spec <each of 3>` | all exit 1 | ✗ FAIL (claim in committed prose is false — see WARNING) |
| `dsx explain` survives non-UTF-8 `DECISIONS.jsonl` | corrupted a byte in a temp `DECISIONS.jsonl`, ran `dsx explain --phase-dir <dir>` | exit 2 (documented: always 0) | ✗ FAIL |
| `dsx gate plan` unaffected by corrupted trail | same corrupted file, `dsx gate plan --spec examples/good-ANALYSIS-SPEC.yaml` | exit 2 (expected: 0, trail is a side channel) | ✗ FAIL |
| D-05 mechanical enforcement | `scripts/gen-finding-catalogue.py --check` on real tree | exit 0 | ✓ PASS |
| D-03a AST boundary test | `python3 -m unittest tests.test_frame_boundary -v` | 2/2 pass | ✓ PASS |
| Full suite | (already run by orchestrator) | 270 tests, exit 0 | ✓ PASS |

### Probe Execution

Not applicable — this project has no `scripts/*/tests/probe-*.sh` convention; no probes declared in PLAN/SUMMARY files for this phase.

### Human Verification Required

None. All must-haves and gaps in this report were resolved by direct, reproducible command execution against the live CLI — no items require subjective human judgment beyond what the phase's own plans already flagged as `human_judgment: true` (citation-locator provenance for the Kohavi and Deng sources, already tracked as open items in the 06-08/06-09 SUMMARYs and not part of this phase's ROADMAP success criteria).

### Gaps Summary

One BLOCKER: `dsx/decisions.py::read_all()` is not tolerant of non-UTF-8 bytes in `DECISIONS.jsonl`, even though its docstring and two call sites (`cmd_explain`, the gate-path trail writer) document an absolute "never blocks / always exits 0 / can never change a gate's exit code" contract. I independently reproduced both consequences against the live CLI: `dsx explain` exits 2 instead of 0, and `dsx gate plan` on an otherwise-clean spec exits 2 instead of 0, when a corrupted `DECISIONS.jsonl` is present. The narrower, tested scenario this phase's suite covers — a JSON-level-truncated tail line from a process kill mid-`append()` — is genuinely handled correctly (and, given `append()`'s `ensure_ascii=True` output, is the realistic shape of an actual dsx-caused crash). The gap is real for any other source of invalid bytes (hand-edit, disk corruption of an already-committed byte, or a future `ensure_ascii=False`). The fix is a one-line change (`errors="replace"` on the `read_text()` call), already specified in `06-REVIEW.md`.

One WARNING (documentation-accuracy, not a ROADMAP Success Criterion failure): the three `examples/known-bad/` fixtures' header comments and one post-mortem assert "today's dsx validate/gate checks pass it" / "passes every gate at every severity threshold" — this is false; all three block at `dsx gate verify` and `dsx gate ship` today on findings unrelated to the documented target defect. ROADMAP Success Criterion 5 only requires passing `dsx validate` structurally, which genuinely holds, so this does not fail the roadmap contract as literally written — but it is a false, committed, falsifiable claim that the test suite does not catch (`test_known_bad_corpus.py` only runs `dsx validate`, never `dsx gate`), and it risks misleading Phase 7/8/9/11 authors about what "passes every gate" means for this corpus going forward.

Three additional WARNING-level and one INFO-level maintainability findings are carried forward from `06-REVIEW.md` (dead `_INFERENCE_FIELDS` constant, non-atomic invocation-id allocation under concurrent gate runs, a non-boundary-safe D-05 allow-list prefix, a dead if/else in a test helper) — none of these block the phase goal.

Everything else — the `validity_frame:`/`inference:` contract surface, the closed vocabularies, the requiredness-by-question_type rules, the D-05/D-03a mechanical enforcement, the paradigm manifest's INFO-only non-blocking behavior, the known-bad corpus's structural validity, `.planning/REVERSALS.md`, the README migration path, and the version-2.0.0 bump — is verified working as documented, independently reproduced against the live CLI rather than trusted from SUMMARY.md prose.

---

_Verified: 2026-08-08T07:36:57Z_
_Verifier: Claude (gsd-verifier)_
