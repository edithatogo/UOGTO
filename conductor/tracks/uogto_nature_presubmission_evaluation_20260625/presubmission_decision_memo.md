# Presubmission Decision Memo

## Decision
- Verdict: major revision before submission.
- Target: Nature-style research article remains possible but not submission-ready in the current package state.
- Basis: repository validation CI and the rewritten manuscript draft are materially stronger, but figure integration supplement packaging privacy audit and deck creation remain incomplete.

## Top Risks
- Manuscript is now a full structured draft, but it still needs Nature-level editorial compression, final figure callouts, and claim-boundary tables.
- PowerPoint deck work is a needs-creation task because no repository deck asset was found.
- Figures are useful but none has reached 100 out of 100 for Nature-readiness.
- Overclaim risk remains unless missing-game-theory elements and mapping robustness are summarized in article-facing tables.

## Must-Fix Before Submission
- Polish the rewritten manuscript into final Nature style with integrated figure callouts and tighter claims.
- Build a coherent supplement package from the article-hardening and ontology-comparison artifacts.
- Complete figure improvement loops and create the PowerPoint deck from powerpoint_asset_inventory.md.
- Add explicit source-leak privacy audit manifest for the arXiv source package.

## 2026-06-25 Manuscript Rewrite Update
- docs/paper/paper.tex has been rewritten from a short scaffold into a full article draft with claim methods results limitations figure plan and evidence-backed framing.
- make manuscript-check passed with 11 citations 11 bibitems and 11 CSL references.
- make manuscript-build passed the manuscript citation and TeX structure checks; local PDF generation remains unavailable because no local TeX engine is installed.
- make manuscript-sourcecheck passed SourceRight CSL validation and citation reconciliation with 11 matched citations and 0 reconciliation issues.
