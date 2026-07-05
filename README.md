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
- Ontology design-pattern documentation is available at [docs/ontology-design-patterns.md](docs/ontology-design-patterns.md).
- Ontology modelling decisions are explained in [docs/modelling-decisions.md](docs/modelling-decisions.md).
- Executable interoperability benchmark fixtures and target inventory are tracked in [docs/interoperability-benchmarks.md](docs/interoperability-benchmarks.md).
- Glossary terms are collected in [docs/glossary.md](docs/glossary.md).
- Audience-specific guidance is available at [docs/uogto-for.md](docs/uogto-for.md).
- Citation and reuse guidance is available at [docs/how-to-cite-and-reuse-uogto.md](docs/how-to-cite-and-reuse-uogto.md).
- Release and DOI workflow notes are maintained in [docs/releases/v1.0.md](docs/releases/v1.0.md).
- Citation metadata is provided in [CITATION.cff](CITATION.cff).
- Zenodo archive metadata is provided in [.zenodo.json](.zenodo.json).
- Documentation index is available at [docs/index.md](docs/index.md).
- Registry preparation materials for LOV and OLS are under [docs/registry/](docs/registry/).
- Comparative ontology mapping outputs, figures, and report are under [docs/ontology-comparison/](docs/ontology-comparison/), with the main report at [docs/ontology-comparison/report.md](docs/ontology-comparison/report.md).
- Article-hardening protocol, evidence package, source-acquisition manifest, tables, figures, and review logs are under [docs/article-hardening/](docs/article-hardening/).

## RI-HERO
The repo is also tracked inside the RI-HERO meta-program, which treats UOGTO as part of a broader health economics research on outcomes framing.

- RI-HERO project: `RI-HERO Meta-Program`
- RI-HERO project board: [RI-HERO Meta-Program](https://github.com/users/edithatogo/projects/9)
- Intake form: `.github/ISSUE_TEMPLATE/ri-hero-meta-program.yml`
- Publication intake form: `.github/ISSUE_TEMPLATE/ri-hero-publication-registry.yml`
- Implementation intake form: `.github/ISSUE_TEMPLATE/ri-hero-implementation-validation.yml`
- Program structure: synthesis, implementation, publication/registry, monitoring
- Synthesis epics: program governance, operating model, and outcomes evidence mapping
- RI-HERO status page: [docs/ri-hero-status.md](docs/ri-hero-status.md)
- Discussions:
  - [Welcome to UOGTO Discussions](https://github.com/edithatogo/UOGTO/discussions/17)
  - [RI-HERO Meta-Program](https://github.com/edithatogo/UOGTO/discussions/18)

## Licensing
This project is dual-licensed:
- **Ontology and Documentation**: Creative Commons Attribution 4.0 International (CC-BY-4.0). See [LICENSE](LICENSE).
- **Code and Tooling**: MIT License. See [LICENSE-CODE](LICENSE-CODE).
