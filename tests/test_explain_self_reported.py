"""11.2-07: `dsx explain`'s self-reported (taken-on-trust) section.

D-13: the decision trail today shows computed choices; it does not disclose
the trust boundary -- which inputs the gate accepted as declared rather than
computed. This module pins the contract that a separately-labelled section,
positioned AFTER the decision records, discloses every value the gate
compares but never computes: ``validity_frame.*``, ``inference.*``,
``analysis.test``, ``declared_at`` (nested under ``inference``).

``frame_digest`` is COMPUTED (D-16) and must never appear in that section --
labelling a computed value "taken on trust" is the exact honesty inversion
this project exists to prevent (T-11.2-11). ``escalate`` (``decisions.py:83``)
stays unrendered, unchanged from before this plan.

``cmd_explain`` must keep returning 0 by construction (D-04) on every path,
including when the spec cannot be loaded at all.

Mirrors the ``TestDecisionTrailCLI`` idiom in ``tests/test_dsx.py``: copy
``examples/good-ANALYSIS-SPEC.yaml`` into a ``tempfile.TemporaryDirectory()``,
drive ``gate`` then ``explain`` through ``--phase-dir``, so nothing writes
into ``examples/``.
"""

from __future__ import annotations

import io
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from dsx import cli


class TestExplainSelfReportedSection(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def _run(self, argv: "list[str]") -> "tuple[int, str, str]":
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = cli.main(argv)
        return code, out.getvalue(), err.getvalue()

    def _gated_spec(self, tmp: str) -> Path:
        spec_path = Path(tmp) / "ANALYSIS-SPEC.yaml"
        shutil.copy(self.ROOT / "examples" / "good-ANALYSIS-SPEC.yaml", spec_path)
        return spec_path

    def _explain_after_gate(self, tmp: str) -> "tuple[int, str, str]":
        spec_path = self._gated_spec(tmp)
        self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
        return self._run(["explain", "--spec", str(spec_path), "--phase-dir", tmp])

    def _self_reported_section(self, out: str) -> str:
        """Locate the labelled section and return everything from its start
        onward. Fails loudly (not a KeyError) if the label is absent, which
        is the expected RED-phase outcome before Task 2 lands."""
        lowered = out.lower()
        if "self-reported" not in lowered:
            self.fail("no 'self-reported' section found in `dsx explain` output")
        return out[lowered.index("self-reported"):]

    # ── section presence, labelling, and position ──────────────────────────

    def test_self_reported_section_is_labelled_and_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._explain_after_gate(tmp)
            self.assertEqual(code, 0)
            lowered = out.lower()
            self.assertIn("self-reported", lowered)
            self.assertIn("taken on trust", lowered)
            self.assertIn("not verified by dsx", lowered)

    def test_self_reported_section_comes_after_the_decision_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._explain_after_gate(tmp)
            self.assertEqual(code, 0)
            section = self._self_reported_section(out)
            section_at = len(out) - len(section)
            # DEC-001 is the first decision record id the gate writes (D-16).
            first_decision_at = out.index("DEC-001")
            self.assertLess(
                first_decision_at, section_at,
                "self-reported section must render after the decision trail",
            )

    # ── declared trust-boundary fields are listed, tied to the exact
    #    "dotted.path: value" rendering so a pre-existing citation mentioning
    #    the same bare word (e.g. "clustered" appears in DEC-007's citation)
    #    cannot produce a false RED->GREEN transition. ──────────────────────

    def test_self_reported_section_lists_declared_validity_frame_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._explain_after_gate(tmp)
            self.assertEqual(code, 0)
            section = self._self_reported_section(out)
            self.assertIn("validity_frame.dependence.structure: clustered", section)
            self.assertIn(
                "validity_frame.estimand.quantity: difference in 7-day activation rate",
                section,
            )

    def test_self_reported_section_lists_declared_inference_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._explain_after_gate(tmp)
            self.assertEqual(code, 0)
            section = self._self_reported_section(out)
            self.assertIn("inference.declared_at: pre_data", section)
            self.assertIn("inference.primary_procedure: two_proportion_z", section)

    def test_self_reported_section_lists_analysis_test_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._explain_after_gate(tmp)
            self.assertEqual(code, 0)
            section = self._self_reported_section(out)
            self.assertIn("analysis.test: two_proportion_z", section)
            # The rest of the `analysis:` block is not part of the declared
            # trust-boundary set (only `test` is compared-but-never-computed).
            self.assertNotIn("outcome_type", section)
            self.assertNotIn("n_per_group", section)

    def test_self_reported_section_names_declared_at_field(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._explain_after_gate(tmp)
            self.assertEqual(code, 0)
            section = self._self_reported_section(out)
            self.assertIn("declared_at", section)

    # ── frame_digest stays computed, never duplicated into self-reported ───

    def test_frame_digest_value_is_in_header_but_not_in_self_reported_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            self._run(["gate", "plan", "--spec", str(spec_path), "--phase-dir", tmp])
            trail = Path(tmp) / "DECISIONS.jsonl"
            import json

            header = json.loads(trail.read_text(encoding="utf-8").splitlines()[0])
            digest = header["frame_digest"]
            self.assertTrue(digest, "fixture invocation must carry a real frame_digest")

            code, out, _ = self._run(
                ["explain", "--spec", str(spec_path), "--phase-dir", tmp]
            )
            self.assertEqual(code, 0)
            self.assertIn(f"frame_digest={digest}", out)  # still in the computed header

            section = self._self_reported_section(out)
            self.assertNotIn(digest, section)

    # ── escalate stays unrendered (unchanged) ───────────────────────────────

    def test_escalate_is_not_rendered_anywhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, out, _ = self._explain_after_gate(tmp)
            self.assertEqual(code, 0)
            self.assertNotIn("escalate", out.lower())

    # ── returns 0 by construction on every path ─────────────────────────────

    def test_returns_zero_on_happy_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            code, _, _ = self._explain_after_gate(tmp)
            self.assertEqual(code, 0)

    def test_returns_zero_when_spec_cannot_be_loaded(self):
        code, out, err = self._run(["explain", "--spec", "/nonexistent/spec.yaml"])
        self.assertEqual(code, 0)
        self.assertIn("no decision trail", (out + err).lower())

    def test_returns_zero_when_no_trail_has_been_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = self._gated_spec(tmp)
            code, out, _ = self._run(["explain", "--spec", str(spec_path)])
            self.assertEqual(code, 0)
            self.assertIn("no decision trail", out.lower())
            # No self-reported section without a trail to explain.
            self.assertNotIn("self-reported", out.lower())


if __name__ == "__main__":
    unittest.main()
