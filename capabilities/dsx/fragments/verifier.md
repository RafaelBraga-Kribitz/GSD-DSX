<dsx_verification_stance>
This phase produced analytical claims. Verify the claims, not the code.

**Start from the deliverable's headline number and work backwards:**

1. Which artefact produced it? If nothing does, the claim is unsupported.
2. Does the artefact's number match the claim's number, to the digit?
3. Does the design license the claim's verb? "Drives", "increases" and "causes"
   require an identification strategy. Correlation with a confident tone is the
   most common defect in shipped analysis.
4. Would the claim survive the obvious challenge — a confounder, a segment that
   moves the other way, a denominator that shifted between periods?

**Run the deterministic audit and treat its output as evidence:**

```
dsx gate verify --phase-dir <phase> --report <phase>/DATA-REVIEW.md --verbose
```

The verify profile now also runs `dq` and `coherence`: profile assertions must
match DATA-PROFILE.yaml, evidence pointers must resolve, and claim strength must
not exceed the question type. Every CRITICAL and HIGH finding is a BLOCKER unless
the phase explicitly and justifiably overrides it. Cite finding codes in
`VERIFICATION.md`.

**Do not accept as verification:** that the notebook ran, that the chart renders,
that the numbers "look reasonable". A leaked feature produces beautiful numbers.
</dsx_verification_stance>
