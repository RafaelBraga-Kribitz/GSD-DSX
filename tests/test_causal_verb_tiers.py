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

    # ── CR-01 (11.2 code review, §4 persona round) ────────────────────────
    # The bare "to" purpose marker used to fire on every infinitive, so
    # ordinary descriptive prose ("tends to increase", "failed to reduce")
    # wrongly blocked at DSX-CLM-011 CRITICAL. The purpose gate now stays shut
    # when "to" follows a raising/control head (_NON_PURPOSE_TO_PRECEDERS),
    # and still fires when "to" follows a noun object, a goal/achievement verb,
    # or opens the clause. These pin both directions so the fix cannot regress.

    def test_cr01_tendency_preceder_produces_no_findings(self):
        """'usage tends to increase after onboarding' (association) is a
        description, not a recommendation — the raising head 'tends' shuts the
        purpose gate, so no causal-verb finding fires."""
        report = claims.check(_claims_spec("usage tends to increase after onboarding", "association"))
        self.assertNotIn("DSX-CLM-010", codes(report))
        self.assertNotIn("DSX-CLM-011", codes(report))

    def test_cr01_failure_preceder_produces_no_findings(self):
        """'the pilot failed to reduce error rate' (descriptive) asserts the
        effect did NOT happen — 'failed to reduce' must not fire."""
        report = claims.check(_claims_spec("the pilot failed to reduce error rate", "descriptive"))
        self.assertNotIn("DSX-CLM-010", codes(report))
        self.assertNotIn("DSX-CLM-011", codes(report))

    def test_cr01_adjective_preceder_produces_no_findings(self):
        """'customers were quick to increase spend' (association): the raising
        adjective 'quick' shuts the gate — it describes propensity, not a
        recommended effect."""
        report = claims.check(_claims_spec("customers were quick to increase spend", "association"))
        self.assertNotIn("DSX-CLM-010", codes(report))
        self.assertNotIn("DSX-CLM-011", codes(report))

    def test_cr01_clause_initial_to_still_fires(self):
        """A clause-initial 'to reduce churn' (association) is a purpose
        adjunct with no governing head, so DSX-CLM-011 still fires CRITICAL."""
        report = claims.check(_claims_spec("To reduce churn, offer bundled incentives", "association"))
        clm011 = [f for f in report.findings if f.code == "DSX-CLM-011"]
        self.assertEqual(len(clm011), 1, f"got codes={codes(report)}")
        self.assertEqual(clm011[0].severity, Severity.CRITICAL)

    def test_cr01_achievement_preceder_still_fires(self):
        """'we managed to reduce churn by 10%' (association): 'managed to'
        asserts the effect occurred, so it is a genuine causal claim and must
        still fire DSX-CLM-011 — the denylist deliberately excludes achievement
        heads to avoid a false negative."""
        report = claims.check(_claims_spec("we managed to reduce churn by 10 percent", "association"))
        clm011 = [f for f in report.findings if f.code == "DSX-CLM-011"]
        self.assertEqual(len(clm011), 1, f"got codes={codes(report)}")

    # ── WR-01 (11.2 code review, §4 persona round) ────────────────────────
    # _check_causal_language now exempts prescriptive (not just causal). A
    # prescriptive claim is a recommendation and is licensed to name an effect;
    # its SUPPORT is enforced by _check_causal_support (DSX-CLM-020/021), so
    # firing DSX-CLM-011 ("retype as causal") on it double-coded one fact with a
    # strength-downgrade remedy. These pin both the fix and the preserved catch.

    def test_wr01_well_identified_prescriptive_fires_no_causal_codes(self):
        """A prescriptive claim that declares a strong identification strategy
        is good work — it must fire NEITHER DSX-CLM-011 (prescriptive is
        licensed to use causal language) NOR DSX-CLM-020/021 (its identification
        clears _check_causal_support). Before WR-01 it wrongly fired DSX-CLM-011
        CRITICAL telling it to downgrade to causal."""
        spec = {
            "claims": [{
                "text": "offer bundled incentives to reduce churn",
                "type": "prescriptive",
                "identification": "randomized_experiment",
                "evidence": "n/a",
            }],
            "design": {},
            "results": {},
        }
        report = claims.check(spec)
        self.assertNotIn("DSX-CLM-011", codes(report))
        self.assertNotIn("DSX-CLM-020", codes(report))
        self.assertNotIn("DSX-CLM-021", codes(report))

    def test_wr01_unidentified_prescriptive_still_fires_clm020_not_clm011(self):
        """An un-identified prescriptive claim still blocks — DSX-CLM-020
        CRITICAL (a recommendation with no identification) — but no longer
        double-codes it with DSX-CLM-011. This is the flagship fixture's catch,
        preserved by the correct code."""
        spec = {
            "claims": [{
                "text": "offer bundled incentives to reduce churn",
                "type": "prescriptive",
                "evidence": "n/a",
            }],
            "design": {},
            "results": {},
        }
        report = claims.check(spec)
        self.assertIn("DSX-CLM-020", codes(report))
        self.assertNotIn("DSX-CLM-011", codes(report))


if __name__ == "__main__":
    unittest.main()
