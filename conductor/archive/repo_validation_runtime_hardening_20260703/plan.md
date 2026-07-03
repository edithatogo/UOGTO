# Implementation Plan

## Phase 1: Create Track And Baseline
- [x] Create track files and registry entry.
- [x] Record baseline evidence for validation, test, CQ, and scratch behavior in status/runlog.

## Phase 2: Validation Semantics
- [x] Add CQ expected-result manifest and enforce it in `scripts/validate.py` and pytest.
- [x] Add negative SHACL fixture tests for core, game-type, execution, examples, and governance shapes.
- [x] Extend semantic audit for namespace policy, object/datatype property separation, annotation completeness, JSON-LD term coverage, and instance naming.

## Phase 3: Build, Pixi, And Packaging Contract
- [x] Make `make test` fresh-checkout safe.
- [x] Align Makefile and Pixi task definitions for required/release gates.
- [x] Replace bare `pip` install commands with environment-specific `python -m pip`.
- [x] Package `uogto` modules explicitly and add clean installed-package smoke tests without relying on `pythonpath = ["."]`.

## Phase 4: Runtime And Playground Support
- [x] Add optional extras for runner/playground dependencies.
- [x] Add console entry points or documented launch commands for supported surfaces.
- [x] Update runner payoff/action resolution and add regression tests for scoped, asymmetric, and duplicate-label cases.

## Phase 5: CI, Supply Chain, And Conductor State
- [x] Pin mutable external installs and verify downloaded release artifacts where feasible.
- [x] Add workflow tests for source pinning/checksum expectations.
- [x] Consolidate Conductor status/runlog conventions and update stale references touched by this track.
- [x] Convert repo-root fixed temp test directories to pytest-managed temp paths.

## Phase 6: Verification And Closeout
- [x] Run `make build`: passed.
- [x] Run `make validate`: passed with CQ expected-result manifest checks.
- [x] Run `make test`: `223 passed, 1 skipped, 26 warnings`.
- [x] Run `make publishing-metadata`: passed.
- [x] Run `make registry-links`: passed.
- [x] Confirm `git status --short --branch` is clean except intentional tracked edits.
- [x] Update Conductor status/runlog with exact evidence and residual external-only items.
