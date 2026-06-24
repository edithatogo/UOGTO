# ROBOT-Style Ontology Report

This report preserves a ROBOT-like reporting surface while keeping RDFLib/pySHACL as the baseline.

## Scope

- Ontology files merged: 49
- Root ontology: `ontologies/core/uogto-core.ttl`
- Java available: True
- ROBOT available: False
- Operating mode: portable-baseline

## Reasoner

- OWL profile screen: owl2_rl_candidate_syntactic_subset
- OWL RL reasoner status: passed
- pySHACL RDFS example status: passed

## Merge

- Root triple count: 307
- Merged triple count: 2327
- Triples added beyond root: 2020

## Import Extraction

- Declared imports found: 0
- Extracted triple count: 307
- Because the ontology files do not currently declare owl:imports, the extracted closure is the root ontology snapshot.

## Quality Snapshot

- Label completeness: 1.0
- Definition completeness: 1.0
- SHACL target class coverage: 0.0535
- SHACL property path coverage: 0.098

## Limitations

- ROBOT-specific execution is deferred until a robot binary or jar is configured.
- The portable baseline remains deterministic and suitable for CI without Java.
