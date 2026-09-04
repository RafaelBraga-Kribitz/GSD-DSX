<#
.SYNOPSIS
  One firing of the autonomous milestone ceremony.

.DESCRIPTION
  Launches a FRESH headless Claude Code process against the repo. Each firing is a
  brand-new process with an empty context window -- that is the whole point: it is
  what stops a multi-day ceremony from degrading inside one ever-growing
  conversation. All continuity lives in git-committed files (.planning/LOOP-BRIEF.md,
  LOOP-LEDGER.md, HUMAN-QUEUE.md), never in conversation memory.

  Registered as a Scheduled Task polling every 15 minutes -- a retry rhythm, not a
  work rhythm: the lock file makes an overlapping poll exit in about a second, so
  work runs effectively back-to-back whenever the machine is free. Safe to run by
  hand too.

.NOTES
  Overlap guard: a lock file prevents a second firing starting while one is running.
  Usage-limit backoff: when a firing's transcript shows a usage/rate-limit hit, a
  .backoff-until file parks polls until the account's allowance returns -- the
  weekly reset is Wednesday 10:00 America/Sao_Paulo (13:00 UTC; Brazil has had no
  DST since 2019), a 5-hour-window hit parks 60 minutes. Resumption is automatic
  two ways: (1) the first poll after the deadline always resumes; (2) every
  $ProbeIntervalMinutes during the hold, a poll spends one trivial, tool-free
  `claude -p` call to check whether the limit was lifted EARLY -- observed for
  real on 2026-09-01: Anthropic sometimes restores a weekly allowance before its
  stated reset, and a pure dead-reckoning wait has no way to notice that on its
  own, so it would otherwise sit idle for up to a full window's worth of already-
  available capacity.
  Logs: .planning/loop-logs/ (gitignored).
#>

$ErrorActionPreference = 'Stop'

$Repo   = 'C:\Users\Benutzer1\Dev\AI\gsd-dsx'
# Milestone branch. Updated 2026-09-02 when v2.3 Test Catalog shipped (merged
# to main, tag v2.3.0) and the loop was repointed at v2.4 Visual Excellence.
# The branch guard below deliberately ABORTS rather than checking out: if this value
# and the working tree disagree, something unexpected has happened and a headless
# firing must not guess.
$Branch = 'gsd/v2.4.0-visual-excellence'
$LogDir = Join-Path $Repo '.planning\loop-logs'
$Lock   = Join-Path $LogDir '.firing.lock'
$Backoff = Join-Path $LogDir '.backoff-until'
$ProbeMarker = Join-Path $LogDir '.backoff-last-probe'
$BackoffLog = Join-Path $LogDir 'backoff.log'
$Stamp  = (Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss')
$Log    = Join-Path $LogDir "firing-$Stamp.log"
# How often (minutes) a held poll spends one trivial probe call checking for an
# early release. 2 poll cycles: frequent enough to catch an early reset within
# ~30 min, infrequent enough that a probe is a rounding error next to a firing.
$ProbeIntervalMinutes = 30

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir -Force | Out-Null }

function Write-Log($msg) {
  $line = "[{0}Z] {1}" -f (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss'), $msg
  Write-Output $line
  Add-Content -Path $Log -Value $line
}

# --- Operator pause switch ---------------------------------------------------
# Checked FIRST, before the lock, the backoff and the branch guard: a paused loop
# must do nothing at all, not even churn the lock file. Added 2026-09-04 because
# the Windows Scheduled Task itself cannot be disabled from automation on this
# box (`Disable-ScheduledTask` returns "Access is denied" without elevation), so
# the wrapper needs its own honest off switch that does not require admin.
#
#   PAUSE:  New-Item -ItemType File .planning\loop-logs\.paused
#   RESUME: Remove-Item .planning\loop-logs\.paused
#
# Deliberately NOT the same thing as the branch guard. The branch guard aborts on
# an UNEXPECTED tree state; this is an INTENTIONAL, operator-set stop that holds
# regardless of which branch is checked out. Any text written into the file is
# echoed to the log as the stated reason, so a future reader learns why.
# Deliberately does NOT use Write-Log: that opens a per-firing `firing-<stamp>.log`,
# and a paused loop writing 96 near-identical files a day is not meaningfully
# stopped. A paused poll appends ONE line to a single rolling `paused.log` and
# creates nothing else.
$PauseFlag = Join-Path $LogDir '.paused'
if (Test-Path $PauseFlag) {
  $reason = (Get-Content $PauseFlag -Raw -ErrorAction SilentlyContinue)
  if ($reason) { $reason = ($reason -replace '\s+', ' ').Trim() }
  if ([string]::IsNullOrWhiteSpace($reason)) { $reason = '(no reason recorded)' }
  $line = "[{0}Z] PAUSED by operator: {1}" -f `
    (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss'), $reason
  Write-Output $line
  Add-Content -Path (Join-Path $LogDir 'paused.log') -Value $line
  exit 0
}

function Get-NextWeeklyReset {
  # Weekly allowance renews Wednesday 10:00 America/Sao_Paulo = 13:00 UTC
  # (Brazil abolished DST in 2019, so the offset is a constant -3).
  $now = (Get-Date).ToUniversalTime()
  $daysAhead = (([int][DayOfWeek]::Wednesday) - ([int]$now.DayOfWeek) + 7) % 7
  $candidate = $now.Date.AddDays($daysAhead).AddHours(13)
  if ($candidate -le $now) { $candidate = $candidate.AddDays(7) }
  return $candidate
}

function Test-UsageLimitHit([string]$Text) {
  # Shared wording check, used both on a real firing's transcript and on a
  # bare probe reply. $Text should already be lowercased. Returns a hashtable
  # so callers get both "was it a limit" and "which kind" from one scan.
  $isLimited = $false
  foreach ($pat in @('usage limit', 'rate limit', 'rate-limit', 'limit reached',
                     'limit will reset', 'out of extra usage', 'usage cap',
                     'hit your limit', 'hit your weekly', 'hit your monthly',
                     'weekly limit', 'exceeded your usage')) {
    if ($Text.Contains($pat)) { $isLimited = $true; break }
  }
  return @{ Limited = $isLimited; Weekly = ($isLimited -and $Text.Contains('week')) }
}

function Invoke-LimitProbe {
  # A trivial, tool-free call that costs almost nothing and definitively answers
  # "does the account accept work right now" -- Claude either replies, or the
  # CLI prints limit wording and exits non-zero. No file reads, no git, no repo
  # side effects; deliberately decoupled from ceremony state.
  $prevPref = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    $out = & claude -p 'Reply with exactly: PROBE-OK' `
        --permission-mode bypassPermissions `
        --dangerously-skip-permissions 2>&1 |
      ForEach-Object { $_.ToString() }
  } finally {
    $ErrorActionPreference = $prevPref
  }
  return (($out -join ' ') -replace "`0", '').ToLowerInvariant()
}

# --- Usage-limit backoff guard (BEFORE the lock; cheapest possible exit) ------
# During a hold, most polls must not spawn a firing log each -- a single
# rolling backoff.log line is enough for the operator to see the loop is
# parked. Every $ProbeIntervalMinutes, though, a poll spends one Invoke-LimitProbe
# call to check for an early release rather than blindly trusting the deadline.
if (Test-Path $Backoff) {
  $untilRaw = (Get-Content $Backoff -Raw -ErrorAction SilentlyContinue).Trim()
  $until = [datetime]::MinValue
  $parsed = [datetime]::TryParseExact($untilRaw, 'yyyy-MM-ddTHH:mm:ssZ',
      [Globalization.CultureInfo]::InvariantCulture,
      ([Globalization.DateTimeStyles]::AssumeUniversal -bor [Globalization.DateTimeStyles]::AdjustToUniversal),
      [ref]$until)

  if ($parsed -and ((Get-Date).ToUniversalTime() -lt $until)) {
    $probeDue = $true
    if (Test-Path $ProbeMarker) {
      $lastProbe = (Get-Item $ProbeMarker).LastWriteTimeUtc
      if (((Get-Date).ToUniversalTime() - $lastProbe).TotalMinutes -lt $ProbeIntervalMinutes) {
        $probeDue = $false
      }
    }

    if (-not $probeDue) {
      Add-Content -Path $BackoffLog -Value ("[{0}Z] parked: usage-limit hold until {1} (UTC); poll skipped." -f `
        (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss'), $untilRaw)
      exit 0
    }

    # Probe due: spend one trivial call to check for an early release.
    Set-Content -Path $ProbeMarker -Value ((Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ'))
    $probeText = Invoke-LimitProbe
    $probeResult = Test-UsageLimitHit $probeText

    if ($probeResult.Limited) {
      # Still genuinely limited. Re-derive the hold window from THIS probe's own
      # wording (Anthropic could equally extend or shorten it) rather than
      # assuming the original deadline still holds.
      if ($probeResult.Weekly) { $newUntil = Get-NextWeeklyReset } else { $newUntil = (Get-Date).ToUniversalTime().AddMinutes(60) }
      $newUntilStr = $newUntil.ToString('yyyy-MM-ddTHH:mm:ssZ')
      Set-Content -Path $Backoff -Value $newUntilStr
      Add-Content -Path $BackoffLog -Value ("[{0}Z] probe: still limited -- hold updated to {1} (UTC)." -f `
        (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss'), $newUntilStr)
      exit 0
    }

    # Probe succeeded -- capacity is back before the dead-reckoned deadline.
    Remove-Item $Backoff -Force -ErrorAction SilentlyContinue
    Remove-Item $ProbeMarker -Force -ErrorAction SilentlyContinue
    Add-Content -Path $BackoffLog -Value ("[{0}Z] probe succeeded (early release, before {1} UTC) -- resuming now." -f `
      (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss'), $untilRaw)
    # Fall through into the normal firing below -- no need to wait for the next poll.
  } else {
    # Deadline passed (or file unparseable -- fail open, never park forever on garbage).
    Remove-Item $Backoff -Force -ErrorAction SilentlyContinue
    Remove-Item $ProbeMarker -Force -ErrorAction SilentlyContinue
    Add-Content -Path $BackoffLog -Value ("[{0}Z] hold ended ({1}) -- resuming normal firings." -f `
      (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss'), $untilRaw)
  }
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

  # --- Sync guard --------------------------------------------------------------
  # A plain --ff-only merge throws on ANY divergence and $ErrorActionPreference =
  # 'Stop' turns that into an immediate script abort -- before Claude ever runs.
  # Observed for real: another tool (Cursor Agent) committed on a stale local
  # checkout and force-pushed, discarding this branch's already-pushed commits
  # from origin. Every 15-minute firing after that died at this exact line for
  # 15 hours straight (62 consecutive failures) doing zero work, because a true
  # fast-forward was permanently impossible until a human intervened.
  #
  # Try the fast path first; if it's not a fast-forward, attempt a real merge
  # (safe when the two sides touch disjoint files, which is the common case for
  # a ledger/HUMAN-QUEUE write colliding with unrelated code/test commits). Only
  # a genuine content conflict is left for a human -- and it fails LOUD, leaving
  # the tree in a clean, non-conflicted state, not silently retried forever.
  $ffOutput = git merge --ff-only "origin/$Branch" 2>&1 | Out-String
  if ($LASTEXITCODE -ne 0) {
    Write-Log "Fast-forward not possible, attempting an auto-merge: $($ffOutput.Trim())"
    $mergeMsg = "merge: reconcile with origin (auto, fast-forward was not possible)`n`nAutomated by run-ceremony-firing.ps1's sync guard."
    $mergeOutput = git merge "origin/$Branch" -m $mergeMsg 2>&1 | Out-String
    if ($LASTEXITCODE -ne 0) {
      git merge --abort 2>&1 | Out-Null
      Write-Log "ABORT: real merge conflict with origin/$Branch -- a human must resolve this by hand. Merge aborted, tree left clean. Details: $($mergeOutput.Trim())"
      exit 1
    }
    Write-Log "Auto-merge succeeded (disjoint changes): $($mergeOutput.Trim())"
    git push 2>&1 | Out-String | ForEach-Object { if ($_.Trim()) { Write-Log $_.Trim() } }
  } else {
    if ($ffOutput.Trim()) { Write-Log $ffOutput.Trim() }
  }

  # --- The firing prompt -----------------------------------------------------
  # Deliberately short. LOOP-BRIEF.md is the real contract and is re-read every
  # firing; duplicating its rules here would let the two drift apart.
  $prompt = @'
You are ONE firing of the recurring autonomous milestone ceremony for this
repository. You are a fresh process with an EMPTY context window and NO memory
of any previous firing. Everything you need to know is on disk.

1. Read, in full and in this order: .planning/LOOP-BRIEF.md, then
   .planning/LOOP-LEDGER.md, then .planning/HUMAN-QUEUE.md. LOOP-BRIEF.md is your
   complete operating contract -- its Section 0 describes the execution model you
   are inside of right now. Follow it exactly: cadence, model/effort routing,
   the expert-persona decision protocol, the non-negotiable ground rules, the
   stage plan, and the reporting rules all bind this firing.

2. Reconcile claims against reality before trusting the ledger: run
   `git log --oneline -15` and `git status`. The ledger is a claim; the repo is
   the fact. If they disagree, correct the ledger first.

3. Work unblocked units from LOOP-LEDGER.md per the brief's Section 1 (as many
   as the pacing cap and your context allow), each to completion including its
   verifying gate. Paste real gate evidence into the ledger -- never check a box
   on an unrun gate. Then append your Log line.

4. Nobody is watching this run. Never wait for interactive input. If a step truly
   cannot proceed without a human answer, record it per the brief (blocker or
   HUMAN-QUEUE item), leave the checkbox unchecked, and move on.

5. If any tool call fails with a usage/rate-limit error: do NOT retry in a loop.
   Append one Log line noting the limit, commit and push whatever is already
   done, and stop -- the wrapper script detects the limit and pauses the polling
   until the allowance returns. Pacing is the wrapper's job, not yours.

6. Commit and push to the ceremony branch. If the push fails, say so in the Log
   line rather than claiming success.

7. Stop at the brief's stop conditions. The scheduler polls every 15 minutes --
   you do not need to arrange the next firing, and there is no scheduling tool
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

  # --- Usage-limit detection --> graceful backoff -----------------------------
  # Operator directive (2026-08-29): when the account hits its token limits, the
  # loop must fail gracefully and return to work BY ITSELF -- both at the weekly
  # reset AND, per Test-UsageLimitHit's periodic probe above, on an early release
  # (observed for real 2026-09-01). The Scheduled Task itself cannot be modified
  # from automation (Access Denied -- verified), so the pause lives here: a
  # .backoff-until file the guard at the top of this script honors.
  #
  # Detection scans the tail of this firing's own transcript via the same
  # Test-UsageLimitHit used by the probe, so the two paths can never drift apart.
  # False positives are cheap (the periodic probe corrects them within
  # $ProbeIntervalMinutes); false negatives only cost a few no-op polls that
  # fail fast at the CLI.
  $tail = ''
  if (Test-Path $Log) {
    $tail = ((Get-Content $Log -Tail 400 -ErrorAction SilentlyContinue) -join ' ')
    $tail = ($tail -replace "`0", '').ToLowerInvariant()
  }
  $limitResult = Test-UsageLimitHit $tail
  if ($limitResult.Limited) {
    if ($limitResult.Weekly) { $until = Get-NextWeeklyReset; $reason = 'weekly allowance exhausted' }
    else { $until = (Get-Date).ToUniversalTime().AddMinutes(60); $reason = '5-hour-window limit (or unclassified limit)' }
    $untilStr = $until.ToString('yyyy-MM-ddTHH:mm:ssZ')
    Set-Content -Path $Backoff -Value $untilStr
    Write-Log "BACKOFF: $reason detected in transcript -- parking all polls until $untilStr (UTC). Resumption is automatic (deadline or an earlier successful probe, whichever comes first)."
    Add-Content -Path $BackoffLog -Value ("[{0}Z] parked by firing-{1}: {2}; hold until {3}." -f `
      (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss'), $Stamp, $reason, $untilStr)
  } else {
    # A clean firing is itself proof capacity exists -- drop any stale probe
    # marker so a future hold's first probe isn't needlessly throttled by it.
    Remove-Item $ProbeMarker -Force -ErrorAction SilentlyContinue
  }
}
catch {
  Write-Log "ERROR: $($_.Exception.Message)"
  throw
}
finally {
  if (Test-Path $Lock) { Remove-Item $Lock -Force }
}
