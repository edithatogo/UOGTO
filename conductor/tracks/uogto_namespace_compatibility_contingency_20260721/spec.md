# Specification: Namespace Compatibility Contingency

## Overview

This track evaluates compatibility options if Bioregistry requires a single namespace. The published `uogto` core and `uogtox` extension IRIs remain authoritative while the compatibility analysis is performed.

## Requirements

- Document the current two-namespace contract and all published consumers.
- Compare non-breaking options: primary-prefix registration only, aliases, generated compatibility contexts, redirects, and a future major-version migration.
- Identify which options preserve RDF identity and which would create new IRIs or require downstream migration.
- Add regression checks that prevent accidental namespace squashing in v1.0 assets and metadata.
- Define a separate migration track trigger if Bioregistry makes namespace squashing an acceptance requirement.

## Out of Scope

- Editing published v1.0.0 IRIs.
- Replacing `uogto`/`uogtox` with a single namespace without a new compatibility decision and release plan.
- Claiming Bioregistry acceptance before maintainer disposition.

## Acceptance Criteria

- A decision record compares compatibility options and recommends a non-breaking default.
- Published namespace and prefix invariants have regression coverage.
- The Bioregistry issue and GitHub issue #95 are cross-referenced.
- A future migration trigger and required evidence are explicit.
- `make build`, `make validate`, and `make test` pass.
