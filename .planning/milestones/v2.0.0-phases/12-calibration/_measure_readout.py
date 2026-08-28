"""S3-4 readout measurement — reuses tests/test_known_bad_corpus.py live functions.

Read-only. Prints the LIVE catch-rate / FPR / friction / miss-attribution numbers
that back 12-READOUT.md, plus (crucially) whether each ABSENT-partition absent_code
fires at ANY severity (not only CRITICAL) across all four gate points — the
DSX-VAL-080-at-HIGH adjudication S3-4 owes the Statistician. Not committed; the
reproducing gate is the test module's own assertions.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
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

print(json.dumps(out, indent=2))
