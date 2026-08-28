---
phase: 06-contract-extension-decision-record-paradigm-manifest
reviewed: 2026-08-08T00:00:00Z
depth: deep
files_reviewed: 27
files_reviewed_list:
  - .claude-plugin/marketplace.json
  - .claude-plugin/plugin.json
  - README.md
  - capabilities/dsx/capability.json
  - dsx/__init__.py
  - dsx/cli.py
  - dsx/decisions.py
  - dsx/frame/__init__.py
  - dsx/frame/paradigm.py
  - dsx/loader.py
  - dsx/spec.py
  - examples/bad-ANALYSIS-SPEC.yaml
  - examples/good-ANALYSIS-SPEC.yaml
  - examples/known-bad/bayesian-continuous-monitoring-ANALYSIS-SPEC.yaml
  - examples/known-bad/bayesian-continuous-monitoring-POSTMORTEM.md
  - examples/known-bad/frequentist-uncontrolled-continuous-ANALYSIS-SPEC.yaml
  - examples/known-bad/frequentist-uncontrolled-continuous-POSTMORTEM.md
  - examples/known-bad/interference-shared-budget-ANALYSIS-SPEC.yaml
  - examples/known-bad/interference-shared-budget-POSTMORTEM.md
  - references/finding-codes.md
  - scripts/gen-finding-catalogue.py
  - templates/ANALYSIS-SPEC.yaml
  - tests/fixtures/d05/bad_check.py
  - tests/test_decisions.py
  - tests/test_dsx.py
  - tests/test_frame_boundary.py
  - tests/test_gen_finding_catalogue.py
  - tests/test_known_bad_corpus.py
findings:
  critical: 0
  warning: 4
  info: 1
  total: 5
status: issues_found
---

# Phase 06: Code Review Report

**Reviewed:** 2026-08-08T00:00:00Z
**Depth:** deep
**Files Reviewed:** 27
**Status:** issues_found

## Summary

This is a re-review after gap-closure plans 06-11, 06-12 and 06-13 landed on top
of the original Phase 6 body of work. A prior `06-REVIEW.md` (superseded by this
one) found two BLOCKERs and three WARNINGs; I independently re-verified each of
those against the current tree rather than trusting the gap-closure plans'
summaries, then did a fresh adversarial pass over the same file set looking for
anything the gap-closure changes might have introduced or missed.

**Previously-found defects, independently re-verified as fixed:**

- **Old CR-01** (`dsx explain` / gate-path trail writer crash on non-UTF-8
  `DECISIONS.jsonl`) — fixed by 06-11. Reproduced the exact prior failing
  scenario (an invocation header followed by a dangling UTF-8 lead byte) against
  the current tree: `dsx explain` now exits 0, and `dsx gate plan` against both a
  passing and a blocking spec now produces the *same* exit code with and without
  the corrupted trail present. `read_all()` decodes with `errors="replace"` and
  wraps the read in `except OSError`; `_write_decision_trail` and `cmd_explain`
  both now guard `except Exception` (confirmed *not* `except BaseException` and
  *not* a bare `except:` — `KeyboardInterrupt`/`SystemExit` are left to
  propagate, matching both docstrings' explicit claims).
- **Old CR-02** (`examples/known-bad/*` fixtures and postmortems asserting a
  false "passes every gate" claim) — fixed by 06-12. I independently ran
  `dsx gate {plan,execute,verify,ship}` against all three fixtures in fresh temp
  directories and diffed the measured CRITICAL/HIGH codes against each fixture
  header's prose and against `_INCIDENTAL_GAP_CODES`: the Bayesian fixture names
  exactly 7 incidental-gap codes, the frequentist fixture exactly 6, the
  interference fixture exactly 5 — all three match what `dsx gate ship --json`
  actually emits today, byte for byte. The retired overclaim strings ("passes
  every gate", "validate/gate checks pass it") no longer appear anywhere under
  `examples/known-bad/`, and `test_no_corpus_file_repeats_a_retired_gate_overclaim`
  now guards against reintroduction.
- **Old WR-01** (`_INFERENCE_FIELDS` dead-code comment overstating enforcement)
  — fixed by 06-13's docs commit; the comment now states plainly that only
  three of the six fields are membership-checked and that no unknown-key check
  exists for the block.
- **Old WR-03** (D-05 allow-list's bare numeric-string prefix `"DSX-SPEC-08"`)
  — fixed by 06-13. `_D05_ALLOWLIST_PREFIXES` is now hyphen-terminated
  (`("DSX-PAR-",)`) and the five individual `DSX-SPEC-08x` codes are named
  exactly in a `frozenset`. `test_d05_covered_code_set_on_the_real_tree_is_exactly_the_documented_set`
  proves the covered set is precisely the family-prefix match unioned with the
  exact-code set — no code became newly exempt or newly enforced beyond intent.
- **Old IN-01** (`_package_for`'s dead if/else) — fixed exactly as suggested;
  collapsed to unconditional `parts[:-1]` with an explanatory comment.
- **WR-02 from the prior review** (non-atomic `next_invocation_id()` +
  `append()` under concurrent `dsx gate` runs) was left deliberately unfixed and
  is now documented accurately in three places (`dsx/decisions.py`'s module and
  function docstrings, and README.md's "Concurrent `dsx gate` invocations are
  not supported" section) — per this review's scope, not re-flagged as a new
  defect.

I also independently re-ran the full test suite (286 tests, 2 skipped, all
green) and `gen-finding-catalogue.py --check` (exits 0).

**New findings from this pass**, all WARNING/INFO — deep review of the newer
Phase 6 surface (`dsx/decisions.py`, `dsx/frame/paradigm.py`) turned up one
reproducible cross-platform correctness defect and a small set of
robustness/documentation gaps that the gap-closure plans' scope didn't touch.
Nothing found rises to BLOCKER level (no gate exit code, security, or data-loss
impact).

## Warnings

### WR-01: `dsx/decisions.py::append()` writes CRLF line endings on Windows, contradicting the documented "single `\n`" format contract

**File:** `dsx/decisions.py:111-119`
**Issue:** The module docstring (lines 12-15) states the append contract in
explicit, normative terms: *"one JSON object per line... followed by a single
`\n`"*. `append()` opens the file with `Path(path).open("a", encoding="utf-8")` —
default text-mode newline translation — and writes `line + "\n"`. On any platform
where `os.linesep != "\n"` (Windows — the platform this review is running on),
Python's text-mode write translates that trailing `"\n"` into `"\r\n"`.
Reproduced directly against this checkout:

```python
>>> append(p, DecisionRecord(id="DEC-001", invocation_id="INV-0001", layer="deterministic", choice="x"))
>>> p.read_bytes()[-5:]
b'""}\r\n'
```

`read_all()` still parses this correctly because `str.splitlines()` treats
`\r\n`/`\r`/`\n` uniformly, so no gate exit code or `dsx explain` output is
affected — that's why the full suite still passes 286/286 on this same machine.
But the on-disk bytes do not match what the docstring promises "any future
writer of this file" (the docstring's own words), and
`test_append_is_deterministic_byte_identical` only proves determinism *within* a
single platform run, not across platforms — its name overstates the guarantee it
actually tests; a fixture or hash produced by a run on Linux/macOS CI will not
byte-match one produced on Windows for the identical record.
**Fix:** Open in binary mode and encode explicitly (also removes the platform
dependency entirely, in keeping with the module's "hermetic, stdlib-only"
design):

```python
def append(path: "str | Path", record: "DecisionRecord | InvocationHeader") -> None:
    line = (json.dumps(record.to_dict(), sort_keys=True) + "\n").encode("utf-8")
    with Path(path).open("ab") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())
```
(equivalently, keep text mode but pass `newline=""` to `open()`, which disables
newline translation on every platform).

### WR-02: `dsx/frame/paradigm.py::check()` does not distinguish an unrecognised `inference.paradigm` value from a legitimate one in the DSX-PAR-001 manifest

**File:** `dsx/frame/paradigm.py:80-105, 128-144`
**Issue:** `paradigm = normalize(declared) if not is_blank(declared) else ""`
treats *any* non-blank string as "declared", not just members of `PARADIGMS`.
When the value is not a `PARADIGMS` member (e.g. a typo like
`paradigm: quantum`), the `if paradigm:` branches in both the `detail` string
(line 105) and the counterfactual (lines 128-144) execute exactly as if a real,
merely-unshipped paradigm had been declared — the caveat sentence *"no
paradigm-conditional family was selected"* only fires when `paradigm` is
empty/blank, not when it's garbage. Reproduced directly:

```python
>>> paradigm.check({"inference": {"paradigm": "quantum"}}).findings[0].title
"paradigm manifest — inference.paradigm: quantum"
>>> ... .context["decisions"][0]["counterfactual"]
"Declaring 'frequentist' instead would select DSX-PAR-010, DSX-ADM- in place of this run's paradigm-conditional set."
```
Nothing in the INFO-severity manifest calls out that `"quantum"` is invalid
vocabulary. `dsx/spec.py::_validate_inference_shape` does catch this
(`DSX-SPEC-085`, HIGH) — but `plan`/`execute` block at CRITICAL, so
`dsx gate plan` and `dsx gate execute` both pass silently with a garbage
paradigm value, and the one output that is supposed to make paradigm-related
gaps "cost nothing to see" (D-10, this module's own stated purpose) presents
the typo identically to an honest declaration until `verify`/`ship`.
**Fix:** Gate the caveat and the counterfactual on membership in `PARADIGMS`
rather than on blankness alone:

```python
from ..spec import PARADIGMS  # already imported at module scope

recognised = paradigm in PARADIGMS
...
+ ("" if recognised else f"\n{paradigm!r} is not a member of PARADIGMS — no paradigm-conditional family was selected")
```
and use the same `recognised` flag to gate the `if paradigm:` branch of the
counterfactual block.

### WR-03: `README.md`'s Development section still claims "121 tests" though the suite is now 286

**File:** `README.md:291`
**Issue:** `python3 -m unittest discover -s tests -v     # 121 tests` — the
actual count (verified by running it) is 286 tests, 2 skipped. `README.md` was
edited twice within this phase (06-04, 06-11 commits) without updating this
inline comment, and this phase alone added several new test modules
(`tests/test_decisions.py`, `tests/test_frame_boundary.py`,
`tests/test_gen_finding_catalogue.py`, `tests/test_known_bad_corpus.py`) plus
hundreds of new cases in `tests/test_dsx.py`, so the comment is now off by more
than 2x.
**Fix:** Either drop the stale count entirely or replace it with a phrase that
does not need updating every phase, e.g. `# full suite`.

### WR-04: `capabilities/dsx/capability.json` and `.claude-plugin/plugin.json` bump `version` to `2.0.0` but leave `description` describing v1.5

**File:** `capabilities/dsx/capability.json:6`, `.claude-plugin/plugin.json:5`
**Issue:** Commit `3b4f870` ("bump package version to 2.0.0 across all
declaration sites") changed the `version` field in both manifests to `"2.0.0"`
but left the `description` field's trailing sentence — *"v1.5 adds ADR/SPEC
finding suppressions and scored CHART-REVIEW.md via dsx-chart-audit."* —
unchanged. The description now advertises itself as version 2.0.0 while its own
trailing clause still names v1.5 features and never mentions any of the actual
v2.0.0 additions this phase ships (the `validity_frame:` gate at CRITICAL
severity, the `DECISIONS.jsonl` decision trail / `dsx explain`, the
`DSX-PAR-001` paradigm manifest) — precisely the features README.md's
"Migrating a pre-v2.0.0 spec" section tells operators to expect.
**Fix:** Update the trailing clause to name the v2.0.0 additions, or drop the
version-specific clause from the manifest description entirely and keep that
history only in README.md, which already carries it accurately.

## Info

### IN-01: Inconsistent normalisation defensiveness between the two Phase 6 shape validators

**File:** `dsx/spec.py:816, 909`
**Issue:** `_validate_validity_frame_shape`'s membership check normalises both
sides — `normalize(value) not in {normalize(k) for k in vocab}` (line 816) —
with an explicit comment explaining why (case-insensitive matching against the
case-sensitive `MISSINGNESS_MECHANISMS` acronyms). `_validate_inference_shape`'s
membership check normalises only the input value —
`normalize(value) not in vocab` (line 909) — against the raw vocabulary dict's
keys. Every current vocabulary referenced by `_INFERENCE_MEMBERSHIP`
(`PARADIGMS`, `PARADIGM_JUSTIFICATIONS`, `DECLARATION_POINTS`) happens to use
already-normalized (lowercase, underscore) keys today, so this is not a live
bug, but the two validators now disagree on whether vocab keys need
normalising, and a future vocabulary added with a mixed-case or hyphenated key
(mirroring how `MISSINGNESS_MECHANISMS` already is) would silently stop
matching in `_validate_inference_shape` while continuing to match in
`_validate_validity_frame_shape`.
**Fix:** Reuse the same `{normalize(k) for k in vocab}` idiom in
`_validate_inference_shape`, or factor the pattern into one shared helper both
functions call.

---

_Reviewed: 2026-08-08T00:00:00Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: deep_
