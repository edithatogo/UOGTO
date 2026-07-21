# Specification: Registry Metadata Enrichment

## Overview

This track implements the remaining repository-owned enrichment recommended after the 2026-07 registry review. It makes FAIRsharing and Wikidata enrichment auditable, preserves the current UOGTO namespace and citation policy, and keeps curator-owned decisions explicit.

## Requirements

- Record the current FAIRsharing enrichment candidates: organisation links, publications, citations, and defensible record associations.
- Record which candidates are blocked on curator guidance or a stable native registry field.
- Record Wikidata enrichment candidates only where stable properties and references support them; do not add speculative author, ORCID, or health-domain claims.
- Add a machine-readable status/evidence record and validation coverage for the enrichment decisions.
- Keep the core `uogto` and extension `uogtox` namespaces unchanged.
- Preserve the existing external gates for FAIRsharing curation and registry follow-up issues.

## Out of Scope

- Changing published v1.0.0 IRIs or release assets.
- Inventing FAIRsharing associations or Wikidata statements without authoritative references.
- Claiming curator or maintainer acceptance from a reachable page alone.

## Acceptance Criteria

- FAIRsharing enrichment candidates and blocking conditions are documented in the registry triage record.
- Wikidata enrichment decisions are documented with property-level evidence or an explicit no-action decision.
- Generated registry handoff/status output includes the enrichment decision state.
- Tests validate the new machine-readable fields and preserve namespace/ORCID consistency.
- `make build`, `make validate`, and `make test` pass.
