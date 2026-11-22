# Downstream game intake and ontology evolution

UOGTO is the semantic authority for games used by Paignia and downstream
applications. Every new downstream game, and every change to its actors,
actions, information, timing, payoff meaning or solution concept, must feed
back into this repository. Reusing existing vocabulary still requires a
recorded mapping and example or evidence update; a new application does not
automatically require a new ontology class.

Paignia owns the reusable Rust representations, game families, rules, solution
methods and diagnostics. Its [implementation intake](https://github.com/edithatogo/paignia/blob/main/docs/integrations/downstream-game-intake.md)
uses the same intake keys below and links back here for semantic dispositions.
Applications retain institution-specific assumptions, empirical data and payoff
construction. Relevant upstream repositories provide their own capabilities
through explicit contracts rather than copied parallel implementations.

## Development workflow

1. **Describe the game and inspect existing support.** Record the originating
   repository, source path and immutable revision; players, legal actions,
   information/observations, strategic timing, payoff units and interpretation,
   solution concept and supported input bounds. Search UOGTO's current terms
   and profiles and Paignia's public contracts before adding vocabulary or code.
2. **Record the semantic disposition here.** Reuse an intake key, or add a stable
   key when the concern is distinct. Use `reuse_existing`, `extension_required`, `unsupported` or
   `mapping_review_pending`, with source evidence and rationale. For reuse, add
   or refine the mapping, example, competency case or documentation in UOGTO.
   For a demonstrated gap, update the smallest suitable ontology module,
   definitions, SHACL constraints, JSON-LD context and example/query coverage.
   Pending concepts remain explicit; applications must not invent canonical
   UOGTO IRIs or treat similar labels as equivalent terms.
3. **Return reusable implementation to Paignia.** Link the same key and UOGTO
   change from the provider intake. New reusable games/mechanics and shared
   algorithms belong in Paignia; the application consumes the supported
   provider contract. Assess relevant existing upstream capabilities before
   writing a substitute. Preserve source revision, licence and attribution for
   any transferred fixture or code.
4. **Bind the actual versions and tests.** A mapping identifies the UOGTO
   revision, full term IRIs, profile/version, source/example paths and fixture
   hashes; its provider link identifies the Paignia revision/packages and
   supported method. Preserve game specification, instance, session and trace
   identities, player/payoff associations and declared ordering. Record explicit
   unsupported cases. Reuse SGC's existing conformance work and acceptance
   receipts rather than creating another receipt system.
5. **Integrate the linked changes.** UOGTO receives the semantic/example update,
   Paignia receives reusable implementation and its independent numerical
   checks, and the application updates its dependency and runs its own bounded
   case. A working application alone does not complete upstream integration.
   Existing code review and CI handle the coherent change; this workflow adds
   no separate human approval loop.

The feedback requirement applies during development, not on every library call.
It does not impose a simulator, ontology reasoner or network service on static
game solving. Existing supported profiles continue to be usable while an
unrelated proposed game or optional dynamic adapter is pending.

## Semantic intake register

This is the canonical semantic intake ledger. Paignia records implementation
and transfer status separately using these same keys. Keys identify reusable
families or cross-cutting concerns; they are not new ontology IRIs, exhaustive
classifications or executable-support declarations.

Initial review baseline: UOGTO `0050e19faec2abaa05e5d474e5eed0150bcbf073`,
22 November 2026. Existing term matches below are starting points. A pending
row does not assert that all requested rules are already represented or solved.

| Intake key | Request or downstream use | Existing semantic starting point | Disposition and next semantic evidence |
| --- | --- | --- | --- |
| `finite-perfect-information` | Reusable finite decision/chance games, including reimbursement and valuation consumers. | [Finite declaration profile](executable-game-subset-v1.md); `GameSpecification` and `ExtensiveFormRepresentation`. | **reuse_existing**, bounded by the existing profile at Paignia `bd880dd756d2ba56cc5f479bc078cea31b53c1d1`. Add each consumer's full-IRI mapping and distinguishing example; general round-trip and consumer acceptance remain SGC-owned and pending. |
| `finite-perfect-recall` | Finite extensive games with declared information sets; generic hidden-information controls. | [Information-set profile](executable-information-set-profile-v1.md); `InformationSet`, controller and decision membership. | **reuse_existing**, bounded by the profile at Paignia `d4047c0648a89f2aee4461ff70bbc9641e5320cd`. Record each consumer's information visibility and native graph pairing; this profile does not certify its solver. |
| `two-player-normal-form` | Payoff-table games and requests for Nash, correlated equilibrium or quantal-response methods. | [Representation terms](../../ontologies/core/temporality.ttl) and [equilibrium terms](../../ontologies/core/equilibria.ttl), plus `QuantalResponseEquilibrium` in the [behavioural-games module](../../ontologies/extensions/behavioural-games.ttl). | **mapping_review_pending**. Map player/action order, complete payoff ownership, solution criteria and selection/catalogue scope. Quantal response is a method request within this intake, not another game family or an assumed Nash result. |
| `evolutionary-population` | Population-strategy dynamics and replicator methods. | [Evolutionary games](../../ontologies/extensions/evolutionary-games.ttl): `EvolutionaryGame`, `ReplicatorDynamic`. | **mapping_review_pending**. Map population state, time, payoff-to-fitness assumptions and trajectory meaning; numerical integration evidence stays with Paignia. |
| `leader-follower-commitment` | Commitment and follower-response games, including bounded Stackelberg requests. | `GameSpecification`, `ExtensiveFormRepresentation`, strategy/action and observation concepts. | **mapping_review_pending**. Specify commitment visibility, response order, tie treatment and solution concept. The narrower `StackelbergSecurityGame` term must not be assigned to unrelated applications by name alone. |
| `repeated-bargaining` | Repeated or alternating-offer bargaining, including a proposed reusable Rubinstein case. | [Bargaining module](../../ontologies/extensions/bargaining.ttl): `BargainingGame`, `BargainingProtocol`; strategic timing remains separate from representation. | **mapping_review_pending**. Map the horizon, offer protocol, discounting, disagreement outcome and information. Do not identify an alternating-offer game with a cooperative bargaining allocation solely because both concern bargaining. |
| `cooperative-attribution` | Coalition values and contribution attribution, including information-source portfolio requests. | [Cooperative module](../../ontologies/extensions/cooperative.ttl): `CooperativeGame`, `ShapleyValue`. | **mapping_review_pending**. Declare players, coalition value function, baseline and allocation interpretation. Attribution is not automatically a strategic equilibrium or an executable game receipt. |
| `strategic-information` | Screening, signalling, enforcement, disclosure and strategic value-of-information requests. | `InformationSet`, `Signal`, `Belief`; [information design](../../ontologies/extensions/information-design.ttl) and [epistemic games](../../ontologies/extensions/epistemic-games.ttl). | **mapping_review_pending**. Record who observes what and when, incentive/payoff ownership, information leakage negatives and the requested solution criterion; reuse the [existing strategic-information plan](../../conductor/tracks/semantic_game_contracts_20261107/strategic-information-integration.md). |

For every added or updated application case, append its source revision and
semantic decision to the appropriate row or a linked case note. Link the UOGTO
change, Paignia implementation disposition and downstream consumer change in
both directions. An intake entry may remain pending while development proceeds,
but it must not be reported as integrated semantic support.

### Originating application leads

These immutable source links seed the pending reviews; they do not replace
the full-IRI mappings and synthetic conformance examples still required.

- `two-player-normal-form`: [NHRA's QRE implementation](https://github.com/edithatogo/nhra_game/blob/3fe4aaa08521d103ddffbedd58eaa9d7d5256a55/src/nhra_gt/solvers_jax.py),
  [GTPCNZ's pedagogical best response](https://github.com/edithatogo/gtpcnz/blob/4cae5a2f5ebeddd8e86de4263de55caf13c6ef1a/models/primarycare_model/engines/nash_opt_adapter.py)
  and [Innovate's provider adapter](https://github.com/edithatogo/innovate/blob/a79a58d1be51a1c8d4968fd9a535d8b7e5992666/rust/crates/innovate-games/src/lib.rs).
- `repeated-bargaining` and `leader-follower-commitment`:
  [NHRA's sequential methods](https://github.com/edithatogo/nhra_game/blob/3fe4aaa08521d103ddffbedd58eaa9d7d5256a55/src/nhra_gt/subgames/sequential.py).
- `strategic-information` and applicable commitment/information-set concerns:
  [GINSIM's extended models](https://github.com/edithatogo/ginsim/blob/26548c26352dcb571acfc44816cf702a52543fe0/src/model/extended_games.py)
  and [Voiage's strategic behaviour](https://github.com/edithatogo/voiage/blob/11a2bc8685f71c2ff351def742d439c28373cd46/voiage/methods/strategic_behavior.py).
- `cooperative-attribution`: [the value-of-perspective design proposal](https://github.com/edithatogo/vop_poc_nz/blob/7778459f1798e3b6631a285b292a3153ee233333/docs/method/COMPONENT_ATTRIBUTION_DESIGN.md).

## Validation and evidence boundaries

Run the existing relevant semantic, SHACL, fixture and competency tests for the
changed behaviour; the repository's `make validate` and `make test` remain the
normal integration gates. Add positive and contrasting negative cases when a
new semantic invariant is introduced. Avoid text-only tests that merely repeat
this policy.

SGC.01's two bounded profiles and SGC.07's reference labels already have their
own evidence. This intake policy closes none of SGC.02–SGC.06 or SGC.08. Static
semantic acceptance remains distinct from numerical correctness; dynamic
execution additionally needs its trace and native-dispatch evidence. Existing
PR #128 costing work, independent review and issue #134 source-recovery holds
retain their owners and dispositions.
