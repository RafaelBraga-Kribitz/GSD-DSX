# Post-mortem: a post-hoc procedure switch after a pre-registered fallback rule

Paired spec: `post-hoc-procedure-switch-ANALYSIS-SPEC.yaml`

## What was concluded

A conversion-analytics team pre-registered a two-proportion z-test as the primary
analysis for a checkout trust-badge experiment, with a fallback rule declared
before the data was touched: once the comparison family grew past four members —
the test would compare the running candidate badge design against every prior
candidate — the team would switch to the same two-proportion z-test with a Holm
adjustment across the comparison family. By the time the fifth candidate design
was evaluated, the team had looked at five comparisons. At that point they saw
sparse cells in the reported arm of the running comparison, switched to Fisher's
exact test on the reasonable-sounding ground that it is the more conservative
choice when cell counts are small, and reported the result as a pre-registered
analysis.

## Why it was wrong

The declared fallback rule was itself a pre-registered test-selection function —
what to do once a stated condition on the data held. The team's substitution
after seeing the data was not that function evaluated on the data; it was a
different function, chosen once the sparse cells were visible. Two arguments,
each tied to one of the two sources verified for this phase, explain why that
substitution invalidates the "pre-registered" label even though the substitute
is the more conservative test.

First, a p-value is interpretable as evidence only under a strong claim that the
same analysis would have been performed had the data come out differently. Once
an analyst can choose the test after seeing the data — even choosing the more
conservative option — that claim no longer holds, because the choice was made
in response to what the data looked like, not fixed in advance of it (Gelman,
A. and Loken, E. (2014), "The Statistical Crisis in Science", American Scientist
volume 102 issue 6 pages 460-465, page 463, the unnumbered section opening
"Menstrual Cycles and Voting"). The article carries no numbered sections, tables
or theorems, so page plus unnumbered heading is the most precise locator
available.

Second, the substitution is itself a new researcher degree of freedom, and being
more conservative does not repair that. Unless there is an explicit rule about
exactly how to adjust for each such degree of freedom, the additional ambiguity
introduced by allowing a post-hoc choice — even a choice toward stricter
inference — can make the overall procedure's behavior harder to characterize,
not easier, because the choice itself was made contingent on the data (Simmons,
J. P., Nelson, L. D. and Simonsohn, U. (2011), "False-Positive Psychology",
Psychological Science volume 22 issue 11 pages 1359-1366, DOI
10.1177/0956797611417632, page 1365, "General Discussion" then "Nonsolutions"
then "Correcting alpha levels", quoting that unless there is an explicit rule
about exactly how to adjust alphas for each degree of freedom, the additional
ambiguity may make things worse by introducing new degrees of freedom).

Together these two arguments are why the check this fixture demonstrates blocks
on branch identity alone and never on which procedure is more conservative: a
gate that let a "stricter" post-hoc substitution pass would still be scoring the
analyst's judgment about the data, at the moment the choice was made, rather than
the plan fixed before the data existed. That is exactly the researcher degree of
freedom both cited sources describe, dressed in the language of caution rather
than the language of a favorable result.

For prevalence context only — not as a description of this fixture's specific
defect — undisclosed discrepancies between a pre-registration and the analysis
actually reported are common in the published literature: Claesen et al. (2021),
Royal Society Open Science volume 8 issue 10 article 211037, section 3.3, found
89% of studies in their sample carried at least one undisclosed discrepancy, and
Goldacre et al. (2019), Trials volume 20 article 118, Results, found 87% of
trials carried discrepancies serious enough to warrant a correction letter. Both
figures describe how common this behavior is across a literature; neither is a
property of the specific switch this fixture encodes.

## The code that catches it

`DSX-PRE-030` (Phase 10; `dsx/frame/prereg.py`'s
`_check_procedure_reconciliation`). It fires at CRITICAL severity, blocking
`dsx gate verify` and `dsx gate ship`, whenever the declared fallback rule
resolves to a branch and the executed procedure at `analysis.test` names a
different label after `normalize()`. This fixture's declared fallback rule
resolves cleanly to `two_proportion_z` — `results.comparisons_looked_at` is 5,
which satisfies the rule's declared condition (`comparisons_looked_at > 4`) — so
`DSX-PRE-010` stays silent; the executed `analysis.test` is `fishers_exact`, a
different label, so `DSX-PRE-030` fires. `dsx gate plan` and `dsx gate execute`
still exit 0 on this fixture, because `prereg` is registered in the verify and
ship gate profiles only (`dsx/cli.py`'s `GATE_PROFILES`) — there is no executed
branch to reconcile against before the data has been analysed.
