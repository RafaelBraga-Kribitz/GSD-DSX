---
phase: 21
phase_name: "viz-vocabulary-reconciliation"
project: "gsd-dsx"
generated: "2026-09-03"
counts:
  decisions: 6
  lessons: 4
  patterns: 4
  surprises: 4
missing_artifacts:
  - "UAT.md"
---

# Phase 21 Learnings: viz-vocabulary-reconciliation

## Decisions

### D-01: two-clause invariant over a bounded universe, with a frozen CAPABILITY_ONLY allowlist
The every-mark-has-a-home invariant was scoped as two directional clauses (capability-completeness, relationship-completeness) over a precisely-bounded mark universe (`RELATIONSHIP_CHARTS ∪ CHART_CAPABILITIES ∪ EXTRA_MARKS ∪ smells sets, minus BANNED_TYPES`), rather than a naive symmetric "every mark needs both a relationship home and a capability home." Marks with no natural relationship fit (`big_number`, `candlestick`, `column_range`, etc.) are placed on a frozen, explicit `CAPABILITY_ONLY` allowlist instead of being forced into a relationship.

**Rationale:** A strict symmetric reading would have exposed ~14 capability-only marks that REQ-P21-01's enumerated 12 never named, forcing a scope expansion beyond the requirement's grant and over-widening the recommendation-surface defaults with marks that fit no relationship (e.g. `big_number`). The frozen allowlist is "provably complete" (every mark accounted for by a home or explicit exemption) without unscoped expansion, and still catches future drift (a new mark with neither a home nor an allowlist entry fails the invariant).
**Source:** 21-CONTEXT.md

### D-02: enrich BANNED_TYPES in place rather than a parallel map or a typed record
`BANNED_TYPES` was promoted in place from `dict[str, str]` to `dict[str, {reason, code, citation}]`, rejecting both a separate parallel `REFUSAL_ENTRIES` sub-map and a `NamedTuple`/dataclass record.

**Rationale:** A second map keyed on the same marks would introduce a drift surface (a mark banned-but-undocumented or documented-but-not-banned) — exactly the "silently absent" failure REQ-P21-02 exists to prevent. A single enriched registry makes completeness a structural property of one keyset. A typed record was rejected as introducing a new type on the gate path against a codebase whose vocabularies are plain dicts (house style); the nested dict matches the idiom with lower churn, with completeness enforced by the invariant test instead of the type system.
**Source:** 21-CONTEXT.md

### Corrected classification: population_pyramid and butterfly are relationship-orphans only, not "double orphans"
S0-2 had labeled `population_pyramid`/`butterfly` as orphaned in both `CHART_CAPABILITIES` and `RELATIONSHIP_CHARTS`. Under the gate-faithful capability-home definition adopted in D-01 (capability home = `CHART_CAPABILITIES` membership OR `EXTRA_MARKS` membership), both marks were already capability-homed via `EXTRA_MARKS["IT011"]`. The homing work was therefore relationship-only for these two; `CHART_CAPABILITIES` was deliberately left untouched for them.

**Rationale:** `EXTRA_MARKS` is a real capability-reachability path — it is exactly what the DSX-VIZ-013 gate check (`_check_input_type_matrix`) admits from — so widening `CHART_CAPABILITIES` for these marks would have been redundant and an over-widening of a base family the D-01 guidance explicitly warns against.
**Source:** 21-CONTEXT.md

### Narrowest single-family homing per orphan mark
Each of the 12 orphan marks was homed to exactly one family/relationship (the narrowest fit), not both a primary and an alternate family, even where a plausible alternate existed (e.g. `waterfall` → composition, not categorical-value; `bump` → categorical-multi, not time-series; `population_pyramid` → distribution, not comparison).

**Rationale:** Picking one family per mark based on its data signature avoids the over-widening failure mode (Pitfall 4) — admitting a mark into a family it doesn't semantically belong to just because it removes friction there too.
**Source:** 21-01-PLAN.md

### Radar citation shipped provisional and non-blocking rather than delaying the phase
Four of the five banned types got clean citations from the HQ-27 Tier-3 pack (Munzner ch.6 + Tufte 1983 for the 3D marks; Muth 2018 for `dual_axis_line`). `radar` had no exact pre-mapped source, so a best-fit provisional citation (Tufte/Munzner proportional-encoding doctrine) was shipped, explicitly flagged in HUMAN-QUEUE.md for operator confirmation at S5-2, rather than blocking Phase 21 on the missing sign-off.

**Rationale:** REQ-P21-02 adds no new blocking gate code — `DSX-VIZ-001` already fires and its `reason` string shipped long ago — so the citation-authenticity read is a non-blocking D-05 concern that can be batched and drained later without holding up the phase.
**Source:** 21-01-PLAN.md; 21-CONTEXT.md

### Execute inline (no subagent delegation) for this plan
The orchestrator executed all three tasks inline (opus) instead of delegating to a subagent.

**Rationale:** The plan left zero design judgment (D-01/D-02 already decided and plan-checker-verified), the orchestrator had to re-run every gate regardless per the brief, and CONTEXT.md required single-firing completion without mid-unit compaction — so tightly-scoped inline execution was judged to beat a blind-exploring subagent spawn.
**Source:** 21-01-SUMMARY.md

---

## Lessons

### An invariant asserting `universe - home == ∅` can pass vacuously
The original invariant test asserted `universe - <home-set> == ∅` for both homing clauses. If the mark universe were ever accidentally emptied (bad import, renamed module), an empty set is trivially a subset of any home, so both clauses would pass vacuously — only the two narrow gate smokes would have caught it.

**Context:** Flagged as LOW-1 in code review and fixed the same unit by adding `test_mark_universe_is_non_vacuous`, which asserts the universe contains anchor marks (`bar`, `line`, `scatter`, `histogram`, `box`) and a floor of ≥30 members (live count 50).
**Source:** 21-REVIEW.md

### A frozen allowlist needs a "no phantom entries" guard, not just a "no false entries" guard
`test_capability_only_allowlist_is_exact_not_a_superset` originally only checked that no `CAPABILITY_ONLY` entry secretly already has a relationship home. It did not check the other direction: a stale or mistyped allowlist entry that no surface actually names at all would be silently subtracted from the "unhomed" set and guard nothing, letting the frozen list rot undetected.

**Context:** Flagged as LOW-2 in code review; fixed by additionally asserting `CAPABILITY_ONLY ⊆ _mark_universe()`, confirming all 14 allowlisted marks are genuine members of the universe.
**Source:** 21-REVIEW.md

### Editing the live vocabulary dict does not update the generated gate artifact
`CHART_CAPABILITIES`/`EXTRA_MARKS` edits only fix the coarse-family admissibility path. The input-type-id path of `_check_input_type_matrix` reads the static generated `dsx/data/input_types.json`, not the live dict, so without explicitly re-running `scripts/gen-input-types.py`, that path stays stale even after the source dict is fixed and even though tests on the live objects would pass.
**Context:** Documented as Pitfall 1 in the plan and confirmed as a real, deliberate step (Task 2) rather than a theoretical concern — the plan's own gate smoke on IT040 was written specifically to catch this staleness.
**Source:** 21-01-PLAN.md

### A shape change to a shared vocabulary value needs a full second-reader sweep, not an assumption
Promoting `BANNED_TYPES` from `dict[str, str]` to `dict[str, dict]]` had exactly one call site that would break silently (the `detail=` reader) if not updated — but that could only be trusted after a repo-wide grep confirmed there were no other readers (no vocab dump, no CLI surface iterating its values).
**Context:** Reviewer explicitly ran and documented this adversarial probe (21-REVIEW.md probe 1) rather than trusting the plan's claim of "one call site" at face value; it held, but the review treated it as a thing to verify, not assume.
**Source:** 21-REVIEW.md

---

## Patterns

### Load module-level constants from a hyphenated script file via importlib, without running its main()
`scripts/gen-input-types.py` cannot be imported as `scripts.gen_input_types` (hyphenated filename, no `__init__.py`). The test loaded `EXTRA_MARKS` from it using `importlib.util.spec_from_file_location` + `exec_module`, relying on the fact that the script's module-level code only defines dicts and a `main()` function, so executing the module has no side effects.

**When to use:** Whenever a test or tool needs live constants/dicts out of a script that isn't structured as an importable package, and the module-level code is verified side-effect-free (no code runs except function/constant definitions).
**Source:** 21-01-PLAN.md; 21-01-SUMMARY.md

### Repo-integrity invariant test, off the gate path, testing data-structure properties directly
The every-mark-has-a-home and refusal-completeness invariants were implemented as a plain `unittest` module that imports and asserts against live Python vocabulary objects directly (not via CLI/gate execution), placed in `tests/` specifically because that directory is never in `dsx.cli.GATE_PROFILES`' import closure — in the same family as the existing `test_finding_catalogue_invariant.py`.

**When to use:** For proving structural completeness/consistency properties of static in-repo data structures (vocabularies, catalogues, registries) at commit/CI time, without adding runtime cost or coupling to the production gate execution path.
**Source:** 21-CONTEXT.md; 21-01-PLAN.md

### Set-identity diff against a pinned pre-change baseline commit to prove zero drift
To prove the finding-code catalogue was untouched, the sorted unique code set was extracted from `references/finding-codes.md` both at a pinned baseline commit (`4b5c32d^`, pre-Phase-21) and at HEAD, and the symmetric difference was asserted empty — a stronger and more direct proof than just re-checking a total count.

**When to use:** Whenever a change touches a shared registry/catalogue and the requirement is "prove nothing was added or removed," not just "prove the count is unchanged" (which could mask a coincidental add+remove).
**Source:** 21-VERIFICATION.md

### RED must fail for the documented reasons, not merely fail
The plan required confirming that RED-phase test failures matched specific documented expectations (exact orphan mark names, exact error types) before proceeding to GREEN, rather than accepting any non-zero exit as sufficient proof the test was meaningful.

**When to use:** In TDD workflows where an assertion could accidentally already pass (or fail for an unrelated reason), which would mask a test that isn't actually exercising the intended behavior.
**Source:** 21-01-PLAN.md

---

## Surprises

### No new EXTRA_MARKS entry was needed to home any of the 12 orphans
Despite `EXTRA_MARKS` being a real, used per-IT-id capability-reachability mechanism (and the load-bearing path for `population_pyramid`/`butterfly`), every one of the 12 orphan homings landed in an existing base `CHART_CAPABILITIES` family — none required adding a new `EXTRA_MARKS` key.
**Impact:** Simplified the implementation (Task 2 touched only base-family dict entries plus the RELATIONSHIP_CHARTS additions) and kept the blast radius smaller than the plan initially considered possible.
**Source:** 21-01-PLAN.md

### Clause 2 surfaced ~14 capability-only marks the requirement never named
Applying the relationship-completeness clause to the full mark universe (rather than just the 12 explicitly enumerated orphans) revealed roughly 14 additional marks (`column`, `grouped_bar`, `multi_line`, `bubble`, `donut`, `sunburst`, `icicle`, `circle_pack`, `timeline`, `gantt`, `big_number`, `candlestick`, `ohlc_bar`, `column_range`) that are capability-homed but have no relationship home — a scope discovery beyond what REQ-P21-01 originally scoped.
**Impact:** Forced the D-01 allowlist design (rather than a simpler "home all marks both ways" approach) and pushed the question of whether any of these should later get a relationship home to Phase 22 rather than resolving it in Phase 21.
**Source:** 21-CONTEXT.md

### The HQ-27 Tier-3 evidence pack had no exact citation for radar specifically
Of the five banned marks, four (the three 3D marks plus dual_axis_line) had clean, directly-applicable citations already prepared in the Tier-3 pack. Radar was the one type with no pre-mapped exact source, despite being no less central to the ban list.
**Impact:** Required shipping a provisional citation and adding an explicit non-blocking human-review flag (HQ-27, drained at S5-2) rather than a clean citation for all five — the one asymmetry in an otherwise uniform enrichment.
**Source:** 21-01-PLAN.md; 21-CONTEXT.md

### The full suite grew by exactly one test between inline execution and independent verification
S1-3 (inline execution) reported 1470 tests passing; S1-4 (independent orchestrator re-run verification) reported 1471. The sole delta was the single anti-vacuity test method added as the LOW-1 review fix — confirming no environmental drift (e.g. a stray root `DECISIONS.jsonl` affecting the `explain` tests) crept in between the two runs.
**Impact:** Gave the verifier confidence that the re-run gates, not the subagent's self-report, were the actual source of truth — consistent with the phase's practice of never trusting an inline/subagent report without an independent gate re-run.
**Source:** 21-VERIFICATION.md
