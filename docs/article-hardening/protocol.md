# UOGTO Article-Hardening Protocol

## Title
UOGTO article-hardening protocol for comparative ontology, modelling-formalism, and reporting evidence.

## Protocol Standards
This protocol adapts three standards:

- PRISMA-ScR: used for the scoping-review structure, including rationale, objectives, eligibility, information sources, source selection, charting, synthesis, limitations, and funding/conflict declarations.
- PRISMA-S: used for transparent reporting of ontology-registry, repository, literature, standards-body, and web searches.
- RO-Crate 1.1: used for packaging protocol documents, search logs, source inventories, scripts, retrieved redistributable artifacts, metadata-only source references, derived metrics, figures, and article-ready evidence.

## Rationale
The completed UOGTO comparative ontology mapping track produced a reproducible baseline for simulation and modelling ontology comparison. That baseline should not be treated as an exhaustive scholarly or standards survey. This article-hardening protocol extends the baseline into a broader evidence package that can support defensible claims about UOGTO coverage, novelty, interoperability, limitations, and future ontology changes.

## Objectives
1. Identify game-theory, simulation, modelling, process, provenance, and reference ontologies or formalisms relevant to UOGTO.
2. Record a reproducible search and screening trail across registries, repositories, scholarly sources, archival sources, standards bodies, and web documentation.
3. Compare UOGTO against parsed RDF/OWL sources, structured non-RDF standards, metadata-only sources, and excluded sources without conflating their evidence levels.
4. Evaluate ontology quality, reasoning/validation status, competency-question coverage, mapping robustness, and use-case coverage.
5. Identify game-theory elements absent from UOGTO and decide whether each should be added, aligned externally, deferred, rejected, or sent for domain review.
6. Produce article-ready tables, figures, methods text, results text, and reproducibility metadata.

## Review Questions
1. Which existing ontologies, vocabularies, standards, schemas, and formalisms overlap with UOGTO's intended game-theory and simulation scope?
2. Which UOGTO modules are well covered by external comparators, and which are UOGTO-specific or under-represented elsewhere?
3. Which external terms or constructs expose material gaps in UOGTO?
4. Which gaps justify UOGTO expansion rather than external alignment only?
5. How robust are UOGTO mapping and coverage claims under alternative evidence levels and mapping features?

## Information Sources
Searches must cover:

- Ontology registries: LOV, OLS, BioPortal, Ontobee, Bioregistry, FAIRsharing, Wikidata, and domain-specific registry pages discovered during search.
- Scholarly and archival sources: Crossref, Semantic Scholar, arXiv, Zenodo, OSF, ACM/IEEE landing pages where publicly available, institutional repositories, and standards-body publication pages.
- Repository surfaces: GitHub, GitLab, SourceForge, standards-body repositories, release pages, package indexes, and project documentation sites.
- Standards and modelling communities: W3C, OMG, IEEE, COMBINE, SBML, CellML, SBGN, SED-ML, KiSAO, MIASE, DEVS, HLA/FOM, ODD/ABM, XMILE, Petri nets, BPMN/process modelling, timed/hybrid automata, OSMO, EMMO, VIMMP, and physics-based simulation communities.
- Baseline UOGTO artifacts: `docs/ontology-comparison/` outputs from the completed comparative mapping track.

## Search Strategy
Each search route must be logged in `docs/article-hardening/search-log.jsonl` using the PRISMA-S fields defined in `docs/article-hardening/search-strategy.md`. Search strings must be specific enough to reproduce intent and broad enough to capture game-theory ontology, simulation ontology, game-description language, model execution, provenance, and reference ontology variants.

## Eligibility Criteria
Include sources when they meet at least one inclusion criterion:

- Defines an OWL/RDF ontology, SKOS vocabulary, controlled vocabulary, or linked-data schema relevant to game theory, simulation, modelling, execution, provenance, or reference semantics.
- Defines a formal modelling language, XML/JSON schema, metamodel, or standards vocabulary that can be charted and compared with UOGTO.
- Provides authoritative documentation for a modelling standard or formalism relevant to UOGTO's article claims.
- Provides a reusable upper/reference ontology used by comparator sources or needed to interpret mappings.

Exclude sources when:

- They are narrative-only and do not define reusable terms, constructs, schemas, or formal semantics.
- They are inaccessible, duplicative, superseded without retained relevance, or impossible to cite or provenance adequately.
- Their licence prohibits local redistribution and no metadata-only representation is sufficient for article evidence.
- They are outside UOGTO's game-theory, simulation, modelling, or execution scope.

## Evidence Levels
Evidence must be classified as:

- `parsed_rdf_owl`: source artifact is retrieved and parsed as RDF, OWL, TTL, RDF/XML, JSON-LD, or SKOS.
- `structured_non_rdf`: source is an XML schema, JSON schema, CSV vocabulary, metamodel, or formal grammar with structured extractable terms.
- `metadata_only`: source cannot be redistributed or parsed locally, but authoritative metadata and URLs can be recorded.
- `literature_only`: source is described in literature without a directly usable public artifact.
- `excluded`: source fails eligibility or licence/provenance criteria.

## Data Charting Fields
Every included or screened source should be charted with:

- `source_id`
- `source_name`
- `source_family`
- `modelling_paradigm`
- `source_type`
- `canonical_url`
- `discovery_route`
- `licence_disposition`
- `artifact_availability`
- `parseability`
- `evidence_level`
- `mapping_relevance`
- `uogto_module_relevance`
- `article_use_category`
- `inclusion_status`
- `screening_rationale`
- `limitations`

## Synthesis Plan
The synthesis must separate:

- Source-discovery counts and source-family coverage.
- Evidence-level coverage: parsed RDF/OWL, structured non-RDF, metadata-only, literature-only, and excluded sources.
- UOGTO module coverage and use-case coverage.
- Mapping confidence and mapping predicate classes.
- Ontology-quality and validation metrics.
- Missing game-theory element triage.
- Article-ready claims, limitations, and future-work recommendations.

## Missing-Element Decision Rules
Candidate missing UOGTO elements must be classified as:

- `add_to_uogto`: evidence supports a new or refined UOGTO class, property, axiom, shape, example, or competency question.
- `align_external_only`: external construct is relevant but better handled as a mapping or annotation.
- `defer_pending_evidence`: relevance is plausible but evidence is too weak or source access is insufficient.
- `reject_as_duplicate`: UOGTO already represents the construct adequately.
- `reject_out_of_scope`: construct is outside UOGTO's intended scope.
- `requires_domain_review`: expert judgement is needed before ontology expansion.

No element should be recommended for addition unless it improves at least one of competency-question coverage, interoperability, article-claim precision, conceptual clarity, or validation/example completeness.

## Reproducibility Plan
All generated artifacts must be reproducible from repository scripts where feasible. The RO-Crate metadata must describe protocol documents, inventories, search logs, scripts, generated metrics, article tables, figures, and source artifacts or source references. When Java tooling is available, generate ROBOT-style ontology reports for reasoner checking, report summaries, merge/diff views, and import extraction; when it is not, keep the RDFLib/pySHACL baseline authoritative and explicit.

## Limitations
Search results may drift over time, registry search interfaces differ, some standards are not redistributable, and metadata-only sources cannot support the same strength of claims as parsed artifacts. The final article must report these limitations explicitly.

## Protocol Amendments
Material changes to source families, eligibility criteria, charting fields, evidence levels, or synthesis methods must be recorded in `.conductor/runlog.md` and reflected in the protocol checklist.

## Funding and Conflicts
No external funding or conflicts are recorded in this repository protocol unless added later by the project owner.

## Negative Evidence

Negative evidence routes use the term `negative_evidence_no_relevant_ontology_found` for searches that were executed but returned no relevant ontology or formalism. The article must treat these outcomes as searched-and-not-found evidence, not as proof of universal absence. 

## PRISMA-ScR Evidence Package
The protocol is packaged as a scoping-review evidence bundle through the following repository artifacts:

- `docs/article-hardening/structured-summary.md`
- `docs/article-hardening/protocol-checklist.md`
- `docs/article-hardening/prisma-scr-artifact-map.md`
- `docs/article-hardening/search-strategy.md`
- `docs/article-hardening/search-log.jsonl`
- `docs/article-hardening/source-extension-inventory.json`
- `docs/article-hardening/source-extension-inventory.md`
- `docs/article-hardening/quality-metrics.json`
- `docs/article-hardening/reasoner-report.md`
- `docs/article-hardening/case-studies.md`
- `docs/article-hardening/ro-crate-metadata.json`

The checklist maps the 20 essential and 2 optional PRISMA-ScR items to these artifacts, while the artifact map expands the crosswalk for drafting and review. Negative evidence remains recorded as a searched-and-not-found outcome rather than an absence proof.

## PRISMA 2020 Flow Diagrams
This package also includes PRISMA 2020-style flow diagrams for source discovery and screening:

- `docs/article-hardening/figures/prisma-2020-source-discovery-flow.md`
- `docs/article-hardening/figures/prisma-2020-screening-flow.md`

The diagrams are derived from the current `search-log.jsonl` and `source-extension-inventory.json` artifacts and should be refreshed whenever those counts change.


## Dual Screening and Adjudication
A simulated dual-screening workflow is used for evidence-package review:

- the researcher proposes an inclusion or exclusion disposition,
- the peer reviewer accepts or rejects the proposal,
- the red team reviewer challenges overclaims, weak evidence, or scope drift,
- the final disposition is recorded in the dual-screening sample register.

This keeps the screening chain explicit without implying that every package element has undergone live double-blind review. The checker treats this surface as `dual_screening` for validation and reporting.

Artifacts:

- `docs/article-hardening/dual-screening.md`
- `docs/article-hardening/dual-screening-sample.csv`
