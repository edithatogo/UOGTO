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
construction. The repository roles below determine which library owns each
capability and how optional composition remains acyclic.

## Current application scope and library partners

The maintainer-defined downstream application set is exactly
[nhra_game](https://github.com/edithatogo/nhra_game),
[gtpcnz](https://github.com/edithatogo/gtpcnz),
[new-drug-reimbursement-game](https://github.com/edithatogo/new-drug-reimbursement-game),
[ginsim](https://github.com/edithatogo/ginsim),
[tobac](https://github.com/edithatogo/tobac) and
[tutorial_health_gt](https://github.com/edithatogo/tutorial_health_gt).
Their game changes enter this semantic ledger and Paignia's implementation
intake. Inclusion identifies ownership and intended integration; each actual
game still needs its own mapping, supported profile and consumer evidence.

| Repository or capability | Ownership and integration contract |
| --- | --- |
| [Innovate](https://github.com/edithatogo/innovate) | A parallel innovation library with capability-specific boundaries. Innovation diffusion, adoption, substitution and domain behaviour stay there. Migrate mature generic game algorithms to Paignia method by method after numerical/behavioural parity and caller compatibility are demonstrated; retain the working implementation until the replacement is qualified. Its optional Paignia adapter is a library integration, not membership of the six-application set. |
| [Kairos](https://github.com/edithatogo/kairos) | Reusable time, scheduling, state, RNG and replay provider, composed through the optional game-execution adapter. Static game solving does not acquire a mandatory simulation dependency. |
| [Voiage](https://github.com/edithatogo/voiage) | Owns value-of-information, value-of-perspective (VoP) and value-of-heterogeneity (VoH) methods and estimands. Compose through explicit outcomes/strategy contracts. A genuinely shared game foundation may be supplied by Paignia after its specific need and parity are established; that does not move the information-value methods into Paignia. |
| [Dapane](https://github.com/edithatogo/dapane) | Reusable costing and valuation provider. Compose through explicit optional adapters and declared valuation-to-utility mappings; monetary costs or transfers do not automatically become game payoffs. |
| [vop_poc_nz](https://github.com/edithatogo/vop_poc_nz) | Its demonstration belongs with Voiage's VoP/VoH work. It is not a direct Paignia application or a generic-game transfer obligation. Route a separate shared-game need through the appropriate intake key only if such a need is demonstrated. |
| [archive-govt-nz](https://github.com/edithatogo/archive-govt-nz) | Archive-only material and Hugging Face registry context. It is not a runtime provider or a direct Paignia application. Preserve archive/source provenance independently of numerical-library ownership. |

Optional composition may use versioned data contracts or adapters that depend
on the selected providers. Keep the dependency graph acyclic: an application
or adapter can consume several libraries, but Paignia's core must not import
an application or create a reverse dependency on a library that consumes it.
Record dependencies per capability rather than imposing one total repository
hierarchy. UOGTO continues to describe relevant cross-cutting semantics without
taking ownership of any provider's numerical method.

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
3. **Return reusable game implementation to Paignia.** Link the same key and
   UOGTO change from the provider intake. New reusable games/mechanics and
   generic game algorithms belong in Paignia; application data, innovation
   models and information-value methods retain the owners above. Assess
   relevant upstream capabilities before writing a substitute. Existing
   generic game methods migrate after parity and consumer qualification, not
   merely because they appear in a partner library. Preserve source revision,
   licence and attribution for any transferred fixture or code.
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
| `discounted-markov` | Paignia T22 discounted policy evaluation. | `DynamicGame`, `MarkovGame`, `TransitionFunction`, `ActionProfile` and `JointPolicy`. | **extension_required**, implemented for the [bounded v1 profile and frozen recurring-funding fixture](executable-discounted-markov-profile-v1.md). Explicit axes, stage reward, model discount and labelled initial/transition/policy weights support local UOGTO admission and projection. Paignia owns native qualification. [UOGTO #144](https://github.com/edithatogo/UOGTO/issues/144) |
| `two-player-normal-form` | Payoff-table games and requests for Nash, correlated equilibrium or quantal-response methods. | [Representation terms](../../ontologies/core/temporality.ttl) and [equilibrium terms](../../ontologies/core/equilibria.ttl), plus `QuantalResponseEquilibrium` in the [behavioural-games module](../../ontologies/extensions/behavioural-games.ttl). | **mapping_review_pending**. Map player/action order, complete payoff ownership, solution criteria and selection/catalogue scope. Quantal response is a method request within this intake, not another game family or an assumed Nash result. |
| `evolutionary-population` | Population-strategy dynamics and replicator methods. | [Evolutionary games](../../ontologies/extensions/evolutionary-games.ttl): `EvolutionaryGame`, `ReplicatorDynamic`. | **mapping_review_pending**. Map population state, time, payoff-to-fitness assumptions and trajectory meaning; numerical integration evidence stays with Paignia. |
| `leader-follower-commitment` | Commitment and follower-response games, including bounded Stackelberg requests. | `GameSpecification`, `ExtensiveFormRepresentation`, strategy/action and observation concepts. | **mapping_review_pending**. Specify commitment visibility, response order, tie treatment and solution concept. The narrower `StackelbergSecurityGame` term must not be assigned to unrelated applications by name alone. |
| `repeated-bargaining` | Repeated or alternating-offer bargaining, including a proposed reusable Rubinstein case. | [Bargaining module](../../ontologies/extensions/bargaining.ttl): `BargainingGame`, `BargainingProtocol`; strategic timing remains separate from representation. | **mapping_review_pending**. Map the horizon, offer protocol, discounting, disagreement outcome and information. Do not identify an alternating-offer game with a cooperative bargaining allocation solely because both concern bargaining. |
| `cooperative-attribution` | Coalition values and contribution attribution where a shared game foundation is needed; Voiage retains information-source and VoP/VoH methods. | [Cooperative module](../../ontologies/extensions/cooperative.ttl): `CooperativeGame`, `ShapleyValue`. | **mapping_review_pending**. Declare players, coalition value function, baseline and allocation interpretation. Establish the generic-game need separately from the Voiage estimand; no direct transfer is inferred from a demo or archive. Attribution is not automatically a strategic equilibrium or an executable game receipt. |
| `strategic-information` | Screening, signalling, enforcement, disclosure and strategic value-of-information requests. | `InformationSet`, `Signal`, `Belief`; [information design](../../ontologies/extensions/information-design.ttl) and [epistemic games](../../ontologies/extensions/epistemic-games.ttl). | **mapping_review_pending**. Record who observes what and when, incentive/payoff ownership, information leakage negatives and the requested solution criterion; reuse the [existing strategic-information plan](../../conductor/tracks/semantic_game_contracts_20261107/strategic-information-integration.md). |

For every added or updated application case, append its source revision and
semantic decision to the appropriate row or a linked case note. Link the UOGTO
change, Paignia implementation disposition and downstream consumer change in
both directions. An intake entry may remain pending while development proceeds,
but it must not be reported as integrated semantic support.

### Application and partner evidence

These immutable source links seed the pending reviews; they do not replace
the full-IRI mappings and synthetic conformance examples still required. The
application leads are a starting sample within the exact six-repository scope.

- `two-player-normal-form`: [NHRA's QRE implementation](https://github.com/edithatogo/nhra_game/blob/3fe4aaa08521d103ddffbedd58eaa9d7d5256a55/src/nhra_gt/solvers_jax.py),
  and [GTPCNZ's pedagogical best response](https://github.com/edithatogo/gtpcnz/blob/4cae5a2f5ebeddd8e86de4263de55caf13c6ef1a/models/primarycare_model/engines/nash_opt_adapter.py).
- `repeated-bargaining` and `leader-follower-commitment`:
  [NHRA's sequential methods](https://github.com/edithatogo/nhra_game/blob/3fe4aaa08521d103ddffbedd58eaa9d7d5256a55/src/nhra_gt/subgames/sequential.py).
- `strategic-information` and applicable commitment/information-set concerns:
  [GINSIM's extended models](https://github.com/edithatogo/ginsim/blob/26548c26352dcb571acfc44816cf702a52543fe0/src/model/extended_games.py).

Partner evidence is separate: [Innovate's provider adapter](https://github.com/edithatogo/innovate/blob/a79a58d1be51a1c8d4968fd9a535d8b7e5992666/rust/crates/innovate-games/src/lib.rs)
is a bounded integration starting point, and [Voiage's strategic behaviour](https://github.com/edithatogo/voiage/blob/11a2bc8685f71c2ff351def742d439c28373cd46/voiage/methods/strategic_behavior.py)
can inform shared semantic review. Neither source transfers an entire partner
library's responsibilities. VoP/VoH demo and archive provenance remain with
their respective owners described above.

### Recorded consumer case: tutorial coordination, edition 0.2

Shared intake key: `finite-perfect-information`; case identity:
`urn:tutorial-health-gt:coordination:v1`. Semantic disposition: **reuse_existing**
for the bounded declaration below. This is a synthetic teaching case, with no
empirical health or financial data and no new ontology term.

The commissioner chooses `no-offer` or `offer`; after an offer, the provider
observes that choice and chooses `participate` or `decline`. Complete terminal
utilities, ordered as commissioner/provider, are `(1, 1)`, `(3, 2)` and `(0, 0)`
respectively. Utilities are invented, dimensionless preferences; they are not
costs, transfers or health outcomes.

| Declaration concern | Existing semantic reference |
| --- | --- |
| Specification | `https://w3id.org/uogto/core#GameSpecification` |
| Representation | `https://w3id.org/uogto/core#ExtensiveFormRepresentation` |
| Observations | `https://w3id.org/uogto/core#PerfectInformation` |
| Sequential strategic timing | `https://w3id.org/uogto/core#DynamicGame`; this does not assert native dynamic execution. |

The [consumer declaration](https://github.com/edithatogo/tutorial_health_gt/blob/3851a2346c8e9cc457c7bfee67848be13fc8ca46/examples/finite-coordination/declaration.json)
has SHA-256 `08fe41af4158af49908e61c82d73511a1dabb7bc1f5a4e4f1a1dc2f97e919fab`.
The repository is private; readers need access to inspect its source. Its
[locked check](https://github.com/edithatogo/tutorial_health_gt/blob/3851a2346c8e9cc457c7bfee67848be13fc8ca46/examples/finite-coordination/check_declaration.py)
ran with UOGTO `0050e19faec2abaa05e5d474e5eed0150bcbf073` and returned
`profile_declaration_compatible`, with `native_execution_qualified=false`.
Contrasting declarations requesting native execution or imperfect information
were rejected. The provider profile is
`paignia/static-finite-perfect-information-sparse-zero/1.0.0`, pinned to
Paignia `bd880dd756d2ba56cc5f479bc078cea31b53c1d1`.

The [paired Paignia case](https://github.com/edithatogo/paignia/blob/main/docs/integrations/downstream-game-intake.md#recorded-consumer-case-tutorial-coordination-edition-02)
records the separate native execution and invalid-graph checks. This note is
the example/mapping update for reuse of the declaration profile. A complete RDF
instance graph, general round-trip mapping and SGC consumer acceptance remain
pending; the declaration validator does not inspect the native graph. The
tutorial's hosted jobs failed before execution, so this records local evidence
only and closes no SGC obligation.

### Recorded consumer case: tutorial coordination, edition 0.3

The same synthetic case and intake key are retained; no new vocabulary,
empirical health data or native dynamic execution is admitted. Edition 0.2
remains the declaration-only rollback at its original pins.

The [provider receipt](https://github.com/edithatogo/paignia/blob/8c17466cd9ca062b897eaa72a6780edc08375885/docs/integrations/downstream-game-intake.md#tutorial-coordination-edition-03)
records signed Paignia 0.1.0 at `a04a19da06cc50e310a172574ed66f62000b891a`.
The declaration check uses UOGTO `d93dfffe192fed2f833bd9b0681694113f663b9c`;
the separate RDF bridge stages the [provider's locked ontology bundle](https://github.com/edithatogo/paignia/blob/a04a19da06cc50e310a172574ed66f62000b891a/verification/uogto_interchange/ontology-lock.json)
at UOGTO `cc0c84201929996580bb4af98774cf2145b224ae`. These two source
revisions are not interchangeable. The admitted profile remains
`paignia/static-finite-perfect-information-sparse-zero/1.0.0`.

The [receiving lesson PR](https://github.com/edithatogo/tutorial_health_gt/pull/15)
merged at `eec4d60558bd8b8e0f999d6ee0188a7bc6bdb40d`. The [lesson workflow](https://github.com/edithatogo/tutorial_health_gt/actions/runs/45641146686/job/139299812534)
and [privacy workflow](https://github.com/edithatogo/tutorial_health_gt/actions/runs/45641146572)
both passed on that exact revision. The hosted lesson log reports the
following asserted RDF fixture digests (SHA-256) and ordered utilities:

| Fixture | SHA-256 | Commissioner/provider |
| --- | --- | --- |
| Baseline | `d44c1716e476febc17986503ab9f1b7ebb1057880578d9a06f476eea44e23b2f` | (3, 2) |
| Changed payoff | `bae0a02a72773b678b89a83d7681b988903674e25f0189efb4dfa141557e1467` | (1, 1) |

The hosted declaration check still returned `native_execution_qualified=false`;
the separate RDF replay validated the pinned bundle, projected the ordered
decision graph to the Rust solver, checked its returned RDF specification
link and rejected duplicate action positions. The provider receipt separately
records independent controls for reordered actions, changed off-path payoffs
and invalid node inventory. The tutorial repository and logs require access;
no private source files are redistributed here.

This is receiving evidence for the named finite perfect-information case,
not an unrestricted RDF round trip, a current-main repin, a qualification of
all SGC leaves, or release/publication approval. General semantic and
dynamic acceptance remain with their existing owners (issue #123).

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
