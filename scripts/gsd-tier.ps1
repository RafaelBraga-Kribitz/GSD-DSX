<#
.SYNOPSIS
  Apply one of the three ceremony tiers documented in docs/gsd-tiers.md.

.DESCRIPTION
  Calls `gsd-tools config-set` once per setting and prints each command as it
  runs. Writes nothing you could not write by hand.

.EXAMPLE
  pwsh scripts/gsd-tier.ps1 -Tier 0
  pwsh scripts/gsd-tier.ps1 -Show
#>
[CmdletBinding(DefaultParameterSetName = 'Apply')]
param(
    [Parameter(ParameterSetName = 'Apply', Mandatory)]
    [ValidateSet('0', '1', '2')]
    [string]$Tier,

    [Parameter(ParameterSetName = 'Show', Mandatory)]
    [switch]$Show,

    [string]$GsdTools = "$env:USERPROFILE\.claude\gsd-core\bin\gsd-tools.cjs",
    [string]$Project = (Resolve-Path "$PSScriptRoot\..").Path
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $GsdTools)) {
    throw "gsd-tools not found at $GsdTools. Pass -GsdTools <path> explicitly."
}

# Keys shared by every tier, in the order they are applied.
$Keys = @(
    'workflow.research'
    'workflow.plan_check'
    'workflow.verifier'
    'workflow.nyquist_validation'
    'workflow.code_review'
    'workflow.code_review_depth'
    'workflow.security_enforcement'
    'workflow.tdd_mode'
    'workflow.pattern_mapper'
    'workflow.ui_review'
    'workflow.api_coverage_gate'
    'workflow.ai_integration_phase'
    'granularity'
    'model_profile'
    'mode'
    'dsx.enforce'
)

$Tiers = @{
    '0' = @{
        'workflow.research'              = 'false'
        'workflow.plan_check'            = 'false'
        'workflow.verifier'              = 'false'
        'workflow.nyquist_validation'    = 'false'
        'workflow.code_review'           = 'false'
        'workflow.code_review_depth'     = 'quick'
        'workflow.security_enforcement'  = 'false'
        'workflow.tdd_mode'              = 'false'
        'workflow.pattern_mapper'        = 'false'
        'workflow.ui_review'             = 'false'
        'workflow.api_coverage_gate'     = 'false'
        'workflow.ai_integration_phase'  = 'false'
        'granularity'                    = 'coarse'
        'model_profile'                  = 'budget'
        'mode'                           = 'yolo'
        'dsx.enforce'                    = 'false'
    }
    '1' = @{
        'workflow.research'              = 'false'
        'workflow.plan_check'            = 'true'
        'workflow.verifier'              = 'true'
        'workflow.nyquist_validation'    = 'false'
        'workflow.code_review'           = 'true'
        'workflow.code_review_depth'     = 'quick'
        'workflow.security_enforcement'  = 'false'
        'workflow.tdd_mode'              = 'false'
        'workflow.pattern_mapper'        = 'false'
        'workflow.ui_review'             = 'true'
        'workflow.api_coverage_gate'     = 'false'
        'workflow.ai_integration_phase'  = 'false'
        'granularity'                    = 'standard'
        'model_profile'                  = 'adaptive'
        'mode'                           = 'yolo'
        'dsx.enforce'                    = 'true'
    }
    '2' = @{
        'workflow.research'              = 'true'
        'workflow.plan_check'            = 'true'
        'workflow.verifier'              = 'true'
        'workflow.nyquist_validation'    = 'true'
        'workflow.code_review'           = 'true'
        'workflow.code_review_depth'     = 'deep'
        'workflow.security_enforcement'  = 'true'
        'workflow.tdd_mode'              = 'true'
        'workflow.pattern_mapper'        = 'true'
        'workflow.ui_review'             = 'true'
        'workflow.api_coverage_gate'     = 'true'
        'workflow.ai_integration_phase'  = 'true'
        'granularity'                    = 'fine'
        'model_profile'                  = 'quality'
        'mode'                           = 'interactive'
        'dsx.enforce'                    = 'true'
    }
}

if ($Show) {
    Write-Output "Current values in $Project\.planning\config.json"
    foreach ($key in $Keys) {
        $value = & node $GsdTools config-get $key --cwd $Project --raw 2>$null
        if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($value)) { $value = '(unset)' }
        '{0,-34} {1}' -f $key, $value.Trim()
    }
    exit 0
}

$settings = $Tiers[$Tier]
Write-Output "Applying tier $Tier to $Project"

foreach ($key in $Keys) {
    $value = $settings[$key]
    Write-Output "  config-set $key $value"
    & node $GsdTools config-set $key $value --cwd $Project | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Failed to set $key" }
}

Write-Output "Tier $Tier applied. Run with -Show to read the values back."
