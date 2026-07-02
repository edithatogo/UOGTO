# Specification: Repo and arXiv Submission Hardening

## Overview

This chore track finishes repository contribution polish and adds a strict arXiv submission-review simulation for the UOGTO manuscript/package. The track is locally complete only when the repository contribution surface is clear, CI has a single aggregate gate suitable for branch protection, and the arXiv review simulation reports a score above `995/1000` with no blockers.

The arXiv review model is grounded in current official arXiv guidance:

- Submission overview: https://info.arxiv.org/help/submit/index.html
- Format requirements: https://info.arxiv.org/help/policies/format_requirements.html
- TeX submissions: https://info.arxiv.org/help/submit_tex.html
- Common TeX processing mistakes: https://info.arxiv.org/help/faq/mistakes.html
- Metadata fields: https://info.arxiv.org/help/prep.html
- 00README and bibliography behavior: https://info.arxiv.org/help/00README.html
- TeX Live package list: https://info.arxiv.org/help/texlive_package_list.html

## Functional Requirements

- Finish the `master` to `main` cleanup by removing stale `master` workflow triggers where they are no longer needed, especially from the WIDOCO Pages workflow.
- Preserve remote `master` until workflow references and branch-protection dependencies are safely migrated.
- Expand the public contribution path with:
  - ontology-change contribution requirements;
  - public issue templates for ontology change proposals, validation failures, documentation fixes, bug reports, and questions/discussion redirects;
  - a stronger pull request template covering ontology, SHACL, examples, competency queries, documentation, manuscript, release, and RI-HERO impacts;
  - standard GitHub labels for external contributors.
- Make dual licensing more machine-readable while preserving the existing ontology/docs CC-BY-4.0 and code/tooling MIT split.
- Add a single always-running GitHub Actions workflow named `Required Gate` that can be used as the aggregate required branch-protection check.
- Add strict arXiv scoring artifacts:
  - `docs/paper/arxiv-strict-review-rubric.md`;
  - `docs/paper/arxiv-strict-review-report.md`;
  - `docs/paper/arxiv-strict-review-iterations.jsonl`;
  - `scripts/maintenance/score_arxiv_submission.py`.
- Simulate strict arXiv reviewer roles covering compliance, TeX/source processing, metadata/category fit, copyright/license, source leaks, manuscript readability, and publisher/provenance.
- Score the submission out of `1000` with blocker overrides, category floors, and a pass threshold of `>995/1000`.
- Record any additional repo or paper improvements found during scoring as either fixed items or explicit follow-up recommendations.

## Non-Functional Requirements

- Preserve the existing uncommitted `docs/paper/paper.tex` changes.
- Keep actual arXiv upload, arXiv-rendered PDF inspection, and arXiv identifier recording as manual external steps.
- Do not claim external arXiv acceptance from local or CI checks.
- Keep validation reproducible through Makefile and Pixi tasks where practical.
- Keep Conductor status and runlog evidence aligned with completed work.

## Acceptance Criteria

- The Conductor track exists with `spec.md`, `plan.md`, `metadata.json`, and `index.md`, and is registered in `conductor/tracks.md`.
- Contribution docs/templates exist for common external contribution flows.
- WIDOCO Pages and validation workflows no longer require `master` branch triggers for normal pushes/PRs.
- `Required Gate` exists and runs the repo, metadata, manuscript, and strict arXiv scoring gates.
- The strict arXiv score report records `>995/1000`, no blockers, and no category below `98%`.
- Tests cover the scoring script, strict-review documents, new issue templates, PR template, and required-gate workflow.
- Local validation commands are run and outcomes are recorded.

## Out of Scope

- Submitting the manuscript to arXiv.
- Removing remote `master` before the new `main`-only workflows and branch-protection settings are proven.
- Claiming journal peer review, arXiv acceptance, or arXiv-rendered PDF approval before those external events occur.
