# Supplementary information for UOGTO

Date: 2026-06-25

This supplement supports the manuscript *Universal Open Game Theory Ontology: Semantics for Games, Simulation, and Executable Multi-Agent Evidence*. It is written for reviewers who need to inspect how the ontology, source discovery, mappings, quality metrics, figures, and submission checks support the article claims. The supplement is not a second narrative paper. It is a structured evidence package, with each section pointing to stable repository artefacts.

## Supplementary methods

### S1. Review protocol and reporting standards

UOGTO's article evidence package follows a scoping-review style protocol. The protocol defines the search scope, source families, inclusion and exclusion criteria, evidence levels, charting fields, reviewer roles, red-team checks, and reproducibility outputs. It also maps PRISMA-ScR style reporting items to repository artefacts so that readers can inspect the evidence behind source discovery and screening.

Primary artefacts:

- `docs/article-hardening/protocol.md`
- `docs/article-hardening/protocol-checklist.md`
- `docs/article-hardening/prisma-scr-artifact-map.md`
- `docs/article-hardening/search-strategy.md`
- `docs/article-hardening/dual-screening.md`

Supplementary Table S1 lists the protocol and reporting artefacts used to support the manuscript methods. Supplementary Figure S1 gives the source-discovery flow. Supplementary Figure S2 gives the screening flow.

### S2. Source register and evidence levels

Source discovery is recorded as an evidence register rather than a narrative search summary. The register distinguishes parsed RDF sources, structured non-RDF sources, metadata-only sources, literature-only sources, excluded sources, and negative evidence. Each search or source record includes evidence level, licence or reuse status, inclusion rationale, and reviewer handoff where available. This distinction is important because a parsed ontology file and a metadata-only standards page do not support the same kind of claim.

Primary artefacts:

- `docs/article-hardening/search-log.jsonl`
- `docs/article-hardening/source-extension-inventory.json`
- `docs/article-hardening/source-extension-inventory.md`
- `docs/ontology-comparison/source-inventory.json`
- `docs/ontology-comparison/source-provenance.json`
- `docs/ontology-comparison/inclusion-exclusion-log.jsonl`

Supplementary Table S2 summarises source families, evidence levels, licence dispositions, and inclusion decisions. Supplementary Figure S3 shows source-family coverage by evidence level.

### S3. Ontology implementation and validation

UOGTO is implemented as modular RDF/OWL source, SHACL shapes, JSON-LD contexts, examples, competency questions, and documentation. The quality benchmark records annotation completeness, orphan classes, relation richness, hierarchy depth, import depth, SHACL coverage, examples per module, competency-query coverage, OWL profile status, and reasoner status. The portable validation baseline uses RDFLib and pySHACL. Optional ROBOT-style outputs are retained as secondary evidence when Java tooling is available.

Primary artefacts:

- `ontologies/`
- `shapes/`
- `examples/`
- `competency-questions/`
- `docs/article-hardening/quality-metrics.json`
- `docs/article-hardening/reasoner-report.md`
- `docs/article-hardening/competency-benchmark.md`
- `docs/article-hardening/robot/`
- `docs/article-hardening/article-facing-tables/module-audit-table.csv`
- `docs/article-hardening/article-facing-tables/module-audit-table.json`
- `docs/article-hardening/article-facing-tables/module-audit-table.md`

Supplementary Table S3 is the module audit table. It gives reviewers a compact account of labels, definitions, SHACL links, examples, competency questions, OWL profile status, and reasoner status. This table replaces the need to infer coverage from raw validation logs.

### S4. Mapping and alignment evidence

The mapping workflow separates candidate generation from accepted alignment. Candidate mappings are generated from deterministic lexical, definitional, hierarchy, property-signature, type-compatibility, and source-reliability signals. Accepted mappings are exported as both RDF alignment triples and SSSOM tables. Rejected mappings and domain-review rows remain available for audit; they are not silently discarded.

Primary artefacts:

- `docs/ontology-comparison/term-inventory.jsonl`
- `docs/ontology-comparison/mapping-candidates.jsonl`
- `docs/ontology-comparison/mapping-review.csv`
- `docs/ontology-comparison/accepted-alignments.ttl`
- `docs/ontology-comparison/accepted-alignments.sssom.tsv`
- `docs/ontology-comparison/accepted-alignments.sssom.yml`

Supplementary Table S4 reports the mapping decision surface, including accepted, rejected, and domain-review rows. Supplementary Figure S4 shows the mapping flow from candidates to reviewed decisions and accepted alignments.

### S5. Robustness, calibration, and network analyses

The mapping evidence is stress-tested rather than treated as a single deterministic output. Robustness analyses ablate exact labels, normalized labels, definition similarity, hierarchy context, property signatures, and embedding similarity. Calibration artefacts record reviewer agreement and adjudication outcomes. Network sensitivity analyses compare accepted-only mappings, accepted plus close/related mappings, and scenarios excluding metadata-only sources.

Primary artefacts:

- `docs/ontology-comparison/mapping-robustness.md`
- `docs/ontology-comparison/mapping-robustness/`
- `docs/ontology-comparison/mapping-calibration.md`
- `docs/ontology-comparison/mapping-calibration/`
- `docs/ontology-comparison/network-analysis.json`
- `docs/ontology-comparison/network-sensitivity.json`
- `docs/ontology-comparison/network-sensitivity.md`
- `docs/ontology-comparison/overlap-metrics.json`
- `docs/article-hardening/article-facing-tables/mapping-robustness-table.csv`
- `docs/article-hardening/article-facing-tables/mapping-robustness-table.json`
- `docs/article-hardening/article-facing-tables/mapping-robustness-table.md`

Supplementary Table S5 is the article-facing mapping robustness table. Supplementary Figure S5 shows the source-module overlap heatmap. Supplementary Figure S6 shows the source similarity or network sensitivity view. These artefacts support the manuscript's cautious claim that UOGTO identifies bridges among modelling traditions, not universal equivalence.

### S6. Case studies and missing-element dispositions

The case-study package covers auction and mechanism design, voting and social choice, security and Stackelberg games, MARL Markov games, ABM policy simulation, system-dynamics feedback games, LLM-agent tool-use games, and executable trace/provenance cases. Missing game-theory elements are triaged before ontology expansion. The allowed dispositions are: add to UOGTO, align externally only, defer, reject duplicate, reject out of scope, or domain review.

Primary artefacts:

- `docs/article-hardening/case-studies.md`
- `docs/article-hardening/case-studies.json`
- `docs/article-hardening/use-case-coverage-matrix.csv`
- `docs/article-hardening/use-case-coverage-matrix.json`
- `docs/article-hardening/uogto-inclusion-decisions.md`
- `docs/article-hardening/article-facing-tables/missing-game-theory-element-dispositions.csv`
- `docs/article-hardening/article-facing-tables/missing-game-theory-element-dispositions.json`
- `docs/article-hardening/article-facing-tables/missing-game-theory-element-dispositions.md`

Supplementary Table S6 gives the missing-element disposition table. Supplementary Table S7 gives case-study and use-case coverage.

### S7. Reproducibility and data packaging

The reproducibility package is designed to make the article evidence reusable, not merely readable. RO-Crate metadata identifies the root data entity, contextual entities, source artefacts, workflows, scripts, and provenance. Tabular outputs are stored in human-readable CSV/Markdown and machine-stable JSON or Parquet where appropriate. The dashboard separates parsed RDF, structured non-RDF, metadata-only, literature-only, and excluded sources.

Primary artefacts:

- `docs/article-hardening/ro-crate-package.md`
- `docs/article-hardening/ro-crate-metadata.json`
- `docs/article-hardening/duckdb-artifact-store.md`
- `docs/article-hardening/tabular-artifact-storage.md`
- `docs/article-hardening/article-evidence-dashboard.md`
- `docs/article-hardening/article-evidence-dashboard.json`
- `docs/article-hardening/article-evidence-dashboard.html`

Supplementary Table S8 lists the reproducibility and packaging artefacts. Supplementary Figure S7 should show the evidence dashboard or the reproducibility chain from ontology source to validation, mapping, tables, and submission checks.

### S8. Figures and visual evidence

The manuscript and supplement figures have completed the first Nature-readiness score loop. The scorecard records all 11 manuscript/supplement figure rows at 100 out of 100 after typography, caption-alignment, accessibility metadata, colour-safety, network-readability, and PDFLaTeX-compatible PRISMA export improvements. Any change to source data, figure numbering, caption text, or manuscript placement should trigger a re-score.

Primary artefacts:

- `docs/article-hardening/figures/`
- `docs/ontology-comparison/figures/`
- `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.csv`
- `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.md`

Supplementary Table S9 records figure readiness and score history. Supplementary Figures S1 to S7 are the current candidate figure set for manuscript and supplement packaging.

### S9. Manuscript source, citation, and arXiv checks

The manuscript source package is checked through SourceRight and repository-native arXiv gates. SourceRight validates the CSL JSON, generates the reference integrity report, and reconciles manuscript citation exports against the canonical reference set. The arXiv path checks source-package cleaning, filename safety, bibliography completeness, PDFLaTeX-compatible figure requirements, source-leak/privacy audit status, and CI preflight evidence.

Primary artefacts:

- `docs/paper/paper.tex`
- `docs/paper/references.csl.json`
- `docs/paper/sourceright-report.md`
- `docs/paper/sourceright-report.json`
- `docs/paper/source-inventory.json`
- `docs/paper/source-review-queue.jsonl`
- `docs/paper/arxiv-source-privacy-audit.json`
- `docs/paper/arxiv-source-privacy-audit.md`
- `.github/workflows/arxiv-preflight.yml`
- `scripts/maintenance/clean_arxiv_source_package.py`
- `scripts/maintenance/audit_arxiv_source_privacy.py`
- `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/arxiv_acceptance_checklist.md`
- `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/arxiv_toolchain_matrix.md`

Supplementary Table S10 records manuscript and arXiv submission gates. The current SourceRight run reports 11 matched citations and 0 citation reconciliation issues. The remaining SourceRight warnings are missing-DOI warnings for references that are standards pages, APIs, or URL-based resources rather than DOI-bearing articles.

### S10. Governance, citation, reuse, and change control

The ontology has governance and reuse documentation for readers who want to cite, extend, or migrate UOGTO. These artefacts record term-level changes, deprecations, replacement IRIs, migration notes, namespace IRIs, preferred prefixes, licence, release assets, and modelling decisions.

Primary artefacts:

- `docs/article-hardening/term-changelog.md`
- `docs/article-hardening/deprecation-policy.md`
- `docs/how-to-cite-and-reuse-uogto.md`
- `ontologies/core/uogto-governance.ttl`
- `docs/modelling-decisions.md`
- `docs/glossary.md`

Supplementary Table S11 records governance, citation, reuse, and change-control artefacts.

## Supplementary results

### Source discovery and screening

The evidence register records 39 source-extension records and the ontology-comparison package records 21 candidate source families. The comparison workflow distinguishes parsed RDF from metadata-only and literature-only evidence. This separation limits overclaiming. Source counts are used to describe search coverage, not to imply that every source was parsed or that every metadata record supports term-level mapping.

### Ontology validation

The quality metrics show that UOGTO's article-facing claims are backed by parse checks, annotation checks, SHACL example validation, competency queries, OWL profile screening, and reasoner status. The module audit table is the recommended reviewer entry point because it compresses these checks into a single table while preserving links to the machine-readable metrics.

### Mapping review and robustness

The mapping workflow generated 460 candidates and accepted 10 conservative alignments. One candidate remained marked for domain review and 449 candidates were rejected. The robustness and calibration artefacts show why these numbers should be read as precision-oriented review evidence rather than evidence of low coverage. UOGTO records candidate matches that look plausible but are not asserted.

### Case-study coverage

The case-study package demonstrates UOGTO across mechanism design, voting/social choice, security, MARL, ABM policy simulation, system dynamics, LLM-agent tool use, and executable trace/provenance settings. These cases are intended to test modelling reach. They are not a claim that every construct in each field has been fully formalized.

### Submission readiness

The submission package now contains a polished manuscript draft, this final supplement prose, SourceRight reference checks, Authentext audit reports, arXiv privacy audit manifests, PRISMA SVG/PDF exports, a created PowerPoint deck, and a completed first figure-score loop. Final submission should freeze figure numbering and caption text before rerunning the score loop and arXiv preflight.

## Supplementary tables

| Table | Title | Primary file |
| --- | --- | --- |
| Supplementary Table S1 | Protocol and reporting artefacts | `docs/article-hardening/protocol-checklist.md` |
| Supplementary Table S2 | Source register and evidence levels | `docs/article-hardening/source-extension-inventory.md` |
| Supplementary Table S3 | Module audit table | `docs/article-hardening/article-facing-tables/module-audit-table.csv` |
| Supplementary Table S4 | Mapping decision surface | `docs/ontology-comparison/mapping-review.csv` |
| Supplementary Table S5 | Mapping robustness, SSSOM, sensitivity, calibration, and adjudication | `docs/article-hardening/article-facing-tables/mapping-robustness-table.csv` |
| Supplementary Table S6 | Missing game-theory element dispositions | `docs/article-hardening/article-facing-tables/missing-game-theory-element-dispositions.csv` |
| Supplementary Table S7 | Case-study and use-case coverage | `docs/article-hardening/use-case-coverage-matrix.csv` |
| Supplementary Table S8 | Reproducibility and packaging artefacts | `docs/article-hardening/ro-crate-metadata.json` |
| Supplementary Table S9 | Figure readiness and score history | `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.csv` |
| Supplementary Table S10 | Manuscript, SourceRight, and arXiv gates | `docs/paper/sourceright-report.md`; `docs/paper/arxiv-source-privacy-audit.md` |
| Supplementary Table S11 | Governance, citation, reuse, and change control | `docs/how-to-cite-and-reuse-uogto.md`; `docs/article-hardening/term-changelog.md` |

## Supplementary figures

| Figure | Title | Primary file |
| --- | --- | --- |
| Supplementary Figure S1 | PRISMA-style source discovery flow | `docs/article-hardening/figures/prisma-2020-source-discovery-flow.svg`; `.pdf` |
| Supplementary Figure S2 | PRISMA-style screening flow | `docs/article-hardening/figures/prisma-2020-screening-flow.svg`; `.pdf` |
| Supplementary Figure S3 | Source-family evidence-level heatmap | `docs/ontology-comparison/figures/source_family_evidence_heatmap.svg` |
| Supplementary Figure S4 | Mapping flow from candidates to decisions | `docs/ontology-comparison/figures/mapping_flow_sankey.svg` |
| Supplementary Figure S5 | Source-module overlap heatmap | `docs/ontology-comparison/figures/source_module_overlap_heatmap.svg` |
| Supplementary Figure S6 | Source similarity network | `docs/ontology-comparison/figures/source_similarity_network.svg` |
| Supplementary Figure S7 | Reviewer workload and mapping review distribution | `docs/ontology-comparison/figures/reviewer_workload.svg` |

## Claim-to-supplement map

| Claim ID | Article claim | Supplement section | Evidence surface | Support level | Residual risk |
| --- | --- | --- | --- | --- | --- |
| C1 | UOGTO is a modular semantic layer for game-theoretic and executable evidence. | S3, S10 | `ontologies/`; `docs/modelling-decisions.md`; `ontologies/core/uogto-governance.ttl` | Strong internal evidence | Final copyedit should keep claims tied to validated modules. |
| C2 | Examples and competency questions validate against ontology and SHACL expectations. | S3 | `shapes/`; `examples/`; `competency-questions/`; `docs/article-hardening/competency-benchmark.md` | Strong local evidence | CI must remain green on the final submission commit. |
| C3 | Source discovery is evidence-levelled and scoping-review aligned. | S1, S2 | `docs/article-hardening/protocol.md`; `docs/article-hardening/search-log.jsonl`; `docs/article-hardening/source-extension-inventory.json` | Strong process evidence | Refresh live searches only if the manuscript makes current-date claims. |
| C4 | Ontology mappings are conservative and reviewable rather than blanket equivalence claims. | S4, S5 | `docs/ontology-comparison/mapping-review.csv`; `docs/ontology-comparison/accepted-alignments.sssom.tsv`; `docs/ontology-comparison/mapping-calibration.md` | Strong mapping evidence | Domain-review candidates should remain explicitly labelled. |
| C5 | Metadata-only sources are separated from parsed RDF and structured non-RDF sources. | S2, S7 | `docs/article-hardening/source-extension-inventory.json`; `docs/article-hardening/article-evidence-dashboard.json`; `docs/article-hardening/ro-crate-metadata.json` | Strong evidence-surface support | Dashboard should be regenerated from final artefacts. |
| C6 | Network and overlap analyses identify bridge concepts and sensitivity rather than universal coverage. | S5 | `docs/ontology-comparison/network-analysis.json`; `docs/ontology-comparison/network-sensitivity.md`; `docs/ontology-comparison/overlap-metrics.json` | Moderate to strong analysis support | Keep bridge claims conditional on sensitivity results. |
| C7 | Quality benchmarking covers annotations, orphan classes, relation richness, hierarchy depth, imports, SHACL, examples, competency questions, profile, and reasoner status. | S3 | `docs/article-hardening/quality-metrics.json`; `docs/article-hardening/reasoner-report.md`; `docs/article-hardening/robot/` | Strong metrics support | Preserve plain-English interpretation for non-ontology reviewers. |
| C8 | Reproducibility surfaces include RO-Crate, DuckDB design, tabular artefacts, dashboard outputs, SourceRight, arXiv checks, and CI. | S7, S9 | `docs/article-hardening/ro-crate-metadata.json`; `docs/article-hardening/duckdb-artifact-store.md`; `docs/paper/sourceright-report.md`; `.github/workflows/` | Strong package support | Re-run SourceRight and arXiv preflight after final citation changes. |
| C9 | The package is improved but not yet frozen for submission. | S8, S9 | `image_scores.csv`; `presubmission_decision_memo.md`; `docs/presentation/uogto_nature_presubmission_deck.pptx` | Strong review evidence | Freeze supplement prose, figure numbering, captions, and deck claims before submission. |

## Data and code availability

All supplement artefacts are stored in the repository. Human-readable tables are available as Markdown or CSV; machine-readable tables are available as JSON or Parquet where appropriate. The source package, SourceRight reports, Authentext reports, arXiv privacy audit, figure scorecard, and generated article-facing tables are version-controlled so that reviewers can trace article claims to concrete files.

## Supplement completion criteria

The supplement is ready for final submission packaging when:

- the manuscript claim set is frozen;
- Supplementary Tables S1 to S11 and Supplementary Figures S1 to S7 are the final numbering scheme;
- `make article-facing-tables`, `make manuscript-sourcecheck`, `make arxiv-privacy-audit`, and `make validate` pass;
- SourceRight reports 0 citation reconciliation issues;
- Authentext audit reports 0 high-signal findings for the supplement prose;
- final release DOI, namespace IRIs, licence, and preferred citation are synchronized across the paper, README, RO-Crate, and citation/reuse page.
