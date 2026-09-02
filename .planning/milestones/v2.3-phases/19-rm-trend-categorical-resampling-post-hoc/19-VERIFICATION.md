---
phase: 19
unit: S3-4
verdict: PASSED
requirements_verified: [REQ-P19-01, REQ-P19-02, REQ-P19-03, REQ-P19-04, REQ-P19-05, REQ-P19-06, REQ-P19-07]
gate_rerun_by_orchestrator: true
full_suite: "Ran 1442 tests OK"
catalogue_total: 275
minted_codes: [DSX-STA-070, DSX-STA-080, DSX-STA-081, DSX-STA-090, DSX-STA-100, DSX-STA-110, DSX-STA-111, DSX-STA-120, DSX-STA-121, DSX-STA-122]
---

# 19-VERIFICATION — Phase 19 goal-backward verification

**Verifier:** autonomous ceremony orchestrator (opus / high, brief §3 verification routing).
**Date:** 2026-09-02. **Unit:** S3-4 (verification `passed`).
**Method:** goal-backward against REQ-P19-01..07 — for each requirement, the delivered
artifact and the gate that proves it, re-run by the orchestrator (not trusted from a
subagent report). All commands run from a clean tree (stray `DECISIONS.jsonl` cleared per
the HUMAN-QUEUE standing note). The LOW-1 fix from `19-REVIEW.md` (two dead imports removed)
is included in every rerun.

## Phase goal

Repeated-measures / trend / categorical / resampling / post-hoc surface: seven declared
sub-vocabularies read declaration-only; ten new HIGH gate codes across six requirements plus
one requirement (categorical) that correctly mints **zero**; every routing function dataless
(anti-two-stage); doc table and code in lockstep; catalogue 265→275 by set-identity.

## Requirement-by-requirement verdict

### REQ-P19-01 — RM sphericity: two-stage Mauchly blocks; unconditional GG is the route — ✅ PASS
`DSX-STA-070` fires only on the exact `mauchly_conditional` token (never on RM presence);
`recommend_rm("continuous")` returns the unconditional Greenhouse-Geisser route.
Oracle: `test_rm_sphericity_gate`, `test_declared_rm_trend_routing` — green.

### REQ-P19-02 — Trend tests need declared companions — ✅ PASS
`DSX-STA-080` on a declared `cochran_armitage` with blank `dose_scores`; `DSX-STA-081` on a
declared `mann_kendall`/`sens_slope` with blank `autocorrelation_handling` (a declared
`none`/`independent` is non-blank and SATISFIES). `trend_test` accepted as str OR list.
Oracle: `test_trend_gate` — green.

### REQ-P19-03 — Categorical mints ZERO codes — ✅ PASS
No DSX-STA-06x/… code minted; delivered as a Yates DEPRECATED row + a log-linear pointer row
+ a Fisher-Freeman-Halton footnote + a CMH surfaced-stratification row. The absent decade is
the tell. Oracle: `test_p19_categorical_rows` (rows present + total additive @275) — green.

### REQ-P19-04 — Resampling needs a complete {method, seed, B, unit} quadruple — ✅ PASS
`DSX-STA-090` fires ONCE naming the missing member(s); B's value is never checked, only its
presence; `seed: 0` is non-blank and satisfies. `recommend_resampling` house-defaults BCa for
an interval. Oracle: `test_resampling_gate`, `test_declared_resampling_posthoc_routing` — green.

### REQ-P19-05 — Declared post-hoc must match the declared omnibus family — ✅ PASS
`DSX-STA-100` on `posthoc ∉ POSTHOC_FAMILY_MAP[omnibus]`; a deprecated post-hoc (SNK) is never
a member of any acceptable set; blank omnibus/posthoc short-circuits. `recommend_posthoc`
returns exactly `POSTHOC_FAMILY_MAP[family]`. Oracle: `test_posthoc_gate` — green.

### REQ-P19-06 — Negative gates: variance-as-location-pretest; observed power — ✅ PASS
`DSX-STA-110` on a declared `variance_test` (member) with a blank or `precondition_to_location`
role — SILENT on `scale_estimand`. `DSX-STA-111` narrowly on `{observed, post_hoc}` only.
`recommend_variance_role`'s precondition disposition is "use Welch unconditionally";
`recommend_power` redirects observed/post-hoc input to the endorsed set, never echoes it.
Oracle: `test_variance_role_gate`, `test_power_reporting_gate` — green.

### REQ-P19-07 — Proportion/count declaration defects — ✅ PASS
`DSX-STA-120` on `proportion_ci_method == wald` (n-independent, no hard-coded cutoff);
`DSX-STA-121` on declared `exposure` with blank `offset`; `DSX-STA-122` on declared `nnt` with
blank `nnt_ci`. `recommend_proportion_ci` house-defaults Wilson, never Wald. Oracle:
`test_proportion_count_gate`, `test_declared_resampling_posthoc_routing` — green.

## Gates re-run by the orchestrator (clean tree)

- **Full suite:** `python3 -m unittest discover -s tests -q` → **Ran 1442 tests OK** (unchanged
  by the LOW-1 import fix; the S3-3 baseline count).
- **Catalogue:** `python3 scripts/gen-finding-catalogue.py --check` → **exit 0, "finding
  catalogue is current"** at **275** (each of the ten codes present exactly once; the 9
  `declared twice` warnings are pre-existing legacy — DSX-CLM-020/021, DSX-COH-030,
  DSX-PAR-002, DSX-SPEC-070, DSX-VAL-021/060 — **none Phase-19**).
- **Targeted Phase-19 gate + routing + categorical + invariant modules:** 77 tests **OK**.
- **Fixture discipline (canonical proof):** `test_causal_verb_golden` —
  `test_every_fixture_ship_finding_set_equals_its_golden_baseline` asserts the bad fixture's
  **ship** finding set *equals* its golden baseline, which contains all ten codes; the good
  fixture is held to its own golden (no ten). Strict set-equality at the strictest gate =
  **bad fires all ten / good silent**. `test_causal_verb_golden` + `test_known_bad_corpus` = 51 OK.
- **Exit contract:** `dsx audit` good → **exit 0**, bad → **exit 1** (blocks by design).
- **Anti-two-stage:** every `recommend_*` signature dataless (asserted per-function in the two
  routing modules) — DECLARED-fields-only invariant preserved.
- **Branch:** `gsd/v2.3.0-test-catalog` confirmed before and after.

## Verdict

**PASSED** — all seven requirements delivered goal-backward; the one LOW review finding fixed;
every verifying gate re-run green from a clean tree. Phase 19 code review + verification complete.
