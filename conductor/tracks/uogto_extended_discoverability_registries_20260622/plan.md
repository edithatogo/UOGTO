# Implementation Plan: Extended Discoverability Registries

This plan captures the second-wave discoverability targets for UOGTO after Zenodo DOI publication, LOV submission, OLS submission, and w3id PR update. Repo-side packet integration is implemented; remaining work is limited to authenticated external submissions, upstream registry review, and prefix.cc rate-limit follow-up.

## Phase 1: Shared Submission Packet
- [x] Task: Create a reusable extended-registry submission packet.
    - [x] Add a repo document under `docs/registry/` summarizing title, abstract, DOI, release URL, documentation URL, canonical RDF asset, namespaces, prefixes, license, maintainer route, and current LOV/OLS/w3id state.
    - [x] Include target-specific notes for FAIRsharing, prefix.cc, Wikidata, Ontobee, BioPortal, Bioregistry, and OBO Foundry.
    - [x] Add validation coverage and generated packet checks so the packet cannot drift from DOI, release, documentation, namespace, and first-wave registry metadata.

### Acceptance Criteria
- [x] Submission packet exists and links to all public canonical assets.
- [x] Packet includes `uogto` and `uogtox` prefix mappings.
- [x] Packet records external first-wave status: DOI minted, LOV submitted, OLS submitted, w3id pending upstream merge.
- [x] `make release-preflight`, `make validate`, and `make test` pass locally.

## Phase 2: FAIRsharing Submission
- [~] Task: Submit UOGTO to FAIRsharing.
    - [x] Confirm the current FAIRsharing submission route and account requirements.
    - [x] Determine the correct registry type and subject classification guidance for UOGTO as an ontology/terminology or standard-like resource.
    - [ ] Submit the record using the shared submission packet.
    - [x] Record account-required blocker and maintainer next action.

### Acceptance Criteria
- [~] FAIRsharing submission URL or record URL is captured in `docs/registry/`; currently blocked pending an authenticated FAIRsharing maintainer session.
- [x] FAIRsharing status is visible in Conductor status/runlog.
- [x] Any requested metadata changes will be converted into follow-up tasks after external review feedback exists.

## Phase 3: prefix.cc Namespace Registration
- [~] Task: Register UOGTO prefixes.
    - [x] Confirm the current prefix.cc add/update route.
    - [x] Submit `uogto` mapping to `https://w3id.org/uogto/core#`.
    - [ ] Submit `uogtox` mapping to `https://w3id.org/uogto/extensions#`.
    - [x] Record submission and live lookup evidence.

### Acceptance Criteria
- [~] `uogto` is live in prefix.cc; `uogtox` is pending with evidence because prefix.cc returned a one-per-day contribution limit and a retry-after date of 2026-06-24.
- [x] Registry docs and Conductor state record the mapping status.

## Phase 4: Wikidata Item
- [~] Task: Create or update Wikidata coverage.
    - [x] Search Wikidata for an existing UOGTO item before creating a new one.
    - [x] Prepare statements for DOI, GitHub repository, documentation/homepage, release/version, license, ontology classification, and maintainers where supported.
    - [ ] Create or update the Wikidata item.
    - [x] Record account-required blocker and no-duplicate search evidence.

### Acceptance Criteria
- [~] Wikidata item URL is recorded; currently blocked pending an authenticated Wikidata edit session.
- [x] DOI, repository, documentation, and license statements are prepared in `docs/registry/extended-discoverability-submissions.md`.
- [x] No duplicate Wikidata item was found before deferring authenticated creation.

## Phase 5: Ontobee Feasibility
- [x] Task: Assess Ontobee after w3id redirect status is resolved.
    - [x] Check whether Ontobee should wait for stable namespace redirects and linked-data entry points.
    - [x] Confirm the current blocker as pending w3id PR merge/live redirect propagation.
    - [x] Record a deferred decision rather than submit prematurely.

### Acceptance Criteria
- [x] Ontobee decision is recorded as deferred.
- [ ] If submitted later, request URL and review state are captured.
- [x] Deferred blocker is specific: pending w3id redirects.

## Phase 6: Conditional BioPortal Submission
- [x] Task: Decide whether BioPortal is in scope.
    - [x] Draft a short domain-positioning note explaining that submission requires a defensible health, biomedical, clinical, behavioural-science, public-health, or simulation use case.
    - [x] Submit to BioPortal only if the positioning is defensible and the current BioPortal route supports UOGTO's distribution format.
    - [x] Record negative conditional decision.

### Acceptance Criteria
- [x] BioPortal decision is recorded with rationale.
- [ ] If submitted later, BioPortal record/request URL is captured.
- [x] If not submitted, the rationale prevents repeated re-evaluation without new domain evidence.

## Phase 7: Conditional Bioregistry Alignment
- [x] Task: Decide whether Bioregistry alignment adds value.
    - [x] Confirm current Bioregistry submission/update process and requirements through the GitHub issue route.
    - [x] Compare UOGTO's prefix state across w3id, prefix.cc, LOV, OLS, and prepared Wikidata/FAIRsharing records.
    - [x] Submit a Bioregistry request because it improves cross-registry identifier alignment.

### Acceptance Criteria
- [x] Bioregistry decision is recorded with rationale.
- [x] Request URL and prefix metadata are captured: https://github.com/biopragmatics/bioregistry/issues/1999.
- [x] External maintainer review remains pending and is visible in status/runlog.

## Phase 8: Negative Decision - OBO Foundry
- [x] Task: Record OBO Foundry as not prioritized.
    - [x] Document that OBO Foundry is not a target unless UOGTO is repositioned for biological or biomedical ontology governance.
    - [x] Revisit only if a concrete biomedical ontology use case and governance fit emerges.

### Acceptance Criteria
- [x] Negative decision is recorded in registry docs and Conductor status.
- [x] OBO Foundry is not treated as open work in routine status.

## Phase 9: Publication Packet Refresh
- [~] Task: Fold accepted/submitted second-wave registry state into release metadata.
    - [x] Update registry documentation, generated publication packet logic, release-readiness checks, Make/Pixi tasks, and the release-assets workflow for `dist/extended-registry-handoff.json`.
    - [x] Refresh local release assets after repo-side packet semantics were updated and local gates passed.
    - [ ] Record remote workflow evidence after the implementation commit is pushed and `Publish Release Assets` is dispatched.

### Acceptance Criteria
- [x] Local `make release-preflight`, `make validate`, and `make test` pass.
- [ ] Updated registry state is committed and pushed.
- [ ] Remote validation and Pages workflows pass.
- [ ] `Publish Release Assets` is dispatched and verified for `extended-registry-handoff.json` after push.

## Current External Blockers
- FAIRsharing record creation requires an authenticated FAIRsharing maintainer account.
- Wikidata item creation requires an authenticated Wikidata account and edit token.
- prefix.cc accepted `uogto` but rejected the same-day `uogtox` submission with a one-per-day contribution limit; retry after 2026-06-24.
- Ontobee should wait until the upstream w3id PR is merged and live redirects resolve.
- Bioregistry request https://github.com/biopragmatics/bioregistry/issues/1999 is pending maintainer review.
