import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PAPER = ROOT / "docs" / "paper" / "paper.tex"
DEFAULT_CSL = ROOT / "docs" / "paper" / "references.csl.json"

CITE_RE = re.compile(r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])*\{([^}]*)\}")
BIBITEM_RE = re.compile(r"\\bibitem\{([^}]*)\}")


def citation_keys(tex: str) -> list[str]:
    keys = []
    for match in CITE_RE.finditer(tex):
        keys.extend(key.strip() for key in match.group(1).split(",") if key.strip())
    return sorted(set(keys))


def bibitem_keys(tex: str) -> list[str]:
    return sorted(set(BIBITEM_RE.findall(tex)))


def csl_ids(path: Path) -> list[str]:
    records = json.loads(path.read_text(encoding="utf-8"))
    return sorted(record["id"] for record in records)


def check_citations(paper_path: Path = DEFAULT_PAPER, csl_path: Path = DEFAULT_CSL) -> dict:
    tex = paper_path.read_text(encoding="utf-8")
    citations = citation_keys(tex)
    bibitems = bibitem_keys(tex)
    references = csl_ids(csl_path)

    citation_set = set(citations)
    bibitem_set = set(bibitems)
    reference_set = set(references)
    return {
        "paper": str(paper_path),
        "csl": str(csl_path),
        "citation_count": len(citations),
        "bibitem_count": len(bibitems),
        "reference_count": len(references),
        "missing_from_csl": sorted(citation_set - reference_set),
        "missing_bibitems": sorted(citation_set - bibitem_set),
        "uncited_csl_references": sorted(reference_set - citation_set),
        "uncited_bibitems": sorted(bibitem_set - citation_set),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Check manuscript LaTeX citations against CSL.")
    parser.add_argument("--paper", default=str(DEFAULT_PAPER))
    parser.add_argument("--csl", default=str(DEFAULT_CSL))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = check_citations(Path(args.paper), Path(args.csl))
    ok = not (
        result["missing_from_csl"]
        or result["missing_bibitems"]
        or result["uncited_csl_references"]
        or result["uncited_bibitems"]
    )
    if args.json:
        print(json.dumps({"ok": ok, **result}, indent=2))
    else:
        print(
            "Manuscript citation check "
            f"{'passed' if ok else 'failed'}: "
            f"{result['citation_count']} citations, "
            f"{result['bibitem_count']} bibitems, "
            f"{result['reference_count']} CSL references."
        )
        for key in [
            "missing_from_csl",
            "missing_bibitems",
            "uncited_csl_references",
            "uncited_bibitems",
        ]:
            if result[key]:
                print(f"{key}: {', '.join(result[key])}")
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
