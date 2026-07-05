# Alignment Evidence Expansion

## Overview

Expand comparative ontology mapping evidence beyond the current small accepted
alignment set while preserving conservative review standards and license
boundaries.

## Functional Requirements

- Prioritize high-value unmatched sources from the comparison report.
- Convert `needs_domain_review` rows into explicit reviewer work queues.
- Add accepted alignments only when evidence is strong enough for assertion.
- Keep metadata-only standards separate from parsed RDF artifacts.

## Acceptance Criteria

- The mapping review queue is updated with reviewer decisions and rationale.
- Accepted alignments, SSSOM exports, comparison reports, and visualizations remain synchronized.
- `make ontology-comparison-all` or the narrow equivalent passes for changed artifacts.

## Out of Scope

- Bulk-accepting candidate mappings without review.
- Importing non-redistributable standards artifacts into the repository.
