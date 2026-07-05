# Implementation Plan: Interoperability Benchmarks and Executable Examples

## Phase 1: Target Selection

- [ ] Task: Build interoperability target inventory
    - [ ] Review existing runner, playground, examples, and alignment modules.
    - [ ] Rank candidate tool targets by relevance, license, maintenance, and testability.
    - [ ] Record target disposition in a benchmark inventory document.

## Phase 2: Fixtures and Queries

- [ ] Task: Add executable fixture coverage
    - [ ] Add or extend examples for at least two priority tools or formats.
    - [ ] Add competency-query expectations or focused tests for those fixtures.
    - [ ] Document asserted versus illustrative mappings.

## Phase 3: Runtime Verification

- [ ] Task: Verify local execution surface
    - [ ] Add runner/playground smoke coverage where dependencies are lightweight.
    - [ ] Keep heavy integrations optional or CI-isolated.
    - [ ] Run `make validate` and focused runtime tests.
