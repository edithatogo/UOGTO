# Product Guidelines: UOGTO

## Source of Truth
- Conductor tracks and their `plan.md` files are the operational source of truth for implementation work.
- Canonical ontology source files live under `ontologies/`; generated release artifacts belong under `dist/`.
- Publication metadata must stay consistent across `CITATION.cff`, `.zenodo.json`, release notes, and registry documents.

## Quality Gates
- Every ontology-facing change must pass `make validate`.
- Repository-side changes that affect scripts, metadata, workflows, or release behavior must pass `make test` when feasible.
- Publishing changes must pass `make publishing-metadata`.
- Release and documentation workflows must not publish artifacts before validation, tests, semantic audit, and publishing metadata checks have passed.

## Publishing and Discoverability
- Zenodo DOI minting, LOV submission, and OLS indexing are live external gates and must not be marked complete from repo-side scaffolding alone.
- GitHub Pages documentation must be generated from validated ontology artifacts.
- WIDOCO and other external build tools should be pinned to deterministic versions.
- Registry submission documents must preserve placeholders for DOI or public artifact URLs until those resources are live.

## Maintenance
- Keep changes narrowly scoped to the active Conductor track.
- Preserve archived Conductor tracks as audit history unless deletion is explicitly requested.
- Record meaningful Conductor status and runlog updates for completed implementation or review-hardening work.
