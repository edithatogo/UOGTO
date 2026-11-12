# Product Definition: UOGTO

## Concept
Universal Open Game Theory Ontology (UOGTO) is a modular semantic layer for game
specifications, players, information, strategies, outcomes, solutions and execution
provenance. It separates a specification from its instances, sessions and traces.
Universality is a research objective, not an established coverage result.

## Automation & Maintenance
The repository provides builds, RDF/SHACL validation, competency queries, regression
tests, packaging and GitHub Actions. Current required checks remain in force.
Conductor records implementation and evidence separately from future research.

## Systematic Review Protocols
Review protocols and dated acquisition/mapping records support coverage research.
Having a protocol does not establish compliance, completed acquisition or exhaustive
coverage. The [November audit](../docs/research/game-semantics-source-audit-20261108.md)
records missing predecessors, source distinctions and retrieval limits.

## Reference tooling and computation boundary

`uogto-runner` inspects graphs and looks up stored payoffs. The first-action baseline
is deterministic; legacy LLM class names are compatibility aliases, not evidence of
model calls. The Streamlit playground visualises graphs and validation results.

[Paignia](https://github.com/edithatogo/paignia) owns reusable Rust game computation
and adapters. UOGTO owns language-neutral semantics, source lineage, profiles and
reference fixtures. Kairos is an optional execution provider. Actual Rust and
external-library compatibility requires versioned receipts and executed tests.

## Development priorities

1. Correct reproduced defects and keep current evidence reproducible.
2. Comprehensively source, attribute and compare identifiable strategic ontologies,
   formal languages, library concepts and related modelling/research approaches.
3. Qualify a finite executable profile through the existing semantic-contract track.
4. Mature release and compatibility practices; measure adapters on independent cases.
5. Test the [frontier programme](../docs/roadmap/frontier-programme-20261108.md)
   against explicit baselines before making novelty claims.

The [next resource-paper plan](../docs/paper/next-version-plan-20261108.md) integrates
corrected claims, comprehensive sourcing receipts and reproducible evidence; later
interoperability and frontier publications require their own experimental results.
