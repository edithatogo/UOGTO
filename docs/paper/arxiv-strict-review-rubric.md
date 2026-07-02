# arXiv Strict Review Rubric

The UOGTO arXiv submission is scored out of `1000` points. A local pass requires:

- score above `995/1000`;
- no blockers;
- no category below `98%`;
- external arXiv UI steps recorded as external rather than locally complete.

## Categories

| Category | Points | Reviewer |
| --- | ---: | --- |
| TeX/source package | 180 | TeX/source processor reviewer |
| Format requirements | 140 | arXiv compliance moderator |
| Metadata and policy | 140 | Metadata/category reviewer |
| Citations and source integrity | 140 | Source-integrity reviewer |
| Moderation and topicality risk | 120 | Moderation reviewer |
| Manuscript quality | 110 | Manuscript readability reviewer |
| Repo/artifact provenance | 100 | Publisher/provenance reviewer |
| Visual PDF QA | 70 | PDF visual reviewer |
| Operational readiness | 100 | Publisher submission manager |

## Blocker Overrides

The score fails regardless of points if a blocking check fails. Blocking checks include
missing upload artifacts, missing title/authorship/abstract, failed privacy audit,
unsafe package filenames, unresolved SourceRight errors, or missing Required Gate.

Official arXiv source constraints are recorded in the Conductor track specification.
