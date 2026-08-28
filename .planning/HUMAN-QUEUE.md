# HUMAN-QUEUE — items only you can answer

Milestone **v2.2 Analytic Surface**. The loop keeps working around these; it only
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

- Phase 13 / 14 / 16 end-of-phase UAT rounds and security sign-offs (batched per phase).
- Any D-06 numeric finding-code veto window — expected from Phase 15 (S4-1) and
  possibly Phase 16 (S3-1, if its gate check mints a `DSX-REP-*` code).
- The S5-6 ship decisions: merge to `main` and the `v2.2.0` release tag.
- Any persona decision the operator vetoes from a daily summary.

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

## Answered

(v2.0.0's answered items — HQ-1 … HQ-7 — are archived at
`.planning/milestones/v2.0.0-HUMAN-QUEUE.md` and
`.planning/milestones/v2.0.0-HUMAN-QUEUE-ARCHIVE.md`.)
