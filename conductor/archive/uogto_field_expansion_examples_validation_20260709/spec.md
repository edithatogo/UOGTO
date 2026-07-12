# Specification: Field Expansion Examples and Validation

## Overview

This track covers GitHub issues #76-#83. It converts manuscript future-work
language into a staged implementation programme for worked examples, SHACL
checks, competency questions, source/mapping decisions, and applied extension
pack boundaries.

## Scope

- Mean-field games (#77).
- Network and congestion-routing games (#78).
- Evolutionary games (#79).
- Institutional economics and information design (#80).
- Learning in games, MARL, and agent-policy coverage (#81).
- Trust, reputation, and provenance-facing coverage (#82).
- Applied extension-pack scoping for health economics, medical decision
  modelling, safety systems, and genomic-policy use cases (#83).

## Out of Scope

- Bulk-importing external terms without example, validation, and decision-ledger
  support.
- Treating graph centrality in the manuscript as proof of module maturity.
- Turning UOGTO core into a domain ontology for health, safety, genomics, or
  policy-specific evidence standards.

## Acceptance Criteria

- Each implementation slice adds at least one worked example graph.
- Each implementation slice adds SHACL checks for relevant invariants.
- Each implementation slice adds or updates competency queries and expected
  results.
- Each implementation slice records accepted, external-alignment, deferred,
  rejected, and domain-review decisions.
- `make build`, `make validate`, and `make test` pass before the slice is
  closed.

