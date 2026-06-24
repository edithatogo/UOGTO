# Article Evidence Dashboard

This dashboard exposes only validated tables and figures from the article-hardening evidence package.
The source lists are separated by evidence level: parsed RDF, structured non-RDF, metadata-only, literature-only, and excluded.

## Summary

- **Parsed RDF**: 4
- **Structured non-RDF**: 18
- **Metadata-only**: 15
- **Literature-only**: 2
- **Excluded**: 0

## Validated Tables

| Table | Formats | Validation gate | Purpose |
| --- | --- | --- | --- |
| Source extension inventory | `source-extension-inventory.json`, `source-extension-inventory.md` | `scripts/maintenance/check_article_hardening_protocol.py` | Living evidence register for search routes, source families, and evidence levels. |
| Search log | `search-log.jsonl` | `scripts/maintenance/check_article_hardening_protocol.py` | Append-only search history with hash-chained evidence records. |
| Quality metrics | `quality-metrics.json`, `reasoner-report.md` | `scripts/maintenance/build_article_hardening_quality.py` | Ontology-quality benchmark and reasoner report for the article-hardening track. |
| Manual review sample | `manual-review-sample.csv`, `manual-review-sample.md`, `manual-review-sample.json`, `manual-review-sample.parquet` | `scripts/maintenance/export_tabular_artifacts.py` | Manually reviewed source sample for reviewer calibration and dual screening. |
| Dual screening sample | `dual-screening-sample.csv`, `dual-screening-sample.md`, `dual-screening-sample.json`, `dual-screening-sample.parquet` | `scripts/maintenance/export_tabular_artifacts.py` | Researcher, peer reviewer, and red-team adjudication sample. |
| UOGTO inclusion candidates | `uogto-inclusion-candidates.csv`, `uogto-inclusion-candidates.md`, `uogto-inclusion-candidates.json`, `uogto-inclusion-candidates.parquet` | `scripts/maintenance/export_tabular_artifacts.py` | Triage table for add-to-UOGTO, align-external-only, defer, reject, or domain-review outcomes. |
| Use-case coverage matrix | `use-case-coverage-matrix.csv`, `use-case-coverage-matrix.md`, `use-case-coverage-matrix.json`, `use-case-coverage-matrix.parquet` | `scripts/maintenance/export_tabular_artifacts.py` | Coverage matrix for the article-hardened case studies and ontology examples. |

## Validated Figures

| Figure | Path | Purpose |
| --- | --- | --- |
| PRISMA 2020 source discovery flow | `figures/prisma-2020-source-discovery-flow.md` | Source discovery count and route summary. |
| PRISMA 2020 screening flow | `figures/prisma-2020-screening-flow.md` | Screening, inclusion, and exclusion flow for the article-hardening register. |

## Source Evidence Categories

### Parsed RDF

- Count: 4

| Source | Family | Status | Rationale |
| --- | --- | --- | --- |
| `schema_org` | `general_web_schema` | `included` | schema.org overlaps UOGTO metadata, creative work, software, dataset, action, and web-discoverability semantics. |
| `ssn_sosa` | `observation_sensor` | `included` | SSN/SOSA observation, procedure, result, and system semantics can align with simulation observation/output traces. |
| `prov_o` | `provenance` | `included` | PROV-O overlaps UOGTO execution provenance, traces, activities, agents, generated outcomes, and source attribution. |
| `owl_time` | `time` | `included` | OWL-Time supports temporal intervals and instants relevant to sessions, traces, event timing, and simulation time. |

### Structured non-RDF

- Count: 18

| Source | Family | Status | Rationale |
| --- | --- | --- | --- |
| `devs` | `discrete_event_simulation` | `included` | DEVS concepts such as atomic/coupled models, events, state transitions, and simulation time overlap UOGTO dynamics and execution traces. |
| `hla_fom` | `distributed_simulation` | `included` | HLA/FOM resources are relevant to distributed simulation object, interaction, federation, and execution interoperability semantics. |
| `gdlf_gamelan` | `game_description_language` | `included` | Game Description Language models game rules, states, legal moves, and terminal conditions that overlap UOGTO rules/actions/outcomes. |
| `gvgai_vgdl` | `game_description_language` | `included` | GVGAI/VGDL is relevant to executable game descriptions, state transitions, and agent evaluation settings. |
| `ludii` | `game_description_language` | `included` | Ludii game descriptions provide structured cross-game constructs useful for evaluating UOGTO rule and component coverage. |
| `sssom` | `mapping_standard` | `included` | SSSOM directly supports reviewable, publishable ontology mapping tables alongside UOGTO RDF/Turtle alignments. |
| `pnml` | `petri_net` | `included` | PNML can support more precise comparison of UOGTO Petri-net examples and discrete-event execution semantics. |
| `fmi` | `physical_modelling` | `included` | FMI is relevant to simulator coupling, model exchange, and co-simulation bindings. |
| `modelica` | `physical_modelling` | `included` | Modelica is relevant to equation-based continuous and hybrid simulation semantics that overlap UOGTO dynamic-game extensions. |
| `pddl` | `planning_language` | `included` | PDDL action preconditions/effects and planning constructs are useful comparators for UOGTO action and transition semantics. |
| `bpmn_2` | `process_modelling` | `included` | BPMN event, activity, gateway, and process constructs provide useful comparator evidence for execution/workflow semantics. |
| `sed_ml` | `simulation_experiment` | `included` | SED-ML describes models, simulations, tasks, data generators, outputs, and KiSAO-backed algorithms that overlap UOGTO execution semantics. |
| `xmile` | `system_dynamics` | `included` | XMILE captures stock-flow/system-dynamics model structure and is relevant to UOGTO dynamic and simulation modules. |
| `cellml` | `systems_biology_modelling` | `included` | CellML is relevant for mathematical model structure and simulation context comparisons. |
| `sbgn` | `systems_biology_modelling` | `included` | SBGN is relevant as a process/network notation comparator, especially for visualizing model dynamics. |
| `sbml` | `systems_biology_modelling` | `included` | SBML model/reaction/simulation ecosystem terms are relevant to UOGTO dynamic model and executable simulation semantics. |
| `sysml` | `systems_engineering` | `included` | SysML is an adjacent systems-modelling standard useful for context around model structure and requirements. |
| `ontouml_ufo` | `upper_ontology` | `included` | OntoUML/UFO can inform conceptual modelling comparisons for agents, events, relations, roles, and social commitments. |

### Metadata-only

- Count: 15

| Source | Family | Status | Rationale |
| --- | --- | --- | --- |
| `odd_protocol` | `agent_based_modelling` | `included` | ODD captures overview/design concepts/details of agent-based models and can be mapped to UOGTO specifications, agents, state, and processes. |
| `kaos` | `agent_policy` | `included` | KAoS is relevant to multi-agent permissions, obligations, policy, and agent coordination semantics adjacent to UOGTO deontic and agent modules. |
| `game_ontology_project` | `game_studies` | `included` | The Game Ontology Project is a structured game concept vocabulary relevant to UOGTO's game specification and outcome concepts. |
| `oaei` | `mapping_evaluation_benchmark` | `included` | OAEI is relevant background for reporting ontology mapping evaluation and manual review calibration. |
| `osmo` | `modelling_simulation_interoperability` | `included` | OSMO is explicitly about simulation, modelling, and optimization and is likely to overlap UOGTO model/execution/binding semantics. |
| `vimmp_ontologies` | `modelling_simulation_interoperability` | `included` | VIMMP ontologies model services, models, interactions, and marketplace semantics around computational modelling. |
| `robot` | `ontology_quality_tool` | `included` | ROBOT is relevant to article hardening because it can support ontology report, reasoning, and profile checks in later phases. |
| `owl_s` | `process_service_ontology` | `included` | OWL-S process/service concepts are relevant to UOGTO executable action and binding semantics. |
| `kisao` | `simulation_algorithm` | `included` | KiSAO is directly relevant to simulation algorithm semantics and SED-ML algorithm references. |
| `miase` | `simulation_experiment` | `included` | MIASE provides reporting requirements for simulation experiments that can be compared with UOGTO model/session/trace coverage. |
| `sbo` | `systems_biology_modelling` | `included` | SBO provides controlled terms for systems biology model semantics and simulation-algorithm contexts. |
| `emmo` | `upper_modelling_reference` | `included` | EMMO is a modelling-oriented upper/reference ontology used by materials modelling and simulation ontology ecosystems. |
| `bfo` | `upper_ontology` | `included` | BFO is relevant as an upper ontology for interpreting overlap with process, object, role, and temporal semantics. |
| `dolce` | `upper_ontology` | `included` | DOLCE provides foundational categories useful when comparing events, qualities, agents, and social objects across modelling ontologies. |
| `p_plan` | `workflow_plan` | `included` | P-Plan models plans, steps, variables, and executions, overlapping UOGTO executable-game and simulation workflow semantics. |

### Literature-only

- Count: 2

| Source | Family | Status | Rationale |
| --- | --- | --- | --- |
| `gdl_ii_iii_gdlz` | `game_description_language` | `included` | These GDL variants are relevant for imperfect information, epistemic, and extended game-description constructs that may expose UOGTO gaps. |
| `stanford_gdl` | `game_description_language` | `included` | GDL captures game rules, legal moves, states, roles, goals, and terminal conditions that overlap UOGTO game specification semantics. |

### Excluded

- Count: 0
- No excluded sources are recorded in the current source inventory.

## Negative Evidence

These search records found no relevant ontology to include and are preserved in the register.

| Record | Surface | Surface type | Query | Results |
| --- | --- | --- | --- | --- |
| `phase2-negative-evidence` | `Game-theory ontology registry and repository sweep` | `web_search` | game theory ontology OR game theory OWL OR game theory RDF registry repository | 0 |

## Quality Reference

- Ontology classes: 299
- Ontology properties: 204
- Example files: 17
- Competency queries: 10

