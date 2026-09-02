# LOOP-LEDGER-ARCHIVE — v2.4 Visual Excellence

Long-form evidence for ledger units, offloaded from `LOOP-LEDGER.md` to keep the
hot-path Log lean (brief §5). One `## <unit-id>` section per unit that needs more
than a pointer. The Log line in `LOOP-LEDGER.md` is the index into this file.

---

## S1-2 — Phase 21 plan (planned 2026-09-02, measured UTC ~22:40Z)

**Outcome: DONE. Plan-checker PASSED 12/12 dimensions.** Phase 21 planned via the
`gsd-plan-phase 21` workflow, driven headlessly through every quality gate, then
stopped at the plan-checker pass (the §15 auto-advance to execute was deliberately
NOT taken — see "Boundary held").

### Artifacts produced
- `21-RESEARCH.md` (gsd-phase-researcher, sonnet — adaptive routing).
- `21-VALIDATION.md` (seeded draft, Nyquist; committed `bfa9be7`).
- `21-01-PLAN.md` (gsd-planner, opus — adaptive routing): 1 plan, 1 wave, 3 TDD
  tasks. RED (write `tests/test_viz_vocabulary_invariant.py` — both D-01 clauses +
  frozen 14-mark CAPABILITY_ONLY allowlist + D-02 refusal completeness + gate
  smokes) → GREEN (home the 12 orphans in CHART_CAPABILITIES/RELATIONSHIP_CHARTS,
  then regenerate `dsx/data/input_types.json`) → GREEN (enrich BANNED_TYPES to
  `{reason,code,citation}`, fix the one `_check_banned` reader, annotate HQ-27,
  prove 275 → 275). Covers REQ-P21-01/02/03.

### Gates (all real, orchestrator-run or independently-agent-verified)
- **gsd-plan-checker (opus/high): `## VERIFICATION PASSED`, 12/12 dimensions**, no
  blockers/warnings. Verified against the LIVE tree, not the plan's prose. Notably
  went deeper than RESEARCH on the zero-mint proof: independently confirmed
  `gen-finding-catalogue.py::extract()` (lines 218-234) reads only the positional
  `report.add()` args `[0..2]` (code/severity/message); the `detail=` reference at
  line 250 is inside a *different* function (`extract_sql_rules()`), so the
  BANNED_TYPES `dict[str,str] → {reason,code,citation}` promotion provably cannot
  mint or alter a code. Also validated the IT040 gate smoke (real interval-range
  record, no EXTRA_MARKS entry, currently excludes histogram → will admit after
  regeneration). Nyquist Dim-8 PASS. CLAUDE.md/CRLF compliance PASS (invariant
  test reads live Python objects, no line-anchored parsing → CRLF N/A).
- **Requirements coverage: 3/3** — REQ-P21-01/02/03 in plan frontmatter (YAML
  block list; the workflow's inline grep missed the block form, verified directly)
  and confirmed by plan-checker Dim-1.
- **Decision-coverage gate: 2/2 passed** (`check.decision-coverage-plan`). The
  planner added a machine-readable `- **D-01 …:**` / `- **D-02 …:**` bullet index
  to the top of `21-CONTEXT.md`'s `## Decisions` section — this is the known
  context-coverage parser false-block documented in HUMAN-QUEUE standing notes
  (discuss writes `### D-01 —` headings the parser can't read). Resolved
  legitimately: the gate is now GENUINELY green (no override needed); the edit is
  purely additive, explicitly comment-marked "decision CONTENT is unchanged," and
  the authoritative `### D-01`/`### D-02` bodies are untouched. Verified faithful
  by reading the diff before accepting.

### Persona-round decisions this firing (loud, per brief §4)
1. **Research ON, not `--skip-research`.** Revised mid-firing after reading config:
   `research=true` AND `nyquist_validation=true`, so skipping would NOT cleanly
   disable the Nyquist expectation (it would warn + risk a plan-checker Dim-8 gap)
   — the brief forbids skipping a Nyquist gate to save time. Also: one authoritative
   CONTEXT.md + a role-distinct RESEARCH.md is not the duplicate-truth drift surface
   D-02 rejected. Rigour > flexibility → run the config's designed pipeline.
2. **Plan-checker at opus, not the adaptive-default haiku.** Brief §3 explicitly
   routes plan-check → opus/high; I am the direct spawner, and this is the S1-2 gate
   on a portfolio-grade repo. Rigour tier.

### Skipped as redundant/non-gate (recorded, not silent)
- **pattern-mapper (§7.8, optional/non-blocking):** RESEARCH already mapped the exact
  analog test files (`test_finding_catalogue_invariant.py`,
  `test_phase20_zero_mint_close.py:79-84`) + the importlib idiom.
- **intel api-surface (§7.9):** advisory HINT ("may be incomplete, never exhaustive"),
  not a gate; planner had exhaustive CONTEXT/RESEARCH grounding; avoids committing a
  repo-wide intel artifact as a planning side effect.
- **spec-less probe fallback (§7.95):** no SPEC.md; requirements are precise; the
  planner did standard goal-backward must_haves derivation (checker Dim-6 PASS).
- **dsx-scope-analysis step (§5.6 dsx hook):** self-gating — "if it produces no
  number/model/chart, skip"; Phase 21 is non-analytical → no ANALYSIS-SPEC.yaml,
  `dsx gate plan` passes cleanly.

### RESEARCH findings beyond CONTEXT (carried into the plan)
- **input_types.json regeneration gotcha:** CHART_CAPABILITIES/EXTRA_MARKS edits only
  reach the gate's IT-id path through the *generated static* `dsx/data/input_types.json`
  — the plan makes `python scripts/gen-input-types.py` + committing the JSON a task step.
- **Zero-mint mechanically verified** (see plan-checker note above).
- **HQ-27 Tier-3 has NO source mapped to `radar`** — the plan populates a best-fit
  provisional citation and flags radar for S5-2 operator correction (D-02's designed
  non-blocking D-05 path), NOT a silent choice. Open item for HQ-27 signing.

### Boundary held
`auto_advance=true` in config means `gsd-plan-phase` §15 would auto-launch
`gsd-execute-phase`. I did NOT take it: S1-2 (plan) and S1-3 (execute) are separate
gated ceremony units, and the plan-checker pass must be committed with its evidence
before any execution. Did not flip the operator's persistent `auto_advance` config.

### Clock note
`date -u` reads 2026-09-02T22:xxZ (machine is UTC-3; local 19:xx). Prior firings'
`2026-09-03T00:xxZ` Log labels ran ~2h ahead of true UTC. This firing uses measured
UTC — so its timestamp reads earlier than the prior line. Git commit timestamps are
the authoritative chronology; Log timestamps are human markers only.
