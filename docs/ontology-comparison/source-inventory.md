# Comparative Ontology Source Inventory

This file is generated from `source-inventory.json` by `scripts/maintenance/build_ontology_comparison_inventory.py`.

## Summary
- Sources: `21`
- Families: `17`

### By Review Status
- `included`: 4
- `needs_review`: 2
- `seeded`: 15

### By Licence Disposition
- `metadata_only`: 8
- `needs_licence_review`: 9
- `redistributable_artifact`: 4

## Sources

### ODD protocol for agent-based models
- ID: `odd_protocol`
- Family: `agent_based_modelling`
- Candidate type: `reporting_protocol`
- Source URL: <https://www.jasss.org/23/2/7.html>
- Artifact URL: not identified
- Expected format: `documentation`
- Licence disposition: `metadata_only`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `medium`
- Discovery route: seed: agent-based modelling ODD protocol
- Inclusion rationale: ODD captures overview/design concepts/details of agent-based models and can be mapped to UOGTO specifications, agents, state, and processes.

### KAoS ontology and policy services
- ID: `kaos`
- Family: `agent_policy`
- Candidate type: `ontology_framework`
- Source URL: <https://ontology.ihmc.us/kaos.html>
- Artifact URL: <https://ontology.ihmc.us/kaos.html>
- Expected format: `OWL/documentation`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `needs_review`
- Priority: `low`
- Discovery route: seed: multi-agent policy ontology
- Inclusion rationale: KAoS is relevant to multi-agent permissions, obligations, policy, and agent coordination semantics adjacent to UOGTO deontic and agent modules.

### DEVS formalism and DEVS metamodel resources
- ID: `devs`
- Family: `discrete_event_simulation`
- Candidate type: `formalism_or_metamodel`
- Source URL: <https://acims.asu.edu/devs/>
- Artifact URL: not identified
- Expected format: `documentation/metamodel`
- Licence disposition: `metadata_only`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `high`
- Discovery route: seed: discrete-event simulation ontology search
- Inclusion rationale: DEVS concepts such as atomic/coupled models, events, state transitions, and simulation time overlap UOGTO dynamics and execution traces.

### High Level Architecture Federation Object Model resources
- ID: `hla_fom`
- Family: `distributed_simulation`
- Candidate type: `standard_schema`
- Source URL: <https://www.sisostds.org/>
- Artifact URL: not identified
- Expected format: `standard/documentation/schema`
- Licence disposition: `metadata_only`
- Redistribution risk: `high`
- Review status: `needs_review`
- Priority: `medium`
- Discovery route: seed: HLA/FOM simulation interoperability search
- Inclusion rationale: HLA/FOM resources are relevant to distributed simulation object, interaction, federation, and execution interoperability semantics.

### Game Description Language and GDL resources
- ID: `gdlf_gamelan`
- Family: `game_description_language`
- Candidate type: `formal_language`
- Source URL: <https://en.wikipedia.org/wiki/Game_Description_Language>
- Artifact URL: not identified
- Expected format: `logic language/documentation`
- Licence disposition: `metadata_only`
- Redistribution risk: `low`
- Review status: `seeded`
- Priority: `medium`
- Discovery route: seed: game description language resources
- Inclusion rationale: Game Description Language models game rules, states, legal moves, and terminal conditions that overlap UOGTO rules/actions/outcomes.

### Game Ontology Project
- ID: `game_ontology_project`
- Family: `game_studies`
- Candidate type: `vocabulary`
- Source URL: <https://www.gameontology.com/>
- Artifact URL: not identified
- Expected format: `documentation/vocabulary`
- Licence disposition: `metadata_only`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `medium`
- Discovery route: seed: game ontology search
- Inclusion rationale: The Game Ontology Project is a structured game concept vocabulary relevant to UOGTO's game specification and outcome concepts.

### schema.org
- ID: `schema_org`
- Family: `general_web_schema`
- Candidate type: `vocabulary`
- Source URL: <https://schema.org/>
- Artifact URL: <https://schema.org/version/latest/schemaorg-current-https.ttl>
- Expected format: `RDF/Turtle`
- Licence disposition: `redistributable_artifact`
- Redistribution risk: `low`
- Review status: `included`
- Priority: `low`
- Discovery route: seed: existing UOGTO alignment
- Inclusion rationale: schema.org overlaps UOGTO metadata, creative work, software, dataset, action, and web-discoverability semantics.

### Ontology for Simulation, Modelling, and Optimization
- ID: `osmo`
- Family: `modelling_simulation_interoperability`
- Candidate type: `ontology`
- Source URL: <https://github.com/virtual-materials-marketplace/osmo>
- Artifact URL: <https://github.com/virtual-materials-marketplace/osmo>
- Expected format: `OWL/RDF`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `high`
- Discovery route: seed: modelling and simulation ontology search
- Inclusion rationale: OSMO is explicitly about simulation, modelling, and optimization and is likely to overlap UOGTO model/execution/binding semantics.

### Virtual Materials Marketplace Ontologies
- ID: `vimmp_ontologies`
- Family: `modelling_simulation_interoperability`
- Candidate type: `ontology_family`
- Source URL: <https://github.com/virtual-materials-marketplace>
- Artifact URL: <https://github.com/virtual-materials-marketplace>
- Expected format: `OWL/RDF`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `medium`
- Discovery route: seed: VIMMP/EMMO marketplace ontology literature
- Inclusion rationale: VIMMP ontologies model services, models, interactions, and marketplace semantics around computational modelling.

### SSN/SOSA
- ID: `ssn_sosa`
- Family: `observation_sensor`
- Candidate type: `ontology`
- Source URL: <https://www.w3.org/TR/vocab-ssn/>
- Artifact URL: <https://www.w3.org/ns/ssn/>
- Expected format: `OWL/RDF`
- Licence disposition: `redistributable_artifact`
- Redistribution risk: `low`
- Review status: `included`
- Priority: `medium`
- Discovery route: seed: W3C observation ontology
- Inclusion rationale: SSN/SOSA observation, procedure, result, and system semantics can align with simulation observation/output traces.

### PROV-O
- ID: `prov_o`
- Family: `provenance`
- Candidate type: `ontology`
- Source URL: <https://www.w3.org/TR/prov-o/>
- Artifact URL: <https://www.w3.org/ns/prov-o.owl>
- Expected format: `OWL/RDF`
- Licence disposition: `redistributable_artifact`
- Redistribution risk: `low`
- Review status: `included`
- Priority: `high`
- Discovery route: seed: W3C provenance ontology
- Inclusion rationale: PROV-O overlaps UOGTO execution provenance, traces, activities, agents, generated outcomes, and source attribution.

### Kinetic Simulation Algorithm Ontology
- ID: `kisao`
- Family: `simulation_algorithm`
- Candidate type: `ontology`
- Source URL: <https://github.com/SED-ML/KiSAO>
- Artifact URL: <https://github.com/SED-ML/KiSAO>
- Expected format: `OWL/RDF`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `high`
- Discovery route: seed: COMBINE/SED-ML simulation algorithm ontology
- Inclusion rationale: KiSAO is directly relevant to simulation algorithm semantics and SED-ML algorithm references.

### Minimum Information About a Simulation Experiment
- ID: `miase`
- Family: `simulation_experiment`
- Candidate type: `minimum_information_standard`
- Source URL: <https://co.mbine.org/standards/miase>
- Artifact URL: not identified
- Expected format: `documentation`
- Licence disposition: `metadata_only`
- Redistribution risk: `low`
- Review status: `seeded`
- Priority: `medium`
- Discovery route: seed: COMBINE simulation experiment reporting standard
- Inclusion rationale: MIASE provides reporting requirements for simulation experiments that can be compared with UOGTO model/session/trace coverage.

### Simulation Experiment Description Markup Language
- ID: `sed_ml`
- Family: `simulation_experiment`
- Candidate type: `schema_standard`
- Source URL: <https://sed-ml.org/>
- Artifact URL: <https://github.com/sed-ml/sed-ml>
- Expected format: `XML schema/documentation`
- Licence disposition: `metadata_only`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `high`
- Discovery route: seed: COMBINE simulation experiment standard
- Inclusion rationale: SED-ML describes models, simulations, tasks, data generators, outputs, and KiSAO-backed algorithms that overlap UOGTO execution semantics.

### XMILE System Dynamics Standard
- ID: `xmile`
- Family: `system_dynamics`
- Candidate type: `schema_standard`
- Source URL: <https://www.oasis-open.org/standard/xmile-v1-0/>
- Artifact URL: <https://www.oasis-open.org/standard/xmile-v1-0/>
- Expected format: `XML schema/documentation`
- Licence disposition: `metadata_only`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `high`
- Discovery route: seed: system dynamics standard
- Inclusion rationale: XMILE captures stock-flow/system-dynamics model structure and is relevant to UOGTO dynamic and simulation modules.

### OWL-Time
- ID: `owl_time`
- Family: `time`
- Candidate type: `ontology`
- Source URL: <https://www.w3.org/TR/owl-time/>
- Artifact URL: <https://www.w3.org/2006/time>
- Expected format: `OWL/RDF`
- Licence disposition: `redistributable_artifact`
- Redistribution risk: `low`
- Review status: `included`
- Priority: `medium`
- Discovery route: seed: W3C time ontology
- Inclusion rationale: OWL-Time supports temporal intervals and instants relevant to sessions, traces, event timing, and simulation time.

### European Materials and Modelling Ontology
- ID: `emmo`
- Family: `upper_modelling_reference`
- Candidate type: `ontology`
- Source URL: <https://github.com/emmo-repo/EMMO>
- Artifact URL: <https://github.com/emmo-repo/EMMO>
- Expected format: `OWL/RDF`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `high`
- Discovery route: seed: EMMC modelling ontology
- Inclusion rationale: EMMO is a modelling-oriented upper/reference ontology used by materials modelling and simulation ontology ecosystems.

### Basic Formal Ontology
- ID: `bfo`
- Family: `upper_ontology`
- Candidate type: `ontology`
- Source URL: <https://github.com/BFO-ontology/BFO-2020>
- Artifact URL: <https://github.com/BFO-ontology/BFO-2020>
- Expected format: `OWL/RDF`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `medium`
- Discovery route: seed: upper ontology used by many applied ontologies
- Inclusion rationale: BFO is relevant as an upper ontology for interpreting overlap with process, object, role, and temporal semantics.

### DOLCE
- ID: `dolce`
- Family: `upper_ontology`
- Candidate type: `ontology`
- Source URL: <https://www.loa.istc.cnr.it/dolce/overview.html>
- Artifact URL: not identified
- Expected format: `OWL/RDF/documentation`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `low`
- Discovery route: seed: upper ontology candidate
- Inclusion rationale: DOLCE provides foundational categories useful when comparing events, qualities, agents, and social objects across modelling ontologies.

### OntoUML / Unified Foundational Ontology
- ID: `ontouml_ufo`
- Family: `upper_ontology`
- Candidate type: `ontology_or_metamodel`
- Source URL: <https://ontouml.org/>
- Artifact URL: <https://github.com/OntoUML>
- Expected format: `metamodel/ontology/documentation`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `low`
- Discovery route: seed: upper ontology and conceptual modelling
- Inclusion rationale: OntoUML/UFO can inform conceptual modelling comparisons for agents, events, relations, roles, and social commitments.

### P-Plan ontology
- ID: `p_plan`
- Family: `workflow_plan`
- Candidate type: `ontology`
- Source URL: <https://vocab.linkeddata.es/p-plan/>
- Artifact URL: <http://purl.org/net/p-plan>
- Expected format: `OWL/RDF`
- Licence disposition: `needs_licence_review`
- Redistribution risk: `medium`
- Review status: `seeded`
- Priority: `medium`
- Discovery route: seed: plan/provenance ontology
- Inclusion rationale: P-Plan models plans, steps, variables, and executions, overlapping UOGTO executable-game and simulation workflow semantics.
