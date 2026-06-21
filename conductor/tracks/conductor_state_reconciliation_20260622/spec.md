# Specification: Conductor State Reconciliation (`conductor_state_reconciliation_20260622`)

## Overview
This track records the repository-side Conductor normalization needed after the ontology, maintenance, scoping-review, and publishing/discoverability work. It keeps the active track registry, archived tracks, status surfaces, run log, and verification gates aligned with the current repository state.

## Scope
- Register completed reconciliation work as a Conductor maintenance track.
- Keep archived tracks discoverable without treating them as active work.
- Ensure CI/Pixi hardening and registry-link maintenance are represented in active Conductor plans.
- Add a follow-up track for SourceRight manuscript source verification.
- Record remaining external gates in `.conductor/status.md`.

## Out of Scope
- Reverting or rewriting existing user changes.
- Completing live Zenodo, GitHub Pages, LOV, OLS, or SourceRight verification gates.
- Claiming remote repository status without a configured remote or authenticated repository slug.

## Acceptance Criteria
- [x] Active Conductor registry includes the reconciliation track as completed.
- [x] Archived tracks are listed in an archive index for audit discoverability.
- [x] Publishing/discoverability registry-link work remains represented by the active publishing track.
- [x] SourceRight manuscript source verification is tracked as a new active follow-up track.
- [x] `.conductor/status.md` and `.conductor/runlog.md` describe current known gaps and next work.
