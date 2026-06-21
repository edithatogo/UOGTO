# Implementation Plan: Publishing and Discoverability

This plan begins after the completed UOGTO ontology modeling, SHACL validation, example, competency-query, and repository maintenance phases. It converts the validated ontology repository into a citable, documented, and discoverable public ontology project.

## Phase 1: Zenodo Integration and DOI Release
- [ ] Task: Configure Zenodo repository integration
    - [ ] Enable the GitHub-Zenodo repository link for `edithatogo/UOGTO`.
    - [ ] Verify Zenodo is configured to archive GitHub releases, not every branch push.
    - [ ] Document the release archive flow in `docs/releases/v1.0.md`.
- [ ] Task: Add citation metadata
    - [ ] Create `CITATION.cff` with title, authors, repository URL, ontology URL, license, version, release date, and preferred citation.
    - [ ] Create `.zenodo.json` with creators, title, description, keywords, related identifiers, license, and communities if applicable.
    - [ ] Cross-check author names and ORCID fields before release.
- [ ] Task: Draft v1.0 release notes
    - [ ] Create `docs/releases/v1.0.md` summarizing ontology scope, included modules, validation status, examples, documentation links, and known limitations.
    - [ ] Include DOI placeholder text that can be replaced after the Zenodo archive is minted.
    - [ ] Add release checklist entries for `make validate`, `make test`, semantic audit, and generated documentation.

### Required Configuration Files
- `CITATION.cff`
- `.zenodo.json`
- `docs/releases/v1.0.md`

### Acceptance Criteria
- [ ] Zenodo shows `edithatogo/UOGTO` as enabled for release archiving.
- [ ] A GitHub `v1.0.0` release creates a Zenodo archive and DOI.
- [ ] `CITATION.cff` metadata matches GitHub release notes and Zenodo metadata.
- [ ] Release notes include validation evidence and links to canonical ontology assets.

## Phase 2: WIDOCO Documentation and GitHub Pages
- [ ] Task: Add WIDOCO documentation configuration
    - [ ] Create `docs/widoco/widoco.properties` defining ontology input paths, output directory, project title, ontology URI, preferred prefix, license, and provenance metadata.
    - [ ] Create `docs/widoco/README.md` with local documentation build instructions and expected output location.
    - [ ] Decide whether documentation is generated from `dist/` combined assets or individual canonical ontology modules, and record the decision in the WIDOCO README.
- [ ] Task: Add CI/CD documentation generation
    - [ ] Create `.github/workflows/widoco-pages.yml`.
    - [ ] Install Java and WIDOCO in the workflow.
    - [ ] Run WIDOCO on push to `master` and on release tags.
    - [ ] Upload the generated HTML as a Pages artifact.
- [ ] Task: Deploy generated documentation to GitHub Pages
    - [ ] Configure Pages deployment in `.github/workflows/widoco-pages.yml`.
    - [ ] Publish generated WIDOCO HTML under the GitHub Pages site root or `/docs/`.
    - [ ] Add links from `README.md`, release notes, and registry submission files to the Pages documentation.

### Required Configuration Files
- `.github/workflows/widoco-pages.yml`
- `docs/widoco/widoco.properties`
- `docs/widoco/README.md`

### Acceptance Criteria
- [ ] WIDOCO runs successfully in CI on the canonical ontology inputs.
- [ ] Generated HTML includes ontology metadata, class/property documentation, namespace declarations, and license information.
- [ ] GitHub Pages deploys the generated documentation for the latest `master` build and release tags.
- [ ] Documentation links are stable and included in the v1.0 release notes.

## Phase 3: Linked Open Vocabularies Submission
- [ ] Task: Prepare LOV metadata checklist
    - [ ] Create `docs/registry/metadata-checklist.md` covering title, description, preferred namespace URI, prefix, version IRI, creators, publisher, license URI, imports, vocabulary status, examples, and documentation URL.
    - [ ] Verify every ontology module includes required standard annotations such as `rdfs:label`, `skos:definition`, `dcterms:title`, `dcterms:description`, `dcterms:creator`, `dcterms:license`, `owl:versionInfo`, and `vann:preferredNamespacePrefix` where applicable.
    - [ ] Confirm the license URI is machine-readable and consistent across repository metadata, ontology headers, `CITATION.cff`, and `.zenodo.json`.
- [ ] Task: Create LOV submission package
    - [ ] Create `docs/registry/lov-submission.md` with ontology title, abstract, namespace, prefix, homepage, documentation URL, GitHub URL, release URL, DOI, license, maintainers, and contact route.
    - [ ] List canonical downloadable RDF URLs for the combined ontology and primary modules.
    - [ ] Record any required LOV issue, pull request, or submission form details.
- [ ] Task: Submit to LOV
    - [ ] Complete the formal LOV submission after v1.0 DOI and WIDOCO Pages documentation are live.
    - [ ] Track submission URL, review feedback, required metadata corrections, and final acceptance status in `docs/registry/lov-submission.md`.

### Required Configuration Files
- `docs/registry/metadata-checklist.md`
- `docs/registry/lov-submission.md`
- Updates to ontology module headers if metadata gaps are found.

### Acceptance Criteria
- [ ] Metadata checklist is complete and all mandatory LOV fields are satisfied.
- [ ] Canonical ontology namespace, prefix, documentation URL, license URI, and DOI are stable.
- [ ] LOV submission record exists with submission date, link, and review status.
- [ ] Any LOV-requested corrections are captured as follow-up Conductor tasks.

## Phase 4: Ontology Lookup Service Indexing
- [ ] Task: Verify OLS compatibility
    - [ ] Create `docs/registry/ols-indexing.md` with OLS inclusion requirements, ontology URL, preferred prefix, title, description, license, homepage, documentation URL, and contact route.
    - [ ] Verify OLS can retrieve the canonical ontology artifact through a stable raw URL, release asset URL, or PURL.
    - [ ] Confirm ontology metadata exposes version, namespace, labels, definitions, hierarchy, and license in formats suitable for OLS indexing.
- [ ] Task: Prepare OLS inclusion request
    - [ ] Document the requested ontology identifier and display title.
    - [ ] Include links to GitHub repository, GitHub Pages WIDOCO documentation, v1.0 release, Zenodo DOI, and canonical RDF download.
    - [ ] Record expected refresh cadence and maintainer contact details.
- [ ] Task: Submit OLS indexing request
    - [ ] Submit the inclusion request after LOV submission materials and WIDOCO documentation are complete.
    - [ ] Track request URL, reviewer feedback, metadata changes, and indexing outcome in `docs/registry/ols-indexing.md`.

### Required Configuration Files
- `docs/registry/ols-indexing.md`
- `docs/registry/metadata-checklist.md`
- Updates to ontology distribution metadata if OLS compatibility checks fail.

### Acceptance Criteria
- [ ] OLS compatibility checklist passes for the published ontology artifact.
- [ ] Inclusion request is submitted with stable documentation, release, DOI, and RDF artifact links.
- [ ] OLS review feedback is tracked and resolved or converted into follow-up Conductor tasks.
- [ ] OLS indexing status is recorded once accepted or rejected.

## Phase 5: Release Gate and Ongoing Documentation Maintenance
- [ ] Task: Add publishing release gate
    - [ ] Update release checklist to require `make validate`, `make test`, semantic audit, WIDOCO build, citation metadata validation, and registry metadata checklist review.
    - [ ] Add a manual approval step before publishing GitHub releases that mint Zenodo DOIs.
- [ ] Task: Keep documentation continuously current
    - [ ] Ensure CI regenerates WIDOCO documentation on ontology changes.
    - [ ] Add scheduled or release-triggered checks for stale registry metadata links.
    - [ ] Record post-release DOI, Pages, LOV, and OLS status in `.conductor/status.md`.

### Required Configuration Files
- `docs/releases/v1.0.md`
- `.github/workflows/widoco-pages.yml`
- `docs/registry/metadata-checklist.md`
- `.conductor/status.md`

### Acceptance Criteria
- [ ] Publishing gate is documented and enforced before v1.0 release.
- [ ] Continuous documentation generation remains green after ontology changes.
- [ ] DOI, documentation, LOV, and OLS statuses are visible from Conductor status.
