# Implementation Plan: Alignment Evidence Expansion

## Phase 1: Candidate Prioritization

- [x] Task: Select high-value mapping candidates
    - [x] Re-read the latest ontology-comparison report and mapping-review CSV.
    - [x] Identify unmatched or needs-domain-review areas with the largest research payoff.
    - [x] Record reviewer assignment and acceptance criteria.

## Phase 2: Evidence Review

- [x] Task: Review candidate mappings
    - [x] Collect source evidence without violating license boundaries.
    - [x] Mark candidates as accepted, rejected, deferred, or needs-domain-review.
    - [x] Update rationale fields for each reviewed row.

## Phase 3: Artifact Regeneration

- [x] Task: Rebuild comparison artifacts
    - [x] Regenerate accepted alignment TTL and SSSOM outputs.
    - [x] Regenerate overlap, network, visual, and report artifacts.
    - [x] Run comparison-focused tests and `git diff --check`.
