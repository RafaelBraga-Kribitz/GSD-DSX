# Phase 12: Calibration - Discussion Log (Assumptions Mode)

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions captured in `12-CONTEXT.md` — this log preserves the analysis.

**Date:** 2026-08-27
**Phase:** 12-calibration
**Mode:** assumptions (headless ceremony — AskUserQuestion gates replaced by a Statistician-led
3-persona round per LOOP-BRIEF §4; orchestrator tie-break rigour > reliability > flexibility)
**Areas analyzed:** Corpus composition & sizing; Catch-attribution (miss) tags; Catch-rate/FPR/friction harness; `dsx stats --paradigm`; §6.5 backlog re-evaluation & reversals; Finding-code footprint

## Assumptions Presented (from gsd-assumptions-analyzer, opus)

### Corpus composition and "full size"
| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| "Full size" is an evidence-driven target (make every §6.5 count decidable), not a fixed N; keep glob discovery + spec+postmortem pairing | Likely | `tests/test_known_bad_corpus.py:544-550,618-632`; `brief.md:355-356,371,373,377`; `ROADMAP.md:1011-1013` |

### Catch-attribution (miss-attribution) tag schema
| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Tags name the currently-ABSENT code that would catch a MISS + the §6.5 item it promotes; distinct from the present-code maps; must live OUTSIDE validity_frame/inference (frame_digest safety) | Likely (meaning); Unclear (carrier) | `tests/test_known_bad_corpus.py:172-248,388-421,50,663-672`; `dsx/decisions.py:241-250`; `11.3-CONTEXT.md:200-208` |

### Catch-rate / FPR / friction harness
| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Reuse live-gate machinery to compute catch rate, FPR, and a LIVE per-family friction column (blocking − own-target); the stale ledger forbidden for lifting is `_INCIDENTAL_GAP_CODES` (+ `_GOLDEN_SHIP_FINDINGS`) | Confident (machinery); Likely (formula) | `tests/test_known_bad_corpus.py:64-88,251-306,555-616`; `tests/test_causal_verb_golden.py:82-142`; `ROADMAP.md:712-715` |

### `dsx stats --paradigm`
| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| New argparse subcommand modelled on `cmd_explain` (reader, exit 0); reads paradigm from DECISIONS.jsonl `choice="paradigm=…"`; risk = frame-history scope + dedup key (polluted test floor) | Confident (wiring); Unclear (scope/dedup) | `dsx/cli.py:67,563-637,810-925,334-393`; `dsx/frame/paradigm.py:616,626`; `dsx/decisions.py:117-121,182-257` |

### §6.5 backlog re-evaluation and D-14 reversals
| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| All 9 items re-scored against measured corpus; most carry; Deng & Hu ratio-metric is the clearest removal-that-reverses (needs a REV record) | Confident (enumeration); Likely (7/8/9 outcome) | `brief.md:369-379,108-110`; `.planning/REVERSALS.md:18-38,60-81`; `tests/test_known_bad_corpus.py:1043-1069` |

### Finding-code footprint
| Assumption | Confidence | Evidence |
|------------|-----------|----------|
| Phase 12 mints ZERO new DSX-* codes; catalogue stays 256; nothing added to GATE_PROFILES | Confident | `references/finding-codes.md:16`; `dsx/cli.py:115-131,563-637` |

## Persona Round — options, answers and votes

Panel (all opus, concurrent): **Statistician** `dsx-statistician` (lead),
**Architect** `dsx-analysis-architect`, **Auditor** `dsx-ml-integrity-auditor`.

| DP | Statistician | Architect | Auditor | Orchestrator decision (tie-break rigour>reliability>flexibility) |
|----|--------------|-----------|---------|------------------------------------------------------------------|
| DP-1 Corpus "full size" | Evidence-driven, source-before-count; **FPR needs denominator > 1 → add multi-spec good-side control** | Coverage-driven via glob predicates + `≥3` floor; 4-file case contract | **Stratify catch rate PRESENT vs ABSENT; floor the ABSENT partition; headline = (miss-rate, FPR)** | **D-01, D-02, D-03, D-04, D-10** — all three adopted (coverage predicates + source-before-count + good-side control + stratified headline) |
| DP-2 Attribution tag | Trustworthy only if live-silence + absent-code asserted; count distinct confirmed cases | **Carrier = sidecar `<slug>-ATTRIBUTION.yaml`**; schema `{absent_code, promotes_backlog_item, rationale?, kind?}` | Harness must verify tag both directions; **hypothetical/unshipped code ⇒ counts as miss** | **D-05, D-06, D-07, D-08** — sidecar (Architect) + live falsifiability both directions + hypothetical-as-miss (Auditor/Statistician) |
| DP-3 Friction | `blocking − own-target` and nothing more; report as a **rate over non-target in-profile cells** | LIVE `ship-blocking − own-target`, per-family column; no stale-constant reuse | **Report RAW and NET; close incidental→own relabel; arithmetic + live-source proofs** | **D-09, D-11** — raw+net, live, rate over non-target cells, three anti-lift/relabel guards |
| DP-4 `dsx stats --paradigm` | **Distinct `frame_digest` grouped by `spec_id`, real `.planning` trails only**; floor hard-excluded (measured 45.8% raw would trip 15% four-fold) | New `stats` subparser, `cmd_stats` reader; source excludes known-bad floor; unit = distinct `spec_id` → `frame_digest` fallback | Count **distinct `frame_digest`**, operator-scoped; synthetic-trail assertion returns distinct-frame %, negative assertion on the floor | **D-12, D-13, D-14** — reader subcommand; hard-exclude the floor; **unit = distinct `frame_digest`** (spec_id label only, it is often unset) + synthetic-trail guard |
| DP-5 §6.5 + reversals | Remove item 6 as **permanently unevaluable**; determinism is NOT new evidence → don't launder (SELF-001); items 4/5 carried | REV-002, **relocate-not-delete** preserving pinned substrings; carry 8, remove 1; items 4/5 carried | REV-002 anchored on Formula-(3) structure; retain+pin; **"unevaluable⇒remove" only for structural unreachability**; items 4/5 carried | **D-15, D-16, D-17** — carry 8 / remove 1; relocate+pin (Architect/Auditor mechanism); **REV-002 framed honestly as reclassification, determinism not laundered as novelty (Statistician rigour wins the framing tie)** |
| Zero-mint | Concur | Concur | Concur | **D-18** — 0 codes, catalogue 256, catalogue-invariant test |

**Divergence resolved:** DP-5 REV-002 framing. The Auditor proposed anchoring "new evidence" on
"Formula (3) was read / access premise falsified / no scalar multiplier." The Statistician
countered that the §6.5 row *already* records those facts (access was never the blocker; no
closed-form scalar multiplier; determinism doesn't lift with time), so they are not new relative
to the current deferral, and claiming them as novelty risks SELF-001. Verified against
`brief.md:376` — the row does already contain that reasoning. **Tie broken on rigour toward the
Statistician:** REV-002 is framed as a reclassification under REQ-P12-05's systematic
re-evaluation recognizing structural unreachability, explicitly not as an evidence-driven
reversal — while adopting the Architect/Auditor relocate-and-pin mechanism.

## Corrections Made
No user corrections (headless). All decisions are persona-round outputs, loud and vetoable via
the daily summary per LOOP-BRIEF §4.

## Auto-Resolved
Not applicable (persona round, not `--auto`).

## External Research
None performed. One flagged need — *which specific retracted papers / p-hacking cases are
admissible under D-05* — is deliberately deferred to the Phase-12 UAT round (the citation read is
a human D-05 gate; candidate sources may be prepared but authenticity must not be asserted here).
