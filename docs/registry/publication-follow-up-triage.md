# Publication Follow-Up Triage

Last verified: `2026-07-05`

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

## Queue

| ID | Registry | Status | Classification | Target artifact | Acceptance criterion |
| --- | --- | --- | --- | --- | --- |
| `lov-review-83` | LOV | `submitted_awaiting_maintainer_review` | external-review | `docs/registry/lov-submission.md` | LOV issue is accepted, rejected, or receives actionable feedback that is converted into a scoped Conductor task. |
| `ols-indexing-1305` | OLS | `accepted_pending_indexing` | external-review | `docs/registry/ols-indexing.md` | OLS exposes UOGTO in the public index or closes the issue with a clear disposition. |
| `fairsharing-curation-8382` | FAIRsharing | `submitted_awaiting_curation` | metadata-follow-up | `docs/registry/extended-discoverability-submissions.md` | Curator decision, public status, issued identifier, or recommended metadata patch is recorded. |
| `ontobee-indexing-212` | Ontobee | `submitted_awaiting_maintainer_review` | external-review | `docs/registry/extended-discoverability-submissions.md` | Ontobee indexes UOGTO, rejects the request, or asks for a scoped metadata/ontology change. |
| `bioregistry-prefix-1999` | Bioregistry | `maintainer_feedback_needs_response` | metadata-policy | `docs/registry/extended-discoverability-submissions.md` | A maintainer response defends the two-namespace design or creates an accepted namespace-consolidation follow-up task. |

## Current Notes

- OLS maintainer feedback on 2026-06-29 says the ontology will be added, but the issue remains open; this is `accepted_pending_indexing`, not locally complete.
- Bioregistry feedback on 2026-06-25 asks whether `https://w3id.org/uogto/core#` and `https://w3id.org/uogto/extensions#` should be squashed together and asks for an ORCID. The repo should not invent ORCID metadata absent from public project metadata.
- Local issue <https://github.com/edithatogo/UOGTO/issues/34> tracks the Bioregistry response decision and any namespace-consolidation follow-up.
- LOV and Ontobee have no maintainer feedback recorded as of this verification pass.
