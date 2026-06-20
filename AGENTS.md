# AGENTS.md

## Project Scope
UOGTO (Universal Open Game Theory Ontology) is a modular, version-controlled repository defining game-theoretic semantics, including classical, cooperative, multi-agent, simulation execution, mechanism design, and executable knowledge graph semantics.

## Ontology Design Rules
1. **Namespaces**: Core: `https://w3id.org/uogto/core#` (prefix `uogto:`). Extensions: `https://w3id.org/uogto/extensions#` (prefix `uogtox:`).
2. **Metadata**: Use `rdfs:label` and `skos:definition` on every class and property.
3. **Properties**: Maintain clean separation between ObjectProperties and DatatypeProperties. Keep domains/ranges open where it helps reuse, but use SHACL shapes to validate specific invariants in closed-world contexts.
4. **Separation of Concerns**: Separate game specification, instance, session, trace, strategy, action, payoff, outcomes, and execution bindings.

## Naming Conventions
- Classes: UpperCamelCase (e.g. `GameSpecification`, `NormalFormGame`)
- Properties: lowerCamelCase (e.g. `hasPlayer`, `payoffValue`)
- Instances: kebab-case (e.g. `prisoners-dilemma`, `defect`)

## Validation Requirements
- All TTL files must parse using RDFLib.
- Examples must validate against SHACL shapes using PySHACL.
- Competency queries must return correct results against examples.
- Before reporting completion on any task, run `make validate` or `make test`.

## Definition of Done (DoD)
- The module is fully implemented in its respective `.ttl` file.
- Classes/properties are fully annotated with labels and definitions.
- Corresponding SHACL shapes are defined and tests cover them.
- Example instances demonstrate the module's usage.
- Competency queries verify model retrieval.
- `make validate` and `make test` pass locally.
- `.conductor/status.md` and `.conductor/runlog.md` are updated.

## Subagent Delegation
- **Ontology Architect**: Design ontology structure, hierarchies, and module splits.
- **RDF/OWL Engineer**: Code OWL class hierarchies, properties, and constraints.
- **SHACL Validation Engineer**: Build SHACL shapes for data validation.
- **JSON-LD/Schema Engineer**: Build and map context files.
- **Examples/Competency Questions Engineer**: Design test instances and SPARQL queries.
- **Documentation/Release Engineer**: Update documentation files, readmes, and changelogs.
- **Reviewer/QA Agent**: Run validators, test coverage, and code quality tools.
