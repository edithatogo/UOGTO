# Linked Open Vocabularies Submission

## Status
Submitted on 2026-06-22 through the active LOV GitHub issue route after `v1.0.0`, WIDOCO documentation, release assets, and the Zenodo DOI were public. Live follow-up on 2026-07-06 confirmed issue `83` remains open with no maintainer comments; public LOV `uogto` vocabulary API/page routes still return 404. A cross-registry metadata supplement was posted on 2026-07-07 after later OLS and Bioregistry feedback clarified biomedical/health relevance, ORCID, and namespace handling.

Submission route checked 2026-06-22: Linked Open Vocabularies frontend repository `pyvandenbussche/lov` is active at <https://github.com/pyvandenbussche/lov>. The current LOV site root is <https://lov.linkeddata.es/>; the historical `/dataset/lov/` URL redirects to a 404. No repository issue template was exposed through the GitHub contents API, so the final submission route should be confirmed at submission time.

## Submission Metadata
- Ontology title: Universal Open Game Theory Ontology (UOGTO)
- Preferred prefix: `uogto`
- Core namespace: `https://w3id.org/uogto/core#`
- Extension namespace: `https://w3id.org/uogto/extensions#`
- Homepage: <https://github.com/edithatogo/UOGTO>
- Documentation: <https://edithatogo.github.io/UOGTO/>
- GitHub repository: <https://github.com/edithatogo/UOGTO>
- Release URL: <https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0>
- DOI: <https://doi.org/10.5281/zenodo.20796937>
- License: <https://creativecommons.org/licenses/by/4.0/>
- Maintainer route: GitHub issues on `edithatogo/UOGTO`

## Cross-Registry Supplement

Supplement URL: <https://github.com/pyvandenbussche/lov/issues/83#issuecomment-4902620021>

The supplement keeps the requested LOV prefix unchanged as `uogto`, confirms `https://w3id.org/uogto/core#` as the primary core namespace, keeps `https://w3id.org/uogto/extensions#` documented separately as `uogtox`, records the approved sole-author/contact ORCID <https://orcid.org/0000-0002-9775-0603>, and mirrors the biomedical/health relevance clarification accepted by OLS.

## Abstract
UOGTO is a modular OWL/SHACL ontology for game-theoretic semantics, including classical games, cooperative games, games of incomplete information, mechanism design, multi-agent reinforcement learning, network and continuous games, norms and contract theory, LLM/digital twin games, and executable knowledge graph bindings.

## Canonical RDF Downloads
- Merged ontology release asset: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl>
- SHACL shapes release asset: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto-shapes.ttl>
- Release checksums: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/SHA256SUMS>
- Registry handoff packet: <https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/registry-handoff.json>
- Source modules: `ontologies/core/`, `ontologies/extensions/`, and `ontologies/alignments/`.

## LOV Checklist
- [x] Confirm all metadata requirements in `docs/registry/metadata-checklist.md`.
- [x] Confirm the WIDOCO documentation URL is reachable.
- [x] Confirm the Zenodo DOI resolves.
- [x] Submit the vocabulary through the current LOV submission route.
- [x] Record submission date.
- [x] Record submission URL or issue URL.
- [x] Post cross-registry metadata supplement after OLS/Bioregistry feedback.
- [ ] Track LOV review feedback.
- [ ] Convert requested changes into Conductor follow-up tasks.

## Submission Record
- Submission date: `2026-06-22`
- Submission URL: <https://github.com/pyvandenbussche/lov/issues/83>
- Metadata supplement: <https://github.com/pyvandenbussche/lov/issues/83#issuecomment-4902620021>
- Review status: `Submitted; metadata supplement posted; awaiting LOV maintainer review; no maintainer feedback as of 2026-07-07`
- Acceptance status: `TBD`
