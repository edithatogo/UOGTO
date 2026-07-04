# Implementation Plan: Alignment Evidence Expansion

## Phase 1: Candidate Prioritization

- [ ] Task: Select high-value mapping candidates
    - [ ] Re-read the latest ontology-comparison report and mapping-review CSV.
    - [ ] Identify unmatched or needs-domain-review areas with the largest research payoff.
    - [ ] Record reviewer assignment and acceptance criteria.

## Phase 2: Evidence Review

- [ ] Task: Review candidate mappings
    - [ ] Collect source evidence without violating license boundaries.
    - [ ] Mark candidates as accepted, rejected, deferred, or needs-domain-review.
    - [ ] Update rationale fields for each reviewed row.

## Phase 3: Artifact Regeneration

- [ ] Task: Rebuild comparison artifacts
    - [ ] Regenerate accepted alignment TTL and SSSOM outputs.
    - [ ] Regenerate overlap, network, visual, and report artifacts.
    - [ ] Run comparison-focused tests and `git diff --check`.
