# Semantic reconciliation and migration — 8 November 2026

This change corrects reproduced semantic and tooling defects, records source gaps,
and binds future executable work to [Paignia](https://github.com/edithatogo/paignia).
The audit baseline is `a5f90557c40f054255a1d6c2541fd76f07aa5090`.
The related Paignia ownership work in PR #126 is now on upstream `main`; the
strategic-information proposal from PR #125 is incorporated in this branch.
Historical source and publication evidence retains its original scope and date.

## Corrected semantics

| Concern | Reconciled treatment | Compatibility implication |
| --- | --- | --- |
| Computation versus result | `EquilibriumComputationProblem` is a `ComputationalProblem` | It no longer entails an equilibrium instance |
| Criterion versus result | `SolutionConcept` describes a criterion; `GameSolution` describes a result; `EquilibriumPredicate` is a solution concept | Consumers relying on the old equilibrium subclass entailment must update |
| Allocation and bargaining | `AllocationSolution` is a game solution; Shapley, core and bargaining results use that branch | Allocation results are not universally equilibrium profiles |
| Structural equations | Definition determines an endogenous variable from causal parents and exogenous factors | Corrects reversed causal wording; the IRI remains stable |
| Runner predicates | Existing action-space, action, player and legacy payoff links are declared and annotated | Existing predicate IRIs are preserved |
| Probability | Finite numeric values in `[0, 1]`; double-only OWL range removed | Decimal, integer, float and double controls can pass; nonnumeric, nonfinite and out-of-range values fail SHACL |
| Player references | Supplied `hasPlayer` values must be resources | Literal identifiers must become IRIs or blank nodes; this does not require every partial description to be executable |

Published core and extension namespaces remain unchanged. These are semantic
corrections, so preserved IRIs do **not** mean unchanged entailments. A release
must include these notes and the tested downstream compatibility matrix.

The aggregate JSON-LD context already uses `hasActionSpace` for the extension
predicate. It keeps that meaning. Use `coreHasActionSpace` for the core predicate,
or the full core IRI; the core-only context retains its core short name. The two
predicates are not declared equivalent merely because their local names match.

## Strategic time, representation and execution

`ontologies/core/temporality.ttl` adds `StaticGame`, `DynamicGame`,
`GameRepresentation`, `NormalFormRepresentation`, `ExtensiveFormRepresentation`
and `hasRepresentation`. A specification can have several representations.
Static and dynamic classifications are disjoint **at the same modelling scope**;
a static stage and the repeated game containing it should have separate identities.

| Model | Strategic structure | Possible representation | Execution implication |
| --- | --- | --- | --- |
| One-shot simultaneous pricing | Static | Normal form, or an extensive form hiding earlier choices | Software may collect choices serially |
| Sequential bargaining | Dynamic | Extensive form or complete contingent strategies in normal form | An offline solver can analyse it |
| Repeated simultaneous pricing | Dynamic overall; simultaneous within stages | Stage structure and/or contingent strategy representation | A parallel API alone does not establish strategic timing |
| Stochastic multi-agent environment | Dynamic when later choices depend on evolving information | State transitions, histories and information structure | A simulator supplies trajectories only if actually invoked |

The new example and CQ21 demonstrate these independent classifications. They are
descriptive evidence: the example does not encode a complete extensive tree or
normal-form payoff tensor and does not establish solver compatibility.

The pre-existing SGC term **static semantic acceptance** means interchange checked
without live simulation. It is independent of the new `StaticGame` class. A
`DynamicGame` may satisfy an offline semantic contract. Conversely, labelling a
specification `DynamicGame` proves no native simulation execution.

## Tooling and alignment interpretation

`RDFGameRunner` performs reference graph inspection and stored-payoff lookup.
`FirstActionPlayer` and `FirstActionPlayerBench` identify the deterministic baseline
accurately. `LLMPlayer` and `LLMPlayerBench` remain compatibility aliases; those
names do not imply a model request. Session output records execution and payoff
origins and whether a model or native solver was invoked. Existing TSV inspection
output remains machine-readable.

The installed-wheel smoke test now runs outside the checkout, imports from the
wheel installation under isolated Python, and explicitly supplies the installed
declared dependency closure. This verifies the wheel's package contents and import
origin; it is not evidence of a fresh online dependency resolution on every OS.

Lexical matching now proposes candidates only. Four pre-existing structural
`skos:narrowMatch` mappings remain accepted, six unsupported equivalence decisions
return to `needs_domain_review`, and two mismatches are rejected. In particular,
`owl:Thing` is not equivalent to UOGTO's physical-device `Thing`, and SOSA's
observed-property relation does not mean an agent's observation of a state or
signal. Exports require explicit scoped evidence for accepted equivalences.
Internal structural checks are labelled as such, without implying external review.

Optional PNG/PDF rendering prefers a working Inkscape or ImageMagick renderer.
Canonical SVG remains available if derivative tools cannot render it; that outcome
does not certify the missing derivative. The renderer regression covers an
installed ImageMagick lacking its SVG delegate.

## Evidence snapshots

- [Current semantic quality](quality/current-semantic-quality.md) is regenerated
  from the reconciled ontology, shapes, examples and competency queries. Its local
  OWL RL check and syntactic profile screen are not formal OWL DL certification.
- [Current mapping report](ontology-comparison/report.md) uses corrected decisions
  over the retained comparison corpus: 21 source records, 460 candidates and four
  accepted mappings. It does not mean the November discovery register was ingested
  into that historical term corpus.
- Prior calibration/robustness outputs retain their earlier scaffold inputs: the
  inspected calibration sample has zero rows and the robustness sample has two.
  The live `article-tables` and `article-facing-tables` compilations are regenerated:
  their SSSOM row now reports four current mappings, while other rows retain the
  dates and limits of their underlying sources. The frozen manuscript retains its
  earlier twelve-mapping snapshot. These mixed-date compilations do not validate
  the corrected mappings or demonstrate independent agreement.
- [The November source audit](research/game-semantics-source-audit-20261108.md)
  adds twenty targeted comparator records and documents acquisition limitations.
  It does not establish exhaustive coverage or twenty executed integrations.

Positive example conformance checks the constraints actually written. It does
not prove complete class coverage, game-theoretic correctness, numerical validity,
causal identification or general solver accuracy. Current test results and any
remaining failures belong in the reconciliation track's metadata and run log.

## Ownership and remaining work

| Component | Owner | Boundary |
| --- | --- | --- |
| Mathematical terms, source lineage, profiles and reference fixtures | UOGTO | Language-neutral semantics and conformance |
| Rust representations, strategic algorithms, solver results and adapters | Paignia | Actual numerical execution and versioned interchange |
| Optional event/time simulation and native traces | Kairos | Needed for claimed native execution, not for every game analysis |
| Empirical payoffs, policy choices and application validity | Domain application | Assumptions must accompany results |
| Strategic information valuation | Paignia and Voiage at their documented boundary | Reuse the existing SGC proposal and application handoffs |

Paignia's inspected bootstrap at
`0e28f1bf33ed8c7be5fa1d63b8cc40517b61d22c` records the planned transfer from
`new-drug-reimbursement-game`; that README is not a package qualification receipt.
Bind an actual transferred revision and its artifacts before claiming compatibility.
Do not duplicate the Rust implementation in UOGTO or require a default Kairos
dependency for offline solving. Paignia PR #1 separately owns its Voiage handoff.

The source audit exposes further modelling decisions, including perfect/imperfect
information as game properties versus individual information sets, behavioural
strategy distributions, history versus state, chance normalisation and reward
aggregation. These need source charting and scoped executable profiles. They remain
visible in the coverage and semantic-contract tracks rather than being silently
declared solved by new labels.

See the [frontier programme](roadmap/frontier-programme-20261108.md) and
[Conductor registry](../conductor/tracks.md) for dependencies and acceptance evidence.
