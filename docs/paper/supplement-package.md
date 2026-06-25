# UOGTO Supplement Package Map

Date: 2026-06-25

Purpose: this map turns the existing article-hardening, ontology-comparison, validation, mapping, and submission artifacts into a coherent supplement package. It is designed for peer reviewers, editors, and reproducibility reviewers who need to trace each article claim to the repo evidence surface that supports it.

Status: mapped for review. The evidence package is substantially assembled, but this file is not yet a typeset journal supplement. Final submission still needs edited supplement prose, final figure numbering, and journal-specific packaging.

## Reader Route

| Reader need | Start here | Then inspect | Decision use |
| --- | --- | --- | --- |
| Editorial novelty and claim boundaries | `docs/paper/paper.tex` | `docs/article-hardening/structured-summary.md`, `docs/article-hardening/uogto-inclusion-decisions.md` | Check whether claims stay within the evidence base. |
| Scoping-review method | `docs/article-hardening/protocol.md` | `docs/article-hardening/protocol-checklist.md`, `docs/article-hardening/prisma-scr-artifact-map.md`, `docs/article-hardening/search-strategy.md` | Check whether discovery and screening are auditable. |
| Source evidence | `docs/article-hardening/source-extension-inventory.md` | `docs/article-hardening/search-log.jsonl`, `docs/ontology-comparison/source-inventory.md`, `docs/ontology-comparison/source-provenance.json` | Check what was found, included, excluded, or treated as metadata only. |
| Ontology implementation | `ontologies/` | `shapes/`, `examples/`, `competency-questions/`, `docs/article-hardening/quality-metrics.json` | Check ontology structure, annotations, validation, and competency coverage. |
| Ontology mappings | `docs/ontology-comparison/accepted-alignments.sssom.tsv` | `docs/ontology-comparison/accepted-alignments.sssom.yml`, `docs/ontology-comparison/mapping-review.csv`, `docs/ontology-comparison/mapping-candidates.jsonl` | Check accepted, rejected, and domain-review mapping decisions. |
| Robustness and calibration | `docs/ontology-comparison/mapping-robustness.md` | `docs/ontology-comparison/mapping-calibration.md`, `docs/ontology-comparison/network-sensitivity.md`, `docs/ontology-comparison/overlap-metrics.json` | Check whether results depend on one matching method or source subset. |
| Reproducibility package | `docs/article-hardening/ro-crate-package.md` | `docs/article-hardening/ro-crate-metadata.json`, `docs/article-hardening/duckdb-artifact-store.md`, `docs/article-hardening/tabular-artifact-storage.md` | Check whether the evidence package can be rerun and reused. |
| Submission readiness | `docs/paper/sourceright-report.md` | `docs/paper/source-inventory.json`, `scripts/maintenance/arxiv_source_clean.py`, `.github/workflows/arxiv-preflight.yml` | Check citation/source review and arXiv packaging gates. |

## Supplement Structure

### Supplement 1. Protocol and Reporting Standards

Primary artifacts:
- `docs/article-hardening/protocol.md`
- `docs/article-hardening/protocol-checklist.md`
- `docs/article-hardening/prisma-scr-artifact-map.md`
- `docs/article-hardening/search-strategy.md`
- `docs/article-hardening/dual-screening.md`

Coverage: scoping-review protocol, PRISMA-ScR artifact linkage, search and screening workflow, reviewer roles, and red-team challenge process.

Open work: convert the protocol checklist into a final journal supplement table after the manuscript claim set is frozen.

### Supplement 2. Source Register and Evidence Levels

Primary artifacts:
- `docs/article-hardening/search-log.jsonl`
- `docs/article-hardening/source-extension-inventory.json`
- `docs/article-hardening/source-extension-inventory.md`
- `docs/ontology-comparison/source-inventory.json`
- `docs/ontology-comparison/source-provenance.json`
- `docs/ontology-comparison/inclusion-exclusion-log.jsonl`

Coverage: query log, result counts, inclusion rationales, evidence levels, licences, source-family coverage, metadata-only sources, structured non-RDF sources, parsed RDF sources, literature-only sources, exclusions, and negative evidence.

Open work: keep the append-only search log current if further live discovery is performed before submission.

### Supplement 3. Ontology Implementation and Validation

Primary artifacts:
- `ontologies/`
- `shapes/`
- `examples/`
- `competency-questions/`
- `docs/article-hardening/quality-metrics.json`
- `docs/article-hardening/reasoner-report.md`
- `docs/article-hardening/competency-benchmark.md`
- `docs/article-hardening/robot/`

Coverage: module structure, labels and definitions, object/datatype property separation, SHACL validation, example graph coverage, competency-query execution, annotation completeness, orphan classes, relation richness, hierarchy depth, import depth, OWL profile, and reasoner status.

Open work: add a compact module audit table to the manuscript or supplement so reviewers do not need to infer coverage from raw validation outputs.

### Supplement 4. Mapping and Alignment Evidence

Primary artifacts:
- `docs/ontology-comparison/term-inventory.jsonl`
- `docs/ontology-comparison/mapping-candidates.jsonl`
- `docs/ontology-comparison/mapping-review.csv`
- `docs/ontology-comparison/accepted-alignments.ttl`
- `docs/ontology-comparison/accepted-alignments.sssom.tsv`
- `docs/ontology-comparison/accepted-alignments.sssom.yml`

Coverage: source term inventory, candidate mappings, accepted mappings, rejected mappings, domain-review mappings, RDF alignment outputs, and SSSOM tabular metadata for review and publication.

Current article-safe framing: the mapping evidence supports conservative alignment and bridge analysis. It does not support a claim that every relevant game-theory or simulation ontology has been exhaustively mapped.

### Supplement 5. Robustness, Calibration, and Network Analyses

Primary artifacts:
- `docs/ontology-comparison/mapping-robustness.md`
- `docs/ontology-comparison/mapping-robustness/`
- `docs/ontology-comparison/mapping-calibration.md`
- `docs/ontology-comparison/mapping-calibration/`
- `docs/ontology-comparison/network-analysis.json`
- `docs/ontology-comparison/network-sensitivity.json`
- `docs/ontology-comparison/network-sensitivity.md`
- `docs/ontology-comparison/overlap-metrics.json`

Coverage: ablation over label, normalized label, definition similarity, hierarchy context, property signature, embedding similarity, reviewer calibration, adjudication outcomes, source-family sensitivity, accepted-only networks, close/related mapping networks, and metadata-only source exclusion.

Open work: distill this into one article table and one supplement figure that state which conclusions are robust across sensitivity settings.

### Supplement 6. Case Studies and Use-Case Coverage

Primary artifacts:
- `docs/article-hardening/case-studies.md`
- `docs/article-hardening/case-studies.json`
- `docs/article-hardening/use-case-coverage-matrix.csv`
- `docs/article-hardening/use-case-coverage-matrix.json`
- `docs/article-hardening/uogto-inclusion-decisions.md`

Coverage: auction and mechanism design, voting and social choice, security and Stackelberg games, MARL Markov games, ABM policy simulation, system-dynamics feedback games, LLM-agent tool-use games, executable trace and provenance cases, and missing-game-theory-element dispositions.

Open work: select two or three cases for the main article and keep the remaining cases in the supplement.

### Supplement 7. Reproducibility and Packaging

Primary artifacts:
- `docs/article-hardening/ro-crate-package.md`
- `docs/article-hardening/ro-crate-metadata.json`
- `docs/article-hardening/duckdb-artifact-store.md`
- `docs/article-hardening/tabular-artifact-storage.md`
- `docs/article-hardening/article-evidence-dashboard.md`
- `docs/article-hardening/article-evidence-dashboard.json`
- `docs/article-hardening/article-evidence-dashboard.html`

Coverage: RO-Crate metadata, root data entity, data entities, contextual entities, workflow/script provenance, DuckDB artifact-store design, CSV/Markdown plus JSON/Parquet table storage, and validated dashboard surfaces.

Open work: ensure the final release archive includes the same files named in this map and that dashboard links are stable.

### Supplement 8. Figures, Tables, and Visual Evidence

Primary artifacts:
- `docs/article-hardening/figures/`
- `docs/ontology-comparison/figures/`
- `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.csv`
- `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/image_scores.md`

Coverage: PRISMA-style flow diagrams, source-family coverage heatmaps, mapping robustness visualizations, network sensitivity figures, dashboard figures, and per-image Nature-readiness scores.

Open work: figure loops remain incomplete because no image is yet scored 100 out of 100. Final submission needs exported, PDFLaTeX-compatible, caption-aligned figures with accessibility checks.

### Supplement 9. Manuscript Source, Citation, and arXiv Checks

Primary artifacts:
- `docs/paper/paper.tex`
- `docs/paper/references.csl.json`
- `docs/paper/sourceright-report.md`
- `docs/paper/sourceright-report.json`
- `docs/paper/source-inventory.json`
- `docs/paper/source-review-queue.jsonl`
- `.github/workflows/arxiv-preflight.yml`
- `scripts/maintenance/arxiv_source_clean.py`
- `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/arxiv_acceptance_checklist.md`
- `conductor/tracks/uogto_nature_presubmission_evaluation_20260625/arxiv_toolchain_matrix.md`

Coverage: citation extraction, SourceRight CSL validation, source-review queue, arXiv cleaner, source package preflight, filename safety, bibliography completeness, PDFLaTeX-compatible figure requirement, and external arXiv toolchain review.

Open work: add an explicit source-leak and privacy audit manifest instead of relying only on cleaner and CI inference.

### Supplement 10. Governance, Citation, Reuse, and Change Control

Primary artifacts:
- `docs/article-hardening/term-changelog.md`
- `docs/article-hardening/deprecation-policy.md`
- `docs/how-to-cite-and-reuse-uogto.md`
- `ontologies/uogto-governance.ttl`
- `docs/modelling-decisions.md`
- `docs/glossary.md`

Coverage: term-level changes, deprecation policy, replacement IRIs, migration notes, ontology governance metadata, citation guidance, namespace IRIs, preferred prefixes, release assets, licence, and modelling decisions.

Open work: align final DOI and release asset names after the release candidate is cut.

## Claim-to-Supplement Map

| Claim ID | Article claim | Primary supplement section | Evidence surface | Support level | Residual risk |
| --- | --- | --- | --- | --- | --- |
| C1 | UOGTO is a modular semantic layer for game-theoretic and executable evidence. | S3, S10 | `ontologies/`, `docs/modelling-decisions.md`, `ontologies/uogto-governance.ttl` | Strong internal evidence | Needs final module audit table. |
| C2 | The repository validates examples and competency questions against ontology and SHACL expectations. | S3 | `shapes/`, `examples/`, `competency-questions/`, `docs/article-hardening/competency-benchmark.md` | Strong local evidence | CI evidence should remain green on final commit. |
| C3 | Source discovery is conducted as an evidence-levelled scoping-review workflow. | S1, S2 | `protocol.md`, `search-log.jsonl`, `source-extension-inventory.json`, `prisma-scr-artifact-map.md` | Strong process evidence | Searches should be timestamped again if claims become current-date claims. |
| C4 | Mapping results are conservative and reviewable, not a blanket equivalence claim. | S4, S5 | `mapping-review.csv`, `accepted-alignments.sssom.tsv`, `mapping-calibration.md` | Strong evidence for conservative mapping | Domain-review candidates need explicit final dispositions. |
| C5 | Metadata-only sources are separated from parsed RDF and structured non-RDF sources. | S2, S7 | `source-extension-inventory.json`, `article-evidence-dashboard.json`, `ro-crate-metadata.json` | Strong evidence-surface support | Dashboard must stay regenerated from final artifacts. |
| C6 | Network and overlap analyses identify bridge concepts and sensitivity, not universal ontology coverage. | S5 | `network-analysis.json`, `network-sensitivity.md`, `overlap-metrics.json` | Moderate to strong analysis support | Needs article-facing compact table and figure. |
| C7 | Quality benchmarking covers annotations, orphan classes, relation richness, hierarchy depth, imports, SHACL coverage, examples, competency questions, profile, and reasoner status. | S3 | `quality-metrics.json`, `reasoner-report.md`, `robot/` | Strong metrics support | Add plain-English interpretation for non-ontology reviewers. |
| C8 | Reproducibility surfaces include RO-Crate, DuckDB design, tabular artifacts, dashboard outputs, SourceRight, arXiv checks, and WIDOCO/validation CI. | S7, S9 | `ro-crate-metadata.json`, `duckdb-artifact-store.md`, `.github/workflows/`, `docs/paper/sourceright-report.md` | Strong package support | Explicit privacy audit manifest still needed. |
| C9 | The work is submission-adjacent but not yet final Nature-ready. | S8, S9 | `image_scores.csv`, `presubmission_decision_memo.md`, `powerpoint_asset_inventory.md` | Strong review evidence | Figure loops, deck creation, privacy audit, and final supplement prose remain. |

## Package Completion Criteria

The supplement package is complete when:
- Every manuscript claim has a row in `docs/paper/supplement-claim-map.csv`.
- Every row names a primary artifact, support level, and residual risk.
- Every figure referenced in the manuscript has a supplement caption source and image score.
- The final source package contains the same artifact set listed here.
- The source-leak and privacy audit manifest is present and reviewed.
- The final release DOI, namespace IRIs, licence, and preferred citation are synchronized across the paper, README, RO-Crate, and citation/reuse page.
