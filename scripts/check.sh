#!/usr/bin/env sh
# Full verification. Run before committing anything.
set -eu
cd "$(dirname "$0")/.."

echo "==> unit tests"
python3 -m unittest discover -s tests -q

echo "==> finding catalogue is current"
python3 scripts/gen-finding-catalogue.py --check

echo "==> capability manifest is valid JSON and internally consistent"
python3 scripts/validate-capability.py

echo "==> gate contract: good spec passes, bad spec blocks, missing spec errors"
# REQ-P11.2-05: run against isolated copies of examples/, not the committed
# tree directly, and never sharing one trail root between the good and bad
# specs. examples/DECISIONS.jsonl is a real, ever-growing, gitignored trail
# (already several distinct historical frame_digest values), and
# DSX-PRE-041's identity-free floor (dsx/frame/prereg.py) fires HIGH at
# verify/ship on any root recording more than one distinct frame_digest —
# an accepted, documented residual (T-11.2-07) whose deliberate cost is
# exactly this: a root shared across two different specs (even a fresh one,
# once both specs' own headers land in it) trips the floor as a false
# positive. Two separate copies, one per spec, is the isolation the floor's
# own design requires. Sibling artifacts (the good fixture's DATA-PROFILE,
# figures, evidence, narrative, entrypoint) still resolve, because each
# whole tree is copied, not just the one spec inside it.
gate_tmp="$(mktemp -d)"
trap 'rm -rf "$gate_tmp"' EXIT
cp -R examples "$gate_tmp/good"
cp -R examples "$gate_tmp/bad"
rm -f "$gate_tmp/good/DECISIONS.jsonl" "$gate_tmp/bad/DECISIONS.jsonl"
for point in plan execute verify ship; do
  ./bin/dsx gate "$point" --spec "$gate_tmp/good/good-ANALYSIS-SPEC.yaml" >/dev/null 2>&1 \
    || { echo "FAIL: good spec blocked at $point"; exit 1; }
  if ./bin/dsx gate "$point" --spec "$gate_tmp/bad/bad-ANALYSIS-SPEC.yaml" >/dev/null 2>&1; then
    echo "FAIL: bad spec passed at $point"; exit 1
  fi
done
rm -rf "$gate_tmp"
trap - EXIT
missing_code=0
./bin/dsx gate ship --spec /nonexistent.yaml >/dev/null 2>&1 || missing_code=$?
[ "$missing_code" -eq 2 ] || { echo "FAIL: missing spec exited $missing_code, expected 2"; exit 1; }

echo "==> determinism: identical input, identical output"
# The bad fixture exits 1 by design, so guard the assignment against `set -e`.
a=$(./bin/dsx audit --spec examples/bad-ANALYSIS-SPEC.yaml --json 2>&1) || true
b=$(./bin/dsx audit --spec examples/bad-ANALYSIS-SPEC.yaml --json 2>&1) || true
[ "$a" = "$b" ] || { echo "FAIL: non-deterministic output"; exit 1; }

echo
echo "all checks passed"
