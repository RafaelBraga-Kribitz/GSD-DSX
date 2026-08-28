"""Seeded, stdlib-only simulation evidence for REQ-P9-07 (D-14).

This module is evidence, never gate logic: nothing under ``dsx/`` imports it
and it is not reachable from any ``dsx gate`` invocation
(``test_no_module_under_dsx_imports_from_tests`` below is the mechanical
proof). It exists to prove, by direct simulation rather than assertion, that
the two formulations behind ``DSX-PAR-010`` (point-null / law-of-iterated-
logarithm) and ``DSX-PAR-011`` (prior-averaged, Deng, Lu & Chen 2016) are
genuinely different results with different properties. Swapping which
ceiling belongs to which formulation would produce a test that passes at one
horizon and fails at another — the "implementation bug for a day" brief
section 6.5 warns about.

Every random draw in this module comes from one ``random.Random(_SEED)``
instance, seeded with the literal integer ``_SEED`` defined below. Never
``random.seed()``, never wall-clock time, never ``os.urandom`` — the point of
an evidence artifact is that it reproduces.

Run on its own:  python3 -m unittest tests.test_par_monitoring_simulation -v
"""

from __future__ import annotations

import ast
import math
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dsx.mathx import inflation_from_peeking  # noqa: E402

# The one literal seed every simulation in this module draws from — the
# Armitage, McPherson & Rowe publication year this simulation's frequentist
# half is evidence for. Memorable, not magic; never random.seed(), never a
# clock.
_SEED = 1969

# Two-sided nominal alpha=0.05 critical value — the same constant
# pocock_boundary() uses for its alpha=0.05 base case.
_NAIVE_Z_THRESHOLD = 1.959963984540054
_LOOK_LADDER = (1, 2, 5, 10, 20)
_TREND_TRIALS = 4000

_K = 19  # the P(B>A) > 0.95 decision threshold DSX-PAR-011 gates on
_PRIOR_AVERAGED_TRIALS = 6000
_PRIOR_AVERAGED_MAX_LOOKS = 60
_PRIOR_AVERAGED_EFFECT = 2.0  # standardized mean shift under H1


def _simulate_naive_crossing_fractions(rng, ladder, trials, threshold):
    """Point-null / law-of-iterated-logarithm formulation.

    Simulate one Brownian-motion path per trial out to the largest look in
    ``ladder`` (cumulative sum of standard-normal increments, z-statistic at
    look ``i`` is the running sum divided by ``sqrt(i)``), and for each ``k``
    in ``ladder`` ask whether the naive z-statistic ever exceeded
    ``threshold`` within the first ``k`` looks.

    Every trial's per-``k`` indicator is nondecreasing in ``k`` by
    construction — crossing within the first ``k`` looks implies crossing
    within the first ``k'`` looks for any ``k' > k``, because it is the same
    underlying path — so the fraction aggregated across ``trials`` is
    guaranteed nondecreasing across ``ladder`` too. The monotone-trend
    property below is enforced by the simulation's structure, not left to
    sampling luck.
    """
    max_k = max(ladder)
    counts = [0] * len(ladder)
    for _ in range(trials):
        cum = 0.0
        crossed_at = None
        for i in range(1, max_k + 1):
            cum += rng.gauss(0.0, 1.0)
            z = cum / math.sqrt(i)
            if crossed_at is None and abs(z) > threshold:
                crossed_at = i
        for idx, k in enumerate(ladder):
            if crossed_at is not None and crossed_at <= k:
                counts[idx] += 1
    return [c / trials for c in counts]


def _simulate_prior_averaged_fdr(rng, k_threshold, trials, max_looks, effect):
    """Prior-averaged formulation (Deng, Lu & Chen 2016).

    A 1:1 prior over H0/H1 (``log(prior_odds) == 0`` at the start), sequential
    Gaussian log-likelihood-ratio updating each look, stopping the first time
    the posterior log-odds reach ``log(k_threshold)`` (i.e. posterior odds
    reach ``k_threshold``) or ``max_looks`` is exhausted with no stop.

    Returns ``(fdr, n_rejects)`` — the observed false-discovery rate among
    trials that stopped and rejected (``H0`` true given a "reject" decision)
    and the number of such trials. A trial that never reaches the threshold
    within ``max_looks`` contributes to neither the numerator nor the
    denominator, matching the property under test: the bound is conditional
    on stopping and rejecting, not unconditional.
    """
    log_k = math.log(k_threshold)
    n_rejects = 0
    n_false_rejects = 0
    for _ in range(trials):
        is_null = rng.random() < 0.5
        mu = 0.0 if is_null else effect
        log_odds = 0.0
        rejected = False
        for _look in range(max_looks):
            x = rng.gauss(mu, 1.0)
            # log-likelihood-ratio contribution of one N(effect, 1) vs N(0, 1) draw.
            log_odds += effect * x - 0.5 * effect * effect
            if log_odds >= log_k:
                rejected = True
                break
        if rejected:
            n_rejects += 1
            if is_null:
                n_false_rejects += 1
    if n_rejects == 0:
        return 0.0, 0
    return n_false_rejects / n_rejects, n_rejects


class ParMonitoringSimulationTests(unittest.TestCase):
    def test_point_null_crossing_fraction_is_nondecreasing_with_no_fixed_ceiling(self):
        """Under the point-null / law-of-iterated-logarithm formulation the
        naive type-I error tends to one as the horizon grows without bound,
        so no fixed ceiling is asserted here — asserting one would produce a
        test that passes at one horizon and fails at another, exactly the
        "implementation bug for a day" D-14 exists to catch. Only the
        direction of the trend and the fact that it moves are asserted."""
        rng = random.Random(_SEED)
        fractions = _simulate_naive_crossing_fractions(
            rng, _LOOK_LADDER, _TREND_TRIALS, _NAIVE_Z_THRESHOLD
        )
        for earlier, later in zip(fractions, fractions[1:]):
            self.assertLessEqual(earlier, later, fractions)
        self.assertGreater(fractions[-1], fractions[0], fractions)

    # D-05: DSX-PAR-011 — this test's reference value is the prior-averaged 1/(K+1) ceiling.
    def test_prior_averaged_fdr_is_at_or_below_the_1_over_k_plus_1_ceiling(self):
        """Prior-averaged formulation (Deng, Lu & Chen 2016): a one-sided
        Monte Carlo bound with an explicit three-standard-error margin, never
        an exact floating-point equality against a simulated statistic — the
        simulated FDR is a random variable, ``1/(K+1)`` is not."""
        rng = random.Random(_SEED)
        fdr, n_rejects = _simulate_prior_averaged_fdr(
            rng, _K, _PRIOR_AVERAGED_TRIALS, _PRIOR_AVERAGED_MAX_LOOKS, _PRIOR_AVERAGED_EFFECT
        )
        self.assertGreater(n_rejects, 100, "too few rejecting trials to bound the FDR")
        ceiling = 1.0 / (_K + 1)
        se = math.sqrt(max(fdr * (1.0 - fdr), 1e-9) / n_rejects)
        margin = 3.0 * se
        self.assertLessEqual(
            fdr, ceiling + margin,
            f"observed FDR {fdr} exceeds 1/(K+1)={ceiling} plus a 3-SE margin of {margin}",
        )

    def test_boundary_arithmetic_is_exact_in_binary64(self):
        """The boundary at the P(B>A) > 0.95 decision threshold (K=19) and one
        step either side of it (K=24, K=15), pinned by exact equality — these
        three fractions are exact in binary64, never approximate."""
        self.assertEqual(1 / (19 + 1), 0.05)
        self.assertEqual(1 / (24 + 1), 0.04)
        self.assertEqual(1 / (15 + 1), 0.0625)

    def test_villes_inequality_is_a_different_bound_over_a_different_event(self):
        """Ville's ``1/k`` at ``k=19`` (~0.0526) is strictly greater than the
        prior-averaged ``1/(K+1)`` at ``K=19`` (0.05) — the two are never
        interchangeable, and 0.0526 is not a rounding of 0.05. Ville's
        inequality bounds ``P(sup_t M_t >= a)`` for a nonnegative martingale
        started at 1; Deng's bound conditions on the decision to reject, a
        different event over a different formulation entirely."""
        self.assertGreater(1 / 19, 1 / (19 + 1))
        self.assertEqual(round(1 / 19, 4), 0.0526)

    def test_determinism_same_seed_same_summary_statistic(self):
        """Two runs seeded with the same literal integer produce identical
        summary statistics — mirrors scripts/check.sh's identical-input-
        identical-output idiom, applied to a simulation instead of a CLI."""
        first = _simulate_prior_averaged_fdr(
            random.Random(_SEED), _K, 500, _PRIOR_AVERAGED_MAX_LOOKS, _PRIOR_AVERAGED_EFFECT
        )
        second = _simulate_prior_averaged_fdr(
            random.Random(_SEED), _K, 500, _PRIOR_AVERAGED_MAX_LOOKS, _PRIOR_AVERAGED_EFFECT
        )
        self.assertEqual(first, second)

    def test_no_module_under_dsx_imports_from_tests(self):
        """Location is the enforcement mechanism for REQ-P9-07: this
        simulation must never become reachable from the gate path. Walks
        every ``.py`` file under ``dsx/`` with ``ast`` and asserts none of
        them imports the top-level ``tests`` package or any submodule of it,
        absolute or relative — the AST-scanner idiom test_frame_boundary.py
        established for the narrower D-03a boundary, applied here to a
        second, wider boundary: not just dsx/frame/, but the whole of
        dsx/. Nothing enforced this before this test existed."""
        violations: "list[str]" = []
        dsx_dir = ROOT / "dsx"
        files = sorted(dsx_dir.rglob("*.py"))
        self.assertTrue(files, "dsx/ has no *.py files to scan")
        for path in files:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name == "tests" or alias.name.startswith("tests."):
                            violations.append(f"{path}: imports {alias.name!r}")
                elif isinstance(node, ast.ImportFrom):
                    if node.level:
                        # A relative import from inside dsx/ can never resolve to the
                        # top-level tests package — dsx/ and tests/ are siblings, and a
                        # relative import only ever walks up within dsx/'s own package.
                        continue
                    module = node.module or ""
                    if module == "tests" or module.startswith("tests."):
                        violations.append(f"{path}: imports from {module!r}")
        self.assertEqual(violations, [], "\n".join(violations))

    def test_inflation_from_peeking_docstring_carries_the_full_citation(self):
        """The automated half of Task 1's acceptance: the citation, the
        reference-value line and the unverified-locator flag must exist on
        the function's own docstring, not merely in a plan document."""
        doc = inflation_from_peeking.__doc__ or ""
        self.assertIn("Citation:", doc)
        self.assertIn("Reference value:", doc)
        self.assertIn("1969", doc)
        self.assertIn("10.2307/2343787", doc)
        self.assertIn(
            "No table number and no page number within the paper was verified", doc
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
