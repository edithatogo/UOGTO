# Presubmission Decision Memo

## Decision
- Verdict: major revision before submission.
- Target: Nature-style research article remains possible but not submission-ready in the current package state.
- Basis: repository validation CI, the rewritten manuscript draft, and the new supplement package map are materially stronger, but figure integration final supplement prose privacy audit and deck creation remain incomplete.

## Top Risks
- Manuscript is now a tighter polished draft with integrated table/figure callouts; remaining manuscript work is final journal copyediting after figure numbering and supplement prose are frozen.
- PowerPoint deck work is now a created first-pass asset; it still needs final article figure binding, thumbnail export, and readability inspection.
- Figures are useful but none has reached 100 out of 100 for Nature-readiness.
- Overclaim risk remains unless missing-game-theory elements and mapping robustness are summarized in article-facing tables.

## Must-Fix Before Submission
- Final copyedit the polished manuscript after figure numbering, captions, and supplement prose are frozen.
- Convert the new supplement package map into final edited journal supplement prose with final figure numbering and table callouts.
- Complete figure improvement loops and polish the created PowerPoint deck against final article figures and slide readability checks.
- Add explicit source-leak privacy audit manifest for the arXiv source package.

## 2026-06-25 Manuscript Rewrite Update
- docs/paper/paper.tex has been rewritten from a short scaffold into a full article draft with claim methods results limitations figure plan and evidence-backed framing.
- make manuscript-check passed with 11 citations 11 bibitems and 11 CSL references.
- make manuscript-build passed the manuscript citation and TeX structure checks; local PDF generation remains unavailable because no local TeX engine is installed.
- make manuscript-sourcecheck passed SourceRight CSL validation and citation reconciliation with 11 matched citations and 0 reconciliation issues.

## 2026-06-25 Supplement Package Update
- docs/paper/supplement-package.md now maps article claims to protocol, source register, ontology validation, SHACL, mappings, SSSOM, metrics, figures, RO-Crate, DuckDB, SourceRight, arXiv, governance, and reuse artifacts.
- docs/paper/supplement-claim-map.csv adds a machine-readable claim-to-artifact table with support level and open-work fields.
- Supplement score increased from 62 to 78 because the package is now mapped; it is not yet a final typeset supplement.

<!-- arxiv-privacy-audit-update -->

### arXiv Source-Leak/Privacy Audit Update

Implemented `docs/paper/arxiv-source-privacy-audit.json` and `docs/paper/arxiv-source-privacy-audit.md` as explicit audit evidence for comments, hidden files, private notes/referee material, unused figures, aux/log/output files, embedded metadata, credentials, and private URLs/local paths. The audit is wired into `arxiv-privacy-audit` and `arxiv-preflight`; missing local external tools remain advisory, not blockers, because CI arXiv preflight is green.


## 2026-06-25 Final Manuscript Prose Update
- `docs/paper/paper.tex` was rewritten from a process-heavy scaffold into a tighter article draft with clearer problem framing, results-first structure, integrated table/figure callouts, and a more restrained limitations section.
- SourceRight was run through `make manuscript-sourcecheck`: CSL validation passed, reference report was generated, and citation reconciliation reported 11 matched citations with 0 citation issues.
- Authentext Pro academic guidance from `https://github.com/edithatogo/authentext` was applied and recorded in `docs/paper/authentext-report.md` / `.json`; the high-signal pattern audit now passes.
- Local PDF generation remains TeX-engine unavailable, but manuscript structure checks pass locally and CI remains the strict PDF gate.
