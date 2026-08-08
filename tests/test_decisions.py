"""Tests for dsx.decisions — decision-record schema, crash-safe append, tolerant reader.

Run:  python3 -m unittest tests.test_decisions -v
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import dsx.decisions as d
from dsx.findings import Report, merge


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

    def test_read_all_does_not_raise_on_undecodable_tail_bytes(self):
        # 06-11 Task 1 (D-08/CR-01 regression): a completed record followed by
        # raw bytes that are not valid UTF-8 (the lead byte of a two-byte
        # sequence with no continuation byte — the exact shape the reviewer
        # and verifier reproduced against the live CLI) must not raise.
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            d.append(
                p,
                d.DecisionRecord(
                    id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x"
                ),
            )
            with p.open("ab") as fh:
                fh.write(b"caf\xc3")
            records = d.read_all(p)
            self.assertEqual([r["id"] for r in records], ["DEC-001"])

    def test_read_all_preserves_records_written_after_an_undecodable_line(self):
        # A middle line that is neither valid UTF-8 nor valid JSON must be
        # disposed of deterministically regardless of decode-error strategy,
        # while the records before and after it still survive in file order.
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            d.append(
                p,
                d.DecisionRecord(
                    id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x"
                ),
            )
            with p.open("ab") as fh:
                fh.write(b"\xff\xfe not json\n")
            d.append(
                p,
                d.DecisionRecord(
                    id="DEC-002", invocation_id="INV-0001", layer="deterministic", choice="y"
                ),
            )
            records = d.read_all(p)
            self.assertEqual([r["id"] for r in records], ["DEC-001", "DEC-002"])

    def test_read_all_returns_empty_list_when_path_is_not_a_readable_file(self):
        # A path that exists but is a directory rather than a readable file —
        # not filesystem permission bits, which behave differently on Windows
        # (06-09 Task 2's own reasoning for its unwritable-directory test).
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            p.mkdir()
            self.assertEqual(d.read_all(p), [])

    def test_next_invocation_id_unaffected_by_undecodable_bytes(self):
        # The unit-level statement of why the gate path is affected at all:
        # _write_decision_trail calls this function before it calls append.
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            d.append(
                p,
                d.InvocationHeader(
                    invocation_id="INV-0001", gate_point="plan", dsx_version="x",
                    frame_digest="y",
                ),
            )
            with p.open("ab") as fh:
                fh.write(b"caf\xc3")
            self.assertEqual(d.next_invocation_id(p), "INV-0002")

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

    # ── Task 2: invocation identity, frame digest, path resolution, report collection ──

    def test_next_invocation_id_missing_file_returns_inv_0001(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            self.assertEqual(d.next_invocation_id(p), "INV-0001")

    def test_next_invocation_id_after_two_headers_returns_inv_0003(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            d.append(
                p,
                d.InvocationHeader(
                    invocation_id="INV-0001", gate_point="plan", dsx_version="x",
                    frame_digest="y",
                ),
            )
            d.append(
                p,
                d.InvocationHeader(
                    invocation_id="INV-0002", gate_point="plan", dsx_version="x",
                    frame_digest="y",
                ),
            )
            self.assertEqual(d.next_invocation_id(p), "INV-0003")

    def test_next_invocation_id_stable_with_no_write_between_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "DECISIONS.jsonl"
            d.append(
                p,
                d.InvocationHeader(
                    invocation_id="INV-0001", gate_point="plan", dsx_version="x",
                    frame_digest="y",
                ),
            )
            first = d.next_invocation_id(p)
            second = d.next_invocation_id(p)
            self.assertEqual(first, second)

    def test_frame_digest_is_64_char_lowercase_hex(self):
        spec = {"validity_frame": {"estimand": "ate"}, "inference": {"paradigm": "frequentist"}}
        digest = d.frame_digest(spec)
        self.assertEqual(len(digest), 64)
        self.assertEqual(digest, digest.lower())
        int(digest, 16)  # raises if not hex

    def test_frame_digest_unchanged_by_edit_outside_frame_blocks(self):
        a = {"title": "a", "validity_frame": {"x": 1}, "inference": {"paradigm": "frequentist"}}
        b = {"title": "CHANGED", "validity_frame": {"x": 1}, "inference": {"paradigm": "frequentist"}}
        self.assertEqual(d.frame_digest(a), d.frame_digest(b))

    def test_frame_digest_changes_when_frame_block_value_changes(self):
        a = {"validity_frame": {"x": 1}, "inference": {"paradigm": "frequentist"}}
        b = {"validity_frame": {"x": 1}, "inference": {"paradigm": "bayesian"}}
        self.assertNotEqual(d.frame_digest(a), d.frame_digest(b))

    def test_frame_digest_unchanged_by_key_insertion_order_permutation(self):
        a = {"validity_frame": {"x": 1, "y": 2}, "inference": {"paradigm": "frequentist"}}
        b = {"validity_frame": {"y": 2, "x": 1}, "inference": {"paradigm": "frequentist"}}
        self.assertEqual(d.frame_digest(a), d.frame_digest(b))

    def test_decisions_path_ends_in_decisions_jsonl_under_root(self):
        p = d.decisions_path("/some/root")
        self.assertEqual(p.name, "DECISIONS.jsonl")
        self.assertEqual(p.parent, Path("/some/root"))

    def test_collect_from_report_flattens_in_gate_profiles_order(self):
        r1 = Report(check="spec")
        r1.context["decisions"] = [{"id": "DEC-001"}]
        r2 = Report(check="design")
        r2.context["decisions"] = [{"id": "DEC-002"}, {"id": "DEC-003"}]
        merged = merge("spec+design", [r1, r2])
        collected = d.collect_from_report(merged)
        self.assertEqual([c["id"] for c in collected], ["DEC-001", "DEC-002", "DEC-003"])

    def test_collect_from_report_empty_for_report_with_no_decisions(self):
        r1 = Report(check="spec")
        merged = merge("spec", [r1])
        self.assertEqual(d.collect_from_report(merged), [])


if __name__ == "__main__":
    unittest.main()
