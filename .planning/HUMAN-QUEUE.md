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

### HQ-33 — Phase 23 license-audit at-locator confirmation (NON-BLOCKING until S5-2)

Filed at S3-3 Wave 1 (2026-09-03) with the concrete evidence gathered while vendoring the
assets — mirrors the security sign-offs (HQ-29/HQ-31): non-blocking, the loop keeps working;
only S5-2 waits on it. REQ-P23-01's explicit plan-review item. Full six-point checklist +
checksums in `.planning/phases/23-style-snippet-layer/23-01-SUMMARY.md`.

**Three vendored (load-bearing) assets to confirm at their locators:**

1. **matplotlib `fivethirtyeight` fork** — VERIFIED by the loop: the installed matplotlib
   3.11.1 LICENSE §2/§3 permit verbatim vendoring of a bundled style sheet, conditioned on
   retaining the MDT copyright + a brief change summary (both in the dsx-538 header). Please
   confirm you accept this reading.
2. **Urban Institute palette (Apache-2.0)** — ASSUMED (carried from Scope §3.3, 2026-08-29,
   not re-fetched this firing). Only palette hexes + rcParams are vendored, no guide prose.
   **This is the one item still needing an at-locator human read** — the house-default style
   rests on it.
3. **Lato `.ttf` (SIL OFL 1.1)** — VERIFIED at-locator by the loop: fetched from the pinned
   canonical Google Fonts OFL source; `OFL.txt` carries the SIL OFL 1.1 text and the Lato
   copyright/reserved-name line; checksums recorded (Regular
   `d636e468…5b251`, Bold `8a0aace7…d16be1`). Please confirm the checksums are acceptable.

The two cite-only styles (dsx-econ, dsx-bbc) vendor nothing and cannot contaminate
(reimplemented-from-doctrine posture; CONTEXT GA-1 Auditor robustness note) — no license
read is owed for them; their `Source:` URLs are public-doctrine provenance only.

## Will be added by the loop when reached

- ~~S0-3: Phase 22 D-05 evidence pack~~ — FILED 2026-09-03 as HQ-27 (see Open).
- ~~Phase 21 security sign-off~~ — FILED 2026-09-02 as HQ-29 (see Open).
- Phase 21/22/23/24 end-of-phase security sign-off + UAT rounds (batched per
  phase; non-blocking until S5-2).
- D-06 numbering veto windows for any new codes Phase 22 mints (from a freshly
  re-measured live catalogue count; silence = accept).
- ~~The Phase 23 license-audit confirmation~~ — FILED 2026-09-03 as HQ-33 (see Open),
  non-blocking until S5-2.
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

**`gsd-tools query commit` (used by GSD planner/researcher/executor subagents)
auto-creates the wrong branch mid-run — recurring, budget for it.** Confirmed
**3×** (S2-2 once; S3-2 twice, one per subagent): when a `gsd-*` subagent commits
via `gsd-tools query commit`, it can create + switch to a stray
`gsd/v2.4-visual-excellence` (**no `.0`**) and land the commit there instead of the
canonical `gsd/v2.4.0-visual-excellence`; the subagent's own return then confidently
**misreports** the branch/push state. **After ANY subagent that may commit, the
orchestrator must reconcile against the repo, not the report:** `git rev-parse
--abbrev-ref HEAD` + `git branch -vv`; if a stray no-`.0` branch holds the work, it is
a linear descendant of canonical → `git checkout` canonical → `git merge --ff-only
<stray>` (no commit lost) → `git branch -d`/`-D` the stray → push; verify tree-hash
identity / `git merge-base --is-ancestor` before deleting. This is exactly why the
loop uses plain `git commit` for orchestrator-authored files, and why the `gsd/*`
count must be re-asserted (5 stale + 1 active) every planning firing.

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

### HQ-28 — Phase 21 discuss persona decisions (answered 2026-09-03 — accepted, no veto)

**Operator verdict:** Accepted both. D-01 (every-mark-has-a-home as an off-gate-path
repo-integrity test, capability home defined gate-faithfully as `CHART_CAPABILITIES ∪
EXTRA_MARKS`, ~14 capability-only marks documented-exempt with promotion deferred to
Phase 22) and D-02 (`BANNED_TYPES` enriched in place to `{reason, code, citation}`
rather than a parallel sub-map — single registry, no drift surface). No veto.

### HQ-29 — Phase 21 end-of-phase security sign-off (answered 2026-09-03)

**Operator verdict:** Approved — signed in `21-SECURITY.md`'s Approval line.

Basis, **independently re-verified in this session rather than trusted from the
report**: `threats_open: 0`, 3/3 threats CLOSED; the mitigation modules behind
T-21-01/02/03 (`test_viz_vocabulary_invariant`, `test_finding_catalogue_invariant`,
`test_gen_finding_catalogue`) re-run green as part of a 79-test run, and
`gen-finding-catalogue.py --check` exit 0. The register's audit row reads 3 threats /
3 closed / 0 open, and a scan for open threat rows found none (every "open" occurrence
in the file is legend or audit-header boilerplate). UAT confirmed: no user-facing
runtime behavior, `nyquist_compliant: true`, 3/3 requirements COVERED. The residual
refusal-citation authenticity read — including the then-provisional `radar` row — was
discharged separately under HQ-27.

### HQ-30 — Phase 22 discuss persona decisions + D-06 numbering (answered 2026-09-03 — accepted, no veto)

**Operator verdict:** Accepted all three. GA-1 (catalog entry-set: 50 admissible
marks + 10 Wilke §5.6 uncertainty marks + 7 refusal rows + ~15 reference-only rows,
landing at 81 — inside REQ-P22-01's 75–90 band; `gauge` and `word_cloud` added to
`BANNED_TYPES` under the existing DSX-VIZ-001 so every catalog refusal row is backed
by a live ban, zero new code). GA-2 (an 11th `RELATIONSHIP_CHARTS` key
`"uncertainty"` carrying Wilke's 10 marks, rather than new input-type ids — the
paradigm-faithful modeling, with `DSX-VIZ-070` retained as a complementary surface).
GA-3 (D-06 numbering `DSX-VIZ-071` from the next-free 07x band, verified against a
re-measured live baseline; `DSX-VIZ-072` contingent and correctly **not** minted —
final diff 275→276, additive-only). No veto.

**Verified at sign-off:** all four HQ-27 decisions were applied to the shipped tree —
D-1 ranks encoded with ties and the tie-break test asserting `<=` never `<`, with
`density` asserted absent; D-2 all 10 Wilke marks present and `fan_chart` /
`gradient_ci_band` correctly absent; D-3 the FT axis attributed with DSX's own
descriptions. **D-4 was found NOT applied** and was corrected in this session (see
HQ-31 note).

### HQ-31 — Phase 22 end-of-phase security sign-off (answered 2026-09-03)

**Operator verdict:** Approved — signed in `22-SECURITY.md`'s Approval line.

Basis, **independently re-verified in this session**: `threats_open: 0`, 12/12 threats
T-22-01…T-22-12 CLOSED; the six mitigation modules re-run **79/79 green**, and
`gen-finding-catalogue.py --check` exit 0 at catalogue **276** — matching the
register's claims exactly. UAT confirmed: no user-facing runtime behavior,
`nyquist_compliant: true`, 5/5 requirements COVERED.

**One gap found and fixed at sign-off (not a threat — a citation-integrity defect):**
operator decision **D-4** from HQ-27 had not been applied. `dual_axis_line` still cited
"Muth 2018 (Datawrapper)" with no record that Datawrapper **publicly reversed that
position in July 2026** ("we've changed our minds"), and no general-audience scoping.
Left as-was, the project would have shipped a hard ban citing a source that had
softened the very claim it rested on. Corrected in all three sites —
`dsx/checks/viz.py` and both the markdown table and JSON payload of
`references/chart-catalog.md` — to cite "Muth 2018, as amended July 2026", record
Datawrapper's expert-audience carve-out, and state plainly that the unconditional ban
is **DSX's own general-audience position**, not an appeal to the amended claim. The
same commit also records that Munzner's anti-3D doctrine is **justification-gated**
(she permits 3D for true 3D spatial data), so ch.6 supplies the presumption and the
hard ban is DSX's application of it. `test_chart_catalog_invariant` +
`test_viz_vocabulary_invariant` re-run green (24 OK) after the edit; JSON payload
re-parsed clean at 81 rows.

### HQ-32 — Phase 23 discuss persona decisions + style/determinism design (answered 2026-09-03 — accepted, no veto)

**Operator verdict:** Accepted all five. GA-1 (four `styles/*.mplstyle`: `dsx-538`
forked under the Matplotlib License, `dsx-urban` as house default on the Apache-2.0
palette with vendored OFL Lato, `dsx-econ`/`dsx-bbc` reimplemented from published
doctrine only — no Economist-PDF embed, no `bbplot` GPL port, no proprietary font;
per-file license headers). GA-2 (`finalise_figure` with a **mandatory** `source`
parameter and no default, `direct_label`, `save_deterministic` — which writes but
deliberately does **not** hash, keeping `dsx seal` the single hashing authority).
GA-3 (the determinism recipe: `svg.fonttype: path`, fixed `svg.hashsalt`,
`metadata={'Date': None}`, vendored font via `font_manager.addfont`, pinned matplotlib
recorded in `FIGURE-MANIFEST.yaml`, proven by an off-gate-path double-render
hash-equality test). D-P23-03 (add `matplotlib` to `test_gate_path_hermetic.FORBIDDEN`
as a structural guard against a future render-on-the-gate-path regression).
D-P23-04 (zero new codes; set-identity 276→276 at S3-4). No veto.

The license-audit confirmation correctly remains a **plan-review item at S3-2**
(REQ-P23-01's own explicit requirement), not folded into this veto window — and the
v2.4 scope's license findings are applied as binding inputs rather than re-opened.


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
