# Specification: Nature-Ready Presubmission Evaluation and Improvement

## Purpose

This track defines a Nature-standard presubmission evaluation of UOGTO from the perspective of a professor of game theory, supported by specialist reviewers for ontology engineering, simulation methods, reproducibility, editorial framing, statistics/network analysis, visual communication, and red-team critique.

## Scope

The review covers:

- GitHub documentation, repository setup, validation, release readiness, citation, reuse, and governance.
- Ontology design, game-theory coverage, modelling quality, mappings, SHACL, examples, competency queries, and source evidence.
- Evaluation protocol, scoping-review evidence package, analysis artefacts, RO-Crate, DuckDB, SSSOM, quality metrics, reviewer decisions, and figures.
- Manuscript, supplement, bibliography, arXiv readiness, claim discipline, and venue fit.
- PowerPoint narrative, slide-level evidence, and presentation design.
- All manuscript, supplement, dashboard, and slide images.
- arXiv submission hardening tools, package cleaning, source-leak/privacy checks, TeX Live compatibility, and generated-PDF verification.

## Known Initial Review Targets

- `docs/paper`: manuscript, bibliography, and seed article readiness.
- `docs/article-hardening`: protocol, evidence package, RO-Crate, metrics, dashboard, source inventories, and supplementary-material candidates.
- `docs/ontology-comparison`: ontology mapping report and comparison figures.
- `validation_report.html`: rendered validation evidence.
- `scripts/maintenance/build_manuscript_pdf.py` and `.github/workflows/manuscript-pdf.yml`: manuscript build/reproducibility surfaces.
- `scripts/maintenance/build_arxiv_source_package.py`, `scripts/maintenance/clean_arxiv_source_package.py`, and `docs/release-process.md`: arXiv package cleaning and preflight surfaces.
- PowerPoint/deck assets: deck now exists at `docs/presentation/uogto_nature_presubmission_deck.pptx`; remaining checks are thumbnail export, final figure binding, and readability re-score.

## Out of Scope

This track does not directly rewrite ontology modules, regenerate analysis artefacts, or redesign figures. It creates the presubmission evaluation protocol, reviewer lanes, scoring matrices, image improvement loop, and implementation backlog. Subsequent implementation tracks may apply the recommended fixes.

## Acceptance Criteria

- Track is registered in `conductor/tracks.md`.
- Track has metadata, specification, plan, index, protocol, matrices, reviewer reports, recommendation backlog, and decision memo scaffold.
- Rubrics are explicit enough for a reviewer to score each surface out of 100.
- Image improvement loop requires inventory, scoring, concrete fixes, and re-scoring until 100/100 or blocker.
- Every reviewer lane has a role definition, required checks, and required output.
- arXiv toolchain review compares candidate tools against the repo-native cleaner and does not replace the authoritative gate unless the benchmark shows stricter behaviour without destructive side effects.
- `.conductor/status.md` and `.conductor/runlog.md` record the track creation.
- Validation checks are run and any blockers are recorded.

## 2026-06-25 Asset-Blocker Supersession
- The earlier PowerPoint/deck asset discovery blocker is superseded by the created deck at `docs/presentation/uogto_nature_presubmission_deck.pptx` and the slide scorecard under `docs/presentation/`.
- Missing local arXiv tools are superseded as submission blockers by CI arXiv Preflight evidence; they remain optional advisory benchmark tools only.

## 2026-06-25T10:13:36+00:00 Current Implementation Boundary
- This track now records completed supplement prose, privacy audit, deck creation, and manuscript/supplement figure loop. Remaining work is final freeze-and-verify plus PowerPoint readability polish, not initial asset creation.

## 2026-07-06 Archive Boundary
- The presubmission evaluation package is repo-complete and archived.
- Remaining submission work is governed by `docs/paper/submission-revision-backlog.csv` and `docs/paper/arxiv-submission-state.md`, not by this evaluation setup track.
