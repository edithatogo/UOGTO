# Conductor Run Log

## [2026-06-24] - Wikidata Live Submission and FAIRsharing Recheck
- Used Chrome with the authenticated Wikidata session to search for `Universal Open Game Theory Ontology`; no duplicate item was found before creation.
- Created Wikidata item https://www.wikidata.org/wiki/Q140323510.
- Added and verified statements: instance of ontology (`Q324254`), DOI `10.5281/zenodo.20796937`, official website `https://edithatogo.github.io/UOGTO/`, source code repository URL `https://github.com/edithatogo/UOGTO`, and copyright license Creative Commons Attribution 4.0 International (`Q20007257`).
- Verified live page health in Chrome for the Wikidata item, Zenodo record, UOGTO documentation site, and GitHub repository.
- Created FAIRsharing draft record https://fairsharing.org/8382 through the authenticated FAIRsharing/GitHub workflow.
- Populated FAIRsharing metadata for record name, abbreviation, homepage, year `2026`, country `Australia`, status `Ready`, registry type `Standard / Terminology Artefact`, contact `Dylan Mordaunt`, taxonomic range `Not Applicable`, subject `Knowledge And Information Systems`, domain `Knowledge Representation`, object type `Dataset`, tags `Semantic Web` and `Ontology`, CC-BY-4.0 licence, GitHub support link, documentation support link, and Zenodo DOI support link.
- Persisted FAIRsharing required `data processes and conditions` metadata using `read` / `User interface`, documentation URL `https://edithatogo.github.io/UOGTO/`, and canonical RDF example URL `https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/uogto.ttl`.
- Verified the public FAIRsharing page now reports `This record is awaiting review by FAIRsharing curators`; recommended-but-nonblocking gaps remain organisation links, publications, citations, and record associations.

## [2026-06-23] - Registry Follow-Up Remote Verification
- Pushed commit `24b9601` and verified remote `Validate UOGTO` run `28023497374` plus `Build WIDOCO Pages` run `28023497352` passed.
- Dispatched `Publish Release Assets` run `28023545152`; it passed release gates, rebuilt registry/w3id/publication packets, passed release preflight, and uploaded assets to `v1.0.0`.
- Downloaded refreshed release packets and verified `extended-registry-handoff.json` reports only FAIRsharing/Wikidata blockers with digest `sha256:07c9e9e66b69582065b97c01fa61df05ad6da8c04ff39a51069e0b70c9f93081`.
- Downloaded refreshed `w3id-redirect-handoff.json` and verified status `live_redirects_verified`, empty blockers, merged_at `2026-06-22T12:29:07Z`, and digest `sha256:82ea92c3fb8465a6bd97dfdfc51545b4e24e08d56ed2e4e7d1b26bd8a58a48ca`.
- Downloaded refreshed `publication-status.json` and verified status `pending_external_publication_steps`, w3id `live_redirects_verified`, blockers only for FAIRsharing/Wikidata, and digest `sha256:f4ad2c38e8af6e9d8659246f2d8714966a9c9dbfdefa0dfb58d14639fb67caa4`.
## [2026-06-23] - Extended Discoverability Registry Implementation
- Implemented the shared second-wave registry packet in `docs/registry/extended-discoverability-submissions.md` and `scripts/maintenance/build_extended_registry_handoff.py`.
- Wired `dist/extended-registry-handoff.json` into Make, Pixi, publication-status generation, release-readiness checks, and the `Publish Release Assets` workflow.
- Submitted `uogto` to prefix.cc and verified the live mapping at http://prefix.cc/uogto.file.txt; `uogtox` remains blocked by prefix.cc's one-per-day contribution limit until after 2026-06-24.
- Opened Bioregistry request https://github.com/biopragmatics/bioregistry/issues/1999 after confirming no existing UOGTO issue.
- Recorded FAIRsharing and Wikidata as prepared but blocked by authenticated account workflows, Ontobee as deferred pending live w3id redirects, BioPortal as conditional/not submitted, and OBO Foundry as not prioritized.
- Local gates passed after implementation: `make release-preflight`, `make validate`, and `make test` (108 passed).
- Pushed implementation commit `8b52503`; remote `Validate UOGTO` run `27960976638` passed and `Build WIDOCO Pages` run `27960977018` passed/deployed.
- Dispatched `Publish Release Assets` run `27961110915`; it passed release gates, built `extended-registry-handoff.json`, passed release preflight, and uploaded the asset to `v1.0.0`.
- Verified the release asset URL returns schema `uogto.extended-registry-handoff.v1`, status `external_actions_pending`, prefix.cc status `partial`, Bioregistry issue `https://github.com/biopragmatics/bioregistry/issues/1999`, and digest `sha256:31e4e76ab2334ce9b92b87fa6e5bb63a0e6f7b5094d242460ae65b37498b0018`.

## [2026-06-22] - Extended Discoverability Track Creation
- Created Conductor track `uogto_extended_discoverability_registries_20260622`.
- Incorporated second-wave recommendations into the track plan: FAIRsharing, prefix.cc, Wikidata, Ontobee feasibility, conditional BioPortal, conditional Bioregistry, and OBO Foundry as not prioritized unless UOGTO is repositioned for biological or biomedical ontology governance.
- Registered the track in `conductor/tracks.md` and updated Conductor status so future `$conductor-status` reports the second-wave discoverability lane.

## [2026-06-22] - DOI Publication and Registry Submission
- Published Zenodo record `20796937` for UOGTO v1.0.0 release assets and recorded DOI `10.5281/zenodo.20796937`.
- Verified `https://zenodo.org/api/records/20796937` returns the expected UOGTO title/DOI and `https://doi.org/10.5281/zenodo.20796937` resolves to the Zenodo record.
- Added direct Zenodo record fallback to `check_doi_status.py` so strict DOI checks pass even before Zenodo search indexing catches up.
- Confirmed upstream w3id PR `6238` has no comments or reviews to address, remains open, and is mergeable.
- Added DOI/publication evidence to w3id PR `6238`: https://github.com/perma-id/w3id.org/pull/6238#issuecomment-4768124045.
- Confirmed no existing UOGTO LOV issue, then opened LOV submission issue https://github.com/pyvandenbussche/lov/issues/83.
- Confirmed no existing UOGTO OLS issue, inspected the current OLS new-ontology template, then opened OLS indexing issue https://github.com/EBISPOT/ols4/issues/1305.
- Updated release notes, registry docs, metadata checklist, generated handoff semantics, and publication status semantics so DOI, LOV, and OLS are no longer reported as blocked.
- Remaining external publication blocker is upstream w3id merge and live redirect propagation.
- Pushed commit `d438c42`; remote `Validate UOGTO` run `27952260669` passed and `Build WIDOCO Pages` run `27952260682` passed/deployed.
- Dispatched release-assets refresh run `27952354134` for `v1.0.0`; it passed release gates, rebuilt registry/Zenodo/w3id/publication-status packets, ran release preflight, and uploaded assets to the GitHub release.
- Downloaded refreshed release packets and verified `registry-handoff.json` status `submitted_to_registries`, `zenodo-handoff.json` status `doi_recorded`, `publication-status.json` status `pending_external_publication_steps`, LOV status `submitted`, OLS status `submitted`, and w3id status `pending_external_w3id_merge`.
- Verified live Pages root returned HTTP 200 and DOI `https://doi.org/10.5281/zenodo.20796937` resolves to Zenodo record `20796937` with HTTP 200.

## [2026-06-22] - Live Publication Status Artifact Upload
- Enabled GitHub Actions workflow write permissions and PR create/approve capability for `edithatogo/UOGTO`.
- Verified the repository setting reports `default_workflow_permissions=write` and `can_approve_pull_request_reviews=true`.
- Manual maintenance dispatch `27923148929` passed end to end and created `https://github.com/edithatogo/UOGTO/pull/1`.
- Reviewed maintenance PR `#1`; it contained remote-status refresh, validation report row reordering, and a no-op changelog entry.
- Hardened maintenance generation by sorting validation-report input file discovery and skipping changelog writes when there are no categorized changes.
- Verified focused maintenance tests, `make release-preflight`, `make validate`, and `make test` after the churn hardening.
- Refreshed Zenodo public search for `UOGTO`; it returned zero records, so there is still no DOI to record.
- Refreshed w3id PR state; PR `6238` is open, clean, and mergeable, with live w3id redirects still pending upstream merge.
- Attempted Chrome browser-control setup for account-side Zenodo inspection, but the Chrome runtime bridge failed before a browser session could start; repo/API-backed checks continued.
- Post-hardening maintenance dispatch `27923371952` failed at `Check Registry Documentation Links` because `http://lov.okfn.org/dataset/lov/` redirects to `https://lov.linkeddata.es/dataset/lov/`, which returns 404.
- Verified `https://lov.linkeddata.es/` returns HTTP 200 and updated the LOV submission route note to use the live root URL while documenting that historical `/dataset/lov/` is dead.
- Verified `python scripts\maintenance\check_registry_links.py --live --allow-unpublished`, `make release-preflight`, `make validate`, and `make test` after the LOV URL correction.
- Reviewed updated maintenance PR `#1`; validation-report churn was gone, but `conductor/remote_status.md` still listed the automated maintenance PR itself.
- Updated `check_github.py` so `gh pr list` requests `headRefName` and filters the `chore/automated-maintenance` branch out of remote-status summaries.
- Verified focused maintenance tests, `make release-preflight`, `make validate`, and `make test` after the self-reference filter.
- Closed stale automated maintenance PR `#1` and deleted branch `chore/automated-maintenance`.
- Fresh maintenance dispatch `27923789206` passed end to end and created PR `#2` from current master.
- Verified PR `#2` diff contained only the expected changelog entry and `conductor/remote_status.md` refresh with no self-reference and no validation-report churn.
- Merged PR `#2`; local master fast-forwarded to merge commit `a10f0d9`.
- Verified post-merge local `make validate` and `make test`, plus remote `Validate UOGTO` run `27923845421` and `Build WIDOCO Pages` run `27923845414`.
- Added `scripts/maintenance/check_zenodo_depositions.py` to inspect authenticated Zenodo depositions through `ZENODO_ACCESS_TOKEN`, with Make/Pixi tasks and handoff/release-note documentation.
- Verified no installed `zenodo-cli`, `zenodo`, `zenodo_get`, or `zenodo-get` executable was available on PATH, and PyPI had no `zenodo-cli` package.
- Searched shallow `.env*` files in surrounding local repo roots. Found one Zenodo-token-shaped value in parent `legal-nz/.env`; token value was not printed or committed.
- Loaded that token only into the checker process and ran `python scripts\maintenance\check_zenodo_depositions.py --json`; Zenodo returned `no_uogto_deposition_found`.
- Checked UOGTO open issues and PRs; both lists are empty.
- Read upstream w3id PR `6238` body, comments, and reviews; there are no comments or reviews to address, and the PR is open/mergeable but unmerged.
- Refreshed live external status: public Zenodo DOI search remains empty, and `/uogto/`, `/uogto/core`, `/uogto/extensions` still return 404.
- Pushed commit `db59bdb` and verified remote `Validate UOGTO` run `27949544161` passed plus `Build WIDOCO Pages` run `27949544173` passed and deployed.
- Pushed commit `da246b9` and verified remote `Validate UOGTO` run `27947593135` passed plus `Build WIDOCO Pages` run `27947593119` passed and deployed.
- Wired scheduled maintenance to upload `dist/publication-status-live.json` as workflow artifact `publication-status-live`.
- Added a workflow contract test target so artifact upload remains part of the maintenance lane.
- Verified focused workflow/publication tests, live status generation, `make release-preflight`, `make validate`, and `make test`.
- Manual maintenance dispatch `27914704264` failed before artifact upload in `update_dependencies.py` because the script could not import `scripts.maintenance.disk_guard` when run under Pixi on Linux.
- Added repo-root import setup to `update_dependencies.py`.
- Verified focused workflow/update-dependencies/publication tests, live status generation, `make release-preflight`, `make validate`, and `make test`.
- Maintenance rerun `27914843364` failed before artifact upload because `disk_guard.py` defaulted to `C:\` on Linux.
- Added cross-platform default disk path detection to `disk_guard.py`.
- Verified focused disk/update/workflow/publication tests, `make release-preflight`, `make validate`, and `make test`.
- Maintenance rerun `27914935755` passed live status artifact upload, then failed in `create-pull-request` with duplicate GitHub Authorization headers.
- Disabled checkout credential persistence in the maintenance workflow; rerun verification remains pending.
- Maintenance rerun `27915044021` passed live status artifact upload, then failed because repository settings do not permit GitHub Actions to create pull requests.
- Marked the maintenance PR creation step `continue-on-error: true`; rerun verification remains pending.
- Maintenance rerun `27915165068` passed end to end after PR creation was made non-fatal.
- Verified `Validate UOGTO` run `27915121389` and `Build WIDOCO Pages` run `27915121386` passed for commit `2f74af8`.
- Confirmed the successful maintenance run passed `Build Live Publication Status` and `Upload Live Publication Status Artifact`; GitHub still annotates repository PR permission denial and Pixi cache restore warnings, but they are non-blocking for publication monitoring.
- Checked upstream action releases after run `27915165068`: `actions/upload-artifact` latest `v7.0.1`, `peter-evans/create-pull-request` latest `v8.1.1`, and `prefix-dev/setup-pixi` latest `v0.9.6`.
- Updated the maintenance workflow pins to `actions/upload-artifact@v7`, `peter-evans/create-pull-request@v8`, and `prefix-dev/setup-pixi@v0.9.6`, with workflow contract tests covering the pins.
- Verified `python -m pytest tests\test_maintenance_workflow.py`, `make release-preflight`, `make validate`, and `make test` after the pin refresh.
- Verified push commit `7a35ff4`: `Validate UOGTO` run `27915341380` passed and `Build WIDOCO Pages` run `27915341370` passed and deployed.
- Verified manual maintenance dispatch `27915375191` passed end to end with refreshed action pins, including live publication-status artifact upload; the previous Node.js 20 deprecation annotation is gone, leaving only the nonfatal repository PR-permission annotation.

## [2026-06-22] - w3id Live Publication Status Integration
- Folded w3id pull request and redirect observations into `build_publication_status.py --live`.
- `dist/publication-status-live.json` is now the single routine publication monitor for Pages, release assets, Zenodo DOI, and w3id state.
- Verified focused publication/w3id tests, live status generation, `make release-preflight`, `make validate`, and `make test`.
- Local live output records PR `merged=false` and three pending 404 namespace redirects while preserving `pending_external_publication_steps`.

## [2026-06-22] - Live Publication Status Observations
- Added optional live observations to the publication status builder for Pages, release assets, and Zenodo DOI search.
- Wired `make publication-status-live`, Pixi `publication-status-live`, and scheduled maintenance.
- Verified focused publication/release tests, `python scripts/maintenance/build_publication_status.py --live --output dist/publication-status-live.json`, `make release-preflight`, `make validate`, and `make test`.
- Local live output recorded release asset observations as live and Zenodo DOI search as empty, leaving status `pending_external_publication_steps`.

## [2026-06-22] - Publication Status Packet
- Added a consolidated `publication-status.json` release artifact for Pages, release assets, DOI, Zenodo, w3id, LOV, and OLS state.
- Wired `make publication-status`, Pixi `publication-status`, release preflight, and release-assets workflow upload.
- Verified focused publication/release tests, `make release-preflight`, `make validate`, and `make test`.

## [2026-06-22] - Publication Status Release Attachment
- Verified remote `Validate UOGTO` run `27914083540` and `Build WIDOCO Pages` run `27914083544` passed for commit `7a9242e`.
- Dispatched `Publish Release Assets` workflow run `27914117992` for existing release tag `v1.0.0`.
- Verified the workflow passed release gates, built registry, Zenodo, w3id, and publication-status packets, passed release preflight, and uploaded assets.
- Verified `publication-status.json` is attached to the `v1.0.0` GitHub release with digest `sha256:e52e18db755e23c1e2317cdf8483960a55e374ad2f8b929512a7c4b9f52d8ec5`.
- Verified `https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/publication-status.json` returns an HTTP download redirect and the downloaded packet contains `pending_external_publication_steps`.

## [2026-06-22] - Zenodo Handoff Release Artifact
- Added `scripts/maintenance/build_zenodo_handoff.py` plus Make and Pixi wiring to generate `dist/zenodo-handoff.json`.
- Added the Zenodo handoff packet to release preflight and the release-assets upload workflow.
- Added tests covering pending DOI handoff state and release-readiness requirements.

## [2026-06-22] - Zenodo Handoff Release Attachment
- Dispatched `Publish Release Assets` workflow run `27913777454` for existing release tag `v1.0.0`.
- Verified the workflow passed release gates, built registry, Zenodo, and w3id handoff packets, passed release preflight, and uploaded assets.
- Verified `zenodo-handoff.json` is attached to the `v1.0.0` GitHub release with digest `sha256:e9a62ecc806cbc162e9dfd7cd818f0472147f3ac6b6d346a2551b218c072db54`.
- Verified `https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/zenodo-handoff.json` returns an HTTP download redirect.

## [2026-06-22] - w3id Status Monitor
- Added `scripts/maintenance/check_w3id_status.py` plus Make, Pixi, and scheduled maintenance wiring for w3id PR and redirect monitoring.
- Added tests covering the current pending-merge state and future strict failure modes for unmerged PRs and non-live redirects.
- Verified `python scripts/maintenance/check_w3id_status.py --live` reports PR `6238` open, `merged=False`, and w3id `/uogto/`, `/uogto/core`, and `/uogto/extensions` returning 404 until upstream merge.

## [2026-06-22] - w3id Handoff Asset Refresh After PR Submission
- Dispatched Publish Release Assets workflow run 27913296574 for v1.0.0 after submitting the upstream w3id pull request.
- Verified the workflow passed release gates, rebuilt registry and w3id handoff packets, passed release preflight, and uploaded release assets.
- Downloaded the refreshed w3id-redirect-handoff.json release asset through gh release download and verified it contains status pending_external_w3id_merge and pull request https://github.com/perma-id/w3id.org/pull/6238.

## [2026-06-22] - w3id Upstream Pull Request Submission
- Forked perma-id/w3id.org to edithatogo/w3id.org, added uogto/.htaccess and uogto/README.md, and pushed branch uogto-namespace-redirects.
- Opened upstream pull request https://github.com/perma-id/w3id.org/pull/6238 for the UOGTO namespace redirects.
- Updated the UOGTO w3id handoff packet state from pending PR submission to pending upstream merge/live redirect verification.

## [2026-06-22] - w3id Submitted-PR Release Attachment
- Dispatched `Publish Release Assets` workflow run `27913296574` for existing release tag `v1.0.0`.
- Verified the workflow passed release gates, built both handoff packets, passed release preflight, and uploaded assets.
- Verified `w3id-redirect-handoff.json` is attached to the `v1.0.0` GitHub release with digest `sha256:92062da793d8d547a8a4e5682a33d261d3e0a63fa6d1bc9576a9051ac3fc3fea`.
- Verified `https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/w3id-redirect-handoff.json` returns an HTTP download redirect.

## [2026-06-22] - w3id Handoff Release Artifact
- Configured the release-assets workflow to upload `dist/w3id-redirect-handoff.json` alongside the registry handoff packet.
- Tightened release readiness checks so the w3id packet must exist and the workflow must name its upload path.
- Recorded Conductor status that the external `perma-id/w3id.org` pull request remains the live publication blocker.

## [2026-06-22] - w3id Handoff Release Attachment
- Dispatched `Publish Release Assets` workflow run `27913057014` for existing release tag `v1.0.0`.
- Verified the workflow passed release gates, built release assets, built both handoff packets, passed release preflight, and uploaded assets.
- Verified `w3id-redirect-handoff.json` is attached to the `v1.0.0` GitHub release with digest `sha256:1e69d5d022c173f659760dbdb3310d5f81d59658028d0505de76a758de6e8fde`.
- Verified `https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/w3id-redirect-handoff.json` returns an HTTP download redirect.

## [2026-06-22] - Existing Release Registry Handoff Asset Refresh
- Dispatched `Publish Release Assets` workflow run `27912459022` for existing release tag `v1.0.0`.
- Verified the workflow passed release gates, built release assets, built the registry handoff packet, passed release preflight, and uploaded assets.
- Verified GitHub release `v1.0.0` now includes `registry-handoff.json` and that its public release asset URL returns an HTTP download redirect.

## [2026-06-22] - Pixi Release Preflight Registry Packet Alignment
- Updated `pixi run release-preflight` to build `dist/registry-handoff.json` before running release readiness checks, matching `make release-preflight`.
- Verified focused registry/release-readiness tests, `make release-preflight`, `make validate`, and `make test`.

## [2026-06-22] - Registry Handoff Release Attachment
- Dispatched `Publish Release Assets` workflow for `v1.0.0`.
- Workflow run `27912429240` passed and completed the release gates, release asset build, registry handoff packet build, release preflight, and GitHub release upload steps.
- Verified `registry-handoff.json` is attached to the `v1.0.0` GitHub release with digest `sha256:043b8c753e09a97e371da9be5c23ab5588da035bea59bfbbfa433adc859b9c7a`.
- Verified `https://github.com/edithatogo/UOGTO/releases/download/v1.0.0/registry-handoff.json` returns an HTTP download redirect.

## [2026-06-22] - Registry Handoff URL Requirement
- Promoted the `registry-handoff.json` release asset URL to a required registry publication URL.
- Added the handoff URL to LOV and OLS registry packet docs.
- Added the handoff URL to the generated registry handoff artifact map and release-readiness packet checks.

## [2026-06-22] - Registry Namespace Redirect Boundary
- Strict registry live checks surfaced pending `w3id.org/uogto` namespace redirects.
- Added explicit namespace URL classification so `--allow-unpublished` skips pending w3id redirects while strict live checks still fail until redirects are configured.
- Updated the registry metadata checklist and Conductor status to keep the w3id redirect task separate from DOI, LOV, and OLS submission state.

## [2026-06-22] - w3id Redirect Handoff Packet
- Added `docs/registry/w3id-submission.md` with proposed `uogto/.htaccess` rules for the pending namespace redirects.
- Added `scripts/maintenance/build_w3id_redirect_handoff.py` plus `make w3id-packet` and Pixi task wiring to emit `dist/w3id-redirect-handoff.json`.
- Added tests covering the generated w3id packet, proposed rewrite rules, and JSON output.
- Included the w3id submission document in publishing metadata and registry link checks without claiming that the external w3id PR has been submitted.

## [2026-06-22] - Manuscript PDF CI Gate
- Added `.github/workflows/manuscript-pdf.yml` to install a minimal LaTeX toolchain on Ubuntu and run `make manuscript-pdf`.
- Added a workflow wiring test so the strict manuscript PDF CI lane keeps using current GitHub actions and the repository `make manuscript-pdf` target.
- Updated manuscript SourceRight Conductor status to distinguish CI strict-PDF coverage from the local Windows machine, which still lacks a TeX engine.

## [2026-06-22] - Manuscript PDF CI Remote Verification
- Verified commit `8118694` on `origin/master`.
- Remote `Validate UOGTO` run `27911901129` passed.
- Remote `Build Manuscript PDF` run `27911901120` passed, proving the strict LaTeX PDF gate in CI.
- Remote `Build WIDOCO Pages` run `27911901116` passed and deployed, and `https://edithatogo.github.io/UOGTO/` returned HTTP 200.

## [2026-06-22] - Registry Handoff Packet Guard
- Confirmed the live DOI check still has no locally recorded or public Zenodo DOI.
- Added `scripts/maintenance/build_registry_handoff.py` plus `make registry-packet` and Pixi task wiring to emit `dist/registry-handoff.json`.
- Added tests covering pending DOI blocker state, ready-mode rejection while placeholders remain, and JSON output.
- Updated the publishing Conductor plan/status so LOV and OLS submission handoff state is represented without claiming external submission.

## [2026-06-22] - Registry Handoff Release Artifact
- Wired `make release-preflight` to generate the registry handoff packet before readiness checks.
- Updated the release-assets workflow to build and upload `dist/registry-handoff.json`.
- Hardened release-readiness checks and tests so future release runs fail if the registry handoff packet is missing or malformed.

## [2026-06-22] - Release Preflight Gate
- Added `scripts/maintenance/check_release_readiness.py` to validate local v1.0 release readiness and harden future DOI-minting release updates.
- Added `make release-preflight` plus a Pixi `release-preflight` task and included the readiness script in the aggregate Pixi `check` task.
- Wired the release-assets GitHub Actions workflow to run the release-readiness script after generated assets are built and before upload.
- Added `scripts/maintenance/check_doi_status.py`, `make doi-status`, Pixi DOI tasks, tests, and scheduled maintenance live DOI monitoring for the Zenodo publication gate.
- Added `scripts/maintenance/record_zenodo_doi.py`, tests, and Make/Pixi wiring so the minted DOI can be recorded consistently across release notes, registry packets, `CITATION.cff`, and `.zenodo.json`.
- Extended release-readiness checks to validate DOI placeholder state locally and require recorded DOI metadata in strict published mode.
- Updated v1.0 release notes and the publishing Conductor track so DOI, LOV, and OLS remain explicit external gates rather than local completion claims; the gate was added after the initial `v1.0.0` publication.
- Stabilized `tests/test_release_readiness.py` so ordinary `pytest` and CI create release-readiness fixture assets before checking the local manifest.
- Verified commit `fd7dc7e`: `Validate UOGTO` run `27910976656` passed, `Build WIDOCO Pages` run `27910976624` built and deployed successfully, and the public Pages root returned HTTP 200.
- Verified commit `850bfab`: `Validate UOGTO` run `27911050014` passed and `Build WIDOCO Pages` run `27911050024` built and deployed successfully.
- Modernized workflow action pins after the latest Pages run reported Node 20 deprecation warnings: `actions/checkout@v7`, `actions/setup-python@v6`, `actions/setup-java@v5`, `actions/upload-pages-artifact@v5`, and `actions/deploy-pages@v5`.
- Updated the publishing metadata checker so release-readiness tests require the Node 24-compatible Pages deploy pin.

## [2026-06-22] - v1.0.0 Release Publication
- Created GitHub release `v1.0.0`: https://github.com/edithatogo/UOGTO/releases/tag/v1.0.0.
- Release-assets workflow run `27910615774` passed and attached `uogto.ttl`, `uogto-shapes.ttl`, JSON-LD contexts, `SHA256SUMS`, and `release-assets-manifest.json`.
- WIDOCO Pages tag workflow run `27910615818` passed after rerun; the first failure was a transient GitHub API 504 while downloading WIDOCO.
- Verified `https://edithatogo.github.io/UOGTO/` returned HTTP 200 and the `uogto.ttl` release asset returned an HTTP download redirect.
- Zenodo public search did not show a UOGTO DOI record yet, so DOI-dependent LOV and OLS submission remain open.

## [2026-06-22] - Conductor State Reconciliation and SourceRight Track
- Added completed Conductor track `conductor_state_reconciliation_20260622` to record archive normalization, status updates, CI/Pixi hardening, registry link checks, and follow-up planning.
- Added `conductor/archive/index.md` so retired and superseded tracks are discoverable without being treated as active work.
- Added pending Conductor track `manuscript_source_verification_20260622` for SourceRight-backed CSL normalization, citation reconciliation, and manuscript source reporting.
- Updated Conductor status to make SourceRight verification an explicit remaining manuscript-quality gate.
- Tightened publishing metadata schema checks so citation repository URLs must be absolute HTTP(S) URLs.

## [2026-06-22] - SourceRight Manuscript Source Verification
- Added `scripts/maintenance/build_manuscript_sources.py` plus focused tests to build canonical manuscript SourceRight inputs from curated standards, review data, and deep-research references.
- Generated `docs/paper/references.csl.json`, `docs/paper/source-inventory.json`, `docs/paper/source-review-queue.jsonl`, `.sourceright/references.csl.json`, `.sourceright/references.verification.json`, and `.sourceright/review-queue.jsonl`.
- Updated `docs/paper/paper.tex` with citation commands and a manual bibliography for the current manuscript source set.
- Ran `sourceright validate-csl --json docs/paper/references.csl.json`; validation passed with no diagnostics.
- Generated SourceRight integrity reports at `docs/paper/sourceright-report.md` and `docs/paper/sourceright-report.json`; the report shows 36 references, 36 local provider candidates, 25 manual-review queue items, 0 errors, 31 warnings, and 25 info items.
- Ran `sourceright citations docs/paper/manuscript-citations.txt .sourceright`; the command completed but SourceRight 0.1.20 detected 0 citation occurrences, so citation-key reconciliation remains open and is recorded in `docs/paper/sourceright-citations.md`.

## [2026-06-22] - Publishing and Discoverability Planning
- Added Conductor track `uogto_publishing_discoverability_20260622` after the completed modeling, validation, release, and maintenance phases.
- Planned Zenodo DOI integration, `CITATION.cff`, `.zenodo.json`, and v1.0 release notes.
- Planned WIDOCO HTML documentation generation and GitHub Pages deployment.
- Planned LOV metadata checklist/submission and OLS indexing request milestones.

## [2026-06-22] - Publishing and Discoverability Implementation
- Implemented repository-side publishing metadata files: `CITATION.cff`, `.zenodo.json`, and `docs/releases/v1.0.md`.
- Added WIDOCO documentation configuration, local build notes, and GitHub Pages workflow.
- Added LOV and OLS registry preparation documents plus shared metadata checklist.
- Added `scripts/maintenance/check_publishing_metadata.py`, `make publishing-metadata`, Pixi publishing metadata task, and focused pytest coverage.
- Left Zenodo DOI minting, GitHub Pages workflow verification, LOV submission, and OLS indexing as explicit external release gates.

## [2026-06-22] - Publishing Review Hardening
- Tightened WIDOCO Pages workflow so validation, tests, semantic audit, publishing metadata checks, and build run before Pages artifact upload.
- Pinned WIDOCO download to release `v1.4.25` instead of resolving the latest release at runtime.
- Replaced selected publishing metadata assertions with JSON Schema-backed validation for `CITATION.cff` and `.zenodo.json`.
- Added negative tests for incomplete citation and Zenodo metadata.

## [2026-06-22] - Publishing Review Follow-Up
- Added `conductor/product-guidelines.md` so Conductor reviews have a complete local guideline context.
- Enabled JSON Schema format checking for publishing metadata URLs and dates.
- Added negative tests for invalid citation URL format and Zenodo language metadata.

## [2026-06-22] - Registry Annotation Gate
- Added DCTERMS and VANN metadata to the primary UOGTO ontology release header.
- Extended the publishing metadata gate to parse source ontology modules and verify release-header registry annotations plus module ontology labels.
- Updated the LOV/OLS metadata checklist and Conductor publishing plan to distinguish repo-side metadata readiness from live DOI, Pages, LOV, and OLS service gates.

## [2026-06-22] - Registry Link Maintenance Gate
- Added `scripts/maintenance/check_registry_links.py` to verify required registry URLs and optionally perform live HTTP checks.
- Added Make/Pixi tasks and scheduled maintenance workflow execution for registry link checks, with known unpublished v1.0 URLs explicitly allowed until release.
- Updated the v1.0 release notes and publishing plan to include the registry link gate.

## [2026-06-22] - Release Asset Packaging Gate
- Added `scripts/maintenance/package_release_assets.py` to generate release asset checksums and a machine-readable release asset manifest.
- Added `.github/workflows/release-assets.yml` so published/manual releases attach generated RDF, SHACL, JSON-LD context, checksum, and manifest assets after validation gates.
- Updated LOV/OLS registry docs to use stable GitHub release download URLs instead of ignored local `dist/` paths.

## [2026-06-22] - WIDOCO Pages Deployment Gate
- Checked live GitHub Actions after push: validation passed, WIDOCO artifact generation reached Pages deployment, and deploy failed with GitHub API 404 because Pages is not enabled for the repository.
- Gated the deploy job behind repository variable `ENABLE_PAGES_DEPLOY=true` so push workflows can keep validating and uploading WIDOCO artifacts until Pages is enabled in repository settings.
- Verified the follow-up push: `Validate UOGTO` run `27910154892` passed, and `Build WIDOCO Pages` run `27910154887` passed the WIDOCO build/artifact job with deploy skipped by the gate.

## [2026-06-22] - GitHub Pages Enablement
- Enabled GitHub Pages for `edithatogo/UOGTO` with Actions as the source and set repository variable `ENABLE_PAGES_DEPLOY=true`.
- Dispatched WIDOCO Pages run `27910289217`; build and deploy both succeeded, and `/index-en.html` returned HTTP 200.
- Root URL returned HTTP 404 because WIDOCO emitted `index-en.html` but not `index.html`; added a CI copy step so future deployments publish a root index.
- Pushed and verified the root-index fix: WIDOCO Pages run `27910392764` deployed successfully, paired `Validate UOGTO` run `27910392787` passed, and both the Pages root URL and `/index-en.html` returned HTTP 200.

## [2026-06-21] - Conductor Status Normalization and CI Hardening
- Reconciled completed scoping-review execution track metadata with checked implementation plans.
- Marked systematic literature review planning as superseded by the completed protocol and execution-paper tracks, then prepared it for archive.
- Checked repository-maintenance acceptance criteria after maintenance scripts and tests were verified.
- Added Linux Pixi platform support, cross-platform Pixi discovery, semantic audit/report generation in checks, and scheduled maintenance PR creation.
- Added pytest sandbox cache directories to `.gitignore`.

## [2026-06-21] - Repository Maintenance and Remote Automation
- Initialized Pixi package manager configurations (`pixi.toml`).
- Created `scripts/maintenance/check_github.py` to query issues/PRs from remote and generate statuses.
- Created `scripts/maintenance/update_dependencies.py` to run bleeding-edge upgrades.
- Created `scripts/maintenance/generate_changelog.py` to parse Git logs and update `CHANGELOG.md` automatically.
- Created unit tests for the maintenance scripts.
- Implemented custom Antigravity agent skill `repo-maintenance` at `.agents/skills/repo-maintenance/SKILL.md`.
- Created GitHub Actions workflow `.github/workflows/maintenance.yml` for CI automation.


## [2026-06-20] - Bootstrap and Core Implementation
- Initialized empty Git repository.
- Created repository layout: `ontologies/`, `shapes/`, `jsonld/`, `examples/`, `competency-questions/`, `scripts/`, `tests/`, `docs/`, `.github/workflows/`.
- Populated Conductor metadata files (`AGENTS.md`, `CONDUCTOR.md`, `.conductor/tasks.yaml`, `.conductor/status.md`).
- Implemented core ontology modules (`uogto-core.ttl` and components).
- Implemented extension modules representing classical, cooperative, MARL, network, evolutionary, mechanism design, deontic logic, social choice, contract theory, and compositional open games.
- Implemented SHACL validation shapes for structural rules.
- Implemented JSON-LD contexts.
- Implemented examples including Prisoner's Dilemma, Stag Hunt, auctions, LLM interaction games, and Petri nets.
- Implemented competency queries.
- Written build, validate, and coverage report scripts.
- Configured pytest test suite.
- Successfully built project using `make build`.
- Successfully validated repo using `make validate`.
- Successfully verified project coverage using `make coverage` and ran tests.

## 2026-06-22 - Manuscript Source Verification
- Added docs/paper/references.csl.json, source inventory, review queue, SourceRight validation report, and citation reconciliation output.
- Split the broad 36-record source inventory from the 11-record manuscript bibliography used by SourceRight.
- Added `scripts/maintenance/check_manuscript_citations.py` and tests to verify that LaTeX `\cite{...}` keys, manual `\bibitem{...}` entries, and `docs/paper/references.csl.json` stay aligned.
- SourceRight CSL validation passes; report has 11 manuscript references, 0 queued manual reviews, 0 unresolved reviews, and 0 provider conflicts.
- SourceRight citation reconciliation now reports 11 numeric citation occurrences, 11 matched citations, and 0 issues for `docs/paper/manuscript-citations.txt`.
- Added `make manuscript-check` as a direct local LaTeX citation-key reconciliation gate.
- `make manuscript-sourcecheck` passes and runs source generation, local LaTeX citation-key reconciliation, SourceRight CSL validation, SourceRight reporting, and SourceRight citation reconciliation.
- Completed SourceRight manuscript source verification: numeric citation reconciliation reports 11 occurrences, 11 matches, and 0 issues; repo-native manuscript checks pass; the manuscript SourceRight manual review queue is empty.
- Narrowed manuscript SourceRight manual-review queuing so missing issued dates only queue scholarly article/book records, not web/API/standards references that legitimately lack publication-date metadata.
- Added `scripts/maintenance/build_manuscript_pdf.py`, `make manuscript-build`, `make manuscript-pdf`, and matching Pixi tasks. The default build gate passes TeX structure checks and compiles when a LaTeX engine is present; the strict PDF gate fails explicitly if no engine is installed.

## [2026-06-23] - Upstream Registry Thread Comment Audit

- Checked upstream PR perma-id/w3id.org#6238 using the GitHub connector.
- Result: merged PR has no review submissions and no inline review threads; the only discussion comment is the existing publication metadata update.
- Checked active upstream registry issues biopragmatics/bioregistry#1999, OntoZoo/ontobee#212, pyvandenbussche/lov#83, and EBISPOT/ols4#1305.
- Result: Bioregistry had one maintainer comment requesting the new prefix issue template; the issue body and follow-up comment already address it. Ontobee, LOV, and OLS currently have no comments.
- Remaining action: no upstream PR/issue comments currently require code, metadata, or response changes. Continue to monitor FAIRsharing and Wikidata separately because those remain account-authenticated submission tasks rather than GitHub PR comments.
