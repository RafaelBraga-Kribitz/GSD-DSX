---
phase: 20-calibration-and-reporting-close
plan: B
type: execute
wave: 2
depends_on: [20-C, 20-D]
files_modified:
  - examples/good-ANALYSIS-SPEC.yaml
  - references/finding-codes.md
  - tests/test_phase20_zero_mint_close.py
autonomous: true
requirements: [REQ-P20-02]
tags: [zero-mint, catalogue-close, d05-allowlist, good-fixture-silence, frozen-snapshot, reporting-close, extend-not-replace]

must_haves:
  truths:
    - "the canonical good fixture examples/good-ANALYSIS-SPEC.yaml is EXTENDED (not replaced) with silent, in-vocabulary, NON-triggering new-family declarations (a satisfying analysis.sphericity_correction and analysis.power_reporting_type — values the Wave-2 gates never fire on) and STAYS SILENT at every threshold: it fires NONE of the fifteen new codes and its CRITICAL/HIGH ship finding set is UNCHANGED from its measured baseline {DSX-CLM-031, DSX-DQ-001, DSX-FIG-001, DSX-NAR-010} (D-08 corpus discipline: extend, never replace; stay silent)"
    - "the catalogue regen is ADDITIVE with frozen snapshots UNMUTATED: python scripts/gen-finding-catalogue.py --check exits 0 at Total 275, references/finding-codes.md is regenerated (a no-op diff — this phase adds zero report.add sites) in the same close, and the frozen Phase-12 snapshot tests/fixtures/finding-codes-phase12.md stays byte-unchanged at 256"
    - "all fifteen milestone codes are already named by EXACT string in scripts/gen-finding-catalogue.py::_D05_ALLOWLIST_CODES (verified: the Phase-18 five 050/051/060/061/062 and the Phase-19 ten 070/080/081/090/100/110/111/120/121/122 were added by exact code during 18-19; DSX-STA- is NOT an allowlisted prefix) — REQ-P20-02's allowlist clause is a VERIFY, satisfied, no edit to scripts/gen-finding-catalogue.py"
    - "the zero-mint TELL holds: Phase 20 adds NO report.add call site, the pre-allocated DSX-STA range stops at 122 with the 123-129 band UNUSED and the 130s reserve UNTOUCHED (no code in that band appears in the catalogue), and the declared total stays exactly 275 (D-01)"
    - "a new tests/test_phase20_zero_mint_close.py CRLF-safely proves all of the above: catalogue total 275, phase12 snapshot 256, the fifteen codes allowlisted by exact string, the 123-onward reserve absent from the catalogue, and the good fixture silent on the fifteen — a runnable oracle, not a claim"
  artifacts:
    - examples/good-ANALYSIS-SPEC.yaml
    - references/finding-codes.md
    - tests/test_phase20_zero_mint_close.py
  key_links:
    - "the good fixture's silent new-family declarations <-> the Wave-2 gate triggers they deliberately avoid (sphericity_correction: unconditional_gg is not mauchly_conditional so DSX-STA-070 stays silent; power_reporting_type: a_priori is not observed/post_hoc so DSX-STA-111 stays silent; both are in-vocab so DSX-STA-040 stays silent) <-> the preserved four-code golden baseline that tests/test_causal_verb_golden.py (owned by 20-A) pins — the extension is provably finding-set-preserving"
    - "zero report.add sites this phase <-> gen-finding-catalogue.py --check green at 275 <-> the regenerated references/finding-codes.md no-op diff <-> the byte-frozen Phase-12 snapshot at 256 — the additive-regen / unmutated-snapshot lockstep (D-01)"
    - "the fifteen codes <-> _D05_ALLOWLIST_CODES by exact string (already satisfied 18-19) <-> the --check citation enforcement — REQ-P20-02's allowlist clause is a standing invariant this plan asserts, not a change it makes"
    - "the unused 123-129 band + untouched 130s reserve <-> the deliberate zero-mint tell (mirroring REQ-P19-03's absent 06x decade) <-> the catalogue staying 275 — the machine-checkable form of 'Phase 20 mints zero codes'"
---

<objective>
Deliver REQ-P20-02: the good fixture is extended (not replaced) and stays silent at every threshold (D-08); the catalogue regen is additive with frozen snapshots unmutated; and the fifteen new codes are in the D-05 allowlist as exact strings. This is the reporting-close half of the terminal phase — the zero-mint proof (D-01): Phase 20 adds no report.add site, so the catalogue stays exactly 275 and the pre-allocated DSX-STA range stops at 122 with the 123-129 band unused and the 130s reserve untouched.

Purpose: Wave 2 (D-07), the catalogue close measured against the settled post-C/post-D state. Two of the three REQ-P20-02 clauses are standing invariants already satisfied during 18-19 (all fifteen codes are allowlisted by exact string; the catalogue is 275) — this plan turns them into a runnable oracle rather than an unverified claim. The one substantive authoring act is extending the canonical good fixture with silent, in-vocabulary new-family declarations that exercise the new families' happy path and provably stay silent (extend, never replace — the D-08 corpus discipline), keeping its finding set identical to the four-code baseline that 20-A's golden test pins.

Output: examples/good-ANALYSIS-SPEC.yaml extended with silent non-triggering new-family declarations; references/finding-codes.md regenerated (no-op at 275, proving lockstep); and a new tests/test_phase20_zero_mint_close.py asserting catalogue 275, phase12 snapshot 256, the fifteen codes allowlisted by exact string, the reserve band absent from the catalogue, and the good fixture silent on the fifteen. scripts/gen-finding-catalogue.py is verified untouched (allowlist already satisfied). Zero codes minted.
</objective>

<execution_context>
@$HOME/.claude/gsd-core/workflows/execute-plan.md
@$HOME/.claude/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/20-calibration-and-reporting-close/20-CONTEXT.md
@examples/good-ANALYSIS-SPEC.yaml
@references/finding-codes.md
@scripts/gen-finding-catalogue.py
@tests/test_causal_verb_golden.py
</context>

<extension_bindings>
The good fixture's analysis block (examples/good-ANALYSIS-SPEC.yaml:154-163) currently declares outcome_type: proportion, estimand_kind: linear_association, n_groups: 2, paired: false, test: two_proportion_z (measured ship set {DSX-CLM-031, DSX-DQ-001, DSX-FIG-001, DSX-NAR-010}, all four tempdir-artifact noise). The SILENT extension adds only these NON-triggering, in-vocabulary scalar new-family fields to that block (each verified against dsx/checks/stats.py Wave-2 predicates and dsx/spec.py vocabularies):

- analysis.sphericity_correction: unconditional_gg — DSX-STA-070 fires ONLY on mauchly_conditional, so unconditional_gg is silent; unconditional_gg is a member of SPHERICITY_CORRECTIONS, so DSX-STA-040 is silent.
- analysis.power_reporting_type: a_priori — DSX-STA-111 fires ONLY on observed / post_hoc, so a_priori is silent; a_priori is a member of POWER_REPORTING_TYPES, so DSX-STA-040 is silent.

Both are independent declared scalar fields the gates read for their TRIGGER value only; neither interacts with outcome_type / test / estimand_kind, so the existing four-code finding set is preserved exactly. The executor MAY add further non-triggering in-vocab new-family fields (e.g. proportion_ci_method: wilson, a complete resampling {method, seed, B, unit} quadruple, variance_test with variance_test_role: scale_estimand) IF and only if the gate re-measure confirms the ship set is unchanged; the two scalar fields above are the mandatory, lowest-risk minimum. Do NOT declare any TRIGGER value (never mauchly_conditional / observed / post_hoc / wald / an incomplete resampling quadruple), and do NOT remove or replace any existing field (extend-not-replace, D-08).
</extension_bindings>

<tasks>

<task type="auto">
  <name>Task 1: Extend the good fixture with silent, non-triggering new-family declarations that preserve its finding set</name>
  <read_first>
    - examples/good-ANALYSIS-SPEC.yaml lines 154-163 (the analysis block to EXTEND — keep every existing field; append the non-triggering scalar fields per <extension_bindings>)
    - dsx/checks/stats.py the Wave-2 gate predicates for DSX-STA-070 (fires on mauchly_conditional only), DSX-STA-111 (fires on observed/post_hoc only), and DSX-STA-040 (membership over _MEMBERSHIP_FIELDS) — confirm unconditional_gg / a_priori are silent AND in-vocab
    - dsx/spec.py SPHERICITY_CORRECTIONS and POWER_REPORTING_TYPES (confirm unconditional_gg and a_priori are members, so DSX-STA-040 stays silent)
    - tests/test_causal_verb_golden.py lines 105-107 (the good fixture's pinned golden ship set {DSX-CLM-031, DSX-DQ-001, DSX-FIG-001, DSX-NAR-010} — owned by 20-A; this extension MUST preserve it exactly, the cross-plan read-only invariant) and lines 306-318 (test_good_fixture_fires_no_causal_verb_finding — must stay green)
    - 20-CONTEXT.md D-08 (both canonical fixtures extended not replaced; the good fixture stays silent; frozen snapshots byte-frozen) and D-01 (zero mint)
  </read_first>
  <files>examples/good-ANALYSIS-SPEC.yaml</files>
  <action>Extend the analysis block of examples/good-ANALYSIS-SPEC.yaml (do NOT replace the file; keep every existing field byte-for-byte) by appending the two mandatory non-triggering, in-vocabulary new-family scalar declarations from <extension_bindings> — analysis.sphericity_correction: unconditional_gg and analysis.power_reporting_type: a_priori — so the canonical good fixture now declares the new families' HAPPY path and provably stays silent. The executor may append further non-triggering in-vocab new-family fields only if the gate re-measure confirms the ship set is unchanged. Then PROVE the extension is finding-set-preserving: re-measure the good fixture and assert it fires NONE of the fifteen new codes and its CRITICAL/HIGH ship set still equals {DSX-CLM-031, DSX-DQ-001, DSX-FIG-001, DSX-NAR-010} — the four-code baseline 20-A's tests/test_causal_verb_golden.py pins (this plan does NOT edit that golden test; it reads it and preserves its entry, the documented cross-plan invariant). Do NOT declare any trigger value; do NOT remove or replace any field; do NOT add a report.add site; do NOT edit dsx/, scripts/, references/, tests/, examples/known-bad/, examples/good-corpus/, or any tracking file in this task.</action>
  <verify>
    <automated>python3 -m unittest tests.test_causal_verb_golden -v && python3 -c "from dsx.loader import load; from dsx.checks import stats; F={'DSX-STA-050','DSX-STA-051','DSX-STA-060','DSX-STA-061','DSX-STA-062','DSX-STA-070','DSX-STA-080','DSX-STA-081','DSX-STA-090','DSX-STA-100','DSX-STA-110','DSX-STA-111','DSX-STA-120','DSX-STA-121','DSX-STA-122'}; a=load('examples/good-ANALYSIS-SPEC.yaml')['analysis']; assert a.get('sphericity_correction')=='unconditional_gg' and a.get('power_reporting_type')=='a_priori', ('non-triggering new-family fields not appended: '+str({k:a.get(k) for k in ('sphericity_correction','power_reporting_type')})); codes={f.code for f in stats.check(load('examples/good-ANALYSIS-SPEC.yaml')).findings}; leaked=F & codes; assert not leaked, ('good fixture leaked a new code: '+str(sorted(leaked))); print('good fixture extended with silent new-family declarations; fires none of the fifteen; golden baseline preserved')"</automated>
  </verify>
  <acceptance_criteria>
    - tests.test_causal_verb_golden is green (test_golden_keys_match_the_examples_tree_on_disk, test_every_fixture_ship_finding_set_equals_its_golden_baseline for the good fixture, and test_good_fixture_fires_no_causal_verb_finding all pass), proving the extension preserved the four-code baseline.
    - The inline check prints "good fixture extended with silent new-family declarations; fires none of the fifteen; golden baseline preserved": the two mandatory non-triggering fields are present and the good fixture fires none of the fifteen new codes.
    - No existing field was removed or replaced (extend-not-replace, D-08); no trigger value was declared; no report.add site was added.
    - No edit to dsx/, scripts/, references/, tests/, examples/known-bad/, examples/good-corpus/, or any tracking file.
  </acceptance_criteria>
  <done>examples/good-ANALYSIS-SPEC.yaml is extended (not replaced) with silent, in-vocabulary new-family declarations, exercises the new families' happy path, fires none of the fifteen, and preserves its four-code golden baseline; zero codes minted.</done>
</task>

<task type="auto">
  <name>Task 2: The zero-mint / catalogue-close proof — catalogue 275, snapshot 256, fifteen allowlisted, reserve unused, additive regen</name>
  <read_first>
    - references/finding-codes.md line 16 (**Total: 275 codes.** — must stay 275 after the no-op regen; the file is generated, never hand-edited) and its DSX-STA table rows (the code family whose 123-onward band must be absent)
    - tests/fixtures/finding-codes-phase12.md line 16 (**Total: 256 codes.** — the frozen Phase-12 snapshot that must stay byte-unchanged at 256)
    - scripts/gen-finding-catalogue.py lines 87-99 (_D05_ALLOWLIST_PREFIXES — confirm DSX-STA- is NOT present) and lines 157-194 (the Phase-18 and Phase-19 dated comment blocks and the _D05_ALLOWLIST_CODES frozenset already carrying all fifteen 050..122 by exact code) and the --check / --write entry points and the if-__name__-guard (so the proof module can import the constant without running main)
    - 20-CONTEXT.md D-01 (zero mint; catalogue stays 275; ranges 123-129 unused and the 130s reserve untouched; a runtime doc/code-divergence code is explicitly NOT wanted) and the "Phase Boundary" note (new codes were added to the D-05 allowlist by exact name during 18-19)
  </read_first>
  <files>references/finding-codes.md, tests/test_phase20_zero_mint_close.py</files>
  <action>Create tests/test_phase20_zero_mint_close.py (stdlib-only: unittest, re, pathlib, importlib.util; CRLF-safe, encoding="utf-8"). Assert the zero-mint / catalogue-close invariants as a runnable oracle: (1) references/finding-codes.md declares a total of 275; (2) tests/fixtures/finding-codes-phase12.md declares a total of 256 (the frozen snapshot, byte-unchanged — assert its declared total and that its parsed code-set is a subset of the current catalogue); (3) load scripts/gen-finding-catalogue.py via importlib.util (so its __main__ guard does not run) and assert the fifteen milestone codes (the Phase-18 050/051/060/061/062 and the Phase-19 070/080/081/090/100/110/111/120/121/122) are ALL members of _D05_ALLOWLIST_CODES by exact string, and that "DSX-STA-" is NOT in _D05_ALLOWLIST_PREFIXES; (4) parse the DSX-STA codes out of references/finding-codes.md and assert the reserve band from 123 upward (construct the code strings programmatically from a numeric range, do not hard-code them) is ABSENT from the catalogue — the deliberate zero-mint tell; (5) assert the good fixture examples/good-ANALYSIS-SPEC.yaml fires NONE of the fifteen at ship (read-only silence proof over the canonical good fixture). Then regenerate references/finding-codes.md by running python3 scripts/gen-finding-catalogue.py --write (a NO-OP diff because this phase added zero report.add sites — the total stays 275) and stage the regenerated file so the doc/code/catalogue lockstep is explicit. Do NOT edit scripts/gen-finding-catalogue.py (the allowlist already carries all fifteen by exact string — this is a VERIFY, not a change); do NOT hand-edit references/finding-codes.md (only the generator writes it); do NOT edit tests/fixtures/finding-codes-phase12.md (byte-frozen); do NOT add any report.add site; do NOT edit dsx/, examples/, or any tracking file.</action>
  <verify>
    <automated>python3 scripts/gen-finding-catalogue.py --check && python3 -m unittest tests.test_phase20_zero_mint_close -v && python3 -c "import re,pathlib,importlib.util; c=pathlib.Path('references/finding-codes.md').read_text(encoding='utf-8'); assert '275 codes' in ' '.join(c.split()), 'catalogue is not 275'; snap=pathlib.Path('tests/fixtures/finding-codes-phase12.md').read_text(encoding='utf-8'); assert '256 codes' in ' '.join(snap.split()), 'phase12 snapshot is not 256'; spec=importlib.util.spec_from_file_location('gfc','scripts/gen-finding-catalogue.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); fifteen={'DSX-STA-050','DSX-STA-051','DSX-STA-060','DSX-STA-061','DSX-STA-062','DSX-STA-070','DSX-STA-080','DSX-STA-081','DSX-STA-090','DSX-STA-100','DSX-STA-110','DSX-STA-111','DSX-STA-120','DSX-STA-121','DSX-STA-122'}; assert fifteen <= set(m._D05_ALLOWLIST_CODES), ('missing from allowlist: '+str(sorted(fifteen-set(m._D05_ALLOWLIST_CODES)))); assert 'DSX-STA-' not in m._D05_ALLOWLIST_PREFIXES; codes=set(re.findall(r'DSX-STA-\d+',c)); reserve={('DSX-STA-%d'%n) for n in range(123,140)}; assert not (reserve & codes), ('reserve band leaked into catalogue: '+str(sorted(reserve & codes))); from dsx.loader import load; from dsx.checks import stats; assert not (fifteen & {f.code for f in stats.check(load('examples/good-ANALYSIS-SPEC.yaml')).findings}), 'good fixture fired a new code'; print('275; snapshot 256; fifteen allowlisted by exact string; 123-onward reserve unused; good silent')"</automated>
  </verify>
  <acceptance_criteria>
    - python3 scripts/gen-finding-catalogue.py --check exits 0 at Total 275; tests.test_phase20_zero_mint_close is green; the inline check prints "275; snapshot 256; fifteen allowlisted by exact string; 123-onward reserve unused; good silent".
    - references/finding-codes.md was regenerated (not hand-edited) and still declares 275; tests/fixtures/finding-codes-phase12.md is byte-unchanged at 256.
    - All fifteen codes are in _D05_ALLOWLIST_CODES by exact string and DSX-STA- is not an allowlisted prefix; the reserve band from 123 upward is absent from the catalogue (the zero-mint tell).
    - The good fixture fires none of the fifteen at ship; no report.add site was added; scripts/gen-finding-catalogue.py is unchanged.
    - No edit to dsx/, examples/, tests/fixtures/finding-codes-phase12.md, or any tracking file.
  </acceptance_criteria>
  <done>A runnable zero-mint oracle proves the catalogue stays 275, the Phase-12 snapshot stays 256, the fifteen codes are allowlisted by exact string, the 123-onward reserve is unused, and the good fixture is silent; references/finding-codes.md is regenerated as a no-op; zero codes minted.</done>
</task>

</tasks>

<single_writer_proof>
Phase 20 is a two-wave, file-disjoint, single-writer split (D-07). This is a Wave-2 catalogue-close plan (depends_on 20-C, 20-D). Every file this plan writes is owned by exactly one plan; the Wave-2 partition with 20-A is disjoint:

| File | Wave-2 writer | 20-A (Wave 2) writes? | Concurrent write? |
|------|---------------|-----------------------|-------------------|
| examples/good-ANALYSIS-SPEC.yaml | 20-B | No | No |
| references/finding-codes.md | 20-B (no-op regen) | No | No |
| tests/test_phase20_zero_mint_close.py | 20-B (new file) | No | No |
| scripts/gen-finding-catalogue.py | 20-B owns; UNCHANGED (allowlist already satisfied) | No | No |
| tests/test_causal_verb_golden.py | — | 20-A | No — 20-B only READS it |

Cross-plan read-only invariant (documented, not a write conflict): 20-B extends examples/good-ANALYSIS-SPEC.yaml with silent, non-triggering, in-vocabulary declarations and its own Task-1 gate PRESERVES the four-code finding set that 20-A's tests/test_causal_verb_golden.py pins; 20-A does not change that good-fixture golden entry (it only adds entries for its own new fixtures). So at merge, 20-A's unchanged golden entry still matches 20-B's extended fixture. File writes are disjoint (20-B writes the fixture; 20-A writes the golden test); the preservation invariant is enforced by 20-B's own gate. Wave-1 files (references/test-selection.md, dsx/checks/stats.py, the guard test modules) are untouched by 20-B. Tracking files stay orchestrator-serial.
</single_writer_proof>

<threat_model>
**register_authored_at_plan_time: true** — authored at planning time (S4-2). /gsd-secure-phase 20 reads this flag. ASVS L1, block_on: high. This plan adds a fixture extension and a read-only catalogue-close proof; no data path, no new I/O surface, no new dependency, no report.add site; there is no high-severity open threat.

## Trust Boundaries

| Boundary | Description |
|----------|-------------|
| the good fixture extension <-> the Wave-2 gate triggers | The extension must declare only non-triggering, in-vocabulary values; the gate re-measure + golden-baseline equality is the boundary control (silent, set-preserving). |
| report.add call sites -> gen-finding-catalogue.py -> references/finding-codes.md | Zero new report.add sites this phase; the --check + no-op regen + byte-frozen Phase-12 snapshot is the boundary control (the D-01 zero-mint invariant). |
| the fifteen codes -> _D05_ALLOWLIST_CODES | A code is citation-enforced only if named by exact string (DSX-STA- is not an allowlisted prefix); the proof asserts all fifteen are present. |

## STRIDE Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation Plan |
|-----------|----------|-----------|----------|-------------|-----------------|
| T-20-B-01 | Tampering (silent mint) | a report.add site or catalogue drift slipping into the terminal phase, moving the total off 275 | high | mitigate | gen-finding-catalogue.py --check green at 275; the proof asserts 275, the byte-frozen 256 snapshot, and the absent 123-onward reserve band — a mint would fail all three. |
| T-20-B-02 | Tampering (good fixture no longer silent) | the extension firing a new code or changing the finding set, breaking the negative-control guarantee | medium | mitigate | The Task-1 gate re-measures the good fixture, asserts none of the fifteen fire, and asserts the four-code golden baseline is preserved (extend-not-replace, D-08). |
| T-20-B-03 | Tampering (snapshot mutation) | the frozen Phase-12 snapshot being edited to absorb a change | medium | mitigate | The proof asserts tests/fixtures/finding-codes-phase12.md declares 256 and its code-set is a subset of the catalogue; the plan never edits it. |
| T-20-B-04 | Tampering (uncited code laundered) | a milestone code missing from _D05_ALLOWLIST_CODES, shipping uncited under the non-allowlisted DSX-STA- prefix | low | mitigate | The proof asserts all fifteen are in _D05_ALLOWLIST_CODES by exact string and DSX-STA- is not an allowlisted prefix. |
| T-20-B-SC | Tampering | npm/pip/cargo installs (supply chain) | low | accept | Zero packages installed; Python stdlib only (unittest, re, pathlib, importlib). No Package Legitimacy Audit owed (vacuously satisfied). |
</threat_model>

<verification>
- After Task 1 commit: `python3 -m unittest tests.test_causal_verb_golden -v` green; the good fixture is extended with silent new-family declarations, fires none of the fifteen, and preserves its four-code golden baseline.
- After Task 2 commit: `python3 scripts/gen-finding-catalogue.py --check` exits 0 at 275; `python3 -m unittest tests.test_phase20_zero_mint_close -v` green; the catalogue is 275, the Phase-12 snapshot is 256, the fifteen codes are allowlisted by exact string, the 123-onward reserve is absent, and the good fixture is silent.
- REQ-P20-02 completeness: the good fixture is extended (not replaced) and stays silent at every threshold; the catalogue regen is additive with frozen snapshots unmutated; the new codes are in the D-05 allowlist as exact strings; catalogue stays 275; zero codes minted.
</verification>

<success_criteria>
- The canonical good fixture is extended (not replaced) with silent, in-vocabulary new-family declarations and stays silent at every threshold, its finding set preserved at the four-code baseline (D-08).
- The catalogue regen is additive with frozen snapshots unmutated: --check green at 275, references/finding-codes.md regenerated as a no-op, the Phase-12 snapshot byte-frozen at 256 (D-01).
- All fifteen new codes are in _D05_ALLOWLIST_CODES by exact string (verified, already satisfied 18-19); DSX-STA- is not an allowlisted prefix.
- The zero-mint tell holds: no report.add site added, the 123-129 band unused and the 130s reserve untouched, the total exactly 275; a runnable oracle (tests/test_phase20_zero_mint_close.py) proves it.
</success_criteria>

<output>
Create `.planning/phases/20-calibration-and-reporting-close/20-B-SUMMARY.md` when done.
</output>
