# 17-VERIFICATION — Phase 17 goal-backward verification

**Verifier:** autonomous ceremony orchestrator (opus / high, brief §3 verification routing).
**Date:** 2026-09-01. **Unit:** S1-4 (verification `passed`).
**Method:** goal-backward against REQ-P17-01..05 — for each requirement, the delivered
artifact and the gate that proves it, re-run by the orchestrator (not trusted from a
subagent report). All commands run from a clean tree (stray `DECISIONS.jsonl` cleared
per the HUMAN-QUEUE standing note before running).

## Phase goal

Foundation repairs + spec vocabulary that Phases 18–20 read: reconcile the Boschloo
doc/code divergence; add the `estimand_kind` routing vocabulary; record the D-12a
disposition table and the D-06 code-range pre-allocation before any downstream code;
pin the `time_to_event` fallthrough; ship **zero** new finding codes.

## Requirement-by-requirement verdict

### REQ-P17-01 — Boschloo reconciliation — ✅ PASS
- `recommend_test` two-proportion small-expected-cell alternative emits `boschloo_exact`
  (`dsx/checks/stats.py:75`); `boschloo_exact` joined `NONPARAMETRIC_TESTS`
  (`stats.py:35`) with `fisher_exact` retained.
- Doc side already named Boschloo (`references/test-selection.md` fn.1, Lydersen–
  Fagerland–Laake 2009 §9) — divergence closed code→doc.
- Pinned regression locks doc+code: `tests/test_boschloo_reconciliation.py` **3/3 ok**
  + REQ-P11-05 baseline updated & re-pinned (`test_no_spec_..._pinned_to_recorded_baseline` ok).

### REQ-P17-02 — `estimand_kind` closed vocabulary — ✅ PASS
- 6-member closed vocab in `dsx/spec.py` (`ESTIMAND_KINDS`): linear/monotone/**nominal**/
  agreement/method_comparison/ordered_trend (the required 5 + `nominal_association`, D-01).
- Additive & absence-allowed: `templates/ANALYSIS-SPEC.yaml` gains `estimand_kind: null`;
  `is_blank` short-circuit makes absence non-blocking (D-10).
- Both canonical fixtures **extended, not replaced** (D-08): 1 line added to each of
  `examples/good-` and `examples/bad-ANALYSIS-SPEC.yaml`.
- `dsx vocab` dumps it (registered in `_VOCABULARIES` under singular key `estimand_kind`).
- `tests/test_estimand_kind_vocab.py` **6/6 ok** (six-member identity; vocab-dump lists all
  six; valid member silent; mis-slot fires exactly one loud finding; absence non-blocking;
  outcome_type membership fires without a declared test).

### REQ-P17-03 — D-12a disposition table — ✅ PASS
- Recorded in `17-CONTEXT.md` **D-02** for all nine Phase 18/19 gate checks *before*
  implementation: eight paradigm-neutral / self-scoping (ship as-is); the observed-power
  ban ships with its Bayesian sibling (post-hoc Bayes-factor "power") **named and
  D-13-deferred** — the requirement's explicitly-named condition.
- Table pre-dates all execute commits (written S1-1, committed before c2c91cd).

### REQ-P17-04 — D-06 range pre-allocation + fallthrough guard — ✅ PASS
- Live catalogue count **re-measured** (not assumed): `260` (S0-2; re-confirmed this
  firing, `grep -cE '^\| \`DSX-...\`' references/finding-codes.md` = 260).
- Ranges pre-allocated in a committed note: `17-CONTEXT.md` **D-03** — one DSX-STA decade
  per theme, **050–129**, 130s reserved.
- `time_to_event` unconditional fallthrough pinned: `tests/test_time_to_event_fallthrough.py`
  **2/2 ok** (behavioural always-routes-to-`log_rank` + source-scan: no equality guard).

### REQ-P17-05 — Zero new codes this phase — ✅ PASS
- Catalogue set-identity: `scripts/gen-finding-catalogue.py --check` = **current** (the
  set-identity gate), code count **260** = the live baseline. Asserted by diff, not review.
- DSX-STA-040 was **widened** (single call site), not multiplied; it is absent from the
  pre-existing duplicate-text warning set.

## Gate evidence (orchestrator-run, clean tree)

- `scripts/check.sh` → **all checks passed**: `Ran 1323 tests ... OK`; finding catalogue
  current; capability `dsx` v2.0.0 conformant; gate contract (good passes / bad blocks /
  missing exits 2); determinism identical.
- Targeted: `test_boschloo_reconciliation` 3/3, `test_estimand_kind_vocab` 6/6,
  `test_time_to_event_fallthrough` 2/2, REQ-P11-05 baseline 1/1 — all ok.
- Code review `17-REVIEW.md`: one LOW finding (missing `Any` import), fixed & re-gated.

## Verdict: **PASSED**

All five requirements satisfied goal-backward with re-run gate evidence. No blocker.

### Human Verification Required

End-of-phase **security sign-off** (`/gsd-secure-phase 17`) and **UAT / validation**
(`/gsd-validate-phase 17`) are S1-5, batched to HUMAN-QUEUE per the loop contract and
**non-blocking until close-out (S5-2)**. No human decision is required to consider S1-4
(review + verification) complete.
