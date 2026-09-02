# LOOP-LEDGER-ARCHIVE — v2.3 Test Catalog

Long gate evidence and retired Log entries for `LOOP-LEDGER.md`. The active
ledger keeps one concise line per unit; the full evidence lands here under a
`## <unit-id>` heading.

## S0-1 — GSD state points at v2.3

**Gate: command output pasted.** Verified 2026-08-29 (firing after milestone-open).

STATE.md frontmatter:
```
milestone: v2.3
milestone_name: Test Catalog
status: executing
current_phase: 17
current_phase_name: foundation-repairs-and-spec-vocabulary
progress:
  total_phases: 4
  completed_phases: 0
  total_plans: 0
  completed_plans: 0
  percent: 0
```

`node ~/.claude/gsd-core/bin/gsd-tools.cjs query init.milestone-op` (exit 0):
```json
{
  "milestone_version": "v2.3",
  "milestone_name": "Test Catalog",
  "milestone_slug": "test-catalog",
  "phase_count": 4,
  "completed_phases": 0,
  "all_phases_complete": false,
  "archive_count": 0,
  "project_exists": true,
  "roadmap_exists": true,
  "state_exists": true,
  "phases_dir_exists": true,
  "agents_installed": true,
  "missing_agents": []
}
```

`.planning/phases/` contents (empty apart from `.gitkeep` — v2.2 dirs archived):
```
.gitkeep
```

All three conditions met: frontmatter (v2.3 / phase 17 / 0/4) ✓; milestone-op
resolves (4 phases, 0 complete) ✓; phases dir empty ✓.

Note for later firings: `gsd-tools` is not on PATH in the Bash tool; invoke it as
`node ~/.claude/gsd-core/bin/gsd-tools.cjs <args>`.

## Retired Log entries (trimmed from LOOP-LEDGER.md 2026-09-02 at S3-1, brief §5 hot-path lean)

2026-08-29T22:40Z | S0-3 | PASS — Phase 18 D-05 citation evidence pack filed to HUMAN-QUEUE as HQ-16 (non-blocking; NOT signed — D-05 is a human read). 11 citations grouped into 6 sets keyed to the granularity ruling (read-per-CODE): A Fisher 1921 (Pearson Fisher-z CI); B Cohen 1960/1968 + Fleiss 1971 + Hayes-Krippendorff 2007; C Shrout-Fleiss 1979 + McGraw-Wong 1996 (ICC triple); D Bland-Altman 1986; E Feinstein-Cicchetti 1990 (kappa companion gate); F Landis-Koch 1977 + Koo-Li 2016 (bands=conventions). All 11 bibliographic locators corroborated across ≥2 independent sources (venue/vol/pages/DOI-or-PMID). Loop caught: Krippendorff worked value = α 0.743 (0.734 in the textbook is a known typo) — the one load-bearing numeric-fixture read; Landis-Koch has TWO 1977 Biometrics papers, bands are in 33(1):159-174 not 33(2):363-374; McGraw-Wong 1996 has a published erratum; Koo-Li band VALUES not confirmed by search (candidate-only). Per brief §5, any fixture/band unconfirmed at source ships catalog-only/convention-labelled. Next = S0-4 (Phase 19 pack → HQ-17). | HUMAN-QUEUE.md `### HQ-16`
2026-08-29T22:10Z | S0-2 | PASS — inherited scope re-verified against live tree; `.planning/v2.3-SCOPE-RECHECK.md` written. All 5 load-bearing premises CONFIRMED at locators: fisher_exact fallback at stats.py:65; boschloo_exact absent from NONPARAMETRIC_TESTS (stats.py:23-26); doc side still names Boschloo (test-selection.md:10 + [^1] Lydersen-Fagerland-Laake 2009) — divergence genuinely live; QUESTION_TYPES closed 5-key (spec.py:22-28) + estimand_kind absent everywhere; time_to_event fallthrough unconditional (stats.py:128-129). Catalogue RE-MEASURED = 260 codes (matches checked-in finding-codes.md; = REQ-P17-05 baseline). All 22 reqs still-valid, none satisfied/contradicted — execution, not re-scoping. Next = S0-3. | .planning/v2.3-SCOPE-RECHECK.md
2026-08-29T22:00Z | S0-1 | PASS — GSD state points at v2.3: STATE.md frontmatter milestone v2.3 / current_phase 17 / progress 0/4; `node gsd-tools.cjs query init.milestone-op` resolves (phase_count 4, completed_phases 0, all_phases_complete false, exit 0); .planning/phases/ empty (only .gitkeep, v2.2 dirs archived). Note: gsd-tools not on Bash PATH — invoke via `node ~/.claude/gsd-core/bin/gsd-tools.cjs`. Next = S0-2. | LOOP-LEDGER-ARCHIVE.md `## S0-1`
2026-08-29T21:30Z | milestone-open | v2.3 opened by operator direction in an interactive session: scope researched (6-agent workflow: 2 repo mappers, 3 domain researchers, 1 adversarial critic — journal preserved), .planning/research/V2.3-V2.4-SCOPE.md + REQUIREMENTS.md (REQ-P17-01..P20-04) + ROADMAP.md (Phases 17-20 active, 21-24 queued) written; STATE.md repointed (v2.3, phase 17, 0/4); v2.2 loop artifacts archived to .planning/milestones/v2.2-LOOP-*, v2.2-HUMAN-QUEUE.md; this ledger + LOOP-BRIEF + HUMAN-QUEUE rewritten for v2.3; branch gsd/v2.3.0-test-catalog created from main; firing script repointed + usage-limit backoff added (weekly reset Wednesday 13:00 UTC = 10:00 São Paulo; 5h-window = 60-min hold). Operator directive of record: token limits WILL hit this week — firings log one line and stop on limit errors, the wrapper owns pacing and self-resumes. Next = S0-1. | .planning/research/V2.3-V2.4-SCOPE.md; scripts/run-ceremony-firing.ps1
