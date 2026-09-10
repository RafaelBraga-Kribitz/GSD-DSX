---
phase: 26-per-skill-read-contracts
reviewed: 2026-09-07T08:48:22Z
depth: deep
files_reviewed: 6
files_reviewed_list:
  - skills/dsx-scope-analysis/SKILL.md
  - skills/dsx-define-metrics/SKILL.md
  - skills/dsx-design-experiment/SKILL.md
  - skills/dsx-build-model/SKILL.md
  - skills/dsx-narrate/SKILL.md
  - tests/test_skill_read_contracts.py
findings:
  critical: 0
  warning: 0
  info: 3
  total: 3
status: clean
---

# Phase 26: Code Review Report — Per-skill read contracts

**Reviewed:** 2026-09-07T08:48:22Z
**Depth:** deep (cross-file: skill blocks ↔ guard ↔ live templates, empirically executed)
**Files Reviewed:** 6 (the exact phase-26 diff `818fb7c..HEAD -- skills/ tests/`; `dsx/` diff confirmed empty)
**Status:** clean — 0 HIGH, 0 MEDIUM, 3 LOW (latent-robustness only, none triggered by current inputs)

## Summary

Phase 26 added one `<inputs>` read-contract block to five DSX skills and a stdlib
repo-integrity guard (`tests/test_skill_read_contracts.py`). I did not take the
GREEN claim on trust: I ran the suite (7/7 OK), dumped the parser's full key sets
(50 EDA paths, 47 profile paths), and mechanically probed the load-bearing
REQ-P26-02 property by renaming **every** skill-named template key (leaf, parent,
and the `column_name` placeholder) and confirming each rename removes the key from
the parsed set. **Every rename is caught** — there is no rename of a referenced key
that the guard would silently miss. All four hard invariants hold. No correctness,
security, or quality defect rises to WARNING or BLOCKER.

### Verification performed (not just asserted)

- **Guard executes GREEN:** `python -m unittest tests.test_skill_read_contracts -v` → 7/7 OK.
- **Every named key resolves live:** all 37 distinct skill-named keys (EDA + profile,
  across the 5 skills and the `D26_02` matrix) are members of the live parsed sets.
  Spot-checks demanded by the brief — `columns[].categorical`, `time.max_gap_days`,
  `unit.largest_unit_share`, `target.weekly_range`, `base_rate.metric`,
  `comparisons_looked_at`, `artifact_status` — all present.
- **`columns[].categorical` traced by byte:** confirmed the commented `categorical:`
  header sits at uncommented indent 6 (sibling of `numeric:`, child of `column_name`
  at indent 4), so it normalizes to `columns[].categorical`, **not**
  `columns[].numeric.categorical`. The indent-stack pop-on-`>=` and the
  "scalars are never pushed as parents" rule both behave correctly on the
  fully-commented `unit:`/`target:` blocks (they attach to root, not to the
  preceding top-level scalar `sentinels_found`).
- **Rename-catch (REQ-P26-02 core):** renaming each leaf key (`null_rate`, `dtype`,
  `verdict`, `overall`, `max_gap_days`, `weekly_range`, `rows_per_unit`, …), each
  parent (`columns`, `time`, `target`, `unit`, `grain`, `implied_dependence`,
  `dependence`, `base_rate`), and the `column_name` placeholder each yields **zero
  surviving referenced keys** → the suite would fail, exactly as REQ-P26-02 demands.
- **CRLF discipline:** EDA.md is CRLF, DATA-PROFILE.yaml is bare-LF (verified live);
  every split uses `\r?\n`. Both parse to non-degenerate sets (50 ≥ 30; profile
  non-empty and includes the uncomment-recovered `columns[].null_rate`).
- **Also-consult demotion (D-26-02):** both prose lines (`dsx-define-metrics:40`
  §1 Joins; `dsx-build-model:40` §4 Wide categoricals) carry **zero backticks**;
  "policy recommendation" and "join fan-out matrix" are prose, never bullets.
  Confirmed independently that `policy_recommendation` lives in EDA.md **body**
  (line 145), outside the front-matter fence — so had it stayed a bullet key,
  `parse_eda_keys` would (correctly) have rejected it. The demotion is load-bearing,
  not cosmetic.
- **Exactly one `<inputs>` block per skill, at the head** (immediately after
  `<objective>`, lines 20–21). Guard is stdlib-only (`re`, `unittest`, `pathlib`,
  `__future__`); **zero `dsx` import**. Skills are not mirrored inside `dsx/`
  (single copy under `skills/`), so byte-identical-`dsx/` and installer-synced
  do not conflict.

## Critical Issues

None.

## Warnings

None. Each candidate I chased collapsed under execution:

- *"Does `columns[].categorical` mis-nest under `numeric`?"* — No; byte-level indent
  check shows it is a sibling at indent 6. Parser output confirms `columns[].categorical`.
- *"Can a rename slip past the guard?"* — No; exhaustive leaf+parent+placeholder
  rename probe leaves zero surviving referenced keys.
- *"Can the profile parse vacuously (LF split under a CRLF-only pattern)?"* — No;
  split is `\r?\n`, and `test_anchor_non_vacuity` + the executed set prove it.

## Info

### IN-01: Uncomment/inline-comment stripping would corrupt a value that legitimately embeds `#`

**File:** `tests/test_skill_read_contracts.py:162,254`
**Issue:** `_INLINE_COMMENT_RE = r"\s+#.*$"` and the profile uncomment
`ln.replace("#", " ", 1)` treat `#` positionally, not YAML-aware. A future template
value such as `foo: "a # b"` or `hash: "#deadbeef"` would be truncated/mangled.
Impact is bounded because the extractor uses values **only** to test emptiness
(`value == ""` → can host children); it never records values. Corruption only
matters if it flips a non-empty value to empty (spurious parent) — not possible for
the current templates (no value embeds `#`).
**Fix:** none required now. If a template ever needs a literal `#` in a value, add a
quoted-string guard before inline-comment stripping. Documenting the assumption here
so it is a conscious constraint, not a latent surprise.

### IN-02: `_KEY_RE` silently drops hyphenated key names

**File:** `tests/test_skill_read_contracts.py:159`
**Issue:** `(?P<name>[A-Za-z_][A-Za-z0-9_]*)` accepts only underscore/alnum keys.
A future template key like `first-period-ratio` would never enter the parsed set,
so a skill referencing it would fail the membership check even though the key
exists (false-non-membership → spurious guard failure, not a silent orphan).
Current templates use underscores exclusively, so nothing is affected.
**Fix:** widen the class to include `-` only if the project adopts hyphenated YAML
keys; otherwise leave as-is (the failure mode is loud, not silent).

### IN-03: Intermediate map-header paths are accepted as members

**File:** `tests/test_skill_read_contracts.py:179-228`
**Issue:** By design the extractor records every dotted path including parents
(`grain`, `time`, `target`, `columns`, `columns[].numeric`, `target.weekly[]`, …).
A skill could therefore name a bare map header (e.g. `time`) as a "key it reads"
and pass membership, even though a map header is not a readable leaf value. This is
the only (very mild) over-acceptance surface. It is intentional — recording parents
is precisely what stops a parent rename from being masked by a same-named leaf
elsewhere (the rejected leaf-only design, D-26-04) — and **no current skill names a
bare parent**. Recording it so the trade-off is on the record.
**Fix:** none required. If desired, `test_skill_keys_are_members_of_live_templates`
could additionally assert each named key is a *leaf* (no other set member has it as
a dotted prefix), but this would add strictness the ratified matrix does not need.

---

**Verdict:** 0 HIGH / 0 MEDIUM / 3 LOW (all latent-robustness, none triggered). All
four hard invariants hold: (1) exactly one `<inputs>` block per skill, at the head;
(2) every named key resolves against the live templates and every referenced-key
rename is provably caught; (3) zero backticks on both Also-consult lines; (4) guard
is stdlib-only with zero `dsx` import. `dsx/` diff empty, catalogue 276→276, no
skill mirror inside `dsx/` to go stale.

---

_Reviewed: 2026-09-07T08:48:22Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
