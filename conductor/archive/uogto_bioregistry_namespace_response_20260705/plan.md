# Implementation Plan: Bioregistry Namespace and ORCID Response

## Phase 1: Evidence Refresh

- [x] Task: Review current feedback and local policy
    - [x] Re-check Bioregistry issue 1999 and maintainer comments.
    - [x] Review UOGTO namespace policy and current registry submission docs.
    - [x] Confirm whether approved public ORCID metadata is available.

## Phase 2: Response Decision

- [x] Task: Decide response path
    - [x] Record whether to defend the two-namespace design or open a namespace-consolidation follow-up.
    - [x] Draft a concise maintainer-facing response grounded in UOGTO policy.
    - [x] Identify any identity-metadata blocker explicitly instead of inventing ORCID data.

## Phase 3: External and Local Update

- [x] Task: Apply the response outcome
    - [x] Post the response to Bioregistry issue 1999 when ready, or record the blocking reason locally.
    - [x] Update `docs/registry/publication-follow-up-triage.json`.
    - [x] Update `docs/registry/publication-follow-up-triage.md`.
    - [x] Update any related registry handoff artifacts if the Bioregistry status changes.

## Phase 4: Verification

- [x] Task: Verify registry coherence
    - [x] Run `make registry-links`.
    - [x] Run `make publication-status`.
    - [x] Run focused registry tests.
    - [x] Run `git diff --check`.

## Evidence

- Bioregistry response posted: <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4885550451>.
- Namespace decision: defend the published `v1.0.0` two-namespace design for the current response; register `uogto` as the primary core prefix and keep `uogtox` as a separately documented extension prefix.
- ORCID decision: approved public sole-author/contact ORCID <https://orcid.org/0000-0002-9775-0603> is now present in `CITATION.cff`, `.zenodo.json`, and the Bioregistry issue body.
- Verification passed: `make registry-links`; `make publication-status`; `make extended-registry-packet`; focused registry pytest (`14 passed`); `git diff --check`.

## Phase: Review Fixes

- [x] Task: Apply review suggestions d0dbd79
- [x] Task: Apply PR review suggestion f4cccd0
