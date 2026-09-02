"""DSX-STA-060/061/062: agreement declaration completeness (REQ-P18-04).

Presence + closed-vocabulary membership only — never a coherence or numeric-agreement
judgment (D-05; ICC combination-coherence is deferred as candidate DSX-STA-063). Drives
``_check_declared_association`` directly so the untouched ``_check_declared_test`` cannot
fire a false DSX-STA-041 (18-RESEARCH.md Pitfall 1).

The weighted-kappa ``weights`` field is the codebase's first field whose valid values span
an enum ({linear, quadratic}) AND a structural type (an explicit matrix). The guard branches
on ``isinstance`` BEFORE any normalize — a nested-list matrix is accepted, never stringified
(18-RESEARCH.md Pitfall 5). DSX-STA-062 requires BOTH p_pos and p_neg (D-04, the
HQ-16-corrected Feinstein-Cicchetti reading).

Stdlib-only, CRLF-safe. Mints nothing.
"""

from __future__ import annotations

import unittest

from dsx.checks import stats
from dsx.findings import Report

_VALID_ICC = {"model": "two_way_random", "type": "single", "definition": "absolute_agreement"}


def _codes(analysis: dict) -> list[str]:
    report = Report(check="test")
    stats._check_declared_association(analysis, {"analysis": analysis}, report)
    return [f.code for f in report.findings]


class Sta060IccTripleTest(unittest.TestCase):
    def test_fires_on_missing_definition(self):
        codes = _codes({"test": "icc", "icc": {"model": "two_way_random", "type": "single"}})
        self.assertIn("DSX-STA-060", codes)  # D-05: DSX-STA-060

    def test_fires_on_out_of_vocab_model(self):
        codes = _codes({"test": "icc", "icc": dict(_VALID_ICC, model="three_way")})
        self.assertIn("DSX-STA-060", codes)

    def test_silent_on_complete_valid_triple(self):
        codes = _codes({"test": "icc", "icc": dict(_VALID_ICC)})
        self.assertNotIn("DSX-STA-060", codes)

    def test_fires_once_only(self):
        codes = _codes({"test": "icc", "icc": {}})
        self.assertEqual(codes.count("DSX-STA-060"), 1)


class Sta061WeightedKappaWeightsTest(unittest.TestCase):
    def test_fires_on_blank_weights(self):
        codes = _codes({"test": "weighted_kappa", "p_pos": 0.9, "p_neg": 0.8})
        self.assertIn("DSX-STA-061", codes)  # D-05: DSX-STA-061

    def test_fires_on_unrecognised_string_weights(self):
        codes = _codes(
            {"test": "weighted_kappa", "weights": "cubic", "p_pos": 0.9, "p_neg": 0.8}
        )
        self.assertIn("DSX-STA-061", codes)

    def test_accepts_linear_weights(self):
        codes = _codes(
            {"test": "weighted_kappa", "weights": "linear", "p_pos": 0.9, "p_neg": 0.8}
        )
        self.assertNotIn("DSX-STA-061", codes)

    def test_accepts_quadratic_weights(self):
        codes = _codes(
            {"test": "weighted_kappa", "weights": "quadratic", "p_pos": 0.9, "p_neg": 0.8}
        )
        self.assertNotIn("DSX-STA-061", codes)

    def test_accepts_explicit_matrix_without_firing(self):
        """Pitfall 5: a non-empty nested list is a declared explicit weight matrix —
        accepted via the isinstance branch, never stringified against the token set."""
        codes = _codes(
            {
                "test": "weighted_kappa",
                "weights": [[1, 0.5], [0.5, 1]],
                "p_pos": 0.9,
                "p_neg": 0.8,
            }
        )
        self.assertNotIn("DSX-STA-061", codes)


class Sta062KappaCompanionsTest(unittest.TestCase):
    def test_fires_when_p_pos_missing(self):
        codes = _codes({"test": "cohens_kappa", "p_neg": 0.8})
        self.assertIn("DSX-STA-062", codes)  # D-05: DSX-STA-062

    def test_fires_when_p_neg_missing(self):
        codes = _codes({"test": "cohens_kappa", "p_pos": 0.9})
        self.assertIn("DSX-STA-062", codes)

    def test_fires_for_fleiss_kappa_missing_both(self):
        codes = _codes({"test": "fleiss_kappa"})
        self.assertIn("DSX-STA-062", codes)

    def test_silent_when_both_companions_present(self):
        codes = _codes({"test": "cohens_kappa", "p_pos": 0.9, "p_neg": 0.8})
        self.assertNotIn("DSX-STA-062", codes)


if __name__ == "__main__":
    unittest.main()
