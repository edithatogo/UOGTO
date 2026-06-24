# Extended Discoverability Submissions

## Status
Second-wave discoverability is repo-side implemented with live prefix.cc mappings for `uogto` and `uogtox`, submitted Bioregistry and Ontobee requests, live Wikidata item `Q140323510`, and FAIRsharing draft record `8382`. FAIRsharing is not yet sent to curation because its required `data processes and conditions` editor did not persist a valid submitted item. BioPortal and OBO Foundry are not current targets without a stronger biomedical scope.

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
- Status: `draft_created_required_field_blocked`
- Route: <https://fairsharing.org/>
- Record: <https://fairsharing.org/8382>
- Guidance: <https://fairsharing.gitbook.io/fairsharing/record-sections-and-fields/general-information/registry-type>
- Recommended registry type: Standards record, terminology artefact / ontology.
- Evidence: FAIRsharing describes terminology artefacts as controlled vocabularies or ontologies and requires enough metadata for community-backed standards.
- Account evidence: draft record created and updated through an authenticated FAIRsharing session on 2026-06-24.
- Populated metadata: title, abbreviation, homepage, year of creation `2026`, country `Australia`, status `Ready`, registry type `Standard / Terminology Artefact`, contact point `Dylan Mordaunt`, taxonomic range `Not Applicable`, subject `Knowledge And Information Systems`, domain `Knowledge Representation`, object type `Dataset`, user tags `Semantic Web` and `Ontology`, CC-BY-4.0 licence, GitHub repository support link, documentation support link, and Zenodo DOI support link.
- Blocker: the public FAIRsharing page reports required field `data processes and conditions`; the edit form exposed the required controls and enabled submit attempts for `read` / `User interface` and `read` / `Other machine-accessible method`, but no data-process item persisted after submit and reload.
- Recommended remaining fields: organisation links, publications, citations, and record associations.
- Next action: resolve the FAIRsharing `data processes and conditions` editor through FAIRsharing support or a manual UI/API correction, then submit/send the record to curation and record curation/DOI status.

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
- Status: `submitted_template_updated`
- Route: <https://bioregistry.io/>
- Issue: <https://github.com/biopragmatics/bioregistry/issues/1999>
- Maintainer template request: <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4769473415>
- Template update comment: <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220>
- Requested prefix: `uogto`
- Requested URI format: `https://w3id.org/uogto/core#`
- Evidence: no prior UOGTO Bioregistry issue was found before opening issue `1999`; the issue body was updated to the new-prefix template without inventing an ORCID absent from repository metadata.
- Next action: track maintainer review feedback.

### OBO Foundry
- Status: `not_prioritized`
- Route: <https://obofoundry.org/>
- Rationale: OBO Foundry is not a target unless UOGTO is explicitly repositioned for biological or biomedical ontology governance.
- Next action: no routine action; revisit only with a concrete biomedical governance fit.

## Follow-Up Queue
- Resolve FAIRsharing record `8382` required `data processes and conditions` persistence, then submit it to curation.
- Track Ontobee issue review feedback and index outcome.
- Track Bioregistry issue review feedback.
