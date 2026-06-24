# Tabular Artifact Storage

tabular analysis artifacts in the article-hardening package should be stored in both human-readable and machine-stable forms where the table is part of the evidence package rather than a transient note.

## Required formats

- Human-readable source: CSV or Markdown
- Machine-stable source: JSON or Parquet

## Current table families

- `manual-review-sample`
- `dual-screening-sample`
- `uogto-inclusion-candidates`
- `use-case-coverage-matrix`

## Storage rule

When a table is used for screening, review, or synthesis, keep a CSV source for compact interchange, a Markdown rendering for review, and JSON plus Parquet exports for stable downstream analysis.

## Reproducibility note

The generated files are produced from `scripts/maintenance/export_tabular_artifacts.py` and should be regenerated whenever the CSV source changes.
