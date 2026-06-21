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
  - Check local LaTeX citation-key drift: `make manuscript-check` or `pixi run manuscript-check`.
  - Check manuscript TeX build readiness: `make manuscript-build` or `pixi run manuscript-build`.
  - Require strict PDF compilation on a LaTeX-equipped release machine: `make manuscript-pdf` or `pixi run manuscript-pdf`.
  - Run the strict PDF gate in CI through `.github/workflows/manuscript-pdf.yml`, which installs LaTeX and executes `make manuscript-pdf`.
  - Validate CSL: `sourceright validate-csl --json docs/paper/references.csl.json`.
  - Generate report: `sourceright report .sourceright`.
  - Reconcile citations: `sourceright citations docs/paper/manuscript-citations.txt .sourceright`.

## Phase 4: Verification
- [x] Task: Run SourceRight CSL validation and citation reconciliation.
  - CSL validation passed. Citation reconciliation reports 11 occurrences, 11 matches, and 0 issues.
- [x] Task: Run manuscript build/check command once available.
  - `make manuscript-build` runs citation checks plus TeX structure validation and compiles a PDF when `latexmk`, `tectonic`, or `pdflatex` is installed.
  - `make manuscript-pdf` requires a LaTeX engine and fails explicitly when PDF output cannot be produced.
- [x] Task: Run repository validation gates after source artifacts are added.
  - Focused manuscript source/build tests passed, `make manuscript-build` passed, `make manuscript-sourcecheck` passed, `make validate` passed, and `make test` passed.
  - Pixi tasks are wired for `manuscript-check`, `manuscript-build`, `manuscript-pdf`, and `manuscript-sourcecheck`. A GitHub Actions workflow now provides a LaTeX-equipped strict PDF lane; local Windows PDF compilation is still not claimed because no local TeX engine is installed.
