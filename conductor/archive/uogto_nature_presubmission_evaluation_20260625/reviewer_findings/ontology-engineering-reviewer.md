# Ontology Engineering Review

## Role

Assess whether UOGTO meets high-quality OWL/RDF/SHACL ontology engineering standards.

## Required Checks

- OWL/RDF syntax, class/property separation, domains/ranges, imports, and profile status.
- Annotation completeness for labels and definitions.
- Orphan classes, hierarchy depth, relation richness, examples per module, and competency-query coverage.
- SHACL coverage for examples, modules, and competency-question links.
- Governance metadata, term-level changelog, deprecation policy, source evidence, and review maturity.
- SSSOM mapping outputs alongside TTL alignments.

## Findings

Pending.

## Required Output

- Ontology engineering score out of 100.
- Must-fix modelling issues.
- Validation and reasoner risks.
- Mapping and governance recommendations.


## 2026-06-25 Executed Review
- Score: 86 out of 100. Core ontology modules parse and examples validate under SHACL through make validate.
- Must improve before Nature submission: add a compact module audit table covering labels definitions SHACL coverage examples competency-question links OWL profile and reasoner status.
