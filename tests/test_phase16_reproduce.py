"""Nyquist validation for Phase 16 (re-run-verification-off-the-gate-path).

Phase 16 splits reproduction across a trust boundary: the `dsx-reproduce` skill
*runs* the analysis entrypoint in the agent runtime and writes REPRO-REPORT.md,
while the deterministic gate only *reads* the report's machine block and never
executes anything. These tests crystallise the structural invariants each
requirement promises into a standing regression guard, the way S1-5 and S2-5 did
for Phases 13/14 (tests/test_phase13_playbooks.py, tests/test_phase14_onboarding.py).

Coverage map (see 16-VALIDATION.md):
  REQ-P16-01  dsx-reproduce skill exists + is capability-registered (14th skill),
              re-runs reproducibility.entrypoint OFF the gate path, compares to
              results.tests, writes REPRO-REPORT.md, opts the spec in, and skips
              honestly; templates/REPRO-REPORT.md carries the machine block + status
  REQ-P16-02  the reproduce-report gate check is declaration-only stdlib (no
              pandas/scipy/entrypoint); DSX-REP-060/061 exist at HIGH
              (behaviour pinned by tests/test_reproduce_report.py, 7 tests)
  REQ-P16-03  remaining Phase-12 corpus cases carry protocol_adherence, additive
              beside catch rate / FPR (pinned by tests/test_known_bad_corpus.py)
  REQ-P16-04  no dsx/checks/ or dsx/frame/ module executes the entrypoint
              (pinned by tests/test_no_entrypoint_execution.py, 3 tests)

REQ-P16-02/03/04 own behavioural tests already; the anchors here assert the
structural facts those tests depend on so a silent regression (a deleted guard, a
downgraded severity, a data library pulled onto the check) names itself.

CRLF-safe: files are read as text with single-line substring anchors, so the
repo's CRLF checkout cannot break a match. No pandas/scipy imported (gate-path
hygiene applies to the tests too).
"""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The reproduce-report gate check must never pull a data library or an execution
# primitive onto the deterministic gate path (REQ-P16-02, D-01).
FORBIDDEN_GATE_IMPORTS = re.compile(
    r"^\s*(?:import|from)\s+"
    r"(?:pandas|scipy|numpy|csv|subprocess|runpy|os|shutil)\b",
    re.MULTILINE,
)


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8", errors="replace")


def registered_skills():
    """Return the skill names capability.json registers, shape-agnostically."""
    cap = json.loads(read("capabilities/dsx/capability.json"))

    def find(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "skills" and isinstance(value, list):
                    return value
                got = find(value)
                if got is not None:
                    return got
        elif isinstance(node, list):
            for item in node:
                got = find(item)
                if got is not None:
                    return got
        return None

    skills = find(cap) or []
    return [s.get("name") if isinstance(s, dict) else s for s in skills]


class TestPhase16Reproduce(unittest.TestCase):
    # ---- REQ-P16-01 : dsx-reproduce skill + template + registration ----
    def test_req01_skill_exists_and_capability_registered(self):
        self.assertTrue(
            (ROOT / "skills" / "dsx-reproduce" / "SKILL.md").is_file(),
            "skills/dsx-reproduce/SKILL.md missing",
        )
        names = registered_skills()
        self.assertIn(
            "dsx-reproduce", names,
            "capability.json does not register dsx-reproduce",
        )
        # It is the 14th DSX skill (13 through Phase 14 + this one, REQ-P16-01).
        dsx = [n for n in names if isinstance(n, str) and n.startswith("dsx-")]
        self.assertEqual(
            len(dsx), 14,
            f"expected 14 registered dsx-* skills, found {len(dsx)}: {sorted(dsx)}",
        )

    def test_req01_skill_reruns_entrypoint_off_gate_path_and_writes_report(self):
        s = read("skills/dsx-reproduce/SKILL.md")
        # It runs the declared entrypoint, and does so OFF the gate path.
        self.assertIn("reproducibility.entrypoint", s)
        self.assertIn("OFF the gate path", s)
        # It compares fresh numbers to the declared results.tests.
        self.assertIn("results.tests", s)
        # It writes the report the gate later reads.
        self.assertIn("REPRO-REPORT.md", s)
        # It never edits a gate module (the purity boundary the phase defends).
        self.assertIn("dsx/", s)  # referenced only in the never-edit statement
        self.assertRegex(
            s, r"never edits? any `?dsx/",
        )

    def test_req01_skill_opts_spec_in_and_skips_honestly(self):
        s = read("skills/dsx-reproduce/SKILL.md")
        # Opt-in stamp is the trigger the gate keys on (not entrypoint-presence).
        self.assertIn("reproducibility.reproduce_report", s)
        # Honest opt-out: skipped/unable with no fabricated numbers.
        self.assertIn("skipped", s)
        self.assertIn("unable", s)
        self.assertRegex(
            s, r"never write a number you did not|no fabricated numbers|never invent",
        )

    def test_req01_skill_carries_triggers_clause(self):
        # Consistency with REQ-P14-04's Triggers invariant across all DSX skills.
        s = read("skills/dsx-reproduce/SKILL.md")
        self.assertIn("Triggers:", s)

    def test_req01_template_has_machine_block_and_status_vocab(self):
        t = read("templates/REPRO-REPORT.md")
        # The gate parses the first fenced yaml block, keyed by a flat status line.
        self.assertIn("```yaml", t)
        self.assertRegex(t, r"(?m)^status:")
        # The full status vocabulary the gate + skill agree on.
        for status in ("reproduced", "mismatch", "skipped", "unable"):
            self.assertIn(status, t, f"template omits status '{status}'")

    # ---- REQ-P16-02 : declaration-only gate check, codes exist at HIGH ----
    def test_req02_repro_check_is_stdlib_only(self):
        src = read("dsx/checks/repro.py")
        self.assertIsNone(
            FORBIDDEN_GATE_IMPORTS.search(src),
            "dsx/checks/repro.py imports a data library or execution primitive — "
            "the reproduce check must stay declaration-only (REQ-P16-02, D-01)",
        )

    def test_req02_both_reproduce_codes_registered_high(self):
        cat = read("references/finding-codes.md")
        for code in ("DSX-REP-060", "DSX-REP-061"):
            # Row shape: | `CODE` | HIGH | ... |  (severity is the second cell).
            row = re.search(
                r"^\|\s*`?" + re.escape(code) + r"`?\s*\|\s*([A-Z]+)\s*\|",
                cat, re.MULTILINE,
            )
            self.assertIsNotNone(row, f"{code} not found as a catalogue row")
            self.assertEqual(
                row.group(1), "HIGH",
                f"{code} must be HIGH — verify/ship blocks only at HIGH",
            )

    # ---- REQ-P16-03 : remaining corpus cases carry protocol_adherence ----
    def test_req03_remaining_corpus_cases_carry_protocol_adherence(self):
        sidecars = sorted(
            (ROOT / "examples" / "known-bad").glob("*-ATTRIBUTION.yaml")
        )
        self.assertTrue(sidecars, "no known-bad ATTRIBUTION sidecars found")
        missing = [
            p.name for p in sidecars
            if not re.search(r"(?m)^protocol_adherence:", p.read_text(
                encoding="utf-8", errors="replace"))
        ]
        self.assertEqual(
            missing, [],
            f"corpus sidecars missing protocol_adherence: {missing}",
        )

    # ---- REQ-P16-04 : entrypoint-execution guard present ----
    def test_req04_entrypoint_execution_guard_present(self):
        self.assertTrue(
            (ROOT / "tests" / "test_no_entrypoint_execution.py").is_file(),
            "REQ-P16-04 guard tests/test_no_entrypoint_execution.py is missing",
        )


if __name__ == "__main__":
    unittest.main()
