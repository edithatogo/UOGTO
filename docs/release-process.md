# Release Process
1. Verify with `make all`.
2. Increment version in `pyproject.toml` and `ontologies/core/uogto-core.ttl`.
3. Build assets using `make build`.
4. Verify publishing metadata with `make publishing-metadata`.
5. Build or verify WIDOCO documentation before release.
6. Enable Zenodo GitHub integration for `edithatogo/UOGTO`.
7. Create a GitHub release tag such as `v1.0.0` only after validation, tests, semantic audit, and documentation checks pass.
8. Build `make zenodo-packet` and attach `dist/zenodo-handoff.json` to the release for DOI handoff review.
9. Record the minted Zenodo DOI in `docs/releases/v1.0.md`, `docs/registry/lov-submission.md`, and `docs/registry/ols-indexing.md`.
10. Submit registry requests after DOI and GitHub Pages documentation are live.

## arXiv Submission
- For TeX submissions, run `make arxiv-upload-ready` and verify the generated PDF before upload. The target runs `make arxiv-preflight`, privacy-audits the cleaned package, then emits `dist/arxiv/uogto-arxiv-source.tar.gz`, `dist/arxiv/arxiv-submission-manifest.json`, `dist/arxiv/00README.json`, and `dist/arxiv/SHA256SUMS`.
- Treat local Tectonic PDF builds as provisional development evidence only. Final publisher sign-off requires a clean GitHub arXiv Preflight run using `ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"`.
- Treat `dist/arxiv/uogto-arxiv-source.tar.gz` as the upload candidate and `dist/arxiv/00README.json` as a processing-settings preview unless the arXiv UI or a programmatic submission path requires including it.
- Follow the detailed checklist in `docs/paper/arxiv-submission-process.md`.
- After arXiv assigns an identifier, complete `docs/paper/arxiv-post-submission-record-template.md` with the arXiv ID/version, PDF approval, upload manifest SHA, commit, CI run, attestation, release tag, and Zenodo DOI.
- This follows arXiv's TeX processing model, which requires submitters to view and confirm the rendered PDF during submission.
