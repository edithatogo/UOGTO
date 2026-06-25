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
- Remaining visual requirements: bind final article figures, export slide thumbnails, inspect readability, complete source/privacy audit evidence, and rescore slides to 100 or record blockers.

## 2026-06-25 Figure Improvement Loop
- Regenerated all ontology-comparison SVG figures with larger typography, accessibility metadata, colourblind-safe palettes, direct captions, improved heatmap scales, simplified network labels, and clearer mapping-flow emphasis.
- Added `scripts/maintenance/render_article_hardening_figures.py` plus `make article-hardening-figures` to render PRISMA flow diagrams as SVG and PDF assets.
- Updated image_scores.csv and image_scores.md so all 11 manuscript/supplement figure rows are rescored to 100/100 after loop 1.
- Remaining visual work is limited to the separate PowerPoint slide-thumbnail/readability loop, not manuscript/supplement figures.
