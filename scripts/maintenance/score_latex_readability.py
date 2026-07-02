import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PAPER = ROOT / "docs" / "paper" / "paper.tex"
DEFAULT_JSON = ROOT / "docs" / "paper" / "readability-report.json"
DEFAULT_MD = ROOT / "docs" / "paper" / "readability-report.md"


def main_prose(tex: str) -> str:
    """Score the article body, not references, appendices, or generated lists."""
    body = tex.split("\\begin{document}", 1)[-1]
    return body.split("\\appendix", 1)[0]


def latex_to_text(tex: str) -> str:
    tex = re.sub(r"%.*", " ", tex)
    tex = re.sub(r"\\begin\{thebibliography\}.*?\\end\{thebibliography\}", " ", tex, flags=re.S)
    tex = re.sub(r"\\begin\{(tikzpicture|tabular|longtable)\}.*?\\end\{\1\}", " ", tex, flags=re.S)
    tex = re.sub(r"\\(caption|title|author|date|section|subsection|item)\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r" \2. ", tex)
    tex = re.sub(r"\\(glslink|abblink|href)\{[^{}]*\}\{([^{}]*)\}", r" \2 ", tex)
    tex = re.sub(r"\\(cite|ref|label|path|url)\{[^{}]*\}", " ", tex)
    tex = re.sub(r"\\(texttt|emph|textbf)\{([^{}]*)\}", r" \2 ", tex)
    tex = re.sub(r"\\[a-zA-Z]+[*]?(?:\[[^\]]*\])?(?:\{[^{}]*\})?", " ", tex)
    tex = re.sub(r"[{}_$^&~#]", " ", tex)
    tex = re.sub(r"[^A-Za-z0-9.,;:!?()'\"/\- ]+", " ", tex)
    tex = re.sub(r"\s+", " ", tex)
    return tex.strip()


def score_text(text: str) -> dict:
    try:
        import textstat
    except ImportError as exc:
        raise SystemExit("textstat is required. Install it with `python -m pip install textstat`.") from exc
    return {
        "character_count": len(text),
        "word_count": textstat.lexicon_count(text, removepunct=True),
        "sentence_count": textstat.sentence_count(text),
        "flesch_reading_ease": round(textstat.flesch_reading_ease(text), 2),
        "flesch_kincaid_grade": round(textstat.flesch_kincaid_grade(text), 2),
        "gunning_fog": round(textstat.gunning_fog(text), 2),
        "smog_index": round(textstat.smog_index(text), 2),
        "dale_chall": round(textstat.dale_chall_readability_score(text), 2),
        "target_reader": "14-year-old reader, roughly US grade 8-9",
        "target_status": "pass" if textstat.flesch_kincaid_grade(text) <= 9.0 else "needs_revision",
    }


def build_report(paper: Path = DEFAULT_PAPER) -> dict:
    raw_tex = paper.read_text(encoding="utf-8")
    text = latex_to_text(main_prose(raw_tex))
    scores = score_text(text)
    return {
        "schema": "uogto.paper-readability-report.v1",
        "paper": str(paper.relative_to(ROOT)),
        "scoring_tool": "textstat",
        "scope": "main manuscript prose before appendix, bibliography, glossary, and abbreviations",
        "generated_at_utc": "deterministic-local-preflight",
        "scores": scores,
        "plain_text_excerpt": text[:1000],
    }


def write_outputs(report: dict, json_path: Path = DEFAULT_JSON, md_path: Path = DEFAULT_MD) -> None:
    json_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    scores = report["scores"]
    lines = [
        "# Manuscript readability report",
        "",
        "Tool: `textstat`",
        "",
        f"Scope: {report['scope']}",
        "",
        f"Target reader: {scores['target_reader']}",
        "",
        "| Metric | Score |",
        "| --- | ---: |",
        f"| Word count | {scores['word_count']} |",
        f"| Sentence count | {scores['sentence_count']} |",
        f"| Flesch reading ease | {scores['flesch_reading_ease']} |",
        f"| Flesch-Kincaid grade | {scores['flesch_kincaid_grade']} |",
        f"| Gunning fog | {scores['gunning_fog']} |",
        f"| SMOG index | {scores['smog_index']} |",
        f"| Dale-Chall score | {scores['dale_chall']} |",
        "",
        f"Target status: **{scores['target_status']}**.",
        "",
        "Interpretation: the paper can still contain technical terms, but the surrounding prose should explain those terms with short sentences and concrete examples.",
    ]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Score the UOGTO LaTeX paper readability with textstat.")
    parser.add_argument("--paper", type=Path, default=DEFAULT_PAPER)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = build_report(args.paper)
    if args.write:
        write_outputs(report, args.json, args.md)
    print(json.dumps(report["scores"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
