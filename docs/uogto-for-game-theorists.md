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

## Good reference points

- [Ontology design patterns](ontology-design-patterns.md)
- [Examples](examples.md)
- [Competency questions](competency-questions.md)