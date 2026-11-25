# Executable discounted Markov profile v1

UOGTO admits an asserted RDF model of a finite, fully observed, two-player
zero-sum Markov game with an infinite discounted horizon. Both players observe
the current state and choose simultaneously from fixed action sets. Each stage
earns the first seat's reward at the current state and joint decision, before
drawing the next state. The second seat receives its negation. The stationary
profile specifies independent action distributions for the two players at each
state.

The profile IRI is `urn:uogto:profile:discounted-markov:1.0.0`. A named
`GameSpecification` is explicitly typed as a `DynamicGame` and `MarkovGame`
and links one `DiscountedZeroSumMarkovRepresentation`. The representation
declares that profile using `dcterms:conformsTo`. The game specification links
the named `TransitionFunction`. All game and binding identities are absolute
IRIs. RDF list cells supply axis order.

## Projection contract

Pass one asserted RDFLib graph and the specification's `URIRef` to
`uogto.interchange.discounted_markov.project_game(graph, specification)`.
The packaged [SHACL shape](../../uogto/interchange/discounted-markov-profile-v1.ttl)
checks types, cardinalities and local values. The projector checks axis and
binding coverage in the selected graph and returns the Paignia `discounted`
game payload.

| Payload field | RDF source |
| --- | --- |
| `players` | Representation's `uogtox:playerOrder` equals the two `uogto:hasPlayer` members. Each player's `uogtox:actionOrder` lists named simultaneous actions linked to the player by `uogto:belongsToPlayer`. |
| `states` | Representation's `uogtox:stateOrder` equals the `uogto:hasState` inventory. Each player declares the full state set using `uogto:observes`. Each state declares every action using `uogto:hasAvailableAction`. |
| `states[].outcomes[i][j]` | The kernel links a `uogtox:hasStageDecision` binding for every state and joint action. `uogtox:atState` identifies the current state. `uogto:hasActionProfile` links the two choices. The first seat's action selects row `i`, and the second seat's action selects column `j`. |
| `reward` and `transition` | The stage decision carries `uogtox:stageReward` and one `uogto:hasTransition` entry per destination. Each entry gives `uogto:transitionsFrom`, `uogto:transitionsTo` and `uogto:probability`. The output vector follows the state axis. |
| `initial` | Representation's `uogtox:hasInitialWeight` entries bind each `uogtox:atState` to a `uogto:probability`. The output vector follows the state axis. |
| `discount` | Representation's `uogtox:modelDiscountFactor` gives the per-stage discount in `[0, 1)`. |
| `method.policy` | The `JointPolicy` linked by `uogtox:hasStationaryProfile` has one `uogtox:hasPolicyRow` per state and player. Each row gives `uogtox:atState`, `uogto:belongsToPlayer` and `uogtox:hasActionWeight` entries labelled by `uogto:hasAction`. The output axes are state, player, action. |

The projector requires explicit entries for zero weights. It rejects missing,
duplicate and foreign bindings, including two stage decision IRIs that
resolve to the same state and pair of actions. It uses the lists and labels
to build arrays and preserves full IRIs verbatim. RDF reward, discount and
probability literals use finite `xsd:double` values. The model discount uses
the new representation predicate. The existing `uogtox:discountFactor`
describes a learning process.

Each initial, transition and policy row must have weights in `[0, 1]` and
absolute mass error at most the exact value of binary64 `1e-12`. The
projector compares the exact sum of the parsed binary64 values to one,
independent of summation order. It returns the parsed weights unchanged.
Paignia owns native admission and normalization by the admitted mass.
The projector selects `method.kind = "evaluate"` with `max_iterations = 300`
and `value_tolerance = 1e-10` as caller-overridable payload defaults.

## Frozen recurring-funding replay

The [synthetic Turtle fixture](../../examples/recurring-funding-discounted-markov-v1.ttl)
uses dimensionless invented rewards. Its SHA-256 is
`2502af2adff68ff9b41e11c68f28ba93a9c452baa0b0f74831fec5ac768f8552`.
The specification and representation IRIs are exposed as
`FROZEN_SPECIFICATION_IRI` and `FROZEN_REPRESENTATION_IRI`, respectively.

```python
import json

from rdflib import Graph
from uogto.interchange.discounted_markov import FROZEN_SPECIFICATION_IRI, project_game

graph = Graph().parse("examples/recurring-funding-discounted-markov-v1.ttl", format="turtle")
print(json.dumps(project_game(graph, FROZEN_SPECIFICATION_IRI), allow_nan=False))
```

The state axis is stable, pressure. The action axes are settle, defer for the
commissioner and accept, contend for the provider. The initial weights are
`[0.75, 0.25]` and the discount is `0.75`. With both players choosing their
first action in every state, the exact Bellman reference is
`[32/13, -16/13]` with initial value `20/13` for the commissioner.

The [competency query](../../competency-questions/cq26-discounted-markov-stage-transitions.rq)
retrieves the 16 labelled transition entries. The
[projection tests](../../tests/test_discounted_markov.py) verify the full
payload and exact Bellman reference, axis order, invalid graphs and both
sides of the binary64 mass boundary. Verification is local to UOGTO. Paignia
owns native solver and replay qualification.
