# Registry and Publication Follow-Through

## Overview

Continue post-release publication monitoring until external registry and
discoverability surfaces reach a clear accepted, rejected, or follow-up-needed
state. This keeps external review separate from local implementation completion.

## Functional Requirements

- Monitor LOV, OLS, Ontobee, Bioregistry, FAIRsharing, Wikidata, Zenodo, GitHub Pages, and w3id status.
- Convert external feedback into scoped Conductor tasks or ontology metadata patches.
- Keep `docs/registry/`, release notes, and publication-status packets current.
- Avoid treating external maintainer review as a local validation failure unless required metadata is wrong.

## Acceptance Criteria

- `make publication-status-live`, `make registry-links`, and `make publishing-metadata` pass or record explicit external blockers.
- All external review feedback is triaged with owner, target artifact, and acceptance criterion.
- Registry documentation states the current status and last verification date.

## Out of Scope

- Republishing v1.0.0 unless release assets are materially wrong.
- Changing ontology semantics purely to satisfy a registry display preference.
