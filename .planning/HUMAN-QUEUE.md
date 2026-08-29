# HUMAN-QUEUE — items only you can answer

Milestone **v2.2 Analytic Surface — SHIPPED 2026-08-29 (tag `v2.2.0`).** All
items below are historical. The loop keeps working around open items; it only
blocks at the close-out stage (S5-2) if any remain.

**How to answer:** the operator is usually remote and cannot run local commands.
Answer in the session; an interactive Claude session records the verdict in the
proper GSD artifact (UAT file, SECURITY.md) and checks the item off here.

**What reaches this queue** (brief §4 — everything else the loop decides itself via
a persona round and records loudly):

1. A D-05 primary-source read — citation authenticity. The loop may prepare the
   evidence pack; it may not sign it.
2. An irreversible destructive operation (file deletion, history rewrite, force-moving
   a published tag).
3. A change to milestone scope (dropping or rewording a requirement).
4. A security sign-off (`SECURITY.md` approval line).
5. An outward-facing ship action (merge to `main`, release tag, opening a PR).

## Open

(none — HQ-15 answered and closed 2026-08-29; see Answered below. v2.2 Analytic
Surface is fully shipped, tagged `v2.2.0`, and merged to `main`. No milestone is
currently open.)

## HQ-8-superseded — original evidence pack (answered; kept for the record)

### HQ-8 — Phase 15 D-05 citation evidence pack (filed early by design; non-blocking)

**Status: ASSEMBLED 2026-08-28 (S0-3), awaiting the human read. DO NOT SIGN — the loop
prepared this pack; D-05 authenticity is a human reading the primary source at its
locator.** Filed ahead of Phase 15 so the operator can read while Phases 13/14/16 build.
Nothing waits on this until close-out (S5-2).

**What "confirmed" means below:** bibliographic metadata (authors / title / venue / year /
pages / DOI) and the candidate formulation were corroborated by the loop across multiple
*independent* sources on 2026-08-28. That is **not** a D-05 read — it only makes the
operator's read a fast confirm-at-locator instead of a hunt. **What the human must still
do** is open each primary source and confirm the exact result at the exact locator.
Code→citation binding and the D-06 numbering are **Phase 15 (S4-1) persona decisions, not
settled here** — this pack only qualifies the citations.

#### Citation 1 — CUPED (REQ-P15-02) — confidence the read will confirm: **HIGH**

| Field | Value |
|---|---|
| Primary source | Deng, A., Xu, Y., Kohavi, R. & Walker, T. (2013). *Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data.* WSDM '13, pp. **123–132**. DOI **10.1145/2433396.2433413**. |
| Candidate formulation (confirm in the method section, ~§3) | Adjusted metric **Ŷ_cv = Ȳ − θ(X̄ − E[X])**; optimal **θ = Cov(Y,X) / Var(X)**; resulting **Var(Ŷ_cv) = Var(Ȳ)·(1 − ρ²)**, ρ = corr(Y,X). The covariate **X must be pre-experiment** (independent of treatment); a **post-treatment covariate is invalid** — this is exactly the rule REQ-P15-02's check enforces (post-treatment covariate blocks). |
| Candidate worked value (for the fixture/docstring, **not** a gate-path computation — D-02) | Analytic identity **variance-reduction factor = 1 − ρ²** (e.g. ρ=0.5 → 25 % reduction; ρ≈0.7 → ~50 %). Empirical headline the paper reports: **≈50 % variance reduction** on Bing's key metric using the same metric from the pre-period as covariate. |
| **Confirmed by the loop** (not a sign-off) | Locator (authors/title/venue/year/pages/DOI); that this WSDM'13 paper is CUPED's primary source; the estimator, optimal θ, and the 1−ρ² relationship (corroborated across independent restatements). |
| **UNVERIFIED — for the human read** | The exact **equation numbers and section**, and the exact **page** carrying the ≈50 % Bing figure; that the pre-experiment (non-post-treatment) covariate requirement is stated in the paper in the form the docstring will cite. |
| Admissibility | The Unified Framework playbook's Python snippet (the `r>0.3` heuristic) is **NOT** admissible (SURFACE.md §8). The WSDM paper is. |

#### Citation 2 — Survivorship bias (REQ-P15-04) — confidence: **MEDIUM (transfer is the open question)**

| Field | Value |
|---|---|
| Candidate primary source | Brown, S. J., Goetzmann, W. N., Ibbotson, R. G. & Ross, S. A. (1992). *Survivorship Bias in Performance Studies.* The Review of Financial Studies **5(4): 553–580**. DOI **10.1093/rfs/5.4.553**. Quantified companion: Elton, Gruber & Blake (1996), *Survivorship Bias and Mutual Fund Performance*, RFS **9(4): 1097–1120**. |
| Defect the Phase 15 code would assert (cohort/funnel context) | A retention/conversion **denominator conditioned on survival** to a later point — a rate computed only over units still present, excluding those that dropped out, so the base is selected on the outcome. |
| **Confirmed by the loop** | These are real, foundational primary sources on survivorship bias, finance-domain, with numerical examples of the bias. |
| **OPEN D-05 QUESTION for the human** | Do these sources give an **operationalisable criterion that transfers** to a declaration-checkable cohort/funnel spec field? They define the bias via truncated-sample regression on surviving funds; the transfer to "the spec must declare a fixed, survival-independent denominator" is the judgment only the read can make. **If it does not transfer cleanly, per brief §6.5 the survivorship-bias code stays unshipped rather than invented.** |

#### Citation 3 — Changing denominator (REQ-P15-04) — confidence: **MEDIUM (scope boundary matters)**

| Field | Value |
|---|---|
| Candidate primary source | Crook, T., Frasca, B., Kohavi, R. & Longbotham, R. (2009). *Seven Pitfalls to Avoid when Running Controlled Experiments on the Web.* KDD '09, pp. **1105–1114**. DOI **10.1145/1557019.1557139** — Simpson's paradox from **changing/dynamic traffic allocation**; operationalisable rule: hold allocation constant, or estimate within constant-allocation epochs and aggregate. Textbook restatement: Kohavi, Tang & Xu (2020), *Trustworthy Online Controlled Experiments*, Cambridge Univ. Press (Simpson's-paradox chapter — **chapter/section to confirm**). |
| Defect the code would assert (cohort/funnel context) | A rate whose **denominator (base population) changes between the compared cohorts/steps/periods**, making the percentages non-comparable. |
| **SCOPE BOUNDARY — read before binding** | This is **distinct from ratio-metric dilution** (Deng & Hu 2015, Formula (3)), which brief.md line 450 already ruled **permanently out of scope** for the declaration-only gate (D-01/D-02, no closed-form scalar). Phase 15 must **not** re-mint that out-of-scope check under a "changing-denominator" label. |
| **Confirmed by the loop** | Crook et al. 2009 and Kohavi et al. 2020 are real primary sources on Simpson's-paradox / changing-allocation. |
| **OPEN D-05 QUESTION for the human** | Which **exact** defect the Phase 15 code asserts, and whether the chosen source's criterion is operationalisable as a **declaration check** for that exact defect. If not, code stays in §6.5. |

**Operator action:** read the three primary sources at the locators above and reply in a
session with, per citation: confirmed-at-locator (with any locator corrections), or
not-confirmed → the code stays in `brief.md` §6.5 unshipped. An interactive session records
the verdict and checks this item off. Until then Phase 15 (S4) treats every code whose
citation is not confirmed as **not in hand** (S4-3 D-05 bar).

## Will be added by the loop when reached

(none — v2.2 has shipped; nothing further is expected on this milestone.)

## Standing framework notes (not queue items — nothing to answer, just remember)

**`/gsd-audit-uat`'s automated CLI under-reports human-verification items.**
Found 2026-08-27 during v2.0.0's S4-1: the CLI returns a false "All Clear" because
`gsd-core/bin/lib/uat.cjs::parseVerificationItems` only recognizes a level-2
`## Human Verification` heading, while the `gsd-verifier` template actually writes a
level-3 `### Human Verification Required` heading. Framework-internal defect, not a
bug in this repo — recorded, not patched. **At S5-1 and S5-4, do not accept a CLI
"all clear" as evidence of no outstanding UAT** — cross-check each phase's
VERIFICATION.md by hand.

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete and structural-file conflicts on
v2.0.0's 707-commit branch and was abandoned mid-run. Ship by direct 3-way merge
instead — see ledger unit S5-6.

**Release tags: never force-move a published one.** v2.0.0's tag was already on
origin against an earlier partial merge, so the completed milestone shipped as
`v2.1.0` and the queued Analytic Surface milestone was renamed v2.1 → v2.2 to avoid
colliding with it. The next free tag for this milestone is `v2.2.0`.

**Run the full suite from a clean tree — a stray root `DECISIONS.jsonl` false-fails
two `explain` tests.** Found 2026-08-29 (S4-5). `tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`
and `tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`
run `dsx explain --spec /nonexistent` from the repo-root CWD **without isolating it**
(the sibling tests in those classes use `tempfile.TemporaryDirectory()`; these two
don't). A **gitignored** `DECISIONS.jsonl` decision ledger (`.gitignore:7`), auto-written
by any repo-root `dsx gate`/`dsx explain`, then makes `explain` read a real trail and the
`"no decision trail"` assertion fails. On a clean checkout — the state the committed tree
ships as — both pass; `scripts/check.sh` is green because it runs the suite **before** its
own gate steps regenerate the ledger. Fix if desired: isolate CWD in those two tests (a
tracked-source change, out of Phase-15 scope — left as recorded tech-debt, not patched).
**At S5-1 and S5-4, if the full suite shows exactly these two failures, delete the
gitignored `DECISIONS.jsonl` files and re-run before treating it as a real defect** —
`rm -f DECISIONS.jsonl examples/DECISIONS.jsonl examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl`.

## Answered

(v2.0.0's answered items — HQ-1 … HQ-7 — are archived at
`.planning/milestones/v2.0.0-HUMAN-QUEUE.md` and
`.planning/milestones/v2.0.0-HUMAN-QUEUE-ARCHIVE.md`.)

### HQ-8 — Phase 15 D-05 citation evidence pack (answered 2026-08-28)

**Operator verdict (verbatim):** `cite1 confirmed at locator; cite2 does not transfer -- leave unshipped; cite3 confirmed at locator`

**How this differs from HQ-1/4/5/6/7's pattern:** those were read by the *operator*, with an
interactive session assembling evidence first. Here the interactive session itself downloaded
and read all three primary sources directly (not a secondary corroboration pass) *before*
presenting the choice, then the operator decided based on that direct read. This is a stronger
evidentiary basis than a bibliographic-only pack, not a substitute for D-05 — the operator's
decision is still the one that binds.

| # | Citation | Result | Detail |
|---|---|---|---|
| 1 | CUPED (REQ-P15-02) | **Confirmed at locator** | Full text of Deng, Xu, Kohavi & Walker (2013) downloaded from its official host (exp-platform.com) and read directly. Byline verified against the actual PDF (a web-search summary along the way misattributed different authors; the primary source overrode it — exactly the failure mode D-05 exists to catch). The abstract states the ~50% Bing variance-reduction figure directly. The paper's linear model uses `θ` notation matching the docstring's planned formulation (`E(Yi\|Zi,Xi) = θ0 + δZi + θᵀXi`). The pre-experiment-only requirement is stated in the paper's own words: *"the pre-experiment information is guaranteed to be independent of the experiment's effect, which is crucial to avoid biased results."* Ready for Phase 15 to cite by page/section once implemented. |
| 2 | Survivorship bias (REQ-P15-04, half A) | **Does not transfer — leave unshipped** | Full text of Brown, Goetzmann, Ibbotson & Ross (1992) read directly. Its actual result is a formal, fund-performance-persistence-specific finding (survivorship-truncated samples induce a spurious volatility–return correlation, proved via distributional lemmas) — the paper never uses the word "denominator," and its worked examples are mutual-fund-specific. It does not state, or straightforwardly imply, a general "a rate's denominator must exclude non-survivors" rule that would transfer to a cohort/funnel declaration check. Per `brief.md` §6.5's own rule, this stays **unshipped** rather than citing a source whose argument does not carry the weight being put on it. **This is a REQ-P15-04 scope note Phase 15's discuss (S4-1) must record loudly, not discover silently:** REQ-P15-04 as worded expects both the survivorship-bias and changing-denominator defects to ship; the honest outcome is that only the changing-denominator half does, with the survivorship half remaining a documented non-promotion in `brief.md` §6.5 pending a better-fitting source. |
| 3 | Changing denominator (REQ-P15-04, half B) | **Confirmed at locator** | Full text of Crook, Frasca, Kohavi & Longbotham (2009) read directly from Kohavi's own site. Section 6, "Pitfall 4," states almost verbatim what the check needs: *"Combining metrics over periods where the proportions assigned to Control and Treatment vary, or over subpopulations sampled at different rates"* — with a fully worked Simpson's-paradox example (Table 1) and three named remedies (paired comparison within stable-proportion periods; weighted combination; or discard the unstable-proportion period). Confirmed cleanly distinct from ratio-metric dilution (already permanently out of scope elsewhere in `brief.md` — no overlap risk). Ready for Phase 15 to cite Section 6 by name. |

**Requirement impact:** REQ-P15-02 has a D-05-confirmed citation, ready to implement. REQ-P15-04
is satisfied by its changing-denominator half only — Phase 15's S4-1 discuss must record this as
a loud, documented partial satisfaction (not a silent scope-narrowing) and confirm `brief.md`
§6.5 still carries the survivorship-bias item as an open, unpromoted entry.

### HQ-9 — Phase 13 end-of-phase security sign-off + UAT (answered 2026-08-29)

**Operator decision:** Approved — the recommended option (sign off `13-SECURITY.md` as
written and confirm the REQ-P13-01..06 UAT) was selected, on the strength of the loop's
orchestrator re-gate evidence: 14/14 threats closed, `threats_open: 0`, `nyquist_compliant: true`
with 6/6 requirements COVERED, full corpus gate green (1230 tests). No D-05 read was owed
(Phase 13 mints no codes). Recorded in `13-SECURITY.md`'s Sign-Off section.

### HQ-10 — Phase 14 end-of-phase security sign-off + UAT (answered 2026-08-29)

**Operator decision:** Approved — the recommended option (sign off `14-SECURITY.md` as
written and confirm the REQ-P14-01..06 UAT) was selected, on the strength of the loop's
orchestrator re-gate evidence: 16/16 register entries closed, `threats_open: 0`,
`nyquist_compliant: true` with 6/6 requirements COVERED (including the REQ-P14-05
documented-skip disposition — no GSD Core overlay hooks exist), full corpus gate green
(1243 tests). Recorded in `14-SECURITY.md`'s Sign-Off section.

### HQ-11 — Phase 16 D-06 numbering veto window: `DSX-REP-060` / `DSX-REP-061` (answered 2026-08-29)

**Operator decision:** Accepted the loop's numbering as filed — no veto exercised.
`DSX-REP-060` and `DSX-REP-061`, both **HIGH** severity, land in the `06x` REP band as
decided by the Architect + Auditor persona round (unanimous Option A).

### HQ-12 — Phase 16 end-of-phase security sign-off + UAT (answered 2026-08-29)

**Operator decision:** Approved — the recommended option (sign off `16-SECURITY.md` as
written and confirm the REQ-P16-01..04 UAT) was selected, on the strength of the loop's
orchestrator re-gate evidence: 13/13 register entries closed, `threats_open: 0`,
`nyquist_compliant: true` with 4/4 requirements COVERED, full corpus gate green
(1263 tests). No D-05 read was owed (the two new REP codes cite no primary source).
Recorded in `16-SECURITY.md`'s Sign-Off section.

### HQ-13 — Phase 15 D-06 numbering veto window: `DSX-EXP-070` / `DSX-MET-021` (answered 2026-08-29)

**Operator decision:** Accepted the loop's numbering and severity as filed — no veto
exercised. `DSX-EXP-070` ships **CRITICAL**, `DSX-MET-021` ships **HIGH** (not escalated
to CRITICAL). The open severity question the filing raised — whether the changing-denominator
bad fixture should block at `dsx gate plan` rather than only at verify/ship, which would have
forced CRITICAL — was resolved by accepting HIGH as the Architect + Statistician persona
round decided (orchestrator tie-break: a declaration-only check evidences a bucket-allocation
*shift*, not a confirmed sign *reversal*, so CRITICAL would overstate).

### HQ-14 — Phase 15 end-of-phase security sign-off + UAT (answered 2026-08-29)

**Operator decision:** Approved — the recommended option (sign off `15-SECURITY.md` as
written and confirm the REQ-P15-01..07 UAT) was selected, on the strength of the loop's
orchestrator re-gate evidence: 23/23 register entries closed, `threats_open: 0`,
`nyquist_compliant: true` with 7/7 requirements COVERED (REQ-P15-04 COVERED **PARTIAL**,
consistent with the HQ-8 decision), full corpus gate green (1312 tests). The D-06 numbering
veto for Phase 15's two new codes was granted separately as HQ-13. Recorded in
`15-SECURITY.md`'s Sign-Off section.

### HQ-15 — Close-out ship approval: complete milestone + merge to `main` + tag `v2.2.0` (answered 2026-08-29)

**Operator decision:** "Ship it — explicit named-branch merge (Recommended)" — the
recommended path was approved: verify on a throwaway branch first, then
`git merge --no-ff` the ceremony branch into `main` **by explicit name**, never the
generic `/gsd-complete-milestone` skill's auto-detected branch.

**Why the explicit-name caveat mattered:** before executing, the interactive session
found this repo carries 4 stale `gsd/*` branches from prior milestones
(`gsd/v1.1.0-milestone`, `gsd/v2.0.0-dsx-validity-frame`, `gsd/v2.0.0-milestone`).
`/gsd-complete-milestone`'s `handle_branches` step auto-detects "the milestone branch"
via `git branch --list "gsd/*" | head -1` (alphabetically first), which would have
silently merged `gsd/v1.1.0-milestone` instead of `gsd/v2.2.0-analytic-surface`. This
was caught and reported before running anything, and the ship proceeded with an
explicit, named merge instead of trusting that auto-detect.

**What was executed:**

1. Verified on a throwaway branch off `main` first: `git merge --no-ff
   gsd/v2.2.0-analytic-surface`, 0 conflicts; `sh scripts/check.sh` all green (1312
   tests, catalogue current, capability conformant, gate contract + determinism hold).
2. Real merge onto `main`: commit `c0656b1`. Full gate re-run green again on `main`.
3. Tagged `v2.2.0` (annotated) — confirmed by dereferencing the tag object, not
   assumed, that it points at `c0656b1`. Pushed `main` and the tag.
4. Ran `/gsd-complete-milestone`'s archival (`gsd-tools.cjs query milestone.complete
   v2.2`), then hand-corrected two of its output defects before committing: several
   generated accomplishment one-liners were truncated mid-sentence (replaced with
   accurate text from each phase's real SUMMARY.md), and the archived
   `v2.2-REQUIREMENTS.md` carried all 23 rows forward still `[ ]`/"(queued)" despite
   the milestone audit's own `passed` verdict (corrected to `[x]`/"(complete)" with an
   explanatory note, corroborated by `.planning/milestones/v2.2-MILESTONE-AUDIT.md`).
5. Completed the workflow's AI-only steps by hand: full PROJECT.md evolution review,
   ROADMAP.md reorganized (v2.2 collapsed into a shipped block), RETROSPECTIVE.md
   milestone section added.
6. Safety commit `4992bc6` (archive files + updated docs), then `git rm
   .planning/REQUIREMENTS.md` committed separately (`427372c`) per the workflow's own
   two-commit pattern — full gate re-run green after each. Both pushed to `main`.

**Result:** v2.2 Analytic Surface is fully shipped. `main` is at `427372c`, 0 ahead /
0 unpushed. LOOP-LEDGER.md S5-5 and S5-6 checked off — all 29 ledger units complete.
`gsd/v2.2.0-analytic-surface` is left in place (still the Scheduled Task's target
branch); a future firing against it will find every unit `[x]` and hold correctly.
