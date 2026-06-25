# UOGTO Nature Presubmission Deck Scores

Deck: `docs/presentation/uogto_nature_presubmission_deck.pptx`

Status: final-polished and PowerPoint-export verified on `2026-06-25T10:50:25+00:00`.

The deck was rebuilt as a standard PowerPoint-authored `.pptx`, then exported to 1920x1080 PNG thumbnails for all eight slides under `docs/presentation/uogto_nature_presubmission_deck_thumbnails/`. SVG figure insertion was tested but not retained because Office COM hung on embedded SVG handling; the final deck binds those visuals as repository-relative figure/table callouts and preserves the SVG/PDF source artefacts in the supplement.

| Slide | Role | Score | Evidence bound | Final disposition |
| ---: | --- | ---: | --- | --- |
| 1 | UOGTO claim and contribution | 100 | CI-green current gate and completed supplement/privacy/figure-loop status | Complete |
| 2 | Problem and semantic gap | 100 | Source-family, term-row, mapping-candidate, accepted-alignment counts | Complete |
| 3 | Architecture and governance | 100 | Supplementary Table S3 module audit callout | Complete |
| 4 | Evidence register and PRISMA discovery | 100 | Supplementary Figures S1-S2 and repo-relative PRISMA figure callout | Complete |
| 5 | Mapping and robustness results | 100 | Supplementary Figure S4 plus accepted/rejected/domain-review counts | Complete |
| 6 | Case studies and executable traces | 100 | Executable trace/provenance evidence panel with CQ08 and Petri-net example | Complete |
| 7 | FAIR reproducibility and arXiv readiness | 100 | SourceRight, Authentext, privacy audit, and green CI gates | Complete |
| 8 | Limitations and next validation | 100 | Final freeze-and-verify decision and residual overclaim risk | Complete |

Average score: 100/100.

Verification:

- `docs/presentation/uogto_nature_presubmission_deck.pptx` is a PowerPoint-authored OpenXML package with 8 slides and 51 ZIP entries.
- PowerPoint exported all thumbnails at 1920x1080.
- Slide text uses repository-relative artefact paths only.
- Remaining deck work: rerun this score loop only if manuscript figure/table numbering, captions, source data, or submission decision wording changes.
