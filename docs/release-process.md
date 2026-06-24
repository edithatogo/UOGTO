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
- For TeX submissions, run `make arxiv-preflight` and verify the generated PDF before upload.
- This follows arXiv's April 2025 TeX processing update, which requires submitters to view and confirm the rendered PDF during submission.
