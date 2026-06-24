from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"
DB_PATH = DOCS / "article-hardening.duckdb"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def read_csv(path: Path, *, delimiter: str = ",") -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        return [dict(row) for row in reader]


def flatten_records(value) -> list[dict]:
    if value is None:
        return []
    if isinstance(value, list):
        rows: list[dict] = []
        for item in value:
            rows.extend(flatten_records(item))
        return rows
    if isinstance(value, dict):
        if "records" in value:
            return flatten_records(value["records"])
        if "sources" in value:
            return flatten_records(value["sources"])
        return [value]
    return [{"value": value}]


def as_text(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def as_int(value):
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return None


def as_float(value):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def ensure_table(con: duckdb.DuckDBPyConnection, name: str, schema: str) -> None:
    con.execute(f"CREATE OR REPLACE TABLE {name} ({schema})")


def insert_rows(con: duckdb.DuckDBPyConnection, table: str, columns: list[str], rows: list[tuple]) -> None:
    if not rows:
        return
    placeholders = ", ".join(["?"] * len(columns))
    con.executemany(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})", rows)


def source_rows() -> list[tuple]:
    path = DOCS / "source-extension-inventory.json"
    if not path.exists():
        return []
    payload = read_json(path)
    rows = []
    for item in flatten_records(payload):
        rows.append(
            (
                str(path),
                now(),
                as_text(item.get("id") or item.get("iri") or item.get("source") or item.get("name")),
                as_text(item.get("label") or item.get("title") or item.get("source_label")),
                as_text(item.get("evidence_level") or item.get("evidenceLevel")),
                as_text(item.get("licence") or item.get("license")),
                as_text(item.get("reviewer_handoff") or item.get("handoff")),
                json.dumps(item, ensure_ascii=False, sort_keys=True),
            )
        )
    return rows


def search_log_rows() -> list[tuple]:
    path = DOCS / "search-log.jsonl"
    if not path.exists():
        return []
    rows = []
    for item in read_jsonl(path):
        rows.append(
            (
                str(path),
                now(),
                as_text(item.get("query") or item.get("search_query") or item.get("term")),
                as_int(item.get("result_count") or item.get("results") or item.get("count")),
                as_text(item.get("evidence_level") or item.get("evidenceLevel")),
                as_text(item.get("inclusion_rationale") or item.get("rationale")),
                as_text(item.get("licence") or item.get("license")),
                as_text(item.get("reviewer_handoff") or item.get("handoff")),
                json.dumps(item, ensure_ascii=False, sort_keys=True),
            )
        )
    return rows


def mapping_rows() -> list[tuple]:
    rows = []
    for path in sorted(DOCS.glob("*mapping*.tsv")) + sorted(DOCS.glob("*mappings*.tsv")) + sorted(DOCS.glob("*sssom*.tsv")) + sorted(DOCS.glob("*alignment*.tsv")):
        if not path.is_file():
            continue
        for item in read_csv(path, delimiter="\t"):
            rows.append(
                (
                    str(path),
                    now(),
                    as_text(item.get("subject_id") or item.get("subject")),
                    as_text(item.get("predicate_id") or item.get("predicate")),
                    as_text(item.get("object_id") or item.get("object")),
                    as_text(item.get("mapping_justification") or item.get("justification")),
                    as_float(item.get("confidence") or item.get("similarity")),
                    json.dumps(item, ensure_ascii=False, sort_keys=True),
                )
            )
    return rows


def metric_rows() -> list[tuple]:
    rows = []
    for path in sorted(DOCS.glob("*metric*.csv")) + sorted(DOCS.glob("*metrics*.csv")) + sorted(DOCS.glob("*benchmark*.csv")) + sorted(DOCS.glob("*metric*.tsv")) + sorted(DOCS.glob("*metrics*.tsv")):
        if not path.is_file():
            continue
        reader_rows = read_csv(path) if path.suffix.lower() == ".csv" else read_csv(path, delimiter="\t")
        for item in reader_rows:
            rows.append(
                (
                    str(path),
                    now(),
                    as_text(item.get("metric") or item.get("metric_name") or item.get("name")),
                    as_float(item.get("value") or item.get("metric_value")),
                    as_text(item.get("unit")),
                    as_text(item.get("module") or item.get("scope")),
                    json.dumps(item, ensure_ascii=False, sort_keys=True),
                )
            )
    for path in sorted(DOCS.glob("*metric*.json")) + sorted(DOCS.glob("*metrics*.json")):
        if not path.is_file():
            continue
        for item in flatten_records(read_json(path)):
            rows.append(
                (
                    str(path),
                    now(),
                    as_text(item.get("metric") or item.get("metric_name") or item.get("name")),
                    as_float(item.get("value") or item.get("metric_value")),
                    as_text(item.get("unit")),
                    as_text(item.get("module") or item.get("scope")),
                    json.dumps(item, ensure_ascii=False, sort_keys=True),
                )
            )
    return rows


def reviewer_decision_rows() -> list[tuple]:
    rows = []
    for path in [DOCS / "manual-review-sample.csv", DOCS / "dual-screening-sample.csv"]:
        if not path.exists():
            continue
        for item in read_csv(path):
            rows.append(
                (
                    str(path),
                    now(),
                    as_text(item.get("reviewer") or item.get("reviewer_id")),
                    as_text(item.get("item") or item.get("mapping") or item.get("source")),
                    as_text(item.get("decision") or item.get("status") or item.get("label")),
                    as_text(item.get("rationale") or item.get("note")),
                    json.dumps(item, ensure_ascii=False, sort_keys=True),
                )
            )
    for path in sorted(DOCS.glob("*review*.csv")) + sorted(DOCS.glob("*review*.tsv")) + sorted(DOCS.glob("*decision*.csv")) + sorted(DOCS.glob("*decision*.tsv")):
        if not path.is_file() or path.name in {"manual-review-sample.csv", "dual-screening-sample.csv"}:
            continue
        reader_rows = read_csv(path) if path.suffix.lower() == ".csv" else read_csv(path, delimiter="\t")
        for item in reader_rows:
            rows.append(
                (
                    str(path),
                    now(),
                    as_text(item.get("reviewer") or item.get("reviewer_id")),
                    as_text(item.get("item") or item.get("mapping") or item.get("source")),
                    as_text(item.get("decision") or item.get("status") or item.get("label")),
                    as_text(item.get("rationale") or item.get("note")),
                    json.dumps(item, ensure_ascii=False, sort_keys=True),
                )
            )
    return rows


def figure_rows() -> list[tuple]:
    rows = []
    for path in sorted(DOCS.glob("*.png")) + sorted(DOCS.glob("*.svg")) + sorted(DOCS.glob("*.jpg")) + sorted(DOCS.glob("*.jpeg")) + sorted(DOCS.glob("*.webp")) + sorted(DOCS.glob("*.pdf")):
        if path.is_file():
            rows.append((str(path), now(), str(path), path.stem, None, json.dumps({"figure_path": str(path), "figure_name": path.stem}, ensure_ascii=False, sort_keys=True)))
    for path in sorted(DOCS.glob("*figure*.json")) + sorted(DOCS.glob("*figures*.json")) + sorted(DOCS.glob("*figure*.md")) + sorted(DOCS.glob("*figures*.md")):
        if not path.is_file():
            continue
        if path.suffix.lower() == ".json":
            for item in flatten_records(read_json(path)):
                rows.append(
                    (
                        str(path),
                        now(),
                        as_text(item.get("figure_path") or item.get("path")),
                        as_text(item.get("figure_name") or item.get("name") or path.stem),
                        as_text(item.get("caption") or item.get("title")),
                        json.dumps(item, ensure_ascii=False, sort_keys=True),
                    )
                )
        else:
            rows.append((str(path), now(), str(path), path.stem, as_text(path.read_text(encoding="utf-8")), json.dumps({"figure_path": str(path), "figure_name": path.stem}, ensure_ascii=False, sort_keys=True)))
    return rows


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists():
        DB_PATH.unlink()

    con = duckdb.connect(str(DB_PATH))
    con.execute("PRAGMA enable_progress_bar=false")

    ensure_table(con, "sources", """
        source_path VARCHAR,
        ingested_at TIMESTAMP,
        source_id VARCHAR,
        source_label VARCHAR,
        evidence_level VARCHAR,
        licence VARCHAR,
        reviewer_handoff VARCHAR,
        payload_json VARCHAR
    """)
    ensure_table(con, "search_logs", """
        source_path VARCHAR,
        ingested_at TIMESTAMP,
        query VARCHAR,
        result_count BIGINT,
        evidence_level VARCHAR,
        inclusion_rationale VARCHAR,
        licence VARCHAR,
        reviewer_handoff VARCHAR,
        payload_json VARCHAR
    """)
    ensure_table(con, "mappings", """
        source_path VARCHAR,
        ingested_at VARCHAR,
        subject_id VARCHAR,
        predicate_id VARCHAR,
        object_id VARCHAR,
        mapping_justification VARCHAR,
        confidence DOUBLE,
        payload_json VARCHAR
    """)
    ensure_table(con, "metrics", """
        source_path VARCHAR,
        ingested_at TIMESTAMP,
        metric_name VARCHAR,
        metric_value DOUBLE,
        unit VARCHAR,
        module VARCHAR,
        payload_json VARCHAR
    """)
    ensure_table(con, "reviewer_decisions", """
        source_path VARCHAR,
        ingested_at TIMESTAMP,
        reviewer VARCHAR,
        item_id VARCHAR,
        decision VARCHAR,
        rationale VARCHAR,
        payload_json VARCHAR
    """)
    ensure_table(con, "figures", """
        source_path VARCHAR,
        ingested_at TIMESTAMP,
        figure_path VARCHAR,
        figure_name VARCHAR,
        caption VARCHAR,
        payload_json VARCHAR
    """)

    insert_rows(con, "sources", ["source_path", "ingested_at", "source_id", "source_label", "evidence_level", "licence", "reviewer_handoff", "payload_json"], source_rows())
    insert_rows(con, "search_logs", ["source_path", "ingested_at", "query", "result_count", "evidence_level", "inclusion_rationale", "licence", "reviewer_handoff", "payload_json"], search_log_rows())
    insert_rows(con, "mappings", ["source_path", "ingested_at", "subject_id", "predicate_id", "object_id", "mapping_justification", "confidence", "payload_json"], mapping_rows())
    insert_rows(con, "metrics", ["source_path", "ingested_at", "metric_name", "metric_value", "unit", "module", "payload_json"], metric_rows())
    insert_rows(con, "reviewer_decisions", ["source_path", "ingested_at", "reviewer", "item_id", "decision", "rationale", "payload_json"], reviewer_decision_rows())
    insert_rows(con, "figures", ["source_path", "ingested_at", "figure_path", "figure_name", "caption", "payload_json"], figure_rows())

    con.execute("""
        CREATE OR REPLACE TABLE manifest AS
        SELECT
            'article-hardening.duckdb' AS database_name,
            CURRENT_TIMESTAMP AS created_at,
            (SELECT COUNT(*) FROM sources) AS source_rows,
            (SELECT COUNT(*) FROM search_logs) AS search_log_rows,
            (SELECT COUNT(*) FROM mappings) AS mapping_rows,
            (SELECT COUNT(*) FROM metrics) AS metric_rows,
            (SELECT COUNT(*) FROM reviewer_decisions) AS reviewer_decision_rows,
            (SELECT COUNT(*) FROM figures) AS figure_rows
    """)
    con.close()


if __name__ == "__main__":
    main()
