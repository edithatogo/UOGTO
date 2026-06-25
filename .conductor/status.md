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
- w3id PR `6238` has been updated with DOI and publication evidence, merged at `2026-06-22T12:29:07Z`, and live `/uogto/core` plus `/uogto/extensions` redirects resolve to the UOGTO documentation site.
- Extended discoverability track `uogto_extended_discoverability_registries_20260622` is implemented repo-side: the shared packet, generated `extended-registry-handoff.json`, Make/Pixi/release workflow wiring, and publication-status integration are in place; prefix.cc `uogto`/`uogtox`, w3id, Ontobee submission, Bioregistry template-update submission, Wikidata item `Q140323510`, and FAIRsharing draft record `8382` are complete; external actions remain pending only for FAIRsharing curator review and registry maintainer review.
- Comparative simulation ontology mapping track `uogto_comparative_simulation_ontology_mapping_20260624` is completed and archived. The archived track records 21 candidate sources across 17 families, 21 provenance records, 4 downloaded redistributable RDF artifacts, 17 metadata-only records, a normalized term inventory with 4,037 rows across 69 UOGTO/external sources, 460 deterministic mapping candidates across 4 external RDF sources, a 460-row mapping review CSV, accepted alignment TTL with 10 accepted mapping triples, overlap/descriptive metrics, network analysis, seven static SVG figures, the comprehensive comparison report at `docs/ontology-comparison/report.md`, and `make ontology-comparison-check` artifact-contract validation.
- Article-hardening protocol track `uogto_article_hardening_protocol_20260624` is planned. It will extend the completed comparative mapping baseline into a broader publication-grade evidence package using a PRISMA-ScR/PRISMA-S search and reporting protocol plus RO-Crate 1.1 reproducibility packaging, covering additional game-description, simulation, systems-biology, workflow/process, Petri-net, automata, planning/service, and reference ontology/formalism sources, and explicit triage of missing game-theory ontology elements for possible UOGTO inclusion, external alignment, deferral, or rejection.
- Article-hardening Phase 1 is implemented: `docs/article-hardening/protocol.md`, `protocol-checklist.md`, and `search-strategy.md` define the PRISMA-ScR protocol structure, PRISMA-S search-log fields, evidence levels, eligibility/charting rules, missing-element decision rules, and RO-Crate reporting requirements; `make article-hardening-protocol` validates the scaffold.
- Article-hardening review governance is implemented: `conductor/agents/article-hardening-review-agents.json`, `conductor/workflows/article-hardening-phase-review.md`, `.agents/skills/article-hardening-review/SKILL.md`, and `docs/article-hardening/reviews/phase-review-log.jsonl` define required peer, editorial, red-team, and devil's-advocate phase review gates.
- Article-hardening ontology-quality benchmarking is implemented: `docs/article-hardening/quality-metrics.json` and `reasoner-report.md` report annotation completeness, orphan classes, relation richness, hierarchy depth, import depth, SHACL coverage, examples per module, competency-query coverage, local OOPS-style pitfall indicators, and OWL profile/reasoner status.
- SHACL coverage now includes example-graph linkage, module-shape coverage, and competency-question to example-graph linkage so coverage claims are explicit rather than inferred.
- Article-hardening ROBOT-style ontology reports are implemented as an optional Java-backed layer: `docs/article-hardening/robot/status.json`, `reasoner-check.md`, `report.md`, `merged-ontology.ttl`, `merge-diff.md`, `import-extraction.ttl`, and `import-extraction.md` preserve a ROBOT-like surface while RDFLib/pySHACL remain the portable baseline.
- Ontology design-pattern documentation is now available at `docs/ontology-design-patterns.md`, describing how UOGTO models games, sessions, traces, strategies, actions, payoffs, outcomes, mechanisms, and execution bindings.
- Article-hardening Phase 2 evidence register is implemented: `docs/article-hardening/search-log.jsonl`, `source-extension-inventory.json`, and `source-extension-inventory.md` provide hash-chained append-only search events, source hashes, evidence levels, inclusion rationales, licence dispositions, and reviewer handoffs for 39 sources.
- Ontology-comparison mappings now include SSSOM outputs alongside Turtle: `docs/ontology-comparison/accepted-alignments.sssom.tsv` and `accepted-alignments.sssom.yml` are generated from the accepted review rows while keeping `accepted-alignments.ttl` unchanged as RDF alignment output.
- Article-hardening research governance is implemented: `conductor/agents/article-hardening-research-agents.json`, `conductor/workflows/article-hardening-research-workflow.md`, `.agents/skills/article-hardening-research/SKILL.md`, and `docs/article-hardening/research/phase-research-log.jsonl` define source-discovery, standards-landscape, game-theory-gap, evidence-curation, and reproducibility research handoffs before phase review.

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
- Registry live-link checks now distinguish strict live mode from account-bound or maintainer-review external gates; w3id namespace redirects are live.
- w3id redirect handoff is prepared in docs/registry/w3id-submission.md and make w3id-packet; release preflight requires dist/w3id-redirect-handoff.json. The external perma-id/w3id.org pull request https://github.com/perma-id/w3id.org/pull/6238 is merged and live redirects are verified.
- w3id PR and redirect monitoring is implemented with `make w3id-status`, `pixi run w3id-status-live`, and scheduled maintenance; current state records PR merged and redirects live.
- SourceRight manuscript citation reconciliation now reports 11 citation occurrences, 11 matches, and 0 issues; the manuscript SourceRight manual review queue is empty.
- GitHub-owned Actions workflow pins have been updated to current Node 24-compatible major releases for checkout, Python setup, Java setup, Pages artifact upload, and Pages deploy.
- Strict manuscript PDF generation is covered by GitHub Actions run `27911901120`, which installed LaTeX and passed `make manuscript-pdf` for commit `8118694`.
- Zenodo account-side inspection now has a token-aware terminal path through `make zenodo-depositions`; the parent `legal-nz/.env` token was found and checked without printing it, and Zenodo returned `no_uogto_deposition_found`.

## Next Recommended Task
- Append live Phase 2 registry/API searches to `docs/article-hardening/search-log.jsonl`, then implement Phase 3 source acquisition/RO-Crate packaging and extend quality benchmarking to parsed external comparator artifacts.
- Continue monitoring LOV/OLS, FAIRsharing curator review, Ontobee issue #212, and Bioregistry issue #1999.

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
- Strict registry live checks no longer fail for w3id namespace redirects; scheduled/live maintenance can use external-review status for remaining registry gates.
- w3id redirect pull request https://github.com/perma-id/w3id.org/pull/6238 is merged and live redirect completion is verified.
- Release-assets workflow dispatch run `27913296574` passed for `v1.0.0` and attached the submitted-PR `w3id-redirect-handoff.json`; the release asset URL returned HTTP 302 to the downloadable object.
- Release-assets workflow dispatch run 27913296574 passed for v1.0.0 and refreshed w3id-redirect-handoff.json; the 2026-06-23 follow-up changes the generated packet to `live_redirects_verified` after PR merge and redirect checks.
- Live w3id monitor reports PR `6238` merged and `/uogto/core` plus `/uogto/extensions` redirect to the UOGTO documentation site.
- Zenodo DOI is recorded and resolves publicly; LOV and OLS requests are submitted and awaiting maintainer review.
- Release-assets workflow dispatch run `27913777454` passed for `v1.0.0` and attached `zenodo-handoff.json`; the release asset URL returned HTTP 302 to the downloadable object.
- `dist/publication-status.json` is part of local release preflight and the release-assets workflow; current generated status should report DOI recorded, LOV/OLS submitted, w3id live, Wikidata complete, and FAIRsharing record `8382` awaiting curator review.
- The attached `publication-status.json` release asset has digest `sha256:e52e18db755e23c1e2317cdf8483960a55e374ad2f8b929512a7c4b9f52d8ec5`.
- Live publication status observations are added to scheduled maintenance so public Pages, release assets, and Zenodo DOI search can be inspected from one generated JSON artifact.
- `dist/publication-status-live.json` includes w3id PR and redirect observations. Current generated output records live w3id redirects while preserving `pending_external_publication_steps` for registry review/account gates.
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
- w3id pull request `https://github.com/perma-id/w3id.org/pull/6238` is merged; live `/uogto/core` and `/uogto/extensions` redirects return 303 to the UOGTO documentation site.
- Post-hardening maintenance dispatch `27923371952` failed on the registry link checker because the historical LOV `/dataset/lov/` URL redirects to 404; the LOV route note now uses the live root `https://lov.linkeddata.es/`, and local live registry link checks pass.
- Remote-status generation now filters the automated `chore/automated-maintenance` branch when using `gh`, preventing the maintenance PR from reporting itself as open repository work.
- Stale automated maintenance PR `#1` was closed and its branch deleted; fresh maintenance run `27923789206` created PR `#2`, which was merged as `a10f0d9` after confirming the diff was limited to changelog and remote-status updates.
- Added `scripts/maintenance/check_zenodo_depositions.py` with Make/Pixi wiring. Parent `.env` token-backed checks were used without printing the token; Zenodo record `20796937` is now published, and w3id PR `6238` is now merged with live redirects verified.
- LOV issue `https://github.com/pyvandenbussche/lov/issues/83` and OLS issue `https://github.com/EBISPOT/ols4/issues/1305` are open; both reference the public DOI, WIDOCO docs, release, and canonical RDF asset.
- Extended discoverability repo-side implementation is complete locally: `uogto` and `uogtox` are live at prefix.cc, Ontobee issue `https://github.com/OntoZoo/ontobee/issues/212` is open, Bioregistry issue `https://github.com/biopragmatics/bioregistry/issues/1999` is template-updated, Wikidata item `Q140323510` and FAIRsharing draft record `8382` exist, and BioPortal/OBO Foundry are recorded as conditional/not prioritized.
- Extended discoverability release evidence is recorded: commit `8b52503` passed remote `Validate UOGTO` run `27960976638`, remote `Build WIDOCO Pages` run `27960977018`, and `Publish Release Assets` run `27961110915`; the `extended-registry-handoff.json` release asset is attached with digest `sha256:31e4e76ab2334ce9b92b87fa6e5bb63a0e6f7b5094d242460ae65b37498b0018`.
- w3id PR `https://github.com/perma-id/w3id.org/pull/6238` is merged; DOI/publication evidence was added in comment `https://github.com/perma-id/w3id.org/pull/6238#issuecomment-4768124045`.
- Remote verification for commit `da246b9` passed: `Validate UOGTO` run `27947593135` succeeded and `Build WIDOCO Pages` run `27947593119` built and deployed successfully.
- Remote verification for commit `db59bdb` passed: `Validate UOGTO` run `27949544161` succeeded and `Build WIDOCO Pages` run `27949544173` built and deployed successfully.
- Remote verification for commit `d438c42` passed: `Validate UOGTO` run `27952260669` succeeded and `Build WIDOCO Pages` run `27952260682` built/deployed successfully.
- Release-assets refresh run `27952354134` passed for `v1.0.0`, rebuilding and uploading release packets that report `registry-handoff.json` status `submitted_to_registries`, `zenodo-handoff.json` status `doi_recorded`, and historical `publication-status.json` status `pending_external_publication_steps`; current local generation records w3id live and remaining registry-review/account gates.
- Live Pages root returned HTTP 200 after the `d438c42` deployment; DOI `https://doi.org/10.5281/zenodo.20796937` redirected to `https://zenodo.org/records/20796937` and returned HTTP 200.

## Extended Discoverability Follow-Up - 2026-06-23
- w3id PR 6238 is merged and /uogto/core plus /uogto/extensions return 303 redirects to <https://edithatogo.github.io/UOGTO/>.
- prefix.cc uogtox is live at <http://prefix.cc/uogtox.file.txt>; both UOGTO prefixes are submitted.
- Ontobee indexing request is open at <https://github.com/OntoZoo/ontobee/issues/212>.
- Bioregistry issue 1999 was updated to the requested new-prefix template and recorded at <https://github.com/biopragmatics/bioregistry/issues/1999#issuecomment-4778481220>.
- FAIRsharing and Wikidata remained blocked by authenticated maintainer-account workflows at this checkpoint; Wikidata was completed on 2026-06-24 and FAIRsharing now has record `8382` awaiting curator review.

## Remote Verification - 2026-06-23
- Commit `24b9601` passed remote `Validate UOGTO` run `28023497374` and `Build WIDOCO Pages` run `28023497352`.
- `Publish Release Assets` run `28023545152` passed and refreshed release packets for `v1.0.0`.
- Refreshed `extended-registry-handoff.json` has blockers only for FAIRsharing and Wikidata, prefix.cc status `submitted`, Ontobee issue #212, Bioregistry template-update evidence, and digest `sha256:07c9e9e66b69582065b97c01fa61df05ad6da8c04ff39a51069e0b70c9f93081`.
- Refreshed `w3id-redirect-handoff.json` has status `live_redirects_verified`, empty blockers, merged_at `2026-06-22T12:29:07Z`, and digest `sha256:82ea92c3fb8465a6bd97dfdfc51545b4e24e08d56ed2e4e7d1b26bd8a58a48ca`.
- Refreshed `publication-status.json` has status `pending_external_publication_steps` with blockers only for FAIRsharing and Wikidata and digest `sha256:f4ad2c38e8af6e9d8659246f2d8714966a9c9dbfdefa0dfb58d14639fb67caa4`.

## Live Account Evidence - 2026-06-24
- Wikidata item created and verified: https://www.wikidata.org/wiki/Q140323510.
- Wikidata statements verified in Chrome: instance of ontology, DOI `10.5281/zenodo.20796937`, official website `https://edithatogo.github.io/UOGTO/`, source code repository URL `https://github.com/edithatogo/UOGTO`, and copyright license Creative Commons Attribution 4.0 International.
- DOI resolved to Zenodo record `https://zenodo.org/records/20796937`; Zenodo record title, UOGTO documentation, and GitHub repository pages loaded successfully.
- FAIRsharing draft record created and populated: https://fairsharing.org/8382.
- FAIRsharing required `data processes and conditions` metadata persisted on 2026-06-24; public page now reports the record is awaiting FAIRsharing curator review.
- FAIRsharing recommended-but-nonblocking gaps: organisation links, publications, citations, and record associations.

- Added reviewer calibration sampling with balanced accepted/rejected mapping review, agreement scoring, and adjudication-ready outputs.

- Added network-analysis sensitivity scenarios for metadata-only exclusion, accepted-only mappings, and close/related mapping inclusion.

## 2026-06-25 - uogto_nature_presubmission_evaluation_20260625

- Status: active
- Track: `conductor/tracks/uogto_nature_presubmission_evaluation_20260625`
- Purpose: Nature-ready professor-level presubmission evaluation of the UOGTO repository, ontology, evidence package, manuscript, supplement, images, and PowerPoint.
- Current state: track scaffold created with specification, protocol, rubrics, review matrices, image scoring workflow, reviewer lanes, recommendations backlog, and decision memo scaffold.
- Known blocker: no PowerPoint deck was found during initial inspection; implementation should locate it or create a new slide inventory.
- Next gate: populate review matrices and image inventory during `$conductor-implement`.
## 2026-06-25 - uogto_nature_presubmission_evaluation_20260625 arXiv Toolchain Hardening

- Status: active
- Added arXiv toolchain hardening to the Nature presubmission evaluation track.
- New reviewer lane: `arxiv-toolchain-reviewer`.
- New artefacts: `arxiv_toolchain_matrix.csv`, `arxiv_toolchain_matrix.md`, `arxiv_acceptance_checklist.md`, and `reviewer_findings/arxiv-toolchain-reviewer.md`.
- Policy boundary: repo-native arXiv cleaner remains authoritative until external tools are benchmarked in isolated output directories.

## CI Hardening Verification - 2026-06-25
- Commit 018a2a4 is pushed to origin/master and records the SourceRight CI install fix plus the repo-local pytest import fix.
- Local validation passed after the fix set: focused arXiv workflow/source-package tests, affected ontology-visual tests, affected article-hardening tests, make validate, and full pytest with 189 tests.
- Remote GitHub Actions passed on commit 018a2a4: Validate UOGTO run 28145232100, Build WIDOCO Pages run 28145232082, and arXiv Preflight run 28145232079.
- Next substantive phase: execute the pending Nature presubmission review matrix for uogto_nature_presubmission_evaluation_20260625; no additional CI fix lane is currently open.


## Nature Presubmission Review Execution - 2026-06-25
- First-pass Nature presubmission review matrix executed for uogto_nature_presubmission_evaluation_20260625.
- review_matrix.csv and review_matrix.md now score all major surfaces including ontology core game-theory coverage manuscript supplement PowerPoint arXiv toolchain and arXiv source-leak privacy audit.
- Decision memo verdict is major revision before submission because the repo evidence base is strong but manuscript supplement figure-loop and deck readiness remain incomplete.
- Next substantive phase: implement the must-fix recommendations from the executed review rather than opening more CI hardening work.

 
## Blocker Reclassification - 2026-06-25 
- Supersedes earlier Nature presubmission notes that described missing PowerPoint and local arXiv tools as blockers. 
- PowerPoint deck absence is now a needs-creation task documented in conductor/tracks/uogto_nature_presubmission_evaluation_20260625/powerpoint_asset_inventory.md. 
- Missing local latexmk pdflatex tectonic and arxiv_latex_cleaner tools are optional advisory benchmark gaps because CI arXiv Preflight run 28145232079 passed. 
- Next implementation work should create the deck and source-leak privacy manifest rather than continue searching for local arXiv tools.

## 2026-06-25 - Supplement Package Mapping
- Nature presubmission supplement package mapping is implemented: docs/paper/supplement-package.md now maps article claims to protocol, source register, ontology validation, SHACL, mappings, SSSOM, metrics, figures, RO-Crate, DuckDB, SourceRight, arXiv, governance, and reuse artifacts.
- docs/paper/supplement-claim-map.csv provides a machine-readable claim-to-artifact table with support level and open-work fields.
- Track uogto_nature_presubmission_evaluation_20260625 supplement score is updated from 62 to 78 and status from reviewed/must-fix to mapped/should-fix; final journal supplement prose, final figure numbering, privacy audit manifest, figure loops, and deck creation remain open.

## 2026-06-25 - PowerPoint Deck Creation
- Created docs/presentation/uogto_nature_presubmission_deck.pptx from the required eight-slide Nature presubmission skeleton.
- Added docs/presentation/uogto_nature_presubmission_deck_scores.md and docs/presentation/uogto_nature_presubmission_deck_notes.md.
- Updated uogto_nature_presubmission_evaluation_20260625 PowerPoint status from needs-creation score 35 to created score 83; final figure binding, thumbnail export, readability inspection, and rescore loop remain open.

## 2026-06-25 - Figure Improvement Loop
- Regenerated ontology-comparison figures through `make ontology-comparison-visuals` with journal-scale typography, accessibility metadata, colourblind-safe palettes, network label simplification, caption/scale notes, and a ranked-bar replacement for the treemap.
- Added `scripts/maintenance/render_article_hardening_figures.py`, `make article-hardening-figures`, and PRISMA SVG/PDF exports for source discovery and screening flows.
- Updated Nature presubmission image scores so all 11 manuscript/supplement figures are rescored to 100/100 after loop 1.

- 2026-06-25T07:36:31+00:00: Added arXiv source-leak/privacy audit manifest (`docs/paper/arxiv-source-privacy-audit.json`, `docs/paper/arxiv-source-privacy-audit.md`) and wired `arxiv-privacy-audit` into preflight. Local package and audit targets passed; local full arXiv preflight remains LaTeX-engine blocked, with CI arXiv preflight green.

- 2026-06-25T07:46:06+00:00: CI evidence for arXiv source-leak/privacy manifest commit `a2ee99d` is green: Validate UOGTO 28154901094; arXiv Preflight 28154901098; Build WIDOCO Pages 28154901113; Build Manuscript PDF 28154901116.
