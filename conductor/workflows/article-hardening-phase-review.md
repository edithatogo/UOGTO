# Article-Hardening Phase Review Workflow

## Purpose
Every phase of `uogto_article_hardening_protocol_20260624` must include peer, editorial, red-team, and devil's-advocate review before the phase is treated as implementation-review ready.

## Required Review Agents
The agent registry is `conductor/agents/article-hardening-review-agents.json`.

Minimum review set for each phase:

- `ontology_peer_reviewer`
- `methods_editor`
- `evidence_red_team`
- `devils_advocate_reviewer`

Additional reviewer for source, modelling, mapping, inclusion, and article-output phases:

- `simulation_modelling_peer_reviewer`

## Phase Review Steps
1. Confirm the phase acceptance criteria and generated artifacts.
2. Assign the minimum review set and any phase-specific additional reviewers.
3. Produce one review note per assigned reviewer under `docs/article-hardening/reviews/`.
4. Record each review in `docs/article-hardening/reviews/phase-review-log.jsonl`.
5. Create an issue/disposition summary that classifies findings as `fix_now`, `defer`, `reject`, `needs_user_input`, or `external_blocker`.
6. Apply fixes that are in scope for the phase.
7. Re-run the phase validator, focused tests, and `make validate`.
8. Update Conductor plan, status, and runlog before commit.

## Reviewer Outputs
Each reviewer note must include:

- phase number and title
- reviewer id
- reviewed artifacts
- findings
- required fixes
- deferred risks
- article-reporting implications
- disposition status

## Reporting Rules
- Editorial review checks whether article language is precise enough for methods/results reuse.
- Red-team review checks whether claims exceed evidence, especially for metadata-only and literature-only sources.
- Devil's-advocate review records plausible counterarguments and reasons not to add candidate UOGTO terms.
- Peer review checks ontology, modelling, SHACL, source-family, and competency-question fit.

## Completion Gate
A phase is review-ready only when:

- the phase implementation artifacts exist,
- the review assignments for the phase are declared,
- review outputs or planned review placeholders exist,
- dispositions are recorded,
- validation passes, and
- Conductor status reflects remaining risks honestly.
