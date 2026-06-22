# Extended Discoverability Submissions

## Status
Second-wave discoverability is partially implemented. Repo-side metadata, a machine-readable packet, prefix.cc core prefix registration, and Bioregistry issue submission are complete. FAIRsharing and Wikidata require authenticated account actions. `uogtox` prefix.cc registration is blocked by prefix.cc's one-per-day contribution limit. Ontobee is deferred until w3id redirects are live. BioPortal and OBO Foundry are not current targets without a stronger biomedical scope.

## Shared Submission Metadata
- Ontology title: Universal Open Game Theory Ontology (UOGTO)
- Preferred core prefix: `uogto`
- Preferred extension prefix: `uogtox`
- Core namespace: `https://w3id.org/uogto/core#`
- Extension namespace: `https://w3id.org/uogto/extensions#`
- Homepage: <https://github.com/edithatogo/UOGTO>
- Documentation: <https://edithatogo.github.io/UOGTO/>
- GitHub repository: <https://github.com/edithatogo/UOGTO>
- Release URL: <https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0>
- DOI: <https://doi.org/10.5281/zenodo.20796937>
- License: <https://creativecommons.org/licenses/by/4.0/>
- Canonical RDF release asset: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl>
- SHACL shapes release asset: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto-shapes.ttl>
- Maintainer route: GitHub issues on `edithatogo/UOGTO`

## Existing First-Wave Registry State
- LOV submission: <https://github.com/pyvandenbussche/lov/issues/83>
- OLS request: <https://github.com/EBISPOT/ols4/issues/1305>
- w3id redirect PR: <https://github.com/perma-id/w3id.org/pull/6238>
- Zenodo record: <https://zenodo.org/records/20796937>

## Target Records

### FAIRsharing
- Status: `prepared_account_required`
- Route: <https://fairsharing.org/>
- Guidance: <https://fairsharing.gitbook.io/fairsharing/record-sections-and-fields/general-information/registry-type>
- Recommended registry type: Standards record, terminology artefact / ontology.
- Evidence: FAIRsharing describes terminology artefacts as controlled vocabularies or ontologies and requires enough metadata for community-backed standards.
- Blocker: submission/update requires an authenticated FAIRsharing account and JavaScript web workflow; no repository-safe token is available.
- Next action: create a FAIRsharing record from the shared submission metadata after logging in with the maintainer account.

### prefix.cc
- Status: `partial`
- `uogto`: submitted and live at <http://prefix.cc/uogto.file.txt>, mapping to `https://w3id.org/uogto/core#`.
- `uogtox`: pending due prefix.cc one-per-day contribution limit, mapping target `https://w3id.org/uogto/extensions#`.
- Route: <http://prefix.cc/>
- Evidence: prefix.cc accepted the `uogto` POST and returned the submitted namespace expansion; a subsequent `uogtox` POST returned `You can add only one per day. Please try again tomorrow.`
- Next action: submit `uogtox` after 2026-06-24 local time.

### Wikidata
- Status: `prepared_account_required`
- Route: <https://www.wikidata.org/>
- Search evidence: Wikidata API search for `UOGTO` and `Universal Open Game Theory Ontology` returned no matching item.
- Blocker: creating or editing a Wikidata item requires an authenticated Wikidata account and edit token.
- Suggested statements:
  - label: Universal Open Game Theory Ontology
  - aliases: UOGTO
  - description: modular OWL/SHACL ontology for game-theoretic semantics
  - DOI: `10.5281/zenodo.20796937`
  - official website / documentation: `https://edithatogo.github.io/UOGTO/`
  - source code repository: `https://github.com/edithatogo/UOGTO`
  - license: Creative Commons Attribution 4.0 International

### Ontobee
- Status: `deferred_pending_w3id`
- Route: <https://ontobee.org/>
- Rationale: Ontobee is most useful once stable namespace redirects resolve and can be used as linked-data term entry points. UOGTO's w3id PR is still pending upstream merge/live redirect propagation.
- Next action: reassess after `https://w3id.org/uogto/core#` and `https://w3id.org/uogto/extensions#` resolve through w3id.

### BioPortal
- Status: `not_submitted_conditional`
- Route: <https://bioportal.bioontology.org/>
- Rationale: BioPortal is primarily a biomedical ontology portal. UOGTO should only be submitted there if the project adopts a defensible biomedical, clinical, public-health, behavioural-science, or health-simulation positioning note.
- Next action: do not submit unless that domain-positioning note is approved.

### Bioregistry
- Status: `submitted`
- Route: <https://bioregistry.io/>
- Issue: <https://github.com/biopragmatics/bioregistry/issues/1999>
- Requested prefix: `uogto`
- Requested URI format: `https://w3id.org/uogto/core#`
- Evidence: no prior UOGTO Bioregistry issue was found before opening issue `1999`.

### OBO Foundry
- Status: `not_prioritized`
- Route: <https://obofoundry.org/>
- Rationale: OBO Foundry is not a target unless UOGTO is explicitly repositioned for biological or biomedical ontology governance.
- Next action: no routine action; revisit only with a concrete biomedical governance fit.

## Follow-Up Queue
- Retry prefix.cc `uogtox` submission after the one-per-day rate limit resets.
- Submit FAIRsharing through an authenticated maintainer session.
- Create or update Wikidata through an authenticated maintainer session.
- Reassess Ontobee after w3id redirects are live.
- Track Bioregistry issue review feedback.
