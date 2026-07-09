# Implementation Plan: Field Expansion Examples and Validation

## Phase 0: Roadmap and Governance

- [x] Add a repository roadmap that maps GitHub issues #76-#83 to concrete
  implementation slices.
- [x] Add an applied extension-pack pattern so domain-specific work can depend
  on UOGTO without changing the shared game layer prematurely.
- [x] Create this Conductor track as the local source of truth for the roadmap.

## Phase 1: Game-Theory Extension Examples

- [ ] Implement #77 mean-field worked example, SHACL checks, competency query,
  and decision ledger.
- [ ] Implement #78 network/congestion worked example, SHACL checks,
  competency query, and decision ledger.
- [ ] Implement #79 evolutionary worked example, SHACL checks, competency
  query, and decision ledger.
- [ ] Implement #80 institutional/information-design examples, SHACL checks,
  competency queries, and decision ledger.

## Phase 2: Agentic and Provenance-Facing Examples

- [ ] Implement #81 learning-in-games/MARL worked example, SHACL checks,
  competency query, and decision ledger.
- [ ] Implement #82 trust/reputation/provenance worked example, SHACL checks,
  competency query, and decision ledger.

## Phase 3: Applied Extension Packs

- [ ] Use `docs/roadmap/applied-extension-pack-pattern.md` to scope the first
  applied packs for health economics/HTA, medical decision modelling, safety
  systems, and genomic policy.
- [ ] Create follow-up implementation issues only after pack boundaries and
  candidate examples are documented.

## Validation Gates

- `make build`
- `make validate`
- focused SHACL/CQ tests for the slice
- `make test`

