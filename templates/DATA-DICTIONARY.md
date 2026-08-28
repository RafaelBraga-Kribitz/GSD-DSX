---
# DATA-DICTIONARY front-matter — the machine-readable half of this file.
#
# It sits next to DATA-PROFILE.yaml and carries the semantics the CSV cannot:
# grain, join keys, per-column meaning, source and PII. The roster below is
# COPIED verbatim from DATA-PROFILE.yaml (column / dtype / null_rate /
# unique_count / source_hash), never recomputed — one extract, one set of
# numbers. A value here that disagrees with the profile is an invented number.
#
# Authoring note: this repo checks out CRLF on Windows. Any parser that reads
# this front-matter must tolerate \r\n — use `\r?\n`, never a bare `\n`, when
# matching line starts or ends.

dataset: <data[].name>
profile_path: DATA-PROFILE.yaml
source_hash: <copied verbatim from DATA-PROFILE.yaml>
grain: <one row = one ...>
primary_key: []
join_keys:
  # each entry is { column, joins_to, cardinality }
  # - { column: user_id, joins_to: users.id, cardinality: many-to-one }
source: <source table / export / warehouse query>
timezone: <IANA tz of any timestamp column, or none>
owner: <who owns this extract and its definitions>
---

# Data dictionary

This file is **written and read, never gated**. No `dsx` check opens it — there is no
existence check and no schema scan over it, so it mints **no finding code**. It is an
analyst artifact like `EDA.md` and `DATA-PROFILE.yaml`: authored once next to the
profile, keyed to the same extract via `source_hash`, and read by later sessions so
grain and join keys are not re-guessed.

## Copied vs authored

- **Copied verbatim from `DATA-PROFILE.yaml`** (deterministic — never recomputed):
  `column`, `dtype`, `null_rate`, `unique_count`, and `source_hash`. A recomputed
  roster that disagrees with the profile is an invented number; copy it, do not
  re-derive it.
- **Authored** (the semantics the CSV cannot carry): `grain`, `primary_key`,
  `join_keys`, and per column `semantic_type`, `description`, `source`, `pii` — plus
  `timezone` and `owner` in the front-matter.

## Column table

`semantic_type` is drawn from the closed set: `identifier`, `foreign_key`,
`timestamp`, `categorical`, `ordinal`, `numeric_measure`, `boolean`, `free_text`,
`derived`.

| column | dtype | semantic_type | null_rate | unique_count | description | source | pii | notes |
|--------|-------|---------------|-----------|--------------|-------------|--------|-----|-------|
| <name> | <copied> | <closed set> | <copied> | <copied> | <authored> | <authored> | yes/no | <authored> |
