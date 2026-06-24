# Comparative Simulation Ontology Mapping Report

## Scope
This report summarises the reproducible comparison of public game-theory, simulation, agent-based modelling, system-dynamics, and adjacent modelling ontologies against UOGTO. It is generated from the track artifacts in `docs/ontology-comparison/`.

## Methodology
The workflow uses the discovery protocol, source inventory, source provenance, normalized term inventory, deterministic mapping candidates, reviewed mappings, overlap metrics, and network analysis artifacts. Redistributable RDF sources are parsed directly; non-redistributable or standards-document sources are represented as metadata-only or transformed-summary records so the report does not overclaim source access.

## Source Inventory
- Candidate sources: 21
- External terms: 3485
- UOGTO terms: 552
- Review candidates: 460
- Accepted mappings: 10

## Mapping Review Results
- Accepted: 10
- Needs domain review: 1
- Rejected: 449

The accepted alignment TTL is evidence-backed by `mapping-review.csv`. Candidate and rejected rows remain audit records and should not be treated as asserted ontology alignments.

## Overlap Findings
| Source | Unmatched terms | Candidate coverage |
| --- | ---: | ---: |
| `schema_org` | 3175 | 0.0137 |
| `owl_time` | 73 | 0.2474 |
| `prov_o` | 57 | 0.4466 |
| `ssn_sosa` | 26 | 0.4694 |
| `bfo` | 1 | 0.0 |
| `devs` | 1 | 0.0 |
| `dolce` | 1 | 0.0 |
| `emmo` | 1 | 0.0 |

## Network Findings
- Source graph nodes: 74
- Term-alignment bipartite edges: 10
- Source-similarity edges: 391
- UOGTO module coverage edges: 11

| Central source or module | Centrality score |
| --- | ---: |
| `uogto_extensions_mean-field-games` | 32 |
| `uogto_extensions_cooperative` | 31 |
| `uogto_extensions_network-games` | 30 |
| `uogto_extensions_congestion-routing-games` | 29 |
| `uogto_extensions_evolutionary-games` | 28 |
| `uogto_extensions_compositional-open-games` | 27 |
| `uogto_extensions_epistemic-games` | 27 |
| `uogto_extensions_causal-games` | 26 |

## Visualisations
- ![source_sizes_bar.svg](figures/source_sizes_bar.svg)
- ![match_classes_bar.svg](figures/match_classes_bar.svg)
- ![source_module_overlap_heatmap.svg](figures/source_module_overlap_heatmap.svg)
- ![uogto_coverage_treemap.svg](figures/uogto_coverage_treemap.svg)
- ![source_similarity_network.svg](figures/source_similarity_network.svg)
- ![mapping_flow_sankey.svg](figures/mapping_flow_sankey.svg)
- ![reviewer_workload.svg](figures/reviewer_workload.svg)

## Recommended UOGTO Follow-Up Work
1. Treat accepted mappings as stable crosswalk evidence and keep `accepted-alignments.ttl` in sync with any future review edits.
2. Prioritise high-volume unmatched sources as candidate extension-review areas rather than immediate equivalence assertions.
3. Use `needs_domain_review` mappings as reviewer work queues for ontology architects and domain experts.
4. Keep metadata-only standards separate from parsed RDF sources until their licences and formal artifacts permit stronger comparison.
5. Re-run `make ontology-comparison-visuals` after any source, mapping, overlap, or network artifact changes.

## Reproducibility
Run `make ontology-comparison-visuals` to regenerate this report and the SVG figures from the JSON/CSV artifacts. The report intentionally separates accepted alignments from candidates and future-work recommendations.
