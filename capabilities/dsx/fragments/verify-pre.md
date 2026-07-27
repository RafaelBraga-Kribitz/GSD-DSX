<dsx_statistical_review>
Before phase verification, `dsx-statistician` reviews the statistical content of
what was produced and writes `STATS-REVIEW.md`.

The agent runs the deterministic audit first (`dsx audit --phase-dir <phase>
--json`), then adds the judgement the code cannot make: whether the effect is
large enough to matter, whether the population generalises to the one the
decision covers, and whether a simpler explanation fits the result.

Findings from the audit are facts. The agent's additions are opinions, and are
labelled as such in the report.
</dsx_statistical_review>
