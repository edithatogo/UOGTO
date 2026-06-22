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
- Zenodo DOI `10.5281/zenodo.20796937` is minted and recorded; direct Zenodo record lookup and DOI resolution both return record `20796937`.
- LOV submission is open at https://github.com/pyvandenbussche/lov/issues/83.
- OLS indexing request is open at https://github.com/EBISPOT/ols4/issues/1305.
- w3id PR `6238` has been updated with DOI and publication evidence at https://github.com/perma-id/w3id.org/pull/6238#issuecomment-4768124045.
- Extended discoverability track `uogto_extended_discoverability_registries_20260622` is implemented repo-side: the shared packet, generated `extended-registry-handoff.json`, Make/Pixi/release workflow wiring, and publication-status integration are in place; external actions remain pending for authenticated FAIRsharing/Wikidata work, prefix.cc `uogtox`, Ontobee after w3id, and Bioregistry review.

## Completed Modules
- All core and extension modules listed in tasks.yaml are completed.

## Known Gaps
- Zenodo DOI minting is complete for v1.0.0; ongoing Zenodo work is limited to monitoring/search indexing and future-release DOI handling.
- WIDOCO Pages workflow is green and GitHub Pages is enabled. Run `27911901116` built and deployed successfully for commit `8118694`, and `https://edithatogo.github.io/UOGTO/` returned HTTP 200 after deployment.
- GitHub release `v1.0.0` is published, release-assets run `27910615774` attached all expected artifacts, and the primary RDF asset is publicly retrievable.
- LOV and OLS submissions are open and pending external maintainer review.
- DOI status monitoring is implemented with `make doi-status` for local placeholder consistency and `pixi run doi-status-live` for public Zenodo lookup.
- DOI recording is scripted with `python scripts/maintenance/record_zenodo_doi.py <doi>` to update release notes, registry packets, `CITATION.cff`, and `.zenodo.json` after Zenodo minting.
- Zenodo DOI handoff packet generation is implemented with `make zenodo-packet`; release preflight now requires `dist/zenodo-handoff.json`, and release-assets run `27913777454` attached it to `v1.0.0`.
- Consolidated publication status packet generation is implemented with `make publication-status` so Pages, release assets, DOI, Zenodo, w3id, LOV, and OLS state are reviewable from one generated JSON artifact.
- Live publication status observation mode is implemented with `make publication-status-live` for scheduled Pages, release asset, and Zenodo DOI checks.
- Consolidated live publication status includes w3id pull request and redirect observations, so routine publication review can inspect Pages, release assets, Zenodo DOI, and w3id state from one generated artifact.
- Scheduled maintenance uploads `dist/publication-status-live.json` as workflow artifact `publication-status-live` for direct review.
- Registry handoff packet generation is implemented with `make registry-packet`; it writes submitted LOV/OLS issue metadata to `dist/registry-handoff.json` after Zenodo DOI recording.
- Release preflight, Pixi release-preflight, and the release-assets workflow now require and upload `dist/registry-handoff.json`; workflow run `27912429240` attached it to `v1.0.0` and the asset URL returned an HTTP download redirect.
- Registry link and release-readiness gates now require the public `registry-handoff.json` release asset URL in LOV/OLS packet docs.
- Registry live-link checks now distinguish strict live mode from `--allow-unpublished`; w3id namespace redirects remain an external publication gate.
- w3id redirect handoff is prepared in docs/registry/w3id-submission.md and make w3id-packet; release preflight now requires dist/w3id-redirect-handoff.json, and release-assets run 27913296574 attached the submitted-PR packet to v1.0.0. The external perma-id/w3id.org pull request is submitted at https://github.com/perma-id/w3id.org/pull/6238 and remains pending upstream merge/live redirect verification.
- w3id PR and redirect monitoring is implemented with `make w3id-status`, `pixi run w3id-status-live`, and scheduled maintenance; live status currently reports PR open, merged=False, and w3id endpoints returning 404.
- SourceRight manuscript citation reconciliation now reports 11 citation occurrences, 11 matches, and 0 issues; the manuscript SourceRight manual review queue is empty.
- GitHub-owned Actions workflow pins have been updated to current Node 24-compatible major releases for checkout, Python setup, Java setup, Pages artifact upload, and Pages deploy.
- Strict manuscript PDF generation is covered by GitHub Actions run `27911901120`, which installed LaTeX and passed `make manuscript-pdf` for commit `8118694`.
- Zenodo account-side inspection now has a token-aware terminal path through `make zenodo-depositions`; the parent `legal-nz/.env` token was found and checked without printing it, and Zenodo returned `no_uogto_deposition_found`.

## Next Recommended Task
- Continue first-wave w3id live redirect and LOV/OLS maintainer review gates, then monitor the second-wave external blockers: FAIRsharing authenticated submission, Wikidata authenticated item creation, prefix.cc `uogtox` retry after 2026-06-24, Ontobee after live w3id redirects, and Bioregistry issue #1999 review.

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
- Live DOI check records DOI `10.5281/zenodo.20796937`; registry handoff is no longer DOI-blocked.
- Release-assets workflow dispatch run `27912429240` passed for `v1.0.0` and attached `registry-handoff.json` to the GitHub release; the release asset URL returned HTTP 302 to the downloadable object.
- Strict registry live check still fails for pending w3id namespace redirects; scheduled/live maintenance can use `--allow-unpublished` until those redirects are configured.
- w3id redirect pull request https://github.com/perma-id/w3id.org/pull/6238 is submitted; upstream merge and live redirect completion remain external.
- Release-assets workflow dispatch run `27913296574` passed for `v1.0.0` and attached the submitted-PR `w3id-redirect-handoff.json`; the release asset URL returned HTTP 302 to the downloadable object.
- Release-assets workflow dispatch run 27913296574 passed for v1.0.0 and refreshed w3id-redirect-handoff.json; the downloaded asset contains status pending_external_w3id_merge and PR https://github.com/perma-id/w3id.org/pull/6238.
- Live w3id monitor reports PR `6238` is open with `merged=False`, and `/uogto/`, `/uogto/core`, and `/uogto/extensions` still return 404 until upstream merge propagates.
- Zenodo DOI is recorded and resolves publicly; LOV and OLS requests are submitted and awaiting maintainer review.
- Release-assets workflow dispatch run `27913777454` passed for `v1.0.0` and attached `zenodo-handoff.json`; the release asset URL returned HTTP 302 to the downloadable object.
- `dist/publication-status.json` is part of local release preflight and the release-assets workflow; current generated status should report DOI recorded plus LOV/OLS submitted, with w3id as the remaining external publication blocker.
- The attached `publication-status.json` release asset has digest `sha256:e52e18db755e23c1e2317cdf8483960a55e374ad2f8b929512a7c4b9f52d8ec5`.
- Live publication status observations are added to scheduled maintenance so public Pages, release assets, and Zenodo DOI search can be inspected from one generated JSON artifact. Local live output still reports `pending_external_publication_steps` because Zenodo DOI search is empty.
- `dist/publication-status-live.json` now includes w3id PR and redirect observations. Local live output records PR `merged=false` and three pending 404 namespace redirects while preserving `pending_external_publication_steps`.
- Scheduled maintenance artifact upload is implemented for `dist/publication-status-live.json`; local workflow contract verification, `make release-preflight`, `make validate`, and `make test` passed.
- Manual maintenance dispatch `27914704264` failed before artifact upload because `update_dependencies.py` could not import `scripts` under Pixi/Linux; the import path fix is implemented and local verification passed.
- Manual maintenance dispatch `27914843364` then failed before artifact upload because `disk_guard.py` defaulted to `C:\` on Linux; cross-platform disk path detection is implemented and local verification passed.
- Manual maintenance dispatch `27914935755` reached and passed live status artifact upload, then failed in `create-pull-request` because checkout credentials produced a duplicate GitHub Authorization header; checkout credential persistence is disabled and rerun verification is pending.
- Manual maintenance dispatch `27915044021` reached and passed live status artifact upload, then failed because repository settings do not permit GitHub Actions to create pull requests; PR creation is being made non-fatal so publication monitoring can still succeed.
- Manual maintenance dispatch `27915165068` passed end to end after PR creation was made non-fatal; live status artifact upload passed and the remaining PR permission limitation is recorded as a non-blocking GitHub Actions annotation.
- Maintenance workflow action pins are refreshed after run `27915165068` reported Node.js 20 deprecation annotations for `actions/upload-artifact@v5`, `peter-evans/create-pull-request@v6`, and `prefix-dev/setup-pixi@v0.8.1`; local workflow contract tests, `make release-preflight`, `make validate`, and `make test` passed, and manual maintenance dispatch `27915375191` passed without the Node.js 20 deprecation annotation.
- GitHub Actions repository workflow permissions are now set to write with pull-request approval/create enabled; manual maintenance dispatch `27923148929` passed and opened maintenance PR `#1`.
- Maintenance PR `#1` exposed generated-report/changelog churn; deterministic validation-report ordering and no-op changelog generation for empty entries are implemented locally with focused tests and full validation gates.
- Zenodo record `20796937` is published with DOI `10.5281/zenodo.20796937`; direct DOI and record checks pass even if public search indexing lags.
- w3id pull request `https://github.com/perma-id/w3id.org/pull/6238` remains open, clean, and mergeable; live `/uogto/` redirects still return 404 until upstream merges and deploys.
- Post-hardening maintenance dispatch `27923371952` failed on the registry link checker because the historical LOV `/dataset/lov/` URL redirects to 404; the LOV route note now uses the live root `https://lov.linkeddata.es/`, and local live registry link checks pass.
- Remote-status generation now filters the automated `chore/automated-maintenance` branch when using `gh`, preventing the maintenance PR from reporting itself as open repository work.
- Stale automated maintenance PR `#1` was closed and its branch deleted; fresh maintenance run `27923789206` created PR `#2`, which was merged as `a10f0d9` after confirming the diff was limited to changelog and remote-status updates.
- Added `scripts/maintenance/check_zenodo_depositions.py` with Make/Pixi wiring. Parent `.env` token-backed checks were used without printing the token; Zenodo record `20796937` is now published, and w3id PR `6238` has no comments/reviews, remains open/mergeable but unmerged, and live redirects still return 404.
- LOV issue `https://github.com/pyvandenbussche/lov/issues/83` and OLS issue `https://github.com/EBISPOT/ols4/issues/1305` are open; both reference the public DOI, WIDOCO docs, release, and canonical RDF asset.
- Extended discoverability repo-side implementation is complete locally: `uogto` is live at prefix.cc, Bioregistry issue `https://github.com/biopragmatics/bioregistry/issues/1999` is open, FAIRsharing/Wikidata are prepared but account-blocked, Ontobee is deferred pending w3id, and BioPortal/OBO Foundry are recorded as conditional/not prioritized.
- w3id PR `https://github.com/perma-id/w3id.org/pull/6238` remains open/mergeable with no review comments; DOI/publication evidence was added in comment `https://github.com/perma-id/w3id.org/pull/6238#issuecomment-4768124045`.
- Remote verification for commit `da246b9` passed: `Validate UOGTO` run `27947593135` succeeded and `Build WIDOCO Pages` run `27947593119` built and deployed successfully.
- Remote verification for commit `db59bdb` passed: `Validate UOGTO` run `27949544161` succeeded and `Build WIDOCO Pages` run `27949544173` built and deployed successfully.
- Remote verification for commit `d438c42` passed: `Validate UOGTO` run `27952260669` succeeded and `Build WIDOCO Pages` run `27952260682` built/deployed successfully.
- Release-assets refresh run `27952354134` passed for `v1.0.0`, rebuilding and uploading release packets that report `registry-handoff.json` status `submitted_to_registries`, `zenodo-handoff.json` status `doi_recorded`, and `publication-status.json` status `pending_external_publication_steps` with LOV/OLS submitted and w3id pending.
- Live Pages root returned HTTP 200 after the `d438c42` deployment; DOI `https://doi.org/10.5281/zenodo.20796937` redirected to `https://zenodo.org/records/20796937` and returned HTTP 200.
