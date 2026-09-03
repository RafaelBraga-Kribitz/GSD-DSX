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

## S2-2 — Phase 22 plan (2026-09-03)

Planned via `gsd-plan-phase 22`, driven by the orchestrator following the workflow
faithfully — researcher, planner, and plan-checker each spawned as a **separate
Agent** (roles never collapsed inline, per the workflow's hard rule that independent
agent contexts are required for a meaningful plan-checker gate).

**Pipeline (all committed):**
- `gsd-phase-researcher` (sonnet) → `22-RESEARCH.md`, committed `0ba32d1`. Surfaced
  three gaps CONTEXT does not name (all verified by running the live tests, not
  inferred): (1) the ten new Wilke uncertainty marks need a `CHART_CAPABILITIES`
  home or Phase 21's `test_every_mark_has_a_capability_home` invariant goes red;
  (2) `tests/test_finding_catalogue_invariant.py` hard-codes `_EXPECTED_TOTAL=275`
  and an exact `_MINTED_CODES` set — this file *is* the additive-mint proof;
  (3) `DSX-VIZ-*` is absent from `gen-finding-catalogue.py`'s `_D05_ALLOWLIST_PREFIXES`,
  so the new code's D-05 enforcement needs an exact-string add to `_D05_ALLOWLIST_CODES`.
  Also flagged: `chart-selection.md`'s "Encoding accuracy" line still ships the OLD
  false 7-item strict order (correct it to D-1's 6-rank-with-ties); `dsx-visualize`
  SKILL enumerates 10 relationships (ripple for the 11th key); recommend dropping
  Abela 2008 / Few's Graph Selection Matrix (never in HQ-27).
- Orchestrator wrote the Nyquist `22-VALIDATION.md` seed (§5.5), committed `684530e`.
- `gsd-planner` (opus) → `22-01..04-PLAN.md` (4 plans / 4 waves), committed `81ea14c`
  (see BRANCH REMEDIATION below — the commit was salvaged onto the canonical branch).
- `gsd-plan-checker` (**opus** — brief §3 override of the adaptive profile's haiku
  default, exactly as S1-2 did) → `## VERIFICATION PASSED`, all 7 focus items green.

**Plans (wave order forced by shared ownership of `dsx/checks/viz.py` + real deps):**
- 22-01 (wave 1, tdd; REQ-P22-02,-03): 11th `RELATIONSHIP_CHARTS["uncertainty"]` key
  + ten §5.6 marks; homes them into `CHART_CAPABILITIES["interval-range"]` (gap 1);
  adds `gauge`/`word_cloud` refusal records + swaps `radar`→Duan 2023; `facet_by`
  orthogonal → routes to DSX-SMELL-007. Mints 0 codes (275→275 at this wave).
- 22-02 (wave 2, tdd; REQ-P22-05): mints `DSX-VIZ-071` (`_check_uncertainty_vocabulary`),
  allowlists by exact string (gap 3), bumps invariant 275→276 + `_MINTED_CODES` (gap 2);
  records the loud **DSX-VIZ-072-not-minted** decision.
- 22-03 (wave 3, execute; REQ-P22-01,-05): `references/chart-catalog.md` (~80 rows,
  three axes + citation, fenced-JSON payload) split acquisition/authoring/verification;
  new conformance + perceptual-tie-break repo-integrity tests.
- 22-04 (wave 4, execute; REQ-P22-04): 5-layer heuristic route-and-cite into the two
  existing taxonomy files + skill ripple (10→11 relationships); corrects the superseded
  perceptual line; drops Abela 2008 / Few's Graph Selection Matrix.

**DSX-VIZ-072 not minted (persona-round decision, GA-3 contingent reservation, HQ-30
veto window).** GA-3 reserved 072 only "if a second distinct uncertainty check is
warranted (e.g. paradigm-mismatch)." The planner found it is not: several §5.6 marks
(error bars, graded error bars) legitimately render either a frequentist confidence
interval or a Bayesian credible interval, so no mark→paradigm partition exists to gate
against; REQ-P22-02's "D-12a-clean" is satisfied by the 11th-key structure by
construction. Matches the research recommendation. Phase 22 blocking-code footprint =
exactly one; set-identity diff proves 275→276, additive-only.

**Plan-checker advisory (non-blocking, no revision required):** 2 LOW warnings —
(1) 22-02 lacks a cosmetic `<artifacts_this_phase_produces>` section (coverage NOT
lost: 22-01's canonical index enumerates 22-02's artifacts and 22-02 lists them in
`must_haves.artifacts` + a loud decision block); (2) chained `&&` verify commands
assume Bash/pwsh7 — executor should run them through the Bash tool, not Windows
PowerShell 5.1. No BLOCKERs.

**BRANCH REMEDIATION (loud — the honesty this project's standard demands).** Mid-plan,
the `gsd-planner` subagent ran `git checkout -b gsd/v2.4-visual-excellence` (no `.0`)
and committed the four plans (`81ea14c`) on that new branch — a direct violation of
plan-phase §0's Git Branch Invariant ("do not create, rename, or switch git branches
during plan-phase"). Its own return then confidently asserted the canonical
`.0` branch name "was inaccurate" — the claim was itself the error. The **reflog was
the fact** (`HEAD@{1}: checkout: moving from gsd/v2.4.0-visual-excellence to
gsd/v2.4-visual-excellence`). The canonical branch is unambiguously
`gsd/v2.4.0-visual-excellence` (with `.0`): it is what `origin` tracks, what
LOOP-BRIEF/STATE/ledger all name, and what session-start reported. Because `81ea14c`
is a **linear descendant** of the canonical branch's tip (`684530e`), the orchestrator
`git checkout gsd/v2.4.0-visual-excellence` → `git merge --ff-only` (Updating
684530e..81ea14c) → `git branch -d gsd/v2.4-visual-excellence` (the safe `-d` confirmed
it was fully merged — no commit lost). Stale `gsd/*` branch count restored to five (the
prior-milestone set), NOT a new sixth — which matters because the ship auto-detect
picks the alphabetically-first `gsd/*`. This is exactly the class of subagent error the
brief's "verify against the repo, not the claim" rule exists to catch.
