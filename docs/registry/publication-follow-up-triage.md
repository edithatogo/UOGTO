# Publication Follow-Up Triage

Last verified: `2026-07-07`

This queue records external registry feedback after UOGTO `v1.0.0`. It keeps
curator and maintainer waiting states separate from repo-side validation
failures.

Machine-readable queue: `docs/registry/publication-follow-up-triage.json`.

## Live Publication State

- Publication status packet: `published`
- Documentation: live at <https://edithatogo.github.io/UOGTO/>
- Release assets: live for `v1.0.0`
- Zenodo DOI: <https://doi.org/10.5281/zenodo.20796937>
- w3id redirects: live for `/uogto/`, `/uogto/core`, and `/uogto/extensions`
- prefix.cc mappings: `uogto` and `uogtox` TXT endpoints return expected namespace URIs
- Wikidata: item <https://www.wikidata.org/wiki/Q140323510> returns entity data with the UOGTO label
- FAIRsharing: record <https://fairsharing.org/8382> is live

## Cross-Registry Lessons Applied

- `uogto` is the primary stable core prefix for `https://w3id.org/uogto/core#`; `uogtox` remains the intentionally separate extension prefix for `https://w3id.org/uogto/extensions#`.
- The approved sole-author/contact ORCID is <https://orcid.org/0000-0002-9775-0603>.
- The OLS biomedical/health relevance clarification is now the reusable registry note for health-facing portals.
- Metadata supplements were posted to LOV <https://github.com/pyvandenbussche/lov/issues/83#issuecomment-4902620021>, OLS <https://github.com/EBISPOT/ols4/issues/1305#issuecomment-4902620274>, and Ontobee <https://github.com/OntoZoo/ontobee/issues/212#issuecomment-4902620502>.

## Queue

| ID | Registry | Status | Classification | Target artifact | Acceptance criterion |
| --- | --- | --- | --- | --- | --- |
| `lov-review-83` | LOV | `submitted_awaiting_maintainer_review` | external-review | `docs/registry/lov-submission.md` | LOV issue is accepted, rejected, or receives actionable feedback that is converted into a scoped Conductor task. |
| `ols-indexing-1305` | OLS | `accepted_pending_indexing` | external-review | `docs/registry/ols-indexing.md` | OLS exposes UOGTO in the public index or closes the issue with a clear disposition. |
| `fairsharing-curation-8382` | FAIRsharing | `submitted_awaiting_curation` | metadata-follow-up | `docs/registry/extended-discoverability-submissions.md` | Curator decision, public status, issued identifier, or recommended metadata patch is recorded. |
| `ontobee-indexing-212` | Ontobee | `submitted_awaiting_maintainer_review` | external-review | `docs/registry/extended-discoverability-submissions.md` | Ontobee indexes UOGTO, rejects the request, or asks for a scoped metadata/ontology change. |
| `bioregistry-prefix-1999` | Bioregistry | `orcid_added_awaiting_maintainer_review` | metadata-policy | `docs/registry/bioregistry-namespace-response.md` | Bioregistry maintainers accept the primary core prefix record, reject it, or request a squashed-namespace compatibility decision that is converted into a scoped Conductor track. |

## Current Notes

- OLS maintainer feedback on 2026-06-29 says the ontology will be added, but the issue remains open; public OLS API/search checks on 2026-07-06 did not yet expose UOGTO. This is `accepted_pending_indexing`, not locally complete. A metadata supplement was posted on 2026-07-07 so the accepted request also has the current namespace, ORCID, and health-relevance note.
- Bioregistry feedback on 2026-06-25 asked whether `https://w3id.org/uogto/core#` and `https://w3id.org/uogto/extensions#` should be squashed together and asked for an ORCID.
- UOGTO response <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4885550451> defends the published two-namespace design for `v1.0.0`, asks Bioregistry to treat `uogto` as the primary core prefix, and keeps `uogtox` documented separately for extension modules.
- ORCID follow-up <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4885988980> records the approved sole-author/contact ORCID <https://orcid.org/0000-0002-9775-0603>, which is now mirrored in `CITATION.cff`, `.zenodo.json`, and the Bioregistry issue body.
- Local issue <https://github.com/edithatogo/UOGTO/issues/34> tracks the Bioregistry response decision; any required namespace squashing should become a separate ontology-compatibility track rather than a metadata-only edit.
- LOV has no maintainer feedback recorded; public LOV `uogto` vocabulary API/page routes still return 404 in the latest live check; the 2026-07-07 metadata supplement is posted.
- Ontobee issue `212` remains open with no maintainer comments; the 2026-07-07 metadata supplement is posted.
