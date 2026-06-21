# Implementation Plan: Manuscript Source Verification

## Phase 1: Source Inventory and Normalization
- [x] Task: Extract source candidates from `docs/deep_research_part*.md`, `docs/references.md`, `docs/review/protocol.md`, and `data/processed/`.
- [x] Task: Remove generated tracking parameters and normalize URLs, DOIs, arXiv IDs, titles, authors, and publication years.
- [x] Task: Classify entries as scholarly source, web standard/specification, software/tool reference, or placeholder requiring review.

## Phase 2: SourceRight Workspace and CSL
- [x] Task: Create `docs/paper/references.csl.json` from normalized source records.
- [x] Task: Run `sourceright validate-csl --json docs/paper/references.csl.json`.
- [x] Task: Generate a SourceRight report and review queue for unresolved metadata, conflicts, or low-confidence records.

## Phase 3: Manuscript Citation Integration
- [x] Task: Add citation commands and bibliography configuration to `docs/paper/paper.tex`.
- [x] Task: Reconcile in-text citations with SourceRight using a text export of the manuscript.
  - SourceRight 0.1.20 reconciled the SourceRight-compatible numeric manuscript export: 11 citation occurrences, 11 matched citations, 0 issues. Output is preserved in `docs/paper/sourceright-citations.md`.
- [x] Task: Document the reproducible SourceRight and manuscript build commands in the track or manuscript README.
  - Rebuild inventory: `make manuscript-sources` or `pixi run manuscript-sources`.
  - Check local LaTeX citation-key drift: `make manuscript-check`.
  - Validate CSL: `sourceright validate-csl --json docs/paper/references.csl.json`.
  - Generate report: `sourceright report .sourceright`.
  - Reconcile citations: `sourceright citations docs/paper/manuscript-citations.txt .sourceright`.

## Phase 4: Verification
- [x] Task: Run SourceRight CSL validation and citation reconciliation.
  - CSL validation passed. Citation reconciliation reports 11 occurrences, 11 matches, and 0 issues.
- [ ] Task: Run manuscript build/check command once available.
- [x] Task: Run repository validation gates after source artifacts are added.
  - Focused manuscript source tests passed, `make validate` passed, and the commit hook ran the repository validation gate successfully for commit `e90946b`.
  - `make manuscript-sourcecheck` passes with local LaTeX citation-key reconciliation, SourceRight CSL validation, SourceRight reference reporting, and SourceRight citation reconciliation.
