"""Tests for `dsx stats --paradigm` (REQ-P12-04).

A pure-reader subcommand that reports the operator's own
frequentist/Bayesian/undeclared frame split, deduplicated by distinct
``frame_digest`` (D-14), sourced from real operator ``.planning/`` decision
trails only — never from the polluted ``examples/known-bad/DECISIONS.jsonl``
fixture floor or a ``templates/`` trail (D-13). Stdlib unittest, no pytest.

Run:  python -m unittest tests.test_cli_stats -v
"""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from dsx import cli  # noqa: E402
from dsx.decisions import DecisionRecord, InvocationHeader, append  # noqa: E402


def _run(argv: "list[str]") -> int:
    """Invoke the CLI, swallow its output, return the exit code."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        return cli.main(argv)


def _capture(argv: "list[str]") -> str:
    """Invoke the CLI, return its stdout."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        cli.main(argv)
    return out.getvalue()


def _seed_trail(path: Path, entries: "list[tuple[str, str, str]]") -> None:
    """Write a DECISIONS.jsonl at ``path`` from ``(invocation_id, frame_digest,
    paradigm)`` triples, using the real ``dsx.decisions`` primitives a genuine
    ``dsx gate`` run writes with — one invocation header plus one
    ``choice="paradigm=…"`` decision record per triple, so the seed cannot
    drift from the writer it stands in for."""
    path.parent.mkdir(parents=True, exist_ok=True)
    for inv_id, digest, paradigm in entries:
        append(
            path,
            InvocationHeader(
                invocation_id=inv_id,
                gate_point="plan",
                dsx_version="test-seed",
                frame_digest=digest,
            ),
        )
        append(
            path,
            DecisionRecord(
                id="DEC-001",
                invocation_id=inv_id,
                layer="deterministic",
                choice=f"paradigm={paradigm}",
            ),
        )


class TestCmdStats(unittest.TestCase):
    def test_always_exits_zero(self):
        # Empty root: no DECISIONS.jsonl anywhere under it.
        with tempfile.TemporaryDirectory() as tmp:
            for extra in ([], ["--json"]):
                code = _run(["stats", "--paradigm", "--root", tmp] + extra)
                self.assertEqual(code, 0, f"empty-root run returned {code}")
            out = _capture(["stats", "--paradigm", "--root", tmp])
            self.assertIn(
                "no operator history",
                out.lower(),
                f"empty history not named honestly: {out!r}",
            )

        # Unreadable / half-written trail: still exits 0, never a traceback.
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "phase" / "DECISIONS.jsonl"
            bad.parent.mkdir(parents=True)
            bad.write_bytes(b"\xff\xfe not json at all {half-written")
            self.assertEqual(_run(["stats", "--paradigm", "--root", tmp]), 0)
            self.assertEqual(
                _run(["stats", "--paradigm", "--root", tmp, "--json"]), 0
            )

    def test_never_sources_the_known_bad_floor(self):
        # A root carrying the polluted fixture floors (a huge known-bad-shaped
        # Bayesian trail and a templates trail) plus one real frequentist
        # operator trail. The floors must be excluded (D-13): the reported
        # split must show zero Bayesian, sourced from the operator trail only.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_trail(
                root / "examples" / "known-bad" / "DECISIONS.jsonl",
                [(f"INV-KB-{i}", "kb-bayes-frame", "bayesian") for i in range(500)],
            )
            _seed_trail(
                root / "templates" / "DECISIONS.jsonl",
                [(f"INV-T-{i}", "tmpl-bayes-frame", "bayesian") for i in range(50)],
            )
            _seed_trail(
                root / "12-calibration" / "DECISIONS.jsonl",
                [("INV-OP-1", "op-freq-frame", "frequentist")],
            )
            out = _capture(["stats", "--paradigm", "--root", str(root), "--json"])
            data = json.loads(out)
            self.assertEqual(
                data["paradigm_split"]["bayesian"],
                0,
                "the known-bad Bayesian floor leaked into the split",
            )
            self.assertNotIn("kb-bayes-frame", out)
            self.assertNotIn("tmpl-bayes-frame", out)

    def test_root_pointed_at_the_floor_still_excludes_it(self):
        # CR-01 regression (12-REVIEW.md): D-13 is an ABSOLUTE boundary, so
        # `--root` pointed AT or INSIDE the excluded tree must still exclude it.
        # The pre-fix code computed exclusion from root-RELATIVE parts, which
        # stripped the 'examples'/'templates' component exactly here and leaked
        # the polluted floor (e.g. `--root examples/known-bad` -> 20% Bayesian).
        # The earlier guard test only ever put the floor UNDER the root, never
        # pointed the root AT it, so it passed green while the boundary leaked.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_trail(
                root / "examples" / "known-bad" / "DECISIONS.jsonl",
                [(f"INV-KB-{i}", "kb-bayes-frame", "bayesian") for i in range(20)],
            )
            _seed_trail(
                root / "templates" / "DECISIONS.jsonl",
                [(f"INV-T-{i}", "tmpl-bayes-frame", "bayesian") for i in range(5)],
            )
            for at_root in (
                root / "examples",
                root / "examples" / "known-bad",
                root / "templates",
            ):
                data = json.loads(
                    _capture(["stats", "--paradigm", "--root", str(at_root), "--json"])
                )
                self.assertEqual(
                    data["distinct_frames"],
                    0,
                    f"--root {at_root} leaked the excluded floor: {data}",
                )
                self.assertEqual(data["paradigm_split"]["bayesian"], 0)
                text = _capture(["stats", "--paradigm", "--root", str(at_root)])
                self.assertIn("no operator history", text.lower())

    def test_excluded_component_match_is_case_folded(self):
        # A fixture tree spelled with different case (Examples/TEMPLATES) must
        # still be excluded on a case-insensitive filesystem (Windows), where
        # `Examples` and `examples` name the same directory. The compare is
        # case-folded, so the floor never enters and the genuine operator trail
        # is the only source counted.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_trail(
                root / "Examples" / "known-bad" / "DECISIONS.jsonl",
                [("INV-KB-1", "kb-bayes-frame", "bayesian")],
            )
            _seed_trail(
                root / "op-phase" / "DECISIONS.jsonl",
                [("INV-OP-1", "op-freq-frame", "frequentist")],
            )
            out = _capture(["stats", "--paradigm", "--root", str(root), "--json"])
            data = json.loads(out)
            self.assertEqual(data["paradigm_split"]["bayesian"], 0)
            self.assertEqual(data["paradigm_split"]["frequentist"], 1)
            self.assertNotIn("kb-bayes-frame", out)

    def test_block_on_flag_is_rejected(self):
        # `dsx stats` always passes; it carries no --block-on, so argparse
        # must reject the flag with exit 2 (D-12/D-18 — not a gate).
        with self.assertRaises(SystemExit) as cm:
            _run(["stats", "--paradigm", "--block-on", "high"])
        self.assertEqual(cm.exception.code, 2)

    def test_dedup_is_by_distinct_frame_digest(self):
        # N distinct frequentist frames, each re-run many times (many
        # invocation records sharing one frame_digest), scattered across
        # several DECISIONS.jsonl files, plus 1 distinct Bayesian frame.
        # The split's denominator is DISTINCT frame_digests (D-14), so the
        # Bayesian share is 1/(N+1) — not the raw-record proportion.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            n = 7
            repeats = 20
            for i in range(n):
                _seed_trail(
                    root / f"phase-{i}" / "DECISIONS.jsonl",
                    [
                        (f"INV-F{i}-{j}", f"freq-frame-{i}", "frequentist")
                        for j in range(repeats)
                    ],
                )
            _seed_trail(
                root / "phase-bayes" / "DECISIONS.jsonl",
                [("INV-B-1", "bayes-frame-1", "bayesian")],
            )

            data = json.loads(
                _capture(["stats", "--paradigm", "--root", str(root), "--json"])
            )
            self.assertEqual(data["distinct_frames"], n + 1)
            self.assertEqual(data["paradigm_split"]["frequentist"], n)
            self.assertEqual(data["paradigm_split"]["bayesian"], 1)
            self.assertAlmostEqual(data["shares"]["bayesian"], 1 / (n + 1))
            # The raw invocation count is a labelled secondary diagnostic only.
            self.assertEqual(data["raw_invocation_count"], n * repeats + 1)

    def test_out_of_vocabulary_paradigm_folds_to_undeclared(self):
        # A paradigm value outside the closed vocabulary is reported in the
        # undeclared bucket, not forced into the binary split.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            _seed_trail(
                root / "p" / "DECISIONS.jsonl",
                [
                    ("INV-1", "frame-freq", "frequentist"),
                    ("INV-2", "frame-oov", "empirical-bayes"),
                ],
            )
            data = json.loads(
                _capture(["stats", "--paradigm", "--root", str(root), "--json"])
            )
            self.assertEqual(data["distinct_frames"], 2)
            self.assertEqual(data["paradigm_split"]["undeclared"], 1)
            self.assertEqual(data["paradigm_split"]["frequentist"], 1)
            self.assertEqual(data["paradigm_split"]["bayesian"], 0)


if __name__ == "__main__":
    unittest.main()
