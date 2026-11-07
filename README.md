# Universal Open Game Theory Ontology (UOGTO)

## Overview
UOGTO (Universal Open Game Theory Ontology) defines modular game-theoretic semantics
for classical, cooperative, multi-agent, mechanism-design and simulation-related
models. It supplies OWL vocabularies, SHACL constraints, examples and competency
queries. Its broad scope is an aim; exhaustive coverage of earlier ontologies and
general executable compatibility have not been established.

## Current capabilities and programme

- Static/dynamic strategic structure is explicit and independent of normal/extensive
  representation and software scheduling. See the
  [semantic reconciliation and migration notes](docs/semantic-reconciliation-20261108.md).
- Python `RDFGameRunner` is reference graph inspection and stored-payoff lookup.
  `FirstActionPlayer` is a deterministic baseline; the legacy `LLMPlayer` alias
  does not invoke a language model. Outputs identify their execution origin.
- [Paignia](https://github.com/edithatogo/paignia) owns the intended Rust computation
  and adapter layer. The versioned executable subset and cross-language conformance
  work remain tracked by [semantic game contracts](conductor/tracks/semantic_game_contracts_20261107/index.md).
- The [November source audit](docs/research/game-semantics-source-audit-20261108.md)
  identifies missing and incompletely examined predecessors and library concepts.
  Current OpenSpiel/PettingZoo fixtures provide local semantic checks; actual
  external adapters remain future work.
- The [maturity and frontier programme](docs/roadmap/frontier-programme-20261108.md)
  links scoped implementation work, library comparisons and research hypotheses
  to the [Conductor registry](conductor/tracks.md).
- [Current quality evidence](docs/quality/current-semantic-quality.md) is separate
  from dated article snapshots. Example conformance does not establish full
  ontology coverage, solver correctness or scientific frontier status.

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
- Reference interoperability fixtures and target inventory are tracked in [docs/interoperability-benchmarks.md](docs/interoperability-benchmarks.md).
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
- Sole-developer merge and validation policy is documented in [docs/governance/sole-developer-harness.md](docs/governance/sole-developer-harness.md).

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
