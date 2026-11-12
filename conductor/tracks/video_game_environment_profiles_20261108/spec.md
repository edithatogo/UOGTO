# Specification — video-game environments and strategic scenario profiles

## Purpose
A video-game title or virtual world is not a complete strategic specification.
Represent an explicitly bounded scenario: actors, observations/information, legal
actions, transitions, horizon, incentives and outcome interpretation. Different
scenarios within the same title can define different games.

Single-agent driving against fixed scripted dynamics is normally a control/MDP
problem. Strategically adaptive drivers, competitive teams, bargaining, coalition
formation or in-game markets may define genuine strategic interactions. A visual
world does not by itself supply player utility functions or equilibrium assumptions.

Use existing GameSpecification/Instance/PlaySession/EventTrace and related terms
first. Map an environment/API separately from a strategic abstraction and its source
of empirical evidence. Keep videogame mechanics and asset metadata in external
vocabularies or applied profiles where suitable. A dynamic game need not be simulated
in real time, and a turn-based representation need not mean sequential information.

## Scope and acceptance
Start with an openly accessible small environment; Grand Theft Auto/DeepGTAV is a
research example and optional later adapter, not a mandatory test dependency. Separate
plugin-code licences from game assets and platform terms. Do not redistribute
proprietary assets or infer data access merely from an open-source plugin.

Acceptance requires a reproducible scenario, explicit abstraction/loss limits,
legally available test artefacts, measured observation/action fidelity and a result
whose meaning is declared. UOGTO does not become a graphics, physics or gameplay engine.
