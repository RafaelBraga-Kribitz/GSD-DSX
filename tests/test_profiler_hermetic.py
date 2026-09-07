"""Hermetic profiler depth tests (Phase 25).

Reference-value, determinism, and pre-existing-key golden tests for the
additive `columns[<col>].numeric` / `columns[<col>].categorical` blocks.
Stdlib unittest only — no pytest dependency.

Run:  python.exe -m unittest tests.test_profiler_hermetic -v
"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dsx.findings import CheckError  # noqa: E402
from dsx.profiler import (  # noqa: E402
    _categorical_block,
    _extract_hour,
    _numeric_block,
    dump_profile_yaml,
    profile_csv,
    write_profile,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "profiler"
REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "templates" / "DATA-PROFILE.yaml"
SKILL = REPO / "skills" / "dsx-explore-data" / "SKILL.md"
ASSERTIONS_REF = REPO / "references" / "data-quality-assertions.md"
EXAMPLES = REPO / "examples"


def _strip_new_blocks(text: str) -> str:
    """Drop every line belonging to a `numeric:`/`categorical:` sub-map, leaving only
    pre-Phase-25 rendered lines (D-04 guard #3). CRLF-tolerant — splits on `\\r?\\n`,
    never assumes `\\n`-only line endings (this repo checks out CRLF on Windows).
    """
    lines = re.split(r"\r?\n", text)
    kept: list[str] = []
    skip_indent = None
    for line in lines:
        indent = len(line) - len(line.lstrip(" "))
        if skip_indent is not None:
            if line.strip() != "" and indent > skip_indent:
                continue
            skip_indent = None
        if line.strip() in ("numeric:", "categorical:"):
            skip_indent = indent
            continue
        kept.append(line)
    return "\n".join(kept)


class TestNumericBlock(unittest.TestCase):
    def test_1_to_10_reference_values(self):
        block = _numeric_block([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.assertEqual(block["min"], 1)
        self.assertEqual(block["q1"], 3.25)
        self.assertEqual(block["median"], 5.5)
        self.assertEqual(block["q3"], 7.75)
        self.assertEqual(block["max"], 10)
        self.assertEqual(block["mean"], 5.5)
        self.assertEqual(block["sd"], 3.0276503540974917)
        self.assertEqual(block["n_zero"], 0)
        self.assertEqual(block["n_negative"], 0)
        self.assertEqual(block["n"], 10)

    def test_median_matches_statistics_median(self):
        import statistics

        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        block = _numeric_block(values)
        self.assertEqual(block["median"], statistics.median(values))

    def test_zeros_and_negatives(self):
        block = _numeric_block([-2.0, -0.0, 0.0, 0.0, 5])
        self.assertEqual(block["n_negative"], 1)
        self.assertEqual(block["n_zero"], 3)
        self.assertEqual(block["min"], -2.0)
        self.assertEqual(block["max"], 5)
        self.assertEqual(block["n"], 5)

    def test_empty(self):
        block = _numeric_block([])
        for key in ("min", "q1", "median", "q3", "max", "mean", "sd"):
            self.assertIsNone(block[key], key)
        self.assertEqual(block["n_zero"], 0)
        self.assertEqual(block["n_negative"], 0)
        self.assertEqual(block["n"], 0)

    def test_single_value(self):
        block = _numeric_block([7])
        for key in ("min", "max", "q1", "median", "q3", "mean"):
            self.assertEqual(block[key], 7, key)
        self.assertIsNone(block["sd"])
        self.assertEqual(block["n_zero"], 0)
        self.assertEqual(block["n_negative"], 0)
        self.assertEqual(block["n"], 1)

    def test_through_profile_csv_numeric_1_10(self):
        profile = profile_csv(FIXTURES / "numeric_1_10.csv")
        numeric = profile["columns"]["value"]["numeric"]
        self.assertEqual(numeric["min"], 1)
        self.assertEqual(numeric["q1"], 3.25)
        self.assertEqual(numeric["median"], 5.5)
        self.assertEqual(numeric["q3"], 7.75)
        self.assertEqual(numeric["max"], 10)
        self.assertEqual(numeric["mean"], 5.5)
        self.assertEqual(numeric["sd"], 3.0276503540974917)
        self.assertEqual(numeric["n_zero"], 0)
        self.assertEqual(numeric["n_negative"], 0)
        self.assertEqual(numeric["n"], 10)
        # D-01 append order: numeric is the LAST key in columns.value, after dtype.
        keys = list(profile["columns"]["value"].keys())
        self.assertEqual(keys, ["null_rate", "n_unique", "dtype", "numeric"])

    def test_numeric_key_absent_for_string_dtype(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "strings.csv"
            csv_path.write_text("level\nA\nB\nA\n", encoding="utf-8")
            profile = profile_csv(csv_path)
            self.assertNotIn("numeric", profile["columns"]["level"])


class TestCategoricalBlock(unittest.TestCase):
    def test_abcde_reference_values(self):
        profile = profile_csv(FIXTURES / "categorical_abcde.csv")
        cat = profile["columns"]["level"]["categorical"]
        self.assertEqual(cat["share_top1"], 0.5)
        self.assertEqual(cat["share_top10"], 1.0)
        self.assertEqual(cat["rare_share"], 0.05)
        self.assertEqual(cat["n_singleton"], 1)
        # D-01 append order: categorical is the LAST key in columns.level, after dtype.
        keys = list(profile["columns"]["level"].keys())
        self.assertEqual(keys, ["null_rate", "n_unique", "dtype", "categorical"])

    def test_percent_arm_boundary(self):
        # N=20000, one level ("rare") has 15 rows: 15 >= 10 but 15/20000 = 0.00075 < 0.001,
        # so it must still be counted as rare (the OR is on count<10 OR share<0.001).
        profile = profile_csv(FIXTURES / "categorical_percent_arm.csv")
        cat = profile["columns"]["level"]["categorical"]
        self.assertAlmostEqual(cat["rare_share"], 15 / 20000)

    def test_top10_truncates_at_ten_with_boundary_tie(self):
        # Levels a..i carry counts 15..7 (sum=99); "m" and "n" both have count 5.
        # share_top10 sums the ten largest counts: the nine a..i plus exactly ONE of the
        # two tied count-5 levels -> (99 + 5) / 109. This pins top-10 *truncation* at a
        # boundary tie, NOT the tie-break rule: because the two boundary levels tie at
        # count 5, the sum is identical whichever is chosen, so no _categorical_block
        # aggregate can observe the count-desc/string-asc order. That order is
        # deterministic insurance over an intermediate ranking that is never emitted
        # (review M-01: the frozen tie-break is unobservable through the outputs).
        profile = profile_csv(FIXTURES / "categorical_top10_tie.csv")
        cat = profile["columns"]["level"]["categorical"]
        self.assertAlmostEqual(cat["share_top10"], (99 + 5) / 109)

    def test_empty_counter(self):
        block = _categorical_block(Counter())
        self.assertIsNone(block["share_top1"])
        self.assertIsNone(block["share_top10"])
        self.assertIsNone(block["rare_share"])
        self.assertEqual(block["n_singleton"], 0)

    def test_categorical_key_absent_for_numeric_dtype(self):
        profile = profile_csv(FIXTURES / "numeric_1_10.csv")
        self.assertNotIn("categorical", profile["columns"]["value"])


class TestProfilerDeterminism(unittest.TestCase):
    def test_two_runs_are_byte_identical(self):
        profile_a = profile_csv(FIXTURES / "numeric_1_10.csv")
        profile_b = profile_csv(FIXTURES / "numeric_1_10.csv")
        with tempfile.TemporaryDirectory() as tmp:
            out_a = write_profile(profile_a, Path(tmp) / "a.yaml")
            out_b = write_profile(profile_b, Path(tmp) / "b.yaml")
            self.assertEqual(out_a.read_bytes(), out_b.read_bytes())

    def test_pre_existing_keys_match_golden(self):
        profile = profile_csv(FIXTURES / "numeric_1_10.csv")
        rendered = dump_profile_yaml(profile)
        filtered = _strip_new_blocks(rendered)
        # The golden is the raw text/byte diff of rendered YAML (never a parsed-as-dict
        # compare — see 25-RESEARCH.md Pitfall 3), split CRLF-tolerantly.
        golden_text = (FIXTURES / "golden_preexisting_numeric_1_10.yaml").read_text(
            encoding="utf-8"
        )
        golden_lines = re.split(r"\r?\n", golden_text)
        filtered_lines = re.split(r"\r?\n", filtered)
        self.assertEqual(filtered_lines, golden_lines)
        # The golden must contain no additive-block lines at all.
        self.assertNotIn("numeric:", golden_text)
        self.assertNotIn("categorical:", golden_text)


class TestTimeBlock(unittest.TestCase):
    """D-02 time-block extension: share_at_hour_00, rows_per_day, ISO-week edge ratios.

    Every value is a pure function of the CSV bytes (hour retained via a SEPARATE
    accumulator; day-grain volume; ISO-week grain edge ratios). The frozen
    time.min/max/max_gap_days keys must stay present and correct alongside the
    additive keys, in append order.
    """

    def _time(self, fixture):
        return profile_csv(FIXTURES / fixture, time_column="ts")["time"]

    def test_extract_hour_helper(self):
        self.assertEqual(_extract_hour("2024-01-01T00:00:00"), 0)
        self.assertEqual(_extract_hour("2024-01-01T13:00"), 13)
        self.assertEqual(_extract_hour("2024-01-01 09:30:00"), 9)
        self.assertIsNone(_extract_hour("2024-01-01"))  # date-only: no time token
        self.assertIsNone(_extract_hour("not-a-date"))

    def test_share_at_hour_00_all_midnight(self):
        self.assertEqual(self._time("time_hour_all_midnight.csv")["share_at_hour_00"], 1.0)

    def test_share_at_hour_00_half(self):
        self.assertEqual(self._time("time_hour_half.csv")["share_at_hour_00"], 0.5)

    def test_share_at_hour_00_date_only_is_null(self):
        self.assertIsNone(self._time("time_hour_date_only.csv")["share_at_hour_00"])

    def test_share_at_hour_00_mixed(self):
        self.assertEqual(
            self._time("time_hour_mixed.csv")["share_at_hour_00"],
            0.3333333333333333,
        )

    def test_rows_per_day(self):
        rpd = self._time("time_rows_per_day.csv")["rows_per_day"]
        self.assertEqual(rpd["min"], 1)
        self.assertEqual(rpd["median"], 5)
        self.assertEqual(rpd["max"], 9)

    def test_edge_period_ratios(self):
        t = self._time("time_edge_ratio.csv")
        self.assertEqual(t["first_period_ratio"], 0.2)
        self.assertEqual(t["last_period_ratio"], 0.1)

    def test_edge_period_ratios_short_are_null(self):
        t = self._time("time_edge_ratio_short.csv")
        self.assertIsNone(t["first_period_ratio"])
        self.assertIsNone(t["last_period_ratio"])

    def test_frozen_time_keys_present_and_correct(self):
        # The pre-existing time.* keys must survive the additive change untouched.
        t = self._time("time_edge_ratio.csv")
        self.assertEqual(t["column"], "ts")
        self.assertEqual(t["min"], "2024-01-01")
        self.assertEqual(t["max"], "2024-02-05")
        self.assertEqual(t["max_gap_days"], 7)

    def test_time_block_append_order(self):
        # New keys render AFTER max_gap_days inside the time: block (D-01 append order).
        keys = list(profile_csv(FIXTURES / "time_edge_ratio.csv", time_column="ts")["time"].keys())
        self.assertEqual(
            keys,
            [
                "column", "min", "max", "max_gap_days",
                "rows_per_day", "first_period_ratio", "last_period_ratio",
                "share_at_hour_00",
            ],
        )

    def test_new_time_keys_absent_when_no_time_column(self):
        # No --time supplied: the time block stays the frozen 4-key shape (25-01 golden).
        keys = list(profile_csv(FIXTURES / "numeric_1_10.csv")["time"].keys())
        self.assertEqual(keys, ["column", "min", "max", "max_gap_days"])

    def test_new_time_keys_deterministic_across_shuffle(self):
        # isocalendar bucketing + day-grain counts are order-independent.
        import random

        rows = (FIXTURES / "time_edge_ratio.csv").read_text(encoding="utf-8").splitlines()
        header, body = rows[0], rows[1:]
        shuffled = body[:]
        random.Random(1234).shuffle(shuffled)
        with tempfile.TemporaryDirectory() as tmp:
            shuf = Path(tmp) / "shuffled.csv"
            shuf.write_text("\n".join([header] + shuffled) + "\n", encoding="utf-8")
            a = profile_csv(FIXTURES / "time_edge_ratio.csv", time_column="ts")["time"]
            b = profile_csv(shuf, time_column="ts")["time"]
        for key in ("rows_per_day", "first_period_ratio", "last_period_ratio", "share_at_hour_00"):
            self.assertEqual(a[key], b[key], key)


class TestUnitBlock(unittest.TestCase):
    """D-02 top-level `unit` block: rows_per_unit {p50,p95,max}, largest_unit_share.

    Type-7 (inclusive) quantiles over per-unit row counts; largest_unit_share uses an
    explicit (count desc, unit-string asc) tie-break. The block is omitted entirely when
    no unit column is declared (D-01), never emitted as null.
    """

    def test_reference_values(self):
        profile = profile_csv(FIXTURES / "unit_counts.csv", unit="unit_id")
        block = profile["unit"]
        rpu = block["rows_per_unit"]
        self.assertEqual(rpu["p50"], 3)
        self.assertEqual(rpu["p95"], 80.8)  # pinned from a real 3.12.10 run
        self.assertEqual(rpu["max"], 100)
        self.assertEqual(block["largest_unit_share"], 0.9090909090909091)  # 100/110

    def test_unit_block_omitted_when_absent(self):
        profile = profile_csv(FIXTURES / "unit_counts.csv")
        self.assertNotIn("unit", profile)

    def test_unit_block_appends_after_sentinels_found(self):
        profile = profile_csv(FIXTURES / "unit_counts.csv", unit="unit_id")
        keys = list(profile.keys())
        self.assertEqual(keys[-1], "unit")
        self.assertEqual(keys[keys.index("unit") - 1], "sentinels_found")

    def test_single_distinct_unit(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "one_unit.csv"
            csv_path.write_text("unit_id\nu1\nu1\nu1\n", encoding="utf-8")
            block = profile_csv(csv_path, unit="unit_id")["unit"]
            self.assertIsNone(block["rows_per_unit"]["p50"])
            self.assertIsNone(block["rows_per_unit"]["p95"])
            self.assertEqual(block["rows_per_unit"]["max"], 3)

    def test_unknown_unit_column_raises(self):
        with self.assertRaises(CheckError):
            profile_csv(FIXTURES / "unit_counts.csv", unit="does_not_exist")

    def test_deterministic_across_shuffle(self):
        import random

        rows = (FIXTURES / "unit_counts.csv").read_text(encoding="utf-8").splitlines()
        header, body = rows[0], rows[1:]
        shuffled = body[:]
        random.Random(99).shuffle(shuffled)
        with tempfile.TemporaryDirectory() as tmp:
            shuf = Path(tmp) / "shuffled.csv"
            shuf.write_text("\n".join([header] + shuffled) + "\n", encoding="utf-8")
            a = profile_csv(FIXTURES / "unit_counts.csv", unit="unit_id")["unit"]
            b = profile_csv(shuf, unit="unit_id")["unit"]
        self.assertEqual(a, b)


class TestTargetBlock(unittest.TestCase):
    """D-02 top-level `target` block: overall, weekly {week,n,base_rate} table,
    weekly_range [min,max], verdict (drifting | stable | null).

    Week bucket = (iso_year, iso_week) from date.isocalendar() on the --time column
    (deterministic, locale-free). overall = mean of the binary target over
    non-null-target rows. verdict = 'drifting' iff any week base_rate < 0.8*overall OR
    > 1.2*overall (strict, multiplicative), else 'stable'; null when <2 populated weeks.
    The block is omitted entirely (key absent) when no target column is declared (D-01);
    --target hard-requires --time; the binary check is closed against {"0","1"} — yes/no/
    true/false are NOT accepted (25-RESEARCH.md Pitfall 4).
    """

    def _target(self, fixture):
        return profile_csv(FIXTURES / fixture, time_column="ts", target="y")["target"]

    def test_drifting_reference_values(self):
        block = self._target("target_drifting.csv")
        self.assertEqual(block["overall"], 0.5)
        self.assertEqual(block["weekly_range"], [0.25, 0.75])
        self.assertEqual(block["verdict"], "drifting")
        self.assertEqual(len(block["weekly"]), 3)
        for wk in block["weekly"]:
            self.assertIn("week", wk)
            self.assertIn("n", wk)
            self.assertIn("base_rate", wk)
            self.assertEqual(wk["n"], 4)
        rates = [wk["base_rate"] for wk in block["weekly"]]
        self.assertEqual(rates, [0.5, 0.25, 0.75])

    def test_stable_reference_values(self):
        block = self._target("target_stable.csv")
        self.assertEqual(block["overall"], 0.5)
        self.assertEqual(block["weekly_range"], [0.5, 0.5])
        self.assertEqual(block["verdict"], "stable")

    def test_boundary_is_stable(self):
        # overall=0.5 → thresholds 0.4 / 0.6; week rates {0.4,0.6,0.5} sit exactly on the
        # ±20% edge, which is strict/exclusive, so the verdict must read 'stable'.
        block = self._target("target_boundary.csv")
        self.assertEqual(block["overall"], 0.5)
        self.assertEqual(block["weekly_range"], [0.4, 0.6])
        self.assertEqual(block["verdict"], "stable")

    def test_single_week_verdict_null(self):
        block = self._target("target_single_week.csv")
        self.assertIsNone(block["verdict"])
        self.assertEqual(len(block["weekly"]), 1)

    def test_non_binary_target_raises_listing_value(self):
        with self.assertRaises(CheckError) as ctx:
            profile_csv(FIXTURES / "target_non_binary.csv", time_column="ts", target="y")
        self.assertIn("2", str(ctx.exception))

    def test_yes_no_target_raises_listing_values(self):
        with self.assertRaises(CheckError) as ctx:
            profile_csv(FIXTURES / "target_yes_no.csv", time_column="ts", target="y")
        msg = str(ctx.exception)
        self.assertIn("no", msg)
        self.assertIn("yes", msg)

    def test_target_requires_time(self):
        with self.assertRaises(CheckError):
            profile_csv(FIXTURES / "target_drifting.csv", target="y")

    def test_unknown_target_column_raises(self):
        with self.assertRaises(CheckError):
            profile_csv(FIXTURES / "target_drifting.csv", time_column="ts", target="nope")

    def test_target_block_omitted_when_absent(self):
        profile = profile_csv(FIXTURES / "target_drifting.csv", time_column="ts")
        self.assertNotIn("target", profile)

    def test_target_block_appends_last(self):
        profile = profile_csv(FIXTURES / "target_drifting.csv", time_column="ts", target="y")
        keys = list(profile.keys())
        self.assertEqual(keys[-1], "target")
        # No unit here, so target appends immediately after sentinels_found.
        self.assertEqual(keys[keys.index("target") - 1], "sentinels_found")

    def test_target_block_keys_and_order(self):
        block = self._target("target_drifting.csv")
        self.assertEqual(
            list(block.keys()), ["overall", "weekly", "weekly_range", "verdict"]
        )

    def test_deterministic_across_shuffle(self):
        import random

        rows = (FIXTURES / "target_drifting.csv").read_text(encoding="utf-8").splitlines()
        header, body = rows[0], rows[1:]
        shuffled = body[:]
        random.Random(7).shuffle(shuffled)
        with tempfile.TemporaryDirectory() as tmp:
            shuf = Path(tmp) / "shuffled.csv"
            shuf.write_text("\n".join([header] + shuffled) + "\n", encoding="utf-8")
            a = profile_csv(FIXTURES / "target_drifting.csv", time_column="ts", target="y")["target"]
            b = profile_csv(shuf, time_column="ts", target="y")["target"]
        self.assertEqual(a, b)

    def test_empty_flag_values_treated_as_absent(self):
        # Review LOW #3: an explicit empty flag ("") is coerced to None, so no degenerate
        # all-null block is emitted and `--target ""` does NOT trip the requires-time
        # guard — it behaves exactly as if the flag were omitted. Before the coercion fix,
        # `target=""` with no --time emitted a null target block instead (this fails then).
        no_time_target = profile_csv(FIXTURES / "target_drifting.csv", target="")
        self.assertNotIn("target", no_time_target)
        with_time_target = profile_csv(
            FIXTURES / "target_drifting.csv", time_column="ts", target=""
        )
        self.assertNotIn("target", with_time_target)
        empty_unit = profile_csv(FIXTURES / "target_drifting.csv", unit="")
        self.assertNotIn("unit", empty_unit)


class TestDocRipple(unittest.TestCase):
    """Doc ripple (Task 1, REQ-P25-03): the three doc surfaces point at the profiler for
    the trust core, and the named exclusions stay agent-side.

    Every assertion is substring-based, so CRLF vs LF line endings never matter (this repo
    checks out CRLF on Windows).
    """

    # Every additive Phase-25 key the profiler now produces (D-01/D-02 vocabulary).
    NEW_KEY_TOKENS = [
        "numeric",
        "categorical",
        "q1",
        "median",
        "q3",
        "mean",
        "sd",
        "n_zero",
        "n_negative",
        "share_top1",
        "share_top10",
        "rare_share",
        "n_singleton",
        "rows_per_day",
        "first_period_ratio",
        "last_period_ratio",
        "share_at_hour_00",
        "rows_per_unit",
        "largest_unit_share",
        "overall",
        "weekly_range",
        "verdict",
        "base_rate",
    ]

    def test_template_documents_every_new_key(self):
        text = TEMPLATE.read_text(encoding="utf-8")
        for token in self.NEW_KEY_TOKENS:
            self.assertIn(token, text, token)

    def test_skill_says_copied_from_the_profile(self):
        text = SKILL.read_text(encoding="utf-8")
        # The phrase must appear once per rippled step (1a/3a/4a/4b/4e/4f) — at least six.
        self.assertGreaterEqual(text.count("copied from the profile"), 6)

    def test_named_exclusions_stay_agent_side(self):
        # The profiler must NOT be asked to produce the named exclusions; the skill still
        # asks the agent to compute them. Staleness (3a) needs the wall clock and is the
        # hermetic canary that the producer never touches it.
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("staleness stays agent-computed", text)

    def test_assertions_reference_marks_keys_producer_only(self):
        text = ASSERTIONS_REF.read_text(encoding="utf-8").lower()
        self.assertIn("producer-only", text)


class TestDQGateIgnoresNewKeys(unittest.TestCase):
    """Whole-vocabulary guard (Task 2, REQ-P25-03 / T-25-07): the DQ gate reads only its six
    known keys via `.get()` on a named path, so a full set of Phase-25 additive keys sitting
    adjacent to them is passed over, never merged into the verdict.

    Proven, not assumed: run the real `dq.check` path against the good example profile with
    every new key populated versus the same profile stripped, and assert the two reports carry
    the identical finding-code set and the identical HIGH-block verdict.
    """

    # A full set of Phase-25 additive keys appended after the existing profile keys — a
    # columns.<col>.numeric + .categorical sub-map, plus top-level unit and target blocks.
    NEW_KEYS_BLOCK = """
    numeric:
      min: 0.0
      q1: 1.0
      median: 2.0
      q3: 3.0
      max: 4.0
      mean: 2.0
      sd: 1.5
      n_zero: 3
      n_negative: 0
      n: 100
    categorical:
      share_top1: 0.5
      share_top10: 1.0
      rare_share: 0.05
      n_singleton: 1
"""
    UNIT_TARGET_BLOCK = """unit:
  rows_per_unit: { p50: 3, p95: 80.8, max: 100 }
  largest_unit_share: 0.9090909090909091
target:
  overall: 0.5
  weekly:
    - { week: [2026, 23], n: 40, base_rate: 0.5 }
  weekly_range: [0.25, 0.75]
  verdict: drifting
"""

    def _codes_and_verdict(self, profile_dir: Path):
        from dsx.checks import dq
        from dsx.findings import Severity
        from dsx.loader import load

        spec = load(EXAMPLES / "good-ANALYSIS-SPEC.yaml")
        report = dq.check(spec, str(profile_dir))
        return {f.code for f in report.findings}, report.blocks(Severity.HIGH)

    def _copy_examples(self, dest: Path):
        for name in (
            "good-ANALYSIS-SPEC.yaml",
            "good-DATA-PROFILE.yaml",
        ):
            (dest / name).write_bytes((EXAMPLES / name).read_bytes())

    def test_gate_verdict_identical_with_and_without_new_keys(self):
        with tempfile.TemporaryDirectory() as tmp_stripped, tempfile.TemporaryDirectory() as tmp_full:
            stripped = Path(tmp_stripped)
            full = Path(tmp_full)
            self._copy_examples(stripped)
            self._copy_examples(full)

            # Inject the additive keys into the FULL copy's profile: a numeric/categorical
            # sub-map appended under an existing column (user_id), plus top-level unit/target
            # blocks appended after the existing keys — never interleaved.
            profile_text = (full / "good-DATA-PROFILE.yaml").read_text(encoding="utf-8")
            lines = re.split(r"\r?\n", profile_text)
            out = []
            for line in lines:
                out.append(line)
                if line.rstrip() == "  user_id:":
                    # append the numeric/categorical sub-map to this column (indent 4)
                    out.extend(self.NEW_KEYS_BLOCK.strip("\n").split("\n"))
            injected = "\n".join(out) + "\n" + self.UNIT_TARGET_BLOCK
            (full / "good-DATA-PROFILE.yaml").write_text(injected, encoding="utf-8")

            stripped_codes, stripped_block = self._codes_and_verdict(stripped)
            full_codes, full_block = self._codes_and_verdict(full)

            self.assertEqual(stripped_codes, full_codes)
            self.assertEqual(stripped_block, full_block)
            # The good profile passes (no HIGH block) either way — the new keys are inert.
            self.assertFalse(full_block, full_codes)


class TestExampleProfilesByteInvariant(unittest.TestCase):
    """D-04 guard #4 (Task 2, REQ-P25-02): the committed example profiles are byte-invariant.

    The sha256 is over RAW bytes (CRLF included, this repo checks out CRLF on Windows), pinned
    from the current committed files — so any future edit to either file fails the suite.
    """

    EXPECTED = {
        "good-DATA-PROFILE.yaml": (
            "3a2d220088a217f60523391f177d66561f2b7e051413855a60e639d30d3275d1"
        ),
        "bad-DATA-PROFILE.yaml": (
            "723d2ba49c31190d33674c8015963dcd02edfb19b7bd0631c963d85b74c6c39a"
        ),
    }

    def test_example_profiles_match_pinned_digests(self):
        import hashlib

        for name, expected in self.EXPECTED.items():
            raw = (EXAMPLES / name).read_bytes()
            actual = hashlib.sha256(raw).hexdigest()
            self.assertEqual(actual, expected, name)


if __name__ == "__main__":
    unittest.main()
