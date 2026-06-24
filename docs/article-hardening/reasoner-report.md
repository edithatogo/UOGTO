# UOGTO Ontology-Quality and Reasoner Benchmark

This report is generated from `scripts/maintenance/build_article_hardening_quality.py`.

## Scope

- Ontology files: 49
- SHACL files: 5
- Example files: 17
- Competency queries: 10

## Annotation Completeness

- Classes: 299
- Properties: 204
- Label completeness: 1.0
- Definition completeness: 1.0

## Structural Metrics

- Orphan classes: 1 of 299 (0.0033)
- Object properties: 150
- Datatype properties: 54
- Relation richness, properties per class: 0.6823
- Domain coverage: 0.8235
- Range coverage: 0.8775
- Maximum class hierarchy depth: 3
- Root classes: 2
- Maximum local import depth: 1
- External import count: 0

## SHACL and Example Coverage

- SHACL target class coverage: 0.0535
- SHACL property path coverage: 0.098
- SHACL shape-term coverage: 36 terms
- Example graphs with SHACL links: 17 of 17
- Module shape coverage: 9 of 9
- Modules with examples: 14
- Example files: 17

## Competency Query Coverage

- Executable queries: 10 of 10
- Queries returning results against ontology plus examples: 4
- Queries linked to example graphs: 10
- Example-graph linkage ratio: 1.0
- Modules mentioned by competency queries: 5

## Pitfall Indicators

- Local OOPS-style open issue count: 4
- Missing labels: 0
- Missing definitions: 0

## OWL Profile and Reasoner Status

- RDF parse status: passed
- OWL profile screen: owl2_rl_candidate_syntactic_subset
- OWL profile screen method: local syntactic screen for constructs that require manual OWL profile review
- OWL RL reasoner status: passed
- OWL RL available: True
- PySHACL RDFS example status: passed

## Limitations

The OWL profile check is a deterministic local syntactic screen, not a formal certification by an external OWL profile reasoner. Metrics are intended for article reporting, regression checks, and prioritising ontology improvements.
