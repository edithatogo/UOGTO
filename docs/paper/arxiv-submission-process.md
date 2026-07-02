# arXiv Submission Process

This process turns the manuscript source into a conservative arXiv upload candidate with machine-readable provenance.

Editor, reviewer, and publisher sign-off is recorded in `docs/paper/arxiv-submission-contract.md` and governed by `conductor/agents/arxiv-submission-agents.json`.

## Current Gate

Run:

```bash
make arxiv-upload-ready
```

This target runs the local arXiv preflight first, then writes local packaging artifacts. It is a development packaging gate, not final submission readiness evidence.

| Artifact | Purpose |
| --- | --- |
| `dist/arxiv/uogto-arxiv-source.tar.gz` | Upload candidate for arXiv's "Add Files" step. |
| `dist/arxiv/arxiv-submission-manifest.json` | Source package provenance, file hashes, TeX Live/compiler selection, privacy-audit summary, and git state. |
| `dist/arxiv/SHA256SUMS` | Checksums for the tarball, manifest, and `00README.json` preview. |
| `dist/arxiv/00README.json` | Review preview of intended arXiv processing settings. It is not included in the tarball by default. |

The tarball is deterministic for a stable cleaned package. The `00README.json` preview records the intended default processing path: `pdflatex` on TeX Live 2025. It is kept outside the upload archive by default because arXiv's current submission system normally generates `00README` during upload; include it only for programmatic or custom submissions after checking the arXiv UI.

Local builds may use bundled Tectonic when `latexmk` or `pdflatex` is unavailable. That is a development fallback only. Final publisher sign-off requires the GitHub arXiv Preflight workflow to run `make arxiv-upload-ready ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"` on a clean commit, so the PDF gate uses an arXiv-compatible `latexmk` or `pdflatex` path. A dirty-tree manifest, pending attestation, or unresolved red-team/devil's-advocate `fix_now` finding blocks submission.

## Operator Checklist

1. Freeze manuscript, supplement, figure numbering, and captions with `make figure-caption-freeze`.
2. Run `make arxiv-upload-ready`.
3. Review `.tmp/manuscript-build/paper.pdf` before upload.
4. Review `docs/paper/arxiv-source-privacy-audit.md` and confirm status is `pass`.
5. Review `dist/arxiv/arxiv-submission-manifest.json` and `dist/arxiv/SHA256SUMS`.
6. Review `docs/paper/arxiv-submission-contract.md` and confirm editor, reviewer, devil's advocate, and publisher sign-off is current.
7. Upload `dist/arxiv/uogto-arxiv-source.tar.gz` to arXiv.
8. In the arXiv UI, verify the selected processor and TeX Live version, then inspect the rendered PDF before final submission.
9. After arXiv assigns an identifier, complete `docs/paper/arxiv-post-submission-record-template.md` and record the identifier in release notes, citation metadata, and registry/publication status documents.

## Submission Metadata

The arXiv web form remains the authoritative submission surface. Use ASCII-only metadata and verify every field before final submission.

| Field | Current value or instruction |
| --- | --- |
| Title | `Universal Open Game Theory Ontology (UOGTO): An extensible semantic resource for strategic-interaction evidence` |
| Authors | `Dylan A Mordaunt` |
| Abstract | Use the manuscript abstract from `docs/paper/paper.tex`, converted to arXiv-safe plain text if needed. |
| Primary category | Proposed primary category: `cs.AI`, subject to arXiv endorsement and final author confirmation in the UI. |
| Cross-list candidates | Consider `cs.MA` and `econ.TH` only if arXiv permits the cross-list and the final author agrees. |
| Comments | Suggested: `Preprint; includes ontology-engineering methods, source-discovery evidence, and repository artefacts.` |
| Report number | Leave blank unless an institution supplies one. |
| Journal reference | Leave blank before journal publication. |
| DOI | Leave blank before journal DOI assignment. |

### Category rationale

The paper presents a machine-readable ontology and validation/repository workflow for strategic-interaction evidence. The proposed `cs.AI` primary category is appropriate because the work supports AI, multi-agent, simulation, and knowledge-graph uses. `cs.MA` and `econ.TH` may be relevant as cross-lists because game-theoretic and multi-agent content is central, but the final category choice must be made by the registered submitting author in the arXiv UI.

### Author and License Steps

- The paper must be submitted by Dylan A Mordaunt or another eligible registered arXiv author acting under arXiv's third-party submission rules.
- The intended path is author self-submit by a registered arXiv author.
- The submitting author must confirm any required endorsement before upload.
- The submitting author must agree to the arXiv submittal agreement, code of conduct, privacy policy, moderation policy, and irrevocable license to distribute the submitted work.
- Metadata should avoid non-ASCII punctuation copied from the PDF because arXiv metadata fields reject some Unicode characters.

## Replacement and Rollback Notes

If arXiv processing fails or the rendered PDF shows a material problem, do not approve the submission. Correct the source package, rebuild the upload-ready artifact, rerun the strict review gate, and upload a corrected source package. If a problem is discovered after announcement, prepare a replacement version and record the reason, arXiv identifier, source manifest, commit, and rendered-PDF inspection in the post-submission record.

## Implemented Controls

- Cleaned source package that excludes unused figures, auxiliary outputs, hidden files, private notes, journal templates, and unreferenced source files.
- Source-leak/privacy audit for comments, local paths, private URLs, credentials, embedded metadata, hidden files, and unreferenced figures.
- Deterministic upload tarball plus SHA-256 checksums.
- `00README.json` preview for compiler and TeX Live review without forcing custom arXiv processing by default.
- CI artifact retention through the `arXiv Preflight` workflow.
- GitHub artifact attestation for the checksum-bound upload artifact set on push and manual workflow runs.
- Makefile and Pixi task alignment so local and CI gates run the same privacy and upload-ready checks.

## Recommended Next Wave

- Add containerized TeX Live 2025 and 2023 matrix builds when reliable images are available for the current arXiv distribution snapshots.
- Add PDF visual regression checks against a frozen reference render after final figure/caption freeze.
- Add an explicit `anc/` packaging path only if data or code must be submitted as arXiv ancillary material; otherwise keep datasets and executable assets in release/Zenodo artifacts.
- Add a containerized TeX Live snapshot matrix when reliable arXiv-equivalent images are available; until then, treat the GitHub `latexmk`/`pdflatex` preflight and arXiv UI render as the binding publisher gates.

## Reference Constraints

- arXiv supports `tar.gz` and `zip` upload bundles for multi-file submissions and does not support `rar`, `bz`, or `bz2` archives.
- arXiv ancillary files belong under an `anc/` directory at the root of a `.tar.gz` or `.zip` package and are versioned with the article.
- arXiv currently supports TeX Live 2025 and 2023, with 2025 as the default.
- The current `00README` JSON format can record compiler and TeX Live selections, but manual creation is usually unnecessary for UI submissions.
