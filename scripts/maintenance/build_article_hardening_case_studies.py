from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "docs" / "article-hardening" / "case-studies.json"
OUTPUT_PATH = ROOT / "docs" / "article-hardening" / "case-studies.md"


def _load() -> dict:
    with DATA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _format_list(values: list[str]) -> str:
    return ", ".join(values)


def build_markdown(payload: dict) -> str:
    lines: list[str] = []
    lines.append("# Article Hardening Case Studies")
    lines.append("")
    lines.append(
        "This register captures the case studies that should be used to stress-test UOGTO before expanding the ontology further."
    )
    lines.append("")
    lines.append("| Case | Focus | Why it matters | Primary analysis lens | Expected artifacts |")
    lines.append("| --- | --- | --- | --- | --- |")
    for case in payload["cases"]:
        lines.append(
            "| {title} | {focus} | {why} | {lens} | {artifacts} |".format(
                title=case["title"],
                focus=case["focus"],
                why=case["why_it_matters"],
                lens=_format_list(case["analysis_lens"]),
                artifacts=_format_list(case["expected_artifacts"]),
            )
        )
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- Use these cases as a fixed review spine for the article-hardening track.")
    lines.append("- Each case should be paired with at least one example instance, one mapping decision, and one evidence note.")
    lines.append(
        "- The set is intentionally broader than the current UOGTO core so that missing or adjacent concepts can be triaged before expansion."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    payload = _load()
    OUTPUT_PATH.write_text(build_markdown(payload), encoding="utf-8")


if __name__ == "__main__":
    main()
