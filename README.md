# Universal Open Game Theory Ontology (UOGTO)

## Overview
UOGTO (Universal Open Game Theory Ontology) is a modular, version-controlled repository defining game-theoretic semantics, including classical, cooperative, multi-agent, simulation execution, mechanism design, and executable knowledge graph semantics.

## Repository Layout
- `ontologies/`: Main OWL/TTL schema definitions.
- `shapes/`: SHACL constraint validation graphs.
- `jsonld/`: JSON-LD context documents.
- `examples/`: Domain usage examples.
- `competency-questions/`: SPARQL verification queries.
- `scripts/`: Tooling for build, validation, and coverage.
- `docs/`: Guides, mappings, and references.

## Quickstart
1. Install dependencies:
   ```bash
   pip install -e .
   ```
2. Build merged files:
   ```bash
   make build
   ```
3. Run validation and tests:
   ```bash
   make all
   ```

## Documentation and Citation
- Human-readable ontology documentation is generated with WIDOCO and published through GitHub Pages at <https://edithatogo.github.io/UOGTO/>.
- Release and DOI workflow notes are maintained in [docs/releases/v1.0.md](docs/releases/v1.0.md).
- Citation metadata is provided in [CITATION.cff](CITATION.cff).
- Zenodo archive metadata is provided in [.zenodo.json](.zenodo.json).
- Registry preparation materials for LOV and OLS are under [docs/registry/](docs/registry/).

## Licensing
This project is dual-licensed:
- **Ontology and Documentation**: Creative Commons Attribution 4.0 International (CC-BY-4.0). See [LICENSE](LICENSE).
- **Code and Tooling**: MIT License. See [LICENSE-CODE](LICENSE-CODE).
