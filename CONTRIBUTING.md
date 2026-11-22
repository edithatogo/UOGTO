# Contributing to UOGTO

UOGTO welcomes issues and pull requests that improve the ontology, examples,
validation shapes, documentation, release artifacts, or manuscript evidence.

## Before Opening an Issue

Use the most specific issue template available:

- **Ontology change proposal** for new classes, properties, alignments, modules,
  deprecations, or vocabulary changes.
- **Validation failure** when RDF parsing, SHACL validation, competency queries,
  or CI checks fail.
- **Documentation fix** for unclear docs, examples, glossary entries, release
  notes, or manuscript-supporting artifacts.
- **Bug report** for scripts, workflows, generated assets, or packaging behavior.
- **Question** for modelling questions that may be better discussed before a PR.

## Ontology Change Contract

Ontology-facing pull requests must keep the model, constraints, examples, and
documentation aligned.

- Add `rdfs:label` and `skos:definition` to every new class and property.
- Keep class names in UpperCamelCase and property names in lowerCamelCase.
- Keep object properties and datatype properties separate.
- Prefer open OWL domains/ranges where reuse matters, and enforce closed-world
  requirements through SHACL shapes.
- Update SHACL shapes for any invariant that examples or downstream users should
  be able to validate.
- Add or update examples showing the intended modelling pattern.
- Add or update competency queries when the change affects retrieval behavior.
- Update docs, glossary entries, and modelling-decision notes when the change
  affects public interpretation.
- Record release, registry, manuscript, and RI-HERO impacts when relevant.

## Games Added by Downstream Projects

Use the [downstream-game intake contract](docs/contracts/downstream-game-intake.md)
for every new or changed game. Record its source revision, full-IRI mapping and
semantic disposition in UOGTO. Existing vocabulary can be reused through an
updated example, mapping or competency case; add ontology terms only where the
case demonstrates a gap. Link the same intake key to Paignia's reusable
implementation and the originating application. Paignia owns shared game rules
and solvers; relevant upstream providers retain their own capabilities, and the
application retains its domain assumptions and data. Keep semantic, numerical
and consumer-execution evidence distinct under the existing SGC track.
The canonical contract names the six current downstream applications. Innovate
remains a parallel innovation library with gradual, parity-qualified generic
game migration; Voiage owns VoP/VoH and their demo. Kairos, Voiage and Dapane
compose as optional providers through explicit contracts without dependency cycles.

## Pull Request Workflow

1. Fork the repo and create a feature branch from `main`.
2. Keep changes scoped to one issue or modelling decision.
3. Run the relevant local gates:

   ```bash
   make validate
   make test
   ```

4. For publishing or registry changes, also run:

   ```bash
   make publishing-metadata
   make registry-links
   ```

5. For manuscript or arXiv-package changes, run:

   ```bash
   make manuscript-pdf
   make arxiv-upload-ready
   ```

6. Open a pull request and complete the checklist in the PR template.

## Licensing

UOGTO is dual licensed:

- ontology and documentation: CC-BY-4.0;
- code and tooling: MIT.

By contributing, you agree that your contribution can be distributed under the
license that applies to the files you change.
