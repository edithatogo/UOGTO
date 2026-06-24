# UOGTO for Simulation Researchers

Use UOGTO when the key need is to describe repeated runs, event traces, scenario parameters, and executable bindings rather than only the static game object.

## What UOGTO captures well

- Sessions, traces, events, and outcomes
- Simulation runs and repeated experiments
- Agent-based modelling and discrete-event execution patterns
- System-dynamics style feedback loops when they are expressed as executable or traced interactions
- Provenance for results and derived artefacts

## Best-fit modules

- `ontologies/core/dynamics.ttl`
- `ontologies/extensions/kg-execution-bindings.ttl`
- `ontologies/extensions/petri-net-devs-hla.ttl`
- `ontologies/extensions/differential-hybrid-games.ttl`
- `ontologies/extensions/causal-games.ttl`
- `ontologies/extensions/digital-twin-games.ttl`
- `ontologies/extensions/verification-games.ttl`

## Recommended reuse pattern

Treat the model as a simulation specification plus one or more session-level traces. Put parameters and execution metadata on the instance or session, not on the abstract game specification. Use trace data for reproducibility claims, network analysis, and scenario comparison.

## Good reference points

- [Ontology design patterns](ontology-design-patterns.md)
- [Examples](examples.md)
- [Release process](release-process.md)