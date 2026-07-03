# Source Acquisition Manifest

Only redistributable or already checked-in comparator artifacts are represented as local files. Licence-constrained, metadata-only, literature-only, and structured non-RDF sources remain as source references with canonical URLs and licence dispositions.

- Local artifacts: 4
- Reference-only sources: 35
- Source inventory: `docs/article-hardening/source-extension-inventory.json`
- Artifact directory: `docs/ontology-comparison/sources`

## Checked-In Artifacts

| Source | Path | Content type | Checksum |
| --- | --- | --- | --- |
| `owl_time` | `docs/ontology-comparison/sources/owl_time.ttl` | `text/turtle` | `sha256:251bd6970b0d7a5efa97ff681afe81a297df85deab3d860fa4f8eeba72d8f16c` |
| `prov_o` | `docs/ontology-comparison/sources/prov_o.owl` | `application/rdf+xml` | `sha256:02a4d7409ee3e1f697a04e4980d8d208a847cc7fa5180ca0d187540abb66919f` |
| `schema_org` | `docs/ontology-comparison/sources/schema_org.ttl` | `text/turtle` | `sha256:320938f0945d717fc317f822c707f10944e7a7a0097018665a3b95dcf475b39d` |
| `ssn_sosa` | `docs/ontology-comparison/sources/ssn_sosa.ttl` | `text/turtle` | `sha256:184d86189191146e314cc52b1bceb96fca11e70aacbc160d71588102a5153eb9` |

## Reference-Only Sources

| Source | Evidence level | Reason |
| --- | --- | --- |
| `bfo` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `bpmn_2` | `structured_non_rdf` | Standards licensing may prevent local redistribution. |
| `cellml` | `structured_non_rdf` | Domain-specific standard; avoid treating it as game-theory evidence. |
| `devs` | `structured_non_rdf` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `dolce` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `emmo` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `fmi` | `structured_non_rdf` | Interface standard, not a standalone ontology source. |
| `game_ontology_project` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `gdl_ii_iii_gdlz` | `literature_only` | Likely literature-only until a stable public specification artifact is acquired. |
| `gdlf_gamelan` | `structured_non_rdf` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `gvgai_vgdl` | `structured_non_rdf` | Benchmark artifacts vary by version and repository; record exact release before acquisition. |
| `hla_fom` | `structured_non_rdf` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `kaos` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `kisao` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `ludii` | `structured_non_rdf` | Licence and corpus redistribution need review before source acquisition. |
| `miase` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `modelica` | `structured_non_rdf` | Language/library evidence should be charted separately from ontology evidence. |
| `oaei` | `metadata_only` | Benchmark tracks are heterogeneous and not a single ontology source. |
| `odd_protocol` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `ontouml_ufo` | `structured_non_rdf` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `osmo` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `owl_s` | `metadata_only` | Recorded as metadata-only until a specific OWL file, checksum, and licence are captured. |
| `p_plan` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `pddl` | `structured_non_rdf` | Not a game ontology; relevance should be limited to action/execution semantics. |
| `pnml` | `structured_non_rdf` | Use metadata until standard/schema licence and exact version are captured. |
| `robot` | `metadata_only` | Method/tool source rather than a comparator ontology; use for methods, not overlap counts. |
| `sbgn` | `structured_non_rdf` | Notation standard, not a direct ontology-alignment target at this phase. |
| `sbml` | `structured_non_rdf` | Systems-biology standard; article claims should distinguish biological modelling context from general game-theory scope. |
| `sbo` | `metadata_only` | Recorded as metadata-only until artifact URL and licence are pinned. |
| `sed_ml` | `structured_non_rdf` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `sssom` | `structured_non_rdf` | Specification fields can evolve; TSV outputs should keep a documented SSSOM version and local validation. |
| `stanford_gdl` | `literature_only` | Use metadata/literature unless a redistributable grammar or corpus is explicitly acquired later. |
| `sysml` | `structured_non_rdf` | Likely too broad for term-level mapping without a narrow use case. |
| `vimmp_ontologies` | `metadata_only` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
| `xmile` | `structured_non_rdf` | Imported from completed ontology-comparison baseline; licence and acquisition status remain as recorded there. |
