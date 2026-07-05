# Implementation Plan: Registry and Publication Follow-Through

## Phase 1: Live Status Refresh

- [x] Task: Refresh external publication observations
    - [x] Run live publication-status, DOI, w3id, and registry link checks.
    - [x] Compare generated status packets with checked-in release documentation.
    - [x] Record any external-state changes in Conductor status and registry docs.

## Phase 2: Feedback Triage

- [x] Task: Review external registry queues
    - [x] Check LOV and OLS issue status.
    - [x] Check Ontobee and Bioregistry request status.
    - [x] Check FAIRsharing curator state and Wikidata metadata.
- [x] Task: Convert feedback into scoped patches
    - [x] Classify feedback as metadata-only, ontology-semantic, documentation, or no-action.
    - [x] Add follow-up subtasks or issues for any required changes.

## Phase 3: Verification

- [x] Task: Verify publication coherence
    - [x] Run `make publishing-metadata`.
    - [x] Run `make registry-links`.
    - [x] Run `make publication-status`.
    - [x] Run `git diff --check`.
