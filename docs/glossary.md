# UOGTO Glossary

This glossary uses the terms as they are applied in the repository, not as a separate ontology.

## Core Terms

- **Ontology**: The full UOGTO release set, including core modules, extension modules, alignments, SHACL shapes, JSON-LD contexts, examples, competency questions, and release assets.
- **Module**: A focused Turtle file that models one slice of the domain, such as games, strategies, outcomes, or a specific extension area.
- **Game specification**: The abstract rule structure for a game, independent of any single run.
- **Game instance**: A concrete instantiation of a game specification.
- **Session**: A run, episode, or execution event that records what happened.
- **Trace**: A time-ordered record of observed events or actions.
- **Strategy**: A planned course of action available to a player or agent.
- **Action**: A local choice made at a decision point.
- **Outcome**: The result of interaction.
- **Payoff**: The value assigned to an outcome for a player or agent.
- **Mechanism**: A rule-governed interaction structure that constrains incentives, allocation, or matching.
- **Alignment**: A document that maps UOGTO terms to an external ontology or standard.
- **SHACL shape**: A closed-world constraint used to validate example graphs and specific modelling assumptions.
- **Competency question**: A SPARQL query used to test whether the ontology can answer a required information need.
- **Release asset**: A generated file distributed with the release, such as merged ontology files, contexts, checksums, or handoff packets.

## Modelling Vocabulary

- **Class**: A category of things that can have instances.
- **Object property**: A relation between two resources.
- **Datatype property**: A relation from a resource to a literal value.
- **Individual**: A named instance used when a single canonical entity needs to be referenced.
- **Annotation property**: Metadata attached to ontology terms or documents.
- **SHACL-only constraint**: A validation rule that should not be encoded as core OWL semantics because it is closed-world, example-specific, or operational rather than ontological.

## Reading Tip

If a term can have many instances, it is usually a class. If it links resources, it is usually an object property. If it links to a literal, it is usually a datatype property. If it is a single canonical record, it may be an individual. If it is a validation rule rather than a domain claim, it belongs in SHACL.