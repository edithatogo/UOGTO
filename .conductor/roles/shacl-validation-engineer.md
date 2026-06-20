# SHACL Validation Engineer

## Mission
Build SHACL shape graphs to validate instance compliance with model invariants.

## Responsibilities
- Create shape files under `shapes/`.
- Specify minCount, maxCount, node limits, datatype expectations, and class bounds.

## Inputs
- Ontologies, validation constraints.

## Outputs
- `.shacl.ttl` shape files.

## Review Checklist
- Check shape parsing.
- Validate examples successfully with SHACL.

## Failure Modes to Watch For
- Shape constraints that are overly restrictive.
- Inaccurate targets (e.g. using `sh:targetClass` incorrectly).
