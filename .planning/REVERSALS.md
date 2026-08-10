# Reversals

This file logs reversals of binding decisions: any entry in `brief.md` section 4's
D-table, or `.planning/PROJECT.md`'s M-table. Reversing one of those decisions
requires a record here, written **before or with** the change that reverses it —
never filed after the fact as a retroactive justification.

A reversal record exists so that "here is what I chose" is replaced by "here is
what would change it" — the same discipline the decision-record subsystem (`5.5`)
applies to an analysis applies to this project's own decisions first (D-14).

## Template

Copy the block below for a new reversal. IDs are allocated sequentially as
`REV-NNN` and are never reused, even if a later reversal supersedes an earlier
one.

```markdown
### Reversal record REV-NNN (D-14)

**Date:** YYYY-MM-DD

**Reversed:** which decision, named by its id (`D-NN` or `M-NN`), plus a
one-line restatement of what it said.

**New evidence:** what became known that was not known when the original
decision was made. This field is the falsifiability test — restating the
original reasoning in different words does not satisfy it.

**What would have made the original correct:** the condition under which the
reversed decision would still stand. This is what makes the reversal an
argument rather than a mood; a reversal that cannot state this condition has
not actually located what changed.

**What did not change:** the scope boundary — what stays exactly as decided,
so a reversal of one item is not silently read as a reversal of its
neighbours.
```

## The `SELF-001` convention

`SELF-001` is the finding logged **inside this file** when a `REV-NNN` record
is filed whose **New evidence** field is empty, or merely restates the
original decision's reasoning without adding anything that was not already
known at the time the original decision was made. Filing one looks like
adding a `SELF-001` line inside the offending `REV-NNN` record, naming which
field was empty and why the stated "new evidence" does not clear the bar.

`SELF-001` is a convention for v2.0.0, not a gate check (M-05). `dsx` does not
adjudicate planning documents — enforcing it mechanically would mean a
subcommand reading and judging prose in `.planning/`, which sits outside the
gate path entirely. `brief.md` section 6.6 item 3 records this gap plainly:
there is no enforcement mechanism yet, and whether one is warranted (a `dsx`
subcommand, versus staying a human convention) is an open question for a
later milestone. Until then, catching an evidence-free reversal depends on
whoever reviews the record noticing that **New evidence** does not hold up.

## Reversal log

### Reversal record REV-001 (D-14)

**Date:** 2026 (during brief drafting, prior to Phase 6 planning)

**Reversed:** the blanket deferral of the prior family under D-12a.

**New evidence:** the identification-strength framing supplies a writable
frequentist mirror for two of the four deferred items. Prior predictive
checking mirrors simulated-data checking; prior strength versus
identification mirrors penalisation strength versus identification. The
original deferral assumed no mirror existed. It did, and the drafter had not
looked for it.

**What would have made the original correct:** if prior choice had no
frequentist analogue, which is false for regularisation and true only for
genuine subjective-belief priors.

**What did not change:** `DSX-PAR-021` (sensitivity) and `DSX-PAR-030`
(convergence) stay deferred. Their mirrors remain unwritten, and D-12a's
scoping rule — a paradigm-specific check ships only when its counterpart also
ships — still governs both.
