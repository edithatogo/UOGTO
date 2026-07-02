# Expert Panel Review for arXiv Manuscript

Date: 2026-07-02

Scope: `docs/paper/paper.tex`, ontology-comparison artifacts, article-hardening artifacts, arXiv submission docs, and RI-HERO context.

## Reviewers

| Agent | Role | Status |
| --- | --- | --- |
| `019f20e4-4144-7601-9086-f966f8f1bbe3` (`Anscombe`) | Economist / game-theory reviewer | completed |
| `019f20e4-7802-7f80-9e41-95aeb2a81f48` (`Leibniz`) | Ontology / semantic-web reviewer | completed |
| `019f20e4-a510-7a80-bc2d-833d8a215a8e` (`Socrates`) | Systematic-review / methods reviewer | completed |
| `019f20e5-2ce4-7cc3-81aa-a8ec1335903e` (`Pascal`) | Preprint editor / publisher reviewer | completed |
| `019f20e5-cadb-70b3-a416-e1cb71bec621` (`Arendt`) | Health economics / outcomes reviewer | completed |
| `019f20e4-d208-7b13-906a-6a391c838c04` (`Mendel`) | Graph / network-analysis reviewer | timed out before final response |

## Consensus Fix-Now Findings

- Correct source-count denominators: the comparison uses 21 candidate sources across 17 source families, not 21 source families.
- Reframe "systematic search" as a structured scoping / PRISMA-ScR-style discovery workflow, not an exhaustive systematic review.
- Explain denominators: six inclusion-producing search records plus one negative-evidence route, 39 retained synthesis records, 21 candidate comparison sources, 17 source families, and 4,037 normalized term rows.
- Add inclusion/exclusion criteria, normalization/deduplication, screening status, and evidence-level summaries to the manuscript methods/results.
- Clarify that accepted mappings are conservative deterministic or pre-filled assertions subject to review, not fully independent expert-adjudicated mappings.
- Soften calibration/adjudication wording where artifacts are scaffolds or samples rather than completed agreement evidence.
- State that SHACL validation is selected example/shape validation, not comprehensive rich SHACL coverage for every module.
- Quantify competency-query coverage and list the main query families.
- Add one worked economics/game-theory example showing specification, instance, session/trace, mechanism, outcomes, and evidence separation.
- Interpret network centrality as centrality in the constructed evidence/mapping graph, not theoretical centrality in economics or ontology correctness.
- Remove or avoid repository process and slide/deck readiness content in the scientific manuscript.
- Add calibrated health economics/outcomes relevance through incentives, resource allocation, reimbursement/priority-setting, intervention uptake, policy response, and outcome attribution, without claiming UOGTO is a health-economics ontology.
- Expand limitations to include non-exhaustive search surfaces, English-language and repository-discoverability bias, standards-access restrictions, licence constraints, snapshot timing, and no dedicated HTA/outcomes systematic review.

## Applied Outcome

The manuscript was updated to address the consensus fix-now findings by:

- correcting denominator language in the abstract and mapping table;
- replacing unqualified systematic-search language with structured scoping-search language;
- adding evidence-level counts and denominator explanations;
- adding a first-price auction worked example;
- tightening SHACL, competency-query, mapping-calibration, and network-analysis language;
- adding graph/network methods;
- adding a Data and Code Availability section;
- removing deck/slide readiness from limitations;
- adding calibrated health economics/outcomes examples;
- extending the glossary with semantic-web terms.

## Deferred Items

- A fuller reproducible search appendix or table with route-level query strings and limitations.
- A compact comparison table against normal/extensive form notation, OpenSpiel/Gym-style environments, GDL/Ludii, mechanism-design formalisms, and ABM/ODD-style descriptions.
- A dedicated RI-HERO or health economics/outcomes extension or companion paper.
- Additional examples for economics-facing modules that are currently vocabulary or alignment surfaces.

## Rejected Scope Expansions

- Do not claim exhaustive systematic review of game theory.
- Do not claim UOGTO solves health economic evaluation, QALY estimation, HTA modelling, or outcomes evidence synthesis.
- Do not move arXiv submission contracts, agent-run details, dirty-tree evidence, or CI attestation details into the manuscript.
