<dsx_verification_stance>
This phase produced analytical claims and figures. Verify the claims and the
geometry, not that the notebook ran.

**Gate A → B → C → D (early exit).** Stop polishing once a higher gate fails:

| Gate | Question | Deterministic proxies |
|---|---|---|
| **A** | Wrong / no analytical question | `DSX-COH-*`, empty decision, `DSX-SPEC-010` |
| **B** | Broken question→metric→conclusion logic | `DSX-CLM-*`, `DSX-CAU-*`, `DSX-STA-*`, `DSX-NAR-*`, `DSX-DEC-*`, `DSX-COH-031`, `DSX-EXP-051` |
| **C** | Chart type fundamentally wrong | `DSX-VIZ-001`, `DSX-VIZ-010`–`014` |
| **D** | Misleading construction / unsealed artifact | `DSX-VIZ-020+`, `DSX-FIG-*`, `DSX-SMELL-*`, `DSX-DQ-*`, `DSX-CODE-*`, `DSX-REP-050+` |

Do not spend ink on takeaway wording while A–D still emit CRITICAL/HIGH.

**Start from the deliverable's headline number and work backwards:**

1. Which artefact produced it? If nothing does, the claim is unsupported.
2. Does the artefact's number match the claim's number, to the digit?
3. Does the design license the claim's verb?
4. Would the claim survive the obvious challenge?

**Run the deterministic audit and treat its output as evidence:**

```
dsx gate verify --phase-dir <phase> --report <phase>/DATA-REVIEW.md --verbose
```

The verify profile runs `dq`, `coherence`, `viz`, `smells`, `figures`,
`narrative`, `code`, and `decision`. Profile assertions must match
DATA-PROFILE.yaml, evidence pointers must resolve, claim strength must not
exceed the question type, every claim text must appear in `narrative.path`,
assumptions must be checked or waived, `decision.replay` must match
`results.tests`, `repro_lock` must be present (or explicitly null), the
entrypoint must not fit before split, chart marks must fit the input-type
matrix, and every `artifact_path` must seal. Every CRITICAL and HIGH finding is
a BLOCKER unless the phase explicitly and justifiably overrides it. Cite finding
codes in `VERIFICATION.md`.

**Do not accept as verification:** that the notebook ran, that the chart renders,
that the numbers "look reasonable". A leaked feature produces beautiful numbers.
A swapped SVG without a matching `svg_sha256` is not the chart you reviewed.
</dsx_verification_stance>
