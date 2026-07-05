# Bioregistry Namespace Response Decision

Date: 2026-07-05

External issue: <https://github.com/biopragmatics/bioregistry/issues/1999>

Maintainer feedback: <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4796538000>

UOGTO response: <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4885550451>

## Decision

Retain the published UOGTO `v1.0.0` two-namespace design for the registry
response. Bioregistry should treat `uogto` as the primary core prefix with URI
format `https://w3id.org/uogto/core#$1`. The extension namespace
`https://w3id.org/uogto/extensions#` remains documented separately through the
`uogtox` prefix and existing prefix.cc mapping.

## Rationale

- The split mirrors UOGTO's existing architecture: stable core semantics in
  `ontologies/core/` and extension modules in `ontologies/extensions/`.
- The two namespaces are already present in release assets, JSON-LD contexts,
  w3id redirects, and prefix.cc mappings.
- Squashing namespaces would affect published IRIs and downstream mappings, so
  it is an ontology-compatibility decision rather than a registry metadata-only
  patch.

## ORCID Handling

No ORCID was supplied in the Bioregistry response because no approved public
ORCID is published in `CITATION.cff`, `.zenodo.json`, or the Bioregistry issue
body. UOGTO should only add an ORCID after it is intentionally published in
project metadata.

## Follow-Up Rule

If Bioregistry requires one squashed namespace before accepting the prefix, open
a separate ontology-compatibility Conductor track. Do not change published IRIs
inside a registry-response-only track.
