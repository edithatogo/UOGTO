# Implementation Plan: Extended Discoverability Registries

This plan captures the recommended second-wave discoverability targets for UOGTO after Zenodo DOI publication, LOV submission, OLS submission, and w3id PR update.

## Phase 1: Shared Submission Packet
- [ ] Task: Create a reusable extended-registry submission packet.
    - [ ] Add a repo document under `docs/registry/` summarizing title, abstract, DOI, release URL, documentation URL, canonical RDF asset, namespaces, prefixes, license, maintainer route, and current LOV/OLS/w3id state.
    - [ ] Include target-specific notes for FAIRsharing, prefix.cc, Wikidata, Ontobee, BioPortal, and Bioregistry.
    - [ ] Add validation coverage or extend existing metadata checks so the packet cannot drift from DOI, release, and documentation metadata.

### Acceptance Criteria
- [ ] Submission packet exists and links to all public canonical assets.
- [ ] Packet includes `uogto` and `uogtox` prefix mappings.
- [ ] Packet records external first-wave status: DOI minted, LOV submitted, OLS submitted, w3id pending upstream merge.
- [ ] `make validate` and `make test` pass.

## Phase 2: FAIRsharing Submission
- [ ] Task: Submit UOGTO to FAIRsharing.
    - [ ] Confirm the current FAIRsharing submission route and account requirements.
    - [ ] Determine the correct registry type and subject classifications for UOGTO as an ontology/terminology or standard-like resource.
    - [ ] Submit the record using the shared submission packet.
    - [ ] Record submission URL, review status, and any maintainer feedback.

### Acceptance Criteria
- [ ] FAIRsharing submission URL or record URL is captured in `docs/registry/`.
- [ ] FAIRsharing status is visible in Conductor status/runlog.
- [ ] Any requested metadata changes are converted into follow-up tasks.

## Phase 3: prefix.cc Namespace Registration
- [ ] Task: Register UOGTO prefixes.
    - [ ] Confirm the current prefix.cc add/update route.
    - [ ] Submit `uogto` mapping to `https://w3id.org/uogto/core#`.
    - [ ] Submit `uogtox` mapping to `https://w3id.org/uogto/extensions#`.
    - [ ] Record submission or live lookup evidence.

### Acceptance Criteria
- [ ] `uogto` and `uogtox` mappings are either live in prefix.cc or pending with evidence.
- [ ] Registry docs and Conductor state record the mapping status.

## Phase 4: Wikidata Item
- [ ] Task: Create or update Wikidata coverage.
    - [ ] Search Wikidata for an existing UOGTO item before creating a new one.
    - [ ] Add statements for DOI, GitHub repository, documentation/homepage, release/version, license, ontology classification, and maintainers where supported.
    - [ ] Record Wikidata item URL and statement coverage.

### Acceptance Criteria
- [ ] Wikidata item URL is recorded.
- [ ] DOI, repository, documentation, and license statements are present or documented as unavailable.
- [ ] No duplicate Wikidata item is created.

## Phase 5: Ontobee Feasibility
- [ ] Task: Assess Ontobee after w3id redirect status is resolved.
    - [ ] Check whether Ontobee accepts UOGTO's non-OBO, game-theory ontology scope and distribution model.
    - [ ] Confirm whether Ontobee requires a stable PURL, OBO-style metadata, OWL profile constraints, or maintainer contact workflow.
    - [ ] Submit only if the route is appropriate; otherwise record a negative decision.

### Acceptance Criteria
- [ ] Ontobee decision is recorded as submitted, deferred, or not appropriate.
- [ ] If submitted, request URL and review state are captured.
- [ ] If deferred, blocker is specific, such as pending w3id redirects.

## Phase 6: Conditional BioPortal Submission
- [ ] Task: Decide whether BioPortal is in scope.
    - [ ] Draft a short domain-positioning note explaining whether UOGTO has a defensible health, biomedical, clinical, behavioural-science, public-health, or simulation use case.
    - [ ] Submit to BioPortal only if the positioning is defensible and the current BioPortal route supports UOGTO's distribution format.
    - [ ] Record submission URL or negative decision.

### Acceptance Criteria
- [ ] BioPortal decision is recorded with rationale.
- [ ] If submitted, BioPortal record/request URL is captured.
- [ ] If not submitted, the rationale prevents repeated re-evaluation without new domain evidence.

## Phase 7: Conditional Bioregistry Alignment
- [ ] Task: Decide whether Bioregistry alignment adds value.
    - [ ] Confirm current Bioregistry submission/update process and requirements.
    - [ ] Compare UOGTO's prefix state across w3id, prefix.cc, LOV, OLS, and any accepted Wikidata/FAIRsharing records.
    - [ ] Submit or defer based on whether Bioregistry improves cross-registry identifier alignment.

### Acceptance Criteria
- [ ] Bioregistry decision is recorded with rationale.
- [ ] If submitted, request URL and prefix metadata are captured.
- [ ] If deferred, dependency on w3id/prefix.cc/LOV/OLS state is explicit.

## Phase 8: Negative Decision - OBO Foundry
- [ ] Task: Record OBO Foundry as not prioritized.
    - [ ] Document that OBO Foundry is not a target unless UOGTO is repositioned for biological or biomedical ontology governance.
    - [ ] Revisit only if a concrete biomedical ontology use case and governance fit emerges.

### Acceptance Criteria
- [ ] Negative decision is recorded in registry docs and Conductor status.
- [ ] OBO Foundry is not treated as open work in routine status.

## Phase 9: Publication Packet Refresh
- [ ] Task: Fold accepted/submitted second-wave registry state into release metadata.
    - [ ] Update registry documentation, release notes, and generated publication packet logic if second-wave registry state becomes part of the official release handoff.
    - [ ] Refresh release assets only after repo-side packet semantics are updated and local gates pass.
    - [ ] Record remote workflow evidence.

### Acceptance Criteria
- [ ] Local `make release-preflight`, `make validate`, and `make test` pass.
- [ ] Updated registry state is committed and pushed.
- [ ] Remote validation and Pages workflows pass.
- [ ] If release packets change, `Publish Release Assets` is dispatched and verified.
