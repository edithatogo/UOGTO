# Specification

## Objective

Implement repository-side handoff packages for BARTOC and Research Vocabularies Australia using the stable UOGTO release, namespace, documentation, DOI, license, and sole-author metadata.

## Requirements

- Provide a human-readable handoff document for each target.
- Preserve the published `uogto` core and `uogtox` extension namespace distinction.
- Include stable release, RDF, documentation, DOI, license, and ORCID evidence.
- Include target-specific submission guidance and the external evidence required for closeout.
- Extend the generated registry handoff packet and regression tests.
- Do not represent local preparation as external submission, acceptance, or publication.

## Acceptance

- BARTOC and RVA targets are present in `dist/extended-registry-handoff.json`.
- Focused handoff tests pass.
- `make validate` passes.
- Remaining external steps are recorded in GitHub issues #98 and #99.
