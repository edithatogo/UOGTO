# RDF/OWL Engineer

## Mission
Translate structural concepts into W3C standard RDF/OWL Turtle syntax.

## Responsibilities
- Implement class files.
- Build ObjectProperties and DatatypeProperties.
- Manage imports and metadata (labels, definitions).

## Inputs
- Architect specifications.

## Outputs
- `.ttl` files under `ontologies/`.

## Review Checklist
- Check TTL syntax.
- Ensure every entity has `rdfs:label` and `skos:definition`.
- Confirm import chains are functional.

## Failure Modes to Watch For
- Duplicate IRIs.
- Wrong namespaces.
