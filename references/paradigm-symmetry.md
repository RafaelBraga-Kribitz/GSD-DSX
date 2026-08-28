# Paradigm symmetry audit — `DSX-PAR-010` / `DSX-PAR-011`

This document is the constraint Phase 9 builds against, not a description of
what Phase 9 already built. It is written before either check exists
(`PITFALLS.md:456-467`, Pitfall 7) so the design it commits to is falsifiable
before the code lands, and it stays committed with the tool — not under
`.planning/` — because `.planning/` is stripped from every pull-request
branch (the `gsd-pr-branch` workflow), and the symmetry argument brief D-12
requires has to survive for an external reader of the shipped tool.

The claim this document exists to support: **`DSX-PAR-010` (frequentist) and
`DSX-PAR-011` (bayesian) are the same check asked twice, with the same
severity and the same cost of dishonest satisfaction on both sides.** Nothing
below is a report of measured behaviour; it is the shape both checks are
required to have.

## What triggers the pair

Both halves trigger on exactly one condition: `design.peeking_policy`
normalizes to `uncontrolled_continuous`. Nothing else.

Neither half reads `results.interim_looks`. `dsx gate plan` runs before any
`results:` block exists in the spec — a trigger that depended on
`results.interim_looks` would silently become a verify/ship-only check, and
ROADMAP's Phase 9 Success Criterion 1 ("`dsx gate plan` exits `1` against an
uncontrolled continuous design") would be false the moment that spec has no
results yet. The trigger has to be readable from a plan-stage spec alone, so
it is readable from `design.peeking_policy` alone.

## Clearing conditions, per paradigm

| Paradigm | Code | Cleared by |
|---|---|---|
| `frequentist` | `DSX-PAR-010` | a non-blank text value in `inference.alpha_spending` **or** a non-blank text value in `inference.threshold_calibration` |
| `bayesian` | `DSX-PAR-011` | a non-blank text value in `inference.prior_justification` **or** a non-blank text value in `inference.threshold_calibration` |

Three structural facts make this table symmetric, and all three are load-bearing:

1. **Each paradigm has exactly two clearing declarations.** Not one, not
   three — the same count on both sides of the table.
2. **Exactly one of the two — `threshold_calibration` — is shared by both
   paradigms.** It is the same field, checked by the same predicate,
   regardless of which paradigm declared it.
3. **Each paradigm-specific declaration (`alpha_spending` for frequentist,
   `prior_justification` for bayesian) is a non-blank free-text scalar,
   evaluated by the same text-only predicate (`dsx.spec.is_blank_text`) as
   the shared field.** No field on either side carries a stronger
   evidentiary bar than the other — there is no numeric sub-dict on one side
   and a free-text field on the other.

No per-paradigm code path and no per-member branch exists anywhere in this
design. A dict keyed by every member of `PARADIGMS`, evaluated by one shared
predicate, is what makes the symmetry a structural property rather than an
inspection result — the same idiom `_PARADIGM_CONDITIONAL` already
establishes in `dsx/frame/paradigm.py`.

## The honest fix versus the cheap fix

**The honest fix**, for either half, is to change `design.peeking_policy`
away from `uncontrolled_continuous` — to `sequential_obf`,
`sequential_pocock`, or `always_valid`. That is what "declaring a sequential
or anytime-valid method" means under REQ-P9-01, and it removes the trigger
for both halves identically, because both halves share the same trigger
condition. Changing the design is the only fix that actually controls the
error rate a peeked test accumulates.

**The cheapest dishonest fix**, for either half, is to type any non-blank
string into the paradigm-specific clearing field — `alpha_spending` on the
frequentist side, `prior_justification` on the bayesian side — while leaving
`design.peeking_policy` at `uncontrolled_continuous` and changing nothing
about how the analysis is actually monitored. A value that carries no text —
a bare number, a boolean, an empty string, or a container — does not clear
either half, so this one-free-text-declaration cost is a floor, not an
overstatement: nothing cheaper than typing an actual string exists.

This cheapest dishonest path costs **exactly the same on both sides: one
free-text declaration.** That equality — not the mere existence of two codes
— is what brief D-12 requires. A pair where both codes exist but one side's
cheapest escape is a plausible paragraph and the other side's cheapest escape
is adopting a real, behaviour-changing method is still an asymmetric pair in
the dimension D-12 cares about, even though the catalogue shows two rows
(`PITFALLS.md:421-478`, Pitfall 7). This design closes that gap by giving
both sides a free-text scalar as their paradigm-specific declaration and the
identical shared field as their alternative — same shape, same predicate,
same cost, on both rows of the table above.

## What does not clear either half

None of the following clears `DSX-PAR-010` or `DSX-PAR-011`, for any
clearing field, on either paradigm: an absent field, a `null`, an empty or
whitespace-only string, a number, a boolean, or a list or mapping of any
size, empty or not — an `int`, a `float`, and a Python `bool` are all
included. This list is pinned by a committed test,
`tests/test_dsx.py::TestPhase9MonitoringDiscipline`, rather than by this
document, so it cannot silently drift from the code's actual behaviour.

Until this closed, the predicate deciding whether a clearing field was
"declared" was the general blank check (`dsx.spec.is_blank`), under which a
bare `0` or `false` reads as present. A spec whose only monitoring-discipline
content was `inference.threshold_calibration: 0` therefore cleared the
CRITICAL pair with zero declared content — cheaper than the one-free-text-
declaration path this document names as the cheapest dishonest fix. That gap
is what this section exists to say is closed: the clearing predicate is now
`dsx.spec.is_blank_text`, which treats every non-string value as blank
regardless of what `is_blank` itself would say about it.

## What the gate cannot adjudicate

A declared `prior_justification` is checked for **presence**, never for
**quality**. Whether the stated justification actually reflects the
operator's real prior odds, or is a sentence typed to clear the gate, is not
something `dsx gate` can tell from the declaration alone — that judgement is
`DSX-PAR-020`'s job and is explicitly deferred under brief D-12a. Likewise, a
declared `threshold_calibration` is the operator's own claim about their own
calibration procedure; the gate reads that the field is non-blank, not that
the calibration described in it was actually performed or performed
correctly.

This is the project's standing known limit, stated plainly rather than
implied by omission: **a frame that lies passes.** Neither `DSX-PAR-010` nor
`DSX-PAR-011` is a stronger check than that limit allows — they enforce that
a monitoring-discipline declaration exists, not that the declaration is
true. Presenting either check as adjudicating the quality of the underlying
statistical practice, rather than the presence of a declaration about it,
would overstate what a declarations-only gate can ever do (brief D-02).

## The undeclared-paradigm case

With no `inference.paradigm` declared at all, every row of the per-paradigm
table above applies simultaneously — both `DSX-PAR-010` and `DSX-PAR-011` can
fire against the same undeclared-paradigm spec. This is deliberate, and it
preserves the brief-D-10 property this whole family depends on: **declaring
a paradigm never adds a finding, it only ever removes one.** An operator who
honestly declares `frequentist` or `bayesian` is left facing exactly one
half of the pair instead of both; an operator who declares nothing is left
facing both. Declaring a paradigm is therefore never more expensive than
staying silent about it — silence is the maximally exposed position, not a
shortcut past the pair.

`DSX-PAR-002` (HIGH) separately names the missing `inference.paradigm`
declaration itself. But the block that actually stops `dsx gate plan` on an
undeclared, uncontrolled-continuous design comes from the monitoring pair's
own CRITICAL severity, not from `DSX-PAR-002` — `DSX-PAR-002`'s HIGH severity
does not block at `plan` on its own (`dsx/cli.py` `GATE_THRESHOLDS`: CRITICAL
at plan/execute, HIGH at verify/ship).

## Reference values and their sources

**`DSX-PAR-010`** reuses `dsx.mathx.inflation_from_peeking()` directly — no
second inflation table is coined. At a nominal alpha of `0.05`, that function
returns `0.142` at five interim looks and `0.248` at twenty.

**`DSX-PAR-011`**'s reference value is `1/(K+1)`, where `K` is the posterior
odds implied by the decision threshold. At the `P(B>A) > 0.95` decision
threshold this family assumes, `K = 19` (since `19/20 = 0.95`), and
`1/(K+1) = 1/20 = 0.05` exactly. This is cited to Deng, Lu & Chen (2016) —
Theorem 1 for the result that licenses this figure under optional stopping
with known prior odds, and the paper's unnumbered §3.2 prose ("rejecting H₀
when observing a posterior odds no less than K exposes us to a risk of false
discovery at most `1/(1+K)`") for the bound in its operational, "at most"
form. Theorem 1 itself states an optional-stopping equality, not the bound
directly — the bound is unnumbered prose immediately following it and again
at §3.2, and citing Theorem 1 alone for the number `1/(K+1)` would be a
locator error.

`1/(K+1)` and `1/k` are **different results, for different conditioning
events, and must never be interchanged.** Ville's inequality gives
`P(sup_t M_t ≥ k) ≤ 1/k` for a nonnegative martingale starting at 1 — at
`k = 19` that is `1/19`, approximately `0.0526`. Deng, Lu & Chen's Theorem 1
never invokes Ville by name; its proof is a likelihood-ratio / change-of-measure
argument, not a maximal-inequality argument. `0.0526` is not `0.05` — the two
numbers are close enough to look like an arithmetic slip from a distance and
are, in fact, two individually correct statements about two different
quantities. Substituting one bound for the other, or reconciling their gap
as an artifact of imprecision, silently launders one theorem's guarantee
into the other's claim.

## Related links

- `references/finding-codes.md` — the generated catalogue; `DSX-PAR-010` and
  `DSX-PAR-011` appear there once shipped.
- `README.md` — "Two tiers of evidentiary rigour" links here as the symmetry
  argument behind the `DSX-PAR-*` family.
