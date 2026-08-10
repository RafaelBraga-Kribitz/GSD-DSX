<#
.SYNOPSIS
  Stamp the house-style skills and their wiring into a GSD project.

.DESCRIPTION
  The dsx capability itself is global — installed once at ~/.gsd/capabilities/dsx
  and visible to every project. These two things are not, and have to be applied
  per project:

    1. the decision-format and plain-language skill files
    2. the agent_skills wiring that points three agents at them

  This script does both, then verifies by resolving the skills back out of
  gsd-tools rather than trusting that the write succeeded. A comma-separated
  agent_skills value is accepted by config-set and then silently resolves to
  nothing, so counting resolved paths is the only check that means anything.

.EXAMPLE
  pwsh scripts/gsd-stamp.ps1 -Project C:\Users\Benutzer1\Dev\warehouse_humanoid_tco
  pwsh scripts/gsd-stamp.ps1 -Project . -Tier 1
  pwsh scripts/gsd-stamp.ps1 -Project . -VerifyOnly
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$Project,

    # Canonical source of the two skills. The design-system template is the
    # thing new projects derive from, so it is the stamping source.
    [string]$SkillSource = "C:\Users\Benutzer1\Dev\braga-design-system-template\skills",

    # Where the skills land inside the target. .claude/skills never collides
    # with a capability's own skills/ directory.
    [string]$SkillDir = ".claude/skills",

    [ValidateSet('0', '1', '2')]
    [string]$Tier,

    [switch]$VerifyOnly,

    [string]$GsdTools = "$env:USERPROFILE\.claude\gsd-core\bin\gsd-tools.cjs"
)

$ErrorActionPreference = 'Stop'

$SKILLS = @('plain-language', 'decision-format')
$AGENTS = @('gsd-planner', 'gsd-executor', 'gsd-verifier')

$projectPath = (Resolve-Path $Project).Path
if (-not (Test-Path (Join-Path $projectPath '.planning'))) {
    throw "$projectPath has no .planning/ directory — not a GSD project."
}
if (-not (Test-Path $GsdTools)) {
    throw "gsd-tools not found at $GsdTools."
}

# Returns the number of agents that did NOT resolve every skill. Status lines go
# to the host, never to the pipeline: a function that emits strings *and* a
# boolean returns an array, and a non-empty array is always truthy — so the
# caller's `if (-not $result)` would never fire and the check could not fail.
function Get-WiringFailureCount {
    param([string]$Path)
    $failures = 0
    foreach ($agent in $AGENTS) {
        $out = & node $GsdTools agent-skills $agent --cwd $Path 2>$null
        $resolved = @($out | Select-String -Pattern '^\s*-\s+@').Count
        if ($resolved -ne $SKILLS.Count) { $failures++ }
        $status = if ($resolved -eq $SKILLS.Count) { 'OK  ' } else { 'FAIL' }
        Write-Host ('  {0} {1,-14} {2}/{3} skills resolved' -f $status, $agent, $resolved, $SKILLS.Count)
    }
    return $failures
}

if ($VerifyOnly) {
    Write-Output "Verifying $projectPath"
    $failures = Get-WiringFailureCount -Path $projectPath
    if ($failures -gt 0) { throw "Verification failed — $failures agent(s) resolve fewer skills than configured." }
    Write-Output 'All agents resolve every skill.'
    exit 0
}

Write-Output "Stamping $projectPath"

# 1. Skill files
$targetSkillRoot = Join-Path $projectPath $SkillDir
New-Item -ItemType Directory -Force -Path $targetSkillRoot | Out-Null
foreach ($skill in $SKILLS) {
    $src = Join-Path $SkillSource "$skill\SKILL.md"
    if (-not (Test-Path $src)) { throw "canonical skill missing: $src" }
    $dst = Join-Path $targetSkillRoot $skill
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Copy-Item $src (Join-Path $dst 'SKILL.md') -Force
    Write-Output "  copied $skill"
}

# 2. Wiring. JSON array — a comma-separated string resolves to nothing.
$value = ($SKILLS | ForEach-Object { '"{0}/{1}"' -f $SkillDir, $_ }) -join ','
$value = "[$value]"
foreach ($agent in $AGENTS) {
    & node $GsdTools config-set "agent_skills.$agent" $value --cwd $projectPath | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "failed to wire $agent" }
    Write-Output "  wired $agent"
}

# 3. Readability defaults
& node $GsdTools config-set workflow.text_mode true --cwd $projectPath | Out-Null
& node $GsdTools config-set workflow.discuss_mode assumptions --cwd $projectPath | Out-Null
Write-Output '  set text_mode=true, discuss_mode=assumptions'

# 4. Optional tier
if ($Tier) {
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'gsd-tier.ps1') -Tier $Tier -Project $projectPath | Out-Null
    Write-Output "  applied tier $Tier"
}

# 5. Verify the effect, not the write.
Write-Output 'Verifying:'
$failures = Get-WiringFailureCount -Path $projectPath
if ($failures -gt 0) { throw "Stamp wrote config but $failures agent(s) do not resolve their skills." }
Write-Output "Done. $projectPath is stamped and verified."
