# ChatGPT Deep Research Output - Part 2

Use this as the **first prompt in a fresh Codex session at the root of a new repo**. I structured it with explicit context, deliverables, validation commands, and a definition of done because Codex’s own docs recommend giving clear context, validation steps, and smaller focused work units; they also note that subagent workflows should be explicitly requested when you want parallel agents. ([OpenAI Developers][1]) ([OpenAI Developers][2])

```text
You are Codex operating at the root of a brand-new Git repository.

Act as the CONDUCTOR AGENT and Lead Ontology Engineer for a new open-source project:

Repository name:
uogto

Project name:
Universal Open Game Theory Ontology

Abbreviation:
UOGTO

Mission:
Bootstrap a production-grade, modular, version-controlled ontology repository for a universal, open, machine-readable game theory ontology. The ontology must support classical game theory, cooperative and non-cooperative games, multi-agent systems, simulation execution, mechanism design, MARL, causal games, network games, mean-field games, evolutionary games, institutional economics, deontic logic, computational social choice, LLM-agent interaction games, digital-twin execution, compositional/open games, Petri-net/DEVS/HLA interoperability, SHACL validation, JSON-LD bindings, SPARQL competency queries, and executable knowledge-graph semantics.

Do not stop at planning. Create the actual repo scaffold and the first working ontology implementation.

If Codex subagents are available in this environment, explicitly spawn parallel subagents after creating the conductor system:
1. Ontology Architect
2. RDF/OWL Engineer
3. SHACL Validation Engineer
4. JSON-LD/Schema Engineer
5. Examples and Competency Questions Engineer
6. Documentation and Release Engineer
7. Reviewer/QA Agent

Wait for all subagents, reconcile their outputs, then write the final files. If native subagents are not available, simulate the same workflow sequentially and record decisions in `.conductor/runlog.md`.

Important:
- Do not ask clarifying questions.
- Make reasonable defaults.
- Prefer durable repo files over chat-only explanations.
- Use open, non-proprietary standards.
- Do not require external network access for validation.
- If internet access is unavailable, include `docs/references.md` with citation placeholders and standards to verify later.
- Keep OWL/RDFS semantics open-world and use SHACL for closed-world validation constraints.
- Avoid over-constraining ontology domains/ranges where it would reduce reuse.
- Every TTL/JSON-LD/SHACL file created must parse successfully.
- Every example graph must validate against the SHACL shapes unless explicitly marked as a negative test.

=====================================================================
CONDUCTOR SYSTEM TO CREATE
=====================================================================

Create a repo-local conductor system that future Codex sessions can follow.

Create these files:

1. `AGENTS.md`
   Purpose:
   - Root instructions for all future Codex work in this repo.
   - Include project scope, ontology design rules, naming conventions, validation requirements, and definition of done.
   - Include instructions to always run validation before reporting completion.
   - Include instructions to update `.conductor/status.md` and `.conductor/runlog.md` after meaningful work.
   - Include subagent role descriptions and when to delegate.

2. `CONDUCTOR.md`
   Purpose:
   - Human-readable operating manual for the conductor system.
   - Explain phases, task graph, quality gates, release gates, and how to add a new ontology module.
   - Include commands for build, validation, examples, and coverage.

3. `.conductor/tasks.yaml`
   Purpose:
   - A task graph with phases:
     - phase_00_bootstrap
     - phase_01_core_ontology
     - phase_02_classical_and_cooperative_games
     - phase_03_information_and_epistemic_games
     - phase_04_dynamics_simulation_and_execution
     - phase_05_mechanism_design_social_choice_and_allocation
     - phase_06_learning_marl_and_evolution
     - phase_07_network_mean_field_and_continuous_games
     - phase_08_norms_contracts_institutions_and_deontic_logic
     - phase_09_llm_agents_digital_twins_and_protocols
     - phase_10_validation_examples_docs_release
   - Each task should include:
     - id
     - owner_role
     - inputs
     - outputs
     - validation_command
     - acceptance_criteria
     - status

4. `.conductor/roles/ontology-architect.md`
5. `.conductor/roles/rdf-owl-engineer.md`
6. `.conductor/roles/shacl-validation-engineer.md`
7. `.conductor/roles/jsonld-schema-engineer.md`
8. `.conductor/roles/examples-engineer.md`
9. `.conductor/roles/docs-release-engineer.md`
10. `.conductor/roles/reviewer-qa.md`

Each role file should contain:
- Mission
- Responsibilities
- Inputs
- Outputs
- Review checklist
- Failure modes to watch for

11. `.conductor/status.md`
   Purpose:
   - Current project state.
   - Completed modules.
   - Known gaps.
   - Next recommended task.

12. `.conductor/runlog.md`
   Purpose:
   - Append-only log of decisions, commands run, validation results, and unresolved issues.

13. `.conductor/module-template.md`
   Purpose:
   - Template for adding a new ontology module.
   - Include required TTL, SHACL, JSON-LD, docs, examples, competency queries, and tests.

14. `scripts/conductor.py`
   Purpose:
   - Read `.conductor/tasks.yaml`.
   - Print task status.
   - Report incomplete tasks.
   - Report which files each task is expected to create.
   - This does not need to be a full orchestrator; it should be a lightweight repo-local task inspector.

=====================================================================
REPOSITORY STRUCTURE TO CREATE
=====================================================================

Create this structure:

uogto/
├── AGENTS.md
├── CONDUCTOR.md
├── README.md
├── LICENSE
├── LICENSE-CODE
├── CITATION.cff
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── pyproject.toml
├── Makefile
├── .gitignore
├── .github/
│   └── workflows/
│       └── validate.yml
├── .conductor/
│   ├── tasks.yaml
│   ├── status.md
│   ├── runlog.md
│   ├── module-template.md
│   └── roles/
├── ontologies/
│   ├── core/
│   │   ├── uogto-core.ttl
│   │   ├── agents.ttl
│   │   ├── games.ttl
│   │   ├── strategies.ttl
│   │   ├── actions.ttl
│   │   ├── outcomes.ttl
│   │   ├── payoffs.ttl
│   │   ├── information.ttl
│   │   ├── dynamics.ttl
│   │   ├── equilibria.ttl
│   │   └── rules.ttl
│   ├── extensions/
│   │   ├── cooperative.ttl
│   │   ├── mechanism-design.ttl
│   │   ├── auctions.ttl
│   │   ├── bargaining.ttl
│   │   ├── marl.ttl
│   │   ├── learning-in-games.ttl
│   │   ├── causal-games.ttl
│   │   ├── network-games.ttl
│   │   ├── mean-field-games.ttl
│   │   ├── evolutionary-games.ttl
│   │   ├── institutional-economics.ttl
│   │   ├── deontic-logic.ttl
│   │   ├── computational-social-choice.ttl
│   │   ├── matching-allocation.ttl
│   │   ├── contract-theory.ttl
│   │   ├── information-design.ttl
│   │   ├── behavioural-games.ttl
│   │   ├── algorithmic-game-theory.ttl
│   │   ├── epistemic-games.ttl
│   │   ├── verification-games.ttl
│   │   ├── security-games.ttl
│   │   ├── differential-hybrid-games.ttl
│   │   ├── congestion-routing-games.ttl
│   │   ├── game-description-languages.ttl
│   │   ├── llm-agent-games.ttl
│   │   ├── digital-twin-games.ttl
│   │   ├── compositional-open-games.ttl
│   │   ├── petri-net-devs-hla.ttl
│   │   ├── trust-reputation-provenance.ttl
│   │   ├── privacy-disclosure.ttl
│   │   └── kg-execution-bindings.ttl
│   └── alignments/
│       ├── prov-o.ttl
│       ├── schema-org.ttl
│       ├── wot-thing-description.ttl
│       ├── mcp-a2a.ttl
│       └── open-games.ttl
├── shapes/
│   ├── core.shacl.ttl
│   ├── game-types.shacl.ttl
│   ├── execution.shacl.ttl
│   ├── governance.shacl.ttl
│   └── examples.shacl.ttl
├── jsonld/
│   ├── context.jsonld
│   ├── core.context.jsonld
│   └── extensions.context.jsonld
├── examples/
│   ├── prisoners-dilemma.jsonld
│   ├── stag-hunt.ttl
│   ├── normal-form-game.jsonld
│   ├── extensive-form-game.ttl
│   ├── first-price-auction.jsonld
│   ├── cooperative-coalition-game.ttl
│   ├── stochastic-markov-game.jsonld
│   ├── marl-gridworld-game.jsonld
│   ├── signalling-game.ttl
│   ├── voting-social-choice-game.jsonld
│   ├── matching-market.ttl
│   ├── contract-principal-agent-game.ttl
│   ├── security-stackelberg-game.jsonld
│   ├── llm-tool-use-game.jsonld
│   ├── digital-twin-security-game.ttl
│   └── petri-net-execution-game.ttl
├── competency-questions/
│   ├── cq01-list-players.rq
│   ├── cq02-list-strategies.rq
│   ├── cq03-find-equilibria.rq
│   ├── cq04-games-with-incomplete-information.rq
│   ├── cq05-security-games-with-targets.rq
│   ├── cq06-mechanisms-with-incentive-constraints.rq
│   ├── cq07-llm-games-with-tool-invocations.rq
│   ├── cq08-executable-games-with-event-traces.rq
│   ├── cq09-games-with-privacy-budget.rq
│   └── cq10-modules-and-imports.rq
├── scripts/
│   ├── build.py
│   ├── validate.py
│   ├── report_coverage.py
│   └── conductor.py
├── tests/
│   ├── test_parse_ttl.py
│   ├── test_parse_jsonld.py
│   ├── test_shacl_examples.py
│   ├── test_competency_queries.py
│   └── test_coverage_thresholds.py
├── docs/
│   ├── architecture.md
│   ├── ontology-design-principles.md
│   ├── module-map.md
│   ├── class-hierarchy.md
│   ├── object-properties.md
│   ├── data-properties.md
│   ├── constraints-and-shacl.md
│   ├── jsonld-bindings.md
│   ├── examples.md
│   ├── competency-questions.md
│   ├── software-architecture-mapping.md
│   ├── release-process.md
│   └── references.md
└── dist/
    └── .gitkeep

=====================================================================
ONTOLOGY DESIGN REQUIREMENTS
=====================================================================

Use these base prefixes:

@prefix uogto:  <https://w3id.org/uogto/core#> .
@prefix uogtox: <https://w3id.org/uogto/extensions#> .
@prefix owl:    <http://www.w3.org/2002/07/owl#> .
@prefix rdf:    <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:   <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:    <http://www.w3.org/2001/XMLSchema#> .
@prefix skos:   <http://www.w3.org/2004/02/skos/core#> .
@prefix sh:     <http://www.w3.org/ns/shacl#> .
@prefix prov:   <http://www.w3.org/ns/prov#> .

Use:
- `rdfs:label` on every class and property.
- `skos:definition` on every major class and property.
- `rdfs:subClassOf` for hierarchy.
- `owl:ObjectProperty` and `owl:DatatypeProperty`.
- SHACL for min counts, required relationships, value classes, and example validation.
- JSON-LD context files for developer-friendly data interchange.
- SPARQL competency queries for retrieval tests.
- Python scripts for parse, validation, and build.

Do not use blank labels such as “TODO”.
If a concept needs future refinement, include a clear `skos:scopeNote`.

Separate:
- Game specification from game instance.
- Game instance from play session.
- Play session from event trace.
- Strategy from action.
- Utility function from payoff.
- Outcome from state.
- Information set from belief.
- Norm from contract.
- Agent capability from tool invocation.
- Ontology schema from executable runtime binding.

Core ontology must include at least:
- GameEntity
- GameSpecification
- GameInstance
- PlaySession
- Player
- Agent
- Coalition
- Institution
- Role
- Strategy
- StrategyProfile
- Action
- ActionProfile
- Outcome
- Payoff
- UtilityFunction
- PreferenceRelation
- State
- InitialState
- TerminalState
- Transition
- TransitionFunction
- InformationSet
- Belief
- Signal
- Rule
- Norm
- Equilibrium
- Solver
- ExecutionModel
- EventTrace

Core object properties must include at least:
- hasPlayer
- participatesIn
- hasRole
- hasStrategy
- hasAvailableAction
- selectsAction
- hasStrategyProfile
- producesOutcome
- assignsPayoff
- hasUtilityFunction
- hasState
- hasInitialState
- hasTerminalState
- hasTransition
- transitionsFrom
- transitionsTo
- observes
- hasInformationSet
- hasBelief
- governedByRule
- governedByNorm
- hasEquilibrium
- solvedBy
- compiledToExecutionModel
- emitsEventTrace

Core data properties must include at least:
- identifier
- name
- description
- version
- probability
- payoffValue
- utilityValue
- timeIndex
- timestamp
- confidence
- sourceReference

=====================================================================
EXTENSION MODULE REQUIREMENTS
=====================================================================

Each extension module must contain:
- At least 5 meaningful classes unless the domain is naturally smaller.
- At least 5 meaningful properties or clearly justified fewer properties.
- Labels and definitions.
- At least one SHACL shape, example, or competency query connected to the module.
- No empty placeholder files.

Implement initial content for all of these modules:

1. Classical / non-cooperative games
   Classes:
   NormalFormGame, MatrixGame, ExtensiveFormGame, RepeatedGame, StochasticGame, BayesianGame, SignalingGame, IncompleteInformationGame.

2. Cooperative games
   Classes:
   CooperativeGame, CoalitionGame, TransferableUtilityGame, NonTransferableUtilityGame, CharacteristicFunction, CoreSolution, ShapleyValue, BargainingSolution.

3. Mechanism design and auctions
   Classes:
   Mechanism, DirectMechanism, Auction, FirstPriceAuction, SecondPriceAuction, VickreyAuction, AllocationRule, PaymentRule, IncentiveCompatibilityConstraint, IndividualRationalityConstraint.

4. MARL and learning in games
   Classes:
   MarkovGame, MultiAgentEnvironment, Policy, JointPolicy, RewardFunction, ObservationSpace, ActionSpace, LearningAlgorithm, SelfPlay, RegretMetric, ExploitabilityMetric.

5. Causal game theory
   Classes:
   CausalGame, CausalModel, CausalGraph, Intervention, CounterfactualOutcome, StructuralEquation, CausalPayoffModel.

6. Network games
   Classes:
   NetworkGame, GraphPlayer, NetworkEdge, LocalInteraction, NeighborSet, DiffusionGame, InfluenceGame.

7. Mean-field games
   Classes:
   MeanFieldGame, PopulationState, RepresentativeAgent, DistributionalState, MeanFieldEquilibrium, PopulationPolicy.

8. Evolutionary games
   Classes:
   EvolutionaryGame, Population, ReplicatorDynamic, EvolutionarilyStableStrategy, MutationOperator, FitnessFunction.

9. Institutional economics
   Classes:
   Institution, InstitutionalRule, GovernanceMechanism, PropertyRight, TransactionCost, EnforcementMechanism, CollectiveChoiceArena.

10. Deontic logic and normative systems
    Classes:
    Norm, Obligation, Permission, Prohibition, Sanction, Violation, ComplianceState, DeonticModality.

11. Computational social choice
    Classes:
    VotingGame, Voter, Candidate, Ballot, SocialChoiceFunction, VotingRule, PreferenceProfile, CondorcetWinner, ManipulationProblem.

12. Matching, allocation, and fair division
    Classes:
    MatchingMarket, Matching, StableMatching, BlockingPair, Allocation, EnvyFreeAllocation, ProportionalAllocation, FairnessCriterion.

13. Contract theory
    Classes:
    ContractGame, PrincipalAgentGame, Contract, Principal, AgentRole, IncentiveScheme, HiddenAction, HiddenInformation, MonitoringTechnology, ParticipationConstraint.

14. Information design and Bayesian persuasion
    Classes:
    InformationDesigner, SignalStructure, DisclosurePolicy, PersuasionMechanism, PosteriorBelief, ReceiverBelief.

15. Behavioural and experimental game theory
    Classes:
    BehaviouralGame, BoundedRationalityModel, QuantalResponseEquilibrium, LevelKModel, CognitiveHierarchyModel, FairnessPreference, ExperimentalProtocol.

16. Algorithmic game theory and complexity
    Classes:
    AlgorithmicGame, ComputationalProblem, EquilibriumComputationProblem, ComplexityClass, ApproximationGuarantee, PriceOfAnarchy, PriceOfStability.

17. Epistemic games
    Classes:
    EpistemicGame, TypeSpace, Type, BeliefHierarchy, CommonKnowledge, PrivateSignal, Rationalizability.

18. Verification games and strategic temporal logic
    Classes:
    VerificationGame, StrategicFormula, TemporalProperty, ReachabilityProperty, SafetyProperty, LivenessProperty, ModelCheckingTask, CounterexampleTrace, WitnessStrategy.

19. Security games
    Classes:
    SecurityGame, StackelbergSecurityGame, CyberSecurityGame, Defender, Attacker, Target, AttackVector, CoverageSchedule, ThreatModel.

20. Differential, continuous-time, and hybrid games
    Classes:
    ContinuousTimeGame, DifferentialGame, StochasticDifferentialGame, HybridGame, ControlVariable, StateEquation, Hamiltonian, IsaacsCondition.

21. Congestion and routing games
    Classes:
    CongestionGame, RoutingGame, PotentialGame, Resource, ResourceEdge, LatencyFunction, NetworkFlow, WardropEquilibrium.

22. Game description languages and general game playing
    Classes:
    RuleEncodedGame, GameDescriptionLanguage, GDLGame, GDLII_Game, LudiiGame, RulePredicate, LegalMoveRule, TerminalRule, GoalRule, TransitionRule.

23. LLM-agent games
    Classes:
    LLMInteractionGame, LLMAgent, PromptState, ContextWindow, MemoryState, ToolInvocation, AgentMessage, AgentCapability, AgentProtocolSession, ConsentBoundary.

24. Digital-twin games
    Classes:
    DigitalTwinGame, DigitalTwin, Thing, InteractionAffordance, PropertyAffordance, ActionAffordance, EventAffordance, ProtocolBinding, CyberPhysicalState.

25. Compositional and open games
    Classes:
    OpenGame, CompositionalGame, Lens, StrategyLens, PlayFunction, CoplayFunction, EquilibriumPredicate, MonoidalComposition.

26. Petri-net, DEVS, and HLA interoperability
    Classes:
    PetriNetGame, PetriNet, Place, TransitionNode, Token, Marking, DEVSAtomicModel, DEVSCoupledModel, Federate, FederationObjectModel.

27. Trust, reputation, provenance, and auditability
    Classes:
    TrustRelation, ReputationScore, IdentityClaim, Credential, ProvenanceTrace, AuditEvent, ActionAttribution.

28. Privacy, disclosure, and strategic data sharing
    Classes:
    PrivacyBudget, PrivateAttribute, DisclosureAction, ConsentPolicy, InformationLeakage, DifferentialPrivacyMechanism.

29. Knowledge-graph execution bindings
    Classes:
    ExecutableGameGraph, ExecutionBinding, RuntimeBinding, SolverBinding, SimulationBinding, SPARQLExecutionQuery, ValidationShape, ConstraintViolation.

=====================================================================
SHACL REQUIREMENTS
=====================================================================

Create SHACL shapes that validate at least:

1. Every GameSpecification has at least one player.
2. Every GameInstance references exactly one GameSpecification.
3. Every PlaySession references one GameInstance.
4. Every StrategyProfile has at least one Strategy.
5. Every Outcome has at least one Payoff or explicit no-payoff marker.
6. Every StochasticGame has a TransitionFunction.
7. Every BayesianGame or EpistemicGame has a TypeSpace or InformationSet.
8. Every SecurityGame has at least one Defender, one Attacker, and one Target.
9. Every Mechanism has an AllocationRule and PaymentRule.
10. Every ContractGame has a Contract.
11. Every LLMAgent has a PromptState.
12. Every ToolInvocation has a ConsentBoundary or is explicitly marked as consent-not-required.
13. Every DigitalTwinGame has a DigitalTwin or RuntimeBinding.
14. Every PetriNet has at least one Place and one TransitionNode.
15. Every executable game has an ExecutionModel or RuntimeBinding.

=====================================================================
JSON-LD REQUIREMENTS
=====================================================================

Create:
- `jsonld/context.jsonld`
- `jsonld/core.context.jsonld`
- `jsonld/extensions.context.jsonld`

They must:
- Define compact aliases for core classes and properties.
- Use `@id` and `@type` correctly for object-valued properties.
- Support examples in `examples/*.jsonld`.
- Parse with rdflib.

=====================================================================
EXAMPLES REQUIREMENTS
=====================================================================

Create meaningful examples for:

1. Prisoner’s dilemma
2. Stag hunt
3. Normal-form game
4. Extensive-form game
5. First-price auction
6. Cooperative coalition game
7. Markov/stochastic game
8. MARL gridworld game
9. Signalling game
10. Voting/social choice game
11. Matching market
12. Principal-agent contract game
13. Stackelberg security game
14. LLM tool-use game
15. Digital-twin security game
16. Petri-net execution game

Each example should:
- Use the ontology classes and properties.
- Validate where applicable.
- Be small enough to understand.
- Include comments or labels.

=====================================================================
COMPETENCY QUESTIONS REQUIREMENTS
=====================================================================

Create SPARQL queries that answer:

1. Which players participate in a game?
2. Which strategies are available to each player?
3. Which equilibria are associated with a game?
4. Which games involve incomplete information?
5. Which security games have targets?
6. Which mechanisms have incentive-compatibility constraints?
7. Which LLM-agent games involve tool invocation?
8. Which executable games emit event traces?
9. Which games use privacy budgets or consent policies?
10. Which modules define which ontology classes?

Tests should execute these queries against the relevant example graphs where feasible.

=====================================================================
PYTHON TOOLING REQUIREMENTS
=====================================================================

Create `pyproject.toml` with dependencies:
- rdflib
- pyshacl
- pytest
- pyyaml
- ruff

Create scripts:

1. `scripts/build.py`
   - Merge all TTL files under `ontologies/` into `dist/uogto.ttl`.
   - Merge SHACL files into `dist/uogto-shapes.ttl`.
   - Copy JSON-LD contexts into `dist/`.
   - Print class/property counts.

2. `scripts/validate.py`
   - Parse all TTL files.
   - Parse all JSON-LD files.
   - Validate examples with SHACL.
   - Run basic SPARQL competency queries.
   - Exit nonzero on failure.

3. `scripts/report_coverage.py`
   - Count classes, object properties, datatype properties, SHACL shapes, examples, and competency queries by module.
   - Fail if a module is empty.
   - Report modules with fewer than expected definitions.

4. `scripts/conductor.py`
   - Read `.conductor/tasks.yaml`.
   - Print task status.
   - Show incomplete tasks.
   - Show expected outputs.
   - Support `--json`.

Create tests:
- `tests/test_parse_ttl.py`
- `tests/test_parse_jsonld.py`
- `tests/test_shacl_examples.py`
- `tests/test_competency_queries.py`
- `tests/test_coverage_thresholds.py`

Create `Makefile` targets:
- `make install`
- `make build`
- `make validate`
- `make test`
- `make coverage`
- `make conductor`
- `make all`

Create GitHub Actions workflow:
- `.github/workflows/validate.yml`
- Install Python dependencies.
- Run `make all`.

=====================================================================
DOCUMENTATION REQUIREMENTS
=====================================================================

Create `README.md` with:
- Project overview.
- Why UOGTO exists.
- Scope.
- Module map.
- Quickstart.
- Validation commands.
- Example usage.
- How to add a module.
- Licensing.
- Citation.

Create docs:
- `docs/architecture.md`
- `docs/ontology-design-principles.md`
- `docs/module-map.md`
- `docs/class-hierarchy.md`
- `docs/object-properties.md`
- `docs/data-properties.md`
- `docs/constraints-and-shacl.md`
- `docs/jsonld-bindings.md`
- `docs/examples.md`
- `docs/competency-questions.md`
- `docs/software-architecture-mapping.md`
- `docs/release-process.md`
- `docs/references.md`

The software architecture mapping should map ontology concepts to execution objects such as:

Ontology concept -> Software architecture object

GameSpecification -> GameSpec
GameInstance -> RuntimeGame
PlaySession -> SimulationRun
Player -> Agent
Strategy -> Policy
Action -> Command/Event
StrategyProfile -> JointPolicy
TransitionFunction -> EnvironmentDynamics
InformationSet -> ObservationModel
UtilityFunction -> RewardFunction
Equilibrium -> SolverResult
Mechanism -> AllocationEngine
Contract -> IncentiveContract
Norm -> RuleEngineConstraint
LLMAgent -> ToolUsingAgentRuntime
ToolInvocation -> CallableToolAction
PromptState -> AgentContextState
DigitalTwin -> CyberPhysicalRuntimeEntity
PetriNet -> DiscreteEventGraph
DEVSModel -> HierarchicalEventSimulator
ExecutionBinding -> RuntimeAdapter
SHACLShape -> ValidationContract
SPARQLQuery -> CompetencyTest

=====================================================================
LICENSING
=====================================================================

Use:
- CC-BY-4.0 for ontology content and documentation.
- MIT for code and scripts.

Create:
- `LICENSE` for ontology/docs.
- `LICENSE-CODE` for code.
- Mention dual licensing clearly in README.

If exact license text is not available locally, include clearly marked placeholders and a note in `.conductor/status.md` that license text should be verified before release.

=====================================================================
QUALITY GATES
=====================================================================

Before finishing, run:

python scripts/build.py
python scripts/validate.py
python scripts/report_coverage.py
pytest

Or, if Makefile is available:

make all

If a command fails:
- Fix the cause.
- Re-run the command.
- If a dependency is unavailable in the environment, document the exact command that failed and why in `.conductor/runlog.md`.

Definition of done:
- Repo scaffold exists.
- Conductor system exists.
- Core ontology exists and parses.
- Extension modules exist and parse.
- SHACL shapes exist and parse.
- JSON-LD contexts exist and parse.
- Examples exist and at least the core examples validate.
- Competency queries exist.
- Build script produces `dist/uogto.ttl` and `dist/uogto-shapes.ttl`.
- Validation script runs or documents environment limitations.
- README and docs exist.
- `.conductor/status.md` reports current status and next tasks.
- Final response summarizes files created, validation commands run, results, and remaining gaps.

=====================================================================
IMPLEMENTATION STYLE
=====================================================================

Prefer simple, maintainable code.
Use Python standard library where possible.
Use rdflib and pyshacl for RDF parsing and validation.
Do not generate enormous files; create concise but meaningful first versions.
Avoid duplicate class definitions unless intentionally imported or aligned.
Use stable IRIs.
Include ontology version metadata.
Use `owl:Ontology` declarations in major TTL files.
Use `skos:definition` for semantic clarity.
Use `rdfs:comment` sparingly for implementation notes.
Use `skos:scopeNote` for design limitations.

=====================================================================
START NOW
=====================================================================

First:
1. Inspect the empty repo.
2. Create the conductor system.
3. Create the repo scaffold.
4. Implement the first working ontology modules, examples, shapes, JSON-LD contexts, scripts, tests, and docs.
5. Run validation/build/test commands.
6. Update `.conductor/status.md` and `.conductor/runlog.md`.
7. Return a concise final summary with:
   - Files created
   - Commands run
   - Validation results
   - Known gaps
   - Recommended next Codex prompt
```

A good next prompt after Codex completes this bootstrap would be:

```text
Continue from the existing conductor system. Read AGENTS.md, CONDUCTOR.md, .conductor/tasks.yaml, .conductor/status.md, and .conductor/runlog.md. Then execute the next incomplete conductor phase. Use subagents if available, run validation, update status and runlog, and summarize results.
```

[1]: https://developers.openai.com/codex/prompting "Prompting – Codex | OpenAI Developers"
[2]: https://developers.openai.com/codex/concepts/subagents "Subagents – Codex | OpenAI Developers"

