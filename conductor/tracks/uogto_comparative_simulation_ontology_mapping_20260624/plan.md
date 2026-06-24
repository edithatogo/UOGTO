# Implementation Plan: Comparative Simulation Ontology Mapping

This track discovers, sources, maps, analyses, and visualises external game-theory and simulation/modelling ontologies against UOGTO. It starts from public registry/literature/repository discovery and ends with reproducible reports, figures, and reviewed alignments.

## Phase 1: Discovery Protocol and Seed Inventory
- [x] Task: Define the discovery protocol.
    - [x] Create `docs/ontology-comparison/discovery-protocol.md` with registry, repository, literature, and standards-body search routes.
    - [x] Include exact search strings for game theory, discrete-event simulation, agent-based modelling, system dynamics, hybrid simulation, simulation algorithms, modelling-and-simulation interoperability, and executable model semantics.
    - [x] Define inclusion/exclusion rules for ontologies, vocabularies, schemas, metamodels, and narrative-only standards.
    - [x] Define licence categories: redistributable artifact, metadata-only, transformed summary only, and excluded.
- [x] Task: Build the seed candidate list.
    - [x] Seed candidates from Game Ontology Project, game description language resources, open-game/compositional-game vocabularies, DEVS/HLA/FOM resources, ODD/ABM resources, XMILE/system-dynamics resources, KiSAO, SED-ML, MIASE, COMBINE-related resources, OSMO, EMMO/VIMMP, Physics-based Simulation Ontology, P-Plan, PROV-O, SSN/SOSA, OWL-Time, schema.org, BFO, DOLCE, UFO/OntoUML, and other discovered adjacent sources.
    - [x] Record source URLs, candidate type, expected artifact format, licence hints, and discovery route in `docs/ontology-comparison/source-inventory.json`.
    - [x] Add `scripts/maintenance/build_ontology_comparison_inventory.py`, `make ontology-comparison-inventory`, and pytest coverage for deterministic validation/rendering.

### Acceptance Criteria
- [x] Discovery protocol records all search surfaces and query strings.
- [x] Source inventory contains seed candidates with source URLs and initial inclusion rationale.
- [x] Inclusion/exclusion log exists and is append-only.

## Phase 2: Source Harvesting and Provenance
- [x] Task: Implement source harvesting.
    - [x] Add `scripts/maintenance/harvest_comparison_sources.py`.
    - [x] Download redistributable RDF/OWL/SKOS artifacts into `docs/ontology-comparison/sources/` or a clearly named subfolder.
    - [x] Store non-redistributable sources as metadata-only records with retrieval URL, licence rationale, and manual review note.
    - [x] Record retrieval timestamp, HTTP status, content type, checksum, byte size, and canonical URL.
- [x] Task: Validate parseability and source integrity.
    - [x] Parse RDF/OWL/SKOS with RDFLib.
    - [x] Detect XML schemas, JSON schemas, CSV vocabularies, and documentation-only sources.
    - [x] Produce `docs/ontology-comparison/source-inventory.md` from the JSON inventory.
    - [x] Add `docs/ontology-comparison/source-provenance.json`, `make ontology-comparison-harvest`, Pixi wiring, and pytest coverage for downloaded and metadata-only provenance paths.

### Acceptance Criteria
- [x] Every source has provenance and licence disposition.
- [x] Redistributable artifacts have checksums and parse status.
- [x] Non-RDF standards are not misrepresented as ontologies.

## Phase 3: Term Extraction and Normalisation
- [x] Task: Implement term extraction.
    - [x] Add `scripts/maintenance/extract_comparison_terms.py`.
    - [x] Extract classes, properties, individuals, SKOS concepts, labels, definitions, comments, synonyms, parent/child context, domains/ranges, imports, and ontology metadata.
    - [x] Extract structured terms from XML/JSON schemas and formal documentation where RDF is unavailable.
- [x] Task: Normalise term inventories.
    - [x] Canonicalise labels, split identifiers, lowercase tokens, remove stopwords, preserve symbols and acronyms, and record source language.
    - [x] Emit `docs/ontology-comparison/term-inventory.parquet` or a deterministic JSONL/CSV fallback.
    - [x] Wire `make ontology-comparison-terms`, Pixi support, generated `docs/ontology-comparison/term-inventory.jsonl`, and pytest coverage.

### Acceptance Criteria
- [x] UOGTO and all included external sources have comparable term inventories.
- [x] Extraction preserves provenance from source artifact to term row.
- [x] Tests cover RDF and non-RDF extraction fixtures.

## Phase 4: Mapping Candidate Generation
- [x] Task: Generate mapping candidates.
    - [x] Add `scripts/maintenance/generate_ontology_mapping_candidates.py`.
    - [x] Compute exact IRI, exact label, normalized label, synonym, definition, hierarchy-context, property-signature, and embedding-assisted candidates.
    - [x] Emit `docs/ontology-comparison/mapping-candidates.jsonl`.
- [x] Task: Score and classify candidates.
    - [x] Score candidates by lexical similarity, definition similarity, structural context, domain/range compatibility, and source reliability.
    - [x] Classify candidate predicates: `skos:exactMatch`, `skos:closeMatch`, `skos:broadMatch`, `skos:narrowMatch`, `skos:relatedMatch`, `owl:equivalentClass`, `owl:equivalentProperty`, `rdfs:subClassOf`, `rdfs:subPropertyOf`, and `no_match`.
    - [x] Wire `make ontology-comparison-mappings`, Pixi support, generated `docs/ontology-comparison/mapping-candidates.jsonl`, and pytest coverage.

### Acceptance Criteria
- [x] Candidate generation is deterministic for a fixed source inventory.
- [x] Each candidate includes evidence features and confidence score.
- [x] Low-confidence and high-impact mappings are flagged for review.

## Phase 5: Human-Review Workflow and Accepted Alignments
- [x] Task: Create review artifacts.
    - [x] Emit `docs/ontology-comparison/mapping-review.csv` with candidate evidence and decision columns.
    - [x] Define review statuses: `accepted`, `rejected`, `needs_domain_review`, `out_of_scope`, and `defer_until_source_clarified`.
- [x] Task: Build accepted alignment outputs.
    - [x] Add `scripts/maintenance/build_comparison_alignments.py`.
    - [x] Generate `docs/ontology-comparison/accepted-alignments.ttl` from reviewed mappings.
    - [x] Validate alignment TTL with RDFLib and check that mapping predicates are from approved namespaces.
    - [x] Wire `make ontology-comparison-alignments`, Pixi support, generated review/alignment artifacts, and pytest coverage.

### Acceptance Criteria
- [x] Accepted mappings are review-backed and machine-readable.
- [x] Rejected mappings preserve rationale for auditability.
- [x] Alignment TTL parses and uses stable UOGTO IRIs.

## Phase 6: Overlap and Descriptive Analysis
- [x] Task: Compute overlap metrics.
    - [x] Add `scripts/maintenance/analyse_ontology_overlap.py`.
    - [x] Compute source-by-UOGTO overlap counts, precision-review summaries, term-type coverage, domain-module coverage, unmatched-source concepts, UOGTO-unique concepts, and source-cluster overlap.
    - [x] Emit `docs/ontology-comparison/overlap-metrics.json`.
- [x] Task: Produce descriptive summaries.
    - [x] Summarise source size, term-type distributions, annotation completeness, hierarchy depth, property density, import count, licence coverage, and parse status.
    - [x] Identify candidate UOGTO enhancement areas and areas where UOGTO already has stronger coverage.
    - [x] Wire `make ontology-comparison-overlap`, Pixi support, generated overlap metrics, and pytest coverage.

### Acceptance Criteria
- [x] Metrics separate source coverage, UOGTO coverage, and bidirectional overlap.
- [x] Outputs identify high-overlap, low-overlap, and no-match areas.
- [x] Tests cover metric calculations on fixtures.

## Phase 7: Network Analysis
- [x] Task: Build ontology and term networks.
    - [x] Add `scripts/maintenance/analyse_ontology_networks.py`.
    - [x] Build source ontology graph, term-alignment bipartite graph, source similarity graph, import/uses graph, and UOGTO module coverage graph.
    - [x] Compute degree, betweenness, closeness, connected components, community clusters, bridge terms, orphan terms, and central source families.
    - [x] Emit `docs/ontology-comparison/network-analysis.json`.
    - [x] Wire `make ontology-comparison-networks`, Pixi support, generated network analysis, and pytest coverage.

### Acceptance Criteria
- [x] Network outputs are deterministic and documented.
- [x] Network analysis distinguishes ontology-level and term-level graphs.
- [x] Results highlight bridge concepts and isolated modelling paradigms.

## Phase 8: Visualisation and Report
- [ ] Task: Generate static figures.
    - [ ] Add `scripts/maintenance/visualise_ontology_comparison.py`.
    - [ ] Generate heatmaps for source/module overlap, bar charts for source sizes and match classes, treemaps for UOGTO coverage, network diagrams for source similarity and mappings, Sankey/domain-flow diagrams for mapping categories, and reviewer workload summaries.
    - [ ] Store figures under `docs/ontology-comparison/figures/`.
- [ ] Task: Generate comprehensive report.
    - [ ] Create `docs/ontology-comparison/report.md`.
    - [ ] Include methodology, source inventory, inclusion/exclusion summary, mapping methods, overlap metrics, network findings, visualisations, and recommended UOGTO follow-up work.
    - [ ] Optionally create `docs/ontology-comparison/dashboard/` with a static HTML dashboard if dependencies are available and maintainable.

### Acceptance Criteria
- [ ] Report is reproducible from source inventory and mapping artifacts.
- [ ] Visualisations are readable in static GitHub rendering and, if generated, in the dashboard.
- [ ] Report clearly separates evidence-backed mappings from candidate/future work.

## Phase 9: CI, Release, and Conductor Integration
- [ ] Task: Add validation and tests.
    - [ ] Add Make/Pixi tasks for source inventory validation, term extraction, mapping generation, overlap analysis, network analysis, visualisation generation, and report checks.
    - [ ] Add pytest coverage for inventory schema, extraction, mapping scoring, alignment TTL generation, overlap metrics, network metrics, and report existence.
    - [ ] Ensure `make validate` and `make test` pass.
- [ ] Task: Update documentation and Conductor state.
    - [ ] Link the comparison report from registry/release docs if useful.
    - [ ] Update `.conductor/status.md`, `.conductor/runlog.md`, and this plan as each phase completes.
    - [ ] Archive the track only after reviewed alignments, analyses, visualisations, and validation gates pass.

### Acceptance Criteria
- [ ] CI/local tests cover all generated artifacts.
- [ ] Conductor status accurately reports implementation progress and remaining review work.
- [ ] Completed artifacts are committed and pushed.
