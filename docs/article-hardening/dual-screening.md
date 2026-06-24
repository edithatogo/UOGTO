# Dual Screening and Adjudication

This artifact defines a simulated dual-screening workflow for the article-hardening evidence package.

## Roles

- Researcher: proposes an initial disposition for each candidate source or claim.
- Peer reviewer: accepts, rejects, or requests revision of the proposal.
- Red team reviewer: challenges any overclaim, weak rationale, or unsupported final disposition.

## Disposition pattern

1. The researcher proposes a screening outcome using the evidence register, source inventory, and mapping notes.
2. The peer reviewer accepts or rejects the proposal based on the recorded evidence.
3. The red team reviewer tests the proposal for overclaim, missing evidence, licence issues, or scope drift.
4. The final disposition is recorded only after the challenge step is resolved.

## Allowed final dispositions

- `accept`
- `reject`
- `accept_with_revision`
- `defer`
- `needs_domain_review`

## Why this exists

The purpose is to make the screening path auditable even when the package uses simulated rather than live dual review. It preserves the researcher-to-peer-to-red-team chain that the article can describe without overstating the amount of human adjudication actually completed.

## Package linkages

- `docs/article-hardening/manual-review-sample.csv`
- `docs/article-hardening/reviews/phase-review-log.jsonl`
- `docs/article-hardening/uogto-inclusion-decisions.md`
- `docs/article-hardening/uogto-inclusion-candidates.csv`
