---
phase: 18-correlation-association-and-agreement
plan: B
type: tdd
wave: 1
depends_on: []
files_modified:
  - dsx/mathx.py
  - templates/APA-TABLE-research.md
  - tests/test_effect_size_kind.py
autonomous: true
requirements: [REQ-P18-05]
tags: [statistics, effect-size, conventions, report-only, mathx, firewall]

must_haves:
  truths:
    - "mathx.EFFECT_SIZE_KINDS stays exactly frozenset({d, h, r}) and interpret_effect is unchanged — the blocking magnitude-band domain never widens (D-06 firewall; kappa/ICC/Kendall's W/phi/Cramer's V/tau_b/rho are NEVER added to it)"
    - "a separate report-only registry REPORT_ONLY_EFFECT_KINDS exists in mathx.py containing at least kappa, icc, kendalls_w, phi, cramers_v, tau_b, rho; it is the set the DSX-STA-012 branch (owned by Plan 18-A's stats.py) consults so a report-only kind is recognised but never banded by a blocking code"
    - "the Krippendorff reference value 0.7598 is pinned AT level=ordinal and always carries its level; the same data pinned at nominal/interval/ratio yields 0.4765/0.7574/0.6621 (D-07 — a level-free pin is wrong because the value is level-dependent)"
    - "the Landis-Koch kappa band boundaries are pinned as a labeled convention (the 1977 published thresholds), with edge-tie handling explicitly labeled a convention choice, not claimed as the paper's exact wording"
    - "ICC (Koo-Li) bands, Kendall's W bands, distance correlation, partial correlation, and Cronbach->McDonald omega are present as NAMED catalog-only entries with NO numeric boundary asserted; Kendall's W carries an explicit 'no band citation exists' note (D-07); no fabricated locator, no invented boundary value"
    - "the convention bands are wired ONLY into the ungated templates/APA-TABLE-research.md, which mints no finding code — so REQ-P18-05's 'conventions never block' is structural, not by discipline"
    - "effect_size_kind: kappa (any report-only kind) on a significant result fires neither DSX-STA-011 nor DSX-STA-012 and yields a report.ok naming the convention — this behaviour is a cross-plan seam with Plan 18-A's stats.py, validated at the Wave-1 merge"
  artifacts:
    - dsx/mathx.py
    - templates/APA-TABLE-research.md
    - tests/test_effect_size_kind.py
  key_links:
    - "REPORT_ONLY_EFFECT_KINDS (mathx.py) <-> the DSX-STA-012 branch in dsx/checks/stats.py (Plan 18-A) — the report-only recognition seam; this plan owns the registry and the test, 18-A owns the consuming branch"
    - "KRIPPENDORFF_REFERENCE ordinal value 0.7598 <-> the pinned numeric assertion carrying level=ordinal; the nominal/interval/ratio values guard against a level-free pin"
    - "EFFECT_SIZE_KINDS frozenset <-> the firewall test asserting it stays exactly {d, h, r} — a future contributor adding a convention kind to it turns the firewall red"
    - "report-only band tables (mathx.py) <-> templates/APA-TABLE-research.md — the ONE wiring point, which mints no finding code (structural enforcement of 'conventions never block')"
---

<objective>
Grow the effect-size vocabulary with the correlation/agreement convention bands (kappa, ICC, Kendall's W, Krippendorff) as REPORT-ONLY conventions that are recognised but never used as blocking thresholds. This plan adds a separate report-only registry and convention-band tables to dsx/mathx.py, wires the bands into the ungated APA template, and extends the effect-size tests — while keeping the blocking band domain (EFFECT_SIZE_KINDS) frozen at {d, h, r}.

Purpose: REQ-P18-05 requires the new agreement/correlation magnitude bands to ship as labeled conventions, never as gated thresholds. D-06 makes this structural: interpret_effect uses a flat abs(value) band that is statistically wrong for these kinds (Cramer's V thresholds are df-dependent; phi and Kendall's W are unsigned with a different null), so widening EFFECT_SIZE_KINDS would be wrong on two counts — it would let DSX-STA-011 adjudicate a convention AND apply a wrong flat band. The bands therefore live in a separate report-only surface consulted only by the DSX-STA-012 recognition branch and the ungated template.

Output: REPORT_ONLY_EFFECT_KINDS + the convention-band tables (Landis-Koch kappa bands pinned; Krippendorff reference value pinned at level=ordinal; ICC/Koo-Li and Kendall's W as named catalog-only entries with no numeric boundary) + a label_convention_band function in dsx/mathx.py; a convention-band note in templates/APA-TABLE-research.md; extensions to tests/test_effect_size_kind.py.

Cross-plan coupling (the ONE semantic seam, per 18-CONTEXT.md D-08): the report-only recognition behaviour (effect_size_kind: kappa fires neither DSX-STA-011 nor DSX-STA-012, yielding a report.ok) is produced by Plan 18-A's DSX-STA-012 branch in dsx/checks/stats.py consulting this plan's REPORT_ONLY_EFFECT_KINDS. This plan owns the registry (the mathx side) and the test that pins the behaviour; Plan 18-A owns the consuming stats.py branch. This plan's files are disjoint from 18-A's (it never writes dsx/checks/stats.py, dsx/spec.py, or references/*). This plan's own registry/band/firewall tests are green in isolation; the cross-plan report-only-firing assertion is guarded so it skips when 18-A's seam is absent and enforces after the Wave-1 merge. This plan mints NO finding code, so it never touches references/finding-codes.md and has no catalogue-regen contention with 18-A.
</objective>

<execution_context>
@$HOME/.claude/gsd-core/workflows/execute-plan.md
@$HOME/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/18-correlation-association-and-agreement/18-CONTEXT.md
@.planning/phases/18-correlation-association-and-agreement/18-RESEARCH.md
@.planning/phases/18-correlation-association-and-agreement/18-VALIDATION.md
@dsx/mathx.py
@templates/APA-TABLE-research.md
@tests/test_effect_size_kind.py
</context>

<artifacts_produced>
Symbols and files this plan creates or extends (NO finding code is minted — bands are conventions; EFFECT_SIZE_KINDS is deliberately NOT widened):

- `REPORT_ONLY_EFFECT_KINDS` — NEW frozenset in `dsx/mathx.py` containing at least kappa, icc, kendalls_w, phi, cramers_v, tau_b, rho; the set the DSX-STA-012 branch (Plan 18-A) consults.
- `KAPPA_BANDS` — NEW report-only band table in `dsx/mathx.py` pinned to the Landis and Koch 1977 published boundaries (labeled convention; edge-tie handling labeled a convention choice).
- `KRIPPENDORFF_REFERENCE` — NEW report-only reference-value table in `dsx/mathx.py` pinning 0.7598 at level=ordinal (and 0.4765/0.7574/0.6621 at nominal/interval/ratio) — the value ALWAYS carries its level.
- Named catalog-only entries (no numeric boundary) in `dsx/mathx.py` for ICC/Koo-Li bands, Kendall's W bands (with an explicit "no band citation exists" note), distance correlation, partial correlation, and Cronbach -> McDonald omega.
- `label_convention_band(kind, value)` — NEW report-only labeling function in `dsx/mathx.py`, distinct from `interpret_effect`, never fed into DSX-STA-011.
- A convention-band note in `templates/APA-TABLE-research.md` (the ungated wiring point; mints no finding code).
- Extensions to `tests/test_effect_size_kind.py`: the EFFECT_SIZE_KINDS firewall assertion, the pinned 0.7598@ordinal + Landis-Koch band assertions, the catalog-only presence assertions (substring only, never numeric equality), and the report-only-firing seam oracle (guarded for isolation).

`dsx/mathx.py`'s existing `EFFECT_SIZE_KINDS` and `interpret_effect` are UNCHANGED. Residual assumption recorded (no silent drop): the report-only-firing behaviour depends on Plan 18-A's stats.py branch and is validated at the Wave-1 merge, not in this plan's isolated run.
</artifacts_produced>

<tasks>

<task type="tdd" tdd="true">
  <name>Task 1 (RED then GREEN then REFACTOR): report-only effect-size registry and convention-band tables in mathx.py</name>
  <read_first>
    - dsx/mathx.py lines 292-319 (EFFECT_SIZE_KINDS = frozenset({"d","h","r"}) and interpret_effect's flat abs(value) band table — the domain this plan must NOT widen and the reason a flat band is wrong for df-dependent/unsigned convention kinds)
    - tests/test_effect_size_kind.py (full file — the existing DSX-STA-011/012 test shapes and the interpret_effect ValueError test; this plan extends, does not rewrite, these)
    - 18-CONTEXT.md D-06 (report-only registry; EFFECT_SIZE_KINDS stays {d,h,r}; the two reasons widening is wrong) and D-07 (the pin-vs-catalog-only disposition table: Krippendorff 0.7598@ordinal PIN with level; Landis-Koch PIN values label convention; ICC/Koo-Li and Kendall's W CATALOG-ONLY no boundaries; dCor/partial/Cronbach->omega pointer only)
    - 18-RESEARCH.md § "The exact EFFECT_SIZE_KINDS/interpret_effect state Plan 18-B must not widen" (the recommended REPORT_ONLY_EFFECT_KINDS + label_convention_band shape) and Anti-Patterns (never widen EFFECT_SIZE_KINDS; never invent a Koo-Li/Kendall's-W boundary) and Assumptions Log A4
    - 18-VALIDATION.md Per-Task Verification Map rows REQ-P18-05 (pinned), REQ-P18-05 (catalog-only), REQ-P18-05 (report-only kind)
  </read_first>
  <files>dsx/mathx.py, tests/test_effect_size_kind.py</files>
  <behavior>
    RED first — author these assertions in tests/test_effect_size_kind.py so they fail against the current tree, then implement to GREEN:
    - Firewall: mathx.EFFECT_SIZE_KINDS equals exactly frozenset({"d","h","r"}) (an equality assertion, not a subset — a future add turns it red); interpret_effect still raises ValueError when given a report-only kind such as "kappa" (its domain is unchanged).
    - Registry: mathx.REPORT_ONLY_EFFECT_KINDS is a frozenset and {"kappa","icc","kendalls_w","phi","cramers_v","tau_b","rho"} is a subset of it; the two sets are disjoint from EFFECT_SIZE_KINDS.
    - Pinned Krippendorff: the report-only reference table gives 0.7598 at level=ordinal (numeric equality allowed here — this value is confirmed at source, HQ-16 B4); it also carries 0.4765/0.7574/0.6621 at nominal/interval/ratio; a lookup with no level (or a level-free pin) is not accepted as the ordinal value.
    - Pinned Landis-Koch: label_convention_band("kappa", value) returns the Landis-Koch band label for representative points across the published boundaries (labeled convention); edge-tie handling is asserted only as a labeled convention, not as the paper's exact wording.
    - Catalog-only: ICC/Koo-Li bands, Kendall's W bands, distance correlation, partial correlation, Cronbach->McDonald omega are each present as a NAMED entry with NO numeric boundary — substring/presence assertions only, never a numeric equality assertion; Kendall's W entry contains the explicit "no band citation exists" note.
  </behavior>
  <action>Implement in dsx/mathx.py exactly per 18-RESEARCH.md's recommended shape, leaving EFFECT_SIZE_KINDS and interpret_effect byte-unchanged. Add REPORT_ONLY_EFFECT_KINDS = frozenset({"kappa","icc","kendalls_w","phi","cramers_v","tau_b","rho"}) with a comment stating it is the recognition set consulted by the DSX-STA-012 branch and is deliberately separate from the blocking EFFECT_SIZE_KINDS. Add KAPPA_BANDS as a report-only table pinned to the Landis and Koch 1977 published boundaries (name the citation; label edge-tie handling a convention). Add KRIPPENDORFF_REFERENCE as a level-keyed table pinning ordinal->0.7598, nominal->0.4765, interval->0.7574, ratio->0.6621, with a comment that the value is level-dependent and MUST carry its level (D-07). Add named catalog-only entries for ICC/Koo-Li bands, Kendall's W bands (with an explicit note that no band citation exists and a D-05 read is owed), distance correlation, partial correlation, and Cronbach->McDonald omega — each named, each with NO numeric boundary and NO fabricated locator. Add label_convention_band(kind, value) -> str as a report-only labeling function distinct from interpret_effect, which for a pinned-band kind (kappa) returns the Landis-Koch label and for a catalog-only kind returns a "convention, no gated boundary" style label; it must NEVER be called by DSX-STA-011 and must never raise as if it were a blocking guard. Run the RED assertions first (they fail against the current tree), implement to GREEN, then REFACTOR only if the tables share extractable lookup logic. Do NOT widen EFFECT_SIZE_KINDS, do NOT branch inside interpret_effect, do NOT edit dsx/checks/stats.py or references/* (Plan 18-A owns those), do NOT mint any finding code, do NOT edit REQUIREMENTS.md/STATE.md/ROADMAP.md.</action>
  <verify>
    <automated>python3 -m unittest tests.test_effect_size_kind -v && python3 -c "from dsx import mathx; assert mathx.EFFECT_SIZE_KINDS==frozenset({'d','h','r'}), mathx.EFFECT_SIZE_KINDS; assert {'kappa','icc','kendalls_w','phi','cramers_v','tau_b','rho'}<=set(mathx.REPORT_ONLY_EFFECT_KINDS); assert set(mathx.EFFECT_SIZE_KINDS).isdisjoint(mathx.REPORT_ONLY_EFFECT_KINDS); assert mathx.KRIPPENDORFF_REFERENCE['ordinal']==0.7598; print('firewall+registry+pin OK')"</automated>
  </verify>
  <acceptance_criteria>
    - tests/test_effect_size_kind.py is GREEN, including the firewall assertion (EFFECT_SIZE_KINDS equals exactly {d,h,r}), the registry subset+disjointness assertion, the pinned 0.7598@ordinal (with the nominal/interval/ratio companions), the Landis-Koch band labels, and the catalog-only presence assertions.
    - interpret_effect still raises ValueError for a report-only kind (its domain is unchanged); EFFECT_SIZE_KINDS is byte-unchanged.
    - No numeric boundary is asserted anywhere for ICC/Koo-Li, Kendall's W, dCor, partial correlation, or Cronbach->omega (presence-only); the Kendall's W entry carries the "no band citation exists" note.
    - dsx/mathx.py mints no finding code and does not import from dsx/checks/stats.py.
  </acceptance_criteria>
  <done>REPORT_ONLY_EFFECT_KINDS and the convention-band tables exist in mathx.py with 0.7598@ordinal and the Landis-Koch bands pinned and the catalog-only items present as named boundary-free entries; EFFECT_SIZE_KINDS stays exactly {d,h,r}; interpret_effect is unchanged; all effect-size tests pass in isolation.</done>
</task>

<task type="auto">
  <name>Task 2: Wire the convention bands into the ungated APA template and add the report-only-firing seam oracle</name>
  <read_first>
    - templates/APA-TABLE-research.md (full file — 18-RESEARCH.md confirms it is genuinely ungated, "mints no finding code", and is the correct D-06 wiring point; this is the ONE place the bands are wired)
    - dsx/mathx.py the Task-1 KAPPA_BANDS / KRIPPENDORFF_REFERENCE / catalog-only entries (the source the template note mirrors)
    - 18-CONTEXT.md D-06 (bands wired only into the ungated template; conventions never block) and 18-RESEARCH.md Pitfall 6 (the report-only control-flow the seam oracle asserts: effect_size_kind kappa -> neither DSX-STA-011 nor DSX-STA-012 -> a report.ok naming the convention) and § "The exact DSX-STA-011/012 site" (the stats.py branch Plan 18-A modifies)
    - 18-VALIDATION.md row REQ-P18-05 (report-only kind) — the seam behaviour and its stdlib-unittest command
  </read_first>
  <files>templates/APA-TABLE-research.md, tests/test_effect_size_kind.py</files>
  <action>In templates/APA-TABLE-research.md add a convention-band note that presents the report-only bands from mathx.py — the Landis-Koch kappa bands (labeled convention), the Krippendorff reference value carrying its level (0.7598 @ ordinal), and the named catalog-only pointers for ICC/Koo-Li and Kendall's W — each framed explicitly as a labeled convention, not a gated threshold, with the "conventions never block" statement in prose. Keep the catalog-only items boundary-free (no numeric band, no fabricated locator). Do not add any finding-code reference to this template (it stays ungated). Then extend tests/test_effect_size_kind.py with the report-only-firing seam oracle: build a spec whose analysis/results declare a significant result with effect_size_kind == kappa, run it through dsx.checks.stats.check, and assert that neither DSX-STA-011 nor DSX-STA-012 fires and that a report.ok entry naming the convention is present. Because this behaviour requires Plan 18-A's stats.py DSX-STA-012 branch to be present, GUARD this single assertion so it is skipped when the seam is absent (detect via whether stats.check produces the report.ok/no-012 result for a kappa kind, e.g. a unittest.skipUnless on a small helper that checks the seam is live) — so this plan is green in isolation (assertion skipped) and the Wave-1 merge enforces it (assertion runs and passes). Also add a template-presence assertion (the convention note names kappa/Landis-Koch and the level-carrying Krippendorff value; substring only). Do NOT edit dsx/checks/stats.py or dsx/mathx.py in this task, do NOT mint a finding code, do NOT edit any tracking file.</action>
  <verify>
    <automated>python3 -m unittest tests.test_effect_size_kind -v && python3 -c "import pathlib,re; t=pathlib.Path('templates/APA-TABLE-research.md').read_text(encoding='utf-8'); assert 'convention' in t.lower() and re.search(r'Landis',t) and '0.7598' in t and re.search(r'ordinal',t,re.I), 'template convention note incomplete'; print('template wiring OK')"</automated>
  </verify>
  <acceptance_criteria>
    - templates/APA-TABLE-research.md carries the convention-band note naming the Landis-Koch kappa bands and the level-carrying Krippendorff value (0.7598 @ ordinal), framed as labeled conventions that never block; the catalog-only items stay boundary-free; the template mints no finding code.
    - tests/test_effect_size_kind.py is green in isolation: the seam oracle for effect_size_kind kappa is SKIPPED when Plan 18-A's stats.py branch is not present, and (post-merge) enforces that kappa fires neither DSX-STA-011 nor DSX-STA-012 and yields a report.ok naming the convention.
    - The SUMMARY records the report-only-firing behaviour as the cross-plan seam validated at the Wave-1 merge with Plan 18-A.
  </acceptance_criteria>
  <done>The ungated APA template presents the convention bands as never-blocking labeled conventions; the report-only-firing seam oracle is in place (skipped in isolation, enforced post-merge); no finding code is minted and no gate path is touched.</done>
</task>

</tasks>

<threat_model>
**register_authored_at_plan_time: true** — this STRIDE register was authored at planning time (S2-2) per the security_contribution contract; /gsd-secure-phase 18 reads this flag. ASVS L1, block_on: high. This plan adds only report-only convention data plus one ungated template note; it has no data path, no gate path, no new I/O surface, and no new dependency. There is no high-severity open threat.

## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| mathx report-only band tables -> DSX-STA-012 recognition branch (Plan 18-A) | The registry is consulted for RECOGNITION only; it must never be routed into the blocking DSX-STA-011 band path. |
| mathx report-only band tables -> templates/APA-TABLE-research.md | The one wiring point; it is ungated and mints no finding code, so a convention can never become a blocking threshold through it. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-18-B-01 | Tampering (of the validation contract) | a convention band mistakenly made blocking by widening EFFECT_SIZE_KINDS or by feeding label_convention_band into DSX-STA-011 | low | mitigate | EFFECT_SIZE_KINDS stays exactly {d,h,r} (firewall test asserts equality); bands live in a separate report-only surface and label_convention_band is never called by the blocking guard; bands wired only into the ungated template. |
| T-18-B-02 | Tampering (false authority) | pinning an unconfirmed boundary (ICC/Koo-Li, Kendall's W) as if cited, or a level-free Krippendorff pin | low | mitigate | Only 0.7598@ordinal (with its level) and the Landis-Koch bands are pinned; ICC/Koo-Li and Kendall's W ship as named catalog-only entries with no numeric boundary and Kendall's W carries a "no band citation exists" note; tests assert presence only, never numeric equality, for catalog-only items. |
| T-18-B-03 | Tampering | the report-only recognition set drifting from the DSX-STA-012 branch that consults it | low | mitigate | The seam oracle (guarded, enforced at the Wave-1 merge) asserts effect_size_kind kappa fires neither 011 nor 012 and yields a report.ok — drift between the registry and the consuming branch turns it red post-merge. |
| T-18-B-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only. No Package Legitimacy Audit owed. |
</threat_model>

<verification>
- After Task 1 commit: `python3 -m unittest tests.test_effect_size_kind -v` green; the inline firewall+registry+pin check exits 0 (EFFECT_SIZE_KINDS exactly {d,h,r}; registry subset+disjoint; 0.7598@ordinal).
- After Task 2 commit: the template convention note is present (Landis-Koch, 0.7598, ordinal); tests green in isolation with the seam oracle skipped.
- Wave-1 merge gate (orchestrator, after 18-A and 18-B merge): `python3 -m unittest discover -s tests -q` fully green — the seam oracle now runs and enforces the report-only-firing behaviour against Plan 18-A's DSX-STA-012 branch.
- This plan's files_modified (dsx/mathx.py, templates/APA-TABLE-research.md, tests/test_effect_size_kind.py) are disjoint from Plan 18-A's, so the two run concurrently in Wave 1.
</verification>

<success_criteria>
- EFFECT_SIZE_KINDS stays exactly {d,h,r} and interpret_effect is unchanged (the D-06 firewall holds).
- REPORT_ONLY_EFFECT_KINDS exists and is the recognition set the DSX-STA-012 branch consults (REQ-P18-05).
- Krippendorff 0.7598 is pinned at level=ordinal (carrying its level); the Landis-Koch kappa bands are pinned as a labeled convention; ICC/Koo-Li, Kendall's W, dCor, partial correlation, and Cronbach->omega are named catalog-only entries with no numeric boundary.
- The bands are wired only into the ungated templates/APA-TABLE-research.md; no finding code is minted.
- The report-only-firing seam oracle is in place (green in isolation via skip, enforced at the Wave-1 merge).
</success_criteria>

<output>
Create `.planning/phases/18-correlation-association-and-agreement/18-B-SUMMARY.md` when done.
</output>
