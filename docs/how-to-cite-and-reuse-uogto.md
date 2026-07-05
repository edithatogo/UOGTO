# How to Cite and Reuse UOGTO

UOGTO is the Universal Open Game Theory Ontology. Use the citation below when referring to the ontology in papers, datasets, software, or downstream ontology work.

## Preferred Citation

> Dylan A Mordaunt ([ORCID 0000-0002-9775-0603](https://orcid.org/0000-0002-9775-0603)). *Universal Open Game Theory Ontology: A semantic resource for strategic-interaction evidence*. Version 1.0.0. Zenodo. DOI: [10.5281/zenodo.20796937](https://doi.org/10.5281/zenodo.20796937).

If you need a machine-readable citation record, use [CITATION.cff](../CITATION.cff).

## Canonical Identifiers

- DOI: [10.5281/zenodo.20796937](https://doi.org/10.5281/zenodo.20796937)
- Author ORCID: [0000-0002-9775-0603](https://orcid.org/0000-0002-9775-0603)
- Repository: <https://github.com/edithatogo/UOGTO>
- Public documentation: <https://edithatogo.github.io/UOGTO/>
- Canonical core namespace: `https://w3id.org/uogto/core#`
- Canonical extension namespace: `https://w3id.org/uogto/extensions#`

## Preferred Prefixes

Use these prefixes in Turtle, SPARQL, SHACL, and JSON-LD where the local vocabulary is UOGTO:

```turtle
@prefix uogto:  <https://w3id.org/uogto/core#> .
@prefix uogtox: <https://w3id.org/uogto/extensions#> .
```

For examples that also reference provenance and semantic annotations, these standard prefixes are commonly used alongside UOGTO:

```turtle
@prefix prov:   <http://www.w3.org/ns/prov#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
```

## Release Assets

The release package is distributed through the GitHub release and mirrored in the generated `dist/` assets. The main release artifacts are:

- `uogto.ttl`
- `uogto-shapes.ttl`
- `context.jsonld`
- `core.context.jsonld`
- `extensions.context.jsonld`
- `release-assets-manifest.json`
- `SHA256SUMS`

Supporting release and publication assets are documented in [docs/releases/v1.0.md](releases/v1.0.md) and include:

- `registry-handoff.json`
- `extended-registry-handoff.json`
- `zenodo-handoff.json`
- `w3id-redirect-handoff.json`
- `publication-status.json`

## Licence

UOGTO is dual-licensed:

- Ontology and documentation: [CC-BY-4.0](../LICENSE)
- Code and tooling: [MIT](../LICENSE-CODE)

If you redistribute or adapt the ontology content, preserve attribution and licence notices for the relevant components.

## How to Reuse

### In Turtle

```turtle
@prefix uogto: <https://w3id.org/uogto/core#> .

<https://example.org/game/prisoners-dilemma>
    a uogto:GameSpecification ;
    uogto:hasGameName "Prisoner's Dilemma" .
```

### In JSON-LD

```json
{
  "@context": {
    "uogto": "https://w3id.org/uogto/core#",
    "uogtox": "https://w3id.org/uogto/extensions#"
  },
  "@id": "https://example.org/game/prisoners-dilemma",
  "@type": "uogto:GameSpecification",
  "uogto:hasGameName": "Prisoner's Dilemma"
}
```

### In a manuscript or software citation

Use the DOI and version together when you need a stable reference to the release:

```text
Dylan A Mordaunt (2026). Universal Open Game Theory Ontology: A semantic resource for strategic-interaction evidence, version 1.0.0. Zenodo. https://doi.org/10.5281/zenodo.20796937
```

## Reuse Notes

- Prefer the canonical namespaces and prefixes above when creating new mappings or examples.
- If you build derived alignments or examples, cite both UOGTO and the external source vocabularies you use.
- If you package a dataset or publication that embeds UOGTO content, keep the DOI, release version, and licence visible in the metadata.
- For release-specific reproduction, link to [docs/releases/v1.0.md](releases/v1.0.md) and the relevant `dist/` release assets.
