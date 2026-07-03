# Implementation Plan: Repository Validation And Runtime Hardening

## Phase 1: Create Track And Baseline

- [x] Task: Create track files and registry entry.
- [x] Task: Record baseline evidence from `make validate`, `make test` before/after `make build`, CQ row counts, and clean status behavior.

## Phase 2: Validation Semantics

- [x] Task: Add CQ expected-result manifest and enforce it in `scripts/validate.py` and pytest.
- [x] Task: Add negative SHACL fixture tests for core, game-type, execution, examples, and governance shapes.
- [x] Task: Extend semantic audit for namespace policy, object/datatype property separation, annotation completeness, JSON-LD term coverage, and instance naming.

## Phase 3: Build, Pixi, And Packaging Contract

- [x] Task: Make `make test` fresh-checkout safe.
- [x] Task: Align Makefile and Pixi task definitions for required/release gates.
- [x] Task: Replace bare `pip` install commands with environment-specific `python -m pip` where appropriate.
- [x] Task: Package `uogto` modules explicitly and add clean installed-package smoke tests.

## Phase 4: Runtime And Playground Support

- [x] Task: Add optional extras for runner/playground dependencies.
- [x] Task: Add console entry points or documented launch commands for supported surfaces.
- [x] Task: Update runner payoff/action resolution and add scoped/asymmetric payoff regression tests.

## Phase 5: CI, Supply Chain, And Conductor State

- [x] Task: Pin mutable external installs and verify downloaded artifacts where feasible.
- [x] Task: Add workflow tests for source pinning/checksum expectations.
- [x] Task: Consolidate Conductor status/runlog conventions and update stale references.
- [x] Task: Convert repo-root fixed temp test directories to pytest-managed temp paths.

## Phase 6: Verification And Closeout

- [x] Task: Run `make build`.
- [x] Task: Run `make validate`.
- [x] Task: Run `make test`.
- [x] Task: Run `make publishing-metadata`.
- [x] Task: Run `make registry-links`.
- [x] Task: Confirm `git status --short --branch` is clean except intentional tracked edits.
- [x] Task: Update Conductor status/runlog with exact evidence and residual external-only items.
