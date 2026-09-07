<#
.SYNOPSIS
  Recovers commits a GSD subagent's `gsd-tools query commit` accidentally left on
  a stray branch instead of the canonical branch, and folds them back in.

.DESCRIPTION
  Known gsd-core defect, documented in HUMAN-QUEUE.md's "Standing framework
  notes": a `gsd-*` subagent committing via `gsd-tools query commit` can create
  and switch to a stray branch mid-run and land the commit there instead of the
  canonical branch, while its own return value confidently misreports success on
  the canonical branch. Confirmed three times in v2.4 alone. This script is the
  standing note's documented manual-reconciliation rule, automated:

    1. Find every local branch whose tip descends from BaselineRef (the
       canonical branch's own tip before the run that may have gone wrong) and
       is not the canonical branch itself. Ancestry, not naming, is what tells
       a stray branch created by THIS run apart from the growing pile of
       genuinely stale branches left over from prior milestones
       (v1.1.0-milestone, v2.0.0-dsx-validity-frame, ...) -- those diverged
       long before BaselineRef and never satisfy the ancestry check, so they
       are never touched.
    2. For each stray found: verify canonical's current tip is still an
       ancestor of the stray (no divergence -- a real conflict is left for a
       human, never force-merged), check out canonical if not already there,
       fast-forward-only merge the stray in (no commit lost, no merge commit
       created), delete the now-fully-merged stray branch, push.
    3. If a stray fails the ancestry check, or the working tree is dirty, or
       canonical cannot be safely checked out: stop and report that one --
       never guess, never force.

  Safe to run at any time, by hand or from the ceremony wrapper. Running it
  when nothing went wrong is a silent no-op (exit 0, "nothing to do").

.PARAMETER Branch
  The canonical branch. Required.

.PARAMETER BaselineRef
  A ref recorded before the run that may have gone wrong -- typically the
  canonical branch's own commit hash, captured right before invoking a
  subagent. Defaults to origin/<Branch> (the last known-good pushed state),
  which is the right default for a standalone, by-hand invocation.

.PARAMETER NoPush
  Reconcile and merge locally but do not push. Default is to push, matching
  the ceremony wrapper's own push-after-every-step discipline.

.PARAMETER Repo
  Working directory. Defaults to the current directory.

.EXAMPLE
  pwsh scripts/gsd-reconcile-branch.ps1 -Branch gsd/v2.6.0-exploration-depth
  # by hand, after any interactive /gsd-execute-phase or /gsd-plan-phase run
  # that spawned subagents -- checks against the last pushed state.
#>

param(
  [Parameter(Mandatory = $true)] [string]$Branch,
  [string]$BaselineRef,
  [switch]$NoPush,
  [string]$Repo = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'
Set-Location $Repo

function Say($msg) { Write-Output "[reconcile] $msg" }

if (-not $BaselineRef) {
  git fetch origin --quiet 2>&1 | Out-Null
  $BaselineRef = "origin/$Branch"
}

try {
  $baselineTip = (git rev-parse $BaselineRef 2>&1 | Out-String).Trim()
} catch {
  $baselineTip = $null
}
if ($LASTEXITCODE -ne 0 -or -not $baselineTip) {
  Say "ABORT: could not resolve BaselineRef '$BaselineRef'. $baselineTip"
  exit 2
}

$status = (git status --porcelain)
if ($status) {
  Say "ABORT: working tree is not clean -- not touching any branch until this is resolved by hand:"
  $status -split "`n" | ForEach-Object { Say "  $_" }
  exit 2
}

# Every local branch whose tip strictly descends from the baseline. Ancestry,
# not name, is the filter -- it naturally excludes branches that diverged
# before $baselineTip ever existed, with no hardcoded exclusion list to keep
# up to date as new milestones come and go.
$allBranches = (git for-each-ref --format='%(refname:short)' refs/heads/) -split "`n" | Where-Object { $_ }
$strays = @()
foreach ($b in $allBranches) {
  if ($b -eq $Branch) { continue }
  $tip = (git rev-parse $b | Out-String).Trim()
  if ($tip -eq $baselineTip) { continue }
  git merge-base --is-ancestor $baselineTip $b 2>&1 | Out-Null
  if ($LASTEXITCODE -eq 0) { $strays += $b }
}

if ($strays.Count -eq 0) {
  Say "clean -- no stray branches descending from $BaselineRef ($baselineTip). Nothing to do."
  exit 0
}

Say "found $($strays.Count) stray branch(es) descending from baseline: $($strays -join ', ')"

$currentBranch = (git branch --show-current | Out-String).Trim()
if ($currentBranch -ne $Branch) {
  Say "HEAD is on '$currentBranch', not canonical '$Branch' -- checking out canonical first."
  git checkout $Branch 2>&1 | ForEach-Object { Say $_ }
  if ($LASTEXITCODE -ne 0) {
    Say "ABORT: could not check out '$Branch'. Stray branch(es) left untouched: $($strays -join ', ')"
    exit 2
  }
}

$recovered = 0
foreach ($stray in $strays) {
  $canonicalTip = (git rev-parse $Branch | Out-String).Trim()
  git merge-base --is-ancestor $canonicalTip $stray 2>&1 | Out-Null
  if ($LASTEXITCODE -ne 0) {
    Say "SKIP '$stray': diverged from '$Branch' (not a clean fast-forward) -- a human must reconcile this one by hand. Branch left in place."
    continue
  }
  Say "merging '$stray' into '$Branch' (fast-forward only)..."
  $mergeOut = git merge --ff-only $stray 2>&1 | Out-String
  if ($LASTEXITCODE -ne 0) {
    Say "SKIP '$stray': fast-forward merge failed unexpectedly: $($mergeOut.Trim())"
    continue
  }
  Say $mergeOut.Trim()
  git branch -d $stray 2>&1 | ForEach-Object { Say $_ }
  Say "recovered '$stray' -> '$Branch'; stray branch deleted."
  $recovered += 1
}

if ($recovered -gt 0 -and -not $NoPush) {
  Say "pushing '$Branch'..."
  git push origin $Branch 2>&1 | ForEach-Object { Say $_ }
}

if ($recovered -lt $strays.Count) {
  Say "$($strays.Count - $recovered) stray branch(es) left unresolved -- see SKIP lines above."
  exit 1
}
exit 0
