# Article-Hardening Protocol Checklist

| Standard | Item | Required Reporting Element | Repository Artifact | Status |
| --- | --- | --- | --- | --- |
| PRISMA-ScR | Title | Identify the work as a scoping-review protocol adapted for ontology comparison. | `docs/article-hardening/protocol.md`; `docs/article-hardening/structured-summary.md`; `docs/article-hardening/prisma-scr-artifact-map.md` | complete |
| PRISMA-ScR | Structured summary | Provide a structured summary that states background, objectives, eligibility, sources, charting, synthesis, and evidence-package scope. | `docs/article-hardening/structured-summary.md` | complete |
| PRISMA-ScR | Rationale | Explain why the completed comparative mapping baseline needs article hardening. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Objectives | State source-discovery, mapping, quality, competency, and article-evidence objectives. | `docs/article-hardening/protocol.md` | complete |
| PRISMA-ScR | Protocol and registration | Record the protocol standard, governance surface, and repository registration context. | `docs/article-hardening/protocol.md`; `conductor/tracks/uogto_article_hardening_protocol_20260624/protocol-standard.md`; `docs/article-hardening/ro-crate-metadata.json` | complete |
| PRISMA-ScR | Eligibility criteria | Define inclusion and exclusion rules for ontologies, schemas, formalisms, standards, papers, repositories, and metadata-only sources. | `docs/article-hardening/protocol.md`; `docs/article-hardening/source-extension-inventory.json`; `docs/article-hardening/uogto-inclusion-decisions.md` | complete |
| PRISMA-ScR | Information sources | List registries, repositories, scholarly/archival sources, standards bodies, and baseline UOGTO artifacts. | `docs/article-hardening/protocol.md`; `docs/article-hardening/search-strategy.md`; `docs/article-hardening/search-log.jsonl`; `docs/article-hardening/source-extension-inventory.md` | complete |
| PRISMA-ScR | Search | Define route categories, required search-log fields, and seed query families. | `docs/article-hardening/search-strategy.md`; `docs/article-hardening/search-log.jsonl` | complete |
| PRISMA-ScR | Selection of sources of evidence | Capture inclusion status, screening rationale, evidence level, limitations, and source-family assignment. | `docs/article-hardening/source-extension-inventory.json`; `docs/article-hardening/source-extension-inventory.md`; `docs/article-hardening/manual-review-sample.csv`; `docs/article-hardening/reviews/phase-review-log.jsonl`; `docs/article-hardening/uogto-inclusion-decisions.md` | complete |
| PRISMA-ScR | Data charting process | Define charting fields for source identity, paradigm, source type, licence, provenance, parseability, mapping relevance, and article use. | `docs/article-hardening/protocol.md`; `docs/article-hardening/quality-metrics.json`; `docs/article-hardening/source-extension-inventory.json` | complete |
| PRISMA-ScR | Data items | Separate evidence levels and required metadata for parsed, structured, metadata-only, literature-only, and excluded sources. | `docs/article-hardening/protocol.md`; `docs/article-hardening/quality-metrics.json`; `docs/article-hardening/case-studies.json` | complete |
| PRISMA-ScR | Critical appraisal of individual sources of evidence | Optional appraisal slot for source-level quality or reasoner review when performed. | `docs/article-hardening/reasoner-report.md`; `docs/article-hardening/robot/report.md`; `docs/article-hardening/robot/reasoner-check.md`; `docs/article-hardening/quality-metrics.json` | optional |
| PRISMA-ScR | Synthesis of results | Define reporting dimensions for source discovery, evidence levels, UOGTO module coverage, mappings, quality, validation, and missing elements. | `docs/article-hardening/protocol.md`; `docs/article-hardening/article-tables/`; `docs/article-hardening/figures/`; `docs/article-hardening/case-studies.md`; `docs/article-hardening/quality-metrics.json` | complete |
| PRISMA-ScR | Selection of sources of evidence | Report selection counts, exclusions, and reviewer decisions. | `docs/article-hardening/search-log.jsonl`; `docs/article-hardening/manual-review-sample.csv`; `docs/article-hardening/reviews/phase-review-log.jsonl`; `docs/article-hardening/uogto-inclusion-decisions.md` | complete |
| PRISMA-ScR | Characteristics of sources of evidence | Summarise the evidence base by source family, paradigm, licence, parseability, and mapability. | `docs/article-hardening/source-extension-inventory.json`; `docs/article-hardening/source-extension-inventory.md`; `docs/article-hardening/case-studies.json`; `docs/article-hardening/quality-metrics.json` | complete |
| PRISMA-ScR | Critical appraisal within sources of evidence | Optional within-source appraisal slot for ontology quality, merge-diff, and import-extraction review. | `docs/article-hardening/reasoner-report.md`; `docs/article-hardening/robot/merge-diff.md`; `docs/article-hardening/robot/import-extraction.md` | optional |
| PRISMA-ScR | Results of individual sources of evidence | Provide per-source outcomes, mapping status, and key extracted descriptors. | `docs/article-hardening/source-extension-inventory.md`; `docs/article-hardening/case-studies.md`; `docs/article-hardening/article-tables/` | complete |
| PRISMA-ScR | Synthesis of results | Summarise mapping overlap, coverage, network structure, quality, and article-ready claims. | `docs/article-hardening/article-tables/`; `docs/article-hardening/figures/`; `docs/article-hardening/quality-metrics.json`; `docs/article-hardening/use-case-coverage-matrix.csv` | complete |
| PRISMA-ScR | Summary of evidence | Provide a concise package-level evidence summary for the article and protocol bundle. | `docs/article-hardening/structured-summary.md`; `docs/article-hardening/case-studies.md`; `docs/article-hardening/article-tables/`; `docs/article-hardening/figures/` | complete |
| PRISMA-ScR | Limitations | Require reporting of search drift, registry differences, licence constraints, and metadata-only evidence limits. | `docs/article-hardening/protocol.md`; `docs/article-hardening/source-extension-inventory.md`; `docs/article-hardening/reasoner-report.md` | complete |
| PRISMA-ScR | Conclusions | State the protocol-level conclusion about what the evidence package can support and where judgment remains needed. | `docs/article-hardening/protocol.md`; `docs/article-hardening/structured-summary.md`; `docs/article-hardening/prisma-scr-artifact-map.md` | complete |
| PRISMA-ScR | Funding | Record funding and conflict status for the evidence package. | `docs/article-hardening/protocol.md`; `docs/article-hardening/ro-crate-metadata.json` | complete |

## Related Package Surfaces

- Distinguish parsed RDF/OWL evidence from structured non-RDF, metadata-only, literature-only, and excluded sources in every table and figure.
- Treat source-discovery counts, mapping confidence, ontology-quality metrics, and UOGTO expansion recommendations as separate claim types.
- Require every proposed UOGTO addition to identify competency-question, interoperability, article-claim, conceptual-clarity, or validation/example impact.
- Preserve ROBOT-style outputs as optional article-hardening enrichments; never let them replace the portable RDFLib/pySHACL baseline.
- Keep protocol amendments visible in Conductor state so article methods do not drift from implementation.
## Supporting Standards

| Standard | Item | Required Reporting Element | Repository Artifact | Status |
| --- | --- | --- | --- | --- |
| RO-Crate 1.1 | Root dataset | Define the article-hardening evidence package as a research object. | `docs/article-hardening/ro-crate-metadata.json` | complete |
| RO-Crate 1.1 | Data entities | Include protocol, checklist, logs, inventories, benchmarks, tables, figures, and scripts. | `docs/article-hardening/ro-crate-metadata.json` | complete |
| RO-Crate 1.1 | Contextual entities | Capture standards, licences, organizations, and external source references. | `docs/article-hardening/ro-crate-metadata.json` | complete |
| UOGTO governance | Missing-element triage | Record add/align/defer/reject/domain-review decisions. | `docs/article-hardening/uogto-inclusion-decisions.md`; `docs/article-hardening/uogto-inclusion-candidates.csv` | complete |
| UOGTO governance | Phase review agents | Require peer, editorial, red-team, and devil's-advocate reviewers. | `conductor/agents/article-hardening-review-agents.json`; `conductor/workflows/article-hardening-phase-review.md` | complete |
| UOGTO governance | Phase research agents | Require discovery, standards, evidence-curation, gap-analysis, and reproducibility researchers. | `conductor/agents/article-hardening-research-agents.json`; `conductor/workflows/article-hardening-research-workflow.md` | complete |- Protocol amendments are recorded in `.conductor/runlog.md`.



## Supporting Review Surfaces

| Standard | Item | Required Reporting Element | Repository Artifact | Status |
| --- | --- | --- | --- | --- |
| UOGTO governance | Dual screening and adjudication | Record researcher proposal, peer acceptance/rejection, red-team challenge, and final disposition. | `docs/article-hardening/dual-screening.md`; `docs/article-hardening/dual-screening-sample.csv` | complete |

## PRISMA 2020 Flow Diagrams

| Standard | Item | Required Reporting Element | Repository Artifact | Status |
| --- | --- | --- | --- | --- |
| PRISMA 2020 | Source discovery flow diagram | Present search-route, record-identification, and negative-evidence discovery paths in PRISMA 2020 style. | `docs/article-hardening/figures/prisma-2020-source-discovery-flow.md` | complete |
| PRISMA 2020 | Screening flow diagram | Present screening, inclusion, exclusion, and negative-evidence disposition in PRISMA 2020 style. | `docs/article-hardening/figures/prisma-2020-screening-flow.md` | complete |
