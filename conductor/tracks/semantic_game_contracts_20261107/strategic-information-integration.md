# Strategic-information semantic profile and conformance

Date: 8 November 2026. Status: planning addition; implementation and qualification
remain pending. No ontology/runtime implementation or new IRI is claimed. Existing
SGC.01–SGC.08 and interoperability owners remain responsible; this is not a separate
scientific-ecosystem track or solver project.

## Parallel-owner reconciliation

Read the [shared reconciliation](https://github.com/edithatogo/paignia/blob/87b4bda345b85310e85239d4845b0f85bf1c6439/docs/integrations/parallel-plan-reconciliation-20261108.md)
and [PR #126](https://github.com/edithatogo/UOGTO/pull/126), which retains the eight
SGC leaves. UOGTO owns ontology, executable profiles and conformance fixtures;
Paignia owns the optional Rust mapping and numerical methods. Paignia #2 merged
a bounded core/solve seed, not a qualified general solver or semantic adapter.
Preserve canonical full IRIs, legacy full-IRI mappings and source-specific
CC-BY-4.0/MIT provenance where applicable; reject namespace collisions and unknown
terms rather than silently normalising them. No ontology asset is forked here.

Static SGC.08 acceptance uses version-matched SGC.01–SGC.05 evidence and does not
wait for optional dynamic SGC.06. Voiage-specific requirements below qualify only
this optional strategic-information composition, not every static semantic
consumer. Semantic conformance, Rust execution and numerical validity remain
separate. The owner PR and this supplement retain their disjoint source scopes;
these references do not change dependency pins or task status.

## Scope

Map the existing executable game subset to the game provider's response evidence
and Voiage's finite signed-information/paired-outcome contracts. UOGTO describes
meaning and validates the declared profile; it cannot certify numerical equilibrium
correctness, causal effectiveness or Rust-native execution merely from RDF labels.

Preserve specification, instance, play-session, policy and event-trace identities,
full existing IRIs, scoped players/actions and payoff ownership. Analyst uncertainty,
within-game state/type, signal realization, simulation replication and solver run
must not be conflated. Static semantic acceptance remains independent of Kairos;
dynamic trace claims additionally need SGC.06 and qualified native dispatch.

## Pending refinements within the current semantic leaves

- [ ] SGC.01–02: inventory existing terms and write a field-level compatibility map
  for public/private observation, recipients, timing, information sets, commitment,
  solution concept, selection rule/catalogue coverage and result provenance.
  Reuse terms where adequate; propose a separately reviewed extension only for a
  demonstrated gap. Do not invent published IRIs in consumer code.
- [ ] SGC.03–04: add closed-world profile negatives for foreign player/world IDs,
  private-to-public signal promotion, nonanticipative-policy violations, ambiguous
  selection, mixed/CE/Bayesian concept substitution and incomplete-catalogue claims.
  Semantic validation must not tighten the whole open-world ontology silently.
- [ ] SGC.05: check semantic round trips across Turtle, JSON-LD and actual Rust
  interchange. Preserve ordering, weights, observation scope and valued-outcome
  metadata; a successful Python reference round trip is not a Rust consumer receipt.
- [ ] SGC.06–07: distinguish solver analysis from selected-policy causal execution,
  and Python/reference origin from native execution. Unsupported concepts, unknown
  versions and missing native evidence remain explicit; no reference fallback is success.
- [ ] SGC.08: for this optional integration, bind the selected profile and artifacts
  to the exact provider and Voiage consumer versions. Keep semantic, numerical,
  static and dynamic acceptance separate; do not close the whole track from one
  profile-specific receipt or make this integration a universal SGC.08 prerequisite.

## Competency questions and test cases

Which actor received which signal, at what decision point, under which information
regime? Which policy/solution concept and selection rule generated a valued outcome?
Was the trace a solver diagnostic or a native play session? Which worlds and draws
were paired, and what objective/perspective and transfer convention was evaluated?

Use small finite fixtures: indistinguishable hidden states, swapped payoff owners,
two coordination equilibria with explicit catalogue scope, negative signed outcomes,
foreign session IDs, invalid distributions and unsupported solver claims. SHACL
validates profile invariants; reference equations/provider tests establish numerical
claims. A graph saying 'Bayesian equilibrium' does not implement its solver.

Before implementation, bind actual term and shape/query paths, versioning and focused
failure tests in the existing leaf. Add shapes/examples/competency queries together,
run make validate and make test, and update .conductor/status.md/runlog.md with actual
results. This planning note does not claim those runs, change published namespaces,
mark leaves complete or modify ontology, generated artifacts, dependencies or pins.

## Coordinated Voiage plan

See the [shared SI01–SI04 plan and SI-V01–SI-V08 cases](https://github.com/edithatogo/voiage/blob/c414752a228e7af5d689d9d5876f8f7372c42447/conductor/tracks/scientific_ecosystem_alignment_20261029/strategic-information-integration.md).
That source commit is a planning proposal, not a dependency pin or an acceptance receipt.
