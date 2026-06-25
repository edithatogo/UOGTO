# PowerPoint Recommendations

## Review Aim

Assess whether the presentation can brief an editor, reviewer, or senior interdisciplinary audience on the problem, contribution, evidence, and submission readiness of UOGTO.

## Created Deck

- Deck: `docs/presentation/uogto_nature_presubmission_deck.pptx`
- Scorecard: `docs/presentation/uogto_nature_presubmission_deck_scores.md`
- Notes: `docs/presentation/uogto_nature_presubmission_deck_notes.md`
- Status: created and first-pass scored. Not yet final 100/100 because final article figures, slide thumbnails, and projector readability checks still need to be bound. Source/privacy audit evidence is now available and should be reflected on slide 7.

## Slide-Level Review

| Slide | Current Role | Score | Main Defect | Recommendation | Acceptance Criterion |
| --- | --- | ---: | --- | --- | --- |
| 1 | UOGTO claim and contribution | 84 | Final DOI and release status need synchronization. | Update the deck after final release and DOI metadata are frozen. | Opening slide matches paper, README, citation page, and RO-Crate. |
| 2 | Problem and semantic gap | 82 | Gap is clear but would benefit from one source-family comparator. | Add a compact comparator/source-count callout. | Slide supports the problem statement without overclaiming. |
| 3 | Architecture and governance | 83 | Architecture is schematic rather than tied to final module audit. | Add final module audit table reference. | Reviewer can trace modules to ontology files and governance metadata. |
| 4 | Evidence register and PRISMA discovery | 84 | Needs final PRISMA flow thumbnail. | Insert exported PRISMA/source discovery visual. | Source-discovery claims visually match the supplement package. |
| 5 | Mapping and robustness results | 82 | Mapping counts need final disposition context. | Add accepted/rejected/domain-review disposition summary. | Mapping slide clearly supports conservative alignment only. |
| 6 | Case studies and executable traces | 80 | Case slide is broad but lacks concrete trace evidence. | Add one executable trace or provenance figure. | The slide demonstrates the differentiating executable-semantics claim. |
| 7 | FAIR reproducibility and arXiv readiness | 88 | Privacy audit evidence exists but is not yet visually bound into the slide. | Add the pass status from `docs/paper/arxiv-source-privacy-audit.md` and SourceRight/Auth reports. | Reproducibility claims match CI, SourceRight, Authentext, privacy audit, and supplement artifacts. |
| 8 | Limitations and next validation | 88 | Decision status should be updated after final freeze-and-verify gates. | Re-score after final figure/caption freeze and CI evidence capture. | Final slide reflects actual submission decision. |

Average score: 84.0/100 after status reconciliation; final score still requires thumbnail/readability inspection.

## Required Narrative Arc

1. Why game-theoretic semantics need a reusable ontology.
2. What UOGTO contributes beyond existing game theory, simulation, ontology, and MARL resources.
3. How the ontology is structured and governed.
4. How evidence was gathered, screened, mapped, and analysed.
5. What the evaluation shows.
6. What case studies demonstrate.
7. What limitations remain.
8. Why the manuscript is ready, or what remains before submission.

## Visual Requirements

- Use figures as evidence, not decoration.
- Keep slide text minimal and specific.
- Ensure every figure is legible when projected.
- Prefer one major idea per slide.
- Avoid unsupported novelty or superiority claims.
- End with a clear decision and next-actions slide.

## 2026-06-25 Creation Disposition

- No deck was found initially, so a new eight-slide editorial deck has been created from `powerpoint_asset_inventory.md`.
- The deck uses editable PowerPoint shapes and a restrained evidence-first narrative.
- The deck is no longer a creation blocker; remaining work is visual polishing and final evidence binding.

## 2026-06-25T10:13:36+00:00 Status Reconciliation

Privacy audit, deck creation, supplement final prose, and manuscript/supplement figure loop are implemented. The PowerPoint work that remains is final article-figure binding, thumbnail export, readability inspection, and re-scoring slides to 100/100 or recording precise blockers.
