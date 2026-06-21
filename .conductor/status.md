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
- Zenodo DOI handoff packet generation is implemented with `make zenodo-packet`; release preflight now requires `dist/zenodo-handoff.json`, and release-assets run `27913777454` attached it to `v1.0.0`.
- Consolidated publication status packet generation is implemented with `make publication-status` so Pages, release assets, DOI, Zenodo, w3id, LOV, and OLS state are reviewable from one generated JSON artifact.
- Live publication status observation mode is implemented with `make publication-status-live` for scheduled Pages, release asset, and Zenodo DOI checks.
- Consolidated live publication status includes w3id pull request and redirect observations, so routine publication review can inspect Pages, release assets, Zenodo DOI, and w3id state from one generated artifact.
- Scheduled maintenance uploads `dist/publication-status-live.json` as workflow artifact `publication-status-live` for direct review.
- Registry handoff packet generation is implemented with `make registry-packet`; it writes LOV/OLS submission metadata to `dist/registry-handoff.json` and preserves the pending DOI blocker until Zenodo metadata is recorded.
- Release preflight, Pixi release-preflight, and the release-assets workflow now require and upload `dist/registry-handoff.json`; workflow run `27912429240` attached it to `v1.0.0` and the asset URL returned an HTTP download redirect.
- Registry link and release-readiness gates now require the public `registry-handoff.json` release asset URL in LOV/OLS packet docs.
- Registry live-link checks now distinguish strict live mode from `--allow-unpublished`; w3id namespace redirects remain an external publication gate.
- w3id redirect handoff is prepared in docs/registry/w3id-submission.md and make w3id-packet; release preflight now requires dist/w3id-redirect-handoff.json, and release-assets run 27913296574 attached the submitted-PR packet to v1.0.0. The external perma-id/w3id.org pull request is submitted at https://github.com/perma-id/w3id.org/pull/6238 and remains pending upstream merge/live redirect verification.
- w3id PR and redirect monitoring is implemented with `make w3id-status`, `pixi run w3id-status-live`, and scheduled maintenance; live status currently reports PR open, merged=False, and w3id endpoints returning 404.
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
- GitHub release `v1.0.0` was refreshed by workflow run `27912459022`, which uploaded `registry-handoff.json`.
- Recorded post-manuscript-CI verification for commit `8118694`: `Validate UOGTO` run `27911901129` passed, `Build Manuscript PDF` run `27911901120` passed, `Build WIDOCO Pages` run `27911901116` passed and deployed, and the Pages root returned HTTP 200.
- Live DOI check still reports no locally recorded/public Zenodo DOI; registry handoff remains `pending_external_doi`.
- Release-assets workflow dispatch run `27912429240` passed for `v1.0.0` and attached `registry-handoff.json` to the GitHub release; the release asset URL returned HTTP 302 to the downloadable object.
- Strict registry live check still fails for pending w3id namespace redirects; scheduled/live maintenance can use `--allow-unpublished` until those redirects are configured.
- w3id redirect pull request https://github.com/perma-id/w3id.org/pull/6238 is submitted; upstream merge and live redirect completion remain external.
- Release-assets workflow dispatch run `27913296574` passed for `v1.0.0` and attached the submitted-PR `w3id-redirect-handoff.json`; the release asset URL returned HTTP 302 to the downloadable object.
- Release-assets workflow dispatch run 27913296574 passed for v1.0.0 and refreshed w3id-redirect-handoff.json; the downloaded asset contains status pending_external_w3id_merge and PR https://github.com/perma-id/w3id.org/pull/6238.
- Live w3id monitor reports PR `6238` is open with `merged=False`, and `/uogto/`, `/uogto/core`, and `/uogto/extensions` still return 404 until upstream merge propagates.
- Open: Zenodo DOI has not surfaced publicly yet; LOV and OLS submission remain blocked on DOI metadata.
- Release-assets workflow dispatch run `27913777454` passed for `v1.0.0` and attached `zenodo-handoff.json`; the release asset URL returned HTTP 302 to the downloadable object.
- `dist/publication-status.json` is now part of local release preflight and the release-assets workflow. Release-assets run `27914117992` attached it to `v1.0.0`; the asset URL returned HTTP 302 and the downloaded packet contains `pending_external_publication_steps` with DOI-blocked LOV/OLS states.
- The attached `publication-status.json` release asset has digest `sha256:e52e18db755e23c1e2317cdf8483960a55e374ad2f8b929512a7c4b9f52d8ec5`.
- Live publication status observations are added to scheduled maintenance so public Pages, release assets, and Zenodo DOI search can be inspected from one generated JSON artifact. Local live output still reports `pending_external_publication_steps` because Zenodo DOI search is empty.
- `dist/publication-status-live.json` now includes w3id PR and redirect observations. Local live output records PR `merged=false` and three pending 404 namespace redirects while preserving `pending_external_publication_steps`.
- Scheduled maintenance artifact upload is implemented for `dist/publication-status-live.json`; local workflow contract verification, `make release-preflight`, `make validate`, and `make test` passed.
- Manual maintenance dispatch `27914704264` failed before artifact upload because `update_dependencies.py` could not import `scripts` under Pixi/Linux; the import path fix is implemented and local verification passed.
- Manual maintenance dispatch `27914843364` then failed before artifact upload because `disk_guard.py` defaulted to `C:\` on Linux; cross-platform disk path detection is implemented and local verification passed.
- Manual maintenance dispatch `27914935755` reached and passed live status artifact upload, then failed in `create-pull-request` because checkout credentials produced a duplicate GitHub Authorization header; checkout credential persistence is disabled and rerun verification is pending.
- Manual maintenance dispatch `27915044021` reached and passed live status artifact upload, then failed because repository settings do not permit GitHub Actions to create pull requests; PR creation is being made non-fatal so publication monitoring can still succeed.
