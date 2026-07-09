# Applied Extension Pack Pattern

Date: 2026-07-09

Applied extension packs let domain projects depend on UOGTO without turning the
shared ontology into a health, safety, genomics, or policy-specific vocabulary.

## Boundary

UOGTO should provide the shared game layer:

- game specification, instance, session, and trace;
- players or agents;
- actions, strategies, policies, observations, payoffs, outcomes, mechanisms,
  rules, and evidence links;
- mappings and provenance enough to audit game claims.

Applied packs should provide domain-local semantics:

- health-economic outcomes, utilities, adverse events, and resource measures;
- medical decision-model states, interventions, cohorts, and evidence grades;
- safety-system hazards, controls, incident evidence, and reporting standards;
- genomic-policy risks, consent constraints, disclosure events, and response
  categories.

## Pack Contents

Each applied pack should include:

1. A namespace separate from `uogto:` and `uogtox:`.
2. Domain-specific classes and properties only where UOGTO should not carry the
   domain burden.
3. Mappings from domain terms to UOGTO game-layer terms.
4. Worked examples showing how domain outcomes and evidence connect to game
   sessions and traces.
5. SHACL shapes for pack-specific constraints.
6. A decision ledger recording which concepts were kept in the pack, aligned
   externally, proposed for UOGTO, deferred, or rejected.

## Candidate First Examples

| Domain | Candidate example | UOGTO connection |
| --- | --- | --- |
| Health economics / HTA | reimbursement or uptake incentive game | mechanism, payoff, outcome, evidence trace |
| Medical decision modelling | diagnostic or treatment choice under information constraints | information state, action, outcome, trace |
| Safety systems | reporting or compliance game after a hazard signal | signal, rule, action, consequence, provenance |
| Genomic policy | disclosure or consent-response game | agent, information, constraint, action, outcome |

## First Gate

Before creating domain-pack implementation issues, record:

- the candidate namespace;
- the first worked example;
- which concepts belong in UOGTO versus the applied pack;
- which external ontologies or standards should be aligned rather than copied;
- the manuscript claim that the pack supports.

