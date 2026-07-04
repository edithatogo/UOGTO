# Implementation Plan: Registry and Publication Follow-Through

## Phase 1: Live Status Refresh

- [ ] Task: Refresh external publication observations
    - [ ] Run live publication-status, DOI, w3id, and registry link checks.
    - [ ] Compare generated status packets with checked-in release documentation.
    - [ ] Record any external-state changes in Conductor status and registry docs.

## Phase 2: Feedback Triage

- [ ] Task: Review external registry queues
    - [ ] Check LOV and OLS issue status.
    - [ ] Check Ontobee and Bioregistry request status.
    - [ ] Check FAIRsharing curator state and Wikidata metadata.
- [ ] Task: Convert feedback into scoped patches
    - [ ] Classify feedback as metadata-only, ontology-semantic, documentation, or no-action.
    - [ ] Add follow-up subtasks or issues for any required changes.

## Phase 3: Verification

- [ ] Task: Verify publication coherence
    - [ ] Run `make publishing-metadata`.
    - [ ] Run `make registry-links`.
    - [ ] Run `make publication-status`.
    - [ ] Run `git diff --check`.
