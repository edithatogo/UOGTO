# Article-Hardening Source Extension Inventory

This generated summary mirrors `source-extension-inventory.json` and `search-log.jsonl`.

## Register Contract

- Search records are hash chained with `previous_record_hash` and `record_hash`.
- Source rows carry immutable `source_hash` values.
- Later searches should append records rather than rewriting prior evidence.

## Summary Counts

- Sources: 39
- Search records: 6
- Baseline-preserved sources: 21
- New candidates: 18

## Evidence Levels

- `literature_only`: 2
- `metadata_only`: 15
- `parsed_rdf_owl`: 4
- `structured_non_rdf`: 18

## Source Families

- `agent_based_modelling`: 1
- `agent_policy`: 1
- `discrete_event_simulation`: 1
- `distributed_simulation`: 1
- `game_description_language`: 5
- `game_studies`: 1
- `general_web_schema`: 1
- `mapping_evaluation_benchmark`: 1
- `mapping_standard`: 1
- `modelling_simulation_interoperability`: 2
- `observation_sensor`: 1
- `ontology_quality_tool`: 1
- `petri_net`: 1
- `physical_modelling`: 2
- `planning_language`: 1
- `process_modelling`: 1
- `process_service_ontology`: 1
- `provenance`: 1
- `simulation_algorithm`: 1
- `simulation_experiment`: 2
- `system_dynamics`: 1
- `systems_biology_modelling`: 4
- `systems_engineering`: 1
- `time`: 1
- `upper_modelling_reference`: 1
- `upper_ontology`: 3
- `workflow_plan`: 1

## Highlighted New Candidates

SSSOM is included as the mapping-standard source for ontology alignment TSV/YAML outputs.

- `bpmn_2`: Business Process Model and Notation 2.0
- `cellml`: CellML
- `fmi`: Functional Mock-up Interface
- `gdl_ii_iii_gdlz`: GDL-II, GDL-III, and GDLZ variants
- `gvgai_vgdl`: General Video Game AI and VGDL resources
- `ludii`: Ludii general game system
- `modelica`: Modelica language and Modelica Standard Library
- `oaei`: Ontology Alignment Evaluation Initiative
- `owl_s`: OWL-S Semantic Markup for Web Services
- `pddl`: Planning Domain Definition Language
- `pnml`: Petri Net Markup Language
- `robot`: ROBOT ontology tool
- `sbgn`: Systems Biology Graphical Notation
- `sbml`: Systems Biology Markup Language
- `sbo`: Systems Biology Ontology
- `sssom`: Simple Standard for Sharing Ontological Mappings (SSSOM)
- `stanford_gdl`: Stanford Game Description Language
- `sysml`: Systems Modeling Language

## Search Records

| Record | Surface type | Included | Evidence level | Hash |
| --- | --- | ---: | --- | --- |
| `phase2-baseline-comparison` | `baseline_artifact` | 21 | `mixed` | `sha256:f7f700a7be818924b308da030f978a901d08da6a000712b5709d26038dcf4c8d` |
| `phase2-mapping-standards` | `web_search` | 3 | `metadata_only` | `sha256:d7196651d166cbdced43c987f8c52ea3e6093fb1f9f44b48e88410639778a5e2` |
| `phase2-game-description` | `project_site` | 4 | `structured_non_rdf` | `sha256:bf7982e31cc8a7b5551293d7e71e462c7f25df89ae7862d8cf8aaf653710d844` |
| `phase2-simulation-standards` | `standards_body` | 4 | `structured_non_rdf` | `sha256:fb250dc79abd98cdce41a0c8903b299b74601adaa0a42ead47e7343cbb36a8fb` |
| `phase2-systems-biology` | `standards_body` | 4 | `structured_non_rdf` | `sha256:3e041eb5df803ff1a26f3b03af0e5a9a239839a3ef22fdb0648237122be96746` |
| `phase2-physical-modelling` | `standards_body` | 3 | `structured_non_rdf` | `sha256:c8934bb1c4b62c97e71cf8475b4ce2aa544ec85248802a3b82c5e44d1aa32cb9` |

## Reviewer Handoff

Phase 2 records are ready for evidence-curation, reproducibility, standards-landscape, game-theory-gap, peer-review, methods-editorial, red-team, and devil's-advocate review before Phase 3 acquisition.

## Negative Evidence

- `phase2-negative-evidence`: searched targeted game-theory ontology registry and repository routes and found no additional relevant ontology to include. This route is preserved as negative evidence, not as a source. 
