# Ontology Lookup Service Indexing

## Status
Submitted on 2026-06-22 through the active OLS GitHub issue route after v1.0 release assets, WIDOCO documentation, and Zenodo DOI metadata were public. Live follow-up on 2026-07-06 confirmed OLS maintainer feedback that the ontology will be added, with issue `1305` still open pending indexing closeout. Public OLS API/search checks on 2026-07-06 did not yet expose a `uogto` ontology entry. A cross-registry metadata supplement was posted on 2026-07-07 so the accepted-pending-indexing request also has the namespace policy, ORCID, release evidence, and health-relevance summary now used across the registry queue.

Submission route checked 2026-06-22: the current OLS repository is `EBISPOT/ols4` at <https://github.com/EBISPOT/ols4>, with homepage <https://www.ebi.ac.uk/ols4/>. The repository exposes a dedicated issue template for adding a new ontology: <https://github.com/EBISPOT/ols4/blob/dev/.github/ISSUE_TEMPLATE/add-a-new-ontology-to-the-ebi-ols-instance-.md>.

## Requested Indexing Metadata
- Ontology identifier: `uogto`
- Display title: Universal Open Game Theory Ontology
- Preferred prefix: `uogto`
- Core namespace: `https://w3id.org/uogto/core#`
- Extension namespace: `https://w3id.org/uogto/extensions#`
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

## Biomedical And Health Relevance

OLS maintainer feedback asked how UOGTO relates to the biomedical field. The accepted response framed UOGTO as relevant to game-theoretic modelling across genomics, clinical genetics, paediatrics, health economics, behavioural and public-health interaction models, mechanism design, and health-simulation settings where strategic interaction and incentives need reusable semantic representation.

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
- [x] Track reviewer feedback.
- [x] Convert requested changes into Conductor follow-up tasks.
  - No metadata changes were requested; OLS maintainer response says the ontology will be added.
- [x] Post cross-registry metadata supplement after Bioregistry namespace/ORCID feedback.

## Request Record
- Request date: `2026-06-22`
- Request URL: <https://github.com/EBISPOT/ols4/issues/1305>
- Review status: `Accepted by OLS maintainer; awaiting indexing closeout`
- Indexing status: `Accepted pending public OLS index URL`; OLS API/search did not expose `uogto` as of 2026-07-06.
- Maintainer acceptance evidence: <https://github.com/EBISPOT/ols4/issues/1305#issuecomment-4833153237>
- Metadata supplement: <https://github.com/EBISPOT/ols4/issues/1305#issuecomment-4902620274>
