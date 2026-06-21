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
- WIDOCO Pages workflow is green and GitHub Pages is enabled. Run `27911901116` built and deployed successfully for commit `8118694`, and `https://edithatogo.github.io/UOGTO/` returned HTTP 200 after deployment.
- GitHub release `v1.0.0` is published, release-assets run `27910615774` attached all expected artifacts, and the primary RDF asset is publicly retrievable.
- LOV submission and OLS indexing remain external registry steps after DOI metadata is live.
- DOI status monitoring is implemented with `make doi-status` for local placeholder consistency and `pixi run doi-status-live` for public Zenodo lookup.
- DOI recording is scripted with `python scripts/maintenance/record_zenodo_doi.py <doi>` to update release notes, registry packets, `CITATION.cff`, and `.zenodo.json` after Zenodo minting.
- Registry handoff packet generation is implemented with `make registry-packet`; it writes LOV/OLS submission metadata to `dist/registry-handoff.json` and preserves the pending DOI blocker until Zenodo metadata is recorded.
- SourceRight manuscript citation reconciliation now reports 11 citation occurrences, 11 matches, and 0 issues; the manuscript SourceRight manual review queue is empty.
- GitHub-owned Actions workflow pins have been updated to current Node 24-compatible major releases for checkout, Python setup, Java setup, Pages artifact upload, and Pages deploy.
- Strict manuscript PDF generation is covered by GitHub Actions run `27911901120`, which installed LaTeX and passed `make manuscript-pdf` for commit `8118694`.

## Next Recommended Task
- Continue `uogto_publishing_discoverability_20260622` for release, DOI, release-asset, LOV, and OLS live gates before treating the project as publication-ready.

## Manuscript Source Verification - 2026-06-22
- Track: conductor/tracks/manuscript_source_verification_20260622/.
- SourceRight CSL validation passes for docs/paper/references.csl.json.
- SourceRight report is captured at docs/paper/sourceright-report.md with 11 manuscript references, 0 queued manual reviews, 0 unresolved reviews, and 0 provider conflicts.
- SourceRight citation reconciliation output is captured at docs/paper/sourceright-citations.md with 11 citation occurrences, 11 matched citations, and 0 issues.
- Strict PDF generation passed remotely in GitHub Actions run `27911901120` for commit `8118694`; current local Windows machine still lacks a TeX engine, so local PDF compilation is not claimed.

## Publishing Live Verification - 2026-06-22
- Recorded `Validate UOGTO` GitHub Actions run `27911982989` passed for commit `c752125`.
- GitHub Pages is enabled and `ENABLE_PAGES_DEPLOY=true` is set. WIDOCO Pages run `27911982986` built and deployed successfully for commit `c752125`; `https://edithatogo.github.io/UOGTO/` returned HTTP 200 after deployment.
- GitHub release `v1.0.0` is published. Release-assets workflow run `27910615774` passed and attached all expected assets. WIDOCO Pages tag workflow run `27910615818` passed after rerun.
- Recorded post-manuscript-CI verification for commit `8118694`: `Validate UOGTO` run `27911901129` passed, `Build Manuscript PDF` run `27911901120` passed, `Build WIDOCO Pages` run `27911901116` passed and deployed, and the Pages root returned HTTP 200.
- Live DOI check still reports no locally recorded/public Zenodo DOI; registry handoff remains `pending_external_doi`.
- Open: Zenodo DOI has not surfaced publicly yet; LOV and OLS submission remain blocked on DOI metadata.
