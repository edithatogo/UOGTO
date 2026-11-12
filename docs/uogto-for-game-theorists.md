# UOGTO for Game Theorists

Use UOGTO when you want a formal, machine-readable model of strategic interaction that still stays close to standard game-theoretic language.

## What UOGTO captures well

- Game specifications and concrete game instances
- Players, strategies, actions, outcomes, and payoffs
- Normal-form, extensive-form, stochastic, epistemic, and mechanism-design settings
- Equilibrium-oriented reasoning and comparison across variants

## Best-fit modules

- `ontologies/core/games.ttl`
- `ontologies/core/strategies.ttl`
- `ontologies/core/actions.ttl`
- `ontologies/core/outcomes.ttl`
- `ontologies/core/payoffs.ttl`
- `ontologies/core/equilibria.ttl`
- `ontologies/extensions/mechanism-design.ttl`
- `ontologies/extensions/auctions.ttl`
- `ontologies/extensions/bargaining.ttl`
- `ontologies/extensions/computational-social-choice.ttl`

## Recommended reuse pattern

Model the formal game in the core ontology, then add an extension module when the article or dataset requires auctions, bargaining, voting, or incentive constraints. Keep examples minimal and use SHACL shapes to enforce the specific assumptions of your case.

Use `StaticGame`/`DynamicGame` for strategic timing and `hasRepresentation` for
normal/extensive form. A normal-form representation may encode a dynamic game's
contingent strategies. See [modelling decisions](modelling-decisions.md).

## Computation and evidence

The Python runner provides reference graph inspection and stored-payoff lookup.
`FirstActionPlayer` selects a deterministic baseline action; legacy `LLMPlayer`
names do not invoke a model. Output identifies this reference origin and makes
no native Rust or equilibrium-solving claim.

[Paignia](https://github.com/edithatogo/paignia) is the intended computation provider.
Gambit/OpenSpiel adapters and a qualified executable subset remain planned work.
An asserted fixture can demonstrate vocabulary use without proving equivalence
of games or execution by an external engine. The
[source audit](research/game-semantics-source-audit-20261108.md) records the
remaining concept-level gaps.

## Good reference points

- [Ontology design patterns](ontology-design-patterns.md)
- [Examples](examples.md)
- [Competency questions](competency-questions.md)
