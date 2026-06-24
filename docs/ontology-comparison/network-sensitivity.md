# Network analysis sensitivity

This report compares network communities and bridge terms across the key network-analysis toggles.

## Scenarios

| scenario | source nodes | source edges | source communities | alignment nodes | alignment edges | alignment communities |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| all_sources__accepted_mappings | 74 | 68 | 6 | 17 | 10 | 7 |
| parsed_sources_only__accepted_mappings | 73 | 51 | 22 | 17 | 10 | 7 |
| all_sources__accepted_plus_close_related | 74 | 68 | 6 | 18 | 11 | 7 |
| parsed_sources_only__accepted_plus_close_related | 73 | 51 | 22 | 18 | 11 | 7 |

## Sensitivity

- Metadata-only exclusion changed source communities by 16.
- Metadata-only exclusion changed source bridge nodes by removing bfo, devs, dolce, emmo, game_ontology_project, metadata_only_sources.
- Accepting close/related mappings changed alignment communities by 0.
- Accepting close/related mappings changed alignment bridge nodes by adding source:http://www.w3.org/ns/prov#agent.

## Bridge Overlap

- Source-graph bridge overlap: format:turtle, import:core, ssn_sosa.
- Alignment-graph bridge overlap: source:http://ogp.me/ns#description, source:http://purl.org/dc/terms/description, source:http://purl.org/dc/terms/identifier, uogto:https://w3id.org/uogto/core#Agent, uogto:https://w3id.org/uogto/core#description.

The accepted-only and close/related variants let the article report how much network structure depends on conservative review versus permissive relational inclusion.
