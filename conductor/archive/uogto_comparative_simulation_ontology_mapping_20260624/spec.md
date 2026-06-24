# Specification: Comparative Simulation Ontology Mapping

## Purpose
Create an auditable comparative-ontology research and analysis lane for UOGTO. The track must identify relevant existing ontologies, vocabularies, standards, schemas, and semantic models for game theory, discrete-event simulation, agent-based modelling, system dynamics, hybrid simulation, systems biology simulation, modelling-and-simulation interoperability, and adjacent executable/modelling semantics.

The outcome should be a sourced corpus, reproducible mappings to UOGTO, quantitative overlap analysis, network/descriptive analyses, and comprehensive visualisations that make UOGTO's coverage, novelty, and alignment opportunities inspectable.

## Scope
- Discover candidate ontologies and modelling standards from ontology registries, literature, GitHub/GitLab repositories, institutional sites, and standards bodies.
- Source redistributable ontology artifacts into the repository with provenance, licence, retrieval timestamp, checksums, and original URLs.
- Preserve non-redistributable sources as metadata-only records with retrieval instructions and licence rationale.
- Parse RDF/OWL/SKOS artifacts where available; extract structured term inventories from XML schemas, JSON schemas, vocabularies, and documentation when formal RDF is unavailable.
- Map classes, properties, individuals, and modelling constructs to UOGTO using exact IRI matches, label/definition similarity, lexical normalization, hierarchy context, embedding-assisted candidates, and human-reviewed mapping decisions.
- Evaluate overlap and matching by domain area, modelling paradigm, entity type, relation type, and confidence level.
- Analyse ontology networks: import/use relations, shared upper ontologies, alignment graph structure, UOGTO coverage centrality, cluster structure, bridge concepts, orphan areas, and semantic gaps.
- Produce visualisations suitable for maintainers and readers: heatmaps, bipartite alignment graphs, ontology similarity networks, Sankey/domain-flow diagrams, treemaps, coverage dashboards, and static report figures.

## Candidate Source Universe
The implementation must start with, but not be limited to, these seed families:

- Game theory and games: Game Ontology Project, game description language resources, open-game/compositional-game vocabularies, mechanism-design and social-choice vocabularies, multi-agent/game AI schemas, and any formal OWL/RDF game-theory ontologies found in LOV, OLS, BioPortal, Ontobee, Wikidata, GitHub, Zenodo, and scholarly search.
- Discrete-event and hybrid simulation: DEVS/DESS/DEVS-Suite related ontologies, HLA/FOM semantic models, DEVS metamodel work, event/process ontologies, and hybrid modelling ontologies.
- Agent-based modelling: ODD/ODD+D semantic resources, ABM model description ontologies, multi-agent system ontologies, KAoS-like agent/policy ontologies where relevant, and agent simulation provenance schemas.
- System dynamics: stock-flow/system-dynamics vocabularies, XMILE/STELLA/Vensim semantic schemas where mappable, causal-loop and feedback-loop ontologies, and model-experiment metadata schemas.
- Simulation experiment and algorithm standards: KiSAO, SED-ML, MIASE, COMBINE-related ontologies, SBO/TEDDY where directly relevant to simulation algorithms or model behaviour.
- General modelling and simulation interoperability: OSMO, EMMO and related VIMMP/marketplace ontologies, Physics-based Simulation Ontology, domain-independent model/execution/provenance ontologies, P-Plan, PROV-O, SSN/SOSA where simulation observation/execution semantics overlap.
- Upper/reference ontologies used by sources: BFO, DOLCE, UFO/OntoUML, EMMO top-level modules, schema.org, SKOS, OWL-Time, and other upper ontologies only insofar as they affect mapping and overlap interpretation.

## Out of Scope
- Blindly importing third-party ontologies into UOGTO semantics without licence/provenance review.
- Treating XML/JSON standards as OWL ontologies unless a documented transformation is created.
- Claiming a source is fully covered by UOGTO solely from lexical similarity.
- Expanding UOGTO itself before the overlap/gap analysis is complete and reviewed.
- Publishing large non-redistributable third-party artifacts in the repository.

## Required Repository Outputs
- `docs/ontology-comparison/source-inventory.md`
- `docs/ontology-comparison/source-inventory.json`
- `docs/ontology-comparison/inclusion-exclusion-log.jsonl`
- `docs/ontology-comparison/term-inventory.parquet` or an equivalent reproducible tabular artifact.
- `docs/ontology-comparison/mapping-candidates.jsonl`
- `docs/ontology-comparison/mapping-review.csv`
- `docs/ontology-comparison/accepted-alignments.ttl`
- `docs/ontology-comparison/overlap-metrics.json`
- `docs/ontology-comparison/network-analysis.json`
- `docs/ontology-comparison/report.md`
- `docs/ontology-comparison/figures/` for static images.
- `docs/ontology-comparison/dashboard/` or a generated HTML report for interactive review if feasible.
- Tests and scripts under `scripts/maintenance/` and `tests/` that rebuild and validate the above.

## Success Criteria
- Discovery coverage is reproducible and records query strings, registries searched, repositories inspected, and inclusion/exclusion decisions.
- Every sourced artifact has provenance, licence, retrieval timestamp, checksum, and parse status.
- Every accepted mapping records source term, UOGTO target, mapping predicate, evidence, confidence, and review status.
- Overlap metrics distinguish exact, close, broad/narrow, related, no-match, and out-of-scope cases.
- Network and descriptive analyses identify high-overlap areas, low-overlap/gap areas, UOGTO-unique areas, and candidate future alignment modules.
- Visualisations are regenerated from data and checked into the repo only as generated artifacts when appropriate.
- `make validate` and `make test` pass after implementation.
