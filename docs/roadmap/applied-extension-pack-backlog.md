# Applied Extension Pack Backlog

Applied packs are companion ontologies that import UOGTO and preserve the core separation between specification, instance, session, trace, strategy, action, payoff, and outcome. Each first slice must include one worked example, local SHACL constraints, competency-query expectations, source evidence, and an explicit non-import ledger.

| Pack | First worked example | Local concepts | Reused UOGTO boundary |
| --- | --- | --- | --- |
| Health economics and HTA | Payer adoption game for a cost-effective intervention | technology appraisal, willingness-to-pay threshold, budget impact | mechanism, players, strategy, payoff, outcome, evidence trace |
| Medical decision modelling | Shared treatment-choice game under uncertain response | treatment option, clinical state, adverse event, quality-adjusted outcome | information set, belief, action, transition, utility, outcome |
| Safety systems | Operator-controller coordination game around a safety barrier | hazard, barrier, safety constraint, incident evidence | rule, action, state, session, trace, outcome |
| Genomic policy | Data-access and disclosure game for genomic research | consent scope, genomic-data category, access condition, disclosure risk | institution, rule, privacy budget, strategy, payoff, provenance |

These packs must not redefine clinical, safety, or genomic standards. Their specifications should name candidate external vocabularies and defer assertions until domain review confirms the mapping.
