# Term-Level Changelog

Use this changelog to record ontology term changes in a form that can be reviewed, migrated, and published.

## Required Fields

| Field | Meaning |
| --- | --- |
| new term | A term added to UOGTO for the first time. |
| changed definition | A term whose meaning changed but whose IRI did not. |
| deprecated term | A term that remains in the repository for compatibility but is no longer preferred. |
| replacement IRI | The preferred IRI that should be used instead of a deprecated term. |
| migration note | A short implementation note for examples, SHACL, and downstream mappings. |

## Entry Template

| Date | Event type | Term label | Term IRI | New term | Changed definition | Deprecated term | Replacement IRI | Migration note | Rationale | Source or reviewer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Example rows should be appended here as the ontology changes.

## Handling Rules

- Keep the changelog at term granularity, not module granularity.
- Record one entry per semantic change, even if multiple files are updated.
- Use the deprecation policy for the decision logic behind the entry.
- Prefer explicit replacement IRIs rather than informal synonym notes.
- Migration notes should tell a downstream maintainer what to change, not just why the change happened.

