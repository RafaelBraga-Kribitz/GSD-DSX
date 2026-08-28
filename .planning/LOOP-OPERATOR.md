# LOOP-OPERATOR — how to start, watch and stop the ceremony

For the human. The agent-facing contract is `LOOP-BRIEF.md`; this file is the
control panel. Everything here is a copy-paste PowerShell command.

## What this is

A Windows Scheduled Task fires `scripts/run-ceremony-firing.ps1` every 4 hours.
Each firing launches a **fresh** `claude -p` process with an empty context window,
does **one** unit from `LOOP-LEDGER.md`, commits, pushes, and exits. Nothing
carries over in conversation memory — all continuity is in git-committed files.
That is what keeps a 10-day ceremony from degrading inside one long session, and
it is why no `/clear` is involved anywhere.

## 1. Start it (run once)

```powershell
$argument = '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "C:\Users\Benutzer1\Dev\AI\gsd-dsx\scripts\run-ceremony-firing.ps1"'
$action   = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $argument -WorkingDirectory "C:\Users\Benutzer1\Dev\AI\gsd-dsx"
$trigger  = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Minutes 15)
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 6) -MultipleInstances IgnoreNew -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "GSD-DSX-v2-Ceremony" -Action $action -Trigger $trigger -Settings $settings -Description "One firing of the gsd-dsx v2.0.0 completion ceremony." -Force
```

**The 15-minute interval is a retry rhythm, not a work rhythm.** A poll that
lands while a firing is already running exits in about a second, because of the
lock file and `MultipleInstances IgnoreNew`. So polls are nearly free, and the
effect is that work runs back-to-back instead of leaving the machine idle between
widely spaced firings. Measured on the original 4-hour interval, the machine
worked 22 minutes out of every 240 — a 9% duty cycle. This is the fix for that.

What the other settings do: `StartWhenAvailable` runs a firing missed because the
machine was asleep; `ExecutionTimeLimit` of 6 hours kills a genuinely runaway
firing while still leaving room for a long phase execution; `MultipleInstances
IgnoreNew` drops an overlapping start rather than running two in parallel (the
script's own lock file is the second guard, and it checks whether the holding
process is really alive so a crashed firing cannot block the queue).

## 2. Smoke-test it before trusting it (recommended)

Run one firing by hand and watch it work. This does real work — it will pick up
`S0-1` and start closing the Phase 11.1.1 security gate.

```powershell
& "C:\Users\Benutzer1\Dev\AI\gsd-dsx\scripts\run-ceremony-firing.ps1"
```

It has succeeded when all three of these are true:

```powershell
git -C C:\Users\Benutzer1\Dev\AI\gsd-dsx log --oneline -3        # a new commit from the firing
git -C C:\Users\Benutzer1\Dev\AI\gsd-dsx status -sb              # nothing unpushed
Select-String -Path C:\Users\Benutzer1\Dev\AI\gsd-dsx\.planning\LOOP-LEDGER.md -Pattern '^\|' | Select-Object -Last 3
```

The third command prints the ledger's Log lines. A real firing always leaves one.
**If the Log gained no line, the firing did nothing — do not assume it worked.**

## 3. Watch it day to day

```powershell
# What has the loop actually done?
Get-Content C:\Users\Benutzer1\Dev\AI\gsd-dsx\.planning\LOOP-LEDGER.md -Tail 25

# What is waiting on you?
Get-Content C:\Users\Benutzer1\Dev\AI\gsd-dsx\.planning\HUMAN-QUEUE.md

# Did the task fire, and when does it fire next?
Get-ScheduledTask -TaskName "GSD-DSX-v2-Ceremony" | Get-ScheduledTaskInfo

# Raw transcript of the most recent firing (gitignored, local only)
Get-ChildItem C:\Users\Benutzer1\Dev\AI\gsd-dsx\.planning\loop-logs\ | Sort-Object LastWriteTime | Select-Object -Last 1 | Get-Content
```

Your one recurring job is `HUMAN-QUEUE.md`. Two items are already waiting there
(the Phase 11 citation reads, and the Phase 11.1.1 security sign-off). Answer
them by editing that file, or by telling an interactive Claude session the verdict
and letting it record the answer in the proper GSD artifact.

## 4. Pause, resume, stop

```powershell
Disable-ScheduledTask   -TaskName "GSD-DSX-v2-Ceremony"     # pause
Enable-ScheduledTask    -TaskName "GSD-DSX-v2-Ceremony"     # resume
Unregister-ScheduledTask -TaskName "GSD-DSX-v2-Ceremony" -Confirm:$false   # stop for good
```

Stop it when `LOOP-LEDGER.md` shows the `MILESTONE COMPLETE` Log line. Nothing
stops the task automatically — a firing after completion is a cheap no-op by
design, but it is still a firing.

## 5. Things that will bite

- **The machine must be awake.** Firings missed to sleep or shutdown are skipped.
  `StartWhenAvailable` catches up one missed run, not a backlog of six. Ten days
  of overnight sleep costs roughly a third of the schedule's slack.
- **Permission posture is wide open.** The script runs `claude` with
  `--dangerously-skip-permissions`, which you chose deliberately so firings never
  stall with no human present. For ten days, an automated process can run any
  command in this repository unchecked. Disable the task when the milestone lands.
- **Do not run an interactive GSD session against this branch while the task is
  live.** Two writers on the same tracking files will conflict. Pause the task
  first.
- **This workspace is not trusted**, so three `permissions.allow` entries in
  `.claude/settings.json` are being ignored. Two of them are also written wrong:
  `Write(.planning/*)` and `Write(STATE.md)` never match, because file permission
  checks only honour `Edit(...)` rules. Irrelevant while permissions are bypassed;
  fix both before ever switching to a narrower posture.
