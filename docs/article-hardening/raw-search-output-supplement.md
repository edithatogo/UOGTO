# Repository-only raw search output supplement

Date: 2026-07-02

This supplement preserves the raw source-discovery outputs behind the UOGTO manuscript's source-discovery, screening, comparative mapping, and narrowing claims. It is a repository evidence artefact only: it does not need to be submitted with the arXiv preprint or a journal manuscript. Its purpose is to let a GitHub reader trace the manuscript counts back to the raw search records and retained source rows.

Primary machine-readable sources:

- `docs/article-hardening/search-log.jsonl`
- `docs/article-hardening/source-extension-inventory.json`
- `docs/article-hardening/source-extension-inventory.md`
- `docs/ontology-comparison/source-inventory.json`
- `docs/ontology-comparison/term-inventory.jsonl`
- `docs/ontology-comparison/mapping-candidates.jsonl`
- `docs/ontology-comparison/mapping-review.csv`
- `docs/ontology-comparison/accepted-alignments.sssom.tsv`
- `docs/article-hardening/candidate-decision-ledger.md`
- `docs/article-hardening/candidate-decision-ledger.csv`
- `docs/article-hardening/candidate-decision-ledger.json`
- `docs/article-hardening/ontology-snapshot-supplement.md`
- `docs/article-hardening/ontology-citation-register.md`
- `docs/article-hardening/network-graph-visualisation-supplement.md`

## How To Read This Supplement

The raw search output is deliberately broader than the manuscript comparison set.

1. Search routes record what was found or preserved at the source-discovery stage.
2. Source-extension records preserve the 39 retained source rows and their evidence levels.
3. The comparative ontology subset narrows the evidence to 21 source families used for term extraction and mapping.
4. Term extraction yields 4,046 rows: 3,468 external RDF rows, 17 external metadata rows, and 561 UOGTO rows.
5. Mapping review narrows 460 candidates to 12 accepted alignments, 0 domain-review rows, and 448 rejected or non-asserted rows.
6. The candidate decision ledger joins route, source, mapping, and ontology-inclusion decisions into one row-level audit table with recorded rationales and heuristics.

This is a scoping-review-style evidence trail, not a claim that all 39 retained source rows were parsed as ontology files or that all 4,046 term rows represent missing UOGTO concepts.

## Raw Search Route Outputs

| Search record | Surface type | Evidence level | Query or route | Raw results | Screened | Included | Raw retained source IDs |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| `phase2-baseline-comparison` | `baseline_artifact` | `mixed` | Import completed comparative simulation ontology mapping inventory as Phase 2 baseline. | 21 | 21 | 21 | `bfo`, `devs`, `dolce`, `emmo`, `game_ontology_project`, `gdlf_gamelan`, `hla_fom`, `kaos`, `kisao`, `miase`, `odd_protocol`, `ontouml_ufo`, `osmo`, `owl_time`, `p_plan`, `prov_o`, `schema_org`, `sed_ml`, `ssn_sosa`, `vimmp_ontologies`, `xmile` |
| `phase2-mapping-standards` | `web_search` | `metadata_only` | SSSOM ROBOT OAEI ontology mapping standard review publication. | 3 | 3 | 3 | `oaei`, `robot`, `sssom` |
| `phase2-game-description` | `project_site` | `structured_non_rdf` | GDL GDL-II GDL-III GDLZ Ludii VGDL General Video Game AI game description language. | 4 | 4 | 4 | `gdl_ii_iii_gdlz`, `gvgai_vgdl`, `ludii`, `stanford_gdl` |
| `phase2-simulation-standards` | `standards_body` | `structured_non_rdf` | PNML BPMN OWL-S PDDL Petri net process planning ontology simulation standard. | 4 | 4 | 4 | `bpmn_2`, `owl_s`, `pddl`, `pnml` |
| `phase2-systems-biology` | `standards_body` | `structured_non_rdf` | SBML SBO CellML SBGN SED-ML KiSAO MIASE simulation ontology standard. | 4 | 4 | 4 | `cellml`, `sbgn`, `sbml`, `sbo` |
| `phase2-physical-modelling` | `standards_body` | `structured_non_rdf` | Modelica FMI SysML co-simulation physical modelling ontology standard. | 3 | 3 | 3 | `fmi`, `modelica`, `sysml` |
| `phase2-negative-evidence` | `web_search` | `excluded` | Game theory ontology OR game theory OWL OR game theory RDF registry repository. | 0 | 0 | 0 | None; negative evidence route preserved. |

Route totals:

- Search records: 7
- Raw route results: 39
- Screened route records: 39
- Included route records: 39
- Negative-evidence routes: 1 route, 0 included sources

## Retained Source Rows Before Narrowing

The source-extension inventory retains 39 source rows across 27 source families. Evidence levels are intentionally mixed:

| Evidence level | Count | Interpretation |
| --- | ---: | --- |
| `parsed_rdf_owl` | 4 | Source has parsed RDF/OWL evidence in the comparison package. |
| `structured_non_rdf` | 18 | Source has structured standards, schema, language, or formalism evidence but is not redistributed as parsed RDF/OWL here. |
| `metadata_only` | 15 | Source is represented by descriptive metadata, registry, landing-page, or standards-page evidence. |
| `literature_only` | 2 | Source is represented through literature or documentation evidence. |

| Source ID | Source name | Evidence level | Parseability | Article-use category | Search record |
| --- | --- | --- | --- | --- | --- |
| `bfo` | Basic Formal Ontology | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `bpmn_2` | Business Process Model and Notation 2.0 | `structured_non_rdf` | `structured_non_rdf` | `process-formalism-comparator` | `phase2-simulation-standards` |
| `cellml` | CellML | `structured_non_rdf` | `structured_non_rdf` | `simulation-standard-comparator` | `phase2-systems-biology` |
| `devs` | DEVS formalism and DEVS metamodel resources | `structured_non_rdf` | `structured_non_rdf` | `baseline-comparator` | `phase2-baseline-comparison` |
| `dolce` | DOLCE | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `emmo` | European Materials and Modelling Ontology | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `fmi` | Functional Mock-up Interface | `structured_non_rdf` | `structured_non_rdf` | `simulation-interoperability-comparator` | `phase2-physical-modelling` |
| `game_ontology_project` | Game Ontology Project | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `gdl_ii_iii_gdlz` | GDL-II, GDL-III, and GDLZ variants | `literature_only` | `literature_or_documentation` | `game-formalism-comparator` | `phase2-game-description` |
| `gdlf_gamelan` | Game Description Language and GDL resources | `structured_non_rdf` | `structured_non_rdf` | `baseline-comparator` | `phase2-baseline-comparison` |
| `gvgai_vgdl` | General Video Game AI and VGDL resources | `structured_non_rdf` | `structured_non_rdf` | `game-ai-comparator` | `phase2-game-description` |
| `hla_fom` | High Level Architecture Federation Object Model resources | `structured_non_rdf` | `structured_non_rdf` | `baseline-comparator` | `phase2-baseline-comparison` |
| `kaos` | KAoS ontology and policy services | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `kisao` | Kinetic Simulation Algorithm Ontology | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `ludii` | Ludii general game system | `structured_non_rdf` | `structured_non_rdf` | `game-formalism-comparator` | `phase2-game-description` |
| `miase` | Minimum Information About a Simulation Experiment | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `modelica` | Modelica language and Modelica Standard Library | `structured_non_rdf` | `structured_non_rdf` | `simulation-language-comparator` | `phase2-physical-modelling` |
| `oaei` | Ontology Alignment Evaluation Initiative | `metadata_only` | `metadata_only` | `mapping-method-context` | `phase2-mapping-standards` |
| `odd_protocol` | ODD protocol for agent-based models | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `ontouml_ufo` | OntoUML / Unified Foundational Ontology | `structured_non_rdf` | `structured_non_rdf` | `baseline-comparator` | `phase2-baseline-comparison` |
| `osmo` | Ontology for Simulation, Modelling, and Optimization | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `owl_s` | OWL-S Semantic Markup for Web Services | `metadata_only` | `parsed_rdf_owl_candidate` | `process-ontology-comparator` | `phase2-simulation-standards` |
| `owl_time` | OWL-Time | `parsed_rdf_owl` | `parsed_rdf_owl_candidate` | `baseline-comparator` | `phase2-baseline-comparison` |
| `p_plan` | P-Plan ontology | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `pddl` | Planning Domain Definition Language | `structured_non_rdf` | `structured_non_rdf` | `action-formalism-comparator` | `phase2-simulation-standards` |
| `pnml` | Petri Net Markup Language | `structured_non_rdf` | `structured_non_rdf` | `simulation-formalism-comparator` | `phase2-simulation-standards` |
| `prov_o` | PROV-O | `parsed_rdf_owl` | `parsed_rdf_owl_candidate` | `baseline-comparator` | `phase2-baseline-comparison` |
| `robot` | ROBOT ontology tool | `metadata_only` | `metadata_only` | `quality-method-candidate` | `phase2-mapping-standards` |
| `sbgn` | Systems Biology Graphical Notation | `structured_non_rdf` | `structured_non_rdf` | `notation-context` | `phase2-systems-biology` |
| `sbml` | Systems Biology Markup Language | `structured_non_rdf` | `structured_non_rdf` | `simulation-standard-comparator` | `phase2-systems-biology` |
| `sbo` | Systems Biology Ontology | `metadata_only` | `parsed_rdf_owl_candidate` | `ontology-comparator` | `phase2-systems-biology` |
| `schema_org` | schema.org | `parsed_rdf_owl` | `parsed_rdf_owl_candidate` | `baseline-comparator` | `phase2-baseline-comparison` |
| `sed_ml` | Simulation Experiment Description Markup Language | `structured_non_rdf` | `structured_non_rdf` | `baseline-comparator` | `phase2-baseline-comparison` |
| `ssn_sosa` | SSN/SOSA | `parsed_rdf_owl` | `parsed_rdf_owl_candidate` | `baseline-comparator` | `phase2-baseline-comparison` |
| `sssom` | Simple Standard for Sharing Ontological Mappings (SSSOM) | `structured_non_rdf` | `structured_non_rdf` | `mapping-publication-standard` | `phase2-mapping-standards` |
| `stanford_gdl` | Stanford Game Description Language | `literature_only` | `literature_or_documentation` | `game-formalism-comparator` | `phase2-game-description` |
| `sysml` | Systems Modeling Language | `structured_non_rdf` | `structured_non_rdf` | `systems-modelling-context` | `phase2-physical-modelling` |
| `vimmp_ontologies` | Virtual Materials Marketplace Ontologies | `metadata_only` | `metadata_only` | `baseline-comparator` | `phase2-baseline-comparison` |
| `xmile` | XMILE System Dynamics Standard | `structured_non_rdf` | `structured_non_rdf` | `baseline-comparator` | `phase2-baseline-comparison` |

## Narrowing From Raw Sources To Manuscript Counts

| Stage | Count | File evidence | Manuscript interpretation |
| --- | ---: | --- | --- |
| Raw search/source route results | 39 | `docs/article-hardening/search-log.jsonl` | Broad source-discovery register. |
| Retained source-extension rows | 39 | `docs/article-hardening/source-extension-inventory.json` | Evidence-levelled source register. |
| Comparative source subset | 21 sources / 17 families | `docs/ontology-comparison/source-inventory.json` | Candidate sources used for ontology comparison and term extraction. |
| Normalized term rows | 4,046 | `docs/ontology-comparison/term-inventory.jsonl` | 3,468 external RDF rows, 17 external metadata rows, and 561 UOGTO rows. |
| Mapping candidates | 460 | `docs/ontology-comparison/mapping-candidates.jsonl` | Deterministic candidate surface for review. |
| Reviewed mapping rows | 460 | `docs/ontology-comparison/mapping-review.csv` | 12 accepted, 0 domain-review, 448 rejected or non-asserted rows. |
| Accepted alignments | 12 | `docs/ontology-comparison/accepted-alignments.sssom.tsv`; `docs/ontology-comparison/accepted-alignments.ttl` | Conservative crosswalks emitted for reuse. |
| Unified candidate decision ledger | 511 | `docs/article-hardening/candidate-decision-ledger.csv`; `.json`; `.md` | Route, source, mapping, and ontology-inclusion candidate decisions with rationales and heuristics. |
| Ontology copy for review | 49 source files / 5 release-copy assets | `docs/article-hardening/ontology-snapshot-supplement.md`; `dist/uogto.ttl` | Compact copy and modular source ledger for the ontology being discussed. |
| Ontology citation register | 19 reference records | `docs/article-hardening/ontology-citation-register.md`; `.json` | Final corresponding references for the ontology and manuscript evidence package. |

## Route-To-Manuscript Interpretation

The narrowing steps support the manuscript's restrained claims:

- The 39 raw retained rows describe discovery breadth and evidence heterogeneity.
- The 21-source comparative subset describes the material actually used for ontology comparison.
- The 4,046 term rows describe extraction breadth, not unmodelled game-theory concepts.
- The 460 mapping candidates describe a review surface, not asserted equivalence.
- The 12 accepted alignments describe conservative reusable mappings.
- Rejected rows, metadata-only rows, and the negative-evidence route are preserved so readers can inspect omissions and non-assertions.
- The ontology snapshot supplement identifies the compact ontology copy and checksums corresponding to these counts.
- The ontology citation register identifies the final reference set corresponding to the ontology evidence package.

## Repository Citation

Use this supplement when citing the repository evidence trail behind the manuscript's search and narrowing claims:

> UOGTO repository-only raw search output supplement, `docs/article-hardening/raw-search-output-supplement.md`, with machine-readable route and source records in `docs/article-hardening/search-log.jsonl` and `docs/article-hardening/source-extension-inventory.json`.

This supplement should be linked from GitHub-facing documentation, but not bundled into the arXiv source tarball or journal submission package unless a reviewer specifically asks for the raw source-discovery ledger.
