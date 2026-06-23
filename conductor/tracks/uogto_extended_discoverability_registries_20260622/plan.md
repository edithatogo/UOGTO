# Implementation Plan: Extended Discoverability Registries

This plan captures the second-wave discoverability targets for UOGTO after Zenodo DOI publication, LOV submission, OLS submission, and live w3id redirects. Repo-side packet integration is implemented; remaining work is limited to authenticated external submissions and upstream registry review.

## Phase 1: Shared Submission Packet
- [x] Task: Create a reusable extended-registry submission packet.
    - [x] Add a repo document under `docs/registry/` summarizing title, abstract, DOI, release URL, documentation URL, canonical RDF asset, namespaces, prefixes, license, maintainer route, and current LOV/OLS/w3id state.
    - [x] Include target-specific notes for FAIRsharing, prefix.cc, Wikidata, Ontobee, BioPortal, Bioregistry, and OBO Foundry.
    - [x] Add validation coverage and generated packet checks so the packet cannot drift from DOI, release, documentation, namespace, and first-wave registry metadata.

### Acceptance Criteria
- [x] Submission packet exists and links to all public canonical assets.
- [x] Packet includes `uogto` and `uogtox` prefix mappings.
- [x] Packet records external first-wave status: DOI minted, LOV submitted, OLS submitted, and w3id merged/live.
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
- [x] Task: Register UOGTO prefixes.
    - [x] Confirm the current prefix.cc add/update route.
    - [x] Submit `uogto` mapping to `https://w3id.org/uogto/core#`.
    - [x] Submit `uogtox` mapping to `https://w3id.org/uogto/extensions#`.
    - [x] Record submission and live lookup evidence.

### Acceptance Criteria
- [x] `uogto` and `uogtox` are live in prefix.cc with TXT endpoint evidence.
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
    - [x] Confirm w3id PR merge/live redirect propagation before submission.
    - [x] Submit the Ontobee indexing request after live w3id redirects were verified.

### Acceptance Criteria
- [x] Ontobee decision is recorded as submitted.
- [x] Request URL and review state are captured: https://github.com/OntoZoo/ontobee/issues/212.
- [x] Former w3id blocker is resolved; Ontobee is now external review pending.

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
- [x] Maintainer template feedback and template-update comment are visible in status/runlog: https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220.

## Phase 8: Negative Decision - OBO Foundry
- [x] Task: Record OBO Foundry as not prioritized.
    - [x] Document that OBO Foundry is not a target unless UOGTO is repositioned for biological or biomedical ontology governance.
    - [x] Revisit only if a concrete biomedical ontology use case and governance fit emerges.

### Acceptance Criteria
- [x] Negative decision is recorded in registry docs and Conductor status.
- [x] OBO Foundry is not treated as open work in routine status.

## Phase 9: Publication Packet Refresh
- [x] Task: Fold accepted/submitted second-wave registry state into release metadata.
    - [x] Update registry documentation, generated publication packet logic, release-readiness checks, Make/Pixi tasks, and the release-assets workflow for `dist/extended-registry-handoff.json`.
    - [x] Refresh local release assets after repo-side packet semantics were updated and local gates passed.
    - [x] Record remote workflow evidence after the implementation commit was pushed and `Publish Release Assets` was dispatched.

### Acceptance Criteria
- [x] Local `make release-preflight`, `make validate`, and `make test` pass.
- [x] Updated registry state is committed and pushed.
- [x] Remote validation and Pages workflows pass.
- [x] `Publish Release Assets` is dispatched and verified for `extended-registry-handoff.json` after push.

## Current External Blockers
- FAIRsharing record creation requires an authenticated FAIRsharing maintainer account.
- Wikidata item creation requires an authenticated Wikidata account and edit token.


## External Review Pending
- Ontobee indexing request https://github.com/OntoZoo/ontobee/issues/212 is pending maintainer review.
- Bioregistry request https://github.com/biopragmatics/bioregistry/issues/1999 is pending maintainer review after the new-prefix template update comment https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220.

## Remote Evidence
- Implementation commit `8b52503` was pushed to `origin/master`.
- Remote `Validate UOGTO` run `27960976638` passed for `8b52503`.
- Remote `Build WIDOCO Pages` run `27960977018` passed and deployed for `8b52503`.
- `Publish Release Assets` workflow run `27961110915` passed for `v1.0.0` and uploaded `extended-registry-handoff.json`.
- Release asset <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/extended-registry-handoff.json> was downloaded and verified with schema `uogto.extended-registry-handoff.v1`, status `external_actions_pending`, prefix.cc status `partial`, Bioregistry issue `https://github.com/biopragmatics/bioregistry/issues/1999`, and digest `sha256:31e4e76ab2334ce9b92b87fa6e5bb63a0e6f7b5094d242460ae65b37498b0018` before the 2026-06-23 follow-up refresh.

## Follow-Up Evidence - 2026-06-23
- w3id PR https://github.com/perma-id/w3id.org/pull/6238 is merged at 2026-06-22T12:29:07Z; /uogto/core and /uogto/extensions return 303 redirects to the UOGTO documentation site.
- prefix.cc uogtox retry succeeded and <http://prefix.cc/uogtox.file.txt> returns https://w3id.org/uogto/extensions#.
- Ontobee indexing request is open at https://github.com/OntoZoo/ontobee/issues/212.
- Bioregistry issue body was updated to the requested new-prefix template and recorded in https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220.
- FAIRsharing and Wikidata remain account-authenticated external actions; no repository-safe credentials were found.
