"""S3-3 measurement spike (Phase 27, D-13 measured-first).

Runs the frozen D-27-01 case (feature-origin-only leak in an innocuously-named
column) through `dsx validate` and all four `dsx gate` points from fresh temp
directories, exactly as the corpus harness does, and records every CRITICAL/HIGH
finding verbatim. Then applies the D-27-02 swap-still-fires counterfactual by
literal code: it re-measures an honest-swap variant (identical except the leaky
column `account_health_index` -> the honestly-available `avg_session_minutes`)
and diffs the finding-code sets. Any code that fires for the leaky spec but not
the swap is a CATCH; any code that fires for both is incidental to the leak.

Run from the repo root with the real interpreter:
  python .planning/phases/27-evidence-case-feature-origin-only-leak/spike/feature-origin-leak-MEASURE.py
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

from dsx import cli  # noqa: E402
from dsx.loader import load  # noqa: E402
from tests._trail_seed import seed_plan_header  # noqa: E402

SPIKE = Path(__file__).resolve().parent
LEAKY_SPEC = SPIKE / "feature-origin-leak-ANALYSIS-SPEC.yaml"
LEAKY_ENTRY = SPIKE / "feature-origin-leak-entrypoint.py"

LEAK_COL = "account_health_index"
SWAP_COL = "avg_session_minutes"

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


def make_swap() -> tuple[Path, Path]:
    """Write the honest-swap variant (leaky column -> honestly-available column)."""
    swap_dir = SPIKE / "_swap"
    swap_dir.mkdir(exist_ok=True)
    swap_spec = swap_dir / "feature-origin-leak-swap-ANALYSIS-SPEC.yaml"
    swap_entry = swap_dir / "feature-origin-leak-entrypoint.py"
    spec_text = LEAKY_SPEC.read_text(encoding="utf-8").replace(LEAK_COL, SWAP_COL)
    spec_text = spec_text.replace('spec_id: "feature-origin-leak"', 'spec_id: "feature-origin-leak-swap"')
    swap_spec.write_text(spec_text, encoding="utf-8")
    swap_entry.write_text(LEAKY_ENTRY.read_text(encoding="utf-8").replace(LEAK_COL, SWAP_COL), encoding="utf-8")
    return swap_spec, swap_entry


def fmt(record: dict) -> str:
    lines = []
    for key in ("validate",) + GATE_POINTS:
        code, blocking = record[key]
        codes = ", ".join(f"{c}({s[0]})" for s, c in [(sev, cd) for sev, cd in blocking]) or "—"
        lines.append(f"  {key:<9} exit={code}  CRIT/HIGH: {codes}")
    return "\n".join(lines)


def main() -> int:
    print("=== LEAKY spec (account_health_index) ===")
    leaky = measure(LEAKY_SPEC)
    print(fmt(leaky))

    swap_spec, _ = make_swap()
    print("\n=== HONEST-SWAP spec (avg_session_minutes) ===")
    swap = measure(swap_spec)
    print(fmt(swap))

    print("\n=== D-27-02 swap-still-fires counterfactual ===")
    catch_found = False
    for point in ("validate",) + GATE_POINTS:
        leaky_codes = {c for _, c in leaky[point][1]}
        swap_codes = {c for _, c in swap[point][1]}
        only_leaky = sorted(leaky_codes - swap_codes)
        if only_leaky:
            catch_found = True
            print(f"  {point}: CATCH — fires only on leaky spec: {only_leaky}")
        else:
            print(f"  {point}: no catch (identical finding-code set) exit_leaky={leaky[point][0]}")

    print("\n=== VERDICT ===")
    if catch_found:
        print("  CAUGHT ⇒ a check flags the feature-origin leak ⇒ NO MINT, close phase.")
    else:
        # A live miss requires: all four gate points return a pass/ship verdict
        # AFTER subtracting documented incidental corpus-gap codes. The swap diff
        # already proved every fired code is independent of the leaky column.
        print("  No code distinguishes the leaky column from an honest one at any point.")
        print("  Every CRITICAL/HIGH finding fires identically for the honest-swap spec ⇒")
        print("  it is incidental to the feature-origin leak, not a catch of it.")
        print("  ⇒ LIVE MISS on the feature-origin defect (entry condition MET, pending")
        print("    the residual-code review below).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
