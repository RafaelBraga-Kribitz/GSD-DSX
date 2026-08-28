---
phase: 10-pre-registered-inference-plan-dsx-pre
verified: 2026-08-20T13:30:00Z
status: passed
score: 5/5 must-haves verified
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: passed
  previous_score: 5/5
  gaps_closed:
    - "SC4 / REQ-P10-02's M-07 grandfather route (missing plan-time header + suppressions[]) — the earlier pass cited the exit-2 message naming `suppressions[]` as evidence without ever declaring a real suppression and observing its effect. CR-01 (10-REVIEW.md) found the route was inert (the raise in `_check_content_lock` happens before `apply_suppressions` ever runs); this is now fixed in `d8ff23e` and independently re-verified below by direct `dsx gate verify` runs, not by re-reading the old report's claim."
  gaps_remaining: []
  regressions: []
---

# Phase 10: Pre-registered inference plan (`DSX-PRE-*`) Verification Report

**Phase Goal:** The declared inference plan is held to the executed one — a fallback rule parses to a
decidable branch, `declared_at` provenance is named for the unverifiable self-declaration it is, and a
procedure switched after seeing the data is blocked with both branches named.

**Verified:** 2026-08-20 (re-verification, against HEAD after CR-01/WR-01 fixes)
**Status:** passed
**Re-verification:** Yes — a deep code review after the first pass found a Critical defect (CR-01) and
a Warning (WR-01); both were fixed in four commits (`cc96644`, `d8ff23e`, `406828d`, `d3490ee`) and
reconciled in the traceability table by `10c527e`. This report re-derives every conclusion from current
HEAD; nothing is carried forward from the superseded `passed` verdict.

## What changed since the superseded pass, and how it was re-checked

**CR-01 (Critical, `10-REVIEW.md`).** `_check_content_lock`'s exit-2 message for a missing plan-time
header named a `suppressions[]` "grandfather route" that did not exist in the code: the `CheckError`
raised directly inside `dsx.cli.run_checks`'s per-check loop (`dsx/cli.py:192`), before
`apply_suppressions` ever runs (`dsx/cli.py:202`). The prior verification pass's SC4 evidence line
("Missing plan-time header on `dsx gate verify` stops at exit 2, naming `suppressions`") tested that
the message *names* the route, not that a declared suppression *works* — exactly the gap CR-01 found.
The fix (`d8ff23e`) adds `_has_grandfather_suppression(spec)` inside `dsx/frame/prereg.py`, checked
*before* the raise, matching `apply_suppressions`'s own bar for a usable row (`code == "DSX-PRE-020"`,
non-blank `reason`, non-blank `authority`).

Re-checked directly against HEAD, not by re-running the unit tests alone: built six scratch
`ANALYSIS-SPEC.yaml` fixtures outside the repository (system temp) and ran real
`python -m dsx gate verify` invocations against fresh, un-seeded phase directories:

| Fixture | `suppressions[]` row | Observed | Matches CR-01's requirement |
|---|---|---|---|
| no suppression | none | exit 2, message names `DSX-PRE-020`, `suppressions`, `authority`, `dsx gate plan` | yes — still blocks |
| valid grandfather row | `code: DSX-PRE-020, reason: "predates the plan gate", authority: "ADR-999"` | no exit 2; run proceeds to the rest of the check suite (blocked at HIGH on unrelated corpus-completeness findings — `DSX-DQ-001`, `DSX-CLM-031`, etc. — with **zero** `DSX-PRE-020` finding anywhere in the output) | yes — the route is now real |
| row missing `reason` | `code: DSX-PRE-020, reason: "", authority: "ADR-999"` | exit 2, same message | yes — does not unlock |
| row missing `authority` | `code: DSX-PRE-020, reason: "...", authority: ""` | exit 2, same message | yes — does not unlock |
| row naming a different code | `code: DSX-PRE-010, ...` | exit 2, same message | yes — does not unlock |
| valid grandfather row **plus** an unknown code (`DSX-FAKE-999`) in the same `suppressions[]` list | both rows present | the missing-header raise is bypassed, but the run still aborts at exit 2 later, in `apply_suppressions`, with `spec.suppressions[1].code 'DSX-FAKE-999' is not a known DSX finding code` | yes — CR-01's explicit "an unknown code still aborts the run at exit 2" property holds even with a valid grandfather row present |

All six outcomes match `tests/test_frame_prereg.py::TestMissingPlanHeader` tests 9–14 (added in `cc96644`,
made to pass in `d8ff23e`), and the live runs above are independent evidence, not a re-read of those
tests. `python -m unittest tests.test_frame_prereg.TestMissingPlanHeader -v` — 14/14 ok.

**Judgment on whether this trades one gap for another (asked for explicitly):** No new gap. The bypass
bar is byte-for-byte the same bar `apply_suppressions` already holds every other suppression in this
codebase to (`dsx/suppressions.py:190-197`) — it is not a weaker or easier-to-obtain bypass than an
ordinary finding suppression, and its use is visible and attributable in the committed spec (a reviewer
can see the `authority` pointer). It does not verify that the authority pointer is *true* — but no
suppression anywhere in this project verifies truthfulness of its `authority` field; that is an
accepted, pre-existing property of the suppression mechanism, not a new limit CR-01's fix introduced.
This now matches what `10-CONTEXT.md` D-09 and `10-03-PLAN.md`'s T-10-10 actually asked for ("the
grandfather path stays walkable and attributable... not mitigated by letting the missing header pass")
— walkable is now true, and D-09's "never silently pass" is still enforced: a spec with no
authority-backed suppression and no recorded plan header still exits 2 unconditionally (row 1, 3, 4, 5
above).

**WR-01 (Warning, `10-REVIEW.md`).** `PREREG_FACTS.get(parsed.fact)` was case-sensitive against an
all-lowercase registry, so `Alpha <= 0.05 -> ...` fired `DSX-PRE-010` even though `alpha` is registered.
Fixed in `d3490ee` via `_PREREG_FACTS_NORMALIZED` (built once at module scope) and `normalize()` at both
call sites (`_resolve_branch` and `_check_rule_resolves`'s `inputs` re-derivation). Re-checked directly:

```
$ python -c "from dsx.frame import prereg; r = prereg._resolve_branch({'inference': {'primary_procedure': 'two_proportion_z', 'fallback_rule': 'Alpha <= 0.05 -> alpha_spending_obf'}, 'design': {'alpha': 0.03}}); print(r)"
_Resolution(branch='alpha_spending_obf', reason=None, source='fallback_rule')
```

No `DSX-PRE-010` fires for the capitalized spelling. `tests/test_frame_prereg.py::TestFactNameCaseNormalization`
(4 tests, including the literal `Comparisons_Looked_At` repro from the review) — all pass.

## Goal Achievement

### Observable Truths (ROADMAP Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A fallback rule resolves to exactly one branch against declared facts; an unparseable rule exits 2, never 0 | VERIFIED | Real gate run: `fallback_rule: "not a valid rule -> "` against a scratch fixture → `dsx check prereg` printed `dsx: fallback_rule condition 'not a valid rule' does not match the expected form <fact> <op> <number> -> <branch>` and exited **2**. `_resolve_branch`'s single-condition grammar with implicit else structurally has exactly two outcomes. `TestFallbackRuleParsing`/`TestBranchResolution`/`TestRuleResolutionFindings` (all pass, `python -m unittest tests.test_frame_prereg -v` → 90/90 ok). |
| 2 | A run whose executed procedure differs from the declared branch exits 1 at `dsx gate verify`, naming both branches in the finding text | VERIFIED | Real gate run against the committed `post-hoc-procedure-switch` fixture with a plan header seeded via the real `InvocationHeader`/`frame_digest`/`append` primitives (mirroring `tests/_trail_seed.py`): `dsx gate verify` exited **1**, sole CRITICAL finding `DSX-PRE-030`, detail: "The declared fallback rule resolves to branch 'two_proportion_z' (source: inference.fallback_rule), but the executed procedure at analysis.test is 'fishers_exact' — a different label." Both literal labels present. `tests/test_known_bad_corpus.py::test_post_hoc_procedure_switch_fixture_blocks_verify_and_ship_naming_pre_030` passes (4 subtests: verify+ship both exit 1 naming DSX-PRE-030 with both labels; plan+execute emit zero DSX-PRE- findings). |
| 3 | A procedure switched after seeing the data blocks even when the substitute is strictly more conservative — proved by fixture, not a second code | VERIFIED | Same real run: `fishers_exact` is the fixture's own documented strictly-more-conservative substitute for the declared branch `two_proportion_z` at the fixture's declared cell counts (fixture header + `post-hoc-procedure-switch-POSTMORTEM.md` argue this explicitly), and it still blocks with `DSX-PRE-030` — no `DSX-PRE-010` in the same run, confirming the rule resolved cleanly and one defect produced one code (D-07). `_check_procedure_reconciliation` reads no admissibility/power/conservatism data — only `normalize(resolution.branch) != normalize(executed)` (confirmed by direct read, `dsx/frame/prereg.py:288-352`). |
| 4 | `declared_at` is named as an unverifiable self-declaration in both the finding remedy and the README; the content lock compares recorded bytes, not the declared string | VERIFIED | Content lock: `_check_content_lock` computes `frame_digest(spec)` and tests set membership against every recorded `plan`-gate-point digest (`dsx/frame/prereg.py:540-568`) — confirmed by a real run (`dsx gate plan` then `dsx gate verify` against the same seeded root → verify emits zero `DSX-PRE-020` and exits 0; a mutated `inference:` block after `plan` would flip this, per `TestContentLockReconciliation`). "Finding remedy" half: `DSX-PRE-030`'s remedy states "'executed' is a convention imposed by this gate point, not a property of the field, the same class of limit as `declared_at`" (`dsx/frame/prereg.py:346-349`, per `10-02-PLAN.md`'s own must-have wording, matched verbatim). README half: `README.md:345-348` states "`declared_at`... is an operator self-declaration that the tool cannot verify" under `## Known limits`, confirmed by direct read and by `TestDocumentedLimits` (8 tests, all pass, `python -m unittest tests.test_frame_prereg.TestDocumentedLimits -v` → 8/8 ok). **The M-07 grandfather-route half of this criterion is what CR-01 found broken and what this re-verification spent most of its effort re-proving above — it is now real, not merely named.** |
| 5 | Every `DSX-PRE-*` check carries a primary-source citation plus a published reference value or named structural criterion; a test asserts every code is reachable from a `GATE_PROFILES` entry | VERIFIED | `python scripts/gen-finding-catalogue.py --check` exits 0, `"DSX-PRE-"` present in `_D05_ALLOWLIST_PREFIXES` (`scripts/gen-finding-catalogue.py:68`, an inclusion list — confirmed it actually inspects, not skips, this family). All three functions in `dsx/frame/prereg.py` carry `Citation:` (Gelman & Loken 2014; Simmons, Nelson & Simonsohn 2011 for `-030`) and `Structural criterion:` lines (no `Reference value:` literal anywhere in the module — grep confirmed, matching D-15's deliberate choice). `TestGateRegistration` (4 tests) run directly: `python -m unittest tests.test_frame_prereg.TestGateRegistration -v` → 4/4 ok, including `test_every_dsx_pre_code_reachable_from_a_gate_profile` (asserts `"prereg"` is in `set().union(*GATE_PROFILES.values())`) and `test_known_dsx_pre_codes_are_exactly_010_020_030`. `references/finding-codes.md:392-394` lists all three codes under `## Pre-registered inference plan`. |

**Score:** 5/5 truths verified (0 present-but-behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `dsx/frame/prereg.py` | Parser, resolver, three `DSX-PRE-*` checks, `check()` dispatcher, `_has_grandfather_suppression` | VERIFIED | 651 lines; `_parse_fallback_rule`, `_resolve_branch`, `_check_rule_resolves`, `_check_procedure_reconciliation`, `_recorded_plan_digests`, `_has_grandfather_suppression`, `_check_content_lock`, `check()` all present and read directly. |
| `dsx/spec.py::PREREG_FACTS` | Closed 3-member fact registry | VERIFIED | `{alpha: design.alpha, comparisons_looked_at: results.comparisons_looked_at, interim_looks: results.interim_looks}`; `_PREREG_FACTS_NORMALIZED` derived from it at module scope in `prereg.py`. |
| `dsx/cli.py` `GATE_PROFILES`/`CHECKS`/`run_checks` | `prereg` registered verify+ship only, root threaded, `gate_invocation` scoping | VERIFIED | Direct read: `"prereg"` present in `verify`/`ship` tuples (`dsx/cli.py:104-112`), absent from `plan`/`execute`; `run_checks`'s `elif name == "prereg":` branch threads `root` and `reconcile_trail` (`dsx/cli.py:190-192`); `prereg.check()` raises *inside* this loop, before `merge()`/`apply_suppressions()` at line 202 — confirmed this is exactly why CR-01 was a real defect and exactly why the fix had to live inside `prereg.py` itself. |
| `dsx/suppressions.py::apply_suppressions` | Bar `_has_grandfather_suppression` must match | VERIFIED | `usable` list built with `code in known`, `_CODE_RE.match(code)`, non-blank `reason`/`authority` (`dsx/suppressions.py:186-197`) — `_has_grandfather_suppression`'s bar (exact code match, non-blank reason/authority) is a strict subset check that agrees with this. |
| `references/finding-codes.md` | `DSX-PRE-010/020/030` listed under a `Pre-registered inference plan` group | VERIFIED | Lines 386-394 confirmed by grep. |
| `examples/known-bad/post-hoc-procedure-switch-{ANALYSIS-SPEC.yaml,POSTMORTEM.md}` | Committed fixture proving REQ-P10-04 by fixture | VERIFIED | Both files read in full; real gate run (this pass) confirms clear at plan/execute, block at verify/ship naming `DSX-PRE-030`. |
| `tests/_trail_seed.py::seed_plan_header` | Shared plan-header-seeding test helper | VERIFIED | Used directly (via its own underlying primitives) in this pass's manual verification runs. |
| `README.md` Known-limits subsection | States 4 limits + `PREREG_FACTS` paragraph | VERIFIED | Read in full at `README.md:338-388`; unchanged by the CR-01/WR-01 fix commits (`git log -- README.md` shows no commit after `e37db84`), and still accurate post-fix because the grandfather route it describes is now genuinely real. |
| `tests/test_frame_prereg.py::TestMissingPlanHeader` | Tests 10-14: a usable suppression unlocks; near-misses and unknown codes do not | VERIFIED | Added in `cc96644` (observed failing), made to pass in `d8ff23e`. 14/14 pass; independently re-run live against HEAD above (six scratch fixtures + one combined-with-unknown-code fixture). |
| `tests/test_frame_prereg.py::TestFactNameCaseNormalization` | 4 tests: capitalized registered facts resolve identically to lowercase | VERIFIED | Added in `406828d` (observed failing), made to pass in `d3490ee`. 4/4 pass; independently re-run live above. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| `dsx/frame/prereg.py` | `dsx/spec.py` | `PREREG_FACTS`, `get`, `as_number`, `normalize`, `is_blank`, `items` imports | WIRED | Confirmed by direct read of the import block (`items` added for `_has_grandfather_suppression`'s row iteration). |
| `dsx/frame/prereg.py` | `dsx/decisions.py` | `decisions_path`, `frame_digest`, `read_all`, `DecisionRecord` — permitted under D-03a | WIRED | Confirmed; `tests/test_frame_boundary.py::TestFrameImportBoundary` passes, `dsx.checks` never imported. |
| `dsx/cli.py::run_checks` | `dsx/frame/prereg.py::check` | Named `elif name == "prereg":` branch passing `root` and `reconcile_trail` | WIRED | Confirmed by direct read (`dsx/cli.py:190-192`). |
| `GATE_PROFILES["verify"/"ship"]` | `CHECKS["prereg"]` | Registration | WIRED | Confirmed present in both tuples, absent from `plan`/`execute`, and by real gate runs (exit 0 at plan, exit 2/1 at verify depending on trail state, this pass). |
| `dsx/frame/prereg.py::_has_grandfather_suppression` | `dsx/suppressions.py::apply_suppressions` | Matching bar; the early return lets execution continue to `apply_suppressions`'s unknown-code check | WIRED | Confirmed by direct read and by the live "valid grandfather row + unknown code" repro above: the run bypasses the missing-header raise, then aborts later inside `apply_suppressions` on the unknown code — proving both halves of the chain actually execute in sequence, not merely coexist as unit-tested units. |
| `scripts/gen-finding-catalogue.py::_D05_ALLOWLIST_PREFIXES` | `dsx/frame/prereg.py` citation docstrings | Inclusion-list D-05 enforcement | WIRED | `"DSX-PRE-"` present in the tuple; `--check` exits 0 with the family actually inspected. |

### Behavioral Spot-Checks (real gate runs against HEAD, not synthetic unit tests)

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| `python -m dsx` from repo root runs the live tree, not a stale bundled snapshot | `python -c "import dsx; print(dsx.__file__)"` | `C:\Users\Benutzer1\Dev\AI\gsd-dsx\dsx\__init__.py` | PASS |
| Unparseable arrow-bearing rule exits 2, never 0 | scratch fixture, `python -m dsx validate`/`check prereg` | `check` printed the `CheckError` text, exited **2** (`validate` alone doesn't run `prereg`, exited 0 as expected — `spec` check only) | PASS |
| Missing plan-time header, no suppression | scratch fixture, fresh dir, `dsx gate verify` | exit **2**, message names `DSX-PRE-020`, `suppressions`, `authority`, `dsx gate plan` | PASS |
| Missing plan-time header, valid `DSX-PRE-020` grandfather suppression | scratch fixture + suppression row | no exit 2; run reaches the rest of the check suite; zero `DSX-PRE-020` findings anywhere | PASS |
| Grandfather row missing `reason` / missing `authority` / naming a different code | 3 scratch fixtures | all three exit **2**, same message — none unlock the route | PASS |
| Valid grandfather row + an unrelated unknown suppression code in the same list | scratch fixture | missing-header raise bypassed; run still aborts at exit **2** later, naming the unknown code, inside `apply_suppressions` | PASS |
| `dsx gate plan` then `dsx gate verify` against the same seeded root, no suppression needed | scratch fixture | plan exit 0; verify exit 0, zero `DSX-PRE-020`/`no plan-time` output | PASS |
| Post-hoc-procedure-switch fixture blocks verify/ship naming both branches | committed fixture + seeded header | exit **1**, `DSX-PRE-030` names `two_proportion_z` and `fishers_exact` | PASS |
| Capitalized registered fact resolves identically to lowercase (WR-01) | `python -c "from dsx.frame import prereg; ..."` | `_Resolution(branch='alpha_spending_obf', reason=None, source='fallback_rule')`, zero `DSX-PRE-010` | PASS |
| `TestGateRegistration`, `TestMissingPlanHeader`, `TestFactNameCaseNormalization`, `TestDocumentedLimits` | `python -m unittest tests.test_frame_prereg -v` | 90/90 ok | PASS |
| `TestFrameImportBoundary`, `TestFrameParadigmReadBoundary` (D-11/D-03a) | `python -m unittest tests.test_frame_boundary -v` | 8/8 ok | PASS |
| `post_hoc_procedure_switch` corpus test | `python -m pytest tests/test_known_bad_corpus.py -k post_hoc_procedure_switch -q` | 1 passed, 4 subtests passed | PASS |
| Full test suite | `python -m pytest -q` | 640 passed, 1058 subtests passed | PASS |
| Project check | `sh scripts/check.sh` | `all checks passed` (pre-existing, unrelated catalogue duplicate-text warnings for `DSX-SPEC-070`/`DSX-VAL-021`/`DSX-VAL-060`/`DSX-COH-030`/`DSX-PAR-002` only, traced outside Phase 10) | PASS |
| Finding-catalogue currency + D-05 enforcement | `python scripts/gen-finding-catalogue.py --check` | exit 0 | PASS |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REQ-P10-01 | 10-01, 10-02 | Fallback rule parses to a decidable branch; unparseable rule exits 2 | SATISFIED | Real gate run (exit 2), `_resolve_branch` structural proof, `TestFallbackRuleParsing`/`TestBranchResolution`/`TestRuleResolutionFindings`/`TestFactNameCaseNormalization` all pass. |
| REQ-P10-02 | 10-03, 10-06 | `declared_at` provenance recorded and its limits documented | SATISFIED | `_check_content_lock` set-membership implementation; missing-header exit-2 grandfather route **now genuinely functional** (CR-01 fixed, independently re-proven live above); README subsection; `TestDocumentedLimits`/`TestContentLockReconciliation`/`TestMissingPlanHeader` all pass. |
| REQ-P10-03 | 10-02, 10-04, 10-05 | Executed-vs-declared mismatch blocks, naming both branches | SATISFIED | Real gate run against committed fixture (exit 1, `DSX-PRE-030`, both labels in `detail`), `TestProcedureReconciliation` pass. |
| REQ-P10-04 | 10-02, 10-05 | Switch after seeing data blocks even when the substitute is more defensible | SATISFIED | `TestNoMeritConsultation` + real gate run against the committed `fishers_exact`-for-`two_proportion_z` fixture — a strictly more conservative substitution, still blocked. |

No orphaned Phase 10 requirements — `.planning/REQUIREMENTS.md:127-130` lists exactly these four, and all
four are addressed by at least one plan's `requirements:` frontmatter. **Traceability reconciliation
confirmed correct:** commit `10c527e` (12:58:00, after both fix commits `d8ff23e` 12:47:50 and `d3490ee`
12:49:27) flips REQ-P10-01 and REQ-P10-02 from "Pending" to "Complete" in the table at
`.planning/REQUIREMENTS.md:217-220` and checks their boxes at `:127-130` — checked by direct read of the
commit diff and the current file state; both now correctly read "Complete"/`[x]` and this is consistent
with the code evidence in this report, not merely trusted from the commit message.

### Anti-Patterns Found

None. Scanned every file this phase modified or that the CR-01/WR-01 fix touched
(`dsx/frame/prereg.py`, `dsx/spec.py`, `dsx/cli.py`, `dsx/suppressions.py`,
`scripts/gen-finding-catalogue.py`, `references/finding-codes.md`, `tests/test_frame_prereg.py`,
`tests/_trail_seed.py`, `tests/test_known_bad_corpus.py`, the known-bad fixture pair, `README.md`,
`brief.md`) for `TBD`/`FIXME`/`XXX`/`TODO`/`HACK`/`PLACEHOLDER` and empty-implementation patterns. The
only regex hits are pre-existing, unrelated code: `dsx/spec.py`'s `_PLACEHOLDER_RE` (an angle-bracket
placeholder-value detector, not a debt marker) and `tests/test_known_bad_corpus.py`'s fake test fixture
codes `DSX-XXX-010`/`DSX-XXX-040` (deliberate test doubles, matched only because "XXX" appears inside a
fabricated finding code string). No genuine debt marker anywhere. No `Reference value:` literal exists
anywhere in `dsx/frame/prereg.py` (grep confirmed), matching D-15's deliberate choice.

### Design-Constraint Compliance (per verification_notes / orchestrator's established facts)

- `DSX-PRE-*` checks never read `inference.paradigm`: confirmed by direct read of `dsx/frame/prereg.py`
  (no `paradigm` token anywhere) and by `tests/test_frame_boundary.py::TestFrameParadigmReadBoundary`
  (8/8 ok, run directly this pass).
- No procedure ranking/conservatism ordering on the gate path: confirmed `_check_procedure_reconciliation`
  reads no admissibility/power/conservatism data at all — only `normalize(resolution.branch) !=
  normalize(executed)` — and REQ-P10-04 is proved entirely by fixture, never by a second finding code.
- Unparseable-rule case carries no code, exit 2 via `CheckError`: confirmed — `_parse_fallback_rule`
  raises directly, `DSX-PRE-011` never appears in that path.
- `DSX-PRE-011` deliberately unspent: confirmed — `known_codes()` for the `DSX-PRE-` prefix returns
  exactly `{DSX-PRE-010, DSX-PRE-020, DSX-PRE-030}`, and
  `TestGateRegistration::test_known_dsx_pre_codes_are_exactly_010_020_030` pins this (run directly, ok).

### Human Verification Required

None. All five ROADMAP success criteria were re-verified against real gate-command output on the
current HEAD (not against unit tests alone, and not against the superseded VERIFICATION.md's
conclusions), including live reproduction of the exact CR-01/WR-01 scenarios the review flagged and the
one scenario (grandfather row + unknown code together) that proves the fix's two moving parts
(`_has_grandfather_suppression` and `apply_suppressions`) actually chain correctly at runtime, not only
in isolation.

### Gaps Summary

No gaps found. The Critical defect (CR-01) that made the M-07 grandfather route inert is fixed and
independently re-verified live against six scratch fixtures plus the committed corpus and unit-test
suite; the fix's bar is exactly as strong as every other suppression in the codebase, so it does not
trade one honesty gap for another. The Warning (WR-01) case-sensitivity gap is fixed and independently
re-verified. All five ROADMAP success criteria are observably true in the codebase on current HEAD: the
mini-DSL resolves to a decidable branch and exits 2 (never 0) when unparseable; a real gate run against
the committed fixture blocks at exit 1 naming both the declared and executed procedure labels; the same
fixture proves the block is on branch identity alone by using a strictly more conservative substitute
that still blocks; `declared_at` is documented as an unverifiable self-declaration in both the finding
remedy and the README, the content lock compares recorded `frame_digest` bytes via set membership never
the declared string, and its missing-header grandfather bypass is now genuinely functional and
attributable; and every `DSX-PRE-*` code carries a citation, a structural criterion, and is proven
reachable from `GATE_PROFILES` by a passing test run directly during this verification. All four
REQ-P10 requirements are correctly reconciled to Complete in `.planning/REQUIREMENTS.md` by `10c527e`.

---

*Verified: 2026-08-20*
*Verifier: Claude (gsd-verifier)*
