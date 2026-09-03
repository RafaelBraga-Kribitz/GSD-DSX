# 21-REVIEW — Phase 21 code review

**Reviewer:** autonomous ceremony orchestrator (opus / high, brief §3 code-review routing).
**Date:** 2026-09-02. **Unit:** S1-4 (code review + fixes).
**Scope:** the Phase-21 execute diff `4b5c32d` (S1-3) — 8 files, +380 / −30. The only
production changes are two source files (`dsx/spec.py`, `dsx/checks/viz.py`) plus the
generated `dsx/data/input_types.json`; the rest is the new invariant test module and
planning/tracking files. Every changed source hunk and the new test module read in full.
The review targets the one risk this reconciliation actually carries — a **shape change to a
shared vocabulary object** (`BANNED_TYPES` str→dict) with a hidden second reader, and
**false-pass risk in the new invariant test** (a repo-integrity oracle that looks like a
proof but passes vacuously).

## Files reviewed

| File | Change | Verdict |
|---|---|---|
| `dsx/spec.py` | `CHART_CAPABILITIES` — 10 capability orphans homed one-family-each (interval-range +histogram/density/ecdf/strip/kde; categorical-value +diverging_bar; categorical-multi +dumbbell/bump; composition +waterfall; matrix +sankey) | PASS |
| `dsx/checks/viz.py` | `RELATIONSHIP_CHARTS` — distribution +kde/population_pyramid, comparison +butterfly; `BANNED_TYPES` str→`{reason,code,citation}`; `_check_banned` reader → `["reason"]` | PASS |
| `dsx/data/input_types.json` | regenerated from the homed `CHART_CAPABILITIES` (Pitfall 1) — IT-id admissibility path refreshed | PASS |
| `tests/test_viz_vocabulary_invariant.py` | new — REQ-P21-01 two-clause homing invariant + frozen `CAPABILITY_ONLY` allowlist + gate smokes; REQ-P21-02 refusal-record completeness | PASS (2 LOW fixes applied this unit) |

## Findings

### LOW-1 — invariant test had no non-vacuity guard on `_mark_universe()` (FIXED)

`test_every_mark_has_a_capability_home` and `test_every_mark_has_a_relationship_home_or_is_allowlisted`
both assert `universe - <home> == ∅`. An empty `universe` is trivially a subset of any home,
so if the vocabulary were ever emptied (a bad import, a renamed module) **both clauses would
pass vacuously** — only the two narrow gate smokes (histogram admitted) would catch it.
This is the exact "looks like a proof, passes vacuously" class the portfolio standard forbids.
**Fix applied this unit:** new `test_mark_universe_is_non_vacuous` asserts the universe holds
the anchor marks `{bar, line, scatter, histogram, box}` and a floor of ≥30 (live count 50) —
mirroring the anti-vacuity superset guard the v2.3 S4-4 no-autoswitch enumeration uses. Additive
assertion; no existing assertion changed.

### LOW-2 — `CAPABILITY_ONLY` allowlist could carry a phantom (non-universe) entry undetected (FIXED)

`test_capability_only_allowlist_is_exact_not_a_superset` guarded one drift direction (an
allowlist entry that secretly *has* a relationship home) but not the other: a stale or
mistyped allowlist mark that **no surface actually names** is silently subtracted from
`unhomed` and guards nothing, letting the frozen allowlist rot. **Fix applied this unit:** the
same test now also asserts `CAPABILITY_ONLY ⊆ _mark_universe()` (no phantom entries). Verified
green — all 14 allowlisted marks are genuine capability-homed members of the 50-mark universe.

## Adversarial false-pass / regression probes — all CLEARED

1. **Does the `BANNED_TYPES` str→dict change break a second reader?** No. Repo-wide grep for
   `BANNED_TYPES` returns exactly two runtime consumers, both in `dsx/checks/viz.py`: the
   membership check `if chart_type in BANNED_TYPES` (line 111 — dict membership tests keys,
   unaffected) and the detail reader (line 116, correctly updated to `["reason"]`). It is not
   vocab-dumped (`_VOCABULARIES` in `spec.py` does not include it) and no `dsx` CLI surface
   iterates its values. No other reader observes the shape change.
2. **Is the homing math exactly the plan's orphan set, no more no less?** Yes. The 10
   capability orphans `[bump, density, diverging_bar, dumbbell, ecdf, histogram, kde, sankey,
   strip, waterfall]` and the 3 relationship orphans `[butterfly, kde, population_pyramid]`
   are each homed into exactly one family; `kde` (the one double orphan) correctly appears in
   both `CHART_CAPABILITIES["interval-range"]` and `RELATIONSHIP_CHARTS["distribution"]`.
   `population_pyramid`/`butterfly` were left out of `CHART_CAPABILITIES` deliberately (already
   capability-homed via `EXTRA_MARKS[IT011]`, Pitfall 2) and only given relationship homes.
3. **Was the generated JSON actually refreshed, or just the live dict?** Refreshed.
   `test_input_type_id_path_admits_a_homed_mark` drives the IT040 path, which reads the
   generated `dsx/data/input_types.json`, and asserts histogram no longer fires DSX-VIZ-013 —
   green only if the JSON was regenerated.
4. **Could the refusal-completeness test pass with an empty/placeholder citation?** No.
   `test_every_banned_type_has_a_complete_refusal_record` asserts each of `reason`/`code`/
   `citation` is present and `.strip()`-non-empty for all five marks; the `radar` PROVISIONAL
   citation is non-empty prose flagged for HQ-27 S5-2, not a blank.
5. **Could `_check_banned` silently stop firing after the shape change?** No.
   `test_check_banned_detail_is_the_reason_string` runs `viz.check` on a `radar` spec and
   asserts exactly one DSX-VIZ-001 finding whose `detail == BANNED_TYPES["radar"]["reason"]`.

## Security / correctness

Declaration-only vocabulary edits (frozensets / dict literals) plus additive test assertions.
The new test module reads `scripts/gen-input-types.py` via `importlib.util` so its `__main__`
guard does not execute (constants only); it reads live Python dicts, not markdown, so no CRLF
concern. No data path, no user-supplied regex, no network, no package install. Clean.

## Verdict

**PASS — 2 LOW findings, both fixed this unit.** The two production hunks are a tightly-scoped,
fully test-covered vocabulary reconciliation with no hidden second reader; the invariant test
is now a genuinely self-guarding oracle (anti-vacuity floor + allowlist-phantom guard added).
Production catalogue byte-frozen at 275 (set-identity, see 21-VERIFICATION). Proceed to
verification.
