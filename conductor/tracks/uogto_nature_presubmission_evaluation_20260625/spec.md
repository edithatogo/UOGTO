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

## Known Initial Review Targets

- `docs/paper`: manuscript, bibliography, and seed article readiness.
- `docs/article-hardening`: protocol, evidence package, RO-Crate, metrics, dashboard, source inventories, and supplementary-material candidates.
- `docs/ontology-comparison`: ontology mapping report and comparison figures.
- `validation_report.html`: rendered validation evidence.
- `scripts/maintenance/build_manuscript_pdf.py` and `.github/workflows/manuscript-pdf.yml`: manuscript build/reproducibility surfaces.
- PowerPoint/deck assets: not yet located; record as blocker until a deck exists or a new slide inventory is created.

## Out of Scope

This track does not directly rewrite ontology modules, regenerate analysis artefacts, or redesign figures. It creates the presubmission evaluation protocol, reviewer lanes, scoring matrices, image improvement loop, and implementation backlog. Subsequent implementation tracks may apply the recommended fixes.

## Acceptance Criteria

- Track is registered in `conductor/tracks.md`.
- Track has metadata, specification, plan, index, protocol, matrices, reviewer reports, recommendation backlog, and decision memo scaffold.
- Rubrics are explicit enough for a reviewer to score each surface out of 100.
- Image improvement loop requires inventory, scoring, concrete fixes, and re-scoring until 100/100 or blocker.
- Every reviewer lane has a role definition, required checks, and required output.
- `.conductor/status.md` and `.conductor/runlog.md` record the track creation.
- Validation checks are run and any blockers are recorded.
