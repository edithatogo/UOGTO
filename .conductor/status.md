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
- Local release preflight now validates generated release assets, metadata, release notes, registry packets, and expected external blockers before publication.
- Conductor state reconciliation is recorded in `conductor_state_reconciliation_20260622`.
- SourceRight manuscript source verification is complete: canonical CSL, sidecar, review queue, report artifacts, manuscript citation plumbing, local LaTeX citation-key checks, manuscript build readiness checks, and SourceRight numeric citation reconciliation are implemented.

## Completed Modules
- All core and extension modules listed in tasks.yaml are completed.

## Known Gaps
- Zenodo account-side GitHub integration and DOI minting remain external release steps.
- WIDOCO Pages workflow is green and GitHub Pages is enabled. Run `27910392764` deployed successfully, and both `https://edithatogo.github.io/UOGTO/` and `/index-en.html` returned HTTP 200.
- Published RDF artifact retrieval still needs verification after the `v1.0.0` release asset workflow runs.
- LOV submission and OLS indexing remain external registry steps after DOI and Pages documentation are live.
- SourceRight manuscript citation reconciliation now reports 11 citation occurrences, 11 matches, and 0 issues; the manuscript SourceRight manual review queue is empty.
- Strict manuscript PDF generation requires a release machine with `latexmk`, `tectonic`, or `pdflatex`; the repository now has `make manuscript-build` and `make manuscript-pdf` gates.

## Next Recommended Task
- Continue `uogto_publishing_discoverability_20260622` for release, DOI, release-asset, LOV, and OLS live gates before treating the project as publication-ready.

## Manuscript Source Verification - 2026-06-22
- Track: conductor/tracks/manuscript_source_verification_20260622/.
- SourceRight CSL validation passes for docs/paper/references.csl.json.
- SourceRight report is captured at docs/paper/sourceright-report.md with 11 manuscript references, 0 queued manual reviews, 0 unresolved reviews, and 0 provider conflicts.
- SourceRight citation reconciliation output is captured at docs/paper/sourceright-citations.md with 11 citation occurrences, 11 matched citations, and 0 issues.
- Open: strict PDF generation on a LaTeX-equipped release machine remains pending.

## Publishing Live Verification - 2026-06-22
- Latest `Validate UOGTO` GitHub Actions run `27910154892` passed for commit `000df52`.
- Latest `Build WIDOCO Pages` GitHub Actions run `27910154887` passed the build/artifact job for commit `000df52`; deploy was skipped because `ENABLE_PAGES_DEPLOY` is not set to `true`.
- GitHub Pages is enabled and `ENABLE_PAGES_DEPLOY=true` is set. WIDOCO Pages run `27910392764` deployed successfully; root and `/index-en.html` returned HTTP 200.
- Open: create `v1.0.0`, then verify Zenodo DOI, uploaded release assets, LOV, and OLS.
