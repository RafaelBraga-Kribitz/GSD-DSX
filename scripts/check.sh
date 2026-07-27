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
for point in plan execute verify ship; do
  ./bin/dsx gate "$point" --spec examples/good-ANALYSIS-SPEC.yaml >/dev/null 2>&1 \
    || { echo "FAIL: good spec blocked at $point"; exit 1; }
  if ./bin/dsx gate "$point" --spec examples/bad-ANALYSIS-SPEC.yaml >/dev/null 2>&1; then
    echo "FAIL: bad spec passed at $point"; exit 1
  fi
done
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
