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

## Licensing
This project is dual-licensed:
- **Ontology and Documentation**: Creative Commons Attribution 4.0 International (CC-BY-4.0). See [LICENSE](LICENSE).
- **Code and Tooling**: MIT License. See [LICENSE-CODE](LICENSE-CODE).
