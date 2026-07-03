"""Export tabular analysis artifacts in human-readable and machine-stable forms."""

from __future__ import annotations

import csv
import json
from pathlib import Path

try:
    import pandas as pd
except ModuleNotFoundError:  # pragma: no cover - exercised in minimal Pixi environments
    pd = None


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "article-hardening"
TABLES = [
    DOCS / "manual-review-sample.csv",
    DOCS / "dual-screening-sample.csv",
    DOCS / "uogto-inclusion-candidates.csv",
    DOCS / "use-case-coverage-matrix.csv",
]


def _tolerant_read_csv(path: Path) -> pd.DataFrame:
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader(fh)
        rows = list(reader)
    if not rows:
        return pd.DataFrame() if pd is not None else []
    header = rows[0]
    width = len(header)
    normalized = []
    for row in rows[1:]:
        if len(row) < width:
            row = row + [""] * (width - len(row))
        elif len(row) > width:
            row = row[: width - 1] + [",".join(row[width - 1 :])]
        normalized.append(row)
    if HAS_PANDAS:
        return pd.DataFrame(normalized, columns=header)
    return [dict(zip(header, row, strict=False)) for row in normalized]


def _escape_markdown(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", r"\|").replace("\n", "<br>")


def _columns(table) -> list[str]:
    if HAS_PANDAS:
        return list(table.columns)
    return list(table[0]) if table else []


def _row_count(table) -> int:
    return int(len(table))


def _records(table) -> list[dict]:
    if HAS_PANDAS:
        return table.to_dict(orient="records")
    return list(table)


def _to_markdown(table) -> str:
    headers = _columns(table)
    lines = [
        "| " + " | ".join(_escape_markdown(col) for col in headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    rows = _records(table)
    for row in rows:
        lines.append("| " + " | ".join(_escape_markdown(row[col]) for col in headers) + " |")
    return "\n".join(lines) + "\n"


def export_table(csv_path: Path) -> None:
    table = _tolerant_read_csv(csv_path)
    base = csv_path.with_suffix("")

    md_path = base.with_suffix(".md")
    md_path.write_text(
        (
            f"# {csv_path.stem.replace('-', ' ').title()}\n\n"
            f"Source CSV: `{csv_path.as_posix()}`\n"
            f"Rows: {_row_count(table)}\n\n"
            + _to_markdown(table)
        ),
        encoding="utf-8",
        newline="\n",
    )

    json_path = base.with_suffix(".json")
    json_payload = {
        "source_csv": csv_path.as_posix(),
        "row_count": _row_count(table),
        "columns": _columns(table),
        "rows": _records(table),
    }
    json_path.write_text(
        json.dumps(json_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    parquet_path = base.with_suffix(".parquet")
    if HAS_PANDAS:
        table.to_parquet(parquet_path, index=False)
    elif not parquet_path.exists():
        raise SystemExit(
            f"Cannot write {parquet_path} because pandas is not installed and no checked-in parquet exists"
        )


def main() -> None:
    for csv_path in TABLES:
        if not csv_path.exists():
            raise SystemExit(f"Missing source table: {csv_path}")
        export_table(csv_path)


if __name__ == "__main__":
    main()
