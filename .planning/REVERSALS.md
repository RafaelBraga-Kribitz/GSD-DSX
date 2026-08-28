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

### Reversal record REV-002 (D-14)

**Date:** 2026-08-27 (Phase 12, plan 12-07)

**Reversed:** the D-13 gated-backlog *deferral* of the ratio-metric dilution
item (`brief.md` §6.5 item 6, Deng & Hu 2015 Formula (3)). It moves from
**deferred** to **permanently out of scope** — relocated into §6.5's "Removed /
permanently out of scope (D-14)" subsection, not left waiting for a promoting
condition.

**New evidence:** Phase 12's charter (REQ-P12-05) required re-evaluating all nine
§6.5 rows against their stated entry conditions using the milestone's now-measured
evidence, under one uniform disposition rule — *evaluable-and-unmet ⇒ carry;
structurally-unreachable ⇒ remove*. Running that pass is the new event: it sorts
item 6 against the other eight and shows item 6 is the **only** row whose entry
condition ("a source of per-unit trigger and outcome data reaching the gate")
cannot be met in principle rather than merely today — Formula (3) is a per-user
sum with no scalar a declaration gate can read, so no future corpus, source or
workload makes it declaration-evaluable. The original row already *hedged* this
("may be permanently out of scope … not merely deferred"); the systematic
re-evaluation is what resolves the hedge into a decision. This is emphatically
**not** the D-01/D-02 determinism doctrine restated as a discovery — that doctrine
pre-dates the deferral and the row already cites it. What changed is the completed
REQ-P12-05 disposition pass that applied the doctrine as a removal rule and found
item 6 uniquely and permanently fails it.

**What would have made the original deferral correct:** a declaration-evaluable
scalar multiplier — an aggregate Formula (3) could collapse to and the gate could
check from the spec alone, the way the additive Formula (1) yields the shipped
`DSX-INT-030`. Formula (3) has none; that is why the condition is structural, not a
forecast about future data access (which D-12 already proved was never the blocker).

**What did not change:** D-01 and D-02 (the determinism doctrine that keeps
computation off the gate path) stand exactly as decided; the additive ratio-metric
case **stays shipped** as `DSX-INT-030`; and §6.5 items 4 (Bayesian admissibility —
`dsx stats --paradigm` measured below 15%) and 5 (`dsx quiz`, awaiting M5) stay
**carried** as evaluable-and-unmet. The "unevaluable ⇒ remove" rule reaches only
item 6's structural unreachability, never a merely-unmet condition.
