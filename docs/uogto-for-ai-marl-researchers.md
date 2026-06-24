# UOGTO for AI and MARL Researchers

Use UOGTO when the interaction model includes agents, policies, tool use, execution traces, or learning dynamics that need to be described in a game-theoretic form.

## What UOGTO captures well

- Multi-agent interaction and policy selection
- MARL-style episodes, trajectories, and outcomes
- LLM-agent and tool-use games
- Execution bindings that connect models to runtime artefacts
- Safety, privacy, and provenance concerns that arise in agentic systems

## Best-fit modules

- `ontologies/extensions/marl.ttl`
- `ontologies/extensions/llm-agent-games.ttl`
- `ontologies/extensions/learning-in-games.ttl`
- `ontologies/extensions/algorithmic-game-theory.ttl`
- `ontologies/extensions/privacy-disclosure.ttl`
- `ontologies/extensions/trust-reputation-provenance.ttl`
- `ontologies/extensions/kg-execution-bindings.ttl`
- `examples/llm-tool-use-game.jsonld`
- `examples/marl-gridworld-game.jsonld`

## Recommended reuse pattern

Model the policy or agent interaction at the level of games, sessions, actions, and traces. Use the execution-binding extension when you need to preserve tool calls, runtime logs, or provenance for auditing and reproduction.

## Good reference points

- [Ontology design patterns](ontology-design-patterns.md)
- [Examples](examples.md)
- [Competency questions](competency-questions.md)