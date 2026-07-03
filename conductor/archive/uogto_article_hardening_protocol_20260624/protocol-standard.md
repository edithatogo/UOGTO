# Protocol Standard Notes

This track uses a hybrid protocol standard because the work is both a scoping review of ontology/formalism sources and a reproducible computational-analysis package.

## PRISMA-ScR
PRISMA-ScR is used for the review protocol structure and final reporting checklist. The track adapts it to ontology engineering by treating ontologies, vocabularies, standards, schemas, repositories, and formal modelling languages as sources of evidence.

Required protocol coverage:

- Title and rationale.
- Objectives and review questions.
- Eligibility criteria.
- Information sources.
- Search strategy.
- Selection process.
- Data charting process and data items.
- Synthesis approach.
- Limitations and threats to validity.
- Funding, conflicts, and protocol amendments.

## PRISMA-S
PRISMA-S is used for search transparency. Each search route must record enough information for a later reviewer to repeat the search or understand why exact replication is impossible.

Required search-log fields:

- `searched_at`
- `surface`
- `surface_type`
- `query`
- `filters`
- `result_count`
- `screened_count`
- `included_count`
- `route_limitations`
- `operator_notes`
- `source_ids_added`

## RO-Crate 1.1
RO-Crate is used to package the research object for the article-hardening evidence package. The crate should describe local artifacts and external referenced sources without copying non-redistributable content.

Required crate coverage:

- Protocol and protocol checklist.
- Search strategy and search log.
- Source inventories and inclusion/exclusion decisions.
- Scripts used for retrieval, extraction, metrics, validation, and figure generation.
- Retrieved redistributable source artifacts.
- Metadata-only source references.
- Derived metrics, benchmark tables, article tables, figures, and reports.
- Licence, access-rights, provenance, and generation metadata where available.

## Initial Standard Sources
- PRISMA-ScR official page: https://www.prisma-statement.org/scoping
- PRISMA 2020 official page: https://www.prisma-statement.org/prisma-2020
- RO-Crate 1.1 specification: https://www.researchobject.org/ro-crate/1.1/
