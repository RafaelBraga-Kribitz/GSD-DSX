---
phase: 06-contract-extension-decision-record-paradigm-manifest
plan: 08
subsystem: fixtures
tags: [known-bad-corpus, interference, peeking-policy, bayesian, frequentist, d-06, req-p6-13]

# Dependency graph
requires:
  - phase: 06-01
    provides: "PEEKING_POLICIES.uncontrolled_continuous member and the ten closed vocabularies (INTERFERENCE_RISKS, INTERFERENCE_MITIGATIONS, PARADIGMS, etc.) this corpus's fixtures declare legal values against"
  - phase: 06-05
    provides: "the validity_frame/inference shape both fixtures model — ten sub-blocks, six inference fields, the none-as-string round-trip pattern"
  - phase: 06-06
    provides: "_validate_validity_frame_shape / _validate_inference_shape — the CRITICAL-level structural checks these fixtures must (and do) pass cleanly today"
provides:
  - "examples/known-bad/ with three real-failure spec+post-mortem pairs: interference-shared-budget, frequentist-uncontrolled-continuous, bayesian-continuous-monitoring"
  - "Both halves of Phase 9's atomic DSX-PAR-010/DSX-PAR-011 pair have a committed target (D-06)"
  - "tests/test_known_bad_corpus.py — glob-discovered pairing, composition, structural-validity and catch-attribution invariants over the corpus directory, extensible by Phase 12 without editing this module"
affects: [08, 09, 12]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Known-bad fixtures are structurally complete clones of the good-fixture shape (all validity_frame sub-blocks, full inference block) with exactly one semantic defect isolated to the field(s) the defect concerns — every other field stays a legal, unremarkable value, so a future diff against the fixture points straight at the encoded failure"
    - "Corpus test discovers fixtures by directory glob and slug-set symmetric-difference, never a hardcoded filename list — the same pattern test_frame_boundary.py and test_gen_finding_catalogue.py use for other self-extending invariants this phase introduced"

key-files:
  created:
    - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
    - examples/known-bad/interference-shared-budget-POSTMORTEM.md
    - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
    - examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md
    - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
    - examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md
    - tests/test_known_bad_corpus.py
  modified: []

key-decisions:
  - "Every known-bad fixture is a full-shape clone of examples/good-ANALYSIS-SPEC.yaml's structure (all ten validity_frame sub-blocks, all six inference fields, decision/metrics/data/design/claims sections) rather than a minimal spec — this guarantees zero CRITICAL findings from any other _validate_* branch in dsx/spec.py (metrics, decision, data, claims) without having to audit each one field-by-field per fixture, and keeps every fixture realistic enough that its post-mortem reads like an actual incident, not a synthetic edge case"
  - "dsx validate (block-on CRITICAL) is the acceptance bar for these fixtures, not dsx gate ship (block-on HIGH) — confirmed from dsx/cli.py's add_common(p_validate, 'CRITICAL') default and the plan's own acceptance criteria/Task 3 action text (cli.main(['validate', ...])), so no fixture needed a fully populated visuals/reproducibility/narrative section the way the canonical good/bad fixtures do"
  - "Kohavi, Tang & Xu (2020)'s exact chapter for the shared-budget interference pattern is flagged unverified rather than invented, per the plan's explicit escalation instruction and the T-6-16 threat mitigation — author/title/venue/year match brief.md section 7's anchored list with high confidence; Imbens & Rubin (2015) Ch.1 Sec.1.6 is cited with full confidence because dsx/spec.py's own _validate_validity_frame_shape docstring already anchors that exact locator (06-06 precedent)"
  - "Task 3 (tdd='true') landed as a single test(06-08) commit rather than a RED/GREEN pair — see Deviations below"

patterns-established: []

requirements-completed: [REQ-P6-13]

coverage:
  - id: D1
    description: "examples/known-bad/interference-shared-budget-{ANALYSIS-SPEC.yaml,POSTMORTEM.md}: a structurally valid causal-experiment spec declaring interference.risk: shared_budget with mitigation: none and an empty residual_note, paired with a post-mortem sourced to Kohavi/Tang/Xu (2020) and Imbens & Rubin (2015) Ch.1 Sec.1.6, naming DSX-INT-010 (Phase 8) as the absent catching code"
    requirement: "REQ-P6-13"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus (test_every_spec_loads_without_raising, test_every_spec_passes_dsx_validate, test_every_postmortem_names_a_catch_attribution_finding_code)"
        status: pass
      - kind: other
        ref: "python3 -m dsx validate --spec examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml"
        status: pass
    human_judgment: true
    rationale: "Whether the post-mortem names a real documented failure pattern sourced to a verifiable primary work (not a synthetic narrative written to fit the fixture) is a provenance judgment call, exactly as the plan's own <human-check> for Task 1 specifies; the Kohavi chapter locator is additionally flagged unverified above and needs human confirmation."
  - id: D2
    description: "examples/known-bad/frequentist-uncontrolled-continuous-{ANALYSIS-SPEC.yaml,POSTMORTEM.md}: uncontrolled_continuous peeking policy under inference.paradigm: frequentist, five interim looks, reference Type-I inflation 0.142 matching dsx.mathx.inflation_from_peeking(5) exactly, post-mortem naming DSX-PAR-010 (Phase 9) and confirming DSX-EXP-060 does not double-fire"
    requirement: "REQ-P6-13"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus (test_every_spec_passes_dsx_validate, test_every_postmortem_names_a_catch_attribution_finding_code)"
        status: pass
      - kind: other
        ref: "python3 -c \"from dsx.loader import load; from dsx.mathx import inflation_from_peeking as inf; f=load('examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml'); assert abs(inf(f['results']['interim_looks']) - 0.142) < 1e-9\""
        status: pass
    human_judgment: false
  - id: D3
    description: "examples/known-bad/bayesian-continuous-monitoring-{ANALYSIS-SPEC.yaml,POSTMORTEM.md}: same peeking policy under inference.paradigm: bayesian, a claim/limitation asserting a weakly informative prior alone controls the false-positive rate under continuous peeking (the defect), post-mortem stating the prior-averaged Ville bound (K=19, ~0.05) explicitly against the point-null formulation it is not, naming DSX-PAR-011 (Phase 9)"
    requirement: "REQ-P6-13"
    verification:
      - kind: unit
        ref: "tests/test_known_bad_corpus.py::TestKnownBadCorpus (test_every_spec_passes_dsx_validate, test_every_postmortem_names_a_catch_attribution_finding_code)"
        status: pass
      - kind: other
        ref: "python3 -c \"import pathlib; t=pathlib.Path('examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md').read_text(encoding='utf-8'); need=['DSX-PAR-011','Deng','2016','Theorem 1','prior-averaged','Ville','19','0.05']; assert all(n in t for n in need)\""
        status: pass
    human_judgment: true
    rationale: "Confirming the Bayesian post-mortem states the prior-averaged formulation unambiguously without conflating it with the point-null result is a domain-correctness judgment call, exactly as the plan's own <human-check> for Task 2 specifies."
  - id: D4
    description: "tests/test_known_bad_corpus.py discovers the corpus by glob, enforces two-directional spec/post-mortem pairing, a minimum of three pairs including interference and Bayesian-continuous slugs, structural validity of every spec, and a catch-attribution finding code in every post-mortem — no hardcoded filename list"
    requirement: "REQ-P6-13"
    verification:
      - kind: unit
        ref: "python3 -m unittest tests.test_known_bad_corpus -v (6 tests, all pass)"
        status: pass
      - kind: other
        ref: "python3 scripts/gen-finding-catalogue.py --check"
        status: pass
    human_judgment: false

duration: 30min
completed: 2026-08-08
status: complete
---

# Phase 6 Plan 08: Known-bad seed corpus Summary

**`examples/known-bad/` ships three real-failure spec+post-mortem pairs — shared-budget interference, uncontrolled-continuous-monitoring frequentist, and the same under Bayesian paradigm — plus `tests/test_known_bad_corpus.py`, giving Phase 8 and both halves of Phase 9's atomic pair a committed target before either phase is written.**

## Performance

- **Duration:** ~30 min
- **Completed:** 2026-08-08
- **Tasks:** 3
- **Files modified:** 7 (3 spec/post-mortem pairs, 1 test module)

## Accomplishments

- `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` — a structurally complete causal-experiment spec (all ten `validity_frame` sub-blocks, full `inference` block) declaring `interference.risk: shared_budget` with `mitigation: none` and an empty `residual_note`: a declared, unaddressed interference risk. Paired post-mortem sources the mechanism to Kohavi, Tang & Xu (2020) and the formal SUTVA statement it violates to Imbens & Rubin (2015) Ch.1 Sec.1.6, and names `DSX-INT-010` (Phase 8, which already names this exact filename in ROADMAP Success Criterion 1) as the currently-absent catching code.
- `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` — `design.peeking_policy: uncontrolled_continuous`, five interim looks, `inference.paradigm: frequentist`, no sequential method named in `primary_procedure`. The post-mortem's reference value (Type-I error ≈ 0.142 at 5 looks under a nominal alpha of 0.05) is grounded in `dsx.mathx.inflation_from_peeking(5)`, which already returns exactly `0.142`, sourced to Armitage, McPherson & Rowe (1969). The post-mortem explicitly confirms `DSX-EXP-060` does not (and should not) fire on this spec, by construction (M-01).
- `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` — the same `uncontrolled_continuous` peeking policy under `inference.paradigm: bayesian`, with a claim and a limitation asserting a weakly informative prior alone controls the false-positive rate while peeking, and no threshold calibration declared. The post-mortem's dedicated "Which formulation this fixture encodes" section states the **prior-averaged** Ville-bound formulation explicitly (`K=19`, bound ≈ `0.05`) against the point-null / law-of-iterated-logarithm formulation it deliberately is not, sourced to Deng, Lu & Chen (2016) Theorem 1. The same formulation note is commented directly in the spec file itself (T-6-17 mitigation).
- Both halves of Phase 9's atomic `DSX-PAR-010`/`DSX-PAR-011` pair (D-06) now have a committed, structurally valid target, sharing the same peeking-policy value so a future symmetry check between them has something to compare.
- `tests/test_known_bad_corpus.py` — 6 tests in `TestKnownBadCorpus`, all discovering the corpus by `Path.glob()` against `examples/known-bad/`, never a hardcoded filename list: two-directional pairing via slug-set symmetric difference, a minimum-of-three-pairs count, interference/Bayesian-continuous composition checks by slug substring, every spec loading without raising, every spec passing `dsx validate` (invoked in-process via `cli.main(["validate", "--spec", ...])`, matching `TestCLI._run`'s idiom in spirit), and every post-mortem naming at least one `DSX-<LETTERS>-<digits>` finding code.
- All three fixtures pass `dsx validate --spec ...` with **zero findings at any severity** (not just below the CRITICAL block threshold) — confirmed directly against each fixture, not just inferred from exit code.
- `git diff --stat dsx/ scripts/ examples/good-ANALYSIS-SPEC.yaml examples/bad-ANALYSIS-SPEC.yaml` is empty — no source, script or canonical-fixture change, exactly as scoped. `python3 -m dsx gate {plan,execute,verify,ship} --spec examples/good-ANALYSIS-SPEC.yaml` all still exit 0. `python3 scripts/gen-finding-catalogue.py --check` exits 0 — this plan adds no finding code, so the catalogue is unchanged. Full suite: 248/248 passing (242 pre-existing + 6 new).

## Task Commits

1. **Task 1: The interference case (REQ-P6-13)** — `df1674f` (feat)
2. **Task 2: Both halves of the Phase 9 monitoring pair (REQ-P6-13, D-06)** — `112af76` (feat)
3. **Task 3: Corpus invariants as a dedicated test module (REQ-P6-13)** — `e52c869` (test) — landed as a single commit rather than a RED/GREEN pair (see Deviations below)

**Plan metadata:** pending (final `docs(06-08)` commit follows this summary)

## Files Created/Modified

- `examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml` — new: shared-budget interference fixture
- `examples/known-bad/interference-shared-budget-POSTMORTEM.md` — new: paired post-mortem
- `examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml` — new: frequentist half of the Phase 9 pair
- `examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md` — new: paired post-mortem
- `examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml` — new: Bayesian half of the Phase 9 pair
- `examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md` — new: paired post-mortem, includes the mandatory formulation section
- `tests/test_known_bad_corpus.py` — new: 6-test corpus-invariant module

## Decisions Made

- **Full-shape cloning over minimal specs.** Every fixture carries the complete `good-ANALYSIS-SPEC.yaml` shape (decision, metrics, data, design, analysis, results, claims, assumptions, limitations, all ten `validity_frame` sub-blocks, full `inference` block) rather than a stripped-down spec built just to satisfy `dsx validate`. This was a deliberate choice beyond the acceptance-criteria floor: it keeps every fixture readable as a plausible real analysis (matching the plan's "structurally complete" framing) and means the only fields readers need to scrutinize for the defect are the ones the post-mortem points at.
- **`dsx validate` (CRITICAL-only) confirmed as the acceptance bar, not `dsx gate ship`.** Read `dsx/cli.py`'s `add_common(p_validate, "CRITICAL")` before writing any fixture, and cross-checked against Task 3's own action text (`cli.main(["validate", "--spec", str(path)])`). This meant fixtures did not need populated `visuals`/`reproducibility`/`narrative` sections the way the canonical good/bad fixtures do — those sections exist in the canonical fixtures to survive the fuller `ship`-level check suite, which known-bad fixtures are never asserted against in this phase.
- **Kohavi, Tang & Xu (2020) chapter locator flagged unverified, not fabricated**, per the plan's explicit "escalate rather than invent" instruction (mirrors 06-06's handling of the Deng citation). Author/title/venue/year are correct and match `brief.md` section 7's anchored source list; the specific chapter covering shared-budget/paid-media interference could not be confirmed against the source text at authoring time. **Escalating for human confirmation** before this citation is treated as fully verified — the Imbens & Rubin (2015) Ch.1 Sec.1.6 locator in the same post-mortem is cited with full confidence, since `dsx/spec.py`'s own `_validate_validity_frame_shape` docstring already anchors that exact locator.
- **`identification.constraint_source: informative_priors` used (with a justification) in the Bayesian fixture's `validity_frame.identification`**, since the fixture's whole point is a prior-based analysis — this is not the defect; it is honest, legal-vocabulary context around the actual defect (the false-positive-control claim in `claims`/`limitations` and the missing threshold calibration in `inference.fallback_rule`).

## Deviations from Plan

### Process deviation (not a Rule 1-4 auto-fix — documented per 06-05/06-06 precedent)

**Task 3's TDD RED/GREEN pair collapsed into a single `test(06-08)` commit.** The plan marks Task 3 `tdd="true"` and specifies the standard RED-then-GREEN cycle. Tasks 1 and 2 already landed the full known-bad corpus (three complete, structurally valid spec+post-mortem pairs) as `feat` commits before Task 3 began — there is no separate "implementation" left for Task 3 to drive with a failing test: the corpus invariants Task 3's tests assert (pairing, composition, structural validity, catch-attribution) were already true the moment the test module was written, because the fixtures they check were built correctly in Tasks 1–2. Writing a genuinely failing RED test would have required deliberately breaking the already-correct corpus first and then "fixing" it back — theater, not signal, and explicitly against the fail-fast guidance to investigate rather than force a spurious failure. I ran every acceptance-criteria script (glob-discovery source scan, pairing/count assertions, full suite, catalogue check) before committing; all pass. This mirrors 06-05's and 06-06's own documented TDD-granularity deviations for the same reason: the task's tests validate previously-landed, already-correct artifacts rather than driving new production code.

---

**Total deviations:** 1 process deviation (TDD commit granularity, no behavioral impact — nothing to auto-fix in this plan, no bugs found)
**Impact on plan:** Zero. Every acceptance criterion in all three tasks passes; the deviation changes commit-message cadence only, and follows established phase precedent.

## Issues Encountered

None. All three fixtures passed `dsx validate` with zero findings at any severity on first attempt, thanks to full-shape cloning from the proven-clean `good-ANALYSIS-SPEC.yaml` structure.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Phase 8's `DSX-INT-010` has a committed target at the exact filename ROADMAP Success Criterion 1 already names (`examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml`); the fixture's `interference.risk`/`mitigation`/`residual_note` combination is exactly what that phase will block on.
- Phase 9's `DSX-PAR-010`/`DSX-PAR-011` atomic pair (D-06) has both halves committed and passing structurally today, so neither code can ship without an already-waiting target — and the frequentist post-mortem's reference value is already pinned to the exact number `dsx.mathx.inflation_from_peeking(5)` returns, so Phase 9's own tests can assert against this fixture directly.
- Phase 12's catch-rate measurement (REQ-P12-02) has its first three "which code would have caught this" attributions recorded in machine-adjacent form (`DSX-<LETTERS>-<digits>` pattern, mechanically enforced by `test_known_bad_corpus.py`), and the corpus can grow past three pairs without editing the test module — it discovers by glob.
- **Open item for a human to confirm:** the Kohavi, Tang & Xu (2020) citation's exact chapter for the shared-budget interference pattern in `interference-shared-budget-POSTMORTEM.md` is flagged as unverified (see Decisions Made above) — author/title/venue/year are correct and match `brief.md`, but the chapter number was not confirmed against the source text.
- No blockers for 06-09/06-10. `git diff --stat dsx/ scripts/` is empty at every commit in this plan, exactly as scoped (this plan touches only `examples/known-bad/` and `tests/`).

---
*Phase: 06-contract-extension-decision-record-paradigm-manifest*
*Completed: 2026-08-08*

## Self-Check: PASSED

- FOUND: examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/interference-shared-budget-POSTMORTEM.md
- FOUND: examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md
- FOUND: examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
- FOUND: examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md
- FOUND: tests/test_known_bad_corpus.py
- FOUND: .planning/phases/06-contract-extension-decision-record-paradigm-manifest/06-08-SUMMARY.md
- FOUND commit: df1674f (feat(06-08): add interference-shared-budget known-bad fixture)
- FOUND commit: 112af76 (feat(06-08): add both halves of Phase 9 monitoring-pair known-bad fixtures)
- FOUND commit: e52c869 (test(06-08): corpus invariants for examples/known-bad (REQ-P6-13))
