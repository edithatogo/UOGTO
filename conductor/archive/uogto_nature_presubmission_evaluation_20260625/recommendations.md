# Recommendations Backlog

Recommendations are added as reviewer lanes complete. Each item must include priority, target artefact, owner role, rationale, implementation guidance, and acceptance criterion.

## Priority Definitions

- `must-fix`: Required before Nature submission.
- `should-fix`: Strongly recommended before submission.
- `stretch`: Improves competitiveness but is not required for first submission.
- `watch`: Monitor during revision or response-to-review.

## Initial Must-Review Items

| Priority | Target Artefact | Owner Role | Recommendation | Acceptance Criterion |
| --- | --- | --- | --- | --- |
| must-fix | Full repo | FAIR/reproducibility reviewer | Confirm a clean external reviewer can find, validate, cite, and reuse the ontology. | Reproducibility score recorded with exact blockers or pass evidence. |
| must-fix | Ontology modules | Game-theory professor | Assess whether core game-theoretic constructs are complete, correctly framed, and not overclaimed. | Missing-game-theory-element triage completed. |
| must-fix | Manuscript | Nature-editorial reviewer | Evaluate novelty, audience framing, methods transparency, limitations, and claims discipline. | Decision memo includes submission-readiness verdict and must-fix manuscript issues. |
| must-fix | Figures and slides | Visual-communications reviewer | Inventory and score every image out of 100, then define improvement loops. | Every image has a score, defect list, and re-score path. |
| must-fix | Analyses and mappings | Statistics/network-analysis reviewer | Check mapping robustness, sensitivity analyses, reviewer calibration, and source-family evidence reporting. | Evidence-backed recommendations recorded with acceptance criteria. |
| must-fix | arXiv source package | arXiv-toolchain reviewer | Benchmark external arXiv/LaTeX hardening tools against the repo-native cleaner before submission. | Tool matrix, acceptance checklist, privacy audit, and conservative gate recommendation are complete. |

## Recording Template

| Priority | Target Artefact | Owner Role | Recommendation | Rationale | Implementation Guidance | Acceptance Criterion | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |


<!-- arxiv-privacy-audit-update -->

### arXiv Source-Leak/Privacy Audit Update

Implemented `docs/paper/arxiv-source-privacy-audit.json` and `docs/paper/arxiv-source-privacy-audit.md` as explicit audit evidence for comments, hidden files, private notes/referee material, unused figures, aux/log/output files, embedded metadata, credentials, and private URLs/local paths. The audit is wired into `arxiv-privacy-audit` and `arxiv-preflight`; missing local external tools remain advisory, not blockers, because CI arXiv preflight is green.

## Current Reconciled Recommendations

Updated: `2026-06-25T10:13:36+00:00`

| Priority | Target Artefact | Owner Role | Recommendation | Rationale | Acceptance Criterion | Status |
| --- | --- | --- | --- | --- | --- | --- |
| should-fix | Full repo | FAIR/reproducibility reviewer | Keep reviewer quickstart, validation, citation, and reuse guidance synchronized with final release metadata. | Core reproducibility surfaces now exist; final release metadata must stay consistent across README, RO-Crate, citation page, and manuscript. | Final reviewer can run the named gates and find DOI, licence, namespace IRIs, prefixes, and release assets. | open-final-freeze |
| complete | Ontology modules | Game-theory professor | Implement article-facing missing-element disposition discipline before adding new terms. | The disposition table exists and prevents broad ontology expansion from becoming unreviewable. | New or changed term proposals carry add, align-only, defer, reject-duplicate, reject-out-of-scope, or domain-review disposition. | complete-ongoing-governance |
| should-fix | Manuscript | Nature-editorial reviewer | Perform final copyedit after supplement and figure numbering are frozen. | Manuscript and supplement are rewritten; final copyedit should preserve synchronized numbering and restrained claims. | Paper, supplement, figure captions, and claim table have no contradictory numbering or claims. | open-final-freeze |
| complete | Supplement | Nature-editorial reviewer | Convert evidence map into final journal-style supplement prose. | Supplement now has methods/results sections, Tables S1-S11, Figures S1-S7, claim map, data/code availability, SourceRight, and Authentext evidence. | `docs/paper/supplement-package.md` and `docs/paper/supplement-authentext-report.md` are present and gates pass. | complete |
| should-fix | PowerPoint | Visual-communications reviewer | Polish existing deck against final article figures and export thumbnails for readability review. | Deck exists and is scored; remaining work is visual binding, not creation. | Final deck thumbnails are exported, inspected, and slide scores reach 100 or record precise blockers. | open-visual-polish |
| complete | Manuscript/supplement figures | Visual-communications reviewer | Complete manuscript/supplement figure loop. | All 11 manuscript/supplement image rows score 100 after loop 1. | `image_scores.csv` and `image_scores.md` show 100/100 or blockers for every manuscript/supplement figure. | complete |
| complete | arXiv source package | arXiv-toolchain reviewer | Add explicit source-leak/privacy audit manifest and keep repo-native cleaner authoritative. | Audit manifest now covers comments, hidden files, private notes, aux/log/output files, metadata, credentials, and private URLs. | `make arxiv-privacy-audit` and `make arxiv-preflight` pass locally/CI; missing optional external tools remain advisory. | complete |
