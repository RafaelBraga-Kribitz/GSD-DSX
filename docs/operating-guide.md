# Operating guide

How GSD-DSX and the house-style skills reach a project, how to choose a ceremony
tier, and how to run several phases at once without losing track of them.

Written against GSD Core 1.7.0 and GSD-DSX 2.0.0. Every claim here was checked
against the running system rather than the reference documentation, because the
two disagree in at least one place — see [gsd-tiers.md](gsd-tiers.md).

---

## 1. What is already global, and what is not

This is the single most useful thing to understand, because it decides how much
work adopting a change actually is.

The dsx capability is installed **once** and is visible from every directory on
the machine, including directories that are not projects yet. The house-style
skills and all configuration are **per project**.

```mermaid
flowchart TD
    subgraph GLOBAL["Global — install once, every project sees it"]
        A["~/.gsd/capabilities/dsx<br/>gates, dsx CLI, IT001-IT040 catalogue"]
        B["~/.claude/agents/<br/>6 dsx agents"]
        C["~/.claude/skills/<br/>9 dsx skills"]
    end

    subgraph PROJECT["Per project — must be applied to each one"]
        D[".planning/config.json<br/>agent_skills, workflow flags, tier, dsx toggles"]
        E[".claude/skills/<br/>plain-language, decision-format"]
    end

    F["node install.mjs<br/>run once from the GSD-DSX repo"] --> GLOBAL
    G["scripts/gsd-stamp.ps1 -Project X<br/>run once per project"] --> PROJECT

    GLOBAL --> H["dsx gates fire<br/>dsx.enforce defaults to true"]
    PROJECT --> I["agents write in plain language<br/>and use the decision format"]
```

**Verified:** the `dsx` capability resolves from `warehouse_humanoid_tco`,
`metric_lineage_simulator` and an empty scratch directory. `dsx.enforce` has a
declared default of `true`, so gates fire in a project that has never been
configured.

**A trap worth knowing:** `~/.gsd/defaults.json` looks like a global config, and
it is not. It applies only when a directory has **no** `.planning/` folder. An
existing project always reads its own `.planning/config.json`, so editing the
defaults file changes nothing for work already under way.

---

## 2. Rolling out to a project

One command per project. It copies the two skills, wires them to the three
agents that talk to you, sets the readability flags, and then verifies by
resolving the skills back out rather than trusting that the write succeeded.

```powershell
pwsh scripts/gsd-stamp.ps1 -Project C:\Users\Benutzer1\Dev\warehouse_humanoid_tco -Tier 2
pwsh scripts/gsd-stamp.ps1 -Project . -VerifyOnly
```

```mermaid
flowchart TD
    A["gsd-stamp.ps1 -Project X"] --> B{".planning/ exists?"}
    B -- no --> Z["stop: not a GSD project"]
    B -- yes --> C["copy plain-language + decision-format<br/>into X/.claude/skills/"]
    C --> D["config-set agent_skills.gsd-planner<br/>gsd-executor, gsd-verifier"]
    D --> E["config-set text_mode=true<br/>discuss_mode=assumptions"]
    E --> F{"-Tier given?"}
    F -- yes --> G["apply tier preset"]
    F -- no --> H["leave ceremony as-is"]
    G --> I
    H --> I["VERIFY: gsd-tools agent-skills per agent"]
    I --> J{"every agent resolves<br/>both skills?"}
    J -- yes --> K["done"]
    J -- no --> L["throw, exit 1"]
```

### Why the verify step is not optional

`config-set` accepts a comma-separated skill list, reports `"updated": true`,
and the config file then looks correct on inspection. The resolver treats the
whole string as one path, finds nothing, and the agent silently receives zero
skills. Only the array form works.

```powershell
# WRONG — writes cleanly, resolves to nothing
config-set agent_skills.gsd-planner "skills/a,skills/b"

# RIGHT
config-set agent_skills.gsd-planner '["skills/a","skills/b"]'
```

The general rule this is an instance of: **verify the effect, not the write.** A
command exiting zero proves it wrote something, not that anything reads it.

---

## 3. Choosing a ceremony tier

Full presets and the exact commands are in [gsd-tiers.md](gsd-tiers.md). The
decision itself is short.

```mermaid
flowchart TD
    A["New piece of work"] --> B{"Will anyone<br/>other than me run it?"}
    B -- yes --> T2["Tier 2 — code others run<br/>full ceremony, fine granularity, quality models"]
    B -- no --> C{"Will it be published<br/>or shown to anyone?"}
    C -- yes --> T1["Tier 1 — published artifact<br/>plan check + verifier + dsx gates on, research off"]
    C -- no --> D{"Would I mind<br/>deleting it tomorrow?"}
    D -- no --> T0["Tier 0 — exploratory<br/>gates off, coarse, budget models"]
    D -- yes --> T1
```

The one asymmetry worth remembering: **Tier 1 keeps the dsx gates on.** A
published chart is exactly where a misleading encoding does damage, because
somebody reads it and believes it. Tier 0 turns them off because a throwaway
notebook has no audience to mislead.

```powershell
pwsh scripts/gsd-tier.ps1 -Tier 0    # exploratory
pwsh scripts/gsd-tier.ps1 -Tier 1    # published artifact
pwsh scripts/gsd-tier.ps1 -Tier 2    # code others run
pwsh scripts/gsd-tier.ps1 -Show      # read current values, change nothing
```

---

## 4. The phase loop and where dsx blocks it

Five gates, all blocking, all shelling out to the bundled Python command-line
tool. They are declarative in `capabilities/dsx/capability.json`, so they fire
without anyone remembering to run them.

```mermaid
flowchart LR
    A["/gsd-discuss-phase"] --> B["/gsd-plan-phase"]
    B --> C["/gsd-execute-phase"]
    C --> D["/gsd-verify-work"]
    D --> E["/gsd-ship"]

    B -.->|"plan:pre"| P1["dsx-scope-analysis<br/>writes ANALYSIS-SPEC.yaml"]
    B -.->|"plan:post"| G1["dsx gate plan"]
    C -.->|"execute:post"| G2["dsx gate execute"]
    D -.->|"verify:post"| G3["dsx gate verify<br/>writes DATA-REVIEW.md"]
    E -.->|"ship:pre"| G4["dsx gate ship"]

    G1 --> X{"exit 0?"}
    X -- no --> STOP["phase blocked<br/>findings name the fix"]
    X -- yes --> C
```

A phase with no `ANALYSIS-SPEC.yaml` passes straight through — the gates use
`--allow-missing`. That is what makes it safe to leave enabled in a repository
where only some phases are analytical. Set `dsx.require_spec true` in a project
that is purely analytics.

### The chart gate specifically

```mermaid
flowchart TD
    A["visual declares type + data_input_type"] --> B{"data_input_type known?"}
    B -- "no" --> E1["DSX-VIZ-013 HIGH<br/>lists every valid id"]
    B -- "IT001-IT040" --> C["look up admissible marks<br/>for that exact signature"]
    B -- "family name" --> D["look up admissible marks<br/>for the coarse family"]
    C --> F{"declared type admissible?"}
    D --> F
    F -- yes --> OK["pass"]
    F -- no --> E2["DSX-VIZ-013 HIGH<br/>names the marks that would pass"]
```

Ask the lookup instead of guessing:

```bash
dsx charts IT005 --relationship comparison   # bar, bullet, dot_plot, horizontal_bar
dsx charts --list                            # the whole catalogue
```

---

## 5. Running work in parallel

Two different mechanisms, often confused.

**Worktrees** parallelise *plans inside one phase*. The executor forks an
isolated git worktree per plan in a wave, runs them concurrently, and merges.
This is automatic when `workflow.use_worktrees` is true.

**Workstreams** parallelise *phases against each other*, each with its own state.

```mermaid
flowchart TD
    subgraph WAVE["One phase, wave-based — worktrees"]
        P["PLAN.md files in a wave"] --> W1["worktree 1"]
        P --> W2["worktree 2"]
        P --> W3["worktree 3"]
        W1 --> M["merge back to branch"]
        W2 --> M
        W3 --> M
    end

    subgraph STREAM["Several phases at once — workstreams"]
        S1["workstream A<br/>phase 07"]
        S2["workstream B<br/>phase 08"]
    end

    M --> G["execute:post dsx gate"]
```

### The one setting that silently disables parallelism

Worktrees are forked from `origin/HEAD` by default. If your branch has commits
that `origin/HEAD` does not — which is true of every milestone branch mid-flight
— GSD degrades to sequential execution and prints a one-line warning that is
easy to miss.

This repository already has the fix:

```json
// .claude/settings.local.json
{ "worktree": { "baseRef": "head" } }
```

Apply it to any project where parallel execution matters:

```bash
node ~/.claude/gsd-core/bin/gsd-tools.cjs worktree set-baseref
node ~/.claude/gsd-core/bin/gsd-tools.cjs worktree base-check
```

### Deciding how much to parallelise

```mermaid
flowchart TD
    A["Phase has several independent plans"] --> B{"Can I actually read<br/>3 agent outputs?"}
    B -- yes --> C["use_worktrees true<br/>baseRef head"]
    B -- no --> D["parallelization false<br/>one agent at a time"]
    C --> E{"Plans tiny?"}
    E -- yes --> F["raise inline_plan_threshold<br/>fewer subagent spawns"]
    E -- no --> G["leave at 2"]
```

There is **no** setting that caps concurrent agents at a specific number.
`parallelization` is a switch, not a dial: `true` runs waves, `false` runs one
at a time. `workflow.inline_plan_threshold` is the nearest thing to a dial — it
controls how small a plan has to be before it runs inline instead of spawning a
subagent, which is really a control on how many separate outputs you have to
read.

---

## 6. Propagating a change in GSD-DSX to every project

When the capability changes — new check, new finding code, new catalogue entry —
this is the whole loop. Note that step 3 is *not* needed for capability changes,
only for skill or config changes.

```mermaid
flowchart TD
    A["change in GSD-DSX repo"] --> B["python -m pytest tests/"]
    B --> C["node install.mjs"]
    C --> D["node install.mjs --check"]
    D --> E{"agents 6/6, skills 9/9,<br/>self-test passed?"}
    E -- no --> F["fix before continuing"]
    E -- yes --> G["every project now has the new gates"]
    G --> H{"did skills or config<br/>change too?"}
    H -- no --> I["done"]
    H -- yes --> J["gsd-stamp.ps1 per project"]
    J --> K["gsd-stamp.ps1 -VerifyOnly per project"]
```

The asymmetry is the point: **capability changes are global and instant**, while
**skill and config changes are per project and manual**. That is why the stamp
script exists.

---

## 7. Command reference

| Task | Command |
|---|---|
| Install or upgrade the capability globally | `node install.mjs` |
| Check the install | `node install.mjs --check` |
| Stamp skills and wiring into a project | `pwsh scripts/gsd-stamp.ps1 -Project X` |
| Check a project's wiring only | `pwsh scripts/gsd-stamp.ps1 -Project X -VerifyOnly` |
| Switch ceremony tier | `pwsh scripts/gsd-tier.ps1 -Tier 0\|1\|2` |
| Read current tier values | `pwsh scripts/gsd-tier.ps1 -Show` |
| Permitted charts for a data shape | `dsx charts IT005 --relationship comparison` |
| Whole chart catalogue | `dsx charts --list` |
| Every closed vocabulary | `dsx vocab` |
| Run one gate by hand | `dsx gate plan --phase-dir .planning/phases/07-x` |
| Full audit of a spec | `dsx audit --spec ANALYSIS-SPEC.yaml` |
| Read the decision trail | `dsx explain` |
| Set one config key | `node ~/.claude/gsd-core/bin/gsd-tools.cjs config-set <key> <value>` |
| Read one config key | `node ~/.claude/gsd-core/bin/gsd-tools.cjs config-get <key>` |
| Confirm skills reach an agent | `node ~/.claude/gsd-core/bin/gsd-tools.cjs agent-skills gsd-planner` |
| Fix worktree base for parallelism | `node ~/.claude/gsd-core/bin/gsd-tools.cjs worktree set-baseref` |

`gsd-tools` is not on PATH on this machine, which is why the full path appears
above. Adding `~/.claude/gsd-core/bin` to PATH would shorten every one of them.

---

## 8. Onboarding a brand-new project

```mermaid
flowchart TD
    A["new repository"] --> B["/gsd-new-project"]
    B --> C["gsd-stamp.ps1 -Project . -Tier 2"]
    C --> D{"analytical work?"}
    D -- yes --> E["config-set dsx.require_spec true"]
    D -- no --> F["leave dsx.require_spec false"]
    E --> G["worktree set-baseref"]
    F --> G
    G --> H["/gsd-plan-phase"]
```

For an existing repository, `/gsd-onboard` replaces `/gsd-new-project` and adds
codebase mapping and document ingest first.
