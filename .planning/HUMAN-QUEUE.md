# HUMAN-QUEUE — items only you can answer

Milestone **v2.4 Visual Excellence**. The loop keeps working around these; it only
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

### HQ-28 — Phase 21 discuss persona decisions (veto window, filed S1-1, 2026-09-03)

**Type:** persona-decision veto window (brief §4 — recorded loudly, **non-blocking**;
silence = accept). **Not** a scope change, not a sign-off. Full rationale in
`.planning/phases/21-viz-vocabulary-reconciliation/21-CONTEXT.md` (D-01, D-02).

Two decisions the loop made for you to veto if you disagree:

- **D-01 (invariant scope).** The every-mark-has-a-home invariant is a repo-integrity
  test (off the gate path) with two clauses: capability-completeness for all non-banned
  marks, and relationship-completeness *or* an explicit frozen `CAPABILITY_ONLY`
  allowlist. "Capability home" is defined gate-faithfully as `CHART_CAPABILITIES ∪
  EXTRA_MARKS`. **Finding beyond S0-2:** `population_pyramid`/`butterfly` are
  relationship-orphans only (not double orphans — capability-homed via `EXTRA_MARKS[IT011]`);
  ~14 capability-only marks (`column`, `grouped_bar`, `bubble`, …) lack a relationship
  home and are documented-exempt, not homed (promotion deferred to Phase 22).
- **D-02 (refusal entries).** `BANNED_TYPES` enriched **in place** to
  `{reason, code, citation}` records (single registry, no drift surface), not a parallel
  sub-map. Refusal citations = HQ-27 Tier-3, batched to S5-2, non-blocking.

### HQ-29 — Phase 21 end-of-phase security sign-off (filed S1-5, 2026-09-02)

**Type:** security sign-off — a `SECURITY.md` approval line (brief §4 item 4). The
loop verified the mitigations; it may not self-sign the approval. **Non-blocking**
for Phase 21 advancement; must be signed by **S5-2** close-out.

**File:** `.planning/phases/21-viz-vocabulary-reconciliation/21-SECURITY.md`
(State B create; `status: verified`, `threats_open: 0`, ASVS L1).

**What the loop verified (machine gate, re-run by the orchestrator — not trusted):**
all three plan-time threats CLOSED by in-tree tests, re-run GREEN 2026-09-02:

| Threat | Category | Mitigation (test) | Re-run |
|---|---|---|---|
| T-21-01 | Tampering | every-mark-has-a-home invariant (`TestEveryMarkHasAHome`) | GREEN |
| T-21-02 | Repudiation | refusal-record completeness + code identity (`TestRefusalEntryCompleteness`, code=DSX-VIZ-001) | GREEN |
| T-21-03 | Tampering | zero-mint set-identity (`test_finding_catalogue_invariant` + `test_gen_finding_catalogue`, 275→275) | GREEN |

No threat rises to `high`; nothing blocks under ASVS-L1 block-on-`high`. No new
packages → no supply-chain gate. **UAT note:** Phase 21 has no user-facing
behavior — its acceptance test IS the automated invariant (55 tests OK; full
suite 1471 OK), so there are no manual UAT steps to run. The one residual human
read (refusal-citation *authenticity*, incl. the provisional `radar` row) is
already tracked under **HQ-27 Tier-3**, not duplicated here.

**To sign:** confirm the audit and write the approval line in `21-SECURITY.md`
(`Approval: verified <initials> <date>`, flip the `- [ ]` Approval box); an
interactive session then checks HQ-29 off here.

## Will be added by the loop when reached

- ~~S0-3: Phase 22 D-05 evidence pack~~ — FILED 2026-09-03 as HQ-27 (see Open).
- ~~Phase 21 security sign-off~~ — FILED 2026-09-02 as HQ-29 (see Open).
- Phase 21/22/23/24 end-of-phase security sign-off + UAT rounds (batched per
  phase; non-blocking until S5-2).
- D-06 numbering veto windows for any new codes Phase 22 mints (from a freshly
  re-measured live catalogue count; silence = accept).
- The Phase 23 license-audit confirmation (dsx-538/dsx-urban forked from
  permissively-licensed sources; dsx-econ/dsx-bbc reimplemented from published
  doctrine only, no GPL port, no unlicensed PDF embed).
- The S5-6 ship decisions: merge to `main` and the `v2.4.0` release tag.
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
and is silently dropped (found v2.3 S5-1). **At S5-1, never accept the CLI's
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
verified phase (found v2.3 close-out).** Same class of naming-convention blind
spot as the audit-uat issues, on a different code path. If it happens again,
read the actual verification file directly before treating it as a real gap.

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete conflicts on v2.0.0's 707-commit
branch and was abandoned mid-run. Ship by direct 3-way merge.

**Ship by EXPLICIT branch name — never the framework's auto-detect.** This repo
now carries five stale `gsd/*` branches from prior milestones; `/gsd-complete-
milestone`'s `handle_branches` picks the alphabetically-first `gsd/*` branch
(`gsd/v1.1.0-milestone`), which is always wrong here (found and bypassed at
v2.2 and v2.3 ship). `git merge --no-ff gsd/v2.4.0-visual-excellence` by name,
verified on a throwaway branch first.

**Release tags: never force-move a published one.** v2.0.0 shipped as tag
`v2.1.0` for this reason; v2.2 shipped as `v2.2.0`; v2.3 shipped as `v2.3.0`.
The next free tag for this milestone is `v2.4.0`.

**`/gsd-complete-milestone` output needs hand-verification — recurring at every
close so far.** At both v2.2's and v2.3's close, its generated accomplishment
bullets were truncated mid-sentence or captured YAML frontmatter instead of
prose, and the archived REQUIREMENTS.md carried all rows forward still
unchecked despite the passed audit — both needed hand-correction each time.
Budget for this as a standing cost, not a surprise. Also: it is NOT
headless-safe (interactive prompts + `git rm REQUIREMENTS.md`) — interactive
session only.

**Run the full suite from a clean tree — a stray root `DECISIONS.jsonl`
false-fails two `explain` tests.** `tests/test_dsx.py::test_explain_missing_spec_exits_zero_not_two`
and `tests/test_explain_self_reported.py::test_returns_zero_when_spec_cannot_be_loaded`
run from repo-root CWD without isolation; any repo-root `dsx gate`/`dsx explain`
leaves a gitignored ledger that breaks them. If exactly these two fail:
`rm -f DECISIONS.jsonl examples/DECISIONS.jsonl examples/known-bad/DECISIONS.jsonl templates/DECISIONS.jsonl`
and re-run before treating it as real.

**Usage-limit backoff is the wrapper's job — proven working in production.**
`scripts/run-ceremony-firing.ps1` detects limit hits, writes
`.planning/loop-logs/.backoff-until`, and re-probes every 30 minutes during a
hold with one trivial `claude -p` call to catch an early release rather than
blindly waiting the full window (fixed 2026-09-01 after a weekly-limit early
release was missed). Observed across v2.3's close: four separate 5-hour-window
hits each self-recovered in 2–7 minutes. Firings: log one line, stop, never
retry-loop, never touch the backoff/probe-marker files.

**A firing that finds uncommitted, ledger-inconsistent changes at start should
hold, not act.** Confirmed working at v2.3's close: a firing found an
interactive session's in-progress `/gsd-complete-milestone` work uncommitted in
the tree and correctly left it untouched (neither committed nor discarded),
logging the observation instead. This is the correct behavior, not a bug to fix.

## Answered

### HQ-27 — Phase 22 D-05 citation evidence pack (answered 2026-09-03)

**Operator verdict: ANSWERED with corrections.** Before the operator signed, an
interactive session ran an **independent primary-source verification pass** (5
parallel research agents, each instructed to actually fetch and read the sources
rather than re-confirm the loop's bibliographic record). **7 of 13 citations
required correction; 2 were load-bearing enough to change what Phase 22 builds.**

**Four binding decisions (D-1 … D-4), recorded in full in
`.planning/v2.4-D05-EVIDENCE-PACK.md`:**

- **D-1 — REQ-P22-05 tie-break: encode the REAL 6-rank order WITH ties.** The
  7-item strict ordering was never Cleveland & McGill's. Their p.536 list is 6
  ranks over 10 tasks; rank 3 is "Length, direction, angle" TOGETHER, and p.537
  states "there is not enough information to separate the ties." Heer & Bostock
  p.206 independently: "Theory also suggests that angle should perform worse than
  length, but the results do not support this." The `length > angle` link the test
  would have asserted has **no support in either cited paper**. Test must assert
  `rank(a) <= rank(b)`, never a strict total order. ("density" is also absent from
  the 1984 paper entirely; "curvature" and "shading" were silently dropped from
  their tied ranks.)
- **D-2 — REQ-P22-02 uncertainty family: adopt Wilke's actual 10 marks from
  §5.6.** Two of the four proposed names do not exist in the book: "fan chart"
  appears nowhere (verified against the full-text index, all 34 pages), and
  "gradient CI band" is not his term — he has two DISTINCT marks, "confidence
  strips" (continuous fade) and "graded confidence band" (nested levels).
  "half-eye" is real but lives in §5.6, not ch.16. Paradigm symmetry IS strongly
  confirmed.
- **D-3 — catalog spine: attribute the nine-category axis, write our own
  descriptions.** The "FT Visual Vocabulary is MIT-licensed" claim is wrong: the
  repo is MIT but the FT carves out its content in writing, twice — "does not
  cover any FT content … all rights reserved." Never vendor the PDF or copy its
  blurbs. Also drop any "exhaustive" claim resting on the FT: the poster
  disclaims exhaustiveness in its own words.
- **D-4 — `dual_axis_line`: cite "Muth 2018, as amended July 2026"** and scope the
  reason string to a **general audience**. Datawrapper publicly reversed its
  position ("we've changed our minds"), carving out expert users; they still hold
  general audiences misread these charts. The ban stands as a deliberate DSX
  position, not an appeal to a softened claim.

**Other corrections signed (no design change):** radar's PROVISIONAL placeholder
is **replaced** by a peer-reviewed source that supports both stated criticisms
nearly verbatim (Duan et al. 2023, J Clin Epidemiol 156:85-94, DOI
10.1016/j.jclinepi.2023.02.020) — and Few 2005 is explicitly NOT usable for those
grounds; the word-cloud citation mix-up is corrected to **Jacob Harris** (Nieman
Lab, 13 Oct 2011), not Robert L. Harris's *Information Graphics* (OUP 1999);
Few's gauge criticism is real but "arbitrary maximum" is **DSX's own reasoning,
not Few's**; Datawrapper's `>5` and `>7` thresholds are **confirmed verbatim** (no
demotion needed) but dated **2018**, not 2025; chart counts corrected (DVC = 60,
not ~77; FT = 74 entries / 66 distinct, not 72); Munzner ch.6's anti-3D doctrine
is **justification-gated**, not absolute, so the hard ban is DSX's application of
her presumption rather than her rule.

**Cross-cutting finding recorded:** the three "spine" sources are **not
independent** — Ribecca authored both the Graphic Continuum and the Data
Visualisation Catalogue, and the FT poster credits the Graphic Continuum as its
inspiration. One design lineage, not three corroborating authorities.

**Eight items remain explicitly unverified** and are listed as such in the pack
(Mackinlay 1986 primary text; the Harris 1999 index; Tufte's verbatim chartjunk
sentence; Few's 2013 edition; the Graphic Continuum's counts from the primary
artifact; FT's stance on axis reuse; Munzner "cardinality"; one Duan et al.
phrasing that would not reproduce on a second fetch and was deliberately dropped).

**Effect:** S2-1 (Phase 22 discuss) is **UNBLOCKED**, subject to D-1 … D-4.


(v2.0.0's items HQ-1…HQ-7, v2.2's items HQ-8…HQ-15, and v2.3's items
HQ-16…HQ-26 are archived at `.planning/milestones/v2.0.0-HUMAN-QUEUE*.md`,
`.planning/milestones/v2.2-HUMAN-QUEUE.md`, and
`.planning/milestones/v2.3-HUMAN-QUEUE.md`. Numbering continues from HQ-27.)
