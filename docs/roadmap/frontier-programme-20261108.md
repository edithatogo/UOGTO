# UOGTO and Paignia: maturity and frontier programme

Date: **8 November 2026**. This is an implementation and research programme,
not a claim that the proposed results have already been achieved. The aim is a
source-grounded semantic layer whose meaning survives transfer between independent
game representations, solvers and environments, with explicit limits.

The immediate [reconciliation](../semantic-reconciliation-20261108.md) repairs
demonstrated defects. The [source audit](../research/game-semantics-source-audit-20261108.md)
establishes why broader coverage and executable evidence are still needed.

## Evidence ladder

| Level | Deliverable | Evidence required to advance |
| --- | --- | --- |
| 1. Correct reference ontology | Typed concepts, scoped constraints, honest tooling | Positive and negative examples, exact CQ answers, regression tests, current reports |
| 2. Source-grounded synthesis | Charted predecessors, libraries and languages | Versioned primary sources, acquisition/licence status, term-level lineage and disagreements |
| 3. Qualified interoperability | Finite profile consumed by Paignia, Gambit and OpenSpiel | Actual independent read/write/run operations, identity and payoff preservation, unsupported-feature errors |
| 4. Reproducible research infrastructure | Stable releases, external cases and measured failures | Cross-version compatibility, clean package use, performance records, reproducible seeds and pinned artifacts |
| 5. Frontier research | A demonstrated improvement on explicit baselines | Held-out evaluation, ablations, uncertainty estimates, reproducible implementation and external criticism |

A large vocabulary, passing local examples, generated review scores or a frontier
roadmap cannot substitute for levels 2–5. A research hypothesis may fail; record
that outcome without relabelling ordinary integration as novelty.

## Track ownership and next work

| Track | Immediate outcome | Dependencies and exit evidence |
| --- | --- | --- |
| [Semantic reconciliation](../../conductor/tracks/semantic_reconciliation_20261108/index.md) | Repair current category, constraint, mapping and tooling defects | Integrated validation and reviewed diff; no external solver claim |
| [Source coverage and synthesis](../../conductor/tracks/ontology_coverage_synthesis_20261108/index.md) | Chart direct GTO predecessor, game vocabularies, languages and library concepts | Acquisition and concept-level evidence before coverage claims |
| [Semantic game contracts](../../conductor/tracks/semantic_game_contracts_20261107/index.md) | Versioned finite subset, full-IRI identity and Rust interchange | SGC.01–05 plus static SGC.08; native traces are a separate optional scope |
| [Repository maturity](../../conductor/tracks/repository_maturity_20261108/index.md) | Formal profile checks, release compatibility and reproducibility | Required checks retained; focused additional gates match the changed behavior |
| [Interoperability and frontier research](../../conductor/tracks/semantic_interoperability_frontier_20261108/index.md) | Real library adapters, adversarial cases and new semantic methods | SGC subset first; library and research leaves advance independently when their inputs are ready |
| [Video-game environment profiles](../../conductor/tracks/video_game_environment_profiles_20261108/index.md) | A bounded strategic scenario grounded in an environment | Start with an accessible open environment; GTA-specific work requires a useful question and suitable access |

Each track specifies checkable leaves, outputs and acceptance criteria. UOGTO owns
semantics; Paignia owns runtime and adapter implementation. Preserve original task
IDs in linked provider/application plans. Do not create a competing Rust engine,
an unconditional simulation prerequisite, or a second consumer acceptance system.

## Coverage before claims of universality

The existing source inventory does not demonstrate that all game-theory ontologies
were examined. Prioritise the direct GTO predecessor identified in Mejbri and
colleagues' [2018 paper](https://eudl.eu/pdf/10.4108/eai.4-1-2018.153533) and acquire
the cited original 2013 work if permitted. Record inaccessible or paper-only sources
honestly. Follow backward and forward citations, terminology variants, registries,
and library references using a dated search protocol with explicit stopping rules.

Keep four source families separate: strategic ontologies; videogame vocabularies
such as GOP/VGO/CGO; declarative languages such as GDL/GDL-II/Ludii/VGDL; and
executable libraries. A source can inform concepts without supplying an OWL import.
Chart game and solution assumptions, information, timing, probability, composition,
learning, cooperation, allocation and execution. Record incompatible definitions
and intentional exclusions. Preserve attribution and per-artifact licences.

For each accepted concept record the primary source/revision, exact supporting
construct, UOGTO IRI, mapping relation, assumptions, example, competency question,
and validation obligation. Use narrower/broader/related mappings when appropriate;
similar labels do not establish equivalence. Measure coverage against a declared
case and concept denominator. Report missing cases instead of pursuing an
unfalsifiable claim to have captured every possible game ontology.

## Learn from libraries at the level of semantics

The [Gambit API](https://gambitproject.readthedocs.io/en/latest/pygambit.html) and
[OpenSpiel concepts](https://openspiel.readthedocs.io/en/latest/concepts.html) are
primary comparators. Pin actual versions when implementing adapters: a latest-docs
page is a discovery source, not a reproducible build dependency.

| Source | Concepts to preserve | Distinguishing test |
| --- | --- | --- |
| Gambit | Strategic versus extensive representations; histories; information sets; perfect recall; chance; mixed and behavioural profiles; exact payoffs; solver diagnostics | A small imperfect-information tree preserves information partitions and payoff ownership on round trip; a mutated partition fails |
| OpenSpiel | Game versus state/trajectory; legal actions; simultaneous and chance nodes; information state versus observation; reward versus return; horizon and termination | A seeded trajectory matches declared legal actions, chance probabilities, information access and return aggregation |
| PettingZoo | AEC versus Parallel scheduling; agent lifecycles; observations/action masks; termination versus truncation | Serial collection of simultaneous actions does not leak earlier choices or change the strategic game |
| PyCID | Decision/utility/chance nodes; causal versus informational edges; interventions | Observation and intervention produce distinguishable records under stated causal assumptions |
| Open Game Engine | Typed component interfaces, composition and profitable deviations | A composed example preserves interfaces and reports a deliberately introduced profitable deviation |

Names and example bindings already exist for some of these concepts. The missing
work is qualified abstraction and execution, including a mapping of unsupported
features. Do not equate an action with a contingent strategy, a current observation
with information history, a training reward with preference utility, or a candidate
profile with a verified equilibrium. Chance distribution normalisation and executable
completeness belong to scoped profiles rather than every partial RDF description.

Start with small matrix games, a finite sequential game, a chance game, an
imperfect-information game and a repeated simultaneous game. Include deliberately
asymmetric payoffs, colliding labels, inaccessible actions and invalid probabilities.
Run the actual external libraries in optional isolated CI jobs. UOGTO's local
reference runner cannot certify their behavior. Keep heavy or restrictive external
dependencies out of the default semantic package.

## Maturity and hardening

Maintain the current required validation checks. Add formal profile/reasoner checks
with documented scope and negative fixtures, then release compatibility checks for
published IRIs and changed entailments. Run package tests from outside the checkout.
Use supported Python versions for each optional adapter without silently raising
the core Python 3.10 minimum. Pin tool and provider revisions in reproducible jobs.

Generate evidence from current inputs with hashes. Frozen publication artifacts
remain dated snapshots until a deliberate manuscript revision regenerates them.
Report optional renderer failures explicitly. Profile ontology loading, SHACL and
interchange at declared graph sizes, then set budgets from measured baselines.
Use property-based or metamorphic tests where they can expose real semantic errors;
avoid tests that merely repeat implementation constants.

Examples of useful metamorphic properties are invariance under consistent player
renaming, preservation of payoff associations under action reordering, legal-action
closure, and preservation of equilibrium claims under mathematically justified
payoff transformations. Each property must state its conditions: an arbitrary
transformation need not preserve every equilibrium refinement or learning dynamic.

## Research intended to advance the frontier

These are hypotheses to test against a refreshed related-work review. Implementing
them is not itself proof that they exceed the state of the art.

1. **Semantic-loss analysis for translations.** Produce a machine-checkable account
   of preserved and discarded players, strategies, information partitions, chance,
   preferences and timing when converting representations. Compare with direct
   library conversions and identity-only round trips. Measure undetected semantic
   errors, false rejection, supported features and cost on held-out cases.
2. **Typed composition with explicit assumptions.** Compose strategic components
   while checking information flow, utility ownership, interface compatibility and
   solution assumptions. Compare with established compositional-game frameworks;
   test counterexamples and ablate each check. Avoid claiming unrestricted
   equivalence or equilibrium preservation for arbitrary games.
3. **Strategic information and causal valuation.** Connect Paignia's game model with
   the existing Voiage handoff to evaluate information when other players adapt.
   Compare with fixed-policy and non-strategic value-of-information baselines.
   Separate model uncertainty, equilibrium selection and causal assumptions.
4. **Auditable natural-language game construction.** Recover an explicit game and
   its assumptions from text, request missing information when needed, and validate
   the result using profiles and solvers. Compare with existing language-to-game
   systems and direct schema-constrained extraction. Score semantic accuracy and
   calibrated abstention, not just valid JSON or RDF.

Use held-out games specified independently of the ontology implementation and
include simpler baselines. Predeclare primary measures and comparison conditions,
report failures and confidence intervals where applicable, and seek external
domain criticism. Coding-agent review is internal engineering evidence. A credible
frontier result is a measured improvement that survives these comparisons.

### Concrete prior-work baselines

| Primary work | Existing contribution relevant to the programme | Fair comparison |
| --- | --- | --- |
| [Ghani et al., Compositional game theory (2016 preprint, revised 2018)](https://arxiv.org/abs/1603.04641) | Open-game composition with stated equilibrium and best-response preservation results | Test supported compositions and off-equilibrium deviations under the same assumptions |
| [Hammond et al., Equilibrium Refinements for Multi-Agent Influence Diagrams: Theory and Practice (2021)](https://arxiv.org/abs/2102.05008) | MAID/EFG equivalence results and equilibrium reasoning | Check strategy/payoff correspondence and relevant refinements, beyond graph identity |
| [Hammond et al., Reasoning about Causality in Games (2023)](https://arxiv.org/abs/2301.02324) | Causal/mechanised games and prediction, intervention and counterfactual queries | Compare answers on matched models with explicit structural assumptions |
| [Deng et al., From Natural Language to Extensive-Form Game Representations (AAMAS 2025)](https://arxiv.org/abs/2501.17282) | GameInterpreter uses information-set reasoning and self-debugging to construct PyGambit models | Hold model, token budget and game instances constant; score strategic correctness separately from executable output |
| [Wang et al., From Natural Language to Extensive-Form Game Representations: Defining and Automatically Verifying Consistency (2026)](https://www.csc.liv.ac.uk/research/seminars/abstract.php?id=1501) | Reference translation instances and an automated checker of reduced strategies and further constraints | Compare against the checker and add held-out ambiguity, information-loss and timing cases |

The 2026 institutional abstract corroborates the consistency framework. Its
[workshop PDF](https://openreview.net/pdf/0cda049e6d21fce6c6b4f4707c8e03674f5c9d15.pdf)
was discoverable through primary indexed text, but direct retrieval encountered a
browser challenge in this audit. Record that limitation when acquiring its exact
dataset/code. It is not evidence of a general guarantee of natural-language fidelity.

These comparators make translation, composition and causal annotations alone
insufficient novelty claims. The proposed improvement is more reliable, explicitly
scoped semantic preservation and loss reporting, tested against these approaches.

## Real video games and GTA

A video-game title, world, scenario, strategic model, runtime session and trace are
different entities. A proposed GTA driving interaction might model two drivers,
their observations, acceleration/lane actions, objectives and a finite horizon.
An alternative with one adaptive controller and fixed traffic is a different
decision problem; additional screen characters do not automatically imply
strategic agents. These are proposed abstractions, not assertions that a specific
GTA plugin already exposes controllable multi-agent play.

[DeepGTAV](https://github.com/aitorzip/DeepGTAV) demonstrates a vision-based driving
research environment. Reuse environmental mechanisms only where they answer a
stated research question. Begin with a small open environment, quantify lost
information in the strategic abstraction, and add a commercial environment only
when it contributes evidence. Code licensing does not grant commercial asset
redistribution rights. UOGTO should describe the model and provenance, not accumulate
every vehicle, weapon or mission as a universal game-theory primitive.

## First executable sequence

Complete the current repair validation; chart GTO and the Gambit/OpenSpiel concept
gaps; agree the smallest Paignia executable profile; implement actual round trips;
then test information leakage and semantic loss on independent cases. Video-game
profiles and strategic-information research can advance on their own prerequisites.
Update Conductor from measured outcomes and leave unimplemented leaves pending.
