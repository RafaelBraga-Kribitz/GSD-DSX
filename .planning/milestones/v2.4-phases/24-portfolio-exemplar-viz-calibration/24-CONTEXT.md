# Phase 24 — Portfolio exemplar and viz calibration — CONTEXT

**Milestone:** v2.4 Visual Excellence (terminal phase). **Requirements:** REQ-P24-01,
REQ-P24-02, REQ-P24-03. **Discuss unit:** S4-1 (ledger). Ran inline at opus/high
(brief §3; S1-1/S2-1/S3-1 precedent — single-writer artifact, no mid-unit
compaction, no subagent touches a tracking file). Persona round inline per brief §4
(Architect + Statistician + Auditor engaged; Advisor not engaged — no
external-tooling/licensing gray area this phase).

## 0. Ground truth (read live this firing, not assumed)

- **Live catalogue = 276 codes** (`references/finding-codes.md` "Total: 276 codes.";
  DSX-VIZ family present incl. `DSX-VIZ-071` — the **only** VIZ code minted this
  milestone — and pre-existing `DSX-VIZ-080`). Phase 24 is calibration + integration,
  **mints zero new codes** → set-identity 276→276 target at S4-4 (D-06 note below).
- **An end-to-end *good* exemplar already exists** but predates v2.4 and exercises
  **none** of its surfaces: `examples/good-ANALYSIS-SPEC.yaml` (causal / frequentist
  onboarding-activation, "passes every dsx gate at every severity threshold"),
  `examples/good-NARRATIVE.md` (Answer/Limits/Method — close to but not strict
  What/So What/Now What), `examples/good-FIGURE-MANIFEST.yaml` (2 figures, **NOT
  sealed** — no `svg_sha256`), `examples/figures/*.svg` (2), `examples/analysis/
  charts.py` (**uses no matplotlib / no `styles/*.mplstyle` / no `dsx_plotstyle.py`
  / no `save_deterministic`** — grep-confirmed empty).
- **`examples/known-bad/` holds only bad *statistical / test-choice* fixtures**
  (p-hacking, wrong test, agreement-estimand defects added at v2.3). **Zero
  bad-*chart*-choice fixtures exist** — Phase 24 introduces the first (REQ-P24-02).
  Convention there = `<name>-ANALYSIS-SPEC.yaml` + `<name>-POSTMORTEM.md`
  (+ `-NARRATIVE.md`/`-ATTRIBUTION.yaml` on some), run by `tests/test_known_bad_corpus.py`.
- **REPRO-REPORT infrastructure exists** (Phase 16): `templates/REPRO-REPORT.md`,
  `dsx/checks/repro.py`, `skills/dsx-reproduce`, `tests/test_reproduce_report.py`.
- **Both selection surfaces already carry a doc/code agreement test:**
  `tests/test_doc_code_agreement.py` cross-checks `references/test-selection.md`
  (v2.3); `tests/test_selection_heuristic_docs.py` verifies
  `references/chart-selection.md` (Phase 22). REQ-P24-03 is therefore largely
  **verify-not-build** (confirm both green + catalogue-current + snapshots-unmutated).
- **Style/seal/uncertainty surfaces to exercise (built this milestone):**
  `styles/{dsx-538,dsx-urban,dsx-econ,dsx-bbc}.mplstyle` + vendored OFL Lato;
  `templates/dsx_plotstyle.py` (`finalise_figure` [mandatory `source`],
  `direct_label`, `save_deterministic` — writes only, `dsx seal` is the single
  hasher, GA-2 Phase 23); the off-gate-path double-render determinism recipe (GA-3);
  the uncertainty family `DSX-VIZ-071` (Wilke §5.6, 10 marks) + `RELATIONSHIP_CHARTS
  ['uncertainty']` (Phase 22).

## 1. Gray areas settled (persona round — loud, not silent)

### GA-1 — The portfolio exemplar's analytical question (the main design choice)

**Decision: upgrade the existing `examples/good-*` onboarding-activation exemplar
*in place* into the full v2.4 capstone — do NOT author a net-new analytical
question.** The capstone gains: (i) its figures re-generated through the v2.4 style
layer (`dsx-urban` house style + `dsx_plotstyle.finalise_figure` with a real
`source` + `save_deterministic`); (ii) **one uncertainty-family figure** — the
activation uplift shown with its **real 95% CI (1.0–3.8pp)** as an error-bar / CI
mark, routed via `DSX-VIZ-071` / `RELATIONSHIP_CHARTS['uncertainty']` — so the
milestone's headline feature is exercised end-to-end on genuine uncertainty content;
(iii) a **sealed** FIGURE-MANIFEST (`svg_sha256` via `dsx seal`, the single hashing
authority); (iv) a strict **What / So What / Now What** NARRATIVE; (v) a
**REPRO-REPORT** proving deterministic re-render.

**Persona round.**
- **Architect (dsx-analysis-architect):** the capstone's job is *integration
  verification of both milestones*, not to invent a new question. The v2.4 delta is
  presentation + uncertainty, not identification. The existing spec already carries a
  95% CI on the uplift and a BH-corrected three-metric family, so an uncertainty-encoded
  uplift figure and a trend line fall out **naturally** from content already present —
  no new estimand. → **(a) upgrade in place.**
- **Statistician (dsx-statistician):** a net-new spec re-opens power, estimand, SRM,
  multiplicity — all already discharged in `good-ANALYSIS-SPEC.yaml`. Re-opening them on
  a terminal phase is gratuitous risk. The existing CI *is* the decision rule (lower
  bound > +1.0pp), so it is honest, load-bearing uncertainty to visualize. Reuse keeps
  the statistical claim **provable and unchanged**; the uncertainty figure must show the
  real CI, not a decorative band, and the narrative must not exceed the verified numbers.
  → **(a).**
- **Auditor (dsx-ml-integrity-auditor / gsd-security-auditor):** reuse = smaller diff,
  gate-passing already largely proven, lower regression risk. One integrity condition:
  the manifest must be **genuinely sealed** and the figures **deterministically
  re-renderable** (`save_deterministic` + REPRO-REPORT), or the capstone claims a
  reproducibility it does not have. → **(a) + mandatory seal/repro proof.**

**Tiebreak (rigour > reliability > flexibility):** unanimous **(a)**. This is the
smaller provable claim (brief §"prefer the smaller, provable claim every time"): reuse
proven-green statistics, upgrade only the v2.4 presentation surface, add exactly one
honest uncertainty figure.

**Rejected — (b) net-new exemplar:** re-opens the full statistical surface on a
terminal phase for no integration-coverage gain the upgrade doesn't already give.

### GA-2 — Known-bad chart-choice fixtures: which codes, and the fixture form

**Decision (direction; exact wiring is an S4-2 plan-research item):** author the first
bad-*chart*-choice fixtures, mirroring the existing known-bad corpus convention
(`-ANALYSIS-SPEC.yaml` + `-POSTMORTEM.md`), and extend `tests/test_known_bad_corpus.py`
+ re-baseline the stratified **catch-rate / false-positive-rate** across the now
chart-inclusive corpus (Phase-12/20 calibration discipline, scope §4).

**Which codes — minimal-honest set (REQ-P24-02 "per new code"):** the only NET-NEW
code this milestone is `DSX-VIZ-071` (uncertainty); Phase 22 also added `gauge` +
`word_cloud` as **new refusal rows** under the existing `DSX-VIZ-001`. So the honest
"per new code" set is: **one fixture that trips `DSX-VIZ-071`** (declares an
uncertainty question / interval-range signature but chooses a non-uncertainty mark, or
the inverse) and **one fixture that trips each new `DSX-VIZ-001` refusal row**
(`gauge`, `word_cloud`) — plus at least one pre-existing banned-type chart defect
(e.g. `radar` / `3d_pie` / `dual_axis_line`) so the corpus has a control-positive
chart defect. **The exact gate *surface* a chart defect is caught on** (a spec field,
a FIGURE-MANIFEST chart declaration, or a `recommend` call) is **NOT yet settled** —
S4-2 research must read `dsx/checks/viz.py`'s enforcement path and confirm which
declared artifact the corpus harness feeds, before the fixtures are authored. Flagged,
not guessed (brief: prefer the honest "unverified" to a claim that looks complete).

**Persona-lite (within discuss latitude, not an irreversible lock):** this settles the
*direction* (fixture form + which codes); the *catch-rate/FPR arithmetic* and the exact
fixture wiring are precedented (Phase 12/20) and self-gating (the re-baseline is
measured, not designed), so they belong in the plan, verified by the plan-checker.

### GA-3 — REQ-P24-03 audit prerequisites: verify-not-build where already covered

**Decision:** REQ-P24-03 ("catalogue current, snapshots unmutated, doc/code agreement
tests green for **both** selection surfaces") is **largely already satisfied** —
`test_doc_code_agreement.py` (test-selection.md) and `test_selection_heuristic_docs.py`
(chart-selection.md) both exist and were green at their phases' close. Phase 24's job is
to **verify** both are green on the final tree + `gen-finding-catalogue.py --check`
exit 0 @276 (catalogue current) + the snapshot/count-pin tests unmutated — **not** to
rebuild them. **If** S4-2 research finds a genuine gap (e.g. one surface's test does not
actually assert doc↔code equality both directions), Phase 24 closes exactly that gap and
no more. No new selection-surface test is authored speculatively.

## 2. D-06 numbering note (loud, veto window — NOT escalated per brief §4)

Phase 24 **mints zero new finding codes.** Calibration fixtures, the exemplar, and the
audit-prerequisite verifications all route to **existing** codes; the catch-rate/FPR
re-baseline and doc/code agreement are off-gate-path repo-integrity tests. Target at
S4-4: **set-identity 276→276, added={} removed={}**, `gen-finding-catalogue.py --check`
exit 0. Re-measure the live count at plan time (do not assume 276 has held) before
asserting zero-mint. Recorded loudly with the standard silence=accept veto window
(HQ-35); **not** escalated (D-06 numeric assignments are persona-round decisions).

## 3. Standing inputs carried in (not re-litigated)

- **Pre-agreed 23→24-split contingency is MOOT:** the v2.4 D-05 queue did **not**
  outrun cadence (Phase 23 shipped; HQ-33/HQ-34 non-blocking until S5-2). Phase 24
  proceeds **inside v2.4** as planned — the plan must not re-open the v2.5 split.
- **Faceting is a declaration, not a chart type** (`facet_by`, Phase 22) — if the
  exemplar facets, it declares, it does not add a mark.
- **`dsx seal` is the single hashing authority** (GA-2 Phase 23): the manifest is
  sealed by `dsx seal`, never by the plot helper; the REPRO-REPORT proves re-render
  equality against the sealed hash.
- **Perceptual tie-break ordering is asserted, never computed** (Cleveland–McGill
  six-rank-with-ties, D-1); the exemplar's uncertainty figure choice cites the
  structural criterion, it does not run a perceptual computation.

## 4. Pre-staged for S4-2 (plan-checker-verifiable)

| REQ | Deliverable | Reuse anchor | Open plan-research question |
|---|---|---|---|
| P24-01 | Upgrade `examples/good-*` → sealed, styled, uncertainty-figured, What/So What/Now What + REPRO-REPORT | `good-ANALYSIS-SPEC.yaml` (green), `dsx_plotstyle.py`, `dsx-urban`, `dsx seal`, `templates/REPRO-REPORT.md` | Does the existing spec need a `visuals:`/manifest field to declare the uncertainty figure so `DSX-VIZ-071` sees it? |
| P24-02 | First bad-chart fixtures (`DSX-VIZ-071`; `gauge`+`word_cloud` under `DSX-VIZ-001`; ≥1 banned control) + `test_known_bad_corpus.py` extension + catch-rate/FPR re-baseline | `examples/known-bad/*` convention, `tests/test_known_bad_corpus.py` | **Which surface does `viz.py` enforce a chart defect on**, and what artifact does the corpus harness feed it? (read `dsx/checks/viz.py`) |
| P24-03 | Verify both doc/code agreement tests green + catalogue current + snapshots unmutated | `test_doc_code_agreement.py`, `test_selection_heuristic_docs.py`, `gen-finding-catalogue.py --check` | Does either test actually assert doc↔code equality *both directions*, or only doc⊆code? |

**Next = S4-2 (Phase 24 plan; plan-checker must pass; opus/high per brief §3).**
