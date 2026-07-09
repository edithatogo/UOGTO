# UOGTO Field Expansion Roadmap

Date: 2026-07-09

This roadmap turns the open field-expansion issues into an implementation plan.
It preserves the manuscript rule that UOGTO should grow selectively: add a term
or pattern only when it improves reusable game semantics, validation coverage,
example clarity, or interoperability. Otherwise record the concept as an
external alignment, deferral, rejection, or domain-review item.

## Current Issue Map

| Issue | Track slice | Primary output | First validation gate |
| --- | --- | --- | --- |
| #76 | Field expansion umbrella | shared pattern, decision ledger, issue sequencing | roadmap documentation and Conductor track present |
| #77 | Mean-field games | worked population-state example, SHACL invariants, competency question | `make build`, `make validate`, focused CQ test |
| #78 | Network and congestion-routing games | route-choice or network-resource example, route/action checks | `make build`, `make validate`, focused CQ test |
| #79 | Evolutionary games | population/strategy-distribution/update-rule example | `make build`, `make validate`, focused CQ test |
| #80 | Institutional economics and information design | institutional-rule and signal/information example pair | `make build`, `make validate`, focused CQ test |
| #81 | Learning in games and MARL | agent-policy/observation/action/reward trace example | `make build`, `make validate`, focused CQ test |
| #82 | Trust, reputation, and provenance | evidence/reputation/signal game example reusing PROV externally | `make build`, `make validate`, focused CQ test |
| #83 | Applied extension packs | extension-pack pattern for local outcomes, risks, constraints, and evidence standards | manuscript-claim calibration and follow-up issue split |

## Shared Implementation Pattern

Each field-expansion slice should add the following artefacts before it claims
module maturity:

1. One worked example graph under `examples/`.
2. SHACL coverage for the example-specific invariants, preferably in an
   existing shape file unless a new domain shape file is justified.
3. One competency query plus an expected-result assertion.
4. Documentation explaining the game layer, instance/session/trace split, and
   evidence boundary.
5. A decision ledger row for concepts that were accepted, externally aligned,
   deferred, rejected, or sent to domain review.

## Decision Rules

- Keep the core game layer domain-neutral.
- Prefer example and validation coverage before new class/property expansion.
- Use existing UOGTO concepts when they already express the reusable game
  meaning.
- Use external alignments when a source term belongs to provenance, evidence,
  health, safety, genomics, or policy-specific semantics rather than game
  semantics.
- Preserve negative evidence so future maintainers can see why a plausible term
  was not asserted.

## Issue-Specific First Pass

### #77 Mean-Field Games

First example: a population routing or crowd-entry game with a representative
agent, population state, action/policy choice, aggregate state, cost/payoff,
outcome, session, and trace. The first pass should avoid importing the full
mean-field PDE vocabulary unless a term is needed to describe reusable game
structure.

### #78 Network and Congestion-Routing Games

First example: a two-route congestion game with players, network resources,
route actions, route costs, selected routes, outcome costs, session, and trace.
The route/action invariant is the main SHACL target.

### #79 Evolutionary Games

First example: a population game with strategy distribution, payoff surface,
selection or update rule, post-update outcome, and trace event. The first pass
should keep biological or epidemiological population semantics external unless
needed by the reusable game layer.

### #80 Institutional Economics and Information Design

First examples: one institutional rule setting and one signal/information
design setting. The examples should show institutions, rules, mechanisms,
signals, incentives, outcomes, and evidence traces without making the core
ontology a full institutional or information-economics ontology.

### #81 Learning in Games and MARL

First example: a multi-agent learning episode with observation, policy or
strategy, action, reward/payoff, outcome, session, and trace. Reuse OpenSpiel
and MARL source evidence where it supports interoperability, but keep
implementation-library details out of the shared ontology unless reusable.

### #82 Trust, Reputation, and Provenance

First example: a reputation-mediated trust game with claim/evidence records,
reputation signal or state, action, payoff/outcome, and provenance trace. PROV
terms should remain external alignments unless UOGTO needs a narrower
game-specific relation.

### #83 Applied Extension Packs

Applied packs should be companion layers, not changes to UOGTO core. A pack may
define local outcomes, risks, constraints, evidence standards, mappings, and
case-study examples for health economics, medical decision modelling, safety
systems, or genomic policy. The first pass should document the extension-pack
interface and create follow-up implementation issues only after the boundary is
clear.

## Validation

Every implementation PR spawned from this roadmap should run:

- `make build`
- `make validate`
- focused tests for new SHACL/CQ coverage
- `make test` before merge

