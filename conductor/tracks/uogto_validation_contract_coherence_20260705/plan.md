# Implementation Plan: Validation Contract and Release Metadata Coherence

## Phase 1: Competency Query Contract

- [x] Task: Consolidate expected-result manifests
    - [x] Move all active expectations into `validation/competency-query-expectations.json`.
    - [x] Delete the stale `competency-questions/expected-results.json` duplicate.
- [x] Task: Complete competency-query coverage
    - [x] Add expected rows for `cq02`, `cq03`, `cq04`, and `cq06`.
    - [x] Update stale required bindings for `cq07` and `cq10`.
    - [x] Add a mechanism-design example assertion for `hasIncentiveConstraint`.
- [x] Task: Harden validator behavior
    - [x] Allow required bindings to match a subset of returned row bindings.
    - [x] Add tests that every `.rq` query has manifest coverage.

## Phase 2: Release and Text-Normalization Coherence

- [x] Task: Align release metadata
    - [x] Set Python package metadata to the ontology release version.
    - [x] Set Pixi workspace metadata to the ontology release version.
- [x] Task: Reduce generated-output churn
    - [x] Add `.gitattributes` text normalization rules for tracked text artifacts.
    - [x] Preserve binary handling for PDF, PowerPoint, and image assets.

## Phase 3: Verification

- [x] Task: Run focused validation
    - [x] Run `make validate`.
    - [x] Run focused competency-query and JSON-LD tests.
    - [x] Run `git diff --check`.
- [x] Task: Run full repository test gate
    - [x] Run `make test`.
    - [x] Record any residual warnings or line-ending-only churn.
