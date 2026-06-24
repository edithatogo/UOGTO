"""Export tabular analysis artifacts in human-readable and machine-stable forms."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd


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
        return pd.DataFrame()
    header = rows[0]
    width = len(header)
    normalized = []
    for row in rows[1:]:
        if len(row) < width:
            row = row + [""] * (width - len(row))
        elif len(row) > width:
            row = row[: width - 1] + [",".join(row[width - 1 :])]
        normalized.append(row)
    return pd.DataFrame(normalized, columns=header)


def _escape_markdown(value: object) -> str:
    text = "" if value is None else str(value)
    return text.replace("|", r"\|").replace("\n", "<br>")


def _to_markdown(df: pd.DataFrame) -> str:
    headers = list(df.columns)
    lines = [
        "| " + " | ".join(_escape_markdown(col) for col in headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(_escape_markdown(row[col]) for col in headers) + " |")
    return "\n".join(lines) + "\n"


def export_table(csv_path: Path) -> None:
    df = _tolerant_read_csv(csv_path)
    base = csv_path.with_suffix("")

    md_path = base.with_suffix(".md")
    md_path.write_text(
        (
            f"# {csv_path.stem.replace('-', ' ').title()}\n\n"
            f"Source CSV: `{csv_path.as_posix()}`\n"
            f"Rows: {len(df)}\n\n"
            + _to_markdown(df)
        ),
        encoding="utf-8",
        newline="\n",
    )

    json_path = base.with_suffix(".json")
    json_payload = {
        "source_csv": csv_path.as_posix(),
        "row_count": int(len(df)),
        "columns": list(df.columns),
        "rows": df.to_dict(orient="records"),
    }
    json_path.write_text(
        json.dumps(json_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    parquet_path = base.with_suffix(".parquet")
    df.to_parquet(parquet_path, index=False)


def main() -> None:
    for csv_path in TABLES:
        if not csv_path.exists():
            raise SystemExit(f"Missing source table: {csv_path}")
        export_table(csv_path)


if __name__ == "__main__":
    main()
