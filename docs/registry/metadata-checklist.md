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
- [x] WIDOCO documentation target: <https://edithatogo.github.io/UOGTO/>
- [ ] Zenodo DOI: `TBD after v1.0.0 release archiving`

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

## Registry Gate
- [x] GitHub release `v1.0.0` is published.
- [ ] Zenodo DOI is minted and recorded.
- [x] WIDOCO Pages documentation is live.
- [x] LOV submission document is complete.
- [x] OLS indexing document is complete.
