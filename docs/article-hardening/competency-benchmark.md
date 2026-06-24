# Competency Benchmark

This benchmark defines the ontology-quality checks used to compare UOGTO modules and related simulation ontologies.

## Metrics
- Annotation completeness: proportion of classes and properties with both `rdfs:label` and `skos:definition`.
- Orphan classes: classes with no parent or no meaningful module attachment.
- Relation richness: object-property density per module.
- Hierarchy depth: maximum and average subclass depth.
- Import depth: depth and breadth of imported ontologies.
- SHACL coverage: proportion of example graphs covered by shapes.
- Examples per module: number of worked examples per module.
- Competency-query coverage: proportion of questions answered by examples or queries.
- OWL profile status: profile conformity and reasoner status.

## Output Expectation
The benchmark is intended to be reported in `docs/article-hardening/quality-metrics.json` and summarized in article tables and figures. It is a protocol surface, not a final results claim.