# Implementation Plan: Interoperability Benchmarks and Executable Examples

## Phase 1: Target Selection

- [x] Task: Build interoperability target inventory
    - [x] Review existing runner, playground, examples, and alignment modules.
    - [x] Rank candidate tool targets by relevance, license, maintenance, and testability.
    - [x] Record target disposition in a benchmark inventory document.

## Phase 2: Fixtures and Queries

- [x] Task: Add executable fixture coverage
    - [x] Add or extend examples for at least two priority tools or formats.
    - [x] Add competency-query expectations or focused tests for those fixtures.
    - [x] Document asserted versus illustrative mappings.

## Phase 3: Runtime Verification

- [x] Task: Verify local execution surface
    - [x] Add runner/playground smoke coverage where dependencies are lightweight.
    - [x] Keep heavy integrations optional or CI-isolated.
    - [x] Run `make validate` and focused runtime tests.
