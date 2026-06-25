# Nature Must-Fix Submission Package Status

Generated: `2026-06-25T08:39:25+00:00`

| Order | Package item | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Manuscript rewrite scaffold | implemented-polished-draft | `docs/paper/paper.tex`; `docs/paper/authentext-report.md`; `docs/paper/authentext-report.json`; `make manuscript-check`; `make manuscript-sourcecheck` |
| 2 | Supplement prose | implemented-final-prose | `docs/paper/supplement-package.md`; `docs/paper/supplement-claim-map.csv`; `docs/paper/supplement-authentext-report.md`; `docs/paper/supplement-authentext-report.json`; `make manuscript-sourcecheck` |
| 3 | Privacy audit manifest | implemented-pass | `docs/paper/arxiv-source-privacy-audit.json`; `docs/paper/arxiv-source-privacy-audit.md`; CI arXiv Preflight run `28154901098` |
| 4 | Deck creation | implemented-needs-final-polish | `docs/presentation/uogto_nature_presubmission_deck.pptx`; `docs/presentation/uogto_nature_presubmission_deck_scores.md`; `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/powerpoint_recommendations.md` |
| 5 | Figure loops | implemented-loop-1 | `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.csv`; `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.md`; `docs/article-hardening/figures/`; `docs/ontology-comparison/figures/` |

Remaining Nature-facing work is now limited to final submission freeze: keep manuscript and supplement claims synchronized, freeze figure numbering and captions, polish the PowerPoint deck against final figures, and rerun SourceRight, Authentext, arXiv, and validation gates after any citation or figure change.


## Manuscript editorial pass

Completed `2026-06-25T09:22:36+00:00`. The manuscript was rewritten for a tighter Nature-style claim hierarchy, reduced repo-process narration, integrated table/figure callouts, and restrained academic prose. SourceRight passed CSL validation and citation reconciliation; Authentext Pro academic audit passed after the humanization pass.


## Supplement editorial pass

Completed `2026-06-25T09:34:00+00:00`. `docs/paper/supplement-package.md` was converted from an evidence map into journal-style supplementary information with Supplementary Methods, Supplementary Results, Tables S1-S11, Figures S1-S7, a claim-to-supplement map, data/code availability, and completion criteria. SourceRight passed via `make manuscript-sourcecheck` with 11 matched citations and 0 citation reconciliation issues. Authentext Pro academic audit passed with 0 findings in `docs/paper/supplement-authentext-report.md` / `.json`.

## CI evidence after supplement/status cleanup

Recorded `2026-06-25T10:21:25+00:00` for commit `170399a`: Validate UOGTO `28163345123`, Build Manuscript PDF `28163345086`, Build WIDOCO Pages `28163345077`, and arXiv Preflight `28163345131` all completed successfully.
