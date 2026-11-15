# Specification: Biomedical Registry Positioning

## Overview

This track converts the conditional BioPortal and OBO Foundry recommendations into a documented decision package. It tests whether UOGTO has a sufficiently specific biomedical scope or governance fit for either registry and preserves a clear defer/no-submit outcome when it does not.

## Requirements

- Assess BioPortal's scope, metadata expectations, and likely positioning for UOGTO.
- Assess OBO Foundry's governance and ontology-scope expectations for UOGTO.
- Reuse the accepted OLS biomedical relevance explanation without overstating UOGTO as a biomedical ontology.
- Produce a positioning note, evidence matrix, and explicit submit/defer/reject decision for each target.
- Define the metadata package that would be required if a future submission is approved.

## Out of Scope

- Submitting to BioPortal or OBO Foundry without an approved positioning decision.
- Adding biomedical domain classes to the shared UOGTO core solely for registry eligibility.
- Replacing the current conditional/no-priority decisions with unsupported acceptance claims.

## Acceptance Criteria

- BioPortal and OBO Foundry decisions are supported by current registry guidance and UOGTO scope evidence.
- The decision package distinguishes health-related applications from biomedical ontology governance.
- Any future submission prerequisites are recorded as actionable follow-up work.
- Manuscript and registry wording remains calibrated.
- `make build`, `make validate`, and `make test` pass.
