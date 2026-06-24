# UOGTO Ontology Design Patterns

This document explains the main modelling patterns used by UOGTO. It is a structural guide, not a new ontology module.

## 1. Game Pattern

Use `uogto:GameSpecification` for the formal game model and `uogto:GameInstance` for a concrete realization.

- `uogto:GameSpecification` carries the rules, participants, actions, and payoff structure.
- `uogto:GameInstance` binds that specification to a concrete run, parameterisation, or scenario.
- `uogto:GameEntity` is the shared superclass for reusable game-theoretic constructs.

This separation keeps the schema, the instantiated game, and the observed play trace distinct.

## 2. Session Pattern

Use `uogto:PlaySession` for an execution episode.

- `uogto:PlaySession` records a single run, simulation, or playthrough.
- `uogto:emitsEventTrace` links the session to recorded events.
- Session-level metadata belongs on the session node, not on the game specification.

This pattern keeps repeated executions comparable and prevents trace data from being mixed into the static game model.

## 3. Trace Pattern

Use `uogto:EventTrace` for a time-ordered log of observed play.

- `uogto:EventTrace` captures state transitions, actions, and outcome-relevant events.
- `uogto:timestamp` is for real-world time when needed.
- `uogto:timeIndex` is for discrete steps in a simulation or sequential model.

Traces are the evidence surface for reproducible execution claims, diagnostic review, and provenance.

## 4. Strategy and Action Pattern

Use `uogto:Strategy` for a complete plan and `uogto:Action` for a single move.

- `uogto:Strategy` is the full behavioural plan a player can commit to.
- `uogto:Action` is the local choice made at a decision point.
- `uogto:StrategyProfile` bundles the strategies chosen by the participating players.
- `uogto:ActionProfile` bundles simultaneous or joint actions.

This distinction is important for normal-form, extensive-form, stochastic, MARL, and mechanism-design cases.

## 5. Payoff and Outcome Pattern

Use `uogto:Outcome` for the result of interaction and `uogto:Payoff` for the utility or reward assigned.

- `uogto:Outcome` captures what happened.
- `uogto:Payoff` captures how it is valued.
- `uogto:PayoffProfile` groups player-specific payoffs.
- `uogto:PlayerPayoffLink` reifies the player-to-payoff relation when the model needs per-player detail.

This keeps outcome semantics separate from valuation semantics.

## 6. Mechanism Pattern

Use the mechanism-design extension for allocation and incentive structure, while keeping the core ontology focused on the game layer.

- `ontologies/extensions/mechanism-design.ttl` models the mechanism-design extension.
- Mechanism-related terms should capture allocation rules, incentive constraints, and rule-driven interaction.
- Mechanism semantics should remain separable from the generic game specification unless the concept is required by the article or example.

The pattern supports article claims about auctions, matching, and incentive compatibility without overloading the core ontology.

## 7. Execution Binding Pattern

Use the execution-binding extension when the ontology needs to point to runnable artifacts or agent/tool integration.

- `ontologies/extensions/kg-execution-bindings.ttl` models execution bindings.
- `uogto:ExecutionModel` captures the compiled or executable representation of a game.
- Execution bindings should link the model to code, runtime artefacts, logs, or agent interfaces.

This pattern bridges the declarative ontology and runnable implementations.

## 8. Mapping Pattern

Use separate modules and alignments for adjacent concepts that should not be folded into core UOGTO.

- Keep domain-specific semantics in the relevant extension module.
- Use SHACL for closed-world constraints on example data.
- Use alignment documents for external ontologies and standards when the concept is adjacent but not core.

This avoids duplicating adjacent modelling vocabularies inside the core ontology.

## 9. Recommended Reading Order

1. `docs/ontology-design-principles.md`
2. `ontologies/core/uogto-core.ttl`
3. `ontologies/extensions/mechanism-design.ttl`
4. `ontologies/extensions/kg-execution-bindings.ttl`
5. `docs/examples.md`
6. `docs/competency-questions.md`

