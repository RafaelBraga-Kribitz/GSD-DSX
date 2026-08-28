# HUMAN-QUEUE — items only you can answer

Milestone **v2.2 Analytic Surface**. The loop keeps working around these; it only
blocks at the close-out stage (S5-2) if any remain.

**How to answer:** the operator is usually remote and cannot run local commands.
Answer in the session; an interactive Claude session records the verdict in the
proper GSD artifact (UAT file, SECURITY.md) and checks the item off here.

**What reaches this queue** (brief §4 — everything else the loop decides itself via
a persona round and records loudly):

1. A D-05 primary-source read — citation authenticity. The loop may prepare the
   evidence pack; it may not sign it.
2. An irreversible destructive operation (file deletion, history rewrite, force-moving
   a published tag).
3. A change to milestone scope (dropping or rewording a requirement).
4. A security sign-off (`SECURITY.md` approval line).
5. An outward-facing ship action (merge to `main`, release tag, opening a PR).

## Open

### HQ-8 — Phase 15 D-05 citation evidence pack (filed early by design; non-blocking)

**Status: not yet assembled.** Ledger unit S0-3 fills this in. It is filed ahead of
Phase 15 deliberately so the operator can read the sources while Phases 13/14/16
build — Phase 15 is the only v2.2 phase minting new finding codes, so it is the only
one carrying a D-05 gate, and nothing else waits on this.

Expected contents once S0-3 runs:

| # | Read | Anchors | Expected |
|---|------|---------|----------|
| 1 | Deng, Xu, Kohavi & Walker (2013), *Improving the Sensitivity of Online Controlled Experiments by Utilizing Pre-Experiment Data*, WSDM '13 — the exact CUPED formulation **plus a published worked value** to test against. | REQ-P15-02 | Formulation and worked value confirmed at locator. The Unified Framework playbook snippet is explicitly **not** an admissible citation. |
| 2 | Survivorship-bias citation candidate — an admissible primary source with operationalisable criteria. | REQ-P15-04 | Confirmed, or the code stays in `brief.md` §6.5 unshipped rather than invented. |
| 3 | Changing-denominator citation candidate — same bar. | REQ-P15-04 | Same. |

## Will be added by the loop when reached

- Phase 13 / 14 / 16 end-of-phase UAT rounds and security sign-offs (batched per phase).
- Any D-06 numeric finding-code veto window — expected from Phase 15 (S4-1) and
  possibly Phase 16 (S3-1, if its gate check mints a `DSX-REP-*` code).
- The S5-6 ship decisions: merge to `main` and the `v2.2.0` release tag.
- Any persona decision the operator vetoes from a daily summary.

## Standing framework notes (not queue items — nothing to answer, just remember)

**`/gsd-audit-uat`'s automated CLI under-reports human-verification items.**
Found 2026-08-27 during v2.0.0's S4-1: the CLI returns a false "All Clear" because
`gsd-core/bin/lib/uat.cjs::parseVerificationItems` only recognizes a level-2
`## Human Verification` heading, while the `gsd-verifier` template actually writes a
level-3 `### Human Verification Required` heading. Framework-internal defect, not a
bug in this repo — recorded, not patched. **At S5-1 and S5-4, do not accept a CLI
"all clear" as evidence of no outstanding UAT** — cross-check each phase's
VERIFICATION.md by hand.

**`/gsd-pr-branch` does not survive a long ceremony branch.** Its per-commit
cherry-pick chain hit recurring modify/delete and structural-file conflicts on
v2.0.0's 707-commit branch and was abandoned mid-run. Ship by direct 3-way merge
instead — see ledger unit S5-6.

**Release tags: never force-move a published one.** v2.0.0's tag was already on
origin against an earlier partial merge, so the completed milestone shipped as
`v2.1.0` and the queued Analytic Surface milestone was renamed v2.1 → v2.2 to avoid
colliding with it. The next free tag for this milestone is `v2.2.0`.

## Answered

(v2.0.0's answered items — HQ-1 … HQ-7 — are archived at
`.planning/milestones/v2.0.0-HUMAN-QUEUE.md` and
`.planning/milestones/v2.0.0-HUMAN-QUEUE-ARCHIVE.md`.)
