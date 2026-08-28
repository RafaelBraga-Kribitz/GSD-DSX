"""Multiplicity-family reporting checks (Phase 11.3, REQ-P11.3-01/-02).

Stdlib unittest — no pytest dependency. Pins two behaviours of
``dsx/checks/design.py`` against inline spec dicts (the ``test_dsx.py``
convention), deliberately avoiding any YAML fixture under
``examples/known-bad/`` so this module never pulls in the corpus harness and
stays file-disjoint from the Wave-2 plans that touch ``test_dsx.py``:

  * DSX-EXP-053 (HIGH) — an under-declared multiplicity family (a non-empty
    list SHORTER than ``results.tests``) must fire and name the reported test
    metrics absent from the declared family (D-01, ROADMAP SC1).
  * DSX-EXP-051 (HIGH) — ``comparisons_looked_at`` exceeding the reported test
    count must fire whether or not a family is declared (D-02, ROADMAP SC2).

Run:  python3 -m unittest tests.test_multiplicity_family -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx.checks import design  # noqa: E402
from dsx.findings import Report  # noqa: E402


def codes(report: Report) -> "set[str]":
    return {f.code for f in report.findings}


def detail_for(report: Report, code: str) -> str:
    """The concatenated title+detail text of the first finding with ``code``."""
    for f in report.findings:
        if f.code == code:
            return f"{getattr(f, 'title', '')} {getattr(f, 'detail', '')}"
    return ""


class TestMultiplicityFamilyUnderDeclared(unittest.TestCase):
    # REQ-P11.3-01: DSX-EXP-053 — family smaller than the reported test set.

    def test_exp_053_fires_and_names_absent_metric(self):
        # family=[a, b] but three metrics reported {a, b, c} → fires naming c.
        spec = {
            "design": {
                "kind": "observational",
                "multiplicity": {
                    "family": ["a", "b"],
                    "correction": "benjamini_hochberg",
                },
            },
            "results": {
                "tests": [
                    {"metric": "a", "p_value": 0.01},
                    {"metric": "b", "p_value": 0.02},
                    {"metric": "c", "p_value": 0.03},
                ],
            },
        }
        report = design.check(spec)
        self.assertIn("DSX-EXP-053", codes(report))
        self.assertIn("c", detail_for(report, "DSX-EXP-053"))

    def test_exp_053_silent_when_family_ge_tests(self):
        # bad-fixture arithmetic: family=5, tests=3 → EXP-053 must stay silent.
        spec = {
            "design": {
                "kind": "observational",
                "multiplicity": {
                    "family": ["a", "b", "c", "d", "e"],
                    "correction": "none",
                },
            },
            "results": {
                "tests": [
                    {"metric": "a", "p_value": 0.01},
                    {"metric": "b", "p_value": 0.02},
                    {"metric": "c", "p_value": 0.03},
                ],
            },
        }
        self.assertNotIn("DSX-EXP-053", codes(design.check(spec)))

    def test_exp_053_no_traceback_on_malformed_block(self):
        # T-11.3-01: a malformed multiplicity/results block must degrade, not raise.
        spec = {
            "design": {"multiplicity": {"family": "not-a-list", "correction": "none"}},
            "results": {"tests": [{"no_metric_key": True}, "not-a-dict"]},
        }
        report = design.check(spec)  # must not raise
        self.assertNotIn("DSX-EXP-053", codes(report))

    def test_exp_053_no_traceback_on_nonscalar_family(self):
        # WR-03 (11.3 S2-4 review): a family declared as a list of mappings and
        # shorter than the reported tests enters the DSX-EXP-053 branch. The
        # naming set-difference must degrade to a controlled finding, never a
        # gate-path TypeError (set() over unhashable dicts).
        spec = {
            "design": {
                "kind": "observational",
                "multiplicity": {
                    "family": [{"metric": "churn"}],  # list of mappings
                    "correction": "holm",
                },
            },
            "results": {
                "tests": [
                    {"metric": "churn", "p_value": 0.01},
                    {"metric": "arpu", "p_value": 0.02},
                ],
            },
        }
        report = design.check(spec)  # must not raise
        # Count-based fire is unchanged (len(family)=1 < len(tests)=2); the
        # non-string family member simply names no metric it cannot cover.
        self.assertIn("DSX-EXP-053", codes(report))
        detail = detail_for(report, "DSX-EXP-053")
        self.assertIn("churn", detail)
        self.assertIn("arpu", detail)

    def test_exp_053_no_traceback_on_nonscalar_test_metric(self):
        # WR-03 sibling site: a test whose `metric` is a non-scalar (dict) must
        # not crash the `reported` set-comprehension; it is skipped, the scalar
        # metrics are still named.
        spec = {
            "design": {
                "kind": "observational",
                "multiplicity": {"family": ["churn"], "correction": "holm"},
            },
            "results": {
                "tests": [
                    {"metric": {"nested": "x"}, "p_value": 0.01},
                    {"metric": "arpu", "p_value": 0.02},
                    {"metric": "ltv", "p_value": 0.03},
                ],
            },
        }
        report = design.check(spec)  # must not raise
        self.assertIn("DSX-EXP-053", codes(report))
        detail = detail_for(report, "DSX-EXP-053")
        self.assertIn("arpu", detail)
        self.assertIn("ltv", detail)

    def test_exp_053_no_traceback_on_nondict_test_entry(self):
        # WR-03 sibling site: a bare non-dict test entry must not crash the
        # `reported` comprehension (t.get on a str) — it is skipped.
        spec = {
            "design": {
                "kind": "observational",
                "multiplicity": {"family": ["churn"], "correction": "holm"},
            },
            "results": {
                "tests": [
                    "not-a-dict",
                    {"metric": "arpu", "p_value": 0.02},
                    {"metric": "ltv", "p_value": 0.03},
                ],
            },
        }
        report = design.check(spec)  # must not raise
        self.assertIn("DSX-EXP-053", codes(report))


class TestExploratoryLooksFamilyIndependent(unittest.TestCase):
    # REQ-P11.3-02: DSX-EXP-051 — fires on the reported test count, family or not.

    def test_exp_051_fires_with_no_family_declared(self):
        # D-15c: family absent, tests len 3, comparisons_looked_at 5 → fires.
        spec = {
            "design": {"kind": "observational"},
            "results": {
                "comparisons_looked_at": 5,
                "tests": [
                    {"metric": "a", "p_value": 0.01},
                    {"metric": "b", "p_value": 0.02},
                    {"metric": "c", "p_value": 0.03},
                ],
            },
        }
        report = design.check(spec)
        self.assertIn("DSX-EXP-051", codes(report))
        # the ratio ("N examined, M reported") is quoted in the detail
        detail = detail_for(report, "DSX-EXP-051")
        self.assertIn("5", detail)
        self.assertIn("3", detail)

    def test_exp_051_silent_on_good_arithmetic(self):
        # good-fixture arithmetic: max(3, 3) = 3, looked = 3, not > 3 → silent.
        spec = {
            "design": {
                "kind": "observational",
                "multiplicity": {
                    "family": ["a", "b", "c"],
                    "correction": "benjamini_hochberg",
                },
            },
            "results": {
                "comparisons_looked_at": 3,
                "tests": [
                    {"metric": "a", "p_value": 0.01},
                    {"metric": "b", "p_value": 0.02},
                    {"metric": "c", "p_value": 0.03},
                ],
            },
        }
        self.assertNotIn("DSX-EXP-051", codes(design.check(spec)))


if __name__ == "__main__":
    unittest.main()
