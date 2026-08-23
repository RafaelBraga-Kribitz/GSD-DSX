<#
.SYNOPSIS
  One firing of the v2.0.0 completion ceremony.

.DESCRIPTION
  Launches a FRESH headless Claude Code process against the repo. Each firing is a
  brand-new process with an empty context window -- that is the whole point: it is
  what stops a 10-day ceremony from degrading inside one ever-growing conversation.
  All continuity lives in git-committed files (.planning/LOOP-BRIEF.md,
  LOOP-LEDGER.md, HUMAN-QUEUE.md), never in conversation memory.

  Registered as a Scheduled Task to fire every 4 hours. Safe to run by hand too.

.NOTES
  Overlap guard: a lock file prevents a second firing starting while one is running.
  Logs: .planning/loop-logs/ (gitignored).
#>

$ErrorActionPreference = 'Stop'

$Repo   = 'C:\Users\Benutzer1\Dev\AI\gsd-dsx'
$Branch = 'gsd/v2.0.0-dsx-validity-frame'
$LogDir = Join-Path $Repo '.planning\loop-logs'
$Lock   = Join-Path $LogDir '.firing.lock'
$Stamp  = (Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss')
$Log    = Join-Path $LogDir "firing-$Stamp.log"

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

function Write-Log($msg) {
  $line = "[{0}Z] {1}" -f (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss'), $msg
  Write-Output $line
  Add-Content -Path $Log -Value $line
}

# --- Overlap guard -----------------------------------------------------------
# A firing may legitimately run for a long time (a full gsd-execute-phase), so the
# guard must tell "still working" apart from "died without cleaning up".
#
# Liveness is decided by process id, not by elapsed time. An interrupted firing
# (Ctrl+C, machine sleep, task timeout) leaves the lock behind; a purely
# time-based guard would then skip every firing until the age threshold passed,
# silently costing a scheduled run. Observed for real on the first manual firing:
# the work committed and pushed fine, but the wrapper never reached its cleanup.
# The age check is kept only as a backstop for a recycled process id.
if (Test-Path $Lock) {
  $holder = (Get-Content $Lock -Raw -ErrorAction SilentlyContinue).Trim()
  $holderPid = ($holder -split '\s+')[0] -as [int]
  $age = (Get-Date) - (Get-Item $Lock).LastWriteTime

  $alive = $false
  if ($holderPid) {
    $proc = Get-Process -Id $holderPid -ErrorAction SilentlyContinue
    # A recycled id belonging to some unrelated program must not count as alive.
    if ($proc -and $proc.Name -match '^(pwsh|powershell)$' -and $age.TotalHours -lt 4) {
      $alive = $true
    }
  }

  if ($alive) {
    Write-Log "SKIP: firing (pid $holderPid) started $([int]$age.TotalMinutes) min ago is still running. Exiting."
    exit 0
  }
  Write-Log "Clearing orphaned lock (pid $holderPid no longer running, $([int]$age.TotalMinutes) min old)."
  Remove-Item $Lock -Force
}
Set-Content -Path $Lock -Value "$PID $Stamp"

try {
  Set-Location $Repo

  # --- Branch guard ----------------------------------------------------------
  # Never force a checkout: this is the user's live working tree. If it is not on
  # the ceremony branch, something unexpected is happening -- stop rather than guess.
  $current = (git branch --show-current).Trim()
  if ($current -ne $Branch) {
    Write-Log "ABORT: expected branch '$Branch' but found '$current'. Not touching the working tree."
    exit 1
  }
  Write-Log "Branch OK: $current"

  git fetch origin --quiet
  git merge --ff-only "origin/$Branch" 2>&1 | Out-String | ForEach-Object { if ($_.Trim()) { Write-Log $_.Trim() } }

  # --- The firing prompt -----------------------------------------------------
  # Deliberately short. LOOP-BRIEF.md is the real contract and is re-read every
  # firing; duplicating its rules here would let the two drift apart.
  $prompt = @'
You are ONE firing of the recurring v2.0.0 completion ceremony for this repository.
You are a fresh process with an EMPTY context window and NO memory of any previous
firing. Everything you need to know is on disk.

1. Read, in full and in this order: .planning/LOOP-BRIEF.md, then
   .planning/LOOP-LEDGER.md, then .planning/HUMAN-QUEUE.md. LOOP-BRIEF.md is your
   complete operating contract -- its Section 0 describes the execution model you
   are inside of right now. Follow it exactly: cadence, model/effort routing,
   the expert-persona decision protocol, the non-negotiable ground rules, the
   stage plan, and the reporting rules all bind this firing.

2. Reconcile claims against reality before trusting the ledger: run
   `git log --oneline -15` and `git status`. The ledger is a claim; the repo is
   the fact. If they disagree, correct the ledger first.

3. Do exactly ONE unblocked unit from LOOP-LEDGER.md, to completion, including its
   verifying gate. Paste real gate evidence into the ledger -- never check a box on
   an unrun gate. Then append your Log line.

4. Nobody is watching this run. Never wait for interactive input. If a step truly
   cannot proceed without a human answer, record it per the brief (blocker or
   HUMAN-QUEUE item), leave the checkbox unchecked, and move on.

5. Commit and push to the ceremony branch. If the push fails, say so in the Log
   line rather than claiming success.

6. Stop after one unit. Do not start a second. The scheduler brings the next firing
   in four hours -- you do not need to arrange it, and there is no scheduling tool
   here for you to call.
'@

  Write-Log "Starting headless firing (fresh context)..."

  # Claude writes advisory warnings to stderr before it does any work. Under
  # Windows PowerShell 5.1 -- which is what the Scheduled Task runs -- `2>&1` turns
  # each of those stderr lines into an ErrorRecord, and with
  # $ErrorActionPreference = 'Stop' the very first one aborts the firing before
  # Claude has done anything at all. PowerShell 7 does not behave this way, so a
  # firing launched by hand from pwsh succeeded while every scheduled firing died.
  # Two consecutive scheduled firings were lost to a benign "workspace has not been
  # trusted" warning before this was found.
  #
  # A warning on a native command's stderr is not a script error. Relax the
  # preference for the duration of this one call, and flatten whatever comes back
  # to plain strings so the log stays readable either way.
  $previousPreference = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  $claudeExit = $null
  try {
    # --dangerously-skip-permissions is required: a headless run has no human to
    # answer a permission prompt, so without it the firing stalls and does nothing.
    & claude -p $prompt `
        --permission-mode bypassPermissions `
        --dangerously-skip-permissions 2>&1 |
      ForEach-Object { $_.ToString() } |
      Tee-Object -FilePath $Log -Append
    $claudeExit = $LASTEXITCODE
  }
  finally {
    $ErrorActionPreference = $previousPreference
  }

  Write-Log "Firing finished (exit code $claudeExit)."
  if ($claudeExit -ne 0) {
    Write-Log "WARNING: non-zero exit -- check the transcript above before trusting this firing."
  }
}
catch {
  Write-Log "ERROR: $($_.Exception.Message)"
  throw
}
finally {
  if (Test-Path $Lock) { Remove-Item $Lock -Force }
}
