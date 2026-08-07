"""Tests for dsx.decisions — decision-record schema, crash-safe append, tolerant reader.

Run:  python3 -m unittest tests.test_decisions -v
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import dsx.decisions as d


# ── Task 1: schema, crash-safe append, tolerant reader ─────────────────────


class TestDecisions(unittest.TestCase):
    def test_decision_record_to_dict_has_all_fields(self):
        rec = d.DecisionRecord(
            id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x"
        )
        out = rec.to_dict()
        for name in (
            "id", "layer", "choice", "inputs", "rule", "citation", "counterfactual",
            "alternatives_rejected", "confidence", "escalate", "invocation_id",
        ):
            self.assertIn(name, out)

    def test_decision_record_type_is_decision(self):
        rec = d.DecisionRecord(
            id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x"
        )
        self.assertEqual(rec.to_dict()["record_type"], "decision")

    def test_invocation_header_type_is_invocation(self):
        hdr = d.InvocationHeader(
            invocation_id="INV-0001", gate_point="plan", dsx_version="x", frame_digest="y"
        )
        self.assertEqual(hdr.to_dict()["record_type"], "invocation")

    def test_append_then_read_all_round_trips(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            rec = d.DecisionRecord(
                id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x",
                rule="r1", citation="c1", counterfactual="cf1",
            )
            d.append(p, rec)
            records = d.read_all(p)
            self.assertEqual(len(records), 1)
            for key, value in rec.to_dict().items():
                self.assertEqual(records[0][key], value)

    def test_three_appends_produce_three_lines_in_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            for i in range(1, 4):
                d.append(
                    p,
                    d.DecisionRecord(
                        id=f"DEC-{i:03d}", invocation_id="INV-0001",
                        layer="deterministic", choice=f"choice-{i}",
                    ),
                )
            records = d.read_all(p)
            self.assertEqual(len(records), 3)
            self.assertEqual([r["id"] for r in records], ["DEC-001", "DEC-002", "DEC-003"])

    def test_read_all_skips_truncated_tail_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            d.append(
                p,
                d.DecisionRecord(
                    id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x"
                ),
            )
            d.append(
                p,
                d.DecisionRecord(
                    id="DEC-002", invocation_id="INV-0001", layer="deterministic", choice="y"
                ),
            )
            with p.open("a", encoding="utf-8") as fh:
                fh.write('{"id": "DEC-003", "trunc')  # no trailing newline, unterminated JSON
            records = d.read_all(p)
            self.assertEqual(len(records), 2)
            self.assertEqual([r["id"] for r in records], ["DEC-001", "DEC-002"])

    def test_read_all_skips_blank_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            d.append(
                p,
                d.DecisionRecord(
                    id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x"
                ),
            )
            with p.open("a", encoding="utf-8") as fh:
                fh.write("\n")
            d.append(
                p,
                d.DecisionRecord(
                    id="DEC-002", invocation_id="INV-0001", layer="deterministic", choice="y"
                ),
            )
            records = d.read_all(p)
            self.assertEqual(len(records), 2)

    def test_read_all_missing_path_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "does-not-exist" / "DECISIONS.jsonl"
            self.assertEqual(d.read_all(p), [])

    def test_append_is_deterministic_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            p1 = Path(tmp) / "a.jsonl"
            p2 = Path(tmp) / "b.jsonl"
            rec = d.DecisionRecord(
                id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x",
                inputs=["a", "b"], rule="r", citation="c", counterfactual="cf",
                alternatives_rejected=["alt"], confidence="high", escalate=True,
            )
            d.append(p1, rec)
            d.append(p2, rec)
            self.assertEqual(p1.read_text(encoding="utf-8"), p2.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
