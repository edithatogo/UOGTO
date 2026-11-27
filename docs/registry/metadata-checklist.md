# Registry Metadata Checklist

This checklist is shared by the Zenodo, LOV, and OLS publication workflows.

## Core Metadata
- [x] Title: `Universal Open Game Theory Ontology (UOGTO)`
- [x] Repository: <https://github.com/edithatogo/UOGTO>
- [x] Core namespace URI: `https://w3id.org/uogto/core#`
- [x] Extension namespace URI: `https://w3id.org/uogto/extensions#`
- [x] Preferred core prefix: `uogto`
- [x] Preferred extension prefix: `uogtox`
- [x] Version: `1.0.0`
- [x] Ontology and documentation license URI: <https://creativecommons.org/licenses/by/4.0/>
- [x] Code license: MIT, see `LICENSE-CODE`
- [x] Citation metadata: `CITATION.cff`
- [x] Zenodo metadata: `.zenodo.json`
- [x] Author ORCID: <https://orcid.org/0000-0002-9775-0603>
- [x] WIDOCO documentation target: <https://edithatogo.github.io/UOGTO/>
- [x] Zenodo DOI: <https://doi.org/10.5281/zenodo.20796937>

## Cross-Registry Lessons From Maintainer Feedback

- [x] Namespace policy: treat `uogto` / `https://w3id.org/uogto/core#` as the primary stable core prefix, while keeping `uogtox` / `https://w3id.org/uogto/extensions#` as the intentionally separate extension namespace unless a future compatibility track changes published IRIs.
- [x] ORCID policy: the approved sole-author/contact ORCID is public project metadata and should be included where registry schemas support contributor or contact ORCID fields.
- [x] Biomedical and health relevance note: UOGTO supports game-theoretic modelling across genomics, clinical genetics, paediatrics, health economics, behavioural/public-health interaction models, mechanism design, and health-simulation settings.
- [x] Cross-registry supplements posted for LOV, OLS, and Ontobee after OLS and Bioregistry feedback.
- [x] Accepted or live records without comment threads, including prefix.cc and Wikidata, require no retroactive edit unless their registry schema has a defensible field for the new metadata.
- [x] BARTOC handoff is recorded in `docs/registry/bartoc-submission.md`.
- [x] RVA handoff is recorded in `docs/registry/rva-submission.md`.

## Ontology Annotation Requirements
- [x] Every class and property is covered by the semantic audit for `rdfs:label` and `skos:definition`.
- [x] Release ontology header exposes `dcterms:title`.
- [x] Release ontology header exposes `dcterms:description`.
- [x] Release ontology header exposes `dcterms:creator`.
- [x] Release ontology header exposes `dcterms:license`.
- [x] Release ontology header exposes `owl:versionInfo`.
- [x] Release ontology header exposes `vann:preferredNamespacePrefix`.
- [x] Release ontology header exposes `vann:preferredNamespaceUri`.
- [x] Publishing metadata gate parses ontology source modules and verifies release header metadata.

## Distribution Requirements
- [x] Merged ontology build command: `make build`
- [x] Validation command: `make validate`
- [x] Test command: `make test`
- [x] Publishing metadata validation command: `python scripts/maintenance/check_publishing_metadata.py`
- [x] Public merged ontology URL is available from a release asset, GitHub Pages, raw GitHub URL, or PURL.
- [x] Public SHACL shapes URL is available from a release asset, GitHub Pages, raw GitHub URL, or PURL.
- [x] w3id namespace redirects are live for `https://w3id.org/uogto/core#` and `https://w3id.org/uogto/extensions#`.

## Registry Gate
- [x] GitHub release `v1.0.0` is published.
- [x] Zenodo DOI is minted and recorded.
- [x] WIDOCO Pages documentation is live.
- [x] LOV submission document is complete.
- [x] LOV submission issue is open: <https://github.com/pyvandenbussche/lov/issues/83>.
- [x] OLS indexing document is complete.
- [x] OLS indexing issue is open: <https://github.com/EBISPOT/ols4/issues/1305>.
- [x] LOV metadata supplement: <https://github.com/pyvandenbussche/lov/issues/83#issuecomment-4902620021>.
- [x] OLS metadata supplement: <https://github.com/EBISPOT/ols4/issues/1305#issuecomment-4902620274>.
- [x] Ontobee metadata supplement: <https://github.com/OntoZoo/ontobee/issues/212#issuecomment-4902620502>.
