# HUMAN-QUEUE — items only you can answer

Milestone **v2.6 Exploration Depth and Backlog Evidence**. The loop keeps working
around these; it only blocks at the close-out stage (S7-2) if any remain.

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

### HQ-40 — v2.6 D-05 citation evidence pack (ANSWERED 2026-09-07 — all five rows read at their locators)

**Operator verdict, row by row.** Each locator below was actually opened and read
(not re-confirmed from the pack's own summary); three were read in full primary
text, one (40b) rests on convergent bibliographic/secondary corroboration after
nine failed attempts to open the ACM primary PDF directly (paywall/certificate/
binary-render failures across doi.org, dl.acm.org, ResearchGate, sci-hub,
archive.org, a TAU mirror, a stat.washington.edu mirror, and DBLP) — flagged as
such rather than silently upgraded to a primary read.

**40a — Hyndman & Fan (1996) — CONFIRMED, no correction.** Cross-checked the
paper's own Type 6 / Type 7 definitions (via a faithful secondary reproduction of
its table, since the ResearchGate host itself 403'd): Type 6 uses plotting
position i/(N+1) — the CPython `method="exclusive"` formula, confirmed verbatim
from the Python 3.12 docs read directly. Type 7 uses (i-1)/(N-1) — the CPython
`method="inclusive"` formula the profiler actually calls
(`dsx/profiler.py:122,388`, `statistics.quantiles(..., method="inclusive")`).
**The mapping the code already asserts (type 7 for the profiler's method) is
correct.** No change owed to `25-*` artifacts; Phase 25 is shipped and this closes
the citation paperwork only.

**40b — Kaufman, Rosset, Perlich & Stitelman (2012) — CONFIRMED (bibliography
primary-grade; definition secondary-corroborated, flagged).** Author list, venue
and locator confirmed exactly as proposed — *ACM Transactions on Knowledge
Discovery from Data*, **Vol. 6, No. 4, Article 15** (Dec. 2012) — independently via
Google Scholar's formatted citation record and ACM's own DL listing (convergent,
not a single source). The legitimacy definition — leakage as "the introduction of
information about the data mining target that should not be legitimately
available to mine from," operationalised in the paper as features observable
strictly before the target instance — appears identically across three
independent secondary indexes quoting the same sentence, but I could not open the
ACM PDF itself to read it first-hand (every route tried failed on a different
technical ground, listed above). **Given the loop's own D-13 measurement
(`27-MEASUREMENT.md`) already independently proved the gap in the code, not in
this citation, this is sufficient to unblock the mint** — proceed with
`DSX-ML-034` under this citation, but the phase's `# D-05:` marker should say
"secondary-corroborated, primary PDF paywalled" rather than claim a direct read,
so the record stays honest.

**Update 2026-09-11 — PRIMARY READ COMPLETED.** The operator supplied the ACM PDF
(DOI 10.1145/2382577.2382579, 21 pp.) and the interactive session read it. Identity
confirmed at p. 15:1 (title, all four authors, TKDD 6(4) Art. 15, Dec. 2012). The
definition is confirmed verbatim at the source: the abstract/§1 sentence quoted above;
Sec. 3.1 p. 15:8 — "We say a second observable v is u leakage legitimate if v is
observable to the client for the purpose of inferring u" (v ∈ legit{u}; trivial rule
y ∉ legit{y}, eq. 1); Sec. 3.2 p. 15:9, eq. (3) t{x} < t{y} ⇔ x ∈ legit{y} — "A
legitimate feature is an ordered set whose every element is observable to the client
earlier than its W-associated target element." That timing form is exactly the
boundary `DSX-ML-034`'s `after_prediction` branch encodes. Updated the same day: the
`DSX-ML-034` docstring, the `# D-05:` test marker, the catalogue-generator comment,
27-CONTEXT.md, 27-SECURITY.md T-27-03 (+ audit-trail row) and the literature record.
The secondary-corroborated status is now historical (2026-09-07 → 2026-09-11).

**40c vs 40d — CONFIRMED: cite 40c only, drop 40d.** Read Wilkinson & the Task
Force on Statistical Inference (1999) in full, primary text. It states the rule
unconditionally, three times: "Always present effect sizes for primary outcomes";
"Always provide some effect-size estimate when reporting a p value"; "Interval
estimates should be given for any effect sizes involving principal outcomes."
This is the direct, operational locator Phase 28's check should cite. 40d (APA
JARS–Quant) was read too, but only the **current 2024 web table** was reachable —
not the actual 2018 published article — and its wording is hedged ("effect sizes
and confidence intervals **or** statistical significance levels," "when
possible"), weaker than what the check enforces. **Do not cite 40d**: it is
either the wrong edition or a weaker rule than the one the code needs: use
Wilkinson & TFSI (1999) alone.

**40e — Gail & Simon (1985) — CONFIRMED, no correction.** Read the published
abstract directly (PubMed, PMID 4027319; *Biometrics* 41(2):361–372, June 1985;
authors Gail M, Simon R). Verbatim: "Qualitative or crossover interactions are
said to occur when one treatment is superior for some subsets of patients and the
alternative treatment is superior for other subsets." This is exactly the
opposite-sign-across-subsets definition Phase 29's `subgroup_harm` criterion
needs — proceed with the citation as proposed.

**Unblocked by this answer:** S3-1 (Phase 27, on 40b) may now close as a live
mint under `DSX-ML-034`; S4-1 (Phase 28, on 40c) may proceed citing Wilkinson &
TFSI (1999) alone; S5-1 (Phase 29, on 40e) may proceed. The Hyndman & Fan row
(40a) blocked nothing gate-side and closes Phase 25's citation paperwork only.

### HQ-41 — Phase 25 end-of-phase sign-off: security + UAT (filed 2026-09-07 by S1-5; non-blocking until S7-2)

**What this is.** Phase 25 (Hermetic profile depth) passed both verify:post gates
technically; two items need the operator's sign-off at close-out (S7-2), neither
blocking any earlier work.

1. **Security sign-off (SECURITY.md approval line — brief §4.4).** The loop re-gated
   all 8 threats at their code locators → **SECURED, `threats_open: 0`, 8/8 CLOSED**
   (`25-SECURITY.md`, `status: verified` technical). The Approval line is written but
   **unsigned** — the loop verifies mitigations, it does not sign. **To answer:** read
   `25-SECURITY.md`; confirm the register + the HIGH threat T-25-07 closure; approve.
2. **UAT round.** `25-VALIDATION.md` is `nyquist_compliant: true`, 0 gaps, all 3
   requirements COVERED by named tests (phase module 51/51 green on real 3.12.10).
   Phase 25 has no user-facing runtime behaviour beyond the CLI flags already tested,
   so its acceptance test IS the automated invariant set. **To answer:** confirm UAT
   accepted (or name a manual check to run).

An interactive session records both verdicts in the proper artifacts (SECURITY.md
Approval line; a UAT note) and checks this item off. **Non-blocking until S7-2.**

### HQ-42 — Phase 26 end-of-phase sign-off: security + UAT (filed 2026-09-07 by S2-5; non-blocking until S7-2)

**What this is.** Phase 26 (Per-skill read contracts) passed both verify:post gates
technically; two items need the operator's sign-off at close-out (S7-2), neither
blocking any earlier work. Phase 26 is skill-only — `dsx/` byte-identical, zero new
codes (276 → 276) — so the attack surface is drift and false read contracts, not
runtime input handling.

1. **Security sign-off (SECURITY.md approval line — brief §4.4).** The loop re-gated
   all 8 threats at their code locators on real Python 3.12.10 → **SECURED,
   `threats_open: 0`, 8/8 CLOSED** (`26-SECURITY.md`, `status: verified` technical):
   the read-contract guard fails loudly on any orphaned key (T-26-02) and never
   vacuous-passes on a CRLF mis-split (T-26-01); `dsx/`+`templates/` byte-identical
   and catalogue 276 → 276 (T-26-04); `node install.mjs --check` self-test passed
   (T-26-03); full suite 1590 OK (T-26-07). The Approval line is written but
   **unsigned** — the loop verifies mitigations, it does not sign. **To answer:** read
   `26-SECURITY.md`; confirm the register + the four HIGH threats (T-26-01/02/04 +
   the guard's discrimination); approve.
2. **UAT round.** `26-VALIDATION.md` is `nyquist_compliant: true`, 0 gaps, all 3
   requirements COVERED by named tests (`tests.test_skill_read_contracts` 7/7 green on
   real 3.12.10). Phase 26 has no user-facing runtime behaviour beyond the
   agent-facing skill prose and the static repo-integrity guard, so its acceptance
   test IS the automated invariant set. **To answer:** confirm UAT accepted (or name a
   manual check to run).

An interactive session records both verdicts in the proper artifacts (SECURITY.md
Approval line; a UAT note) and checks this item off. **Non-blocking until S7-2.**

### HQ-43 — Phase 27 end-of-phase sign-off: security + UAT (filed 2026-09-07 by S3-5; non-blocking until S7-2)

**What this is.** Phase 27 (Evidence case — feature-origin-only leak) passed both
verify:post gates technically; two items need the operator's sign-off at close-out
(S7-2), neither blocking any earlier work. Phase 27 mints one code (`DSX-ML-034`,
feature provenance) under a **secondary-corroborated** D-05 citation (Kaufman et al.
2012, HQ-40 row 40b — primary ACM PDF paywalled, flagged honestly) [**2026-09-11:
since read first-hand from the operator-supplied PDF — see the HQ-40 40b update**] and promotes a
corpus **MISS** fixture; the attack surface is provenance laundering, catalogue/count
tampering, and a fixture silently flipping MISS→CATCH — not runtime input handling.
`dsx/checks/dq.py` stays byte-frozen.

1. **Security sign-off (SECURITY.md approval line — brief §4.4).** The loop re-gated
   all 12 threats at their code locators on real Python 3.12.10 → **SECURED,
   `threats_open: 0`, 12/12 CLOSED** (`27-SECURITY.md`, `status: verified` technical):
   the D-05 docstring + `# D-05:` marker honestly record "secondary-corroborated,
   primary PDF paywalled" and claim no first-hand read (T-27-03 HIGH); the fixture
   declares no `feature_provenance` block and validates PASS/CRITICAL=0, so it stays an
   honest miss (T-27-01 HIGH); catalogue 276→277 with exactly one CRITICAL DSX-ML-034
   row (T-27-04); count pins 277 and spec count 43 moved in lockstep (T-27-02a/02b);
   DSX-ML-034 out of `_SECTION_65_BACKLOG_CODES`, sidecar id a frozen `_SECTION_65_ITEM_IDS`
   member (T-27-06/07); `dq.py` byte-frozen (T-27-09); full suite 1599 OK (T-27-10 golden
   re-measure); `node install.mjs --check` self-test passed (T-27-11). The Approval line is
   written but **unsigned** — the loop verifies mitigations, it does not sign. **To answer:**
   read `27-SECURITY.md`; confirm the register + the D-05 honesty threat T-27-03 and the
   MISS-integrity threat T-27-01; approve.
2. **UAT round.** `27-VALIDATION.md` is `nyquist_compliant: true`, 0 gaps, all 3
   requirements COVERED by named tests (phase module `tests.test_ml_feature_provenance`
   + `tests.test_known_bad_corpus` = 60/60 green on real 3.12.10; golden 6/6; full suite
   1599 OK). Phase 27 has no user-facing runtime behaviour beyond the declaration-only
   check and the corpus fixture, so its acceptance test IS the automated invariant set.
   **To answer:** confirm UAT accepted (or name a manual check to run).

An interactive session records both verdicts in the proper artifacts (SECURITY.md
Approval line; a UAT note) and checks this item off. **Non-blocking until S7-2.**

### HQ-44 — Phase 28 end-of-phase sign-off: security + UAT (filed 2026-09-08 by S4-5; non-blocking until S7-2)

**What this is.** Phase 28 (Evidence case — magnitude no test computed) passed both
verify:post gates technically; two items need the operator's sign-off at close-out
(S7-2), neither blocking any earlier work. Phase 28 mints one code (`DSX-CLM-034`,
claim→cited-test traceability) under a **human-confirmed** D-05 citation (Wilkinson &
TFSI 1999, read in full primary text — HQ-40 row 40c) and promotes a corpus **MISS**
fixture built on the collision/mislabel construction (the claim's 27%/18% are the REAL
reported numbers of OTHER metrics, so `DSX-CLM-033` clears while no test computed the
CLAIMED metric). The attack surface is D-05 over-claiming, catalogue/count tampering, a
fixture silently flipping MISS→CATCH, and the new `_PER_FIXTURE_INCIDENTAL_CODES` map
being abused — not runtime input handling. `dsx/checks/dq.py` stays byte-frozen.

1. **Security sign-off (SECURITY.md approval line — brief §4.4).** The loop re-gated
   all 14 threats at their code locators on real Python 3.12.10 → **SECURED,
   `threats_open: 0`, 14/14 CLOSED** (`28-SECURITY.md`, `status: verified` technical):
   the D-05 docstring + `# D-05:` marker cite Wilkinson & TFSI (1999) as the MOTIVATING
   PRINCIPLE only and disclaim any numeric-overlap mandate (T-28-01 HIGH); the fixture
   declares no `supported_by` and validates PASS/CRITICAL=0, so the magnitude miss stays
   honest (T-28-08 HIGH); catalogue 277→278 with exactly one `DSX-CLM-034 | HIGH` row
   (T-28-02/04); the mint lives in a brand-new function, not the uncited shared one
   (T-28-03 HIGH); DSX-CLM-034 out of `_SECTION_65_BACKLOG_CODES`, sidecar id a frozen
   `_SECTION_65_ITEM_IDS` member (T-28-09/10); the golden ship set is re-measured live
   (T-28-12); `dq.py` byte-frozen (T-28-06); spec count 44 (T-28-11); full suite 1615 OK;
   `node install.mjs --check` self-test passed (T-28-13). The Approval line is written but
   **unsigned** — the loop verifies mitigations, it does not sign. **To answer:** read
   `28-SECURITY.md`; confirm the register + the D-05 honesty threat T-28-01 and the
   MISS-integrity threat T-28-08; approve.
2. **UAT round.** `28-VALIDATION.md` is `nyquist_compliant: true`, 0 gaps, all 3
   requirements COVERED by named tests (phase modules `tests.test_claims_supported_by` +
   `tests.test_known_bad_corpus` = 67/67 green on real 3.12.10; fixture `dsx validate`
   PASS CRITICAL=0; full suite 1615 OK). Phase 28 has no user-facing runtime behaviour
   beyond the declaration-only check and the corpus fixture, so its acceptance test IS
   the automated invariant set. **To answer:** confirm UAT accepted (or name a manual
   check to run).

An interactive session records both verdicts in the proper artifacts (SECURITY.md
Approval line; a UAT note) and checks this item off. **Non-blocking until S7-2.**

### HQ-45 — Phase 29 end-of-phase sign-off: security + UAT (filed 2026-09-08 by S5-5; non-blocking until S7-2)

**What this is.** Phase 29 (Evidence case — subgroup harm under a prescriptive
recommendation) passed both verify:post gates technically; two items need the
operator's sign-off at close-out (S7-2), neither blocking any earlier work. Phase 29
mints one code (`DSX-COH-041`, subgroup-harm disposition obligation) under a
**human-confirmed** D-05 citation (Gail & Simon 1985, read at its locator in full —
HQ-40 row 40e) and promotes the corpus's **FIRST `kind: target`** fixture — the
load-bearing inverse of the Phase-27/28 permanent misses (D-29-00): the newly-minted
code is PRESENT and fires CRITICAL at plan/verify/ship. The attack surface is D-05
over-claiming (laundering Gail & Simon's motivating definition into an asserted
likelihood-ratio mechanic), catalogue/count tampering, a frozen case widened to
manufacture a miss, a fixture silently gaining a `decision.subgroup_harm[]` row
(flipping the honest TARGET into a silenced case), and the new `kind: target`
vocabulary mis-routing a code — not runtime input handling. `dsx/checks/dq.py` and
`dsx/cli.py` stay byte-frozen.

1. **Security sign-off (SECURITY.md approval line — brief §4.4).** The loop re-gated
   all 15 threats at their code locators on real Python 3.12.10 → **SECURED,
   `threats_open: 0`, 15/15 CLOSED** (`29-SECURITY.md`, `status: verified` technical):
   the D-05 docstring + `# D-05:` marker cite Gail & Simon (1985) as the MOTIVATING
   DEFINITION only and disclaim the likelihood-ratio mechanic (T-29-02 HIGH); the
   fixture declares `subgroup_harm_floor: 500` and deliberately omits the
   `subgroup_harm[]` disposition row, so the missing-row CRITICAL fires — an honest
   TARGET (T-29-08 HIGH); catalogue 278→279 with the DSX-COH-041 row (T-29-03); the
   mint lives in a brand-new function `_check_subgroup_harm_disposition` (T-29-04 HIGH);
   DSX-COH-041 out of `_SECTION_65_BACKLOG_CODES`, sidecar id a frozen `_SECTION_65_ITEM_IDS`
   member (T-29-09); the `kind` vocabulary is `("miss","caught","target")` and
   DSX-COH-041 is wired in `_TARGET_DEFECT_CODES` at plan/verify/ship (T-29-10 HIGH); the
   golden ship set is re-measured live (T-29-12); `_ABSENT_PARTITION_FLOOR` stays 3
   (T-29-14); `dq.py`+`cli.py` byte-frozen (T-29-06/07); spec count 45 (T-29-11); full
   suite 1627 OK; `node install.mjs --check` self-test passed (T-29-13). The Approval
   line is written but **unsigned** — the loop verifies mitigations, it does not sign.
   **To answer:** read `29-SECURITY.md`; confirm the register + the D-05 honesty threat
   T-29-02 and the TARGET-integrity threat T-29-08; approve.
2. **UAT round.** `29-VALIDATION.md` is `nyquist_compliant: true`, 0 gaps, all 3
   requirements COVERED by named tests (phase modules `tests.test_subgroup_harm_disposition`
   + `tests.test_known_bad_corpus` = 72/72 green on real 3.12.10; fixture `dsx validate`
   PASS CRITICAL=0; full suite 1627 OK). Phase 29 has no user-facing runtime behaviour
   beyond the declaration-only check and the corpus TARGET fixture, so its acceptance
   test IS the automated invariant set. **To answer:** confirm UAT accepted (or name a
   manual check to run).

An interactive session records both verdicts in the proper artifacts (SECURITY.md
Approval line; a UAT note) and checks this item off. **Non-blocking until S7-2.**

### HQ-46 — Phase 30 end-of-phase sign-off: security + UAT (filed 2026-09-10 by S6-5; non-blocking until S7-2)

**What this is.** Phase 30 (Calibration re-baseline, terminal) passed both verify:post
gates technically; two items need the operator's sign-off at close-out (S7-2), neither
blocking any earlier work. Phase 30 **measures** the grown corpus (42 known-bad + 15
good-control) with the three v2.6 cases classified from the committed harness wiring
(2 misses DSX-ML-034/DSX-CLM-034 + 1 target DSX-COH-041) and **mints zero codes**
(set-identity 279 → 279). It designs nothing. The attack surface is record integrity —
a readout number drifting from a measured value, an FPR of 0/15 dressed as a ~0 point
estimate, a frozen gate module/fixture/catalogue silently reshaped, a stale doc claim
left un-pinned, a `kind: target` case double-counted into the headline — not runtime
input handling. `dsx/` (incl. `dq.py`, `cli.py`, `viz.py`), `examples/` and
`references/finding-codes.md` stay byte-frozen for the whole phase.

1. **Security sign-off (SECURITY.md approval line — brief §4.4).** The loop re-gated
   all 11 threats at their code locators on real Python 3.12.10 → **SECURED,
   `threats_open: 0`, 11/11 CLOSED** (`30-SECURITY.md`, `status: verified` technical):
   the three CRITICAL threats are closed at the byte level — frozen-surface `git diff`
   **empty** for `dsx/`+`examples/`+`references/finding-codes.md` (T-30-03), catalogue/
   fixtures/`dq.py`/`viz.py` byte-frozen + invariant "code SET == frozen Phase-12
   snapshot + sanctioned mints" (T-30-09), and set-identity **279 → 279** re-measured,
   not assumed (T-30-11 zero-mint); the readout numbers equal measured values,
   reproduced live by `test_stratified_catch_rate_and_fpr_report` **OK** (T-30-01); FPR
   0/15 is reported as a bounded observation with its one-sided 95% upper bound ≈0.181,
   never a ~0 point estimate, and no interval is quoted on the construction-invariant
   miss-rate (T-30-02); the doc re-baselines name the three v2.6 codes and flip
   39→42 with the new agreement test pinning doc==live (T-30-06/07/08); full suite
   **1629 OK** (no skips), `node install.mjs --check` self-test passed, `scripts/check.sh`
   all passed (T-30-04/10). The Approval line is written but **unsigned** — the loop
   verifies mitigations, it does not sign. **To answer:** read `30-SECURITY.md`; confirm
   the register + the three CRITICAL freeze/zero-mint threats and the two HIGH
   record-integrity threats (T-30-01, T-30-02); approve.
2. **UAT round.** `30-VALIDATION.md` is `nyquist_compliant: true`, 0 gaps, all 3
   requirements COVERED by named tests (reproducer + `tests.test_literature_corpus_count_agreement`
   + `tests.test_finding_catalogue_invariant` green on real 3.12.10; full suite 1629 OK;
   `scripts/check.sh` all passed). Phase 30 has no user-facing runtime behaviour beyond
   the declaration-only doc records and the static agreement guard, so its acceptance test
   IS the automated invariant set. **To answer:** confirm UAT accepted (or name a manual
   check to run).

An interactive session records both verdicts in the proper artifacts (SECURITY.md
Approval line; a UAT note) and checks this item off. **Non-blocking until S7-2.**

## Will be added by the loop when reached

- ~~S0-3: the v2.6 D-05 citation evidence pack~~ — **FILED as HQ-40 (2026-09-06)**,
  see Open above. Non-blocking for Phases 25–26; the Kaufman/Wilkinson-or-JARS/Gail
  rows block S3-1, S4-1 and S5-1 respectively.
- Phase 25/26/27/28/29/30 end-of-phase security sign-off + UAT rounds (batched per
  phase; non-blocking until S7-2). **Phase 25 filed as HQ-41; Phase 26 filed as HQ-42;
  Phase 27 filed as HQ-43 (all 2026-09-07); Phase 28 filed as HQ-44; Phase 29 filed as
  HQ-45 (both 2026-09-08); Phase 30 filed as HQ-46 (2026-09-10) — all six phase
  sign-offs now batched to S7-2.**
- D-06 numbering veto windows for any code Phases 27–29 mint, and for any number
  reserved in `_SECTION_65_BACKLOG_CODES` for a miss sidecar (from a freshly
  re-measured live catalogue count; silence = accept).
- Phase 29's documented subgroup-harm case source, if research finds one whose
  authenticity needs a human read.
- The S7-6 ship decisions: merge to `main` and the `v2.6.0` release tag, together
  with the S7-5 interactive-complete step, after S7-4's audit PASSES.
- Any persona decision the operator vetoes from a daily summary.

## Standing framework notes (not queue items — nothing to answer, just remember)

**`/gsd-audit-uat`'s automated CLI under-reports human-verification items —
multiple documented defects.** (1) `gsd-core/bin/lib/uat.cjs::parseVerificationItems`
only recognizes a level-2 `## Human Verification` heading while the verifier
template writes level-3 `### Human Verification Required` (found v2.0.0).
(2) `uat.cjs:78` filters on `f.includes('-VERIFICATION')`, which matches this
project's `NN-VERIFICATION.md` naming but not a bare `VERIFICATION.md` — check
which convention the current milestone's phases use before trusting the CLI's
file discovery. (3) The frontmatter-status gate only emits a verification file
when `status ∈ {human_needed, gaps_found}`; a phase whose VERIFICATION.md
carries `verdict: PASSED` with no `status:` key resolves to `status:unknown`
and is silently dropped (found v2.3 S5-1). **At S7-1, never accept the CLI's
"all clear" — hand-check every phase's verification file directly.**

**`check.decision-coverage-plan` false-blocks on this project's CONTEXT.md
decision-bullet style (found v2.3 S1-2).** The plan-phase decision-coverage
gate's regexes expect `- **D-NN:** …` (colon-immediate) or an em-dash inside
the bold; this project's discuss rounds write `- **D-06 range
pre-allocation** — one …` (title inside the bold, separator after the closing
`**`), matching none of the regexes → `total:0, reason:"could-not-parse"`. This
is a parser format-mismatch, **not** an uncovered decision — the
`gsd-plan-checker`'s Dimension-7 (Context Compliance) substantively verifies the
same property. **At every phase plan gate, do NOT treat a could-not-parse/
total:0 result as a real coverage gap** — confirm via the plan-checker Dim-7
pass instead.

**`init.manager`'s `verification_status` can read "missing" for a genuinely
verified phase (found v2.3 close-out; confirmed again at v2.4's).** Same class of
naming-convention blind spot as the audit-uat issues, on a different code path. If
it happens again, read the actual verification file directly before treating it as
a real gap.

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete conflicts on v2.0.0's 707-commit
branch and was abandoned mid-run. Ship by direct 3-way merge.

**Ship by EXPLICIT branch name — never the framework's auto-detect.** This repo
now carries six stale `gsd/*` branches from prior milestones (`v1.1.0-milestone`,
`v2.0.0-dsx-validity-frame`, `v2.0.0-milestone`, `v2.2.0-analytic-surface`,
`v2.3.0-test-catalog`, `v2.4.0-visual-excellence`); `/gsd-complete-milestone`'s
`handle_branches` picks the alphabetically-first `gsd/*` branch, which is always
wrong here (found and bypassed at v2.2, v2.3 and v2.4 ship).
`git merge --no-ff gsd/v2.6.0-exploration-depth` by name, verified on a throwaway
branch first.

**`gsd-tools query commit` (used by GSD planner/researcher/executor subagents)
auto-creates the wrong branch mid-run — recurring, budget for it.** Confirmed
three times in v2.4: when a `gsd-*` subagent commits via `gsd-tools query commit`,
it can create + switch to a stray branch (v2.4's was `gsd/v2.4-visual-excellence`,
**no `.0`**) and land the commit there instead of the canonical branch; the
subagent's own return then confidently **misreports** the branch/push state.
**Guarded automatically since 2026-09-07 by `scripts/gsd-reconcile-branch.ps1`**,
which `run-ceremony-firing.ps1` now runs after every headless firing (win or
lose): it records the canonical branch's tip before the firing starts, then
afterward finds any local branch whose tip descends from that recorded point —
ancestry, not name, is the filter, so it never touches the six-and-counting
genuinely stale `gsd/*` branches from prior milestones — and folds a clean
fast-forward case back into canonical, deleting the stray, no commit lost.
Proven against six scripted scenarios before being wired in (stray off
canonical, HEAD literally left on the stray, a clean tree with nothing to
recover, a genuinely diverged stray, an old stale branch that must stay
untouched, and a dirty tree). A real divergence (not the common case) is left
alone and reported (exit 1) — a human reconciles that one by hand, same as
before this guard existed: `git rev-parse --abbrev-ref HEAD` + `git branch -vv`,
then `git checkout` canonical → `git merge --ff-only <stray>` → `git branch -d`
the stray → push. **Also runs standalone**, for the same bug hitting an
interactive `/gsd-execute-phase` or `/gsd-plan-phase` outside the headless loop:
`pwsh scripts/gsd-reconcile-branch.ps1 -Branch <canonical>` (defaults
`BaselineRef` to `origin/<canonical>` when run by hand). This is exactly why the
loop uses plain `git commit` for orchestrator-authored files, and why the
`gsd/*` count must be re-asserted (6 stale + 1 active) every planning firing.

**Release tags: never force-move a published one.** v2.0.0 shipped as tag
`v2.1.0` for this reason; v2.2 as `v2.2.0`; v2.3 as `v2.3.0`; v2.4 as `v2.4.0`;
`v2.4.1` and `v2.5.0` were interactive releases. The next free tag for this
milestone is `v2.6.0`.

**`/gsd-complete-milestone` output needs hand-verification — recurring at every
close so far.** At v2.2's, v2.3's and v2.4's close, its generated accomplishment
bullets were truncated mid-sentence or captured YAML frontmatter instead of
prose, STATE.md's generated body contradicted its own frontmatter, and the
archived REQUIREMENTS.md carried all rows forward still unchecked despite the
passed audit — all needed hand-correction each time. Budget for this as a standing
cost, not a surprise. Also: it is NOT headless-safe (interactive prompts +
`git rm REQUIREMENTS.md`) — interactive session only.

**Run the full suite from a clean tree, on the real interpreter.** A stray root
`DECISIONS.jsonl` false-fails two `explain` tests
(`tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`,
`tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`);
if exactly these two fail: `rm -f DECISIONS.jsonl examples/DECISIONS.jsonl
examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl` and re-run. A bare
`python3` on this machine can resolve to a package-less stub (Python 3.14.6) that
reports the matplotlib determinism test as *skipped*; the real interpreter is
`C:\Users\Benutzer1\AppData\Local\Programs\Python\Python312\python.exe`.

**`node install.mjs --check` is now a real gate (fixed in v2.5.0).** Before
2026-09-06 its self-test ran `gate ship` alone and had failed on every fresh install
since Phase 10, and the installer shipped the gitignored `examples/DECISIONS.jsonl`
into the overlay; both fixed. Installed skill/agent copies had silently drifted
from the repo for two weeks. Every phase that touches `skills/`, `agents/`,
`templates/` or `references/` ends with `node install.mjs` and a passing `--check`.

**Usage-limit backoff is the wrapper's job — proven working in production.**
`scripts/run-ceremony-firing.ps1` detects limit hits, writes
`.planning/loop-logs/.backoff-until`, and re-probes every 30 minutes during a
hold with one trivial `claude -p` call to catch an early release rather than
blindly waiting the full window. Firings: log one line, stop, never retry-loop,
never touch the backoff/probe-marker files. The pause switch
`.planning/loop-logs/.paused` is the operator's; the loop never creates or removes it.

**A firing that finds uncommitted, ledger-inconsistent changes at start should
hold, not act.** Confirmed working at v2.3's close: a firing found an
interactive session's in-progress `/gsd-complete-milestone` work uncommitted in
the tree and correctly left it untouched (neither committed nor discarded),
logging the observation instead. This is the correct behavior, not a bug to fix.

## Answered

### HQ-39 — v2.6 scope: open the milestone with both halves (answered 2026-09-06 — operator direction; reverses HQ-38)

**Operator verdict: "Both: EDA depth + paper evidence."** Asked after the operator
directed that the ceremony run rather than stay paused. Three options were offered
in the decision-block shape: both halves (~6 phases), EDA depth only (~3), paper
evidence only (~4). The operator chose both. Consequences, all recorded:

- **SEED-002 promoted** (Phase 25) — this reverses **HQ-38**, answered hours earlier
  the same day, which had held the seed on its unmet D-13 entry condition. The
  reversal is by operator direction with a stated reason (the portfolio work starting
  now should consume hash-bound numbers from its first phase rather than produce the
  evidence first); the seed carries both decisions in order.
- **SEED-001 E-26 promoted** (Phase 26), its entry condition likewise overridden by
  direction; E-27 … E-31 unchanged.
- **§6.5 items 7, 8, 9 get their corpus cases built and measured** (Phases 27–29)
  under the brief's D-13 rule: a case the gate already catches closes its phase with
  no mint. Nothing is promoted by this answer; only the evidence is commissioned.
- Terminal calibration re-baseline (Phase 30). Ships as `v2.6.0`.

Recorded in `.planning/research/V2.6-SCOPE.md`, `REQUIREMENTS.md`, the seeds, and
STATE.md. The v2.4 queue (HQ-27 … HQ-38) is archived at
`.planning/milestones/v2.4-HUMAN-QUEUE.md`; numbering continues from HQ-40.
