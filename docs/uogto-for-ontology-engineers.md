# UOGTO for Ontology Engineers

Use UOGTO when you need a modular ontology that is versioned, validated, documented, and easy to align with adjacent vocabularies.

## What UOGTO captures well

- Clean separation between core and extension modules
- Annotated classes and properties with labels and definitions
- SHACL validation for example data and constrained use cases
- External alignments and reusable namespace conventions
- Release assets and publication metadata for downstream reuse

## Best-fit modules and surfaces

- `ontologies/core/uogto-core.ttl`
- `ontologies/core/uogto-governance.ttl`
- `shapes/`
- `jsonld/`
- `ontologies/alignments/`
- `docs/ontology-comparison/`
- `docs/how-to-cite-and-reuse-uogto.md`

## Recommended reuse pattern

Keep ontology content modular, keep validation in SHACL, and keep external mappings in alignment files rather than folding them into the core model. For publication and reuse, rely on the release package, citation metadata, and namespace guidance already recorded in the repo.

## Good reference points

- [Ontology design principles](ontology-design-principles.md)
- [Module map](module-map.md)
- [How to cite and reuse UOGTO](how-to-cite-and-reuse-uogto.md)