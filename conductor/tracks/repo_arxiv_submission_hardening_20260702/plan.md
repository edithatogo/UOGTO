# Implementation Plan: Repo and arXiv Submission Hardening

## Phase 1: Conductor Track and Requirements Inventory

- [x] Task: Create track specification with official arXiv source constraints.
- [x] Task: Create implementation plan with scoring loop and validation gates.
- [x] Task: Register the track in `conductor/tracks.md`.

## Phase 2: Repository Contribution Polish

- [x] Task: Expand contributor guidance for ontology, SHACL, examples, competency queries, documentation, release, and deprecation impacts.
- [x] Task: Add public issue templates for ontology proposals, validation failures, documentation fixes, bug reports, and questions.
- [x] Task: Strengthen the pull request template with ontology, manuscript, release, and RI-HERO checks.
- [x] Task: Add standard GitHub labels for external contributors.
- [x] Task: Add machine-readable dual-license metadata while preserving CC-BY-4.0 for ontology/docs and MIT for code/tooling.
- [x] Task: Remove stale `master` workflow triggers where normal operation should follow `main`.

## Phase 3: Required Gate and Branch Protection

- [x] Task: Add an always-running `Required Gate` workflow for validation, tests, publishing metadata, registry links, manuscript build, arXiv upload-ready packaging, and strict scoring.
- [x] Task: Add or update tests that assert `Required Gate` remains present and complete.
- [x] Task: After workflow validation, update `main` branch protection to require `Required Gate` while retaining review and safety settings.

## Phase 4: Strict arXiv Review Simulation

- [x] Task: Add the strict arXiv rubric, report, and iteration log artifacts.
- [x] Task: Add `scripts/maintenance/score_arxiv_submission.py` with a 1000-point rubric and blocker overrides.
- [x] Task: Add tests for scoring categories, blocker handling, threshold logic, and report artifacts.
- [x] Task: Run the scoring loop and record findings until the score is above `995/1000` with no blockers.

## Phase 5: Validation and Documentation Synchronization

- [x] Task: Run `make validate`.
- [x] Task: Run `make test`.
- [x] Task: Run `make publishing-metadata`.
- [x] Task: Run `make registry-links`.
- [x] Task: Run `make manuscript-pdf`.
- [x] Task: Run `make arxiv-upload-ready`.
- [x] Task: Update arXiv submission process/contract, Conductor status/runlog, and RI-HERO status with final score and remaining external arXiv UI steps.

## Phase 6: Closeout

- [x] Task: Review git diff for unrelated changes and preserve existing `docs/paper/paper.tex` edits.
- [x] Task: Commit scoped implementation changes.
- [x] Task: Record residual blockers, if any.
