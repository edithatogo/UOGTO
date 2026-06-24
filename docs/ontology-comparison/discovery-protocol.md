# Comparative Simulation Ontology Discovery Protocol

## Purpose
This protocol governs discovery for the UOGTO comparative simulation ontology mapping track. It records where to search, how to search, how to decide whether a source is in scope, and how to handle source licences before artifacts are copied into the repository.

## Search Surfaces
- Ontology registries: LOV, OLS, Ontobee, BioPortal, Bioregistry, FAIRsharing, Wikidata, Linked Open Vocabularies mirrors, and OBO Foundry only for relevant upper/reference ontologies.
- Scholarly search: Google Scholar, Semantic Scholar, Crossref, arXiv, PubMed/Europe PMC for systems-biology simulation standards, and domain conference proceedings for modelling-and-simulation ontology papers.
- Code and artifact repositories: GitHub, GitLab, institutional repositories, Zenodo, Figshare, W3C, OASIS, COMBINE, SISO, EMMC, and standards-body publication pages.
- Project sites: official documentation sites for modelling standards, ontology projects, and simulation frameworks.

## Search Strings
Use these exact starter queries and record additional queries in `inclusion-exclusion-log.jsonl`:

- `"game theory ontology" OWL OR RDF`
- `"game ontology" "OWL" "RDF"`
- `"mechanism design ontology" OR "social choice ontology"`
- `"open games" ontology RDF`
- `"discrete event simulation ontology" OWL OR RDF`
- `"DEVS ontology" OR "DEVS metamodel" ontology`
- `"HLA FOM ontology" OR "High Level Architecture" ontology simulation`
- `"agent based modelling ontology" OR "agent-based modeling ontology"`
- `"ODD protocol" ontology agent based modelling`
- `"system dynamics ontology" "stock flow" ontology`
- `"XMILE" ontology OR schema "system dynamics"`
- `"hybrid simulation ontology" OR "hybrid systems ontology"`
- `"simulation algorithm ontology" KiSAO`
- `"SED-ML" ontology simulation experiment description`
- `"MIASE" ontology simulation experiment`
- `"modelling and simulation ontology" OSMO`
- `"European Materials Modelling Ontology" EMMO`
- `"physics based simulation ontology"`
- `"model execution ontology" provenance simulation`
- `"P-Plan" ontology workflow plan`
- `"PROV-O" simulation provenance ontology`

## Inclusion Rules
Include a source when at least one condition is true:

- It is an OWL/RDF/SKOS ontology or vocabulary for game theory, simulation, model execution, agent systems, system dynamics, or modelling-and-simulation interoperability.
- It is a formal schema, metamodel, or standard with terms that can be mapped to UOGTO concepts even when no RDF artifact exists.
- It is an upper/reference ontology that a candidate source imports or relies on for modelling semantics.
- It is a provenance, plan, observation, time, or algorithm vocabulary directly relevant to executable model semantics.

## Exclusion Rules
Exclude or defer a source when:

- It is only a narrative article with no extractable term inventory.
- It is a software package without a stable vocabulary, schema, or ontology surface.
- It is domain-specific with no meaningful overlap with games, agents, simulation, model execution, provenance, observations, time, or systems modelling.
- The licence forbids redistribution and the source cannot be represented safely as metadata-only.
- The source cannot be retrieved, identified, or cited with enough provenance for audit.

## Licence Dispositions
- `redistributable_artifact`: artifact may be copied into the repo with licence and provenance.
- `metadata_only`: record source metadata and retrieval instructions, but do not copy artifact.
- `transformed_summary_only`: extract limited term metadata or a derived summary only when allowed.
- `excluded`: do not use except for an exclusion rationale.
- `needs_licence_review`: defer harvesting until licence terms are confirmed.

## Review States
- `seeded`: initial candidate added before full source review.
- `included`: source is in scope and can enter term extraction.
- `metadata_only`: source is in scope but artifact is not copied.
- `excluded`: source is out of scope or unusable.
- `needs_review`: source needs human/legal/domain review.

## Evidence Requirements
Every source record must contain:

- Stable `id`, `name`, `family`, `candidate_type`, `source_url`, `discovery_route`, `inclusion_rationale`, and `licence_disposition`.
- `artifact_url` when a formal artifact URL is known.
- `expected_format` and `redistribution_risk`.
- `review_status` and `priority`.
- Notes distinguishing official evidence from inferred relevance.
