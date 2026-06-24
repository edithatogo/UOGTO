# UOGTO Modelling Decisions

This page explains why some concepts are represented as classes, properties, individuals, or SHACL-only constraints.

## 1. Classes

Use a class when the concept represents a reusable kind of thing with multiple possible instances.

Examples:

- `uogto:GameSpecification`
- `uogto:GameInstance`
- `uogto:PlaySession`
- `uogto:EventTrace`
- `uogto:Strategy`
- `uogto:Action`
- `uogto:Outcome`
- `uogto:Payoff`

Why this choice works:

- It supports reuse across modules and examples.
- It keeps the ontology open to future instances.
- It lets SHACL validate specific example constraints without closing the class definition.

## 2. Object Properties

Use an object property when the concept is a relationship between two resources.

Examples:

- `uogto:hasPlayer`
- `uogto:hasStrategy`
- `uogto:hasAction`
- `uogto:hasOutcome`
- `uogto:emitsEventTrace`
- `uogto:hasGovernanceRecord`

Why this choice works:

- Relationships remain explicit and queryable.
- The same relation can be reused across modules.
- Domains and ranges can stay open where that supports reuse.

## 3. Datatype Properties

Use a datatype property when the concept points to a literal value such as a label, number, date, or URI string.

Examples:

- `uogto:payoffValue`
- `uogto:timeIndex`
- `uogto:timestamp`
- `uogto:sourceReference`
- `uogto:reviewDate`

Why this choice works:

- Literal values are simple and interoperable.
- Numeric and date fields stay easy to query and validate.
- Operational metadata stays separate from structural relationships.

## 4. Individuals

Use an individual when the repo needs one canonical named thing rather than a reusable type.

Examples:

- A specific governance record such as `uogto:currentGovernanceRecord`
- A release-specific metadata node when the project needs a stable reference
- A canonical example instance where the exact resource matters more than the class it belongs to

Why this choice works:

- It gives downstream documents a stable identifier.
- It avoids turning singleton metadata into a pseudo-class.
- It makes release and governance facts easy to reference directly.

## 5. SHACL-only Constraints

Use SHACL when the requirement is about validation rather than ontology meaning.

Examples:

- A shape that requires at least one example graph for a competency question
- A closed-world rule that checks the number of bindings in a sample graph
- A release checklist rule that is specific to generated artefacts
- A module-specific constraint that should not become a global OWL axiom

Why this choice works:

- OWL stays open-world and reusable.
- Validation can be stricter where needed.
- Example data can be checked without overcommitting the ontology semantics.

## 6. Decision Rule

When choosing between an OWL term and a SHACL rule, ask whether the statement is part of the domain model or part of a validation expectation.

- Domain model statement: usually a class or property.
- Single named record: usually an individual.
- Validation expectation: usually SHACL.

## 7. Practical Test

Before adding a new term, check the following:

1. Does the term need multiple instances? If yes, make it a class.
2. Does it connect two resources? If yes, make it an object property.
3. Does it connect to a literal? If yes, make it a datatype property.
4. Is it a singleton record or release anchor? If yes, consider an individual.
5. Is it a constraint or quality check? If yes, prefer SHACL.

## 8. Cross-References

- [Ontology design principles](ontology-design-principles.md)
- [Ontology design patterns](ontology-design-patterns.md)
- [Glossary](glossary.md)