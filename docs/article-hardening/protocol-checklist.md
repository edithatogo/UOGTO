# Article-Hardening Protocol Checklist

| Standard | Item | Required Reporting Element | Repository Artifact | Status |
| --- | --- | --- | --- | --- |
| PRISMA-ScR | Title | Identify the work as a scoping-review-style protocol adapted for ontology comparison. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Rationale | Explain why the completed comparative mapping baseline needs article hardening. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Objectives | State source-discovery, mapping, quality, competency, and article-evidence objectives. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Review questions | Define ontology-comparison and UOGTO-inclusion questions. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Eligibility criteria | Define inclusion and exclusion rules for ontologies, schemas, formalisms, standards, papers, repositories, and metadata-only sources. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Information sources | List registries, repositories, scholarly/archival sources, standards bodies, and baseline UOGTO artifacts. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-S | Search strategy | Define route categories, required search-log fields, and seed query families. | `docs/article-hardening/search-strategy.md` | complete |
| PRISMA-ScR | Selection process | Require inclusion status, screening rationale, evidence level, limitations, and source-family assignment. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Data charting | Define charting fields for source identity, paradigm, source type, licence, provenance, parseability, mapping relevance, and article use. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Data items | Separate evidence levels and required metadata for parsed, structured, metadata-only, literature-only, and excluded sources. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Synthesis | Define reporting dimensions for source discovery, evidence levels, UOGTO module coverage, mappings, quality, validation, and missing elements. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Limitations | Require reporting of search drift, registry differences, licence constraints, and metadata-only evidence limits. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Protocol amendments | Require material protocol changes to be recorded in Conductor runlog and checklist updates. | `.conductor/runlog.md` | complete |
| RO-Crate 1.1 | Root dataset | Define the article-hardening evidence package as a research object. | `docs/article-hardening/search-strategy.md` | complete |
| RO-Crate 1.1 | Data entities | Require protocol, checklist, search logs, inventories, scripts, source artifacts/references, metrics, tables, and figures. | `docs/article-hardening/search-strategy.md` | complete |
| RO-Crate 1.1 | Contextual entities | Require standards, licences, people/organizations where available, and external source references. | `docs/article-hardening/search-strategy.md` | complete |
| UOGTO governance | Missing-element triage | Require evidence-backed add/align/defer/reject/domain-review decisions for missing game-theory elements. | `docs/article-hardening/protocol.md` | complete |

## Reporting Improvements To Preserve

- Distinguish parsed RDF/OWL evidence from structured non-RDF, metadata-only, literature-only, and excluded sources in every table and figure.
- Treat source-discovery counts, mapping confidence, ontology-quality metrics, and UOGTO expansion recommendations as separate claim types.
- Require every proposed UOGTO addition to identify competency-question, interoperability, article-claim, conceptual-clarity, or validation/example impact.
- Keep protocol amendments visible in Conductor state so article methods do not drift from implementation.
