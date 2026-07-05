# Nature Must-Fix Submission Package Status

Generated: `2026-06-25T08:39:25+00:00`

| Order | Package item | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Manuscript rewrite scaffold | implemented-polished-draft | `docs/paper/paper.tex`; `docs/paper/authentext-report.md`; `docs/paper/authentext-report.json`; `make manuscript-check`; `make manuscript-sourcecheck` |
| 2 | Supplement prose | implemented-final-prose | `docs/paper/supplement-package.md`; `docs/paper/supplement-claim-map.csv`; `docs/paper/supplement-authentext-report.md`; `docs/paper/supplement-authentext-report.json`; `make manuscript-sourcecheck` |
| 3 | Privacy audit manifest | implemented-pass | `docs/paper/arxiv-source-privacy-audit.json`; `docs/paper/arxiv-source-privacy-audit.md`; CI arXiv Preflight run `28154901098` |
| 4 | Deck polish | implemented-final-polished | `docs/presentation/uogto_nature_presubmission_deck.pptx`; `docs/presentation/uogto_nature_presubmission_deck_scores.md`; `docs/presentation/uogto_nature_presubmission_deck_thumbnails/`; `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/powerpoint_recommendations.md` |
| 5 | Figure loops | implemented-loop-1 | `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.csv`; `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.md`; `docs/article-hardening/figures/`; `docs/ontology-comparison/figures/` |
| 6 | arXiv upload-ready package | implemented-local-provisional-ci-strict-pending | `make arxiv-upload-ready`; `scripts/maintenance/build_arxiv_upload_ready.py`; `docs/paper/arxiv-submission-process.md`; `docs/paper/arxiv-submission-contract.md`; `dist/arxiv/*` generated artifact set |

Remaining Nature-facing work is now limited to final submission freeze: keep manuscript and supplement claims synchronized, freeze figure numbering and captions, polish the PowerPoint deck against final figures, and rerun SourceRight, Authentext, arXiv, and validation gates after any citation or figure change.


## Manuscript editorial pass

Completed `2026-06-25T09:22:36+00:00`. The manuscript was rewritten for a tighter Nature-style claim hierarchy, reduced repo-process narration, integrated table/figure callouts, and restrained academic prose. SourceRight passed CSL validation and citation reconciliation; Authentext Pro academic audit passed after the humanization pass.


## Supplement editorial pass

Completed `2026-06-25T09:34:00+00:00`. `docs/paper/supplement-package.md` was converted from an evidence map into journal-style supplementary information with Supplementary Methods, Supplementary Results, Tables S1-S11, Figures S1-S7, a claim-to-supplement map, data/code availability, and completion criteria. SourceRight passed via `make manuscript-sourcecheck` with 11 matched citations and 0 citation reconciliation issues. Authentext Pro academic audit passed with 0 findings in `docs/paper/supplement-authentext-report.md` / `.json`.

## CI evidence after supplement/status cleanup

Recorded `2026-06-25T10:21:25+00:00` for commit `170399a`: Validate UOGTO `28163345123`, Build Manuscript PDF `28163345086`, Build WIDOCO Pages `28163345077`, and arXiv Preflight `28163345131` all completed successfully.

## PowerPoint deck polish

Completed `2026-06-25T10:50:25+00:00`. The deck is rebuilt as a valid PowerPoint-authored `.pptx`, bound to frozen manuscript/supplement evidence callouts, exported to 1920x1080 thumbnails, and rescored to 100/100.

## CI evidence after deck polish

Recorded `2026-06-25T10:55:55+00:00` for commit `22f9996`: Validate UOGTO `28165111146`, Build Manuscript PDF `28165111152`, Build WIDOCO Pages `28165111115`, and arXiv Preflight `28165111193` all completed successfully.

## Figure/caption freeze evidence (1574b09)

Completed `2026-06-25T12:45:00Z` and remotely verified on commit `1574b09783d46761178c1a0798b7f87da514f14b`.

`make figure-caption-freeze` now generates `docs/paper/figure-caption-freeze-manifest.md` and `docs/paper/figure-caption-freeze-manifest.json`. The manifest freezes manuscript figure callouts, Supplementary Figures S1-S7, source/rendered file hashes, caption/title intent, and image-score-loop status. The submission package must rerun the image score loop if any frozen callout, caption, numbering, placement, path, hash, or deck placement changes before submission.

CI evidence:
- Validate UOGTO: success, run 28170678354
- Build Manuscript PDF: success, run 28170678355
- Build WIDOCO Pages: success, run 28170678491
- arXiv Preflight: success, run 28170678436

## arXiv upload-ready gate

Implemented `2026-07-02`. `make arxiv-upload-ready` now runs the local arXiv preflight, requires the privacy audit manifest to pass, and generates an upload candidate plus provenance artifacts under `dist/arxiv/`: `uogto-arxiv-source.tar.gz`, `arxiv-submission-manifest.json`, `00README.json`, and `SHA256SUMS`.

Local source-package, privacy-audit, and upload-ready generation passed on 2026-07-02. The generated upload tarball SHA-256 is `23aad9174f75b2408071bca8b22e516941aa8760c7e481bb0463368f7cddd4c2`. The previous local PDF-compilation blocker is resolved for development: raw `make arxiv-upload-ready` now passes using `.pixi/envs/default/python.exe`, bundled Tectonic, and locally installed SourceRight `0.1.20`.

The strict arXiv-engine gate is deliberately stronger than the local fallback. `make arxiv-preflight-strict` currently fails locally because this workstation resolves bundled Tectonic rather than `latexmk` or `pdflatex`; the GitHub arXiv Preflight workflow is configured to install `latexmk`/TeX Live and run `make arxiv-upload-ready ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"`.

The CI arXiv Preflight workflow now runs the upload-ready target, retains `dist/arxiv/*` as the `uogto-arxiv-upload-ready` artifact for 90 days, and signs checksum-bound artifact provenance with GitHub artifact attestations on push/manual runs. The final remaining arXiv actions are: confirm a clean CI attestation, upload the tarball, inspect the arXiv-rendered PDF, complete `docs/paper/arxiv-post-submission-record-template.md`, and record the assigned arXiv identifier after acceptance.

## 2026-07-05 submission revision decision

The active route is arXiv-first, then journal-specific revision. Nature Human
Behaviour remains the primary aspirational venue only as a Resource-style
submission; Medical Decision Making / Medical Decision Making Policy & Practice
is the strongest alternative if the manuscript is refitted as a tutorial,
technical note, or methods explainer.

The current external arXiv state is recorded in
`docs/paper/arxiv-submission-state.md` as `not_submitted`: no identifier is
assigned, no version is assigned, and the arXiv-rendered PDF has not been
inspected. The final manifest and tarball hashes must come from the successful
clean CI arXiv Preflight artifact selected for upload, not from a local
dirty-tree run.

Devil's advocate review update `2026-07-02`: final submission status is `do-not-submit-yet` until clean strict-engine CI, remote attestation, clean-tree manifest, and arXiv-rendered PDF inspection are complete. Red-team and devil's advocate review notes are archived under `docs/paper/reviews/`.
