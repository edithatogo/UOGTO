# arXiv Submission State

Updated: `2026-07-05`

This file records the live arXiv submission state for the UOGTO manuscript. It is
deliberately separate from the post-submission template so the repository can
track the external blocker without pretending that an identifier exists.

## Status

| Field | Current value |
| --- | --- |
| Submission state | `not_submitted` |
| arXiv identifier | `not assigned` |
| arXiv version | `not assigned` |
| arXiv-rendered PDF inspected | `no` |
| arXiv-rendered PDF approval state | `blocked_until_external_upload` |
| Submitter | `not recorded` |
| Submission date UTC | `not recorded` |
| Primary category | proposed `cs.AI`; final choice belongs to the registered submitting author in the arXiv UI |
| Cross-list candidates | `cs.MA`; `econ.TH`, subject to arXiv UI availability and author approval |
| License selected in arXiv UI | `not recorded` |

## Current Repository Evidence

| Evidence item | State |
| --- | --- |
| Source package process | `docs/paper/arxiv-submission-process.md` |
| Editor/reviewer/publisher contract | `docs/paper/arxiv-submission-contract.md` |
| Post-submission record template | `docs/paper/arxiv-post-submission-record-template.md` |
| Privacy audit | `docs/paper/arxiv-source-privacy-audit.md`; `.json` |
| Strict scoring report | `docs/paper/arxiv-strict-review-report.md` |
| Final manifest SHA-256 | pending the successful clean CI arXiv Preflight artifact used for upload |
| Final tarball SHA-256 | pending the successful clean CI arXiv Preflight artifact used for upload |
| Final `SHA256SUMS` SHA-256 | pending the successful clean CI arXiv Preflight artifact used for upload |
| GitHub Actions arXiv Preflight run | pending current branch CI after the submission-revision commit |
| GitHub artifact attestation | pending current branch CI after the submission-revision commit |

## Closeout Rule

This track can be repo-complete with the arXiv identifier still unassigned
because identifier assignment and rendered-PDF inspection require an external
registered-author arXiv upload. Do not mark the external submission complete
until all of the following fields are replaced with concrete values:

- arXiv identifier.
- arXiv version.
- arXiv-rendered PDF inspection timestamp and approver.
- Upload manifest SHA-256 from the uploaded clean CI artifact.
- Upload tarball SHA-256 from the uploaded clean CI artifact.
- `SHA256SUMS` SHA-256 from the uploaded clean CI artifact.
- GitHub Actions arXiv Preflight run URL.
- GitHub artifact attestation verification command or URL.

## Update Procedure After External Upload

1. Copy `docs/paper/arxiv-post-submission-record-template.md` into the relevant
   release notes or publication-status record.
2. Replace all `TODO` values with the arXiv identifier, version, submitter,
   category, licence, artifact hashes, CI run, attestation evidence, release
   tag, and Zenodo DOI where available.
3. Update this state file from `not_submitted` to the actual state.
4. Re-run `make validate`, `make test`, and the current manuscript/arXiv gates.
