# Implementation Plan: Registry Metadata Enrichment

## Phase 1: Evidence Baseline

- [x] Task: Capture current FAIRsharing and Wikidata evidence
  - [x] Record live URLs, known metadata, and current curator/indexing uncertainty.
  - [x] List candidate organisation, publication, citation, and association fields.
  - [x] List Wikidata candidate properties and the evidence required for each.
- [x] Task: Phase verification checkpoint

## Phase 2: Repository Implementation

- [x] Task: Extend machine-readable registry triage metadata
  - [x] Add enrichment candidates, decisions, owners, and acceptance criteria.
  - [x] Keep external-review and account-gated states fail-closed.
- [x] Task: Update human-readable registry documentation and release handoff guidance.
- [x] Task: Add regression tests for enrichment metadata and namespace/ORCID invariants.
- [x] Task: Phase verification checkpoint

## Phase 3: Validation and Closeout

- [x] Task: Run `make build`, `make validate`, `make test`, registry packet generation, and link checks.
- [x] Task: Reconcile GitHub issue #93, Project #8, `conductor/status.md`, and `conductor/runlog.md`.
- [x] Task: Phase verification checkpoint
