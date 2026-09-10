"""D-13 measurement driver for the frozen D-29-02 case (Phase 29, S5-3).

Runs the four/five-point gate protocol (validate + plan/execute/verify/ship)
against the DEFECT spike (segment D opposing) and against the SWAP counterfactual
(segment D flipped to positive so nothing opposes), from a FRESH
tempfile.TemporaryDirectory() per gate point — mirroring
tests/test_known_bad_corpus.py::_gate_findings exactly (fresh --phase-dir, the
entrypoint seeded into it, a plan-time decision header seeded for verify/ship).

Mints NOTHING. Reads the real gate via dsx.cli.main. Records every finding at
each point verbatim. Never writes a DECISIONS.jsonl under the repo root or the
spike directory.

Run:
  C:/Users/Benutzer1/AppData/Local/Programs/Python/Python312/python.exe \
    .planning/phases/29-evidence-case-subgroup-harm-prescriptive/spike/subgroup-harm-without-disposition-MEASURE.py
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

import yaml  # noqa: E402

from _trail_seed import seed_plan_header  # noqa: E402
from dsx import cli  # noqa: E402
from dsx.loader import load  # noqa: E402

SPIKE_DIR = Path(__file__).resolve().parent
DEFECT_SPEC = SPIKE_DIR / "subgroup-harm-without-disposition-ANALYSIS-SPEC.yaml"
ENTRYPOINT_NAME = "subgroup-harm-without-disposition-entrypoint.py"
GATE_POINTS = ("plan", "execute", "verify", "ship")


def _seed_entrypoint(tmp: Path) -> None:
    """Copy the spike entrypoint into the fresh phase dir under its declared
    relative name, exactly as _gate_findings does via _seed_entrypoint."""
    source = SPIKE_DIR / ENTRYPOINT_NAME
    dest = Path(tmp) / ENTRYPOINT_NAME
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, dest)


def _run(argv: list[str]) -> tuple[int, str]:
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = cli.main(argv)
    raw = err.getvalue() or out.getvalue()
    return code, raw


def validate(spec_path: Path) -> tuple[int, list[dict]]:
    code, raw = _run(["validate", "--spec", str(spec_path), "--json"])
    try:
        report = json.loads(raw)
        findings = report.get("findings", [])
    except json.JSONDecodeError:
        findings = []
    return code, findings


def gate(spec_path: Path, point: str) -> tuple[int, list[dict]]:
    with tempfile.TemporaryDirectory() as tmp:
        _seed_entrypoint(Path(tmp))
        if point in ("verify", "ship"):
            seed_plan_header(tmp, spec_path)
        argv = ["gate", point, "--spec", str(spec_path), "--phase-dir", tmp, "--json"]
        code, raw = _run(argv)
        try:
            report = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise AssertionError(
                f"dsx gate {point} did not emit parseable JSON (exit {code}): {raw!r}"
            ) from exc
    return code, report["findings"]


def _sev(findings: list[dict], sev: str) -> list[str]:
    return sorted(f["code"] for f in findings if f.get("severity") == sev)


def measure(label: str, spec_path: Path) -> dict:
    rows = {}
    vc, vf = validate(spec_path)
    rows["validate"] = (vc, _sev(vf, "CRITICAL"), _sev(vf, "HIGH"))
    for point in GATE_POINTS:
        code, findings = gate(spec_path, point)
        rows[point] = (code, _sev(findings, "CRITICAL"), _sev(findings, "HIGH"))
    print(f"\n=== {label} ({spec_path.name}) ===")
    print(f"{'point':<10} {'exit':<5} CRITICAL / HIGH")
    for point, (code, crit, high) in rows.items():
        print(f"{point:<10} {code:<5} CRITICAL={crit}  HIGH={high}")
    return rows


def build_swap(defect_spec_path: Path, out_path: Path) -> None:
    """Swap counterfactual, applied BY LITERAL CODE: flip segment D's effect from
    -0.06 (opposing) to +0.06 (aligned) so NOTHING opposes the positive overall.
    overall_effect stays declared at +0.032 (minimal perturbation isolates the
    opposition of D, nothing else)."""
    spec = load(str(defect_spec_path))
    for seg in spec["results"]["segments"]:
        if seg["name"] == "D":
            assert seg["effect"] == -0.06, f"unexpected D effect {seg['effect']!r}"
            seg["effect"] = 0.06
    out_path.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")


def _sign(v: float) -> int:
    return (v > 0) - (v < 0)


def met_seam_check(spec_path: Path) -> None:
    spec = load(str(spec_path))
    overall = spec["results"]["overall_effect"]
    effects = [(s["name"], s["effect"]) for s in spec["results"]["segments"]]
    osign = _sign(overall)
    opposing = [(n, v) for n, v in effects if _sign(v) == -osign]
    print("\n=== MET-030/031 seam (metrics.py:316,:334) ===")
    print(f"overall_effect={overall:+g} sign={osign}; effects={effects}")
    print(f"opposing={opposing} (count={len(opposing)} of {len(effects)})")
    print(f"MET-030 all-oppose  len(opposing)==len(effects): "
          f"{len(opposing)}=={len(effects)} -> {len(opposing) == len(effects)}")
    print(f"MET-031 >=half      len(opposing)>=len(effects)/2: "
          f"{len(opposing)}>={len(effects)/2} -> "
          f"{bool(opposing) and len(opposing) >= len(effects) / 2}")


def main() -> int:
    print(f"interpreter: {sys.executable}")
    met_seam_check(DEFECT_SPEC)
    defect_rows = measure("DEFECT (D opposing)", DEFECT_SPEC)

    with tempfile.TemporaryDirectory() as td:
        swap_spec = SPIKE_DIR / "_swap-ANALYSIS-SPEC.yaml"
        # Write the swap spec BESIDE the entrypoint so any parent-relative resolve
        # still finds it; delete it after measuring so the spike dir stays clean.
        try:
            build_swap(DEFECT_SPEC, swap_spec)
            met_seam_check(swap_spec)
            swap_rows = measure("SWAP (D flipped positive)", swap_spec)
        finally:
            if swap_spec.exists():
                swap_spec.unlink()

    print("\n=== SWAP-STILL-FIRES DIFF (per point: codes that TOGGLE) ===")
    for point in ("validate", *GATE_POINTS):
        d_crit, d_high = set(defect_rows[point][1]), set(defect_rows[point][2])
        s_crit, s_high = set(swap_rows[point][1]), set(swap_rows[point][2])
        stopped = (d_crit - s_crit) | (d_high - s_high)   # fired on DEFECT, gone on SWAP => CATCH
        started = (s_crit - d_crit) | (s_high - d_high)   # appeared only under SWAP
        print(f"{point:<10} stopped-under-swap(CATCH)={sorted(stopped)}  "
              f"started-under-swap={sorted(started)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
