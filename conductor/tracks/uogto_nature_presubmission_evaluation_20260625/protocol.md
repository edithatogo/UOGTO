# Nature-Style Presubmission Evaluation Protocol

## Review Standard

This protocol evaluates UOGTO against a high-bar Nature-style research article standard: strong conceptual novelty, methodological transparency, reproducible artefacts, restrained claims, high-quality figures, and clear value for readers outside the immediate ontology niche.

## Scoring Rules

All scores are out of 100.

- `95-100`: Submission-grade for a top-tier venue; only editorial polishing remains.
- `85-94`: Strong, but one or more visible weaknesses should be fixed before submission.
- `70-84`: Promising, but material revision is needed.
- `50-69`: Major revision required before external submission.
- `<50`: Not submission-ready for the assessed category.

Each score must include evidence, a rationale, and an acceptance criterion for improvement.

## Repository and GitHub Setup Rubric

| Criterion | Weight |
| --- | ---: |
| Clear repository purpose, installation, validation, and reuse instructions | 15 |
| Reproducible environment and dependency lock/setup clarity | 15 |
| Release readiness, versioning, DOI, licence, citation, and namespace guidance | 15 |
| Contributor governance, issue templates, change policy, deprecation policy | 10 |
| CI or local validation gates for RDF, SHACL, CQ, mappings, manuscript, and artefacts | 20 |
| Artefact discoverability and separation of source/generated outputs | 15 |
| Reviewer-friendly navigation and evidence traceability | 10 |

## Ontology Quality Rubric

| Criterion | Weight |
| --- | ---: |
| Game-theoretic conceptual coverage and correctness | 15 |
| Modular separation of specification, instance, session, trace, strategy, action, payoff, outcome, mechanism, and execution bindings | 15 |
| OWL/RDF modelling quality and property/class separation | 15 |
| Annotation completeness with labels and definitions | 10 |
| SHACL coverage for examples, modules, and competency questions | 10 |
| Mapping quality, SSSOM inspectability, and external ontology alignment | 10 |
| Reasoner/profile status, orphan classes, hierarchy depth, relation richness | 10 |
| Evidence traceability for term sources and governance metadata | 15 |

## Evidence and Analysis Rubric

| Criterion | Weight |
| --- | ---: |
| Scoping review protocol completeness and PRISMA-ScR mapping | 10 |
| Search logs, source inventory, negative evidence, and reviewer handoff | 10 |
| FAIR and RO-Crate completeness | 10 |
| DuckDB/CSV/Markdown/JSON/Parquet analysis artefact consistency | 10 |
| Mapping robustness and reviewer calibration | 10 |
| Network analysis validity and sensitivity checks | 10 |
| Source-family heatmaps and evidence-level reporting | 10 |
| Case study breadth and executable trace/provenance support | 15 |
| Reproducibility from clean checkout | 15 |

## Manuscript and Supplement Rubric

| Criterion | Weight |
| --- | ---: |
| Novelty claim is clear, important, and not overstated | 15 |
| Abstract and introduction frame the contribution for a broad scientific audience | 10 |
| Related work fairly positions game theory, simulation, ontology, and AI/MARL work | 10 |
| Methods are complete enough to reproduce ontology development and evaluation | 15 |
| Results are evidence-backed and not merely descriptive | 15 |
| Limitations and threats to validity are candid | 10 |
| Figures are necessary, readable, and tightly linked to claims | 10 |
| Supplement carries detail without hiding essential methods | 10 |
| Bibliography and citation extraction are robust | 5 |

## PowerPoint Rubric

| Criterion | Weight |
| --- | ---: |
| Narrative arc makes the problem, contribution, evidence, and implications clear | 20 |
| Slides are visually restrained, readable, and figure-led | 20 |
| Technical claims are supported by visible evidence | 15 |
| Ontology and evaluation details are understandable without overloading slides | 15 |
| Speaker flow supports a 10-15 minute editorial or reviewer briefing | 10 |
| Figures are accessible, high contrast, and projection-safe | 10 |
| Ends with a clear submission-readiness and next-actions slide | 10 |

## Image Scoring Rubric

Each image is scored out of 100:

| Criterion | Points |
| --- | ---: |
| Scientific accuracy | 20 |
| Interpretability without excessive caption dependence | 15 |
| Visual hierarchy and design quality | 15 |
| Reproducibility from tracked source or script | 15 |
| Accessibility, contrast, colour-blind safety, and legibility | 10 |
| Caption and manuscript/slide alignment | 10 |
| Nature-readiness: necessity, economy, and editorial polish | 15 |

An image reaches `100/100` only when no known scientific, design, accessibility, reproducibility, or caption-alignment defect remains.

## Decision Rule

- `ready`: all must-fix items resolved; no category below 95.
- `ready after minor fixes`: no category below 90; only editorial or cosmetic issues remain.
- `major revision before submission`: any category below 90, or any unresolved methodological, reproducibility, or novelty risk.
- `not yet submission-ready`: any core evidence, ontology, reproducibility, or manuscript claim is incomplete or unverifiable.
