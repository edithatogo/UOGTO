# Implementation Plan: UOGTO Article Hardening Protocol

This track turns the completed comparative ontology baseline into a broader publication-grade protocol and evidence package. It is intentionally comprehensive; later phases may narrow individual source families after the protocol and feasibility evidence are in place.

## Phase 1: Standards-Based Protocol
- [x] Task: Create the protocol scaffold.
    - [x] Create `docs/article-hardening/protocol.md` as a PRISMA-ScR-aligned scoping-review protocol adapted for ontology and modelling-formalism comparison.
    - [x] Create `docs/article-hardening/protocol-checklist.md` mapping PRISMA-ScR items to repo artifacts and implementation status.
    - [x] Record PRISMA-S search-reporting fields for each search route.
    - [x] Record RO-Crate 1.1 packaging requirements for the track outputs.
- [x] Task: Define eligibility and charting rules.
    - [x] Define inclusion/exclusion rules for OWL/RDF ontologies, SKOS vocabularies, XML/JSON schemas, formal modelling languages, narrative standards, papers, software repositories, and metadata-only sources.
    - [x] Define charting fields for source family, modelling paradigm, source type, licence, provenance, artifact availability, parseability, mapping relevance, and article-use category.
    - [x] Define confidence categories for parsed artifact evidence, structured non-RDF evidence, metadata-only evidence, and literature-only evidence.

### Acceptance Criteria
- [x] Protocol includes rationale, objectives, information sources, search strategy, eligibility criteria, charting fields, synthesis plan, limitations, and reproducibility plan.
- [x] Protocol checklist has one row per required standard item and points to target artifacts.
- [x] Protocol explains how PRISMA-ScR, PRISMA-S, and RO-Crate are being used.

## Phase 2: Broader Source Discovery
- [ ] Task: Extend the discovery search.
    - [ ] Search ontology registries: LOV, OLS, BioPortal, Ontobee, Bioregistry, FAIRsharing, Wikidata, and relevant domain registries.
    - [ ] Search scholarly and archival sources: Crossref, Semantic Scholar, arXiv, Zenodo, OSF, ACM/IEEE landing pages where publicly available, and institutional standards pages.
    - [ ] Search repository surfaces: GitHub, GitLab, SourceForge where relevant, standards-body repositories, and project documentation sites.
    - [ ] Search game description and game AI resources: GDL, GDL-II/GDL-III/GDLZ, Ludii, General Video Game AI, Game Ontology Project, and procedural game-description schemas.
    - [ ] Search modelling and simulation resources: DEVS, HLA/FOM, ODD/ABM, XMILE, Petri net, BPMN/process, timed/hybrid automata, SBO/SBML/CellML/SBGN/SED-ML/KiSAO/MIASE/TEDDY, OSMO, EMMO, VIMMP, and physics-based simulation ontologies.
- [x] Task: Build the extended inventory.
    - [x] Create `docs/article-hardening/search-strategy.md`.
    - [x] Create append-only `docs/article-hardening/search-log.jsonl`.
    - [x] Create `docs/article-hardening/source-extension-inventory.json` and generated Markdown summary.
    - [x] Preserve the completed comparative mapping inventory as the baseline and explicitly mark newly added candidates.

Phase 2 note: the living evidence register is implemented with deterministic seed records and hash validation; live registry/API searches remain append-only follow-up records before Phase 3 acquisition.

### Acceptance Criteria
- [x] Each search route records query string, date, surface, result count where available, screening decision, and limitations.
- [x] Every new candidate has a source-family assignment and eligibility rationale.
- [x] Metadata-only and non-redistributable sources are labelled as such.

## Phase 3: Source Acquisition and Reproducible Packaging
- [ ] Task: Acquire permissible artifacts.
    - [ ] Download redistributable RDF/OWL/SKOS/XML/JSON artifacts into a clearly named article-hardening source folder.
    - [ ] Record checksums, retrieval timestamps, content types, canonical URLs, licence disposition, and parse status.
    - [ ] Record metadata-only sources without copying restricted material.
- [ ] Task: Build an RO-Crate package.
    - [ ] Generate `docs/article-hardening/ro-crate-metadata.json`.
    - [ ] Include protocol, inventories, search logs, scripts, source artifacts or source references, derived tables, figures, and reports in the crate graph.
    - [ ] Validate that each crate entity has type, name, provenance, and licence or access-rights metadata where available.

### Acceptance Criteria
- [ ] Source acquisition is deterministic for publicly retrievable artifacts.
- [ ] RO-Crate metadata validates structurally and references all primary outputs.
- [ ] Restricted or metadata-only sources are represented without republishing prohibited content.

## Phase 4: Ontology Quality and Formal-Reasoning Evaluation
- [x] Task: Add ontology-quality metrics.
    - [x] Measure annotation completeness, missing labels/definitions, class/property counts, object/datatype property balance, hierarchy depth, import depth, relation richness, domain/range use, module coverage, and orphan concepts.
    - [x] Add OOPS-style pitfall checks where feasible without depending on external services.
    - [x] Compare UOGTO metrics against parsed external RDF/OWL sources and summarize non-RDF sources separately.
- [x] Task: Add reasoner and validation checks.
    - [x] Run RDFLib parse checks, OWL profile/consistency checks where feasible, SHACL validation for UOGTO examples, and mapping TTL validation.
    - [x] Produce `docs/article-hardening/quality-metrics.json` and `docs/article-hardening/reasoner-report.md`.
    - [x] Produce ROBOT-style ontology reports when Java tooling is available, keeping RDFLib/pySHACL as the portable baseline.
        - [x] Emit `docs/article-hardening/robot/status.json`, `reasoner-check.md`, `report.md`, `merged-ontology.ttl`, `merge-diff.md`, `import-extraction.ttl`, and `import-extraction.md`.

Phase 4 note: quality benchmarking currently covers UOGTO local ontology artifacts, local OOPS-style proxy indicators, SHACL/example/query coverage, and OWL/RDFS status; external comparator metrics will be added after Phase 3 acquisition expands parsed artifacts.

### Acceptance Criteria
- [x] Metrics distinguish UOGTO, parsed external ontologies, structured non-RDF sources, and metadata-only sources.
- [x] Reasoner/validation limitations are explicit.
- [x] Tests cover metric schema and deterministic report generation.

## Phase 5: Competency Questions and Use-Case Benchmarking
- [ ] Task: Define article-relevant competency questions.
    - [ ] Create competency questions for classical games, cooperative games, incomplete-information games, dynamic games, mechanism design, agent-based simulation, system dynamics, discrete-event simulation, multi-agent reinforcement learning, executable traces, and ontology alignment.
    - [ ] Map each competency question to UOGTO modules, example data, SPARQL queries, and comparator-source evidence where available.
- [ ] Task: Build use-case coverage matrices.
    - [ ] Create `docs/article-hardening/competency-benchmark.md`.
    - [ ] Create `docs/article-hardening/use-case-coverage-matrix.csv`.
    - [ ] Score coverage by exact support, partial support, adjacent support, metadata-only evidence, no support, and not applicable.

### Acceptance Criteria
- [ ] Competency questions are executable where UOGTO examples exist.
- [ ] Coverage matrix is reproducible and separates evidence level from interpretive score.
- [ ] Article recommendations cite concrete benchmark gaps.

## Phase 6: Mapping Robustness and Manual Review Sampling
- [ ] Task: Harden mapping methods.
    - [ ] Re-run or extend deterministic mapping candidate generation for newly included parsed sources.
    - [ ] Add ablation summaries for exact labels, normalized labels, definitions, hierarchy context, property signatures, and optional embeddings.
    - [ ] Calibrate mapping-confidence thresholds against accepted/rejected examples from the completed comparison baseline.
- [ ] Task: Add manual review sample.
    - [ ] Create `docs/article-hardening/manual-review-sample.csv`.
    - [ ] Sample high-confidence, borderline, low-confidence, high-impact, and no-match candidates across source families.
    - [ ] Record reviewer decision, rationale, uncertainty, and article-use implication.

### Acceptance Criteria
- [ ] Mapping robustness outputs explain which features materially affect candidate rankings.
- [ ] Manual-review sample is balanced across source families and confidence bands.
- [ ] Accepted claims in the article evidence package are review-backed.

## Phase 7: UOGTO Inclusion Decisions for Missing Game-Theory Elements
- [ ] Task: Identify missing or under-modelled game-theory elements.
    - [ ] Compare UOGTO against parsed and metadata-only game-theory ontology/formalism sources for absent classes, properties, axioms, relation patterns, metadata conventions, and modelling constructs.
    - [ ] Classify gaps by domain: normal-form games, extensive-form games, cooperative games, Bayesian/epistemic games, stochastic/dynamic games, mechanism design, social choice, open games/compositional games, game description languages, equilibrium/refinement concepts, and computational/game-AI constructs.
    - [ ] Create `docs/article-hardening/uogto-inclusion-candidates.csv` with source evidence, candidate UOGTO term, gap type, affected module, competency-question impact, interoperability impact, modelling risk, and proposed disposition.
- [ ] Task: Decide whether each candidate should be included in UOGTO.
    - [ ] Define decision categories: `add_to_uogto`, `align_external_only`, `defer_pending_evidence`, `reject_as_duplicate`, `reject_out_of_scope`, and `requires_domain_review`.
    - [ ] Create `docs/article-hardening/uogto-inclusion-decisions.md` summarising accepted additions, deferred candidates, rejected candidates, rationale, and required ontology module changes.
    - [ ] For `add_to_uogto` candidates, specify required class/property names, labels, SKOS definitions, SHACL/example/test impacts, and migration or backwards-compatibility risks before implementation.

### Acceptance Criteria
- [ ] Every material missing game-theory element has a recorded evidence source and decision rationale.
- [ ] Inclusion recommendations distinguish ontology expansion from external alignment-only mappings.
- [ ] No UOGTO expansion is proposed without a competency-question, interoperability, article-claim, or conceptual-clarity justification.

## Phase 8: Article Tables, Figures, and Narrative Evidence
- [ ] Task: Generate article-ready tables.
    - [ ] Produce source-family table, eligibility table, quality-metrics table, use-case coverage table, mapping-overlap table, and limitations/threats-to-validity table.
    - [ ] Store generated tables under `docs/article-hardening/article-tables/`.
- [ ] Task: Generate article-ready figures.
    - [ ] Produce PRISMA-style flow diagram, source-family coverage chart, ontology-quality comparison chart, coverage heatmap, mapping robustness figure, source similarity/network figure, and evidence-level breakdown.
    - [ ] Store generated figures under `docs/article-hardening/figures/`.
- [ ] Task: Draft article-methods and results inserts.
    - [ ] Produce methods text for protocol, search, eligibility, charting, mapping, quality evaluation, reasoner checks, and synthesis.
    - [ ] Produce results text that explicitly separates reproducible findings from limitations and future work.

### Acceptance Criteria
- [ ] Tables and figures are generated from checked-in data artifacts.
- [ ] Narrative inserts cite artifact paths and avoid overclaiming metadata-only sources.
- [ ] Figures render in GitHub and are suitable for manuscript adaptation.

## Phase 9: Validation, Documentation, and Conductor Integration
- [ ] Task: Add validation tasks and tests.
    - [ ] Add Make/Pixi targets for protocol validation, extended inventory checks, source acquisition checks, RO-Crate validation, quality metrics, competency benchmarks, mapping robustness, and article artifact generation.
    - [ ] Add pytest coverage for schemas, deterministic generation, and required report sections.
    - [ ] Run `make validate` and `make test`.
- [ ] Task: Update repo and Conductor state.
    - [ ] Link article-hardening outputs from README or docs where appropriate.
    - [ ] Update `.conductor/status.md`, `.conductor/runlog.md`, and this plan as phases complete.
    - [ ] Archive the track only after implementation, review, fixes, and validation pass.

### Acceptance Criteria
- [ ] Local validation gates pass.
- [ ] Conductor status and runlog describe remaining work honestly.
- [ ] Completed artifacts are committed and pushed at phase boundaries.
