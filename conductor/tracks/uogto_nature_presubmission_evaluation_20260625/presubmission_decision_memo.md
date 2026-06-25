# Presubmission Decision Memo

## Decision
- Verdict: major revision before submission.
- Target: Nature-style research article remains possible; current package state is now in final freeze-and-verify rather than evidence-construction mode.
- Basis: repository validation CI, the rewritten manuscript draft, final supplement prose, SourceRight/Authentext evidence, privacy audit, deck creation, and completed first figure loop are materially stronger; final submission still needs freeze-and-verify packaging rather than more evidence-map construction.

## Top Risks
- Manuscript is now a tighter polished draft with integrated table/figure callouts; remaining manuscript work is final journal copyediting after figure numbering and supplement prose are frozen.
- PowerPoint deck work is now a created first-pass asset with scored slides; it still needs final article figure binding, thumbnail export, and readability inspection.
- Manuscript and supplement figures reached 100 out of 100 in the first Nature-readiness loop; re-score only after source data, captions, or placement change.
- Overclaim risk remains a copyediting risk even though missing-element dispositions and mapping robustness are now summarized in article-facing tables.

## Must-Fix Before Submission
- Final copyedit the polished manuscript after figure numbering, captions, and supplement prose are frozen.
- Polish the created PowerPoint deck against final article figures and slide readability checks.

## 2026-06-25 Manuscript Rewrite Update
- docs/paper/paper.tex has been rewritten from a short scaffold into a full article draft with claim methods results limitations figure plan and evidence-backed framing.
- make manuscript-check passed with 11 citations 11 bibitems and 11 CSL references.
- make manuscript-build passed the manuscript citation and TeX structure checks; local PDF generation remains unavailable because no local TeX engine is installed.
- make manuscript-sourcecheck passed SourceRight CSL validation and citation reconciliation with 11 matched citations and 0 reconciliation issues.

## 2026-06-25 Supplement Package Update
- docs/paper/supplement-package.md now maps article claims to protocol, source register, ontology validation, SHACL, mappings, SSSOM, metrics, figures, RO-Crate, DuckDB, SourceRight, arXiv, governance, and reuse artifacts.
- docs/paper/supplement-claim-map.csv adds a machine-readable claim-to-artifact table with support level and open-work fields.
- Supplement score increased from 62 to 90: it now has final-prose supplementary sections, numbered tables and figures, claim-to-supplement mapping, SourceRight evidence, and Authentext pass. It is not yet a journal-typeset supplement.

<!-- arxiv-privacy-audit-update -->

### arXiv Source-Leak/Privacy Audit Update

Implemented `docs/paper/arxiv-source-privacy-audit.json` and `docs/paper/arxiv-source-privacy-audit.md` as explicit audit evidence for comments, hidden files, private notes/referee material, unused figures, aux/log/output files, embedded metadata, credentials, and private URLs/local paths. The audit is wired into `arxiv-privacy-audit` and `arxiv-preflight`; missing local external tools remain advisory, not blockers, because CI arXiv preflight is green.


## 2026-06-25 Final Manuscript Prose Update
- `docs/paper/paper.tex` was rewritten from a process-heavy scaffold into a tighter article draft with clearer problem framing, results-first structure, integrated table/figure callouts, and a more restrained limitations section.
- SourceRight was run through `make manuscript-sourcecheck`: CSL validation passed, reference report was generated, and citation reconciliation reported 11 matched citations with 0 citation issues.
- Authentext Pro academic guidance from `https://github.com/edithatogo/authentext` was applied and recorded in `docs/paper/authentext-report.md` / `.json`; the high-signal pattern audit now passes.
- Local PDF generation remains TeX-engine unavailable, but manuscript structure checks pass locally and CI remains the strict PDF gate.

## 2026-06-25 Final Supplement Prose Update
- `docs/paper/supplement-package.md` is now final-prose supplementary information rather than an evidence map, with Supplementary Methods, Supplementary Results, Supplementary Tables S1-S11, Supplementary Figures S1-S7, claim-to-supplement mapping, data/code availability, and completion criteria.
- `docs/paper/supplement-claim-map.csv` was synchronized with the final-prose sections and no longer carries stale implementation blockers for module tables, privacy audit, deck creation, or figure loops.
- SourceRight was run through `make manuscript-sourcecheck`: CSL validation passed and citation reconciliation reported 11 matched citations with 0 citation issues.
- Authentext Pro academic guidance from `https://github.com/edithatogo/authentext` was applied and recorded in `docs/paper/supplement-authentext-report.md` / `.json`; the supplement audit passes with 0 findings.

## 2026-06-25T10:13:36+00:00 Track Memo Cleanup
- Reconciled the decision memo with implemented privacy audit, deck creation, figure loop, and final supplement prose.
- Remaining Nature-facing work is now final freeze-and-verify: freeze table/figure numbering, polish deck readability, rerun gates after any figure/citation changes, and record CI evidence.

## 2026-06-25T10:21:25+00:00 CI Evidence Update
- Commit `170399a` passed Validate UOGTO (`28163345123`), Build Manuscript PDF (`28163345086`), Build WIDOCO Pages (`28163345077`), and arXiv Preflight (`28163345131`).
