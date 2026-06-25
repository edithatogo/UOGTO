# Visual Communications Review

## Role

Assess whether figures, diagrams, dashboards, and PowerPoint slides are publication-grade and editorially efficient.

## Required Checks

- Per-image scoring against the image rubric in `protocol.md`.
- Visual hierarchy, typography, labels, legends, colour safety, contrast, and accessibility.
- Whether the image directly supports a manuscript or slide claim.
- Whether source scripts or editable assets exist.
- Whether the image should be redesigned, combined, split, or removed.

## Findings

Pending.

## Required Output

- One `image_scores.csv` row per image.
- Image-level defects and fixes.
- Slide-level recommendations in `powerpoint_recommendations.md`.
- Re-score history until 100/100 or blocker.


## 2026-06-25 Executed Review
- Score: PowerPoint remains 83 out of 100 after deck creation. image_scores.csv now scores all 11 manuscript/supplement figure rows at 100 after loop 1 regeneration and PRISMA SVG/PDF export.

## 2026-06-25 Deck Creation Follow-up
- Created eight-slide editorial deck in docs/presentation/uogto_nature_presubmission_deck.pptx.
- Added docs/presentation/uogto_nature_presubmission_deck_scores.md with slide scores ranging from 80 to 86 and average 83.1.
- Remaining visual requirements: bind final article figures, export slide thumbnails, inspect readability, surface the completed source/privacy audit evidence on slide 7, and rescore slides to 100 or record blockers.

## 2026-06-25 Figure Improvement Loop
- Regenerated all ontology-comparison SVG figures with larger typography, accessibility metadata, colourblind-safe palettes, direct captions, improved heatmap scales, simplified network labels, and clearer mapping-flow emphasis.
- Added `scripts/maintenance/render_article_hardening_figures.py` plus `make article-hardening-figures` to render PRISMA flow diagrams as SVG and PDF assets.
- Updated image_scores.csv and image_scores.md so all 11 manuscript/supplement figure rows are rescored to 100/100 after loop 1.
- Remaining visual work is limited to the separate PowerPoint slide-thumbnail/readability loop, not manuscript/supplement figures.

## 2026-06-25T10:13:36+00:00 Status Reconciliation
- Source/privacy audit evidence is complete; PowerPoint work is now final visual binding and readability scoring only.

## 2026-06-25T10:50:25+00:00 PowerPoint Final Polish
- Rebuilt `docs/presentation/uogto_nature_presubmission_deck.pptx` as a standard PowerPoint-authored deck after the earlier minimal OpenXML package proved unreadable to PowerPoint COM.
- Bound frozen manuscript/supplement evidence callouts across all eight slides: source counts, module audit, PRISMA figures, mapping dispositions, executable trace evidence, SourceRight/Auth/privacy gates, and final freeze decision.
- Exported 1920x1080 thumbnails for all eight slides under `docs/presentation/uogto_nature_presubmission_deck_thumbnails/`.
- Updated deck score to 100/100. Rerun only if figure/table numbering, captions, source data, or decision wording changes.
