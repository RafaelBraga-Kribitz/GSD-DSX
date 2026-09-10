"""Phase 30 (S6-3) calibration re-baseline measurement — reuses
tests/test_known_bad_corpus.py live functions.

Read-only, OFF the gate path. Prints the LIVE headline pair (miss-rate, FPR),
the stratified PRESENT/ABSENT partitions with independent denominators, the FPR
over the good-control corpus, per-family friction, and — for the corpus's one
`kind: target` sidecar (subgroup-harm-without-disposition, Phase 29) — the
severity of its firing code (DSX-COH-041) at all four gate points. That target
block is the honest inverse of the ABSENT loop's `fires_at_any_severity` detail:
it does NOT touch the PRESENT-partition denominator.

Copied forward from .planning/milestones/v2.0.0-phases/12-calibration/_measure_readout.py
(Phase-12 template) with the body unchanged except: (1) the ROOT-resolves assertion
below, and (2) the appended `out["target"]` block. NOT the reproducer of record —
the durable gate is tests/test_known_bad_corpus.py::test_stratified_catch_rate_and_fpr_report.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# The new file sits at .planning/phases/30-calibration-rebaseline/, three levels
# below the repo root — same depth as the Phase-12 template — so parents[3] still
# resolves ROOT. Assert it rather than assume (plan 30-01 Task 1).
assert (ROOT / "tests" / "test_known_bad_corpus.py").exists(), (
    f"ROOT misresolved to {ROOT}; adjust parents index"
)
sys.path.insert(0, str(ROOT))

import tests.test_known_bad_corpus as T  # noqa: E402
from dsx.loader import load  # noqa: E402

tc = T.TestKnownBadCorpus()
SPEC = T.SPEC_SUFFIX
ATTR = T.ATTRIBUTION_SUFFIX
POINTS4 = ("plan", "execute", "verify", "ship")

out = {}

# ── FPR over the good-control corpus ──────────────────────────────────────────
good = sorted(T.GOOD_CORPUS_DIR.glob(f"*{SPEC}"))
fpr_blockers = {}
for p in good:
    _c, findings = tc._gate_findings(p, "ship")
    fp = T._false_positive_findings(findings, T._FPR_TEMPDIR_NOISE_CODES)
    if fp:
        fpr_blockers[p.name[: -len(SPEC)]] = sorted(fp)
out["fpr"] = {"num": len(fpr_blockers), "denom": len(good), "blockers": fpr_blockers}

# ── PRESENT partition (live, per-case) ────────────────────────────────────────
effective = T._effective_target_map()
present = []
pd = pc = 0
for path in tc._spec_paths():
    slug = path.name[: -len(SPEC)]
    for point in T._CRITICAL_THRESHOLD_POINTS:
        expected = effective.get(slug, {}).get(point)
        if not expected:
            continue
        pd += 1
        code, findings = tc._gate_findings(path, point)
        problems = T._classify_target_defect(slug, point, code, findings, effective)
        caught = problems == []
        pc += int(caught)
        present.append((slug, point, sorted(expected), caught))
out["present"] = {"caught": pc, "denom": pd, "cases": present}

# ── ABSENT partition (miss attribution) + any-severity firing check ───────────
absent = []
ad = am = 0
for sidecar in tc._attribution_paths():
    data = load(str(sidecar))
    if data.get("kind", "miss") != "miss":
        continue
    ad += 1
    slug = sidecar.name[: -len(ATTR)]
    spec_path = T.CORPUS_DIR / f"{slug}{SPEC}"
    absent_code = data["absent_code"]
    all_crit = set()
    any_sev = {}  # code present at any severity, per point
    fires_any = False
    for point in POINTS4:
        _c, findings = tc._gate_findings(spec_path, point)
        crit = {f["code"] for f in findings if f.get("severity") == "CRITICAL"}
        all_crit |= crit
        for f in findings:
            if f["code"] == absent_code:
                fires_any = True
                any_sev.setdefault(point, []).append(f.get("severity"))
    missed_critical = absent_code not in all_crit
    am += int(missed_critical)
    absent.append({
        "slug": slug,
        "absent_code": absent_code,
        "promotes": data.get("promotes_backlog_item"),
        "missed_critical": missed_critical,
        "fires_at_any_severity": fires_any,
        "any_severity_detail": any_sev,
    })
out["absent"] = {"misses": am, "denom": ad, "cases": absent}

# ── Headline ──────────────────────────────────────────────────────────────────
headline = T._headline((pc, pd), (am, ad), (out["fpr"]["num"], out["fpr"]["denom"]))
out["headline"] = {"miss_rate": headline[0], "fpr": headline[1]}
out["absent_floor"] = T._ABSENT_PARTITION_FLOOR

# ── Friction per family (raw/net) + corpus totals ─────────────────────────────
friction = []
tr = tn = 0
for path in tc._spec_paths():
    slug = path.name[: -len(SPEC)]
    _c, findings = tc._gate_findings(path, "ship")
    blocking = {f["code"] for f in findings if f["severity"] in ("CRITICAL", "HIGH")}
    own = T._own_target_codes(slug)
    raw, net = T._friction(blocking, own)
    tr += raw
    tn += net
    friction.append({"slug": slug, "raw": raw, "net": net,
                     "blocking": sorted(blocking), "own": sorted(own)})
cells = T._non_target_in_profile_cells(effective, {p.name[:-len(SPEC)] for p in tc._spec_paths()},
                                       T._CRITICAL_THRESHOLD_POINTS)
out["friction"] = {"total_raw": tr, "total_net": tn, "cells": cells,
                   "raw_rate": T._friction_rate(tr, cells),
                   "net_rate": T._friction_rate(tn, cells),
                   "families": friction}

# ── TARGET sidecar(s) (kind: target) — the honest inverse of the ABSENT block ──
# For each `kind: target` sidecar (the corpus's first is subgroup-harm-without-
# disposition, Phase 29), measure the severity of its firing code (`absent_code`,
# which for a target names the code that FIRES) at all four gate points. This is a
# read-only supplement: it does NOT touch the PRESENT-partition denominator. It lets
# the readout cite DSX-COH-041's full plan/verify/ship CRITICAL catch profile as the
# target's evidential content, mirroring how the two new misses cite
# fires_at_any_severity:false.
target = []
for sidecar in tc._attribution_paths():
    data = load(str(sidecar))
    if data.get("kind", "miss") != "target":
        continue
    slug = sidecar.name[: -len(ATTR)]
    spec_path = T.CORPUS_DIR / f"{slug}{SPEC}"
    fires_code = data["absent_code"]  # schema-legacy field; for a target it FIRES
    severity_by_point = {}
    for point in POINTS4:
        _c, findings = tc._gate_findings(spec_path, point)
        sev = [f.get("severity") for f in findings if f["code"] == fires_code]
        severity_by_point[point] = sev
    target.append({
        "slug": slug,
        "fires_code": fires_code,
        "promotes": data.get("promotes_backlog_item"),
        "severity_by_point": severity_by_point,
    })
out["target"] = target

print(json.dumps(out, indent=2))
