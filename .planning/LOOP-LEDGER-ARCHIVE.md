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
