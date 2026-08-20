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
