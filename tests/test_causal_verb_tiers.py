"""Phase 11.2 Plan 02 (REQ-P11.2-03): the tiered causal-verb lexicon widening.

D-04: ``CAUSAL_VERBS`` (spec.py:52-60) has finite verbs but lacks bare
infinitives ("reduce", "increase", "decrease") and gerunds ("reducing",
"increasing"), so a recommendation phrased "...to reduce churn" passes
clean. This pins the two-tier fix: an always-hit set (finite verbs +
gerunds) and a purpose-gated set (bare infinitives / noun-homographs),
routed through a shared ``causal_verb_matches`` helper in both
``_check_causal_language`` (DSX-CLM-010/011) and ``_check_decision_language``
(DSX-COH-010). Mints no new finding code (one-fact-one-code, D-04).

The gerund is NOT an epistemic softener — only genuine ``HEDGE_TERMS`` route
to the MEDIUM path; a bare gerund with no hedge is CRITICAL like any other
causal verb hit (D-04 amendment to REQ-P11.2-03's literal wording).

Run:  python -m unittest tests.test_causal_verb_tiers -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx.checks import claims, coherence  # noqa: E402
from dsx.findings import Report, Severity  # noqa: E402


def codes(report: Report) -> set[str]:
    return {f.code for f in report.findings}


def _claims_spec(text: str, ctype: str) -> dict:
    return {
        "claims": [{"text": text, "type": ctype, "evidence": "n/a"}],
        "design": {},
        "results": {},
    }


class TestCausalVerbTiers(unittest.TestCase):
    def test_tier1_bare_infinitive_in_purpose_construction_fires_clm011(self):
        """Test 1 (Tier 1 claim): 'offer bundled incentives to reduce churn',
        typed 'association', must fire DSX-CLM-011 CRITICAL. RED today
        because 'reduce' (bare infinitive) is not in CAUSAL_VERBS — only
        'reduces'/'reduced' are."""
        report = claims.check(_claims_spec("offer bundled incentives to reduce churn", "association"))
        clm011 = [f for f in report.findings if f.code == "DSX-CLM-011"]
        self.assertEqual(
            len(clm011), 1,
            f"expected exactly one DSX-CLM-011, got codes={codes(report)}",
        )
        self.assertEqual(clm011[0].severity, Severity.CRITICAL)

    def test_tier1_bare_infinitive_in_decision_rule_fires_coh010(self):
        """Test 2 (Tier 1 decision rule): a descriptive question with a
        decision_rule containing 'to reduce churn' must fire DSX-COH-010
        CRITICAL. RED today for the same reason as Test 1."""
        report = coherence.check(
            {
                "question_type": "descriptive",
                "claims": [],
                "decision": {"decision_rule": "Offer bundled incentives to reduce churn"},
                "design": {},
            }
        )
        coh010 = [f for f in report.findings if f.code == "DSX-COH-010"]
        self.assertEqual(
            len(coh010), 1,
            f"expected exactly one DSX-COH-010, got codes={codes(report)}",
        )
        self.assertEqual(coh010[0].severity, Severity.CRITICAL)

    def test_gerund_with_hedge_routes_to_clm010_medium(self):
        """Test 3 (gerund + hedge): 'reducing churn may be possible', typed
        'association', must fire DSX-CLM-010 MEDIUM — the verb hit (gerund)
        plus the genuine HEDGE_TERMS hit ('may') route through the existing
        softener path. Passes today only by accident of 'reduces'/'reduced'
        matching being absent; asserted here to pin the post-widening
        routing precisely."""
        report = claims.check(_claims_spec("reducing churn may be possible", "association"))
        self.assertNotIn("DSX-CLM-011", codes(report))
        clm010 = [f for f in report.findings if f.code == "DSX-CLM-010"]
        self.assertEqual(
            len(clm010), 1,
            f"expected exactly one DSX-CLM-010, got codes={codes(report)}",
        )
        self.assertEqual(clm010[0].severity, Severity.MEDIUM)

    def test_gerund_without_hedge_fires_clm011_not_medium(self):
        """Test 4 (gerund, no hedge): 'increasing spend drives revenue',
        typed 'association', must fire DSX-CLM-011 CRITICAL — NOT
        DSX-CLM-010 MEDIUM. The gerund is a verb hit, not a softener (D-04
        amendment). This case already contains the finite verb 'drives', so
        it is expected to already fire CRITICAL pre-widening; it is asserted
        here to pin that the post-widening gerund path does not accidentally
        downgrade it to MEDIUM."""
        report = claims.check(_claims_spec("increasing spend drives revenue", "association"))
        self.assertNotIn("DSX-CLM-010", codes(report))
        clm011 = [f for f in report.findings if f.code == "DSX-CLM-011"]
        self.assertEqual(
            len(clm011), 1,
            f"expected exactly one DSX-CLM-011, got codes={codes(report)}",
        )
        self.assertEqual(clm011[0].severity, Severity.CRITICAL)

    def test_negative_noun_no_purpose_context_produces_zero_findings(self):
        """Test 5 (negative noun, D-06 negative case): 'sales increase in
        Q4', typed 'descriptive', must produce zero causal-verb findings —
        the bare noun-homograph 'increase' has no purpose/recommendation
        marker before it, so the gate stays shut. RED today because
        'increase' (bare) is a substring the naive `verb in lowered` scan
        would catch once 'increase' is added to any flat lexicon; this pins
        that the widening must be purpose-gated, not a flat addition."""
        report = claims.check(_claims_spec("sales increase in Q4", "descriptive"))
        self.assertNotIn("DSX-CLM-010", codes(report))
        self.assertNotIn("DSX-CLM-011", codes(report))

    def test_exemption_causal_typed_claim_with_increase_noun_stays_exempt(self):
        """Exemption 1 (D-06): a claim 'associated with an increase in
        revenue' typed 'causal' must not fire a NEW DSX-CLM-011 — the
        existing ctype=='causal' early return (claims.py:111-112) stays
        untouched by the widening."""
        report = claims.check(_claims_spec("associated with an increase in revenue", "causal"))
        self.assertNotIn("DSX-CLM-011", codes(report))

    def test_exemption_interpretation_field_not_scanned(self):
        """Exemption 2 (D-06): the string 'the activation increase' placed
        in results.tests[].interpretation must not produce a causal-verb
        finding — no causal-verb scanner reads that field, and the widening
        must not newly reach into it."""
        spec = {
            "claims": [{"text": "the model performs as expected", "type": "descriptive", "evidence": "n/a"}],
            "design": {},
            "results": {
                "tests": [
                    {"name": "t1", "interpretation": "the activation increase was notable"}
                ]
            },
        }
        report = claims.check(spec)
        self.assertNotIn("DSX-CLM-010", codes(report))
        self.assertNotIn("DSX-CLM-011", codes(report))


if __name__ == "__main__":
    unittest.main()
