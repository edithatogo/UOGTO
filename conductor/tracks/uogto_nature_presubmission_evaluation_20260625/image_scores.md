# Image Scores and Improvement Loop

## Process

1. Inventory every image used in the manuscript, supplement, dashboard, and PowerPoint.
2. Create one row per image in `image_scores.csv`.
3. Score each image against the seven image rubric criteria in `protocol.md`.
4. For any total below 100, record defects and a concrete fix plan.
5. Re-render or regenerate the image during implementation.
6. Re-score until the image is 100/100 or a blocker is recorded.

## Initial State

The inventory row in `image_scores.csv` is a placeholder for the implementation pass. It must be replaced by concrete image rows before the image loop can be marked complete.

## 100/100 Threshold

An image can only be marked 100/100 when:

- the scientific content is correct;
- labels, legends, colours, and scales are interpretable;
- the image is accessible and projection-safe;
- the source or generation script is tracked;
- the caption or slide claim matches the visual;
- the image is necessary for the article or presentation narrative.
