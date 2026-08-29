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

### HQ-13 — Phase 15 D-06 numbering veto window: `DSX-EXP-070` / `DSX-MET-021` (non-blocking; veto via daily summary or by S5-2)

**Status: filed 2026-08-29 (S4-1). Decided by the loop's persona round; NOT a blocker.** Per brief §4,
D-06 numeric finding-code assignments are decided by the loop ("next free number in family,
catalogue-consistent") and recorded loudly — not escalated. This entry is the operator's **veto window**
before Phase 15 ships. The loop proceeds through S4-2..S4-5 unless vetoed.

**What the loop decided (Architect + Statistician 2-persona round, both opus/high; full rationale in
`.planning/phases/15-cuped-and-bi-declaration-checks-new-codes-d-05/15-CONTEXT.md` D-02/D-03):**

| Code | Severity | Finding (fixed plain text; finalised at S4-3) | Citation (D-05, confirmed via HQ-8) |
|---|---|---|---|
| `DSX-EXP-070` | CRITICAL | CUPED declared with a covariate that is not pre-experiment. | Deng, Xu, Kohavi & Walker (2013), WSDM '13, pp.123-132. |
| `DSX-MET-021` | HIGH | Metric pooled across buckets sampled at different rates with no reweighting declared. | Crook, Frasca, Kohavi & Longbotham (2009), KDD '09, §6 Pitfall 4. |

- **Why these numbers:** `EXP-070` is the next free EXP band (design-correctness, not the SPEC-044 vocab
  question); `MET-021` is the free slot adjacent to its closest sibling `DSX-MET-020` in the 02x
  denominator band. Catalogue moves **258 → 260** additively; the frozen Phase-12 snapshot (256) is not
  mutated.
- **Why MET not INT for changing-denominator:** the DSX-INT family lives in the causal-gated
  `dsx/frame/interference.py` (runs only for causal/prescriptive/experiment specs) and would silently
  skip the descriptive/diagnostic cohort/funnel BI specs REQ-P15-03 targets. MET runs unconditionally.
- **Why MET-021 is HIGH not CRITICAL** (the one persona split, orchestrator tie-break rigour>reliability):
  a declaration-only check can only evidence that the bucket allocation *shifted*, not that the pooled
  result's sign *reversed*; CRITICAL would overstate. HIGH matches the sibling HIGH `DSX-MET-020`
  denominator code and still blocks the bad fixture at verify/ship. **Open item for the operator:** if you
  intended the changing-denominator bad fixture to block at `dsx gate plan` (not just verify/ship), that
  forces CRITICAL — say so in the daily summary and the loop re-numbers before S4-2 locks.
- **Survivorship-bias code is NOT minted** — its citation (Brown et al. 1992) does not transfer (your
  answered HQ-8); it stays in `brief.md` §6.5 with a falsifiable D-13 entry condition. REQ-P15-04 therefore
  ships PARTIAL (changing-denominator half only); the REQUIREMENTS.md wording change is queued to S4-4.
- **No D-05 primary-source read owed at discuss** — both shipping citations were read and confirmed by you
  at their locators in answered HQ-8.

**Operator action (optional):** veto or amend the numbering/severity via the daily summary, or confirm at
the S5-2 drain. Silence = accept. Nothing downstream blocks on this.

### HQ-11 — Phase 16 D-06 numbering veto window: `DSX-REP-060` / `DSX-REP-061` (non-blocking; veto via daily summary or by S5-2)

**Status: filed 2026-08-29 (S3-1). Decided by the loop's persona round; NOT a blocker.** Per brief §4,
numeric finding-code assignments (D-06, irreversible) are decided by the loop using "next free number in
family, catalogue-consistent" and recorded loudly — *not* escalated. This entry exists only so the operator
has an explicit **veto window** before Phase 16 ships. The loop proceeds through S3-2..S3-5 unless vetoed.

**What the loop decided (Architect + Auditor 2-persona round, both opus/high, unanimous Option A — full
rationale in `.planning/phases/16-re-run-verification-off-the-gate-path/16-CONTEXT.md` D-06):**

| Code | Severity | Finding (final text finalised at S3-3) |
|---|---|---|
| `DSX-REP-060` | HIGH | Reproduce report declared (`reproducibility.reproduce_report`) but `REPRO-REPORT.md` is missing — the reproduced verdict is unsubstantiated. |
| `DSX-REP-061` | HIGH | `REPRO-REPORT.md` present but its declared re-run numbers do not overlap `results.tests` — the analysis does not reproduce. |

- **Why mint (not reuse):** none of the 11 existing `DSX-REP-*` codes names "report missing" or "declared
  numbers don't overlap"; reusing one emits false text and the catalogue dedupes by code, hiding the drift.
- **Why in Phase 16 (not moved to Phase 15):** keeps the reproduce skill + its enforcing gate in one phase
  (no trust-without-enforcement window); Phase 15's codes carry D-05 statistical citations — these are
  engineering-hygiene checks with none.
- **Band:** `06x` is the next free block in the REP family (max was `DSX-REP-053`), catalogue-consistent
  (06x = reproduce-report). Both HIGH because verify/ship blocks only at HIGH.
- **Consequence recorded:** ROADMAP's "Phase 15 is the only phase that extends the catalogue" was amended
  (D-07) — Phase 15 **and** 16 extend it. No requirement dropped/reworded. Catalogue moves 256 → 258
  additively; the frozen Phase-12 snapshot anchor is not mutated.
- **No D-05 owed by Phase 16** (its codes cite no primary source; brief.md line 389 assigns none).

**Operator action (optional):** veto or amend the numbering via the daily summary, or confirm at the S5-2
drain. Silence = accept. Nothing downstream blocks on this.

### HQ-9 — Phase 13 end-of-phase security sign-off + UAT (batched; non-blocking until S5-2)

**Status: filed 2026-08-28 (S1-5). Technical gates PASS; awaiting operator sign-off.** Per brief §4
category 4 (a `SECURITY.md` approval line is a human item) and the standing UAT batch. The loop
completed the technical verification; the operator confirms the sign-off line at the close-out drain
(S5-2). Nothing downstream blocks on this until then.

**What the loop already verified (orchestrator re-gate, real commands — brief §5):**
- **Security — SECURED, `threats_open: 0`** (`13-SECURITY.md`): 14/14 threats closed. Gate-path
  purity (zero `dsx/`|`scripts/` edits), route-and-cite discipline (anti-parallel-advice grep 0 lines
  ×5 files), zero-mint set-identity (catalogue 256, `added=[] removed=[]`, `--check` exit 0), D-05
  advisory boundary (`dsx-scope-analysis` emits `gsd-tier.ps1`, no config mutation). Skill-only phase,
  asvs_level 1 L1 short-circuit — no auditor spawn needed.
- **Validation — `nyquist_compliant: true`, 0 gaps** (`13-VALIDATION.md`): 6/6 REQ-P13-01..06 COVERED
  by green automated tests (`tests/test_phase13_playbooks.py` 8 tests + `test_finding_catalogue_invariant`
  2 tests). Full gate `sh scripts/check.sh` = all passed (Ran 1230 tests OK).

**Operator action at S5-2:** (1) confirm the `13-SECURITY.md` Sign-Off approval line as written (or
flag any threat disposition), and (2) run/confirm the Phase 13 UAT for REQ-P13-01..06. There is **no
D-05 primary-source read owed by Phase 13** (it mints no codes and cites only existing ones — all 28
citations verified present). An interactive session records the verdict and checks this item off.

### HQ-10 — Phase 14 end-of-phase security sign-off + UAT (batched; non-blocking until S5-2)

**Status: filed 2026-08-28 (S2-5). Technical gates PASS; awaiting operator sign-off.** Per brief §4
category 4 (a `SECURITY.md` approval line is a human item) and the standing UAT batch. The loop
completed the technical verification; the operator confirms the sign-off line at the close-out drain
(S5-2). Nothing downstream blocks on this until then.

**What the loop already verified (orchestrator re-gate, real commands — brief §5):**
- **Security — SECURED, `threats_open: 0`** (`14-SECURITY.md`): 16/16 register entries closed (15
  threats + 1 supply-chain accept; 7 at high severity). Gate-path purity (empty `dsx/`+`scripts/`+
  `capability.json` manifest diff over the 5 feature commits; `report.add` cli.py=0), zero-mint
  set-identity (256, `added=[] removed=[]`, `--check` exit 0), gate-path hermeticity (`test_gate_path_hermetic`
  2 OK), documented-skip honesty (`hooks:[]`, no `aliases` key, `supported:["*"]`, DSX-DQ-001 named),
  disclosure guarded on literal `research`, Triggers on 13/13 skills, `data_storage` 0 in skills/shims.
  Doc/skill/template phase, asvs_level 1 L1 short-circuit — no auditor spawn needed.
- **Validation — `nyquist_compliant: true`, 0 gaps** (`14-VALIDATION.md`): 6/6 REQ-P14-01..06 COVERED
  by green automated tests (`tests/test_phase14_onboarding.py` 11 tests + `test_gate_path_hermetic` 2 +
  `test_finding_catalogue_invariant` 2). Full gate `sh scripts/check.sh` = all passed (Ran 1243 tests OK).

**Operator action at S5-2:** (1) confirm the `14-SECURITY.md` Sign-Off approval line as written (or
flag any threat disposition), and (2) run/confirm the Phase 14 UAT for REQ-P14-01..06. There is **no
D-05 primary-source read owed by Phase 14** (it mints no codes and cites only the existing `DSX-DQ-001`
— verified present). An interactive session records the verdict and checks this item off.

### HQ-12 — Phase 16 end-of-phase security sign-off + UAT (batched; non-blocking until S5-2)

**Status: filed 2026-08-29 (S3-5). Technical gates PASS; awaiting operator sign-off.** Per brief §4
category 4 (a `SECURITY.md` approval line is a human item) and the standing UAT batch. The loop
completed the technical verification; the operator confirms the sign-off line at the close-out drain
(S5-2). Nothing downstream blocks on this until then. The Phase 16 D-06 numbering veto is tracked
**separately** as HQ-11 (same drain).

**What the loop already verified (orchestrator re-gate, real commands — brief §5):**
- **Security — SECURED, `threats_open: 0`** (`16-SECURITY.md`): 13/13 register entries closed (12
  threats + 1 supply-chain accept; 3 critical + 8 high). Gate-path purity (`git diff ec216b2..HEAD
  -- dsx/ scripts/` = only `dsx/checks/repro.py`, stdlib `math`/`re`/`pathlib` only — no execution
  primitive), entrypoint-execution guard (`test_no_entrypoint_execution` 3 OK, AST scan + pos/neg
  controls), gate-path hermeticity (`test_gate_path_hermetic` 2 OK), verdict-agnostic + honest-skip
  (`test_reproduce_report` 7 OK), zero-drift catalogue (invariant 2 OK = 258 + set-identity vs
  snapshot ∪ {060,061}; `--check` exit 0; frozen anchor byte-unchanged), additive calibration
  (`test_known_bad_corpus` 45 OK; known-bad `ANALYSIS-SPEC.yaml` diff empty). Skill/template/test
  phase, asvs_level 1 L1 short-circuit — no auditor spawn needed.
- **Validation — `nyquist_compliant: true`, 0 gaps** (`16-VALIDATION.md`): 4/4 REQ-P16-01..04 COVERED
  by green automated tests (`tests/test_phase16_reproduce.py` 9 + `test_reproduce_report` 7 +
  `test_no_entrypoint_execution` 3 + `test_known_bad_corpus` 45). Full gate `sh scripts/check.sh` =
  all passed (Ran 1263 tests OK).

**Operator action at S5-2:** (1) confirm the `16-SECURITY.md` Sign-Off approval line as written (or
flag any threat disposition), and (2) run/confirm the Phase 16 UAT for REQ-P16-01..04. There is **no
D-05 primary-source read owed by Phase 16** — its two new codes (`DSX-REP-060`/`061`) are
engineering-hygiene checks that cite no primary source (brief.md line 389 assigns none). The D-06
numbering veto for those codes is HQ-11. An interactive session records the verdict and checks this
item off.

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

