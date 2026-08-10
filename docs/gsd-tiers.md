# Ceremony tiers

Three named configuration presets, so that work whose mistakes cost nothing does
not pay for checks designed for work whose mistakes cost a lot.

Verified against GSD Core version 1.7.0. Every key below was confirmed to exist
by running `config-set` against a scratch copy of the configuration file. There
is no recommended-presets table in the installed documentation, so the tier names
here are local to this project; the configuration key names are GSD Core's own.

## How to switch

`gsd-tools` is not on the system PATH on this machine, so the commands use the
full path to the bundled command-line tool. Set the two variables once per
terminal session.

PowerShell:

```powershell
$GSD  = "$env:USERPROFILE\.claude\gsd-core\bin\gsd-tools.cjs"
$PROJ = "c:\Users\Benutzer1\Dev\AI\gsd-dsx"
node $GSD config-set workflow.research false --cwd $PROJ
```

Or apply a whole tier in one command with the helper script in this repository:

```powershell
pwsh scripts/gsd-tier.ps1 -Tier 0    # exploratory
pwsh scripts/gsd-tier.ps1 -Tier 1    # published artifact
pwsh scripts/gsd-tier.ps1 -Tier 2    # code others run
pwsh scripts/gsd-tier.ps1 -Show      # print current values without changing them
```

The script only calls `config-set`. It writes nothing that you could not write by
hand, and every line it runs is printed as it goes.

## The tiers

| Setting | Tier 0 exploratory | Tier 1 published artifact | Tier 2 code others run |
|---|---|---|---|
| `workflow.research` | `false` | `false` | `true` |
| `workflow.plan_check` | `false` | `true` | `true` |
| `workflow.verifier` | `false` | `true` | `true` |
| `workflow.nyquist_validation` | `false` | `false` | `true` |
| `workflow.code_review` | `false` | `true` | `true` |
| `workflow.code_review_depth` | `quick` | `quick` | `deep` |
| `workflow.security_enforcement` | `false` | `false` | `true` |
| `workflow.tdd_mode` | `false` | `false` | `true` |
| `workflow.pattern_mapper` | `false` | `false` | `true` |
| `workflow.ui_review` | `false` | `true` | `true` |
| `workflow.api_coverage_gate` | `false` | `false` | `true` |
| `workflow.ai_integration_phase` | `false` | `false` | `true` |
| `granularity` | `coarse` | `standard` | `fine` |
| `model_profile` | `budget` | `adaptive` | `quality` |
| `mode` | `yolo` | `yolo` | `interactive` |
| `dsx.enforce` | `false` | `true` | `true` |

### Tier 0, exploratory

Notebooks, chart drafts, one-off analysis, anything you will delete afterwards.

Research off, plan check off, verifier off, coarse granularity, budget model
profile, confirmation gates off. The data-science gates are off too, because a
throwaway notebook has no audience to mislead.

The point of this tier is that a wrong answer costs you the time to notice and
redo it, and nothing else.

### Tier 1, published artifact

Charts, README files, case study pages — anything published but not executed by
other people.

Plan check and verifier on, research off, code review at `light` depth, security
enforcement off. The data-science gates stay **on**: this tier is exactly where a
misleading chart does damage, because someone reads it and believes it.

Note on vocabulary: `quick` is correct, and the installed documentation is not.
`gsd-core/references/planning-config.md` lists the allowed values for
`workflow.code_review_depth` as `light`, `standard`, `deep`. The running code
rejects `light` and accepts `quick`:

```text
Error: Invalid workflow.code_review_depth 'light'. Valid values: quick, standard, deep
```

The real vocabulary is `quick`, `standard`, `deep`. Trust `config-set` over the
reference table when the two disagree.

### Tier 2, code others run

Full ceremony as it was configured on 2026-08-10, plus fine granularity and the
quality model profile.

`mode` returns to `interactive` here, so that confirmation gates actually appear.
The other two tiers leave it on `yolo`, which is how this project was already
configured.

## Concurrent agents: what is actually available

The brief asked for `parallelization.max_concurrent_agents` to be set to `2`.

**That key does not exist in GSD Core 1.7.0.** `config-set` rejects it as an
unknown key, and no concurrency limit of any kind appears in the configuration
schema. There is no way to cap agents at two.

The only real lever is `parallelization`, which is a switch, not a dial:

- `true` — agents run in parallel waves, as many as the phase plan produces.
- `false` — agents run one at a time, sequentially.

This has deliberately been left at its current value of `true` rather than
substituting `false`, because full serialisation is a larger change than the cap
that was asked for, and guessing at your intent is worse than telling you the
control does not exist.

If review bandwidth is the binding constraint, the honest choice is:

```powershell
node $GSD config-set parallelization false --cwd $PROJ
```

A related lever worth knowing about is `workflow.inline_plan_threshold`
(default `2`). Plans with that many tasks or fewer run inline instead of spawning
a subagent. Raising it reduces how many separate agent outputs you have to read,
without turning parallelism off entirely.
