"""S4-3 measurement driver (Phase 28, D-13 measured-first).

Runs the FROZEN D-28-01 collision fixture (a descriptive/observational churn readout
whose headline magnitude 27% vs 18% is quoted for metric C = churn, which NO
results.tests[] entry computes; the two computed tests are on OTHER metrics whose
reported effects x100 are exactly 27 and 18) through `dsx validate` and all four
`dsx gate` points from fresh temp directories, exactly as the corpus harness does
(tests/test_known_bad_corpus.py::_gate_findings), and records every CRITICAL/HIGH
finding verbatim. Then applies the D-28-02 swap-still-fires counterfactual BY LITERAL
CODE, in two directions:

  * HONEST swap  — the claim's collision literals 27/18 are replaced by 15/9, numbers
    that genuinely appear in a cited test (test A's CI lower bound x100 = 15; test B's
    CI lower bound x100 = 9). Numbers still reconcile, so DSX-CLM-033 stays silent.
    Any code whose firing STOPS under this swap is a CATCH of the target defect; any
    code that fires in both is incidental. (This is the Phase-27-style defect->honest
    diff.)
  * BREAK swap   — 27/18 are replaced by 33/44, numbers absent from every test, so the
    numeric collision is broken. DSX-CLM-033 FIRES. This is the corroborating probe:
    it shows DSX-CLM-033 is a pure numeric-membership gate (metric-blind), so its
    SILENCE on the collision fixture is not a verification that churn was computed —
    it is the miss.

Only the claim's percent literals ("27%","18%") and their narrative echoes are
rewritten; the tests' reported numbers (0.27, 0.18, the CI bounds) are untouched, so
each swap isolates the claim<->test numeric relationship and nothing else.

Run from the repo root with the real interpreter:
  C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe \
    .planning/phases/28-evidence-case-magnitude-no-test-computed/spike/magnitude-no-test-computed-MEASURE.py
"""

from __future__ import annotations

import io
import json
import shutil
import sys
import tempfile
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))

from _trail_seed import seed_plan_header  # noqa: E402
from dsx import cli  # noqa: E402
from dsx.loader import load  # noqa: E402

SPIKE = Path(__file__).resolve().parent
BASE_SPEC = SPIKE / "magnitude-no-test-computed-ANALYSIS-SPEC.yaml"
BASE_NARR = SPIKE / "magnitude-no-test-computed-NARRATIVE.md"
BASE_ENTRY = SPIKE / "magnitude-no-test-computed-entrypoint.py"

NARR_REL = ".planning/phases/28-evidence-case-magnitude-no-test-computed/spike/magnitude-no-test-computed-NARRATIVE.md"

GATE_POINTS = ("plan", "execute", "verify", "ship")


def _seed_entrypoint(tmp: Path, spec_path: Path) -> None:
    """Copy the spec's declared reproducibility.entrypoint into tmp (as the harness does)."""
    spec = load(str(spec_path))
    repro = spec.get("reproducibility")
    entry = repro.get("entrypoint") if isinstance(repro, dict) else None
    if not isinstance(entry, str) or not entry.strip():
        return
    source = Path(spec_path).parent / entry
    if not source.is_file():
        return
    dest = Path(tmp) / entry
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, dest)


def _run(argv: list[str]) -> tuple[int, list[dict]]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = cli.main(argv)
    raw = err.getvalue() or out.getvalue()
    try:
        report = json.loads(raw)
    except json.JSONDecodeError:
        return code, [{"code": "<NON-JSON>", "severity": "?", "raw": raw[:400]}]
    return code, report.get("findings", [])


def _blocking(findings: list[dict]) -> list[tuple[str, str]]:
    keep = []
    for f in findings:
        sev = str(f.get("severity", "")).upper()
        if sev in ("CRITICAL", "HIGH"):
            keep.append((sev, f.get("code", "?")))
    return sorted(set(keep))


def measure(spec_path: Path) -> dict:
    record: dict = {}
    vcode, vfind = _run(["validate", "--spec", str(spec_path), "--json"])
    record["validate"] = (vcode, _blocking(vfind))
    for point in GATE_POINTS:
        with tempfile.TemporaryDirectory() as tmp:
            tmpp = Path(tmp)
            _seed_entrypoint(tmpp, spec_path)
            if point in ("verify", "ship"):
                seed_plan_header(tmpp, spec_path)
            argv = ["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
            code, findings = _run(argv)
            record[point] = (code, _blocking(findings))
    return record


def make_variant(tag: str, repl: dict[str, str]) -> Path:
    """Write a swap variant: rewrite only the claim's percent literals in BOTH the
    spec and the narrative, repoint narrative.path at the swapped narrative, and copy
    the entrypoint alongside so the harness can seed it. Returns the swap spec path."""
    swap_dir = SPIKE / f"_swap_{tag}"
    swap_dir.mkdir(exist_ok=True)
    swap_spec = swap_dir / f"magnitude-{tag}-ANALYSIS-SPEC.yaml"
    swap_narr = swap_dir / f"magnitude-{tag}-NARRATIVE.md"
    swap_narr_rel = f".planning/phases/28-evidence-case-magnitude-no-test-computed/spike/_swap_{tag}/magnitude-{tag}-NARRATIVE.md"

    spec_text = BASE_SPEC.read_text(encoding="utf-8")
    narr_text = BASE_NARR.read_text(encoding="utf-8")
    for old, new in repl.items():
        spec_text = spec_text.replace(old, new)
        narr_text = narr_text.replace(old, new)
    spec_text = spec_text.replace(NARR_REL, swap_narr_rel)
    spec_text = spec_text.replace('spec_id: "magnitude-no-test-computed"', f'spec_id: "magnitude-{tag}"')

    swap_spec.write_text(spec_text, encoding="utf-8")
    swap_narr.write_text(narr_text, encoding="utf-8")
    shutil.copy(BASE_ENTRY, swap_dir / "magnitude-no-test-computed-entrypoint.py")
    return swap_spec


def fmt(record: dict) -> str:
    lines = []
    for key in ("validate",) + GATE_POINTS:
        code, blocking = record[key]
        codes = ", ".join(f"{c}({s[0]})" for s, c in blocking) or "—"
        label = key if key == "validate" else f"gate {key}"
        lines.append(f"  {label:<13} exit={code}  CRIT/HIGH: {codes}")
    return "\n".join(lines)


def diff(defect: dict, swap: dict, tag: str) -> bool:
    print(f"\n=== swap diff: {tag} (a code only in DEFECT that STOPS under swap is a CATCH) ===")
    catch = False
    for point in ("validate",) + GATE_POINTS:
        d_codes = {c for _, c in defect[point][1]}
        s_codes = {c for _, c in swap[point][1]}
        only_defect = sorted(d_codes - s_codes)
        only_swap = sorted(s_codes - d_codes)
        if only_defect:
            catch = True
            print(f"  {point}: CATCH — fires only on defect, stops under swap: {only_defect}")
        elif only_swap:
            print(f"  {point}: swap-only (starts firing under swap): {only_swap} — NOT a catch")
        else:
            print(f"  {point}: identical CRIT/HIGH set (no toggle)")
    return catch


def main() -> int:
    print("=== DEFECT (collision) fixture: churn 27% vs 18%, no test computes churn ===")
    defect = measure(BASE_SPEC)
    print(fmt(defect))

    honest = measure(make_variant("honest", {"27%": "15%", "18%": "9%"}))
    print("\n=== HONEST swap: 27->15, 18->9 (both genuinely appear in a cited test) ===")
    print(fmt(honest))

    brk = measure(make_variant("break", {"27%": "33%", "18%": "44%"}))
    print("\n=== BREAK swap: 27->33, 18->44 (absent from every test; collision broken) ===")
    print(fmt(brk))

    catch_honest = diff(defect, honest, "HONEST (defect vs genuinely-reconciling)")
    diff(defect, brk, "BREAK (defect vs collision-broken)")

    print("\n=== VERDICT ===")
    # A catch of the target defect = a code that fires on the collision fixture AND
    # stops firing when the claim's numbers are swapped for genuinely-reconciling ones.
    if catch_honest:
        print("  CAUGHT — a code flags the mislabelled magnitude on the merits.")
    else:
        print("  No code stops firing under the honest swap ⇒ nothing catches the")
        print("  churn-metric-binding defect. DSX-CLM-033 is silent on the collision")
        print("  fixture (27/18 match test A/B via the x100 bridge) and FIRES only under")
        print("  the BREAK swap (33/44 absent) ⇒ it is a pure numeric-membership gate,")
        print("  metric-blind; its silence here is the miss.")
        print("  ⇒ LIVE MISS on the magnitude-no-test-computed defect.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
