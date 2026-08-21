# Deferred items — Phase 11.1

Out-of-scope discoveries logged during plan execution, not fixed per the
deviation-rules scope boundary (only auto-fix issues directly caused by the
current task's changes).

## 11.1-02, Task 2

**Item:** `11.1-02-PLAN.md` Task 2's second `<verify><automated>` command
(`assert not found` over `re.findall(r'DSX-[A-Z]+-\d{3}', t)` against the
whole file) fails against `agents/dsx-ml-integrity-auditor.md` regardless of
this plan's edits, because the file's pre-existing "Step 1 — Deterministic
screen" section already names `DSX-CODE-001`–`003` (confirmed present at the
worktree's base commit `f42a300`, before any task-2 change) when documenting
the `dsx check ml repro code` command. Those codes already exist and ship
today — they are not the forward-reference-to-an-unshipped-code drift class
T-11.1-08 exists to catch (see `references/finding-codes.md`) — but the
verify script's whole-file regex scan does not distinguish "existing,
already-shipped code named for context" from "code that does not exist yet."

**Resolution taken:** Not fixed. The task's own `<acceptance_criteria>` list
(the authoritative pass bar) does not restate this specific automated check;
it requires only that the leakage-heuristics block gain the two new signals,
that the closing disclaimer survive, that no other file changes, and that the
full suite stay green — all of which hold. Task 1's identical-shaped check
passed cleanly because `references/leakage-taxonomy.md` carried no
pre-existing finding-code reference to begin with. Confirmed directly: neither
new signal (7 or 8) added by this task names any finding code.

**Left for:** whoever next edits `11.1-02-PLAN.md`'s verify script, or scopes
a phase touching `agents/dsx-ml-integrity-auditor.md` again — narrow the scan
to the `<leakage_heuristics>` block, or to lines added by the diff, rather
than the whole file.

## UAT decision (Option A) — code-review findings WR-02 and IN-01

**Item:** Two of the seven findings in `11.1-REVIEW.md`, both independently
reproduced, deliberately deferred at UAT rather than fixed. The other five
(CR-01, CR-02, CR-03, CR-04, WR-01) were routed to a gap-closure plan due
before Phase 11.2 — see `11.1-UAT.md` test 2.

**WR-02 — `dsx/decisions.py::append()` writes `
`, contract says `
`.**
The module docstring (`dsx/decisions.py:13-15`) states each record is followed
by a single `
`; `append()` (line 116) opens in text mode with no `newline=`
argument, so Windows translates it to `
`. Reproduced. Note the review
understated one thing and overstated another: this is *already materialised*,
not latent — roughly 28.5 MB / 31,290 lines of existing decision-trail files
carry the wrong terminator — but the practical consequence is narrower than
"a future consumer would break", because a naive newline-splitting JSON parser
still reads every record (the extra byte is insignificant whitespace to JSON).
Real exposure is byte-exact consumers only: checksums, golden-file comparison,
byte-offset arithmetic.

**Resolution taken:** Not fixed. One-line fix (`newline="
"` on the open).
Deferred because nothing reading the file today is affected.

**Left for:** whoever next touches `dsx/decisions.py`. Two things to decide at
that point, neither resolved here: (a) existing files stay mixed-terminator
unless rewritten, since only new lines get the fix; (b) this graduates to
urgent the moment any work computes a checksum or byte offset over the trail.
Add a byte-level assertion — none exists today.

**IN-01 — dead entries in `SPLIT_MARKERS` (`dsx/checks/code.py:23-33`).**
Reproduced, and wider than the review states: there are **three** dead entries,
not one. `TimeSeriesSplit(` is shadowed by `TimeSeriesSplit`, `StratifiedGroupKFold`
by `GroupKFold`, and `GroupShuffleSplit` by `ShuffleSplit` — all by the same
mechanism, since `_first_line_matching` tests plain substring membership.

**Resolution taken:** Not fixed. Purely cosmetic; measured as a no-op.

**Left for:** whoever next edits `SPLIT_MARKERS`. **Fix trap, do not skip
this:** removing the *live* entry instead of the dead one also looks like a
no-op, because the dead entry silently takes over — a green test run does NOT
prove the removed entry was the redundant one. Do not remove `KFold(`; it is
the only entry catching a bare `KFold(...)` call. There is currently zero test
coverage of the affected markers, so add the regression test as part of the fix.
