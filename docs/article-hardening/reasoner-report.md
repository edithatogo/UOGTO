# UOGTO Ontology-Quality and Reasoner Benchmark

This report is generated from `scripts/maintenance/build_article_hardening_quality.py`.

## Scope

- Ontology files: 48
- SHACL files: 5
- Example files: 16
- Competency queries: 10

## Annotation Completeness

- Classes: 298
- Properties: 197
- Label completeness: 1.0
- Definition completeness: 1.0

## Structural Metrics

- Orphan classes: 0 of 298 (0.0)
- Object properties: 149
- Datatype properties: 48
- Relation richness, properties per class: 0.6611
- Domain coverage: 0.8173
- Range coverage: 0.8731
- Maximum class hierarchy depth: 3
- Root classes: 1
- Maximum local import depth: 1
- External import count: 0

## SHACL and Example Coverage

- SHACL target class coverage: 0.0537
- SHACL property path coverage: 0.1015
- Modules with examples: 13
- Example files: 16

## Competency Query Coverage

- Executable queries: 10 of 10
- Queries returning results against ontology plus examples: 3
- Modules mentioned by competency queries: 5

## Pitfall Indicators

- Local OOPS-style open issue count: 3
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
