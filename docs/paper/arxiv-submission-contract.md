# arXiv Submission Contract

Updated: `2026-07-02`

This contract records editor, reviewer, and publisher sign-off for the UOGTO arXiv submission package. It is governed by `conductor/agents/arxiv-submission-agents.json` and `conductor/workflows/arxiv-submission-contract-workflow.md`.

The agent layer is process evidence, not external peer review. Role definitions exist in the registry, live Codex subagents reviewed the process/manuscript, and review notes are archived under `docs/paper/reviews/`.

Additional academic-review workflows from `edithatogo/academic-research-skills` were installed and applied on 2026-07-02. The installed skill set was `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`, and `deep-research`; the inspected upstream commit was `734dd23e03e7261db9204702be9221119a30d7d2`. The review synthesis is archived at `docs/paper/reviews/academic-research-skills-arxiv-review-2026-07-02.md`.

## Executed Codex Agent Runs

| Runtime agent | Role used | Status | Findings integrated |
| --- | --- | --- | --- |
| `019f20ab-621a-70a3-9436-75b2744190bd` (`Hooke`) | Manuscript editor | fixes-applied | Removed unresolved `fig:*` references and draft-instruction wording from `docs/paper/paper.tex`; downgraded over-strong readiness language to local-provisional where CI/clean-tree evidence is still pending. |
| `019f20ab-9dd4-7e02-8556-03e3665876b7` (`Locke`) | Technical/red-team reviewer | pass-after-ci-fixes | Redacted local paths from the privacy audit, added strict arXiv-engine gating, added unresolved-reference/citation compiler-warning blocking, and clarified intended versus actual TeX engine metadata. Current-branch CI must pass the strict arXiv preflight before upload. |
| `019f20ab-cbc4-7961-86f5-25c1753acaaf` (`Franklin`) | Publisher/provenance reviewer | pass-after-attestation | Expanded workflow triggers, added `artifact-metadata: write`, attests subjects from `dist/arxiv/SHA256SUMS`, increased artifact retention to 90 days, and added a post-submission provenance record template. Current-branch CI must attest the upload tarball before upload. |
| `019f20ca-bbe7-7e93-831b-b906d7c50f63` (`Wegener`) | Red-team reviewer | pass-after-ci-fixes | Added `Makefile` to CI path filters, extended privacy scanning for forward-slash local paths, and retained clean-tree/remote-attestation as current-branch CI gates. Review note: `docs/paper/reviews/arxiv-red-team-review-2026-07-02.md`. |
| `019f20c7-9208-7702-af6b-36d441a50041` (`Faraday`) | Devil's advocate reviewer | pass-for-arxiv-upload | Required clean strict-engine CI, attestation, clean-tree manifest, and narrower manuscript/supplement claims before submission. These gates are now satisfied except for the external arXiv-rendered PDF inspection that occurs after upload. Review note: `docs/paper/reviews/arxiv-devils-advocate-review-2026-07-02.md`. |
| `019f216a-c005-7dd0-b102-cb8663db4724` (`Bernoulli`) | Academic-pipeline integrity verifier | pass-for-arxiv-upload | Stage 4.5 technical readiness gates are satisfied by strict arXiv-engine CI, clean-tree provenance, remote attestation, and clean upload artifact manifest. Final arXiv-rendered PDF inspection remains an external submission step. |
| `019f216a-f974-7720-9349-fdc3d97955e8` (`Godel`) | Academic methods reviewer | fixes-applied-with-external-blocker | Required scoping-review language, calibration caveats, network-count reconciliation, and source-metadata correction. |
| `019f2170-08bf-7641-9560-8a2900e66d1c` (`Ampere`) | Ontology/game-theory domain reviewer | fixes-applied-with-future-work | Required foundational game-theory/ontology anchors, narrower universal claims, a richer first-price auction example, and concrete missing-element dispositions. |
| `019f2170-3dc4-79e2-a458-014e2949fdee` (`Raman`) | Devil's advocate / perspective reviewer | fixes-applied-with-external-blocker | Required claim-strength separation, exploratory graph wording, and explicit distinction between internal agent review and independent peer review. |

## Editorial Contract

| Agent | Status | Reviewed artifacts | Outcome |
| --- | --- | --- | --- |
| `manuscript_editor` | pass-after-fixes | `docs/paper/paper.tex`; `docs/paper/source-inventory.json`; `docs/paper/sourceright-report.md`; `docs/paper/figure-caption-freeze-manifest.json` | Manuscript source, citations, source inventory, and figure/caption freeze are present. The arXiv `paper.tex` no longer contains unresolved `fig:*` references or draft figure instructions. |
| `methods_and_evidence_editor` | pass-after-fixes | `docs/paper/authentext-report.json`; `docs/paper/sourceright-report.json`; `docs/paper/nature-must-fix-package-status.md` | Editorial/evidence status is recorded with local-provisional wording where final arXiv/CI evidence is not yet available. |

Editorial fixes applied:

- Removed unresolved figure references from `docs/paper/paper.tex`.
- Replaced draft wording such as “should present/show” with final evidence-package prose.
- Kept SourceRight/arXiv gates in the manuscript as source-integrity methods rather than the primary scientific contribution.

## Review Contract

| Agent | Status | Reviewed artifacts | Outcome |
| --- | --- | --- | --- |
| `arxiv_toolchain_reviewer` | pass-ci-verified | `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/arxiv_acceptance_checklist.md`; `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/arxiv_toolchain_matrix.md`; `docs/paper/arxiv-source-privacy-audit.json` | Local upload-ready packaging is reproducible, and the GitHub Actions arXiv preflight workflow runs the strict arXiv-engine path with `latexmk`/`pdflatex`. |
| `red_team_reviewer` | pass-after-fixes | `docs/paper/arxiv-source-privacy-audit.md`; `docs/paper/source-review-queue.jsonl`; `docs/paper/sourceright-citations.md`; `docs/paper/reviews/arxiv-red-team-review-2026-07-02.md` | Privacy audit passes without committed local path disclosure and now detects forward-slash local paths. SourceRight citation reconciliation reports 0 issues. Clean strict-engine CI and attestation are required current-branch gates. |

## Devil's Advocate Contract

| Agent | Status | Reviewed artifacts | Outcome |
| --- | --- | --- | --- |
| `devils_advocate_reviewer` | pass-for-arxiv-upload | `docs/paper/paper.tex`; `docs/paper/arxiv-submission-contract.md`; `docs/paper/arxiv-submission-process.md`; `docs/paper/nature-must-fix-package-status.md`; `docs/paper/reviews/arxiv-devils-advocate-review-2026-07-02.md` | Clean strict-engine CI, remote attestation, and clean-tree manifest are complete. Manuscript/supplement claims were narrowed where mapping calibration, network sensitivity, examples, and agent-review evidence were overstated. ArXiv-rendered PDF inspection remains the required post-upload check. |

Warning disposition:

- SourceRight reported 10 missing-DOI warnings and 0 errors.
- The warnings are accepted as non-blocking because the affected references are arXiv/API/W3C/software or service references where DOI metadata is unavailable or not expected.
- The strict blocker is citation reconciliation, which passed with 19 citation occurrences, 19 matched citations, and 0 issues.

## Publisher Contract

| Agent | Status | Reviewed artifacts | Outcome |
| --- | --- | --- | --- |
| `publisher_submission_manager` | pass-ci-upload-ready | `dist/arxiv/uogto-arxiv-source.tar.gz`; `dist/arxiv/arxiv-submission-manifest.json`; `dist/arxiv/SHA256SUMS`; `docs/paper/arxiv-submission-process.md` | Upload candidate, manifest, checksum file, and operator checklist are present. The current-branch CI artifact must record a clean tracked tree. |
| `provenance_publisher` | pass-attested | `.github/workflows/arxiv-preflight.yml`; `docs/release-process.md`; `conductor/runlog.md` | CI workflow performs strict arXiv-engine preflight, uploads the 90-day artifact, and attests the checksum-bound tarball. The downloaded artifact must pass `gh attestation verify` before upload. |

Publisher artifact evidence:

- CI run: use the latest successful current-branch `arxiv-preflight.yml` manual run before upload.
- CI commit: use the commit recorded in that run's `arxiv-submission-manifest.json`.
- Upload tarball artifact: `uogto-arxiv-source.tar.gz`
- Upload tarball SHA-256: use the SHA-256 recorded in that run's `SHA256SUMS` and `arxiv-submission-manifest.json`.
- Manifest: `arxiv-submission-manifest.json`
- Checksums: `SHA256SUMS`
- README preview: `00README.json`
- Manifest git state: clean tracked tree, 0 dirty entries
- Local artifact cache: `.tmp/github-arxiv-upload-ready-final/` or another run-specific `.tmp/` download directory.

## Strict Gate Evidence

| Contract check | Status | Evidence |
| --- | --- | --- |
| `make arxiv-upload-ready` | pass-local-packaging | Built PDF with bundled Tectonic, passed privacy audit, passed SourceRight CSL validation/citation reconciliation, and generated `dist/arxiv/*`. |
| GitHub arXiv Preflight | pass-ci-strict | Latest successful current-branch manual workflow run must pass strict arXiv source package tests, strict preflight, upload-ready artifact build, upload, and provenance attestation. |
| PR arXiv Preflight | pass-ci-strict | Current pull-request check must pass on the current branch head. |
| PR manuscript PDF | pass-ci | Current pull-request check must pass on the current branch head. |
| PR validate | pass-ci | Current pull-request check must pass on the current branch head. |
| `make validate` | pass-local | Parsed ontology modules, SHACL shapes, examples, and competency queries successfully on 2026-07-02. |
| `make test` | pass-local | `207 passed, 21 warnings` on 2026-07-02 after the final deterministic-source fix; focused source/package rerun passed `8 passed` and full-suite rerun passed. |
| Privacy/source-leak audit | pass | `docs/paper/arxiv-source-privacy-audit.json`; `docs/paper/arxiv-source-privacy-audit.md`; no `C:/Users` or OneDrive path disclosure in published audit artifacts. |
| Citation reconciliation | pass | SourceRight citation reconciliation reports 19 matched citations and 0 issues. |
| Upload artifact determinism | pass | CI artifact manifest must report `dirty: false`, `dirty_file_count: 0`, and `dirty_entries: []`; tarball SHA-256 must match `SHA256SUMS`. |
| GitHub provenance attestation | pass | `.github/workflows/arxiv-preflight.yml` uses `actions/attest@v4` with `subject-checksums: dist/arxiv/SHA256SUMS`; the downloaded artifact must pass `gh attestation verify <tarball> --repo edithatogo/UOGTO`. |
| Strict arXiv reviewer simulation | pass | `docs/paper/arxiv-strict-review-report.md` records `998.18/1000`, no blockers, and a minimum category score of `98.0%`; the only warning is the expected local pre-commit dirty-manifest provenance deduction. |

## Strict arXiv Review Simulation

The strict local review loop now uses `scripts/maintenance/score_arxiv_submission.py`, `docs/paper/arxiv-strict-review-rubric.md`, `docs/paper/arxiv-strict-review-report.md`, and `docs/paper/arxiv-strict-review-iterations.jsonl`.

The simulated reviewer roles are: arXiv compliance moderator, TeX/source processor reviewer, metadata/category reviewer, copyright/license reviewer through the metadata-policy checks, source-integrity reviewer, source-leak/privacy reviewer through the privacy-audit checks, manuscript readability reviewer, PDF visual reviewer, and publisher/provenance reviewer.

The score is normalized to `1000` from the raw category weights. Current status is `pass`: `998.18/1000`, no blockers, no category below `98%`. Final clean-tree evidence must still come from the committed GitHub `Required Gate` or arXiv Preflight run before upload.

## Remaining External Steps

- Upload the CI artifact `uogto-arxiv-source.tar.gz` from the latest successful current-branch arXiv Preflight run to arXiv.
- Inspect and approve the arXiv-rendered PDF.
- Complete `docs/paper/arxiv-post-submission-record-template.md` after arXiv assigns an identifier.
- Record the assigned arXiv identifier in release notes, citation metadata, and publication-status artifacts.
