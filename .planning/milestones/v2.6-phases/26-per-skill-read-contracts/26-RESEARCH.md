# Phase 26: Per-skill read contracts - Research

**Researched:** 2026-09-07
**Domain:** Repo-integrity documentation engineering — five skill-prompt edits + one
off-gate-path static-parsing test. NOT an analytical/ANALYSIS-SPEC phase: there is no
dataset, no metric, no decision rule. This research verifies FEASIBILITY of the
already-settled 26-CONTEXT.md design against the live tree; it does not re-derive the
design.
**Confidence:** HIGH — every claim below was checked against the live file, not
recalled from training data or from CONTEXT.md's prose alone.

## Summary

26-CONTEXT.md's design (D-26-01..04) is grounded and executable as written, with one
correction to its own stated rationale (see "Correction to CONTEXT's premise" below)
that does not change its conclusion. All keys named in the D-26-02 per-skill mapping
resolve against the live `templates/EDA.md` and `templates/DATA-PROFILE.yaml` — zero
orphaned keys found. All five skills currently open `<objective>…</objective>` with
zero existing read step, confirming S0-2 premise 4 live. The
`capabilities/dsx/fragments/executor.md` three-tier fallback wording lives at L10-17
of the current file (CONTEXT cites L16-17; the file has grown since that citation was
written — content and wording match, only the line numbers moved). `node install.mjs`
re-syncs `skills/` into the runtime overlay; `node install.mjs --check` verifies
presence + self-test but does NOT diff file content, so the phase-end command must be
`node install.mjs && node install.mjs --check` (Phase 25's own precedent), not
`--check` alone. `tests/test_gate_path_hermetic.py` walks an import closure that
starts only from `dsx.cli.GATE_PROFILES`-resolved `dsx/checks/*.py` and `dsx/frame/*.py`
files — `tests/test_skill_read_contracts.py` is structurally outside that closure by
construction (nothing in `dsx/` ever imports from `tests/`), so it cannot trip the
invariant regardless of what it imports; D-26-04's "zero imports from dsx/" is a
stricter-than-necessary but harmless additional safety margin, not a requirement of
the hermeticity test itself.

**Primary recommendation:** Implement D-26-01..04 exactly as written in 26-CONTEXT.md.
The one correction below (PyYAML actually parses these templates; the
uncomment-preprocessing step is still mandatory for a different, verified reason) should
change the *justification comment* the plan writes into the new test's docstring, not
the design.

**Correction to CONTEXT's premise (verified live, does not change the design):**
CONTEXT.md says "no PyYAML — the templates carry placeholders like `<int>` and
`MCAR | MAR | …` that will not load." This was tested live and is **false as stated**:
`yaml.safe_load()` parses `templates/EDA.md`'s front-matter cleanly (placeholders like
`<int>`, `<float | null>`, and pipe-delimited enums like `MCAR | MAR | MNAR |
not_assessed` are all valid YAML plain scalars — nothing about them breaks the
parser) `[VERIFIED: live python -m yaml.safe_load on templates/EDA.md, this session]`.
`templates/DATA-PROFILE.yaml` also parses cleanly as YAML. **The real reason a
straight-PyYAML approach fails is different and stronger than "won't load":** every
per-column and flag-gated key the skills need (`columns[].null_rate`, `unit.*`,
`target.*`, etc.) lives behind a leading `#` — a YAML *comment* — and every conformant
parser (PyYAML, the stdlib, `dsx/loader.py`'s own bundled fallback) discards comments
by design. `yaml.safe_load()` on the live file returns `"columns": null` and no
`unit`/`target` keys at all, because those blocks are 100% commented out
`[VERIFIED: live python -m yaml.safe_load on templates/DATA-PROFILE.yaml, this
session]`. So the uncomment-preprocessor is mandatory regardless of which parser
follows it — this part of D-26-04 is correct, just for the "comments are invisible to
any parser" reason, not the "won't load" reason.

**A second, independent reason not to `import yaml` in the new test:** PyYAML is an
*optional* dependency in this repo's own established pattern —
`dsx/loader.py` (L20-23) wraps `import yaml` in a `try/except`, falling back to a
bundled stdlib-only parser when PyYAML is absent, specifically because "a blocking
gate must never fail because of a missing dependency" `[VERIFIED: dsx/loader.py L1-23,
read this session]`. `tests/test_families_yaml.py` reuses that same dual-path loader
rather than importing `yaml` directly. A new test that does `import yaml` unconditionally
would introduce the repo's first hard (non-optional) third-party test dependency and
would be the first test to defect from the loader's own optional-PyYAML precedent — an
avoidable regression. Reusing `dsx.loader` itself is not an option either, because
D-26-04 requires zero imports from `dsx/`. **Conclusion: write the stdlib-only,
line-oriented indent-stack parser exactly as D-26-04 specifies — for the "comments are
invisible" and "no new hard dependency" reasons, not the inaccurate "won't load" one.**
This is a one-sentence rationale fix for the new test's module docstring, not a design
change.

## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| REQ-P26-01 | Each of the five skills gains one named-input read step at its head naming EDA/profile keys, what each changes, and the absent-artifact fallback, mirroring the executor fragment | Verified insertion points (exact tag sequences, quoted below) for all five skills; verified zero existing read step in each; verified the exact executor-fragment wording to mirror (L10-17) |
| REQ-P26-02 | An off-gate-path repo-integrity test asserts every named EDA/profile key exists in the live templates (CRLF-tolerant) | Verified every key in D-26-02's table resolves against the live templates (table below); verified `templates/EDA.md` is CRLF and `templates/DATA-PROFILE.yaml` is bare-LF — the `\r?\n` split handles both, but this is a live fact worth pinning, not an assumption; verified the exact indentation math the uncomment-preprocessor must reproduce |
| REQ-P26-03 | `dsx/` byte-identical, zero new codes, installer re-synced and `--check` passes | Verified `git status --porcelain -- dsx/` is empty at research time (clean baseline to diff against); verified `node install.mjs`'s copy mechanics and `--check`'s presence-only (not content) semantics — confirming the correct phase-end command is `node install.mjs && node install.mjs --check`; verified `scripts/gen-finding-catalogue.py --check` exits 0 today and `tests/test_finding_catalogue_invariant.py`'s `_EXPECTED_TOTAL = 276` is the live re-measure mechanism |

## Architectural Responsibility Map

This phase has no application runtime tiers (browser/server/API/DB) — it edits agent
prompts and adds a static-analysis test. Mapped onto the nearest equivalent tiers in
this project's own architecture:

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Named-input read step (what a skill reads, what it changes) | Skill prompt (`skills/*/SKILL.md`) | — | Prompt-level contract; the agent reading the skill is the "runtime" that consumes it. No code executes this — it is instruction text an LLM agent follows. |
| Key-existence guard (renamed key fails loudly) | Test / CI layer (`tests/test_skill_read_contracts.py`, off gate path) | Repo-integrity layer generally (precedent: `tests/test_selection_heuristic_docs.py`, `tests/test_phase14_onboarding.py`) | Structural regression guard over prose+template agreement, not a runtime gate — it never participates in `dsx gate <point>`. |
| Fallback wording (`eda_artifact: none`) | Skill prompt, mirroring `capabilities/dsx/fragments/executor.md` | Executor fragment (source of truth for the ladder) | The executor fragment already states this rule for the general analytical loop; the five skills each restate the SAME three-tier ladder scoped to their own outputs — no new tier, no new mechanism. |
| Installed-copy sync | Installer (`install.mjs`) | Runtime overlay (`~/.gsd/capabilities/dsx`, or `.claude/` when `--local`) | Existing mechanism, unchanged this phase — re-run only, not modified. |

## Standard Stack

No new libraries. The phase adds one `unittest`-based test module using only stdlib
(`pathlib`, `re`, `unittest`) — matching every existing repo-integrity test's pattern
(`tests/test_phase14_onboarding.py`, `tests/test_selection_heuristic_docs.py`,
`tests/test_gate_path_hermetic.py` all use only `pathlib`/`re`/`unittest`/`ast`, no
third-party imports for their own document-parsing logic).

**Do not `import yaml`.** See "Correction to CONTEXT's premise" above — PyYAML is an
optional dependency in this repo's own established pattern (`dsx/loader.py`), and even
if imported it would not solve the actual problem (comments are invisible to every
YAML parser, PyYAML included). The line-oriented indent-stack parser D-26-04 specifies
is the correct approach for a different, stronger reason than CONTEXT states.

**Installation:** none — no new packages.

## Package Legitimacy Audit

Not applicable — this phase installs zero external packages (skill-doc edits + one
stdlib-only test file). Section omitted per the protocol's own conditional trigger.

## Architecture Patterns

### System Architecture Diagram

```
Agent invokes a skill (e.g. dsx-scope-analysis)
        |
        v
[SKILL.md <objective>] -> [SKILL.md <inputs>]  <-- NEW: read step, this phase
        |                        |
        |                        v
        |                 Agent reads, if present:
        |                 - EDA.md front-matter (phase directory)
        |                 - DATA-PROFILE.yaml (fallback source)
        |                        |
        |            EDA.md absent? --------------> record eda_artifact: none
        |                        |                          |
        |                        v                          v
        |              named keys inform the skill's   source facts from
        |              output (e.g. grain.verdict ->    DATA-PROFILE.yaml,
        |              validity-frame units)             else declare with
        |                        |                        computed_by honesty
        |                        v                          |
        +----------------> [SKILL.md process/design_mode/order_of_operations/
                             definition_contract/structure] (unchanged, existing)
                                        |
                                        v
                             skill's normal output (ANALYSIS-SPEC.yaml /
                             metric def / experiment design / model spec /
                             narrative) -- now grounded in measured evidence

Separately, off the execution path entirely:

[tests/test_skill_read_contracts.py]  (unittest, run by scripts/check.sh)
        |
        v
Parse each of the 5 SKILL.md files' <inputs>...</inputs> block
        |
        v
Parse templates/EDA.md front-matter + templates/DATA-PROFILE.yaml
(uncommenting # example lines first) into the live dotted-path key sets
        |
        v
Assert every key a skill's <inputs> block names is a member of the
matching live key set -- FAIL LOUDLY (named skill + region + key) if not
        |
        v
Negative control: feed a fabricated key through the same matcher,
assert it is rejected -- proves the assertion actually discriminates
```

### Recommended Project Structure

No new directories. Edits land in-place:

```
skills/
├── dsx-scope-analysis/SKILL.md      # <inputs> inserted after </objective>
├── dsx-define-metrics/SKILL.md      # <inputs> inserted after </objective>
├── dsx-design-experiment/SKILL.md   # <inputs> inserted after </objective>
├── dsx-build-model/SKILL.md         # <inputs> inserted after </objective>
└── dsx-narrate/SKILL.md             # <inputs> inserted after </objective>, before <precondition>
tests/
└── test_skill_read_contracts.py     # NEW — off gate path, zero dsx/ imports
```

### Pattern 1: The `<inputs>` block (D-26-01, verified against live skill heads)

**What:** A literal `<inputs>…</inputs>` block, one per skill, placed immediately
after `</objective>` (before `<precondition>` specifically for `dsx-narrate`).

**Verified insertion points — exact current tag sequences (all five confirmed to have
ZERO existing read step; S0-2 premise 4 holds live):**

```
dsx-scope-analysis/SKILL.md (lines 16-21 today):
<objective>
Produce `ANALYSIS-SPEC.yaml` — the contract every later gate reads. Nothing else
in the analytical loop is checkable until this exists.
</objective>

<process>
   -> insert <inputs>...</inputs> between </objective> and <process>

dsx-define-metrics/SKILL.md (lines 15-20 today):
<objective>
A metric definition precise enough that two people implementing it independently
produce the same number.
</objective>

<definition_contract>
   -> insert <inputs>...</inputs> between </objective> and <definition_contract>

dsx-design-experiment/SKILL.md (lines 16-21 today):
<objective>
Design mode: a fully specified experiment whose sample size is derived, not
guessed. Readout mode: an honest reading of one that has run.
</objective>

<design_mode>
   -> insert <inputs>...</inputs> between </objective> and <design_mode>

dsx-build-model/SKILL.md (lines 15-20 today):
<objective>
A model whose offline score predicts its production score. Everything below
exists to close the gap between those two numbers.
</objective>

<order_of_operations>
   -> insert <inputs>...</inputs> between </objective> and <order_of_operations>

dsx-narrate/SKILL.md (lines 16-21 today):
<objective>
The version the decision-maker reads, in which every sentence still survives the
audit.
</objective>

<precondition>
   -> insert <inputs>...</inputs> between </objective> and <precondition>
   (matches D-26-01's explicit narrate exception)
```

All five files check out CRLF on this machine (`skills/dsx-scope-analysis/SKILL.md`:
109 CRLF / 0 bare-LF; same pattern confirmed for the other four)
`[VERIFIED: live byte scan, this session]` — consistent with repo CLAUDE.md's
"this repo checks out CRLF on Windows" rule and with `templates/EDA.md` (206 CRLF / 0
bare-LF). **`templates/DATA-PROFILE.yaml` is the outlier: 0 CRLF / 72 bare-LF**
`[VERIFIED: live byte scan, this session]` — the two templates the guard reads do NOT
share one line-ending convention. This is exactly why the guard must split on `\r?\n`
(which matches both CRLF and bare LF) rather than assume one convention repo-wide; a
`\n`-only split still works on both files by coincidence (an LF always precedes the
match), but a hypothetical `\r\n`-only split would silently fail to find any line
break in `templates/DATA-PROFILE.yaml`. Use `\r?\n` as CONTEXT already specifies —
this finding just makes the reason concrete rather than a generic CRLF-discipline
reminder.

**Skeleton (from D-26-01, unchanged — reproduced here so the plan doesn't need to
re-open CONTEXT.md for it):**
```
<inputs>
**Read `EDA.md` front-matter first when it exists** in the phase directory —
{one clause on why this skill starts from measured evidence, not assumption}.

EDA front-matter keys read:
- `grain.verdict`
- `base_rate.verdict`

DATA-PROFILE keys read (the fallback source when EDA is absent):
- `primary_key_unique`
- `duplicate_rate`

These set: {what each key changes in this skill's output — prose}.
Also consult (EDA prose, not front-matter): §1 Joins — {plain text, no backticks}.
When absent: no `EDA.md` → record `eda_artifact: none` and {per-skill fallback}.
</inputs>
```

### Pattern 2: The guard's key-set builder (D-26-04, grounded against live templates)

**Verified: every key named in D-26-02's mapping resolves against the live
templates.** Full table, produced this session by reading both template files in
full and checking each named key by hand against the file content:

| Skill | Key (as named in D-26-02) | Source template | Live? | Notes |
|---|---|---|---|---|
| scope-analysis | `grain.verdict` | EDA.md | ✅ live | `grain: verdict: match \| mismatch \| undeclared` |
| scope-analysis | `grain.implied_dependence.structure` | EDA.md | ✅ live | nested under `grain.implied_dependence` |
| scope-analysis | `grain.implied_dependence.cluster_var` | EDA.md | ✅ live | same block |
| scope-analysis | `missingness[]` | EDA.md | ✅ live | top-level list-of-maps; bare `[]` (no leaf) reads the whole array |
| scope-analysis | `base_rate.verdict` | EDA.md | ✅ live | `base_rate: verdict: stable \| drifting` |
| scope-analysis | `contradictions` | EDA.md | ✅ live | top-level `contradictions: []` — **no `[]` suffix** per D-26-02's own correction (it's a scalar-list key referenced bare, matching `primary_key`'s convention below) |
| scope-analysis | `stop_triggered` | EDA.md | ✅ live | top-level |
| scope-analysis | `primary_key_unique` | DATA-PROFILE.yaml | ✅ live (uncommented top-level) | `primary_key_unique: true` |
| scope-analysis | `duplicate_rate` | DATA-PROFILE.yaml | ✅ live (uncommented top-level) | `duplicate_rate: 0.0` |
| scope-analysis | `unit.rows_per_unit` | DATA-PROFILE.yaml | ✅ **commented example**, needs uncomment | `# unit:\n#   rows_per_unit: {...}` |
| scope-analysis | `unit.largest_unit_share` | DATA-PROFILE.yaml | ✅ commented example | same `# unit:` block |
| scope-analysis | `columns[].null_rate` | DATA-PROFILE.yaml | ✅ commented example | `# column_name:\n#   null_rate: 0.0` — placeholder token literally `column_name` |
| scope-analysis | `target.verdict` | DATA-PROFILE.yaml | ✅ commented example | `# target:\n#   verdict: stable` (line also carries a **trailing inline comment** — see Pitfall 2) |
| define-metrics | `grain.declared`, `.observed`, `.verdict`, `.duplicate_rate` | EDA.md | ✅ all live | `grain:` block, four direct leaves |
| define-metrics | `primary_key` | DATA-PROFILE.yaml | ✅ live top-level | `primary_key: []` — scalar-list, bare (no `[]`) |
| define-metrics | `primary_key_unique`, `duplicate_rate` | DATA-PROFILE.yaml | ✅ live top-level | as above |
| define-metrics | `columns[].n_unique`, `columns[].dtype` | DATA-PROFILE.yaml | ✅ commented example | same `# column_name:` block |
| design-experiment | `dependence.icc`, `.outcome_sd`, `.weekly_cycle_amplitude` | EDA.md | ✅ live | `dependence:` block |
| design-experiment | `base_rate.overall` | EDA.md | ✅ live | |
| design-experiment | `grain.implied_dependence.structure`, `.cluster_var` | EDA.md | ✅ live | shared with scope-analysis |
| design-experiment | `target.overall`, `target.weekly_range` | DATA-PROFILE.yaml | ✅ commented example | `# target:` block |
| design-experiment | `unit.rows_per_unit`, `unit.largest_unit_share` | DATA-PROFILE.yaml | ✅ commented example | shared with scope-analysis |
| build-model | `leakage_suspects[]` | EDA.md | ✅ live | top-level list-of-maps |
| build-model | `grain.implied_dependence.structure`, `.cluster_var` | EDA.md | ✅ live | shared |
| build-model | `segments_candidates[]` | EDA.md | ✅ live | top-level list-of-maps |
| build-model | `columns[].n_unique`, `.dtype` | DATA-PROFILE.yaml | ✅ commented example | shared with define-metrics |
| build-model | `columns[].categorical` | DATA-PROFILE.yaml | ✅ commented example | **intermediate node, not a leaf** — the `categorical:` sub-map header itself, one level under `columns.column_name`; resolves ONLY if the parser records every intermediate dotted path, not just leaves (D-26-04 already requires this) |
| build-model | `unit.rows_per_unit` | DATA-PROFILE.yaml | ✅ commented example | shared |
| build-model | `time.column`, `time.max_gap_days` | DATA-PROFILE.yaml | ✅ **live top-level**, no uncomment needed | `time:\n  column: null\n  ...\n  max_gap_days: null` are NOT commented — only the additive `rows_per_day`/`first_period_ratio`/`last_period_ratio`/`share_at_hour_00` siblings are |
| narrate | `dataset` | EDA.md | ✅ live top-level | |
| narrate | `base_rate.overall`, `.metric` | EDA.md | ✅ live | |
| narrate | `segments_candidates[]` | EDA.md | ✅ live | shared with build-model |
| narrate | `comparisons_looked_at`, `artifact_status` | EDA.md | ✅ live top-level | |
| narrate | `row_count` | DATA-PROFILE.yaml | ✅ live top-level | not commented |
| narrate | `time.min`, `time.max` | DATA-PROFILE.yaml | ✅ **live top-level**, no uncomment needed | same `time:` block as build-model's `time.column` |
| narrate | `target.overall` | DATA-PROFILE.yaml | ✅ commented example | shared with design-experiment |

**Zero orphaned keys found.** No key in D-26-02's table failed to resolve against the
live templates — the mapping needs no trimming for correctness (D-26-02 already
permits trimming for skill-relevance reasons, which is a plan-time editorial choice,
not a grounding fix).

**Also-consult prose references — verified not present as front-matter keys (grounding
problems #1/#2 CONTEXT.md already resolved, re-confirmed here):** `templates/EDA.md`'s
`## 1. Shape and identity` → `### Joins` section (line 102-105) is prose only — no
front-matter key named `joins`. `## 4. Distributions` → `### Wide categoricals`
(line 143-145) carries `policy_recommendation` only as prose in the section body, not
in the front-matter block (lines 16-80). Confirmed: naming either as a backticked key
would be a REQ-P26-02 guard failure, exactly as D-26-02 already states.

### Uncomment-preprocessor indentation math (grounded, not assumed)

D-26-04 specifies `raw.replace("#", " ", 1)` (replace the first `#` with one space,
preserving column position/length). Traced by hand against the live file's actual
bytes to confirm the resulting indent hierarchy is coherent:

```
Raw line 19:  columns:                          (indent 0)
Raw line 20:    # column_name:                  (2 spaces, '#', 1 space, text)
Raw line 21:    #   null_rate: 0.0               (2 spaces, '#', 3 spaces, text)
```

After `#`→` ` replace (length-preserving):
```
columns:                    (indent 0)
    column_name:            (indent 4 — the space that replaced '#', plus the
                              original 2 leading spaces, plus the 1 space already
                              after '#', = 4 total spaces before "column_name:")
      null_rate: 0.0         (indent 6 — same math, one level deeper)
```

This produces a coherent 2-space-per-level indent stack: `columns`(0) >
`column_name`(4) > `null_rate`(6), which normalizes correctly to
`columns[].null_rate` under the `column_name → []` rule. Spot-checked against a
second, structurally different block (`# target:` / `#   verdict: stable  # stable |
drifting | null...`) with the same result. **The single per-element placeholder token
DATA-PROFILE.yaml uses today is literally `column_name`** (residual #5's ask) —
confirmed live, not inferred: `templates/DATA-PROFILE.yaml` line 20 reads exactly
`  # column_name:`.

### Anti-Patterns to Avoid

- **Leaf-only key matching.** D-26-04 already rejects this (a `base_rate:`→`baseline:`
  rename would leave a bare `overall` leaf matchable against an unrelated `overall`
  elsewhere in the tree and silently pass). Confirmed both templates DO contain
  leaf-name collisions across blocks that would make leaf-only matching genuinely
  unsafe here: `overall` appears under both `base_rate` and (commented) `target`;
  `verdict` appears under `grain`, `base_rate`, `branch`, `time.tz_verdicts[]`, and
  (commented) `target` — five distinct `verdict` leaves. Full dotted-path matching is
  not just theoretically safer, it is empirically necessary for this exact template
  pair.
- **`import yaml` (or any third-party parser) in the new test.** See "Correction to
  CONTEXT's premise" above.
- **Matching on live-YAML-only scan** (i.e., skipping the uncomment step). Would
  false-fail every `unit.*`, `target.*`, and `columns[].*` key any of the five skills
  name — that is 8 of the ~30 D-26-02 key rows, spanning all five skills. This is
  residual #1 from CONTEXT.md; confirmed here as a real, not hypothetical, failure
  mode against the live file.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| General-purpose YAML parsing | A full YAML-1.1/1.2-compliant parser | Nothing — the guard only ever needs a **key-path extractor**, not a value parser. Reuse the narrow "indent-stack + inline-flow-awareness" logic D-26-04 already specifies, scoped to path extraction only (no type coercion, no anchors/aliases, no multi-document support) | The templates are not general YAML anyway (placeholder scalars, mixed comment/live sections) — a general parser solves a problem this guard doesn't have, and (per PyYAML's optional-dependency status in this repo) would introduce a new hard test dependency for no benefit |

**Key insight:** the temptation here is to reach for PyYAML because it happens to
parse these files without error — but "parses without error" and "recovers the
commented example keys the skills actually need" are different problems, and PyYAML
solves only the first one. The narrow, purpose-built parser D-26-04 specifies is the
correct level of hand-rolling: small, scoped to exactly what REQ-P26-02 requires, and
it avoids the dependency question entirely.

## Common Pitfalls

### Pitfall 1: Trailing inline comments on already-commented example lines

**What goes wrong:** Some commented example lines in `templates/DATA-PROFILE.yaml`
carry a SECOND `#`-delimited comment after the value, e.g. (live, line 72):
```
#   verdict: stable        # stable | drifting | null (null when < 2 populated weeks)
```
and (live, line 56-57):
```
#   first_period_ratio: null   # ISO-week edge ratio; null when < 5 populated weeks
#   last_period_ratio: null    # ISO-week edge ratio; null when < 5 populated weeks
```
**Why it happens:** the template author documents the semantics of an example value
inline, using the same `#` convention the outer comment-out uses.

**How to avoid:** the preprocessor must (1) replace only the FIRST `#` on the line
(the one that comments out the whole line) with a space, per D-26-04's
`raw.replace("#", " ", 1)`, then (2) separately strip any remaining trailing `# …`
from the now-uncommented value (D-26-04 already calls for this: "then drop trailing
inline comments"). Doing step 2 before step 1, or doing only step 1, will either
corrupt the key/value split or leave the trailing-comment stripping unimplemented.
This is not a hypothetical edge case — it hits 3 of the live commented example lines
this session's read touched (`verdict`, `first_period_ratio`, `last_period_ratio`),
and `first_period_ratio`/`last_period_ratio` sit directly adjacent to keys the D-26-02
table does NOT name (a reminder that the parser must handle these lines gracefully
even when their resulting path is never asserted against).

**Warning signs:** a test that passes on the D-26-02-named keys but would silently
mis-key `target.verdict`'s VALUE as containing `#` — since D-26-04 only extracts key
paths (never values) this specific mis-key risk doesn't surface as a false pass, but a
future extension that DOES read values would hit it immediately.

### Pitfall 2: Mixed line-ending conventions between the two live templates

**What goes wrong:** assuming both templates the guard reads share one line-ending
convention (the repo CLAUDE.md's general CRLF rule) and hand-writing a `\r\n`-only
split.

**Why it happens:** `templates/EDA.md` genuinely IS CRLF (206/206 lines), matching the
general repo convention and its own file-header comment ("this repo checks out CRLF
on Windows... use `\r?\n`, never a bare `\n`"). `templates/DATA-PROFILE.yaml` is the
exception — 0 CRLF, 72 bare-LF, verified live this session.

**How to avoid:** use `\r?\n` (or `text.splitlines()`, which handles both
transparently) for every line-oriented operation across BOTH templates, exactly as
D-26-01's parse contract already specifies for the `<inputs>` block regex. Do not
special-case one template's line endings.

**Warning signs:** a parser that silently returns zero lines (not an error) for
`templates/DATA-PROFILE.yaml` if it naively splits on `\r\n` only — the failure mode
is a vacuous pass (empty key set), not a crash, which is exactly the class of bug
D-26-04's own anchor non-vacuity pin (`len(eda) >= 30`) is designed to catch. Verify
the DATA-PROFILE side has an equivalent non-vacuity assertion, not just the EDA side.

### Pitfall 3: `--check` alone does not prove installed skill content is current

**What goes wrong:** running only `node install.mjs --check` at phase end and treating
a pass as proof the installed `dsx-scope-analysis`/etc. skill copies now carry the new
`<inputs>` block.

**Why it happens:** `check()` in `install.mjs` (L280-313) only verifies (a) each
manifest-declared skill DIRECTORY exists under the runtime home (existence check via
`fs.existsSync`, not a content diff) and (b) the self-test (four gate points against
the good/bad example specs) passes. Neither check reads the skill file's text content.
A stale installed copy with the OLD (pre-edit) `SKILL.md` would still pass `--check`.

**How to avoid:** run `node install.mjs && node install.mjs --check` — the first
command actually re-copies `skills/` into the runtime overlay (`install()`, L176-193);
the second only verifies presence + self-test after the copy. This is the exact
pattern Phase 25 used (`25-04-PLAN.md` line 144, `25-04-SUMMARY.md` line 71) and
confirmed working then (7 payload entries, 14 skills, self-test passed).

**Warning signs:** none externally visible — `--check` alone will report success even
against a stale install. The only guard is doing the re-sync step, not skipping to
the verification step.

## Code Examples

### The executor-fragment three-tier honesty ladder to mirror (D-26-03)

```
Source: capabilities/dsx/fragments/executor.md, current file lines 10-17
(CONTEXT.md cites L16-17; the file has since grown other bullets above this one —
content and wording are unchanged, only the line numbers shifted)

- **Read `EDA.md` front-matter first when it exists** in the phase directory: it
  carries the measured grain, missingness mechanisms, leakage suspects, base-rate
  verdict and segment candidates this phase already established, and its
  `comparisons_looked_at` seeds `results.comparisons_looked_at` (add confirmatory
  looks to that count; never reset it). `stop_triggered: true` means the data
  contradicted the spec — resolve the listed `contradictions` before computing.
  No `EDA.md` → record `eda_artifact: none` and source those facts from
  `DATA-PROFILE.yaml` or declare them with `computed_by` honesty.
```

Three tiers, in order: (1) recorded absence (`eda_artifact: none`), (2) profile
fallback (`DATA-PROFILE.yaml`), (3) declared honesty (`computed_by`). Each of the
five skills' `When absent:` sentence must name all three tiers in this order, scoped
to that skill's own facts — D-26-03's drafted example for scope-analysis already does
this correctly ("record `eda_artifact: none` and source grain, dependence,
missingness and base-rate facts from the DATA-PROFILE keys above; where the profile is
also absent, declare each with `computed_by` honesty rather than asserting it").

### Guard test skeleton (style precedent: `tests/test_phase14_onboarding.py`)

```python
"""Off-gate-path repo-integrity guard (REQ-P26-02): the <inputs> block each of the
five downstream skills carries must name only keys that exist in the live templates.
...
Zero imports from dsx/ (D-26-04) -- structurally outside test_gate_path_hermetic's
import-closure walk regardless (that walk starts only from dsx.cli.GATE_PROFILES-
resolved dsx/checks and dsx/frame files; tests/ is never in it), this is additional
margin, not a load-bearing requirement of that other test.

Deliberately does not `import yaml`: PyYAML is an optional dependency in this repo's
own pattern (dsx/loader.py falls back to a bundled parser when absent), and even with
PyYAML the per-column/flag-gated example keys these skills read are behind YAML `#`
comments that any conformant parser discards -- an uncomment-preprocessing step is
required either way, so a hand-rolled line-oriented key-path extractor is used
directly instead of a parse-then-preprocess-then-reparse round trip.

CRLF discipline: templates/EDA.md is CRLF; templates/DATA-PROFILE.yaml is bare-LF
(verified live) -- every split uses `\r?\n`, never a bare `\n` or `\r\n`-only pattern.

Run: python -m unittest tests.test_skill_read_contracts -v
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EDA_TEMPLATE = ROOT / "templates" / "EDA.md"
PROFILE_TEMPLATE = ROOT / "templates" / "DATA-PROFILE.yaml"

FIVE_SKILLS = (
    "dsx-scope-analysis",
    "dsx-define-metrics",
    "dsx-design-experiment",
    "dsx-build-model",
    "dsx-narrate",
)

_INPUTS_RE = re.compile(r"<inputs>(.*?)</inputs>", re.DOTALL)
_BULLET_KEY_RE = re.compile(r"^\s*-\s+`([^`]+)`\s*$")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _lines(text: str) -> list[str]:
    return re.split(r"\r?\n", text)

# ... parse_eda_keys(), parse_profile_keys() (uncomment-then-indent-stack),
# extract_inputs_block(skill_text), extract_key_region(inputs_text, header),
# per D-26-01/D-26-04's parse contract above.


class TestSkillReadContracts(unittest.TestCase):
    def test_negative_control_orphan_key_is_rejected(self):
        eda_keys = parse_eda_keys(_read(EDA_TEMPLATE))
        self.assertNotIn("grain.__orphan__", eda_keys)

    def test_anchor_non_vacuity(self):
        eda_keys = parse_eda_keys(_read(EDA_TEMPLATE))
        self.assertGreaterEqual(len(eda_keys), 30)
        self.assertIn("grain.verdict", eda_keys)
        profile_keys = parse_profile_keys(_read(PROFILE_TEMPLATE))
        self.assertIn("columns[].null_rate", profile_keys)  # only present after uncomment

    def test_every_skill_carries_at_least_one_key_region(self):
        checked = 0
        for name in FIVE_SKILLS:
            text = _read(SKILLS / name / "SKILL.md")
            m = _INPUTS_RE.search(text)
            self.assertIsNotNone(m, f"{name}: no <inputs> block found")
            checked += 1
        self.assertEqual(checked, 5)

    # ... per-skill, per-region set-membership tests against parse_eda_keys() /
    # parse_profile_keys(), plus the also-consult zero-backtick assertion.
```

## State of the Art

Not applicable in the "library version" sense — this is a repo-local prompt-doc +
static-test pattern. The relevant precedent IS the repo's own prior art, already
established and directly reusable:

| Precedent | What it does | Relevance to this phase |
|---|---|---|
| `tests/test_selection_heuristic_docs.py` | Off-gate-path Markdown-content invariant, CRLF-safe via whitespace-collapse | Same class of test as REQ-P26-02's guard; note it DOES `import` from `dsx.checks.viz` for a vocabulary constant — the new test is stricter (zero dsx/ imports) per D-26-04 |
| `tests/test_phase14_onboarding.py` | Doc/skill/template phase Nyquist validation via structural assertions (file existence, required steps, honesty claims) rather than runtime behaviour | Closest structural precedent for how to write `tests/test_skill_read_contracts.py`'s docstring, ROOT resolution, and per-requirement test method naming |
| `dsx/loader.py` | PyYAML-optional, bundled-fallback YAML subset parser | Establishes the "PyYAML is optional here" precedent this research cites against `import yaml` in the new test |

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| — | none | — | Every claim in this document was verified live this session (file reads, byte-level line-ending scans, a live `git status` check, a live `python -m unittest`-style YAML parse attempt, and direct inspection of `install.mjs`/`test_gate_path_hermetic.py`/`gen-finding-catalogue.py`/`test_finding_catalogue_invariant.py` source). No `[ASSUMED]` tags were needed. |

**This table is empty.** All claims in this research were verified or cited — no user
confirmation needed.

## Open Questions

The six residuals 26-CONTEXT.md flagged for the S2-2 plan gate are all now resolved
by this research (not merely restated):

1. **Residual 1 (DATA-PROFILE list IS checked, uncomment pre-processor mandatory).**
   RESOLVED — confirmed live: 8 of the ~30 named keys across the five skills
   (`unit.*`, `target.*`, `columns[].*`) exist ONLY as commented example lines; a
   live-YAML-only scan would false-fail on all 8. See "Pattern 2" table above.
2. **Residual 2 (verbatim notation both sides).** RESOLVED — traced the exact
   indentation math the uncomment step must reproduce (`columns`(0) >
   `column_name`(4) > `null_rate`(6)); confirmed `column_name` is the live placeholder
   token (residual 5, same finding).
3. **Residual 3 (Also-consult zero-backtick + one-key-per-bullet as explicit
   assertions).** RESOLVED at the design level (D-26-01 already specifies both as
   parse-contract assertions, not conventions) — this research adds no new finding
   here beyond confirming the two prose-only facts (joins matrix, wide-categorical
   `policy_recommendation`) really are absent from EDA.md's front-matter block, so the
   zero-backtick assertion has something real to enforce.
4. **Residual 4 (per-skill region matrix, ≥1 region not both-required).** RESOLVED —
   the D-26-02 table shows every one of the five skills reads BOTH an EDA region and a
   DATA-PROFILE region (no skill is EDA-only or profile-only in the settled mapping),
   so `checked == 5` combined with "≥1 region per skill" is satisfied trivially by the
   current mapping; the ≥1 rule still matters as a forward-looking guard if the plan
   trims a skill down to one region.
5. **Residual 5 (`column_name` placeholder token).** RESOLVED — confirmed live,
   `templates/DATA-PROFILE.yaml` line 20: `  # column_name:`. Document this exact
   token in the new test's docstring per the residual's own instruction.
6. **Residual 6 (byte-identity + installer mechanics).** RESOLVED — `git status
   --porcelain -- dsx/` is empty at research time (clean baseline); the phase-end
   command sequence is `node install.mjs && node install.mjs --check` (not `--check`
   alone — see Pitfall 3); `python scripts/gen-finding-catalogue.py --check` exits 0
   today with pre-existing warnings unrelated to this phase (duplicate-declaration
   notices for codes this phase does not touch); `tests/test_finding_catalogue_invariant.py`'s
   `_EXPECTED_TOTAL = 276` is the live re-measure mechanism for the 276→276 proof.

No new open questions surfaced. The one item worth flagging forward (not blocking):
CONTEXT.md's stated rationale for avoiding PyYAML ("won't load") is inaccurate; the
plan's new-test docstring should state the corrected rationale (comments are invisible
to any parser; PyYAML is optional in this repo) rather than repeat the inaccurate one
verbatim from CONTEXT.md.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python (real interpreter) | Running the new test + full suite + catalogue check | ✓ | 3.12.10 (`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`) | — |
| Node.js | `install.mjs` re-sync | ✓ | confirmed runnable this session (`node -e` calls succeeded) | — |
| PyYAML | NOT required — see Standard Stack / Don't Hand-Roll | ✓ present on this machine (6.0.3) but must NOT be imported by the new test | 6.0.3 | stdlib-only line-oriented parser (the design) |
| Git | `git status --porcelain -- dsx/` byte-identity proof | ✓ | confirmed working tree query succeeded, 0 lines changed under `dsx/` at research time | — |

No missing dependencies. Nothing blocks execution.

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | `unittest` (Python 3.12 stdlib) — no pytest in this repo |
| Config file | none — `scripts/check.sh` runs `python3 -m unittest discover -s tests -q`; individually `python -m unittest tests.test_skill_read_contracts -v` |
| Quick run command | `"C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe" -m unittest tests.test_skill_read_contracts -v` |
| Full suite command | `"C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe" -m unittest discover -s tests -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| REQ-P26-01 | Each of the 5 skills carries exactly one `<inputs>…</inputs>` block, at the correct insertion point, with ≥1 key region | unit | `python -m unittest tests.test_skill_read_contracts.TestSkillReadContracts.test_every_skill_carries_at_least_one_key_region -v` | ❌ Wave 0 (new file) |
| REQ-P26-01 | Each `When absent:` sentence names the eda_artifact:none tier before the DATA-PROFILE/computed_by tiers (structural presence of the fallback line, not full-ladder semantic proof) | unit | same test file — a dedicated per-skill assertion that the `When absent:` line exists and contains `eda_artifact: none` | ❌ Wave 0 |
| REQ-P26-02 | Every named EDA front-matter key exists in `templates/EDA.md`'s live key set (dotted-path, `[]` for list-of-map) | unit | per-skill, per-region set-membership test against `parse_eda_keys()` | ❌ Wave 0 |
| REQ-P26-02 | Every named DATA-PROFILE key exists in `templates/DATA-PROFILE.yaml`'s live-plus-uncommented key set | unit | per-skill, per-region set-membership test against `parse_profile_keys()` | ❌ Wave 0 |
| REQ-P26-02 | A renamed/fabricated key FAILS the suite (negative control — the load-bearing anti-silent-orphan proof) | unit | `test_negative_control_orphan_key_is_rejected` — feeds `grain.__orphan__` / `columns[].__orphan__` through the same matcher and asserts non-membership | ❌ Wave 0 |
| REQ-P26-02 | Anti-vacuity: the parser did not degenerate to an empty or over-broad set | unit | `test_anchor_non_vacuity` — `len(eda_keys) >= 30`, known real keys present, `columns[].null_rate` present only after uncomment | ❌ Wave 0 |
| REQ-P26-02 | CRLF-tolerant across both templates (one CRLF, one bare-LF, verified live) | unit | implicit in every parse test — assert both templates parse with a nonzero key count using `\r?\n` splitting | ❌ Wave 0 |
| REQ-P26-03 | `dsx/` byte-identical for the phase | smoke | `git diff --stat -- dsx/` (expect empty output); baseline confirmed empty at research time via `git status --porcelain -- dsx/` | ✅ (git, no new file) |
| REQ-P26-03 | Zero new finding codes (276 → 276) | smoke | `python scripts/gen-finding-catalogue.py --check` (exit 0, confirmed today) THEN `python -m unittest tests.test_finding_catalogue_invariant -v` (`_EXPECTED_TOTAL = 276`) | ✅ existing |
| REQ-P26-03 | Installed copies re-synced and `--check` passes | smoke | `node install.mjs && node install.mjs --check` (NOT `--check` alone — see Pitfall 3) | ✅ existing installer |

### Sampling Rate
- **Per task commit:** `python -m unittest tests.test_skill_read_contracts -v` (fast — reads 7 small files, no I/O beyond that)
- **Per wave merge:** `python -m unittest discover -s tests -q` (full suite — confirmed 1583 tests passing as of the 25-VERIFICATION.md baseline; this phase adds test methods, not new dsx/ modules, so the count should only grow)
- **Phase gate:** full suite green, `scripts/gen-finding-catalogue.py --check` exit 0, `node install.mjs && node install.mjs --check` exit 0, `git diff --stat -- dsx/` empty — all four before `/gsd-verify-work`

### Wave 0 Gaps
- [ ] `tests/test_skill_read_contracts.py` — the entire test file is new; covers REQ-P26-01 and REQ-P26-02 in full
- [ ] No shared fixtures needed — the test reads `templates/EDA.md`, `templates/DATA-PROFILE.yaml`, and the five `skills/*/SKILL.md` files directly via `Path(__file__).resolve().parents[1]`, matching every existing repo-integrity test's pattern
- [ ] No framework install needed — `unittest` is stdlib

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | No auth surface touched — prompt text and a local static-analysis test |
| V3 Session Management | no | N/A |
| V4 Access Control | no | N/A |
| V5 Input Validation | no (narrow sense) | The new test's only "input" is the repo's own committed files, resolved via `Path(__file__).resolve().parents[1]` (no user-controlled path, no network, no untrusted data) — same trust model as every other repo-integrity test in `tests/` |
| V6 Cryptography | no | N/A |

### Known Threat Patterns for this stack

None applicable. This phase has zero new attack surface: no new executable code path,
no new network call, no new file write outside git-tracked source, no new dependency,
no change to any `dsx/` module (the only Python that ever runs against untrusted
analyst input). The new test reads only files this repo already commits and controls;
the skill edits are agent-facing prose an LLM reads, not code that parses external
input. `security_enforcement: true` in `.planning/config.json` is acknowledged; this
section is intentionally thin because the phase genuinely has no security-relevant
surface — a longer table here would manufacture relevance that doesn't exist.

## Sources

### Primary (HIGH confidence — read live, this session)
- `.planning/phases/26-per-skill-read-contracts/26-CONTEXT.md` — the settled design (D-26-01..04), read in full
- `.planning/REQUIREMENTS.md` — REQ-P26-01..03 exact text
- `.planning/STATE.md` — phase status, prior decisions
- `templates/EDA.md`, `templates/DATA-PROFILE.yaml` — read in full, byte-scanned for line endings
- `skills/dsx-scope-analysis/SKILL.md`, `skills/dsx-define-metrics/SKILL.md`, `skills/dsx-design-experiment/SKILL.md`, `skills/dsx-build-model/SKILL.md`, `skills/dsx-narrate/SKILL.md` — heads read, byte-scanned for line endings
- `capabilities/dsx/fragments/executor.md` — read in full, fallback wording located at L10-17
- `install.mjs` — read in full (`install()`, `check()`, `CAPABILITY_PAYLOAD`)
- `capabilities/dsx/capability.json` — read in full, confirmed all five skills in `manifest.skills`
- `tests/test_gate_path_hermetic.py` — read in full, confirmed closure-walk starting point excludes `tests/`
- `tests/test_selection_heuristic_docs.py`, `tests/test_phase14_onboarding.py` — read as style precedent
- `scripts/check.sh`, `scripts/gen-finding-catalogue.py`, `tests/test_finding_catalogue_invariant.py` — read, confirmed 276-count mechanism and current-catalogue exit-0 status live
- `dsx/loader.py` — read, confirmed PyYAML-optional pattern
- Live shell checks this session: line-ending byte scans of both templates and all five skill files; `python -m unittest`-style `yaml.safe_load()` attempts on both templates; `git status --porcelain -- dsx/` (empty); `pip show pyyaml` (6.0.3, confirmed present but not to be imported); `python scripts/gen-finding-catalogue.py --check` (exit 0)

### Secondary (MEDIUM confidence)
- `.planning/research/V2.6-SCOPE.md` §3 Phase 26 — background only; CONTEXT.md supersedes it per the phase's own instructions, consulted for context not as a design source
- `.planning/phases/25-hermetic-profile-depth/25-04-PLAN.md`, `25-04-SUMMARY.md` — precedent for the `node install.mjs && node install.mjs --check` command pattern, cross-checked against `install.mjs`'s own source (primary)

### Tertiary (LOW confidence)
- none

## Metadata

**Confidence breakdown:**
- Key grounding (D-26-02 mapping vs live templates): HIGH — every key checked by direct file read, table above is exhaustive
- Insertion points (D-26-01 vs live skill heads): HIGH — every skill's head read, exact tag sequence quoted
- Guard mechanics (D-26-04 parser approach): HIGH — indentation math traced by hand against real bytes; PyYAML behavior empirically tested live, correcting CONTEXT's stated rationale without changing its conclusion
- Installer/byte-identity mechanics (REQ-P26-03): HIGH — `install.mjs` read in full; live `git status` and `gen-finding-catalogue.py --check` run this session
- Security: HIGH (by absence — verified no new surface exists, not merely asserted)

**Research date:** 2026-09-07
**Valid until:** effectively unbounded for the template/skill content claims (they are
repo-local facts, not external library behavior) — re-verify only if `templates/EDA.md`,
`templates/DATA-PROFILE.yaml`, `install.mjs`, or `tests/test_gate_path_hermetic.py`
change before this phase executes.
