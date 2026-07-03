# Repository Validation And Runtime Hardening

## Summary

Strengthen UOGTO validation semantics, fresh-checkout gates, runtime packaging, Conductor state, and CI supply-chain determinism.

## Requirements

- Validate competency-query expected results against example graphs, not only query syntax.
- Add negative SHACL fixtures for representative shape failures.
- Make `make test` fresh-checkout safe when generated `dist/` assets are needed.
- Align Make and Pixi gate command sequences.
- Treat `uogto.runner` and `uogto.playground` as supported importable product surfaces.
- Add isolated install/import smoke tests for packaged modules.
- Harden runner behavior for scoped games, asymmetric payoffs, per-player actions, and payoff profile/link ontology patterns.
- Pin the default Pixi Python to 3.10 for CI parity.
- Pin mutable CI/toolchain inputs where feasible and document the policy for action/tag updates.
- Consolidate active Conductor status surfaces and remove stale references touched by this track.
- Ensure the full test suite leaves no repo-root scratch directories.
