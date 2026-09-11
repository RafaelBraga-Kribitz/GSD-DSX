# GSD Core: known defects and gaps this project works around

The ceremony that builds this project runs on GSD Core (the installed copy at
`~/.claude/gsd-core`, `VERSION` 1.7.0). Over four milestones the loop hit a set of
framework defects, each recorded at the time in the milestone's human queue as a
"standing framework note" and worked around locally. This file is the one place
they live now, so the next milestone does not rediscover them and so they can be
reported upstream in one go. Nothing here patches the installed copy: the
workarounds are all on this repository's side.

Every "still present" verdict below was checked against the installed 1.7.0 code on
2026-09-11, by reading the line cited. "Observed" means the behaviour was seen and
recorded but the responsible code was not traced.

## Defects

| # | Where | What goes wrong | Found | Status in 1.7.0 (2026-09-11) | This project's workaround |
|---|---|---|---|---|---|
| 1 | `bin/lib/uat.cjs:78` | `audit-uat` discovers verification files with `f.includes('-VERIFICATION')`, so a bare `VERIFICATION.md` is never read. | v2.0.0 | Still present (line 78). | Phases are named `NN-VERIFICATION.md`; the close hand-checks every verification file. |
| 2 | `bin/lib/uat.cjs:80-81, 294` | A verification file is only reported when its frontmatter `status` is `human_needed` or `gaps_found`; a file carrying `verdict: PASSED` and no `status:` key resolves to `unknown` and is silently dropped, so "all clear" can mean "not read". | v2.3 S5-1 | Still present (lines 80-81; `parseVerificationItems` parses only `human_needed`). | Never accept the CLI's all-clear at the ship gate; read each file. |
| 3 | `bin/lib/decisions.cjs:35` | The plan-phase decision-coverage gate parses `- **D-NN:** …` (colon inside the bold); this project's discuss rounds write `- **D-06 range pre-allocation** — …`, which matches nothing, so the gate reports `total:0, reason:"could-not-parse"` — a parser mismatch that reads as an uncovered decision. | v2.3 S1-2 | Still present (`bulletColonRe`). | The plan-checker's Dimension 7 (context compliance) is treated as the real coverage check; a could-not-parse result is not a gap. |
| 4 | `workflows/complete-milestone.md:646` | `handle_branches` selects the milestone branch with `git branch --list "gsd/*" … \| head -1` — the alphabetically first `gsd/*` branch, which was always a stale one here. | v2.2, v2.3, v2.4 ship | Still present (line 646). | Ship by explicit branch name (`git merge --no-ff <branch>`), rehearsed on a throwaway branch; stale branches were deleted 2026-09-11. |
| 5 | `bin/lib/commands.cjs:842-857` (`query commit`) | The subagent-facing commit command creates and switches to whatever branch name it is given (`git checkout -b <branch>`), with no check against the canonical branch, and reports the name it was given. A subagent that mistypes the branch (v2.4: `gsd/v2.4-visual-excellence`, no `.0`) lands its commit on a new stray branch while its own return claims success on the canonical one. Confirmed three times in v2.4. | v2.4 | Still present. | `scripts/gsd-reconcile-branch.ps1` folds stray commits back by ancestry; the headless wrapper runs it after every firing. |
| 6 | `references/planning-config.md:277` | Documents `workflow.code_review_depth` as `light` / `standard` / `deep`; the code rejects `light` and accepts `quick` (`config-set` error text: "Valid values: quick, standard, deep"). | v2.4 | Still present (docs line 277). | `docs/gsd-tiers.md` uses `quick`; trust `config-set` over the reference table. |
| 7 | `workflows/complete-milestone.md` (STATE and MILESTONES rewrite) | The close's accomplishment extraction produced fragments at four consecutive closes, and its STATE rewrite regressed the phase/plan counters at the v2.6 close. | v2.3–v2.6 closes | Observed. | Generated records are hand-corrected at every close (recorded in `.planning/STATE.md`). |
| 8 | `gsd-tools audit-open` (`bin/lib/audit.cjs`) | Reports a phase CONTEXT's "open questions" as open forever, because it matches the bold bullet markers and those bullets are never rewritten once resolved. | v2.4, v2.6 close | Observed. | Accepted at close with the reason recorded in `.planning/STATE.md` Deferred Items. |
| 9 | `init.manager` (`bin/lib/init.cjs:146`) | `verification_status` can read `missing` for a phase whose verification file exists and passed. | v2.3, v2.4 close | Observed. | Read the file before treating it as a gap. |
| 10 | `workflows/pr-branch.md` | Its per-commit cherry-pick chain hit recurring modify/delete conflicts on a 707-commit ceremony branch and was abandoned mid-run. | v2.0.0 | Observed. | Ship by direct three-way merge. |

Closed since it was recorded: the v2.0.0 note that `parseVerificationItems` only
recognised a level-2 `## Human Verification` heading while the template wrote a
level-3 `### Human Verification Required`. In 1.7.0 the template writes
`## Human Verification Required` (`templates/verification-report.md:82`) and the
parser matches `/^human\s+verification/i` at level 2 (`uat.cjs:296`), so the two
agree again. Defect 2 is what remains of that note.

## Gaps (not defects)

- There is no way to cap concurrent agents: `parallelization` is a boolean
  (`bin/lib/config-loader.cjs:549-555`) and no `max_concurrent_agents` key exists
  in the schema. See `docs/gsd-tiers.md`.

## Reporting upstream

The installed copy carries no repository pointer (no `package.json`, no URL in
`bin/gsd-tools.cjs` or the references), so the upstream location is the
operator's to supply. Each row above is written to be filed as-is: file, line,
symptom, version, and the date of the last check.
