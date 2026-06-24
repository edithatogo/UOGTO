# Specification: UOGTO Article Hardening Protocol

## Purpose
Create a comprehensive, standards-based article-hardening lane for the UOGTO ontology paper. This track extends the completed comparative simulation ontology mapping baseline into a publication-grade evidence package: broader source discovery, explicit protocol registration artifacts, ontology-quality assessment, reasoner and SHACL evaluation, competency-question benchmarking, manual review sampling, reproducibility packaging, and article-ready figures/tables.

The work must remain broad at first. Narrowing decisions should happen only after the protocol, source universe, and feasibility evidence are visible.

## Protocol Standard
The track protocol must be written as a scoping-review protocol aligned with:

- PRISMA-ScR for scoping-review reporting structure, including rationale, objectives, eligibility, information sources, search, selection, data charting, synthesis, limitations, and funding/conflicts statements.
- PRISMA-S for transparent search-strategy reporting across ontology registries, scholarly databases, standards bodies, repositories, and web search surfaces.
- RO-Crate 1.1 for packaging the protocol, source inventories, scripts, retrieved artifacts, derived datasets, analysis outputs, provenance, and article evidence as a machine-readable research object.

## Scope
- Reassess the completed comparative simulation ontology mapping as the baseline corpus, not as the final exhaustive survey.
- Add article-hardening search surfaces for game description languages, general game AI formalisms, planning/action/service-process ontologies, Petri net and workflow ontologies, timed/hybrid automata resources, system dynamics and stock-flow standards, systems-biology simulation standards, process/event ontologies, model execution provenance, and upper/reference ontologies that materially affect mapping interpretation.
- Create a protocol document that can be reused in an article methods section and, if desired later, registered on OSF or attached to Zenodo.
- Produce a protocol compliance checklist and search-log schema before further implementation.
- Extend source inventory and inclusion/exclusion logging only where new candidates pass the protocol rules.
- Evaluate UOGTO and comparator artifacts using ontology-quality metrics, reasoning checks, SHACL validation, annotation completeness, relation richness, module coverage, mapping confidence, and reproducibility checks.
- Benchmark UOGTO against competency questions and use-case coverage matrices relevant to game theory, simulation, agent-based modelling, system dynamics, mechanism design, multi-agent reinforcement learning, and executable knowledge graphs.
- Produce article-ready figures and tables that distinguish evidence-backed results from metadata-only sources, speculative mappings, and future-work candidates.
- Package all reproducible outputs in an RO-Crate manifest with provenance links back to the exact scripts and source artifacts.

## Candidate Extension Families
The implementation must start broad and include at least these families in the protocol search universe:

- Game theory and mathematical game semantics: formal game-theory ontologies, open games, compositional game theory, mechanism design, auction and social-choice vocabularies, cooperative-game resources, epistemic-game resources, and game-theoretic equilibrium representation.
- Game description and game AI formalisms: Game Description Language, GDL-II/GDL-III/GDLZ, Ludii, General Video Game AI resources, game ontology/project vocabularies, strategy-game model languages, and procedural game-description schemas.
- Discrete-event and process simulation: DEVS, DESS, HLA/FOM, event/process ontologies, workflow ontologies, Petri net ontologies, BPMN/OWL mappings, and simulation execution provenance.
- Agent-based modelling and multi-agent systems: ODD, ODD+D, ABM model-description resources, agent/action/policy ontologies, multi-agent system ontologies, KAoS-like policy resources where relevant, and model-run trace vocabularies.
- System dynamics and stock-flow modelling: XMILE, STELLA/Vensim-adjacent resources, stock-flow ontologies, causal-loop vocabularies, feedback-loop schemas, and model-experiment metadata.
- Hybrid, timed, and cyber-physical models: timed automata, hybrid automata, state-machine ontologies, control and cyber-physical modelling vocabularies, and execution trace standards.
- Systems biology and simulation experiment standards: SBO, SBML, CellML, SBGN, SED-ML, KiSAO, MIASE, TEDDY, COMBINE archive metadata, and algorithm/experiment ontologies where they illuminate simulation semantics.
- Scientific modelling and materials/simulation ecosystems: OSMO, EMMO, VIMMP/marketplace ontologies, physics-based simulation ontologies, computational experiment ontologies, and model provenance frameworks.
- General semantic infrastructure: PROV-O, P-Plan, OWL-Time, SSN/SOSA, SKOS, schema.org, BFO, DOLCE, UFO/OntoUML, service/process ontologies such as OWL-S, and other reference ontologies only when they support interpretation of modelling or execution semantics.

## Out of Scope
- Expanding UOGTO semantics solely because an external term exists.
- Claiming coverage from lexical similarity without review evidence.
- Republishing non-redistributable third-party artifacts.
- Treating XML, JSON, PDF, or narrative standards as OWL ontologies unless a documented transformation or structured extraction method is created.
- Registering or publicly posting protocol artifacts without a later explicit user instruction.

## Required Outputs
- `docs/article-hardening/protocol.md`
- `docs/article-hardening/protocol-checklist.md`
- `docs/article-hardening/search-strategy.md`
- `docs/article-hardening/search-log.jsonl`
- `docs/article-hardening/source-extension-inventory.json`
- `docs/article-hardening/source-extension-inventory.md`
- `docs/article-hardening/quality-metrics.json`
- `docs/article-hardening/reasoner-report.md`
- `docs/article-hardening/competency-benchmark.md`
- `docs/article-hardening/use-case-coverage-matrix.csv`
- `docs/article-hardening/manual-review-sample.csv`
- `docs/article-hardening/article-tables/`
- `docs/article-hardening/figures/`
- `docs/article-hardening/ro-crate-metadata.json`
- Scripts and tests needed to regenerate or validate the above artifacts.

## Success Criteria
- The protocol is explicit enough that an independent reviewer can reproduce search routes, eligibility decisions, charting fields, and synthesis methods.
- The protocol cites or links the relevant protocol standards and records where the track intentionally adapts them for ontology engineering rather than clinical evidence synthesis.
- New ontology/formalism candidates are recorded with discovery route, source type, licence disposition, inclusion status, and relevance rationale.
- Quality, reasoning, SHACL, mapping, and competency-question checks are reproducible from repository scripts.
- Article-ready evidence separates parsed RDF/OWL sources, structured non-RDF standards, metadata-only sources, and excluded sources.
- `make validate` or `make test` passes before the track is treated as ready for implementation review.
