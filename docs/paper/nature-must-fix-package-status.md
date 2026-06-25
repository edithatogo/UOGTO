# Nature Must-Fix Submission Package Status

Generated: `2026-06-25T08:39:25+00:00`

| Order | Package item | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Manuscript rewrite scaffold | implemented-polished-draft | `docs/paper/paper.tex`; `docs/paper/authentext-report.md`; `docs/paper/authentext-report.json`; `make manuscript-check`; `make manuscript-sourcecheck` |
| 2 | Supplement map | implemented-map | `docs/paper/supplement-package.md`; `docs/paper/supplement-claim-map.csv`; `docs/article-hardening/article-facing-tables/` |
| 3 | Privacy audit manifest | implemented-pass | `docs/paper/arxiv-source-privacy-audit.json`; `docs/paper/arxiv-source-privacy-audit.md`; CI arXiv Preflight run `28154901098` |
| 4 | Deck creation | implemented-needs-final-polish | `docs/presentation/uogto_nature_presubmission_deck.pptx`; `docs/presentation/uogto_nature_presubmission_deck_scores.md`; `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/powerpoint_recommendations.md` |
| 5 | Figure loops | implemented-loop-1 | `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.csv`; `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.md`; `docs/article-hardening/figures/`; `docs/ontology-comparison/figures/` |

Remaining Nature-facing work is editorial: convert the manuscript scaffold and supplement map into final polished prose, freeze figure numbering/captions, and re-score deck/figures only if source data or manuscript placement changes.


## Manuscript editorial pass

Completed `2026-06-25T09:22:36+00:00`. The manuscript was rewritten for a tighter Nature-style claim hierarchy, reduced repo-process narration, integrated table/figure callouts, and restrained academic prose. SourceRight passed CSL validation and citation reconciliation; Authentext Pro academic audit passed after the humanization pass.
