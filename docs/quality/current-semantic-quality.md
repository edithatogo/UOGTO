# UOGTO Ontology-Quality and Reasoner Benchmark

This report is generated from `scripts/maintenance/build_article_hardening_quality.py`.

## Scope

- Ontology files: 54
- SHACL files: 8
- Example files: 30
- Competency queries: 21

## Annotation Completeness

- Classes: 307
- Properties: 211
- Label completeness: 1.0
- Definition completeness: 1.0

## Structural Metrics

- Orphan classes: 1 of 307 (0.0033)
- Object properties: 157
- Datatype properties: 54
- Relation richness, properties per class: 0.6873
- Domain coverage: 0.7962
- Range coverage: 0.8626
- Maximum class hierarchy depth: 4
- Root classes: 2
- Maximum local import depth: 1
- External import count: 0

## SHACL and Example Coverage

- SHACL target class coverage: 0.0749
- SHACL property path coverage: 0.1564
- SHACL shape-term coverage: 60 terms
- Example graphs with SHACL links: 30 of 30
- Module shape coverage: 17 of 17
- Modules with examples: 25
- Example files: 30

## Competency Query Coverage

- Executable queries: 21 of 21
- Queries returning results against ontology plus examples: 21
- Queries linked to example graphs: 21
- Example-graph linkage ratio: 1.0
- Modules mentioned by competency queries: 15

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
