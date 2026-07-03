from __future__ import annotations

import csv
import json
import os
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path

try:
    import duckdb
except ModuleNotFoundError:  # pragma: no cover - depends on optional local environment
    duckdb = None


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"
DB_PATH = DOCS / "article-hardening.duckdb"
STATUS_PATH = DOCS / "article-hardening-duckdb-status.json"

SEARCH_LOG = DOCS / "search-log.jsonl"
SOURCE_EXTENSION_INVENTORY = DOCS / "source-extension-inventory.json"
MANUAL_REVIEW_SAMPLE = DOCS / "manual-review-sample.csv"
DUAL_SCREENING_SAMPLE = DOCS / "dual-screening-sample.csv"
UOGTO_INCLUSION_CANDIDATES = DOCS / "uogto-inclusion-candidates.csv"
USE_CASE_COVERAGE_MATRIX = DOCS / "use-case-coverage-matrix.csv"


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def read_tsv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return [dict(row) for row in reader]


def flatten_records(value) -> list[dict]:
    if value is None:
        return []
    if isinstance(value, list):
        rows: list[dict] = []
        for item in value:
            if isinstance(item, dict):
                rows.append(item)
            else:
                rows.append({"value": item})
        return rows
    if isinstance(value, dict):
        if "records" in value and isinstance(value["records"], list):
            return flatten_records(value["records"])
        if "sources" in value and isinstance(value["sources"], list):
            return flatten_records(value["sources"])
        return [value]
    return [{"value": value}]


def normalize_row(row: dict, *, source_path: str, family: str) -> dict:
    normalized = {key: value for key, value in row.items()}
    normalized["source_path"] = source_path
    normalized["family"] = family
    normalized["ingested_at"] = datetime.now(timezone.utc).isoformat()
    normalized["raw_json"] = json.dumps(row, ensure_ascii=False, sort_keys=True)
    return normalized


def register_rows(con: duckdb.DuckDBPyConnection, table_name: str, rows: list[dict]) -> None:
    if rows:
        con.register(f"{table_name}_view", rows)
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM {table_name}_view")
        con.unregister(f"{table_name}_view")
    else:
        con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM (SELECT NULL AS placeholder) WHERE FALSE")


def ingest_sources() -> list[dict]:
    if not SOURCE_EXTENSION_INVENTORY.exists():
        return []
    payload = read_json(SOURCE_EXTENSION_INVENTORY)
    rows = []
    for row in flatten_records(payload):
        rows.append(normalize_row(row, source_path=str(SOURCE_EXTENSION_INVENTORY), family="sources"))
    return rows


def ingest_search_logs() -> list[dict]:
    if not SEARCH_LOG.exists():
        return []
    rows = []
    for row in read_jsonl(SEARCH_LOG):
        rows.append(normalize_row(row, source_path=str(SEARCH_LOG), family="search_logs"))
    return rows


def ingest_csv_family(path: Path, family: str) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for row in read_csv(path):
        rows.append(normalize_row(row, source_path=str(path), family=family))
    return rows


def discover_optional_tsvs(patterns: Iterable[str]) -> list[Path]:
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(sorted(DOCS.glob(pattern)))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in candidates:
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        unique.append(path)
    return unique


def ingest_mappings() -> list[dict]:
    rows: list[dict] = []
    for path in discover_optional_tsvs(["*mapping*.tsv", "*mappings*.tsv", "*sssom*.tsv", "*alignment*.tsv"]):
        for row in read_tsv(path):
            rows.append(normalize_row(row, source_path=str(path), family="mappings"))
    return rows


def ingest_metrics() -> list[dict]:
    rows: list[dict] = []
    for path in discover_optional_tsvs(["*metric*.csv", "*metrics*.csv", "*benchmark*.csv", "*metric*.tsv", "*metrics*.tsv"]):
        reader_rows = read_csv(path) if path.suffix.lower() == ".csv" else read_tsv(path)
        for row in reader_rows:
            rows.append(normalize_row(row, source_path=str(path), family="metrics"))
    for path in discover_optional_tsvs(["*metric*.json", "*metrics*.json"]):
        payload = read_json(path)
        for row in flatten_records(payload):
            rows.append(normalize_row(row, source_path=str(path), family="metrics"))
    return rows


def ingest_reviewer_decisions() -> list[dict]:
    rows: list[dict] = []
    for path in [MANUAL_REVIEW_SAMPLE, DUAL_SCREENING_SAMPLE]:
        rows.extend(ingest_csv_family(path, "reviewer_decisions"))
    for path in discover_optional_tsvs(["*review*.csv", "*review*.tsv", "*decision*.csv", "*decision*.tsv"]):
        rows.extend(ingest_csv_family(path, "reviewer_decisions"))
    return rows


def ingest_figures() -> list[dict]:
    rows: list[dict] = []
    figure_files = discover_optional_tsvs(["*.png", "*.svg", "*.jpg", "*.jpeg", "*.webp", "*.pdf"])
    for path in figure_files:
        rows.append(
            normalize_row(
                {
                    "figure_path": str(path),
                    "figure_name": path.stem,
                    "figure_extension": path.suffix.lower().lstrip("."),
                },
                source_path=str(path),
                family="figures",
            )
        )
    for path in discover_optional_tsvs(["*figure*.json", "*figures*.json", "*figure*.md", "*figures*.md"]):
        if path.suffix.lower() == ".json":
            payload = read_json(path)
            for row in flatten_records(payload):
                rows.append(normalize_row(row, source_path=str(path), family="figures"))
        else:
            rows.append(
                normalize_row(
                    {
                        "figure_path": str(path),
                        "figure_name": path.stem,
                        "figure_note": path.read_text(encoding="utf-8"),
                    },
                    source_path=str(path),
                    family="figures",
                )
            )
    return rows


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    if duckdb is None:
        STATUS_PATH.write_text(
            json.dumps(
                {
                    "schema": "uogto.article-hardening.duckdb-status.v1",
                    "status": "optional_dependency_unavailable",
                    "database": str(DB_PATH.relative_to(ROOT)),
                    "dependency": "duckdb",
                    "fallback": "article evidence dashboard reads JSON/CSV artifacts directly when the DuckDB store is absent",
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        print("DuckDB optional dependency is unavailable; recorded portable fallback status.")
        return
    if DB_PATH.exists():
        DB_PATH.unlink()

    con = duckdb.connect(str(DB_PATH))
    con.execute("PRAGMA enable_progress_bar=false")
    con.execute("CREATE SCHEMA IF NOT EXISTS article_hardening")
    con.execute("SET schema 'article_hardening'")

    register_rows(con, "sources", ingest_sources())
    register_rows(con, "search_logs", ingest_search_logs())
    register_rows(con, "mappings", ingest_mappings())
    register_rows(con, "metrics", ingest_metrics())
    register_rows(con, "reviewer_decisions", ingest_reviewer_decisions())
    register_rows(con, "figures", ingest_figures())

    con.execute(
        """
        CREATE OR REPLACE TABLE manifest AS
        SELECT
            'article-hardening.duckdb' AS database_name,
            CURRENT_TIMESTAMP AS created_at,
            (
                SELECT COUNT(*) FROM sources
            ) AS source_rows,
            (
                SELECT COUNT(*) FROM search_logs
            ) AS search_log_rows,
            (
                SELECT COUNT(*) FROM mappings
            ) AS mapping_rows,
            (
                SELECT COUNT(*) FROM metrics
            ) AS metric_rows,
            (
                SELECT COUNT(*) FROM reviewer_decisions
            ) AS reviewer_decision_rows,
            (
                SELECT COUNT(*) FROM figures
            ) AS figure_rows
        """
    )
    con.close()
    STATUS_PATH.write_text(
        json.dumps(
            {
                "schema": "uogto.article-hardening.duckdb-status.v1",
                "status": "built",
                "database": str(DB_PATH.relative_to(ROOT)),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
