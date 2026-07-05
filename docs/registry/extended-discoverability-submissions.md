# Extended Discoverability Submissions

## Status
Second-wave discoverability is repo-side implemented with live prefix.cc mappings for `uogto` and `uogtox`, submitted Bioregistry and Ontobee requests, live Wikidata item `Q140323510`, and FAIRsharing record `8382` awaiting curator review. BioPortal and OBO Foundry are not current targets without a stronger biomedical scope. Live follow-up on 2026-07-05 confirmed FAIRsharing, prefix.cc, Wikidata, and Zenodo pages/endpoints are reachable.

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
- w3id redirect status: merged at `2026-06-22T12:29:07Z`; `/uogto/core` and `/uogto/extensions` return 303 redirects to <https://edithatogo.github.io/UOGTO/>.
- Zenodo record: <https://zenodo.org/records/20796937>

## Target Records

### FAIRsharing
- Status: `submitted_awaiting_curation`
- Route: <https://fairsharing.org/>
- Record: <https://fairsharing.org/8382>
- Guidance: <https://fairsharing.gitbook.io/fairsharing/record-sections-and-fields/general-information/registry-type>
- Recommended registry type: Standards record, terminology artefact / ontology.
- Evidence: FAIRsharing describes terminology artefacts as controlled vocabularies or ontologies and requires enough metadata for community-backed standards.
- Account evidence: draft record created and updated through an authenticated FAIRsharing session on 2026-06-24.
- Populated metadata: title, abbreviation, homepage, year of creation `2026`, country `Australia`, status `Ready`, registry type `Standard / Terminology Artefact`, contact point `Dylan Mordaunt`, taxonomic range `Not Applicable`, subject `Knowledge And Information Systems`, domain `Knowledge Representation`, object type `Dataset`, user tags `Semantic Web` and `Ontology`, CC-BY-4.0 licence, GitHub repository support link, documentation support link, and Zenodo DOI support link.
- Curation evidence: required `data processes and conditions` metadata persisted on 2026-06-24 with `read` / `User interface` access for the public documentation and canonical RDF artifact; the public page now reports `This record is awaiting review by FAIRsharing curators`.
- Recommended remaining fields: organisation links, publications, citations, and record associations. These are nonblocking and require curation guidance or defensible FAIRsharing record associations before adding.
- Next action: monitor FAIRsharing curator review and record the FAIRsharing DOI/status when issued.

### prefix.cc
- Status: `submitted`
- Route: <http://prefix.cc/>
- `uogto`: submitted and live at <http://prefix.cc/uogto.file.txt>, mapping to `https://w3id.org/uogto/core#`.
- `uogtox`: submitted and live at <http://prefix.cc/uogtox.file.txt>, mapping to `https://w3id.org/uogto/extensions#`.
- Evidence: prefix.cc accepted the `uogto` POST and the later `uogtox` retry; both TXT endpoints return the expected mappings.
- Next action: monitor for any future mapping correction requests; no repo-side blocker remains.

### Wikidata
- Status: `created_verified`
- Route: <https://www.wikidata.org/wiki/Q140323510>
- Item: <https://www.wikidata.org/wiki/Q140323510>
- Search evidence: Wikidata search for `Universal Open Game Theory Ontology` returned no matching item before creation.
- Account evidence: created through the authenticated Wikidata session `Doughnuted` on 2026-06-24.
- Verified statements:
  - label: Universal Open Game Theory Ontology
  - aliases: UOGTO; Open Game Theory Ontology; Universal Open Game-Theory Ontology
  - description: modular OWL and SHACL ontology for game-theoretic semantics
  - instance of: ontology (`Q324254`)
  - DOI: `10.5281/zenodo.20796937`
  - official website / documentation: `https://edithatogo.github.io/UOGTO/`
  - source code repository URL: `https://github.com/edithatogo/UOGTO`
  - copyright license: Creative Commons Attribution 4.0 International (`Q20007257`)
- Live verification: Wikidata item, documentation site, GitHub repository, and Zenodo record loaded successfully in Chrome; DOI resolved to `https://zenodo.org/records/20796937`.

### Ontobee
- Status: `submitted`
- Route: <https://ontobee.org/>
- Issue: <https://github.com/OntoZoo/ontobee/issues/212>
- Evidence: w3id PR `6238` is merged and live redirects resolve before submission.
- Next action: track Ontobee issue review feedback and record the index URL if accepted.

### BioPortal
- Status: `not_submitted_conditional`
- Route: <https://bioportal.bioontology.org/>
- Rationale: BioPortal is primarily a biomedical ontology portal. UOGTO should only be submitted there if the project adopts a defensible biomedical, clinical, public-health, behavioural-science, or health-simulation positioning note.
- Next action: do not submit unless that domain-positioning note is approved.

### Bioregistry
- Status: `maintainer_feedback_needs_response`
- Route: <https://bioregistry.io/>
- Issue: <https://github.com/biopragmatics/bioregistry/issues/1999>
- Maintainer template request: <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4769473415>
- Template update comment: <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220>
- Namespace/ORCID feedback: <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4796538000>
- Requested prefix: `uogto`
- Requested URI format: `https://w3id.org/uogto/core#`
- Evidence: no prior UOGTO Bioregistry issue was found before opening issue `1999`; the issue body was updated to the new-prefix template without inventing an ORCID absent from repository metadata.
- Latest feedback: maintainer asked whether the core and extension URI formats should be squashed together and requested an ORCID.
- Next action: prepare a response from the namespace design rationale; do not invent ORCID metadata absent from public project metadata.

### OBO Foundry
- Status: `not_prioritized`
- Route: <https://obofoundry.org/>
- Rationale: OBO Foundry is not a target unless UOGTO is explicitly repositioned for biological or biomedical ontology governance.
- Next action: no routine action; revisit only with a concrete biomedical governance fit.

## Follow-Up Queue
- See `docs/registry/publication-follow-up-triage.md` and `.json` for owner, target artifact, acceptance criterion, and evidence URL per item.
- Monitor LOV issue `83` for maintainer feedback.
- Monitor OLS issue `1305` until public indexing is complete; maintainer has stated they will add the ontology.
- Monitor FAIRsharing record `8382` curator review and DOI/status outcome.
- Track Ontobee issue review feedback and index outcome.
- Respond to Bioregistry issue `1999` about two namespace formats and ORCID metadata.
