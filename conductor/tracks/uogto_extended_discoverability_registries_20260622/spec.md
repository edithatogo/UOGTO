# Specification: Extended Discoverability Registries

## Purpose
Extend UOGTO discoverability beyond the completed first-wave publication path: GitHub release assets, Zenodo DOI, WIDOCO Pages, w3id PR, LOV submission, and OLS submission.

This track converts the recommended second-wave registry targets into an auditable Conductor plan. It should not replace the existing `uogto_publishing_discoverability_20260622` track; it starts after DOI recording and LOV/OLS submission are complete.

## Scope
- Submit UOGTO to FAIRsharing as a terminology/ontology or standard-like resource.
- Register RDF namespace mappings for `uogto` and `uogtox` in prefix.cc.
- Create or update Wikidata coverage for UOGTO with DOI, repository, documentation, release, license, and ontology classification metadata.
- Evaluate Ontobee feasibility after w3id redirects resolve.
- Evaluate BioPortal only if UOGTO is positioned for biomedical, clinical, public-health, behavioural-science, or health-simulation ontology users.
- Evaluate Bioregistry if stable cross-registry prefix alignment is useful after w3id, LOV, OLS, and prefix.cc state is known.
- Record a negative decision for OBO Foundry unless UOGTO is explicitly repositioned for biological or biomedical ontology governance.

## Out of Scope
- Reworking ontology semantics solely to satisfy a registry unless a maintainer requests a specific correction.
- Claiming acceptance or indexing before an external maintainer, service, or live record confirms it.
- Submitting to biomedical-specific registries without a defensible domain positioning note.

## Inputs
- Zenodo DOI: `10.5281/zenodo.20796937`
- Documentation: `https://edithatogo.github.io/UOGTO/`
- Repository: `https://github.com/edithatogo/UOGTO`
- Release: `https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0`
- Canonical RDF asset: `https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl`
- Current LOV issue: `https://github.com/pyvandenbussche/lov/issues/83`
- Current OLS issue: `https://github.com/EBISPOT/ols4/issues/1305`
- Current w3id PR: `https://github.com/perma-id/w3id.org/pull/6238`

## Success Criteria
- Each recommended registry has either a submitted record/request URL or a documented negative/conditional decision.
- Public metadata remains consistent with `CITATION.cff`, `.zenodo.json`, release notes, registry docs, and generated publication packets.
- Conductor status/runlog record submissions, review outcomes, and unresolved external blockers.
- `make validate` and `make test` pass after repo-side updates.
