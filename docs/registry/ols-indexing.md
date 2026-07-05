# Ontology Lookup Service Indexing

## Status
Submitted on 2026-06-22 through the active OLS GitHub issue route after v1.0 release assets, WIDOCO documentation, and Zenodo DOI metadata were public. Live follow-up on 2026-07-05 confirmed OLS maintainer feedback that the ontology will be added, with issue `1305` still open pending indexing closeout.

Submission route checked 2026-06-22: the current OLS repository is `EBISPOT/ols4` at <https://github.com/EBISPOT/ols4>, with homepage <https://www.ebi.ac.uk/ols4/>. The repository exposes a dedicated issue template for adding a new ontology: <https://github.com/EBISPOT/ols4/blob/dev/.github/ISSUE_TEMPLATE/add-a-new-ontology-to-the-ebi-ols-instance-.md>.

## Requested Indexing Metadata
- Ontology identifier: `uogto`
- Display title: Universal Open Game Theory Ontology
- Preferred prefix: `uogto`
- Core namespace: `https://w3id.org/uogto/core#`
- Homepage: <https://github.com/edithatogo/UOGTO>
- Documentation: <https://edithatogo.github.io/UOGTO/>
- Release URL: <https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0>
- DOI: <https://doi.org/10.5281/zenodo.20796937>
- License: <https://creativecommons.org/licenses/by/4.0/>
- Maintainer route: GitHub issues on `edithatogo/UOGTO`

## Candidate Artifact URLs
- Merged ontology release asset: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl>
- SHACL shapes release asset: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto-shapes.ttl>
- Release checksums: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/SHA256SUMS>
- Release asset manifest: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/release-assets-manifest.json>
- Registry handoff packet: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/registry-handoff.json>

## OLS Compatibility Checklist
- [x] Public ontology artifact URL is stable and fetchable.
- [x] Ontology metadata exposes title, description, version, license, and preferred prefix.
- [x] Class and property labels are present.
- [x] Class and property definitions are present.
- [x] Hierarchical relationships are represented in OWL/RDFS where applicable.
- [x] License and maintainer metadata are public.
- [x] WIDOCO documentation and DOI links are live.

## Inclusion Request Checklist
- [x] Confirm metadata checklist in `docs/registry/metadata-checklist.md`.
- [x] Prepare OLS issue or request with ontology identifier, display title, artifact URL, docs URL, DOI, license, and contact route.
- [x] Submit inclusion request.
- [x] Record request date.
- [x] Record request URL.
- [ ] Track reviewer feedback.
- [ ] Convert requested changes into Conductor follow-up tasks.

## Request Record
- Request date: `2026-06-22`
- Request URL: <https://github.com/EBISPOT/ols4/issues/1305>
- Review status: `Accepted by OLS maintainer; awaiting indexing closeout`
- Indexing status: `Accepted pending public OLS index URL`
- Maintainer acceptance evidence: <https://github.com/EBISPOT/ols4/issues/1305#issuecomment-4833153237>
