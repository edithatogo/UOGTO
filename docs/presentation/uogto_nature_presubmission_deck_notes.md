# UOGTO Nature Presubmission Deck Notes

Updated: `2026-06-25T10:50:25+00:00`

This is an editorial briefing deck, not a conference talk. It now follows the frozen manuscript/supplement callout structure and has been rebuilt as a standard PowerPoint-authored `.pptx`.

Design choices:

- restrained palette with one central claim per slide;
- short numbered evidence points rather than paragraph-heavy slides;
- direct bindings to Supplementary Tables S1-S11 and Figures S1-S7 where relevant;
- explicit claim boundaries on conservative mappings, metadata-only evidence, and final freeze requirements;
- PowerPoint-exported thumbnails for all slides in `docs/presentation/uogto_nature_presubmission_deck_thumbnails/`.

Implementation note: embedded SVG insertion was tested through PowerPoint COM but was not retained because it hung in this environment. The final deck uses repository-relative figure/table callout panels, while the source SVG/PDF figures remain in `docs/article-hardening/figures/` and `docs/ontology-comparison/figures/`.

Next pass: only rerun the slide score loop if the manuscript/supplement figure numbers, captions, source data, or submission decision wording changes.
