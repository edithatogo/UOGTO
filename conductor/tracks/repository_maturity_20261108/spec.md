# Specification — maturity and hardening

Make semantic changes, releases and optional integrations reproducible and
reviewable without confusing historical metrics with current evidence.

## Requirements

- Keep published IRIs stable; document intentional changes in entailments.
- State the scope of reasoner/profile checks and test known invalid cases.
- Preserve core Python compatibility while isolating optional engine requirements.
- Verify installed artifacts from outside the checkout and pin external inputs.
- Measure validation/interchange performance before setting regression budgets.
- Keep current reports tied to input hashes and dated publication snapshots distinct.
- Preserve existing required checks and sole-developer workflow. No repeated human
  approval or scientific-publication prerequisite is added to ordinary code changes.

## Acceptance

Each leaf supplies its own actual commands, fixtures and outcomes. Missing optional
providers cannot be reported as executed. Semantic-contract and provider numerical
qualification remain with their existing owners.
