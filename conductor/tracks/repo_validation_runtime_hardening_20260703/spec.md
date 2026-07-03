# Specification: Repository Validation And Runtime Hardening

## Overview

This chore track turns UOGTO's green checks into stronger evidence-bearing gates. It hardens competency-query validation against examples, negative SHACL coverage, fresh-checkout build/test ordering, Make/Pixi parity, package installation, runtime/playground support, CI supply-chain determinism, and Conductor status consistency.

## Functional Requirements

- Add a competency-query expected-result manifest and enforce it in local validation and pytest.
- Validate competency queries against ontology plus example graphs, not ontology files alone.
- Add negative SHACL fixture tests for representative core, game-type, execution, example, and governance shapes.
- Ensure `make test` is fresh-checkout safe when generated `dist/` assets are required.
- Align Makefile and Pixi task definitions for `test`, `required-gate`, and release-preflight paths.
- Package `uogto` runtime modules explicitly and declare optional playground dependencies.
- Keep runner and playground as supported product surfaces with import or launch smoke coverage.
- Harden runner payoff/action resolution for multi-game graphs, asymmetric payoffs, per-player action identity, and the current `PayoffProfile` / `PlayerPayoffLink` pattern.
- Pin CI/toolchain inputs that otherwise float, including SourceRight git installation and WIDOCO release artifact verification.
- Consolidate `conductor/` and `.conductor/` status conventions so future status reads have one canonical current path.
- Remove stale PR, test-count, and branch-name references from current Conductor status surfaces.
- Ensure the full test suite leaves no repo-root scratch directories behind.

## Non-Functional Requirements

- Preserve existing ontology namespaces and public IRIs.
- Keep changes narrowly scoped to validation/runtime/CI hardening.
- Do not claim external arXiv, registry, or publication steps are complete unless they are verified live.
- Keep generated `dist/` artifacts ignored and reproducible from tracked sources.

## Acceptance Criteria

- `make validate` fails when a required CQ binding is absent or the result count is below the manifest threshold.
- Negative SHACL tests prove representative invalid graphs are rejected.
- `make test` passes from a fresh checkout after invoking its declared prerequisites.
- Makefile and Pixi required/release gates use equivalent command ordering.
- `pip install .` exposes the `uogto` package and supported imports.
- Runner tests cover scoped game retrieval and current payoff-profile semantics.
- CI workflows pin or verify mutable third-party toolchain inputs.
- Current Conductor status points to `conductor/` as canonical and contains no stale PR #19, stale `207 passed`, or obsolete `origin/master` guidance.
- `git status --short --branch` is clean after verification except intentional tracked edits.

## Out of Scope

- Changing ontology public IRIs or releasing a new ontology version.
- Submitting to arXiv or changing external registry state.
- Rewriting the Streamlit playground UI beyond making it importable and dependency-declared.
