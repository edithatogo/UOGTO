# arXiv Post-Submission Provenance Record Template

Copy this template into the release notes after arXiv assigns an identifier.

## Submission Identity

| Field | Value |
| --- | --- |
| arXiv identifier | `TODO` |
| arXiv version | `v1` |
| Submission date UTC | `TODO` |
| Submitter | `TODO` |
| Primary category | `TODO` |
| Secondary categories | `TODO` |
| License selected in arXiv UI | `TODO` |
| arXiv-rendered PDF inspected and approved | `TODO: yes/no, reviewer, timestamp` |

## Artifact Binding

| Field | Value |
| --- | --- |
| Git commit | `TODO` |
| Git branch/tag | `TODO` |
| Upload manifest SHA-256 | `TODO` |
| Upload tarball SHA-256 | `TODO` |
| `SHA256SUMS` SHA-256 | `TODO` |
| GitHub Actions arXiv Preflight run URL | `TODO` |
| GitHub artifact attestation URL or verification command | `TODO` |
| Release tag | `TODO` |
| Zenodo DOI | `TODO` |

## Post-Submission Updates

- [ ] Record arXiv ID in `docs/releases/`.
- [ ] Record arXiv ID in citation metadata.
- [ ] Update publication-status artifacts.
- [ ] Link GitHub release, Zenodo DOI, and arXiv version.
- [ ] Archive the exact upload-ready artifact set or release asset.
- [ ] Re-run `make validate`.
- [ ] Re-run `make test`.
