# Implementation Plan: Extended Discoverability Registries

This plan captures the second-wave discoverability targets for UOGTO after Zenodo DOI publication, LOV submission, OLS submission, and live w3id redirects. Repo-side packet integration is implemented and complete; remaining FAIRsharing, Ontobee, and Bioregistry work is external curator/maintainer review tracked in the registry follow-up queue, not active repository implementation.

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
- [x] Task: Submit UOGTO to FAIRsharing.
    - [x] Confirm the current FAIRsharing submission route and account requirements.
    - [x] Determine the correct registry type and subject classification guidance for UOGTO as an ontology/terminology or standard-like resource.
    - [x] Submit the record using the shared submission packet.
    - [x] Create FAIRsharing draft record https://fairsharing.org/8382 through the authenticated account workflow.
    - [x] Populate title, abbreviation, homepage, year, country, status, registry type, contact, subject/domain, object type, tags, licence, GitHub, documentation, and Zenodo DOI support links.
    - [x] Persist required `data processes and conditions` metadata and move the public record to FAIRsharing curator review.

### Acceptance Criteria
- [x] FAIRsharing record URL is captured in `docs/registry/`: https://fairsharing.org/8382. The public page reports `This record is awaiting review by FAIRsharing curators`.
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
- [x] Task: Create or update Wikidata coverage.
    - [x] Search Wikidata for an existing UOGTO item before creating a new one.
    - [x] Prepare statements for DOI, GitHub repository, documentation/homepage, release/version, license, ontology classification, and maintainers where supported.
    - [x] Create the Wikidata item: https://www.wikidata.org/wiki/Q140323510.
    - [x] Record account-authenticated creation evidence and no-duplicate search evidence.

### Acceptance Criteria
- [x] Wikidata item URL is recorded: https://www.wikidata.org/wiki/Q140323510.
- [x] DOI, repository, documentation, ontology classification, and license statements are live on the Wikidata item.
- [x] No duplicate Wikidata item was found before creation.

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
- [x] No BioPortal record/request URL is required for this track because the recorded decision is `not_submitted_conditional`; capture a URL only if a future biomedical positioning note reopens BioPortal.
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
- No current repo-actionable second-wave account blockers remain. FAIRsharing record https://fairsharing.org/8382 is awaiting curator review; Ontobee and Bioregistry remain maintainer-review pending. These are external follow-up items tracked in `docs/registry/extended-discoverability-submissions.md` and the generated handoff packet.


## External Review Pending
- Ontobee indexing request https://github.com/OntoZoo/ontobee/issues/212 is pending maintainer review.
- Bioregistry request https://github.com/biopragmatics/bioregistry/issues/1999 is pending maintainer review after the new-prefix template update comment https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220.
- FAIRsharing record https://fairsharing.org/8382 is pending FAIRsharing curator review.

## Closeout Evidence - 2026-07-03
- Live prefix.cc TXT endpoints still return the expected mappings: `uogto` -> `https://w3id.org/uogto/core#`; `uogtox` -> `https://w3id.org/uogto/extensions#`.
- Wikidata entity data for `Q140323510` still reports label `Universal Open Game Theory Ontology` and DOI `10.5281/ZENODO.20796937`.
- GitHub API checks confirm Ontobee issue `212` and Bioregistry issue `1999` are still open, so no acceptance is claimed.
- The release `extended-registry-handoff.json` remains the external-review handoff surface for curator/maintainer follow-up.

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
- FAIRsharing and Wikidata remained account-authenticated external actions at this checkpoint; Wikidata was completed on 2026-06-24 and FAIRsharing record https://fairsharing.org/8382 is now awaiting curator review.

## Remote Evidence - 2026-06-23 Follow-Up
- Follow-up implementation commit `24b9601` was pushed to `origin/master`.
- Remote `Validate UOGTO` run `28023497374` passed for `24b9601`.
- Remote `Build WIDOCO Pages` run `28023497352` passed and deployed for `24b9601`.
- `Publish Release Assets` workflow run `28023545152` passed for `v1.0.0` and refreshed `extended-registry-handoff.json`, `w3id-redirect-handoff.json`, and `publication-status.json`.
- Refreshed `extended-registry-handoff.json` was downloaded and verified at this checkpoint with status `external_actions_pending`, blockers `fairsharing,wikidata`, prefix.cc status `submitted`, Ontobee issue `https://github.com/OntoZoo/ontobee/issues/212`, Bioregistry template-update comment `https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220`, and digest `sha256:07c9e9e66b69582065b97c01fa61df05ad6da8c04ff39a51069e0b70c9f93081`; the 2026-06-24 refresh supersedes this account-blocker state.
- Refreshed `w3id-redirect-handoff.json` was downloaded and verified with status `live_redirects_verified`, empty blockers, merged_at `2026-06-22T12:29:07Z`, and digest `sha256:82ea92c3fb8465a6bd97dfdfc51545b4e24e08d56ed2e4e7d1b26bd8a58a48ca`.
- Refreshed `publication-status.json` was downloaded and verified at this checkpoint with status `pending_external_publication_steps`, w3id status `live_redirects_verified`, blockers only for `fairsharing` and `wikidata`, and digest `sha256:f4ad2c38e8af6e9d8659246f2d8714966a9c9dbfdefa0dfb58d14639fb67caa4`; the 2026-06-24 refresh supersedes this account-blocker state.

## Live Account Evidence - 2026-06-24
- Wikidata duplicate check for `Universal Open Game Theory Ontology` returned no matching item before creation.
- Created Wikidata item https://www.wikidata.org/wiki/Q140323510 through the authenticated `Doughnuted` session.
- Added and verified statements: instance of ontology (`Q324254`), DOI `10.5281/zenodo.20796937`, official website `https://edithatogo.github.io/UOGTO/`, source code repository URL `https://github.com/edithatogo/UOGTO`, and copyright license Creative Commons Attribution 4.0 International (`Q20007257`).
- Verified live pages in Chrome: Wikidata item, Zenodo record `https://zenodo.org/records/20796937`, documentation site, and GitHub repository.
- Created FAIRsharing draft record https://fairsharing.org/8382 through the authenticated FAIRsharing/GitHub workflow.
- Populated FAIRsharing record metadata: name, abbreviation, homepage, year `2026`, country `Australia`, status `Ready`, registry type `Standard / Terminology Artefact`, contact `Dylan Mordaunt`, taxonomic range `Not Applicable`, subject `Knowledge And Information Systems`, domain `Knowledge Representation`, object type `Dataset`, tags `Semantic Web` and `Ontology`, CC-BY-4.0 licence, GitHub support link, documentation support link, and Zenodo DOI support link.
- FAIRsharing required `data processes and conditions` metadata was persisted on 2026-06-24 with `read` / `User interface` access and the canonical RDF artifact as example URL; the public page now reports that the record is awaiting FAIRsharing curator review.
- FAIRsharing recommended-but-nonblocking gaps remain organisation links, publications, citations, and record associations; these require curation guidance or defensible FAIRsharing record associations before adding.
