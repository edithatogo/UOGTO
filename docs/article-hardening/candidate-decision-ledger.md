# Candidate decision ledger

Date: 2026-07-02

This repository-only supplement joins the article-hardening source register, search log, mapping-review table, and UOGTO inclusion-candidate table into one decision ledger. It is intended to answer four audit questions:

1. What candidates were considered?
2. Which candidates were included, excluded, or left for review?
3. What reason was recorded for each decision?
4. What assumptions or heuristics governed those decisions?

The full row-level ledger is available in:

- `docs/article-hardening/candidate-decision-ledger.csv`
- `docs/article-hardening/candidate-decision-ledger.json`

## Scope counts

| Candidate scope | Rows |
| --- | --- |
| mapping_candidate | 460 |
| ontology_inclusion_candidate | 5 |
| search_route | 7 |
| source_candidate | 39 |

## Decision-class counts

| Decision class | Rows |
| --- | --- |
| excluded | 451 |
| included | 58 |
| needs_review | 2 |

## Assumptions and heuristics

- `search-route screening`: Routes were screened at the evidence-surface level. A route can be included even when individual sources remain metadata-only, licence-constrained, or deferred for later acquisition.
- `source inclusion`: Sources were retained when they exposed game, agent, simulation, execution, provenance, time, process, planning, system-modelling, mapping, or ontology-quality semantics relevant to UOGTO. Retention does not imply parsed RDF availability or semantic equivalence.
- `source exclusion`: The negative-evidence route records searched-but-not-found evidence. Exclusion means no additional releasable source was found for that route, not that the domain was unsearched.
- `mapping-candidate generation`: Mapping candidates were generated from deterministic lexical, normalized-label, definition, embedding, structural, property-signature, source-reliability, synonym, exact-IRI, exact-label, and type-compatibility signals.
- `mapping acceptance`: Accepted mappings are intentionally conservative. Rejected rows remain audit evidence and should not be counted as missing UOGTO concepts without domain review.
- `ontology-inclusion dispositions`: Candidate ontology additions are triaged into add, align externally, defer, duplicate reject, out-of-scope reject, or domain review. A domain-review disposition is a stop signal for direct assertion, not a rejection of relevance.

## Search-route decisions

| Route ID | Decision | Recorded rationale |
| --- | --- | --- |
| phase2-baseline-comparison | included_for_phase2_register | Preserves the completed comparison baseline before appending new article-hardening candidates. |
| phase2-mapping-standards | included_for_phase2_register | Adds mapping publication, review, and quality-method sources needed to harden UOGTO mapping evidence. |
| phase2-game-description | included_for_phase2_register | Adds game-description and game-AI formalism sources likely to expose rule, move, state, imperfect-information, and execution gaps. |
| phase2-simulation-standards | included_for_phase2_register | Adds process, Petri-net, service/action, and planning standards adjacent to UOGTO simulation and execution semantics. |
| phase2-systems-biology | included_for_phase2_register | Adds systems-biology modelling standards relevant to simulation experiments, algorithms, model dynamics, and reporting. |
| phase2-physical-modelling | included_for_phase2_register | Adds continuous, hybrid, co-simulation, and systems-modelling sources for dynamic-game and digital-twin coverage analysis. |
| phase2-negative-evidence | negative_evidence_no_relevant_ontology_found | Targeted searches across registries, repositories, and documentation surfaces found no additional relevant ontology or formalism to include for this route. |

## Source-candidate decisions

All source candidates are shown here because this table is short enough for review. Licence disposition, parseability, module relevance, and search-record links are retained in the CSV/JSON ledger.

| Source ID | Source name | Decision | Recorded rationale |
| --- | --- | --- | --- |
| bfo | Basic Formal Ontology | included | BFO is relevant as an upper ontology for interpreting overlap with process, object, role, and temporal semantics. |
| bpmn_2 | Business Process Model and Notation 2.0 | included | BPMN event, activity, gateway, and process constructs provide useful comparator evidence for execution/workflow semantics. |
| cellml | CellML | included | CellML is relevant for mathematical model structure and simulation context comparisons. |
| devs | DEVS formalism and DEVS metamodel resources | included | DEVS concepts such as atomic/coupled models, events, state transitions, and simulation time overlap UOGTO dynamics and execution traces. |
| dolce | DOLCE | included | DOLCE provides foundational categories useful when comparing events, qualities, agents, and social objects across modelling ontologies. |
| emmo | European Materials and Modelling Ontology | included | EMMO is a modelling-oriented upper/reference ontology used by materials modelling and simulation ontology ecosystems. |
| fmi | Functional Mock-up Interface | included | FMI is relevant to simulator coupling, model exchange, and co-simulation bindings. |
| game_ontology_project | Game Ontology Project | included | The Game Ontology Project is a structured game concept vocabulary relevant to UOGTO's game specification and outcome concepts. |
| gdl_ii_iii_gdlz | GDL-II, GDL-III, and GDLZ variants | included | These GDL variants are relevant for imperfect information, epistemic, and extended game-description constructs that may expose UOGTO gaps. |
| gdlf_gamelan | Game Description Language and GDL resources | included | Game Description Language models game rules, states, legal moves, and terminal conditions that overlap UOGTO rules/actions/outcomes. |
| gvgai_vgdl | General Video Game AI and VGDL resources | included | GVGAI/VGDL is relevant to executable game descriptions, state transitions, and agent evaluation settings. |
| hla_fom | High Level Architecture Federation Object Model resources | included | HLA/FOM resources are relevant to distributed simulation object, interaction, federation, and execution interoperability semantics. |
| kaos | KAoS ontology and policy services | included | KAoS is relevant to multi-agent permissions, obligations, policy, and agent coordination semantics adjacent to UOGTO deontic and agent modules. |
| kisao | Kinetic Simulation Algorithm Ontology | included | KiSAO is directly relevant to simulation algorithm semantics and SED-ML algorithm references. |
| ludii | Ludii general game system | included | Ludii game descriptions provide structured cross-game constructs useful for evaluating UOGTO rule and component coverage. |
| miase | Minimum Information About a Simulation Experiment | included | MIASE provides reporting requirements for simulation experiments that can be compared with UOGTO model/session/trace coverage. |
| modelica | Modelica language and Modelica Standard Library | included | Modelica is relevant to equation-based continuous and hybrid simulation semantics that overlap UOGTO dynamic-game extensions. |
| oaei | Ontology Alignment Evaluation Initiative | included | OAEI is relevant background for reporting ontology mapping evaluation and manual review calibration. |
| odd_protocol | ODD protocol for agent-based models | included | ODD captures overview/design concepts/details of agent-based models and can be mapped to UOGTO specifications, agents, state, and processes. |
| ontouml_ufo | OntoUML / Unified Foundational Ontology | included | OntoUML/UFO can inform conceptual modelling comparisons for agents, events, relations, roles, and social commitments. |
| osmo | Ontology for Simulation, Modelling, and Optimization | included | OSMO is explicitly about simulation, modelling, and optimization and is likely to overlap UOGTO model/execution/binding semantics. |
| owl_s | OWL-S Semantic Markup for Web Services | included | OWL-S process/service concepts are relevant to UOGTO executable action and binding semantics. |
| owl_time | OWL-Time | included | OWL-Time supports temporal intervals and instants relevant to sessions, traces, event timing, and simulation time. |
| p_plan | P-Plan ontology | included | P-Plan models plans, steps, variables, and executions, overlapping UOGTO executable-game and simulation workflow semantics. |
| pddl | Planning Domain Definition Language | included | PDDL action preconditions/effects and planning constructs are useful comparators for UOGTO action and transition semantics. |
| pnml | Petri Net Markup Language | included | PNML can support more precise comparison of UOGTO Petri-net examples and discrete-event execution semantics. |
| prov_o | PROV-O | included | PROV-O overlaps UOGTO execution provenance, traces, activities, agents, generated outcomes, and source attribution. |
| robot | ROBOT ontology tool | included | ROBOT is relevant to article hardening because it can support ontology report, reasoning, and profile checks in later phases. |
| sbgn | Systems Biology Graphical Notation | included | SBGN is relevant as a process/network notation comparator, especially for visualizing model dynamics. |
| sbml | Systems Biology Markup Language | included | SBML model/reaction/simulation ecosystem terms are relevant to UOGTO dynamic model and executable simulation semantics. |
| sbo | Systems Biology Ontology | included | SBO provides controlled terms for systems biology model semantics and simulation-algorithm contexts. |
| schema_org | schema.org | included | schema.org overlaps UOGTO metadata, creative work, software, dataset, action, and web-discoverability semantics. |
| sed_ml | Simulation Experiment Description Markup Language | included | SED-ML describes models, simulations, tasks, data generators, outputs, and KiSAO-backed algorithms that overlap UOGTO execution semantics. |
| ssn_sosa | SSN/SOSA | included | SSN/SOSA observation, procedure, result, and system semantics can align with simulation observation/output traces. |
| sssom | Simple Standard for Sharing Ontological Mappings (SSSOM) | included | SSSOM directly supports reviewable, publishable ontology mapping tables alongside UOGTO RDF/Turtle alignments. |
| stanford_gdl | Stanford Game Description Language | included | GDL captures game rules, legal moves, states, roles, goals, and terminal conditions that overlap UOGTO game specification semantics. |
| sysml | Systems Modeling Language | included | SysML is an adjacent systems-modelling standard useful for context around model structure and requirements. |
| vimmp_ontologies | Virtual Materials Marketplace Ontologies | included | VIMMP ontologies model services, models, interactions, and marketplace semantics around computational modelling. |
| xmile | XMILE System Dynamics Standard | included | XMILE captures stock-flow/system-dynamics model structure and is relevant to UOGTO dynamic and simulation modules. |

## Mapping-candidate decisions

The 460 mapping candidates are stored row-by-row in the CSV/JSON ledger. The summary below preserves the decision distribution without making the Markdown supplement unwieldy.

| Review status | Decision predicate | Rows |
| --- | --- | --- |
| accepted | owl:equivalentClass | 5 |
| accepted | owl:equivalentProperty | 5 |
| needs_domain_review | skos:relatedMatch | 1 |
| rejected | no_match | 449 |

## Ontology-inclusion candidate decisions

| Candidate ID | Candidate label | Disposition | Rationale |
| --- | --- | --- | --- |
| cand-001 | strategic-interaction ontology core term | add_to_uogto | Strong fit for strategic interaction vocabulary |
| cand-002 | discrete-event simulation transition semantics | align_external_only | Useful as an alignment target but too domain-specific for direct inclusion |
| cand-003 | agent-based run and state-transition trace | add_to_uogto | Captures traces, runs, and agent state transitions |
| cand-004 | system-dynamics feedback-loop game feature | requires_domain_review | Potential fit but needs tighter scope and examples |
| cand-005 | no robust general health-economics game ontology found | reject_out_of_scope | Search documented but no robust ontology candidate was found |

## Interpretation limits

- `included` source rows describe retained evidence surfaces, not necessarily parsed RDF artefacts.
- `excluded` mapping rows are negative evidence against a specific asserted mapping, not evidence that the source concept is irrelevant.
- `needs_review` rows should not be promoted to ontology assertions without domain review and examples.
- Candidate generation scores are deterministic heuristics; final ontology claims should use reviewed decisions, not raw similarity scores alone.

## Source artefacts

- `docs/article-hardening/search-log.jsonl`
- `docs/article-hardening/source-extension-inventory.json`
- `docs/article-hardening/uogto-inclusion-candidates.json`
- `docs/ontology-comparison/mapping-review.csv`
