"""DSX-STA-050/051: declared correlation coefficient vs declared scale/kind (REQ-P18-03).

Drives ``_check_declared_association`` DIRECTLY (not through ``stats.check(spec)``) so the
untouched ``_check_declared_test`` can never fire a false DSX-STA-041 against these fixtures
(18-RESEARCH.md Pitfall 1). Every test still asserts DSX-STA-041 is ABSENT from the
findings, so a future refactor that routes through the full entry point cannot silently
reintroduce the false 041 without turning this red.

D-03 whitelist: DSX-STA-050 fires ONLY for Pearson r against a declared-``ordinal`` operand;
a declared ``point_biserial`` and any declared-``dichotomous`` (2-level) operand are
whitelisted (point-biserial IS Pearson r on a {0,1} dichotomy), and an absent operand_scale
is non-blocking.

Stdlib-only, CRLF-safe. Mints nothing.
"""

from __future__ import annotations

import unittest

from dsx.checks import stats
from dsx.findings import Report


def _codes(analysis: dict) -> list[str]:
    report = Report(check="test")
    stats._check_declared_association(analysis, {"analysis": analysis}, report)
    return [f.code for f in report.findings]


class Sta050ScaleGateTest(unittest.TestCase):
    def test_fires_for_pearson_against_ordinal_operand(self):
        codes = _codes({"test": "pearson_correlation", "operand_scale": "ordinal"})
        self.assertIn("DSX-STA-050", codes)  # D-05: DSX-STA-050
        self.assertNotIn("DSX-STA-041", codes)  # Pitfall 1: no false 041

    def test_whitelist_point_biserial_never_fires_050(self):
        codes = _codes({"test": "point_biserial", "operand_scale": "ordinal"})
        self.assertNotIn("DSX-STA-050", codes)
        self.assertNotIn("DSX-STA-041", codes)

    def test_whitelist_dichotomous_operand_never_fires_050(self):
        codes = _codes({"test": "pearson_correlation", "operand_scale": "dichotomous"})
        self.assertNotIn("DSX-STA-050", codes)
        self.assertNotIn("DSX-STA-041", codes)

    def test_absent_operand_scale_is_non_blocking(self):
        codes = _codes({"test": "pearson_correlation"})
        self.assertNotIn("DSX-STA-050", codes)
        self.assertNotIn("DSX-STA-041", codes)


class Sta051KindGateTest(unittest.TestCase):
    def test_fires_for_correlation_family_on_agreement(self):
        codes = _codes({"test": "pearson_correlation", "estimand_kind": "agreement"})
        self.assertIn("DSX-STA-051", codes)  # D-05: DSX-STA-051
        self.assertNotIn("DSX-STA-041", codes)

    def test_fires_for_correlation_family_on_method_comparison(self):
        codes = _codes({"test": "spearman_correlation", "estimand_kind": "method_comparison"})
        self.assertIn("DSX-STA-051", codes)
        self.assertNotIn("DSX-STA-041", codes)

    def test_silent_for_correlation_family_on_association_kind(self):
        codes = _codes({"test": "spearman_correlation", "estimand_kind": "monotone_association"})
        self.assertNotIn("DSX-STA-051", codes)
        self.assertNotIn("DSX-STA-041", codes)

    def test_silent_for_non_correlation_test_on_agreement(self):
        codes = _codes({"test": "cohens_kappa", "estimand_kind": "agreement"})
        self.assertNotIn("DSX-STA-051", codes)


if __name__ == "__main__":
    unittest.main()
