# Phase 26: Per-skill read contracts — Context

**Milestone v2.6 Exploration Depth and Backlog Evidence · S2-1 discuss · 2026-09-07
(autonomous firing).** The second phase of the milestone, unblocked by Phase 25's
completion (S1-5 DONE). Five downstream skills — `dsx-scope-analysis`,
`dsx-define-metrics`, `dsx-design-experiment`, `dsx-build-model`, `dsx-narrate` —
each gain **one named-input read step at the head** that names the `EDA.md`
front-matter keys and the `DATA-PROFILE.yaml` keys it reads, what each changes in its
output, and the recorded fallback when the EDA artifact is absent (`eda_artifact:
none`), **mirroring the executor fragment's existing rule** (`capabilities/dsx/
fragments/executor.md` L16-17). An off-gate-path repo-integrity test then makes a
renamed template key fail the suite instead of silently orphaning a read step.
Requirements: REQ-P26-01 … REQ-P26-03 (3). Phase 26 **mints zero new finding codes**
and keeps **`dsx/` byte-identical** (REQ-P26-03) — it is skill-doc + one test only.

## Phase Boundary

Skill-only. **No `dsx/` change of any kind** (byte-identical for the phase, proven by
`git diff --stat -- dsx/` empty); **zero new codes** (set-identity 276 → 276,
re-measured live); the new repo-integrity test is **off the gate path** — it imports
nothing from `dsx/` and touches only `tests/`. The templates it validates against
(`templates/EDA.md`, `templates/DATA-PROFILE.yaml`) are **not edited**: the settled
per-skill mapping names only keys that already exist in them (verified this firing),
so no template grows. Installed copies of the five edited skills are re-synced and
`node install.mjs --check` must pass at phase end.

**In-scope edits:** `skills/{dsx-scope-analysis,dsx-define-metrics,dsx-design-experiment,
dsx-build-model,dsx-narrate}/SKILL.md` (one `<inputs>` block each, at the head) +
new `tests/test_skill_read_contracts.py` (the guard) + installer re-sync.
**Frozen (prove byte-unchanged):** everything under `dsx/`; `templates/EDA.md` and
`templates/DATA-PROFILE.yaml`; catalogue set-identity **276 → 276**.

## Ground truth read this firing (assumptions mode)

Live structures read in full, so the mapping is grounded against reality — not the
scope table, which V2.6-SCOPE.md §3 explicitly calls "a starting proposal, not the
decision":

- **`templates/EDA.md` front-matter** — the authorized key set a read step may name
  (dotted paths): top-level `eda_version, dataset, spec_path, profile_path,
  profile_source_hash, question_type, columns_scoped, completed_through,
  artifact_status, comparisons_looked_at, interim_looks, ledger_rows, stop_triggered,
  contradictions, spec_validate_exit, rerun_clean, seed`; `grain.{declared, observed,
  verdict, duplicate_rate, rows_per_unit, largest_unit_share, implied_dependence.
  structure, implied_dependence.cluster_var}`; `missingness[].{column, rate,
  mechanism, evidence}`; `time.{staleness_days, first_period_ratio, last_period_ratio,
  tz_verdicts, gaps}`; `base_rate.{metric, overall, weekly_range, verdict}`;
  `branch.{ran, verdict, downgrade_to, blocked_on}`; `segments_candidates[].{column,
  levels, headline_range, n_min, underpowered}`; `leakage_suspects[].{column,
  reason}`; `dependence.{icc, outcome_sd, weekly_cycle_amplitude}`.
- **`templates/DATA-PROFILE.yaml`** — uncommented top-level keys `profile_version,
  computed_by, source_path, source_hash, row_count, columns, primary_key,
  primary_key_unique, duplicate_rate, time.{column,min,max,max_gap_days},
  sentinels_found`. **Critical subtlety:** the per-column and flag-gated keys a skill
  most wants to read — `columns[].{null_rate,n_unique,dtype,numeric.*,categorical.*}`,
  `time.{rows_per_day,first_period_ratio,last_period_ratio,share_at_hour_00}`,
  `unit.*`, `target.*` — exist in the template **only as commented `#` example lines**
  (they are per-column / emitted only under `--unit`/`--target`, so they cannot appear
  as live top-level YAML). A naive "is this a live YAML key" scan would false-fail on
  exactly these; the guard parser MUST uncomment `#` lines before matching.
- **`capabilities/dsx/fragments/executor.md` L16-17** — the read-contract rule the
  five steps mirror: read EDA front-matter first when present; `stop_triggered: true`
  ⇒ resolve `contradictions` before computing; no EDA ⇒ record `eda_artifact: none`
  and source the facts from `DATA-PROFILE.yaml` or declare them with `computed_by`
  honesty. Three-tier honesty ladder: recorded absence → profile fallback → declared.
- **The five skills** — each opens `<objective>…</objective>` then a process block
  (`<process>` / `<design_mode>` / `<order_of_operations>` / `<structure>` /
  `<definition_contract>`). Today **none** carries a read step (S0-2 premise 4:
  read-cue hits = 0 for all five; `dsx-explore-data` is the only consumer).

Two grounding problems the scope's proposal carried, both resolved below: the scope
gave `dsx-define-metrics` a "joins matrix" and `dsx-build-model` a
`policy_recommendation` as if front-matter keys — **both live only in EDA prose**
(§1 Joins; §4 Wide categoricals), so naming them as keys would fail REQ-P26-02's
guard. They are handled as prose "Also consult" references, never machine-parsed keys.

## Decisions

Settled by an internal advisor round (brief §4) — **Architect** (`dsx-analysis-architect`,
read-contract design + grounded mapping + fallback) and **Auditor**
(`dsx-ml-integrity-auditor`, guard-test correctness / anti-silent-orphan), spawned in
parallel on grounded prompts (no re-exploration). Both proposed → self-critiqued →
recommended; the orchestrator converged, breaking the one divergence by
**rigour > reliability > flexibility**. Zero codes minted ⇒ no D-06 veto item owed;
these are design decisions, vetoable via this CONTEXT (silence = accept).

### D-26-01 — The read-step shape (the one persona divergence)

**Divergence.** Architect proposed a *visible* `<inputs>` block with bold-labeled,
comma-separated key lines. Auditor proposed *hidden* `<!-- reads:eda-frontmatter -->`
HTML-comment fences with **one key per line** (wrap-proof) and warned that
single-line comma lists silently drop keys when an author hard-wraps.

**Decision — visible `<inputs>` block, one backtick-wrapped key per bullet line.**
Takes the Architect's visible form (rejecting hidden HTML-comment fences) *and* the
Auditor's one-key-per-line + loud-fail rigour. Literal skeleton, placed immediately
after `</objective>` in every skill (for `dsx-narrate`, before `<precondition>`):

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

**Why visible over hidden fences (rigour > reliability > flexibility).** A portfolio
artifact read by skeptical engineers should parse the keys the reader *sees*; a hidden
comment fence creates a parallel structure that can silently drift from the visible
prose. One-key-per-bullet gives the Auditor's wrap-safety without the hidden layer:
each key is on its own visible line, so nothing is dropped on a wrap, and any
non-conforming line inside a key region fails loudly (stray prose cannot smuggle in as
"zero keys").

**Parse contract (what the guard requires of the shape).** Locate exactly one
`<inputs>…</inputs>` per skill (`(?s)`, CRLF via `\r?\n`). The line
`EDA front-matter keys read:` opens the EDA region; the region is the contiguous run
of bullet lines that follow, each matching `^\s*-\s+` + one backtick token + end
(`^\s*-\s+\`([^\`]+)\`\s*$`) — a bullet with anything else fails. The line
`DATA-PROFILE keys read` opens the profile region, same bullet rule. The
`These set:` / `Also consult:` / `When absent:` lines are prose and are **never**
parsed as keys; the guard additionally asserts the `Also consult:` line contains
**zero backticks** (the mechanism that keeps joins / `policy_recommendation` honest
but unparsed). Keys are matched as **full dotted paths** with `[]` marking a list
element (`missingness[]`, `columns[].n_unique`, `grain.implied_dependence.structure`).

### D-26-02 — The grounded per-skill mapping

Every key below is verbatim from the authorized sets above; the scope proposal's
corrections are noted. Ratifiable at the S2-2 plan gate: a read step should name only
keys the skill genuinely consumes, and the plan may trim if a listed key proves unused
(the guard passes on any real key, so trimming is safe, over-naming is a maintenance
cost not a gate failure).

| Skill | EDA front-matter keys | DATA-PROFILE keys | These set | Also consult (prose) |
|---|---|---|---|---|
| `dsx-scope-analysis` | `grain.verdict`, `grain.implied_dependence.structure`, `grain.implied_dependence.cluster_var`, `missingness[]`, `base_rate.verdict`, `contradictions`, `stop_triggered` | `primary_key_unique`, `duplicate_rate`, `unit.rows_per_unit`, `unit.largest_unit_share`, `columns[].null_rate`, `target.verdict` | validity-frame units, dependence, missingness; refuses to scope past `stop_triggered: true` (resolve `contradictions` first) | none |
| `dsx-define-metrics` | `grain.declared`, `grain.observed`, `grain.verdict`, `grain.duplicate_rate` | `primary_key`, `primary_key_unique`, `duplicate_rate`, `columns[].n_unique`, `columns[].dtype` | metric `grain`, `denominator` (fan-out / double-count risk), `computed_by` | §1 Joins — the join fan-out matrix informing the denominator |
| `dsx-design-experiment` | `dependence.icc`, `dependence.outcome_sd`, `dependence.weekly_cycle_amplitude`, `base_rate.overall`, `grain.implied_dependence.structure`, `grain.implied_dependence.cluster_var` | `target.overall`, `target.weekly_range`, `unit.rows_per_unit`, `unit.largest_unit_share` | `dsx power` inputs, `design.baseline_rate`, `variance_adjustment` (cluster from `cluster_var`), whole-week run duration | none |
| `dsx-build-model` | `leakage_suspects[]`, `grain.implied_dependence.structure`, `grain.implied_dependence.cluster_var`, `segments_candidates[]` | `columns[].n_unique`, `columns[].dtype`, `columns[].categorical`, `unit.rows_per_unit`, `time.column`, `time.max_gap_days` | `model.features_excluded_for_leakage`, split type (temporal/grouped/`grouped_temporal`), `entity_column`, encoding policy | §4 Wide categoricals — the policy recommendation informing encoding |
| `dsx-narrate` | `dataset`, `base_rate.overall`, `base_rate.metric`, `segments_candidates[]`, `comparisons_looked_at`, `artifact_status` | `row_count`, `time.min`, `time.max`, `target.overall` | population sentence, base for relative %, the "what would change this" section | none |

Corrections vs the scope proposal: `contradictions[]`→`contradictions` (top-level, no
brackets); bare `weekly_cycle_amplitude`→`dependence.weekly_cycle_amplitude`;
`grain.implied_dependence` expanded to its two real leaves; whole-block `base_rate`
expanded to `.overall`/`.verdict`/`.metric` leaves; `dataset` added to ground the
population sentence; "joins matrix" and "policy_recommendation" moved from key lists to
prose "Also consult" (grounding problems #1/#2).

### D-26-03 — The fallback wording

Per-skill `When absent:` sentence, each mirroring the executor fragment's three-tier
honesty ladder (recorded absence → profile fallback → `computed_by` declaration),
naming the tier the specific skill would otherwise fake. Authored per the Architect's
D-A3 drafts, e.g. scope-analysis: "no `EDA.md` → record `eda_artifact: none` and
source grain, dependence, missingness and base-rate facts from the DATA-PROFILE keys
above; where the profile is also absent, declare each with `computed_by` honesty
rather than asserting it — and never read a missing EDA as a `stop_triggered` clear."
The four remaining sentences are drafted in the S2-1 persona record and finalized
verbatim into each skill at execute (S2-3).

### D-26-04 — The guard-test contract (REQ-P26-02)

Adopt the Auditor's design in full — it is what makes a renamed template key *fail*
rather than silently orphan.

- **File:** `tests/test_skill_read_contracts.py`, `unittest`, class
  `TestSkillReadContracts`. Discovered by `scripts/check.sh` (`unittest discover`).
  Roots via `Path(__file__).resolve().parents[1]`. **Zero imports from `dsx/`** — off
  the gate path (the `test_gate_path_hermetic` invariant keeps `tests/` out of the
  gate import closure); mints no code; `dsx/` byte-identical.
- **Template path-sets** built by a shared line-oriented parser (no PyYAML — the
  templates carry placeholders like `<int>` and `MCAR | MAR | …` that will not load):
  indent-stack + inline-flow awareness yields **every dotted path incl. intermediates**,
  `[]` for list-of-map elements. EDA: lines strictly between the first two `---` lines,
  skipping `#` comment lines and stripping inline `# …`. DATA-PROFILE: **uncomment**
  every `#` example line first (`raw.replace("#"," ",1)`, preserving indentation) so
  per-column/flag-gated example keys count as existing, then drop trailing inline
  comments; normalize the per-column placeholder `columns.column_name.*` → `columns[].*`.
- **Matching:** full dotted-path set-membership, per skill, per region; a missing key
  fails with a message naming the skill, the region and the orphaned key ("was the
  template key renamed or removed?"). Leaf-only matching is **rejected** — a parent
  rename (`base_rate:`→`baseline:`) would leave a leaf like `overall` matchable
  elsewhere and silently orphan the read step, the exact failure REQ-P26-02 forbids.
- **Anti-silent-orphan proof (the load-bearing part):** an in-file **negative control**
  feeds a fabricated key (`grain.__orphan__`, `columns[].__orphan__`) through the same
  helper and asserts it raises, plus asserts the parser did not invent it; an **anchor
  non-vacuity pin** asserts known real keys are present and `len(eda) >= 30` so a
  degenerate/over-broad parse fails immediately; **per-skill non-vacuity** requires
  each of the five skills to carry an `<inputs>` block with ≥1 key region, and
  `checked == 5`.

## Named exclusions (not omissions)

- **No `dsx/` edits, no new codes** — skill-doc + test only (D-01/D-02 boundary;
  REQ-P26-03). The guard reads templates and skill files as ground truth; it needs no
  live `dsx` symbol.
- **Templates unchanged.** The mapping names only pre-existing EDA/profile keys, so
  neither `templates/EDA.md` nor `templates/DATA-PROFILE.yaml` grows. If the plan finds
  a genuinely needed fact with no key, that is a *scope* question (a template grows) —
  escalate, do not invent a key to satisfy a read step.
- **The executor fragment is not re-edited** — it already carries the contract; Phase
  26 mirrors it into the five skills.
- **Prose-only EDA facts (joins matrix, wide-categorical policy recommendation)** are
  named as "Also consult" prose, never machine-parsed keys.

## Residuals flagged for the S2-2 plan gate

1. **DATA-PROFILE list IS checked** (REQ-P26-02: "every profile key it names exists in
   templates/DATA-PROFILE.yaml"). The plan must implement the uncomment pre-processor
   exactly, or the guard false-fails on every per-column key. Resolved in D-26-04;
   flagged so the plan does not regress to a live-YAML-only scan.
2. **Verbatim notation on both sides** — read steps write `missingness[]`,
   `columns[].n_unique`, `grain.implied_dependence.structure` exactly as the templates
   render them; the guard uses one normalization policy applied to both the key set and
   the extracted tokens.
3. **`Also consult:` zero-backtick assertion** and one-key-per-bullet enforcement are
   the two mechanisms keeping prose-only refs honest-but-unparsed; the plan must encode
   both as explicit assertions, not conventions.
4. **Per-skill region matrix** — require ≥1 region per skill and validate whichever
   regions are present, rather than hard-requiring both EDA and DATA-PROFILE regions
   for all five (some skills may legitimately read only EDA); confirm the matrix
   against the D-26-02 table.
5. **`column_name → []` normalization** hardcodes the single per-element placeholder
   token the profile template uses today; document this in the test docstring so a
   future second placeholder is not missed.
6. **Byte-identity + installer** — `git diff --stat -- dsx/` empty for the phase; two
   runs diff cleanly (static prose); `node install.mjs --check` passes after the five
   skill edits; catalogue 276 → 276 re-measured.

## Persona round record (loud, per brief §4)

- **Architect (`dsx-analysis-architect`, opus-class, grounded):** proposed the visible
  `<inputs>` shape, the grounded per-skill mapping (correcting the scope's two
  prose-only misfilings), and the five fallback sentences; self-critiqued the
  backtick-boundary fragility (mitigated by one-key-per-bullet) and flagged the
  DATA-PROFILE commented-key validation as the top blocking residual.
- **Auditor (`dsx-ml-integrity-auditor`, opus-class, grounded):** proposed the guard's
  parse/assertion contract, argued decisively for full dotted-path over leaf-only
  matching (rename-safety), specified the uncomment pre-processor for the commented
  profile keys, and designed the negative-control + anchor-pin that prove the guard
  bites; self-critiqued the intended coupling of the anchor pin to template keys
  (forces a reviewed update on a legitimate rename).
- **Convergence:** one divergence (visible block vs hidden HTML-comment fences),
  resolved to the **visible block** by rigour > reliability > flexibility — the keys a
  skeptical reader sees must be the keys the guard parses, and one-key-per-bullet buys
  the Auditor's wrap-safety without a hidden parallel structure. All other
  recommendations adopted as proposed. No requirement reworded; no scope change; no
  human escalation owed (zero codes, no D-05 read — Phase 26's D-05 burden is 0).
