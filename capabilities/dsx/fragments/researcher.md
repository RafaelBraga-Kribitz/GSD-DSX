<dsx_research_contract>
For an analytical phase, research the **data and the decision**, not just the
libraries.

**Establish before planning:**

- **What decision is waiting on this?** An analysis with no pending decision has
  no success criterion. Find the decision or find out there isn't one — both are
  useful findings.
- **Does the metric already have an owner and a definition?** Check the semantic
  layer, the dbt models, the existing dashboards. Two definitions of the same
  word is the most expensive thing you can discover late.
- **What does the data actually contain?** Row counts, period covered, known
  outages, upstream filters, late-arriving records, timezone of the date column.
  Report these as numbers, not as "data looks fine".
- **What is the grain of each source, and where does joining change it?** Fan-out
  is the single most common cause of numbers that disagree.
- **Has this been analysed before?** A prior result that contradicts yours is
  worth more than another week of modelling. Before concluding none exists, grep the
  dated files in `docs/dsx/learnings/` on domain / question_type / metric.
- **What is the baseline?** For prediction: the trivial rule to beat. For an
  experiment: the current rate and its natural week-to-week variance — if the
  metric swings 3pp on its own, a 2pp MDE is not detectable.

**Report findings as declarations that land in ANALYSIS-SPEC.yaml** — metric
definitions, data periods, row counts, baseline rates. Prose that cannot be
transferred into the spec is prose the gates cannot check.
</dsx_research_contract>
