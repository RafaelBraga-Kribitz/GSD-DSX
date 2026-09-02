---
phase: 20-calibration-and-reporting-close
plan: C
wave: 1
requirements: [REQ-P20-03]
status: complete
mints_codes: 0
catalogue_total: 275
---

# 20-C SUMMARY — no-autoswitch made category-complete + fallthrough-position regression

Wave-1 structural guard (D-07 rigour tie-break). Delivers REQ-P20-03. **Zero finding
codes minted; no production file touched** — only two existing structural-guard test
modules were extended. Catalogue stays 275. Executed inline on the ceremony branch
`gsd/v2.3.0-test-catalog` by the orchestrator (never `handle_branching`).

## Task 1 — `tests/test_no_shapiro_autoswitch.py`

Added `NoAutoswitchEveryNewCategoryTest` (3 methods) that **dynamically enumerates**
every public `recommend_*` router in `dsx.checks.stats` via `dir()` + `inspect` and:

- **anti-vacuity**: the enumerated set is a superset of the eight known new-category
  routers (`recommend_association/rm/trend/resampling/posthoc/variance_role/power/
  proportion_ci`) and includes `recommend_test` — a rename cannot silently empty the proof;
- **dataless proof**: for every router except `recommend_test`, `inspect.signature`
  carries none of the banned data-then-pick parameters `{data, n, n_groups, paired,
  normal, equal_variance, n_per_group, distribution, overdispersed}` (whole-name set
  intersection) — the mechanical anti-two-stage guarantee (REQ-P18-06), now
  category-complete AND future-proof (a NEW category added without a dataless router
  turns it red automatically);
- **explicit exclusion**: `recommend_test` legitimately consumes DECLARED shape fields
  and is pinned as the one declared-shape router, covered instead by the pre-existing
  Welch-unconditional / normality-declared assertions (which remain green after the
  Phase-18/19 sections were appended to `test-selection.md` — the setUp scopes them to
  the "in order of how much they matter" section, so the appended sections do not perturb).

Enumeration confirmed = the 9 routers exactly. Module: **7 tests OK**.

## Task 2 — `tests/test_time_to_event_fallthrough.py`

Added `TimeToEventFallthroughPositionTest` (2 methods), preserving both existing legs:

- **code side**: the LAST `return _rec(` in `recommend_test`'s source names `log_rank`
  (terminal unconditional fallthrough — a new outcome branch appended after it would
  shadow `time_to_event`);
- **doc side**: the FINAL data row of the `## Decision table` has Outcome =
  `time-to-event`, proving no Phase-18/19 addition inserted a decision-table outcome row
  after it (the six new sections are separate `##` sections after the table).

Module: **4 tests OK**.

## Plan-defect caught and corrected (orchestrator, brief §5)

Both 20-C Task 2 and 20-D Tier-1 (and both plans' inline `<verify>` commands) bound the
decision-table block with `...split('[^1]',1)[0]`. **That is buggy:** `[^1]` is an
**in-cell footnote MARKER inside the proportion row** (`...expected cell < 5)[^1]` on line
10), not only the footnote *definition* (line 26). `split('[^1]',1)[0]` therefore
truncates the table at row 10 — the "15 rows" / "terminal row = time-to-event" assertions
would have **failed**, not passed. Corrected parse: bound the block at the **next `##`
heading** (`re.split(r'\r?\n##\s', after, 1)[0]`); footnote lines don't start with `|` so
they are already excluded. Verified: **15 data rows parsed, terminal outcome cell =
`time-to-event`**. The same correction must be carried into 20-D Tier-1 next firing.

## Gate (re-run by orchestrator from the working tree)

- `python -m unittest tests.test_no_shapiro_autoswitch -v` → **7 OK**;
  `tests.test_time_to_event_fallthrough -v` → **4 OK**.
- Full suite `python -m unittest discover -s tests -q` → **Ran 1447 tests OK**
  (S3-5 baseline 1442 + 5 new; the "declared twice" warnings are pre-existing legacy,
  none Phase-20; the two `explain` tests passed — no stray root `DECISIONS.jsonl`).
- `git diff --name-only` = only the two test files (production code byte-frozen);
  `gen-finding-catalogue.py --check` = "finding catalogue is current" (275, zero mints).
