# Implementation Plan: Bioregistry Namespace and ORCID Response

## Phase 1: Evidence Refresh

- [ ] Task: Review current feedback and local policy
    - [ ] Re-check Bioregistry issue 1999 and maintainer comments.
    - [ ] Review UOGTO namespace policy and current registry submission docs.
    - [ ] Confirm whether approved public ORCID metadata is available.

## Phase 2: Response Decision

- [ ] Task: Decide response path
    - [ ] Record whether to defend the two-namespace design or open a namespace-consolidation follow-up.
    - [ ] Draft a concise maintainer-facing response grounded in UOGTO policy.
    - [ ] Identify any identity-metadata blocker explicitly instead of inventing ORCID data.

## Phase 3: External and Local Update

- [ ] Task: Apply the response outcome
    - [ ] Post the response to Bioregistry issue 1999 when ready, or record the blocking reason locally.
    - [ ] Update `docs/registry/publication-follow-up-triage.json`.
    - [ ] Update `docs/registry/publication-follow-up-triage.md`.
    - [ ] Update any related registry handoff artifacts if the Bioregistry status changes.

## Phase 4: Verification

- [ ] Task: Verify registry coherence
    - [ ] Run `make registry-links`.
    - [ ] Run `make publication-status`.
    - [ ] Run focused registry tests.
    - [ ] Run `git diff --check`.

