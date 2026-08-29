"""Behavioural proof of the reproduce-report gate check (REQ-P16-02, D-02/D-04/D-11).

``dsx/checks/repro.py::_check_reproduce_report`` is the DAAF "reproduced" verdict
stolen onto the gate as a pure declaration check. This module pins its four
firing/silence properties against tmp-dir fixtures, without executing any
entrypoint and without importing any third-party package:

  * DSX-REP-060 fires at verify/ship when ``reproducibility.reproduce_report`` is
    declared but the named ``REPRO-REPORT.md`` is missing (strict-only).
  * DSX-REP-061 fires when the report is present but its declared lead-metric
    number does not overlap ``results.tests`` — even under a success-claiming
    ``status``, because the gate trusts numbers, not verdicts (D-04).
  * NEITHER fires when the field is absent (silent opt-out, D-02), when the
    numbers overlap, or when the report carries an honest ``status: skipped`` /
    ``unable`` (D-11 — the missing-interpreter case is not a gate exit 1).

CRLF discipline (repo CLAUDE.md): the check parses on ``\\r?\\n``; the reports
written here use ``\\n`` and the check tolerates either.

Run:  python -m unittest tests.test_reproduce_report -v
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from dsx.checks import repro
from dsx.loader import load

ROOT = Path(__file__).resolve().parent.parent
_GOOD_SPEC = ROOT / "examples" / "good-ANALYSIS-SPEC.yaml"


def codes(report) -> set[str]:
    """The set of finding codes in a Report (mirrors test_dsx.py's ``codes`` idiom)."""
    return {f.code for f in report.findings}


def _spec_with(reproducibility: dict) -> dict:
    """A minimal spec with a non-empty results.tests whose lead metric is
    ``activation_rate`` / effect 0.024 (matching the good fixture's lead), plus
    the given ``reproducibility`` block."""
    return {
        "results": {
            "tests": [
                {"metric": "activation_rate", "effect": 0.024, "p_value": 0.0011},
            ]
        },
        "reproducibility": reproducibility,
    }


def _write_report(directory: Path, *lines: str) -> None:
    """Write a REPRO-REPORT.md whose FIRST fenced block is a ```yaml block of the
    given flat ``key: value`` lines."""
    body = "\n".join(lines)
    fence = "`" * 3
    (directory / "REPRO-REPORT.md").write_text(
        "# Reproduce report\n\n" + fence + "yaml\n" + body + "\n" + fence + "\n",
        encoding="utf-8",
    )


class TestReproduceReport(unittest.TestCase):
    def test_060_fires_when_declared_but_report_missing(self):
        spec = _spec_with({"reproduce_report": "REPRO-REPORT.md"})
        with tempfile.TemporaryDirectory() as tmp:
            found = codes(repro.check(spec, phase_dir=tmp, strict=True))
        self.assertIn("DSX-REP-060", found, found)

    def test_060_is_strict_only(self):
        spec = _spec_with({"reproduce_report": "REPRO-REPORT.md"})
        with tempfile.TemporaryDirectory() as tmp:
            found = codes(repro.check(spec, phase_dir=tmp, strict=False))
        self.assertNotIn("DSX-REP-060", found, found)

    def test_silent_when_reproduce_report_absent(self):
        # A spec that declares an entrypoint but no reproduce_report stays silent.
        spec = _spec_with({"entrypoint": "analysis/run.py"})
        with tempfile.TemporaryDirectory() as tmp:
            found = codes(repro.check(spec, phase_dir=tmp, strict=True))
        self.assertNotIn("DSX-REP-060", found, found)
        self.assertNotIn("DSX-REP-061", found, found)

        # D-02 back-compat pin: the committed good fixture declares an entrypoint
        # but no reproduce_report, so it must emit neither code.
        good = load(_GOOD_SPEC)
        good_found = codes(
            repro.check(good, phase_dir=str(ROOT / "examples"), strict=True)
        )
        self.assertNotIn("DSX-REP-060", good_found, good_found)
        self.assertNotIn("DSX-REP-061", good_found, good_found)

    def test_061_fires_when_numbers_disagree(self):
        spec = _spec_with({"reproduce_report": "REPRO-REPORT.md"})
        with tempfile.TemporaryDirectory() as tmp:
            _write_report(Path(tmp), "status: reproduced", "activation_rate: 0.24")
            found = codes(repro.check(spec, phase_dir=tmp, strict=True))
        self.assertIn("DSX-REP-061", found, found)

    def test_silent_when_numbers_overlap(self):
        spec = _spec_with({"reproduce_report": "REPRO-REPORT.md"})
        with tempfile.TemporaryDirectory() as tmp:
            _write_report(Path(tmp), "status: reproduced", "activation_rate: 0.024")
            found = codes(repro.check(spec, phase_dir=tmp, strict=True))
        self.assertNotIn("DSX-REP-060", found, found)
        self.assertNotIn("DSX-REP-061", found, found)

    def test_061_short_circuits_on_skipped_status(self):
        # D-11: an honest missing-interpreter opt-out — no fresh numbers, no exit 1.
        spec = _spec_with({"reproduce_report": "REPRO-REPORT.md"})
        with tempfile.TemporaryDirectory() as tmp:
            _write_report(Path(tmp), "status: skipped")
            found = codes(repro.check(spec, phase_dir=tmp, strict=True))
        self.assertNotIn("DSX-REP-060", found, found)
        self.assertNotIn("DSX-REP-061", found, found)

    def test_verdict_pass_does_not_suppress_061(self):
        # D-04: the gate trusts numbers, not a verdict — a success status with a
        # disagreeing number still fails.
        spec = _spec_with({"reproduce_report": "REPRO-REPORT.md"})
        with tempfile.TemporaryDirectory() as tmp:
            _write_report(Path(tmp), "status: reproduced", "activation_rate: 0.24")
            found = codes(repro.check(spec, phase_dir=tmp, strict=True))
        self.assertIn("DSX-REP-061", found, found)


if __name__ == "__main__":
    unittest.main()
