# Bioregistry Namespace and ORCID Response

## Overview

Resolve the Bioregistry maintainer feedback for UOGTO prefix registration by
deciding how to present UOGTO's core and extension namespace policy, preparing
the external response, and updating local publication-follow-up evidence after
the response is posted or a follow-up modelling decision is opened.

## Functional Requirements

- Review the Bioregistry feedback in issue 1999 and the local namespace policy
  documented for UOGTO.
- Decide whether to defend the current two-namespace design
  (`https://w3id.org/uogto/core#` and `https://w3id.org/uogto/extensions#`) or
  open a separate namespace-consolidation follow-up.
- Prepare a concise Bioregistry response grounded in the documented UOGTO
  namespace policy and current publication metadata.
- Provide ORCID metadata only when it is approved and intentionally public; do
  not infer or invent contributor identifiers.
- Update `docs/registry/publication-follow-up-triage.json` and
  `docs/registry/publication-follow-up-triage.md` after the response,
  decision, or follow-up issue is recorded.

## Acceptance Criteria

- A clear namespace response decision is recorded with rationale.
- Bioregistry issue 1999 has either a posted UOGTO response or a documented
  reason why maintainer-facing response is blocked pending identity approval.
- Any ORCID handling is explicitly sourced from approved public metadata or
  omitted with a stated reason.
- Local triage documentation reflects the latest Bioregistry status and links
  to the external evidence.
- `make registry-links`, `make publication-status`, and focused registry tests
  pass after local documentation updates.

## Out of Scope

- Changing UOGTO namespace IRIs without a separate ontology-compatibility track.
- Republishing release assets unless the namespace decision exposes a material
  metadata defect.
- Supplying private contributor metadata or unsourced identifiers.

