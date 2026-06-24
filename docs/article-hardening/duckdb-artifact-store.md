# DuckDB Artifact Store

This repository keeps a lightweight DuckDB database for the article-hardening
evidence set so the main analysis surfaces can be queried consistently without
giving up the human-readable CSV, Markdown, JSON, and Parquet exports.

The database is built from the current repo artifacts and is intended to hold:

- sources
- search logs
- mappings
- metrics
- reviewer decisions
- figures

The store is populated by
[`scripts/maintenance/build_article_hardening_duckdb.py`](../../scripts/maintenance/build_article_hardening_duckdb.py)
and writes the database file to
`docs/article-hardening/article-hardening.duckdb`.

The builder is intentionally tolerant:

- JSONL sources are loaded row by row.
- JSON inputs are normalized from either list or object-shaped records.
- CSV and TSV inputs are ingested where present.
- Missing families are created as empty tables so downstream SQL stays stable.

The database is a convenience layer over the canonical artifact files, not a
replacement for them.
