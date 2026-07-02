# arXiv Submission Contract Workflow

## Purpose

This workflow coordinates editor, reviewer, and publisher agents for the UOGTO arXiv submission package. It complements the article-hardening research/review workflows by adding a publication-facing contract gate.

## Agent Registry

Use `conductor/agents/arxiv-submission-agents.json`.

Required role groups:

- editor agents
- reviewer agents
- devil's advocate reviewer
- publisher agents

## Contract Steps

1. Confirm the latest manuscript and article evidence artifacts are generated.
2. Assign editor agents to check claim discipline, citation reconciliation, figure/caption freeze, methods wording, and evidence-limit wording.
3. Assign reviewer agents to check arXiv toolchain behavior, privacy/source-leak audit status, package contents, and warning disposition.
4. Assign a distinct devil's advocate reviewer to argue against submission readiness unless the evidence supports the manuscript/process claims.
5. Assign publisher agents to check manifest/checksum handoff, CI artifact retention, provenance attestation, and manual arXiv upload instructions.
6. Record sign-off, executed agent run identifiers, evidence paths, warnings, and remaining external steps in `docs/paper/arxiv-submission-contract.md`.
7. Run `make arxiv-upload-ready`.
8. Run `make validate`.
9. Run `make test`.
10. Treat any failed command, failed privacy audit, missing upload artifact, missing checksum, unresolved citation reconciliation issue, or unresolved devil's advocate `fix_now` finding as a blocker.
11. Treat arXiv upload, arXiv-rendered PDF inspection, and arXiv identifier recording as external manual steps, not local automation blockers.

## Strict Contract

The submission is locally upload-ready only when all of the following are true:

- `make arxiv-upload-ready` passes.
- `dist/arxiv/uogto-arxiv-source.tar.gz` exists.
- `dist/arxiv/arxiv-submission-manifest.json` exists.
- `dist/arxiv/SHA256SUMS` exists and includes the tarball.
- `docs/paper/arxiv-source-privacy-audit.json` has status `pass`.
- SourceRight citation reconciliation reports 0 issues.
- Editor/reviewer/devil's-advocate/publisher sign-off is recorded in `docs/paper/arxiv-submission-contract.md`.
- `make validate` passes.
- `make test` passes.

Final publisher sign-off also requires:

- The upload-ready manifest is generated from a clean commit or records a dirty tree as a blocker.
- The GitHub arXiv Preflight workflow passes with `ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"`.
- The upload artifact set is retained and attested from `dist/arxiv/SHA256SUMS`.
- The completed arXiv post-submission record links the arXiv ID, rendered-PDF approval, manifest hash, commit, CI run, attestation, release tag, and Zenodo DOI.

## Output Standard

The contract document must include:

- assigned agent ids,
- executed Codex agent run ids where subagents were used,
- reviewed artifacts,
- contract checks,
- result status,
- warning dispositions,
- fixes applied,
- validation evidence,
- remaining external/manual steps.
