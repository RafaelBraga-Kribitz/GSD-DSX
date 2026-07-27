# gsd-dsx

**Data science, analytics and BI rigour for GSD Core.**

## Purpose

Specialise the GSD phase loop for analytical work without forking gsd-core.
Agents fill structured contracts; deterministic Python gates block the loop when
the contracts and artifacts do not hold up.

## Success bar — ten quality dimensions

Every analytical phase that ships under dsx must satisfy these with code where
decidable, and with strong agent guardrails where judgement is required:

1. Analytical Question
2. Analytical Logic
3. Chart Type
4. Missing Evidence
5. Data Quality
6. Code Quality
7. Statistical Issues
8. Plot Construction
9. Visual Design
10. Communication and Data Storytelling

## Determinism doctrine

| Stochastic (agent judgement) | Deterministic (code) |
|---|---|
| Framing the question, choosing the design, writing claims and narrative | Checking the spec is coherent and that produced artifacts satisfy it |

Gates never read live warehouses. They check declarations and hermetic artifacts
(`ANALYSIS-SPEC.yaml`, `DATA-PROFILE.yaml`, evidence files). `dsx profile`
computes profiles from local CSV when available; the gate still only reads the
written profile.

## Current state

- **v1.4.0** shipped: Phases 1–4 complete. Ten quality dimensions gated where
  decidable (DQ, evidence, coherence, viz/seals/smells, narrative/code, analytical
  logic / stats extensions including decision replay and repro_lock).

## Non-goals

- Patching gsd-core workflows
- Third-party Python deps inside the gate process
- Reading production databases from `dsx gate`
