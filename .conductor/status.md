# UOGTO Project Status

## Current State
- Repository scaffold successfully established.
- Conductor system (AGENTS.md, CONDUCTOR.md, tasks.yaml, status.md, runlog.md, module-template.md, scripts) configured.
- Core ontology modules implemented (`ontologies/core/`).
- Extension modules implemented (`ontologies/extensions/`).
- Alignments implemented (`ontologies/alignments/`).
- SHACL shapes, JSON-LD contexts, examples, and competency queries are created.
- Testing suite and CI configuration complete.
- Repository maintenance automation implemented (Pixi dependencies, remote issue checks, auto-changelogs, agent skills, and GitHub Actions).
- Conductor track/archive state normalized; superseded review planning is archived and active track metadata matches completed plans.
- CI maintenance workflow now supports Linux Pixi execution and opens pull requests for generated maintenance changes.
- Publishing and discoverability planning track added for Zenodo DOI archiving, WIDOCO/GitHub Pages documentation, LOV submission, and OLS indexing.
- Publishing metadata scaffolding implemented: `CITATION.cff`, `.zenodo.json`, v1.0 release notes, WIDOCO Pages workflow, LOV/OLS registry docs, and metadata checks.
- Registry annotation checks now validate the primary ontology release header for DCTERMS/VANN metadata and source module ontology labels.
- Scheduled maintenance now audits registry documentation links while allowing known unpublished v1.0 publication URLs until release.
- Release asset packaging now builds generated RDF, SHACL, JSON-LD context, checksum, and manifest files for attachment to the `v1.0.0` GitHub release.
- Conductor state reconciliation is recorded in `conductor_state_reconciliation_20260622`.
- SourceRight manuscript source verification is in progress: canonical CSL, sidecar, review queue, report artifacts, and manuscript citation plumbing are implemented; SourceRight citation-key detection remains open.

## Completed Modules
- All core and extension modules listed in tasks.yaml are completed.

## Known Gaps
- Zenodo account-side GitHub integration and DOI minting remain external release steps.
- WIDOCO Pages workflow is configured but still needs a successful GitHub Actions run after push.
- Published RDF artifact retrieval still needs verification after the `v1.0.0` release asset workflow runs.
- LOV submission and OLS indexing remain external registry steps after DOI and Pages documentation are live.
- SourceRight citation reconciliation currently detects 0 citation occurrences from the generated manuscript text export, despite canonical CSL coverage for the cited keys.
- The manuscript still lacks a dedicated LaTeX/PDF build command in the repository.

## Next Recommended Task
- Continue `uogto_publishing_discoverability_20260622` for live release gates and close SourceRight citation-detection/build-command gaps before treating the manuscript as publication-ready.

## Manuscript Source Verification - 2026-06-22
- Track: conductor/tracks/manuscript_source_verification_20260622/.
- SourceRight CSL validation passes for docs/paper/references.csl.json.
- SourceRight report is captured at docs/paper/sourceright-report.md with 36 references, 25 queued manual reviews, 0 unresolved reviews, and 0 provider conflicts.
- Open: SourceRight citation reconciliation output is captured at docs/paper/sourceright-citations.md but detects 0 citation occurrences; final manuscript source review and LaTeX build remain pending.
