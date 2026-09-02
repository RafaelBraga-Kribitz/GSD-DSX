"""recommend_association is dataless routing — the anti-two-stage proof (REQ-P18-01/06).

The load-bearing assertion is structural: ``inspect.signature(recommend_association)``
must list exactly one parameter, ``estimand_kind`` — no ``data``, no ``n``, no
distribution flag. A future contributor who adds a data-shape argument (turning the
lookup into a two-stage "inspect the data, then pick" procedure) turns this red, exactly
as ``tests/test_no_shapiro_autoswitch.py`` guards the ``recommend_test`` decision surface.
The routing assertions pin the three acceptable-coefficient SETs (D-01) and the
ValueError on a kind with no association route.

Stdlib-only, CRLF-safe (``\r?\n``). Mints nothing.
"""

from __future__ import annotations

import inspect
import re
import unittest
from pathlib import Path

from dsx.checks import stats

ROOT = Path(__file__).resolve().parent.parent
TEST_SELECTION = ROOT / "references" / "test-selection.md"


class RecommendAssociationSignatureTest(unittest.TestCase):
    def test_signature_is_exactly_estimand_kind_dataless(self):
        """The anti-two-stage proof (REQ-P18-06): the signature carries ONLY
        ``estimand_kind`` — no data/n/distribution parameter. This is a stronger
        guarantee than a branch of a function that already accepts data-shape args.
        """
        params = list(inspect.signature(stats.recommend_association).parameters)
        self.assertEqual(
            params, ["estimand_kind"],
            f"recommend_association must be dataless — its only parameter is "
            f"estimand_kind; found {params}. A data/n/distribution parameter would "
            "make it a two-stage inspect-then-pick procedure (REQ-P18-06).",
        )


class RecommendAssociationRoutingTest(unittest.TestCase):
    def test_linear_association_routes_pearson_and_point_biserial(self):
        self.assertEqual(
            set(stats.recommend_association("linear_association")["tests"]),
            {"pearson_correlation", "point_biserial"},
        )

    def test_monotone_association_routes_spearman_and_kendall(self):
        self.assertEqual(
            set(stats.recommend_association("monotone_association")["tests"]),
            {"spearman_correlation", "kendall_tau_b"},
        )

    def test_nominal_association_routes_phi_and_cramers_v(self):
        self.assertEqual(
            set(stats.recommend_association("nominal_association")["tests"]),
            {"phi", "cramers_v"},
        )

    def test_agreement_has_no_association_route(self):
        """agreement/method_comparison/ordered_trend route elsewhere — a ValueError,
        not a silent empty set, so a mis-call is loud."""
        with self.assertRaises(ValueError):
            stats.recommend_association("agreement")

    def test_return_shape_carries_effect_size_and_citation(self):
        out = stats.recommend_association("linear_association")
        self.assertIn("effect_size", out)
        self.assertIn("citation", out)


class CorrelationFamilyInvariantTest(unittest.TestCase):
    """CORRELATION_FAMILY (the set DSX-STA-051 keys on) must stay the exact union of the
    ``_ASSOCIATION_ROUTES`` acceptable-coefficient sets. The stats.py comment claims the
    two "cannot drift", but they are two separate module literals — only this test enforces
    it. A coefficient added to a route (or to the family) without the other turns this red,
    so DSX-STA-051's family and ``recommend_association``'s routes cannot silently diverge
    under permanent D-06 numbering (18-REVIEW.md LOW-1).
    """

    def test_family_equals_union_of_route_coefficient_sets(self):
        union = set().union(
            *(tests for tests, _effect, _citation in stats._ASSOCIATION_ROUTES.values())
        )
        self.assertEqual(set(stats.CORRELATION_FAMILY), union)


class AssociationDocMirrorTest(unittest.TestCase):
    """REQ-P18-01/02: the catalog-only pointer rows are present in the doc mirror."""

    def setUp(self):
        raw = TEST_SELECTION.read_text(encoding="utf-8")
        self.flat = re.sub(r"\s+", " ", raw.replace("\r\n", "\n")).lower()

    def test_pointer_rows_named(self):
        self.assertIn("association / agreement", self.flat)
        self.assertIn("distance correlation", self.flat)
        self.assertIn("partial correlation", self.flat)
        self.assertIn("cronbach", self.flat)
        self.assertIn("mcdonald", self.flat)


if __name__ == "__main__":
    unittest.main()
