"""Golden-file finding-set equality over every ``examples/**`` fixture, plus the
noun-homograph negative case (REQ-P11.2-03, D-06, plan 11.2-08).

This is the phase's verdict-neutrality gate. The causal-verb lexicon was widened
across this milestone (the two-tier always-hit / purpose-gated split in
``dsx/spec.py::causal_verb_matches``, consumed by
``dsx/checks/claims.py::_check_causal_language`` and
``dsx/checks/coherence.py::_check_decision_language``). A widening is only safe if
it changed no existing fixture's verdict except where a fixture was built to
demonstrate the new catch. This module pins every committed fixture's
CRITICAL/HIGH finding set at ``dsx gate ship`` against a golden baseline measured
2026-08-26, so any future lexicon or check change that moves a finding set — adds
a finding, drops one, or shifts a severity across the CRITICAL/HIGH line — turns
this suite red rather than sliding through unnoticed.

The golden baseline is the *measured* reality, not an aspiration: each set below
was read off a real ``dsx gate ship --json`` run against a fresh
``tempfile.TemporaryDirectory()`` per fixture (never the shared
``examples/known-bad/DECISIONS.jsonl`` — its identity-free floor would trip
``DSX-PRE-041`` on a shared root, RESEARCH landmine f). A plan-time header is
seeded first, exactly as ``tests/test_known_bad_corpus.py::_gate_findings`` does,
because from Phase 10 ``prereg`` makes the trail a gate input at ship and a
missing header aborts the run at exit 2.

The two live noun-collision sites this widening had to leave untouched are
asserted explicitly, in addition to the generic equality:
  * ``weak-identification-mmm`` — its decision-rule and claim prose name media
    channels and revenue with no purpose-gated recommendation, so no causal-verb
    finding may fire against it.
  * the good fixture — its ``results.tests[].interpretation`` carries the phrase
    "activation increase", a bare purpose-gated homograph with no preceding
    purpose marker, which must not be read as a causal verb.

Run:  python3 -m unittest tests.test_causal_verb_golden -v
"""

from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from _trail_seed import seed_plan_header  # noqa: E402
from dsx import cli  # noqa: E402
from dsx.checks import claims as claims_check  # noqa: E402
from dsx.checks import coherence as coherence_check  # noqa: E402
from dsx.loader import load  # noqa: E402

EXAMPLES_DIR = ROOT / "examples"
SPEC_GLOB = "**/*-ANALYSIS-SPEC.yaml"

# The three causal-verb finding codes the two-tier lexicon feeds: the two claim
# codes (``dsx/checks/claims.py::_check_causal_language``) and the one coherence
# code (``dsx/checks/coherence.py::_check_decision_language``). The noun-collision
# and negative-case assertions below are scoped to exactly this set — a fixture
# may legitimately carry any number of *other* findings; what the widening must
# never do is fire one of these three against prose that names no recommendation.
_CAUSAL_VERB_CODES = frozenset({"DSX-CLM-010", "DSX-CLM-011", "DSX-COH-010"})

# Golden per-fixture CRITICAL/HIGH finding set at ``dsx gate ship``, keyed by the
# fixture's POSIX path relative to the repository root. Measured 2026-08-26 (plan
# 11.2-08) against a fresh tempfile.TemporaryDirectory() per fixture, with a
# plan-time header seeded first. This is the pinned post-widening reality: the
# only fixture carrying a causal-verb code
# (``prescriptive-churn-recommendation``) is this phase's own flagship, whose
# DSX-COH-010 (a causal decision-rule under a descriptive question) plus
# DSX-CLM-020 (a prescriptive claim with no identification) are the catch it
# exists to demonstrate. DSX-CLM-011 no longer fires on the prescriptive claim:
# WR-01 (11.2 code review, §4 persona round) exempted prescriptive from
# _check_causal_language because it double-coded the DSX-CLM-020 fact and gave a
# strength-downgrade remedy. The flagship still blocks (CLM-020/COH-001/COH-010
# all CRITICAL); every other fixture's set is exactly what it was before.
_GOLDEN_SHIP_FINDINGS: "dict[str, frozenset[str]]" = {
    "examples/bad-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-ADM-020", "DSX-CAU-010", "DSX-CLM-020", "DSX-CLM-030", "DSX-CLM-033",
        "DSX-CLM-070", "DSX-CLM-080", "DSX-CODE-001", "DSX-CODE-002", "DSX-COH-020",
        "DSX-COH-031", "DSX-DEC-020", "DSX-DQ-001", "DSX-EXP-006", "DSX-EXP-011",
        "DSX-EXP-021", "DSX-EXP-050", "DSX-EXP-051", "DSX-EXP-060", "DSX-FIG-001",
        "DSX-FIG-030", "DSX-INT-010", "DSX-MET-001", "DSX-MET-011", "DSX-MET-020",
        "DSX-MET-030", "DSX-MET-040", "DSX-ML-011", "DSX-ML-012", "DSX-ML-021",
        "DSX-ML-022", "DSX-ML-032", "DSX-ML-041", "DSX-ML-050", "DSX-ML-060",
        "DSX-ML-070", "DSX-ML-071", "DSX-ML-072", "DSX-ML-090", "DSX-NAR-010",
        "DSX-REP-050", "DSX-SMELL-009", "DSX-SMELL-010", "DSX-SMELL-013",
        "DSX-SPEC-010", "DSX-SPEC-026", "DSX-SPEC-081", "DSX-SPEC-082",
        "DSX-SPEC-085", "DSX-SQL-001", "DSX-SQL-007", "DSX-SQL-008", "DSX-SQL-012",
        "DSX-STA-002", "DSX-STA-003", "DSX-STA-007", "DSX-STA-020", "DSX-STA-041",
        "DSX-VAL-011", "DSX-VIZ-001", "DSX-VIZ-012", "DSX-VIZ-013", "DSX-VIZ-020",
        "DSX-VIZ-030", "DSX-VIZ-051", "DSX-VIZ-061", "DSX-VIZ-063", "DSX-VIZ-070",
    }),
    "examples/good-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-DQ-001", "DSX-FIG-001", "DSX-NAR-010",
    }),
    # Phase 12-04 (REQ-P12-03, D-04): the good-side FPR control corpus — twelve
    # genuinely clean ANALYSIS-SPECs spanning both paradigms (6 frequentist, 6
    # Bayesian) and all three outcome shapes (proportion, continuous, count/ratio),
    # so the false-positive rate has a denominator with resolution rather than 0/1.
    # Each set below was measured 2026-08-27 against a fresh
    # tempfile.TemporaryDirectory() per spec via _ship_findings above (never
    # guessed). Every set is frozenset(): unlike examples/good-ANALYSIS-SPEC.yaml
    # (which references sibling artifacts absent from the fresh tempdir and so
    # fires the four artifact-stripping noise codes), each control spec takes the
    # minimal-reference route — it references only committed, cwd-resolvable
    # artifacts (a per-spec NARRATIVE.md doubling as claim evidence, and the shared
    # examples/good-corpus/_control_readout.py entrypoint) — so a fresh-tempdir
    # ship run resolves every reference and fires none of DSX-DQ-001 /
    # DSX-CLM-031 / DSX-FIG-001 / DSX-NAR-010. plan 12-05 therefore needs no
    # tempdir sibling-seeding for this corpus; the FPR count is honest at zero.
    "examples/good-corpus/bayes-continuous-nps-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/bayes-continuous-revenue-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/bayes-count-sessions-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/bayes-count-tickets-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/bayes-proportion-adoption-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/bayes-proportion-signup-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/freq-continuous-aov-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/freq-continuous-timeontask-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/freq-count-installs-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/freq-count-referrals-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/freq-proportion-checkout-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/good-corpus/freq-proportion-email-open-ANALYSIS-SPEC.yaml": frozenset(),
    "examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-COH-031", "DSX-MET-040", "DSX-NAR-001", "DSX-PAR-011",
        "DSX-REP-001", "DSX-REP-030", "DSX-STA-041", "DSX-VAL-041",
    }),
    "examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-COH-031", "DSX-EXP-007", "DSX-MET-040", "DSX-NAR-001",
        "DSX-PAR-010", "DSX-REP-030",
    }),
    # Phase 11.3-01 (D-02): DSX-EXP-051 now fires family-independently — this fixture
    # declares comparisons_looked_at:5 with no multiplicity.family and no results.tests
    # (base=0), a real undisclosed-multiple-comparisons catch incidental to its
    # data-leakage target. Measured re-baseline, §4 persona round (rigour); still BLOCKS.
    "examples/known-bad/full-frame-cleaning-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-CODE-020", "DSX-CODE-021", "DSX-CODE-030", "DSX-COH-031",
        "DSX-EXP-051", "DSX-MET-040", "DSX-ML-090", "DSX-NAR-001",
    }),
    # Phase 12-01 (REQ-P12-01/02, D-01/D-02): three coverage-class MISS fixtures.
    # Each set measured 2026-08-27 against a fresh tempfile.TemporaryDirectory()
    # per fixture with a plan-time header seeded, via _ship_findings above — never
    # guessed. Each fixture encodes a defect a declaration-only gate cannot catch
    # (undisclosed forking / data fabrication / undisclosed selective exclusion),
    # so every code below is a shared corpus-completeness incidental gap
    # (_INCIDENTAL_GAP_CODES in tests/test_known_bad_corpus.py), not the encoded
    # miss; the miss's absent-code attribution lives in each fixture's
    # <slug>-ATTRIBUTION.yaml sidecar (D-06/D-07).
    "examples/known-bad/garden-of-forking-paths-p-hacking-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-COH-031", "DSX-DEC-001", "DSX-MET-040", "DSX-NAR-001",
        "DSX-REP-030", "DSX-REP-050",
    }),
    "examples/known-bad/retracted-fabricated-field-experiment-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-COH-031", "DSX-DEC-001", "DSX-MET-040", "DSX-NAR-001",
        "DSX-REP-030", "DSX-REP-050",
    }),
    # question_type: descriptive, so no decision.replay requirement (no DSX-DEC-001)
    # and no unchecked-assumption gap (no DSX-COH-031) fire; the measured set is
    # correspondingly smaller.
    "examples/known-bad/operator-known-answer-selective-exclusion-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-MET-040", "DSX-NAR-001", "DSX-REP-030", "DSX-REP-050",
    }),
    "examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-COH-031", "DSX-INT-010", "DSX-MET-040", "DSX-NAR-001",
        "DSX-REP-030",
    }),
    # Phase 11.3-01 (D-02): DSX-EXP-051 now fires family-independently — this fixture
    # declares comparisons_looked_at:5 with no multiplicity.family and no results.tests
    # (base=0), a real undisclosed-multiple-comparisons catch incidental to its
    # procedure-switch target. Measured re-baseline, §4 persona round (rigour); still BLOCKS.
    "examples/known-bad/post-hoc-procedure-switch-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-COH-031", "DSX-EXP-051", "DSX-MET-040", "DSX-NAR-001",
        "DSX-PRE-030", "DSX-REP-030", "DSX-STA-041",
    }),
    "examples/known-bad/prescriptive-churn-recommendation-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-020", "DSX-CLM-031", "DSX-COH-001", "DSX-COH-010",
        "DSX-MET-040", "DSX-NAR-001", "DSX-REP-030",
    }),
    "examples/known-bad/triggering-dilution-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-COH-031", "DSX-INT-030", "DSX-MET-040", "DSX-NAR-001",
        "DSX-REP-030",
    }),
    "examples/known-bad/weak-identification-mmm-ANALYSIS-SPEC.yaml": frozenset({
        "DSX-CLM-031", "DSX-COH-031", "DSX-INT-030", "DSX-MET-040", "DSX-NAR-001",
        "DSX-REP-030", "DSX-VAL-040",
    }),
}


def _seed_entrypoint(tmp: "str | Path", spec_path: "str | Path") -> None:
    """Copy a fixture's own declared ``reproducibility.entrypoint`` into ``tmp``.

    Mirrors ``tests/test_known_bad_corpus.py::_seed_entrypoint`` (plan 11.1-08):
    the fresh-temporary-directory-per-call choice makes a fixture's entrypoint
    unreachable to the entrypoint check unless it is seeded there first, because
    the resolve root a real ``dsx gate`` run passes to ``code.check`` is that
    temporary directory. A no-op for every fixture that declares no entrypoint.
    """
    spec = load(str(spec_path))
    repro = spec.get("reproducibility")
    entry = repro.get("entrypoint") if isinstance(repro, dict) else None
    if not isinstance(entry, str) or not entry.strip():
        return
    source = Path(spec_path).parent / entry
    if not source.is_file():
        return
    dest = Path(tmp) / entry
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, dest)


def _ship_findings(spec_path: Path) -> "frozenset[str]":
    """Run one real ``dsx gate ship --json`` against ``spec_path`` in a fresh
    temporary phase directory and return its sorted CRITICAL/HIGH finding-code set.

    Seeds the fixture's entrypoint and a plan-time header first, exactly as
    ``tests/test_known_bad_corpus.py::_gate_findings`` does, so ``prereg``'s
    content-lock reconciliation has a header to read and the run reaches the
    emitter rather than aborting at exit 2. Blocking output goes to stderr and
    passing output to stdout (``dsx/findings.py::emit``), so whichever stream is
    non-empty holds the JSON report.
    """
    with tempfile.TemporaryDirectory() as tmp:
        _seed_entrypoint(tmp, spec_path)
        seed_plan_header(tmp, spec_path)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            cli.main(
                ["gate", "ship", "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
            )
        raw = err.getvalue() or out.getvalue()
        report = json.loads(raw)
    return frozenset(
        f["code"] for f in report["findings"] if f.get("severity") in ("CRITICAL", "HIGH")
    )


class TestCausalVerbGolden(unittest.TestCase):
    def _spec_paths(self) -> "list[Path]":
        return sorted(EXAMPLES_DIR.glob(SPEC_GLOB))

    def test_golden_keys_match_the_examples_tree_on_disk(self):
        """A fixture added or removed under ``examples/`` without updating the
        golden baseline fails loudly here, rather than silently escaping the
        per-fixture equality below (a fixture with no golden entry would never be
        gated)."""
        disk = {p.relative_to(ROOT).as_posix() for p in self._spec_paths()}
        golden = set(_GOLDEN_SHIP_FINDINGS)
        self.assertEqual(
            golden, disk,
            "the golden baseline and the examples/ tree on disk disagree: "
            f"{sorted(golden ^ disk)} — every ANALYSIS-SPEC under examples/ must "
            "have a measured golden entry, and every golden key must name a real "
            "fixture",
        )

    def test_every_fixture_ship_finding_set_equals_its_golden_baseline(self):
        """The verdict-neutrality gate. For every fixture under ``examples/**``,
        the CRITICAL/HIGH finding set at ``dsx gate ship`` is exactly its committed
        golden set — the causal-verb widening added or removed no finding from any
        fixture except the flagship's own expected catch, which is baked into the
        golden set above and therefore not an exception to this equality but a
        pinned member of it."""
        specs = self._spec_paths()
        self.assertTrue(specs, "no ANALYSIS-SPEC fixtures found under examples/")
        for path in specs:
            rel = path.relative_to(ROOT).as_posix()
            with self.subTest(spec=rel):
                measured = _ship_findings(path)
                expected = _GOLDEN_SHIP_FINDINGS[rel]
                self.assertEqual(
                    measured, expected,
                    f"{rel} ship finding set drifted from its golden baseline:\n"
                    f"  added:   {sorted(measured - expected)}\n"
                    f"  dropped: {sorted(expected - measured)}\n"
                    "Investigate the cause and fix the check or the fixture — do "
                    "NOT edit the golden set to absorb an unexpected change "
                    "(T-11.2-13).",
                )

    def test_weak_identification_mmm_fires_no_causal_verb_finding(self):
        """The first live noun-collision site: weak-identification-mmm's prose
        names media channels and revenue but recommends no purpose-gated
        intervention, so none of the three causal-verb codes may fire against it —
        the widening must be blind to it."""
        path = EXAMPLES_DIR / "known-bad" / "weak-identification-mmm-ANALYSIS-SPEC.yaml"
        measured = _ship_findings(path)
        self.assertEqual(
            measured & _CAUSAL_VERB_CODES, frozenset(),
            "weak-identification-mmm fired a causal-verb finding "
            f"{sorted(measured & _CAUSAL_VERB_CODES)} — the widening must not read "
            "its channel/revenue prose as a recommendation",
        )

    def test_good_fixture_fires_no_causal_verb_finding(self):
        """The second live noun-collision site: the good fixture's
        ``results.tests[].interpretation`` carries "activation increase", a bare
        purpose-gated homograph with no preceding purpose marker. It must not be
        read as a causal verb, so none of the three causal-verb codes may fire."""
        path = EXAMPLES_DIR / "good-ANALYSIS-SPEC.yaml"
        measured = _ship_findings(path)
        self.assertEqual(
            measured & _CAUSAL_VERB_CODES, frozenset(),
            "the good fixture fired a causal-verb finding "
            f"{sorted(measured & _CAUSAL_VERB_CODES)} — 'activation increase' is a "
            "noun homograph, not a recommendation",
        )


class TestNounNegativeCase(unittest.TestCase):
    """The purpose-gate's whole reason to exist: a bare purpose-gated homograph
    ("increase") with no preceding purpose marker names a quantity, not a
    recommendation, and must fire no causal-verb finding. Exercised as an inline
    synthetic spec run straight through ``claims.check`` and ``coherence.check`` —
    NOT a committed known-bad fixture, because a known-bad fixture must block and
    this input must not. No text is matched against file bytes here, so there is
    no CRLF surface; the assertions read finding codes off the returned Reports."""

    NOUN_SPEC = {
        "question_type": "descriptive",
        "decision": {
            "owner": "analytics",
            "decision_rule": "Report whether sales increase in Q4 relative to Q3.",
        },
        "claims": [
            {
                "text": "Sales increase in Q4 relative to Q3.",
                "type": "descriptive",
                "evidence": "RESULTS.md#sales",
                "population": "all Q4 orders",
            }
        ],
    }

    def _codes(self, report) -> "set[str]":
        return {f.code for f in report.findings}

    def test_claims_check_emits_no_causal_verb_code_on_a_noun(self):
        report = claims_check.check(self.NOUN_SPEC)
        codes = self._codes(report)
        for code in ("DSX-CLM-010", "DSX-CLM-011"):
            with self.subTest(code=code):
                self.assertNotIn(
                    code, codes,
                    f"claims.check fired {code} on the noun phrase 'sales increase "
                    "in Q4' — a bare purpose-gated homograph with no purpose marker "
                    "must not be read as a causal verb",
                )

    def test_coherence_check_emits_no_causal_verb_code_on_a_noun(self):
        report = coherence_check.check(self.NOUN_SPEC)
        codes = self._codes(report)
        self.assertNotIn(
            "DSX-COH-010", codes,
            "coherence.check fired DSX-COH-010 on the decision rule 'report whether "
            "sales increase in Q4' — the bare homograph 'increase' has no preceding "
            "purpose marker and must not be read as a causal decision rule",
        )


if __name__ == "__main__":
    unittest.main()
