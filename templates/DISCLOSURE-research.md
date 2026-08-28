# Research AI-assistance disclosure (template)

This template follows the **GUIDE-LLM** disclosure structure. GUIDE-LLM here is the
STRUCTURE this file mirrors — it is a **template, not a third-party dependency**:
nothing is installed and nothing is imported. Author the disclosure in-repo from the
sections below.

This block is written and read **only for a research-domain readout** (`dsx.domain ==
research`), is **optional even then**, and is **not gated** — no `dsx` check opens it,
so it mints no finding code. It is an analyst artifact like `EDA.md`: written, read,
ungated. Fill the placeholders; delete any sub-part that does not apply, with a one-line
reason.

## AI-assistance disclosure

### AI-assisted steps

What the model did — the concrete steps the assistant performed (drafting, code
generation, chart construction, literature triage). State the model/version where it
matters to reproducibility.

### Human-reviewed decisions

What a human decided and checked — the judgement calls that were not delegated
(metric definitions, the decision rule, which results to trust, what to publish). Name
who reviewed.

### Data handling

What data the assistant saw and how — whether raw records, a profile, or only
aggregates; where the data lived; any PII or access constraints that applied.

### Reproducibility

How to reproduce — seed(s), environment, and a pointer to the analysis entrypoint
(`scripts/*.py` or the notebook/spec) so the reported numbers can be regenerated.
