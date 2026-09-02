# 19-REVIEW — Phase 19 code review

**Reviewer:** autonomous ceremony orchestrator (opus / high, brief §3 code-review routing).
**Date:** 2026-09-02. **Unit:** S3-4 (code review + fixes).
**Scope:** the phase-19 source/test/doc diff `1ffb161..HEAD` (the S3-2 plan-done commit to
HEAD) — 18 files, +1619 / −24. The correctness-bearing core (`dsx/checks/stats.py` +574,
`dsx/spec.py` +88, the catalogue generator and the invariant test) read in full; the ten
gate-test modules and the doc lockstep read in full.

## Files reviewed

| File | Change | Verdict |
|---|---|---|
| `dsx/checks/stats.py` | seven dataless `recommend_*` routing fns + seven `_check_declared_*` gate helpers + `_check_declared_advanced_stats` dispatcher wired at BOTH `check()` sites; six scalar fields joined `_MEMBERSHIP_FIELDS` | PASS (1 fix applied, LOW-1 below) |
| `dsx/spec.py` | eight closed sub-vocabs + `POSTHOC_FAMILY_MAP` routing dict; `_VOCABULARIES` registration (8 sets; the map deliberately not registered) | PASS |
| `scripts/gen-finding-catalogue.py` | the ten codes added to `_D05_ALLOWLIST_CODES` **by exact name** (not via prefix) | PASS |
| `tests/test_finding_catalogue_invariant.py` | count 265→275; `_MINTED_CODES` +10; `_SNAPSHOT_TOTAL` frozen 256 | PASS |
| `references/test-selection.md` | ten gate-code rows + RM/trend/resampling/post-hoc/proportion sections + Yates DEPRECATED + log-linear pointer + FFH footnote + CMH surfaced (D-08 lockstep) | PASS |
| `references/finding-codes.md` | regen in-commit → 275 | PASS |
| `examples/bad-ANALYSIS-SPEC.yaml` | +16 lines: ten dedicated declared fields, each in-vocabulary, so only the ten intended gates fire (no DSX-STA-040 noise) | PASS |
| `tests/test_rm_sphericity_gate.py` `…_trend_gate` `…_resampling_gate` `…_posthoc_gate` `…_variance_role_gate` `…_power_reporting_gate` `…_proportion_count_gate` | new per-gate modules, codes asserted exhaustively | PASS |
| `tests/test_declared_rm_trend_routing.py` `…_declared_resampling_posthoc_routing.py` | dataless-signature (anti-two-stage) + house-default routing proofs | PASS |
| `tests/test_p19_categorical_rows.py` | REQ-P19-03 zero-mint proof (rows present + absent DSX-STA-06x decade + total stays additive) | PASS |
| `tests/test_causal_verb_golden.py` | bad-fixture golden ship set +10 (the exact ten) | PASS |

## Findings

### LOW-1 — two dead imports in `dsx/checks/stats.py` (FIXED)

`dsx/checks/stats.py` imported `DOSE_SCORE_SCHEMES` and `RESAMPLING_METHODS` from
`dsx.spec` but referenced neither in executable code:

- `DOSE_SCORE_SCHEMES` — deliberately **not** in `_MEMBERSHIP_FIELDS` (its gate trigger is
  `dose_scores` presence, not membership; documented in the code) and used by no route or
  helper → appeared on exactly one line, the import.
- `RESAMPLING_METHODS` — the `_RESAMPLING_ROUTES` table uses literal frozensets; the name
  appeared only in a comment and a docstring ("drawn from RESAMPLING_METHODS"), never as an
  evaluated binding. The route ⊆ vocab claim **is** enforced, but by a *test*
  (`test_declared_resampling_posthoc_routing.test_interval_route_draws_only_from_resampling_methods`)
  that imports the vocab from `dsx.spec` directly — not through this import.

No runtime or gate impact (Python does not error on unused imports; `scripts/check.sh` runs
no linter — unittest + catalogue `--check` + gate-contract + determinism only, which is why
S3-3's gate passed regardless). But dead imports are the mirror of the S1-4 finding (a
*missing* `Any` import) and this repo's demonstrated standard is import hygiene.

**Fix applied:** removed both imports from the `from ..spec import (...)` block. Verified the
module still imports and neither name is bound in its namespace; full suite unchanged at
**1442 OK**, catalogue `--check` exit 0 @275.

## Adversarially probed, cleared with no finding

- **`is_blank` semantics on legitimate falsy declarations.** `is_blank(0)` / `is_blank(0.0)`
  is `False` (only `None`/empty-string/empty-container are blank), so a declared
  `resampling.seed: 0`, a declared `dose_scores: 0`, or an explicit
  `autocorrelation_handling: none` are all **non-blank and SATISFY** — DSX-STA-081/090 do
  not false-fire on a legitimate explicit declaration. Confirmed against the trend and
  resampling gates.
- **Crash-safety on wrong-typed declarations.** `normalize()` does `str(value)` first, so a
  non-string `sphericity_correction`/`omnibus`/etc. yields a token (out-of-vocab → recognised
  loudly), never an `AttributeError`. `_check_declared_resampling` guards
  `isinstance(resampling, dict)`; `_check_declared_trend` handles str-OR-list-OR-other
  (`isinstance(raw,(list,tuple,set))` then the `is_blank` scalar branch), so a dict/other
  `trend_test` yields a harmless non-matching token. No crash path found.
- **Anti-two-stage invariant (DECLARED-only).** Every `recommend_*` signature is dataless —
  `inspect.signature` free of any data/n/distribution parameter (the routing test modules
  assert this per-function). Every `_check_declared_*` predicate compares declared
  strings/structures against a closed vocabulary or a presence check; none reads a datum.
- **Over-block guards honoured (D-06).** DSX-STA-070 keys on the exact `mauchly_conditional`
  token, never on the mere presence of a repeated-measures design; DSX-STA-110 keys on the
  declared `variance_test_role` (silent on `scale_estimand`), never on Levene/BF presence
  alone; DSX-STA-111 fires narrowly on `{observed, post_hoc}` only; DSX-STA-090 fires ONCE
  naming the missing quadruple member(s), never four codes and never a check of B's value.
- **`_MEMBERSHIP_FIELDS` × gate interaction (no double-report).** The six scalar fields are
  registered so a *mis-slotted* value is loud via DSX-STA-040; an *in-vocabulary but
  discouraged* value (`mauchly_conditional`, `wald`, `observed`) is a valid member → 040 is
  silent and only the intended gate fires. One code per defect, confirmed on the bad fixture.

## Scoping observation (not a defect — recorded, no fix)

**DSX-STA-100 fires when a declared `omnibus` is not a `POSTHOC_FAMILY_MAP` key** (an
unrecognised omnibus → empty acceptable set → any declared post-hoc "not matched"). This is
by design under the declaration-completeness doctrine: an omnibus+post-hoc pair the catalogue
cannot recognise cannot be validated as matched, and blocking is the safe direction for a
portfolio artifact. `omnibus` is intentionally not in `_MEMBERSHIP_FIELDS`, so the four
covered families (`welch_anova`/`anova`/`kruskal_wallis`/`friedman`) are the recognised set;
broadening the family map is a future-phase decision, not a Phase-19 defect. The **good
fixture does not false-fire** (its ship set equals its own golden), so there is no
regression. Left as-is per "prefer the smaller, provable claim."

## Security

Declaration-only: string comparison, `dict.get`, `isinstance`, closed-vocabulary membership.
No data path, no user-supplied regex, no file/network I/O, no eval. Clean.
