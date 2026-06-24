# Article-Hardening Search Strategy

## Purpose
This search strategy records the PRISMA-S reporting fields, search route taxonomy, seed query families, and RO-Crate packaging expectations for the UOGTO article-hardening track.

## PRISMA-S Search Log Fields
Each line in `docs/article-hardening/search-log.jsonl` must include the standard PRISMA-S route fields plus the stricter living-register fields needed for append-only evidence review:

- `searched_at`: ISO 8601 date or datetime.
- `record_id`: stable append-only search-event identifier.
- `surface`: searched registry, repository, database, website, or standards source.
- `surface_type`: one of `ontology_registry`, `scholarly_index`, `archive`, `repository`, `standards_body`, `project_site`, `web_search`, or `baseline_artifact`.
- `query`: exact query string, API request, URL, or manual browsing route.
- `filters`: date, field, language, file-type, licence, or result filters used.
- `result_count`: result count when available, otherwise `null`.
- `screened_count`: number of results inspected.
- `included_count`: number of sources added or retained.
- `route_limitations`: known limitations, authentication boundaries, unstable ranking, pagination limits, or API constraints.
- `operator_notes`: short notes on interpretation, duplicates, or manual judgement.
- `source_ids_added`: list of source identifiers added to the inventory.
- `evidence_level`: strongest evidence level represented by included sources on this route.
- `screening_decision`: route-level inclusion, exclusion, duplicate, or deferral decision.
- `inclusion_rationale`: reason the route or source family belongs in the article-hardening evidence package.
- `licence`: route-level licence disposition or pointer to per-source licence dispositions.
- `reviewer_handoff`: assigned research/review roles and next action.
- `previous_record_hash`: prior JSONL record hash for append-only chain validation.
- `record_hash`: SHA-256 hash over the record payload excluding `record_hash`.

## Search Route Taxonomy
Search routes must be grouped by:

- `baseline_artifact`: completed `docs/ontology-comparison/` outputs.
- `ontology_registry`: LOV, OLS, BioPortal, Ontobee, Bioregistry, FAIRsharing, Wikidata, and discovered domain registries.
- `scholarly_index`: Crossref, Semantic Scholar, arXiv, ACM/IEEE landing pages, Google Scholar-style manual searches when used, and institutional bibliographic pages.
- `archive`: Zenodo, OSF, Figshare, institutional repositories, release archives, and persistent identifier landing pages.
- `repository`: GitHub, GitLab, SourceForge, package repositories, standards-body repositories, and project release pages.
- `standards_body`: W3C, OMG, IEEE, COMBINE, SBML, CellML, SBGN, SED-ML, KiSAO, MIASE, DEVS, HLA/FOM, XMILE, BPMN, Petri net, timed/hybrid automata, OSMO, EMMO, and VIMMP sources.
- `project_site`: project documentation for Ludii, Game Description Language variants, Game Ontology Project, General Video Game AI, and other discovered game or simulation resources.
- `web_search`: targeted public web searches used only when registry/repository/standards routes are insufficient.

## Seed Query Families
Use exact strings or documented variants for:

- `"game theory ontology" OWL RDF`
- `"game ontology" "game theory" ontology`
- `"open games" ontology compositional game theory`
- `"mechanism design" ontology OR vocabulary`
- `"social choice" ontology OR vocabulary`
- `"Game Description Language" ontology OR schema`
- `"GDL-II" "GDL-III" "GDLZ" game description`
- `Ludii game description language ontology schema`
- `"discrete event simulation" ontology DEVS OWL`
- `"HLA" "FOM" ontology simulation`
- `"agent based modelling" ontology ODD ODD+D`
- `"system dynamics" ontology "stock flow" XMILE`
- `"Petri net" ontology OWL`
- `"BPMN" ontology OWL process`
- `"timed automata" ontology OR "hybrid automata" ontology`
- `SBO SBML CellML SBGN SED-ML KiSAO MIASE ontology simulation`
- `OSMO EMMO VIMMP simulation ontology`
- `PROV-O P-Plan OWL-Time SSN SOSA simulation provenance`
- `OWL-S process ontology action planning`

## Reporting Rules
Reports must separate:

- Search route counts from source-family counts.
- Included sources from excluded and duplicate sources.
- Parsed RDF/OWL artifacts from structured non-RDF standards and metadata-only sources.
- Mapping evidence from ontology-expansion recommendations.
- UOGTO additions from external-alignment-only recommendations.

## RO-Crate Packaging Requirements
The future `docs/article-hardening/ro-crate-metadata.json` must describe:

- Root dataset: the UOGTO article-hardening evidence package.
- Data entities: protocol, checklist, search strategy, search log, source inventories, scripts, retrieved redistributable artifacts, generated metrics, tables, figures, reports, and validation outputs.
- Contextual entities: UOGTO, relevant standards, source registries, licences, software tools, authors/contributors where known, and external URLs for metadata-only sources.
- Provenance relations: generated artifacts should identify the script or source artifact used to create them.
- Access rights: non-redistributable or metadata-only sources must be referenced but not copied.

## Reporting Risks
- Registry and web search rankings may drift.
- Some relevant standards are not machine-readable ontologies.
- Metadata-only sources can support discovery and contextual claims, but not term-level mapping claims.
- Future article text must not imply full UOGTO coverage from lexical similarity alone.

## Negative Evidence

Search routes that return no relevant ontology or formalism should be recorded as `negative_evidence_no_relevant_ontology_found` with `included_count` equal to zero and `source_ids_added` empty. These routes are valid article evidence because they delimit what was searched and not found. 
