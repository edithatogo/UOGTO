# Specification — semantic reconciliation and hardening

## Problem and scope

At `a5f90557c40f054255a1d6c2541fd76f07aa5090`, current validation accepts literal
players and out-of-range probabilities; the class hierarchy confuses computation
problems and allocation solutions with equilibria; runner predicates are undeclared;
the baseline player does not call a language model; and automatic lexical mapping
decisions assert unsafe equivalences. Existing reports describe an earlier snapshot.

The user authorizes correction of these defects, reconciliation with
[Paignia](https://github.com/edithatogo/paignia), and a source-grounded frontier plan.
Preserve published IRIs and distinguish corrected meaning from namespace migration.
Use focused semantic tests and normal repository CI, without adding human approval
steps to routine development. Independent research assessment is evidence for a
scientific claim, not a recurring development gate.

## Requirements

- Distinguish solution criteria, results, allocation results, equilibrium predicates,
  algorithms and computational problems; correct causal-equation direction.
- Declare the runner's existing vocabulary and preserve existing fixture behavior.
- Reject malformed player values and probability bounds with positive controls.
- Describe static/dynamic strategic structure separately from representation and
  runtime execution; normal form does not entail a static interaction.
- Identify graph inspection and first-action selection as reference tooling.
- Stop lexical prefill from publishing equivalence assertions; reject known false
  mappings and retain unresolved candidates without presenting them as accepted.
- Exercise an installed wheel outside the source checkout with declared dependencies.
- Reconcile current and historical evidence, Conductor status, source limitations
  and Paignia's actual source-transfer status.

## Acceptance and boundaries

Run focused tests, `make validate`, `make test`, and the proportionate release
checks. Record failures honestly and compare the exact changed head in hosted CI.
No Rust solver, external-engine adapter, exhaustive literature search, empirical
behavioral validity, package release or scientific frontier claim is established by
this correction track. Those outcomes require their own implementation evidence.

Rollback is a normal revert of the affected coherent change; retain old identifiers,
historical release artifacts and clearly dated research snapshots.
