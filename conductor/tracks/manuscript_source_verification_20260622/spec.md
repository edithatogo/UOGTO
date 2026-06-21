# Specification: Manuscript Source Verification (`manuscript_source_verification_20260622`)

## Overview
This track covers SourceRight-backed source verification for the UOGTO manuscript. The current paper source exists at `docs/paper/paper.tex`; it now has explicit citation commands, a manual bibliography, canonical CSL JSON, SourceRight sidecar files, and generated report artifacts.

## Scope
- Build a canonical manuscript source inventory from `docs/deep_research_part*.md`, `docs/references.md`, review protocol outputs, and literature-review data files.
- Remove generated tracking parameters such as `utm_source=chatgpt.com` from source URLs before citation normalization.
- Create `docs/paper/references.csl.json` as the canonical SourceRight input.
- Use SourceRight to validate CSL, produce an integrity report, and reconcile in-text manuscript citations.
- Update manuscript citation and bibliography plumbing so source checks are reproducible.

## Out of Scope
- Treating SourceRight as a substitute for final expert source review.
- Claiming all sources are verified before SourceRight outputs and any review queue are inspected.
- Rewriting ontology semantics based on manuscript source verification without a separate ontology-design track.

## Acceptance Criteria
- [x] `docs/paper/references.csl.json` exists and passes `sourceright validate-csl`.
- [x] SourceRight report output is generated and committed in a compact reviewable form.
- [x] Any uncertain or conflicting records are captured in a review queue or explicit TODO section.
- [~] `docs/paper/paper.tex` contains citation commands that reconcile against the canonical references.
  - The manuscript contains citation commands and all cited keys exist in the canonical CSL. SourceRight 0.1.20 citation reconciliation currently detects zero citation occurrences from the text export, so tool-level reconciliation remains open.
- [~] Manuscript build/check commands still pass after citation integration.
  - Repository validation and focused manuscript-source tests passed. A dedicated LaTeX/PDF manuscript build command is not yet available in this repository.
