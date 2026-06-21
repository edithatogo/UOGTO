# Implementation Plan: Publishing and Discoverability

This plan begins after the completed UOGTO ontology modeling, SHACL validation, example, competency-query, and repository maintenance phases. It converts the validated ontology repository into a citable, documented, and discoverable public ontology project.

## Phase 1: Zenodo Integration and DOI Release
- [~] Task: Configure Zenodo repository integration
    - [ ] Enable the GitHub-Zenodo repository link for `edithatogo/UOGTO`.
    - [ ] Verify Zenodo is configured to archive GitHub releases, not every branch push.
    - [x] Add a release asset workflow so generated RDF, SHACL, JSON-LD, checksum, and manifest files are attached to `v1.0.0` before Zenodo archives the release.
    - [x] Document the release archive flow in `docs/releases/v1.0.md`.
- [x] Task: Add citation metadata
    - [x] Create `CITATION.cff` with title, authors, repository URL, ontology URL, license, version, release date, and preferred citation.
    - [x] Create `.zenodo.json` with creators, title, description, keywords, related identifiers, license, and communities if applicable.
    - [x] Cross-check author names and ORCID fields before release.
- [x] Task: Draft v1.0 release notes
    - [x] Create `docs/releases/v1.0.md` summarizing ontology scope, included modules, validation status, examples, documentation links, and known limitations.
    - [x] Include DOI placeholder text that can be replaced after the Zenodo archive is minted.
    - [x] Add release checklist entries for `make validate`, `make test`, semantic audit, and generated documentation.

### Required Configuration Files
- `CITATION.cff`
- `.zenodo.json`
- `docs/releases/v1.0.md`
- `.github/workflows/release-assets.yml`

### Acceptance Criteria
- [ ] Zenodo shows `edithatogo/UOGTO` as enabled for release archiving.
- [ ] A GitHub `v1.0.0` release creates a Zenodo archive and DOI.
- [x] Release asset packaging is automated for generated ontology, shape, context, checksum, and manifest files.
- [x] `CITATION.cff` metadata matches GitHub release notes and Zenodo metadata.
- [x] Release notes include validation evidence and links to canonical ontology assets.

## Phase 2: WIDOCO Documentation and GitHub Pages
- [x] Task: Add WIDOCO documentation configuration
    - [x] Create `docs/widoco/widoco.properties` defining ontology input paths, output directory, project title, ontology URI, preferred prefix, license, and provenance metadata.
    - [x] Create `docs/widoco/README.md` with local documentation build instructions and expected output location.
    - [x] Decide whether documentation is generated from `dist/` combined assets or individual canonical ontology modules, and record the decision in the WIDOCO README.
- [x] Task: Add CI/CD documentation generation
    - [x] Create `.github/workflows/widoco-pages.yml`.
    - [x] Install Java and WIDOCO in the workflow.
    - [x] Run WIDOCO on push to `master` and on release tags.
    - [x] Upload the generated HTML as a Pages artifact.
- [x] Task: Deploy generated documentation to GitHub Pages
    - [x] Configure Pages deployment in `.github/workflows/widoco-pages.yml`.
    - [x] Publish generated WIDOCO HTML under the GitHub Pages site root or `/docs/`.
    - [x] Add links from `README.md`, release notes, and registry submission files to the Pages documentation.
    - [x] Gate the deploy job behind `ENABLE_PAGES_DEPLOY=true` so artifact generation can remain green until Pages is enabled in repository settings.
    - [x] Copy WIDOCO `index-en.html` to `index.html` in CI so the Pages root URL resolves.

### Required Configuration Files
- `.github/workflows/widoco-pages.yml`
- `docs/widoco/widoco.properties`
- `docs/widoco/README.md`

### Acceptance Criteria
- [x] WIDOCO runs successfully in CI on the canonical ontology inputs.
  - GitHub Actions run `27910154887` passed the WIDOCO build job on 2026-06-21 UTC after commit `000df52`.
- [x] Generated HTML includes ontology metadata, class/property documentation, namespace declarations, and license information.
  - The same run generated WIDOCO HTML from `dist/uogto.ttl` and uploaded the Pages artifact successfully.
- [x] GitHub Pages deploys the generated documentation for the latest `master` build and release tags after Pages is enabled and `ENABLE_PAGES_DEPLOY=true` is set.
  - Pages is enabled, `ENABLE_PAGES_DEPLOY=true` is set, workflow run `27910392764` deployed successfully, and both `https://edithatogo.github.io/UOGTO/` and `/index-en.html` returned HTTP 200.
- [x] Documentation links are stable and included in the v1.0 release notes.

## Phase 3: Linked Open Vocabularies Submission
- [~] Task: Prepare LOV metadata checklist
    - [x] Create `docs/registry/metadata-checklist.md` covering title, description, preferred namespace URI, prefix, version IRI, creators, publisher, license URI, imports, vocabulary status, examples, and documentation URL.
    - [x] Verify ontology headers expose required registry annotations such as `rdfs:label`, `skos:definition`, `dcterms:title`, `dcterms:description`, `dcterms:creator`, `dcterms:license`, `owl:versionInfo`, `vann:preferredNamespacePrefix`, and `vann:preferredNamespaceUri` where applicable.
    - [x] Confirm the license URI is machine-readable and consistent across repository metadata, ontology headers, `CITATION.cff`, and `.zenodo.json`.
- [x] Task: Create LOV submission package
    - [x] Create `docs/registry/lov-submission.md` with ontology title, abstract, namespace, prefix, homepage, documentation URL, GitHub URL, release URL, DOI, license, maintainers, and contact route.
    - [x] List canonical downloadable RDF URLs for the combined ontology and primary modules.
    - [x] Record any required LOV issue, pull request, or submission form details.
- [ ] Task: Submit to LOV
    - [ ] Complete the formal LOV submission after v1.0 DOI and WIDOCO Pages documentation are live.
    - [ ] Track submission URL, review feedback, required metadata corrections, and final acceptance status in `docs/registry/lov-submission.md`.

### Required Configuration Files
- `docs/registry/metadata-checklist.md`
- `docs/registry/lov-submission.md`
- Updates to ontology module headers if metadata gaps are found.

### Acceptance Criteria
- [x] Metadata checklist is complete and all mandatory LOV fields are satisfied in repo-side metadata.
- [ ] Canonical ontology namespace, prefix, documentation URL, license URI, and DOI are stable.
- [x] LOV submission record exists with submission date, link, and review status.
- [ ] Any LOV-requested corrections are captured as follow-up Conductor tasks.

## Phase 4: Ontology Lookup Service Indexing
- [~] Task: Verify OLS compatibility
    - [x] Create `docs/registry/ols-indexing.md` with OLS inclusion requirements, ontology URL, preferred prefix, title, description, license, homepage, documentation URL, and contact route.
    - [x] Define stable release asset URLs for canonical ontology artifacts.
    - [ ] Verify OLS can retrieve the canonical ontology artifact through the published release asset URL or PURL.
    - [x] Confirm ontology metadata exposes version, namespace, labels, definitions, hierarchy, and license in formats suitable for OLS indexing.
- [x] Task: Prepare OLS inclusion request
    - [x] Document the requested ontology identifier and display title.
    - [x] Include links to GitHub repository, GitHub Pages WIDOCO documentation, v1.0 release, Zenodo DOI, and canonical RDF download.
    - [x] Record expected refresh cadence and maintainer contact details.
- [ ] Task: Submit OLS indexing request
    - [ ] Submit the inclusion request after LOV submission materials and WIDOCO documentation are complete.
    - [ ] Track request URL, reviewer feedback, metadata changes, and indexing outcome in `docs/registry/ols-indexing.md`.

### Required Configuration Files
- `docs/registry/ols-indexing.md`
- `docs/registry/metadata-checklist.md`
- Updates to ontology distribution metadata if OLS compatibility checks fail.

### Acceptance Criteria
- [x] OLS compatibility checklist passes for repo-side ontology metadata.
- [ ] OLS compatibility checklist passes for the published ontology artifact.
- [ ] Inclusion request is submitted with stable documentation, release, DOI, and RDF artifact links.
- [ ] OLS review feedback is tracked and resolved or converted into follow-up Conductor tasks.
- [ ] OLS indexing status is recorded once accepted or rejected.

## Phase 5: Release Gate and Ongoing Documentation Maintenance
- [x] Task: Add publishing release gate
    - [x] Update release checklist to require `make validate`, `make test`, semantic audit, WIDOCO build, citation metadata validation, and registry metadata checklist review.
    - [x] Add a manual approval step before publishing GitHub releases that mint Zenodo DOIs.
- [~] Task: Keep documentation continuously current
    - [x] Ensure CI regenerates WIDOCO documentation on ontology changes.
    - [x] Add scheduled or release-triggered checks for stale registry metadata links.
    - [x] Record post-release DOI, Pages, LOV, and OLS status in `.conductor/status.md`.

### Required Configuration Files
- `docs/releases/v1.0.md`
- `.github/workflows/widoco-pages.yml`
- `docs/registry/metadata-checklist.md`
- `.conductor/status.md`

### Acceptance Criteria
- [x] Publishing gate is documented and enforced before v1.0 release.
- [x] Scheduled maintenance runs registry documentation link checks with known unpublished release URLs explicitly allowed.
- [x] Continuous documentation generation remains green after ontology changes.
  - `Build WIDOCO Pages` run `27910392764` passed after Pages enablement and deployed the generated documentation.
- [x] DOI, documentation, LOV, and OLS statuses are visible from Conductor status.
