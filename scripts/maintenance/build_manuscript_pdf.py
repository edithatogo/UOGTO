import argparse
import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PAPER = ROOT / "docs" / "paper" / "paper.tex"
DEFAULT_OUTDIR = ROOT / ".tmp" / "manuscript-build"

REQUIRED_TOKENS = (
    r"\documentclass",
    r"\begin{document}",
    r"\end{document}",
    r"\maketitle",
    r"\begin{thebibliography}",
    r"\end{thebibliography}",
)


def check_tex_structure(paper_path: Path) -> list[str]:
    tex = paper_path.read_text(encoding="utf-8")
    issues = [f"missing required token: {token}" for token in REQUIRED_TOKENS if token not in tex]
    if tex.find(r"\begin{document}") > tex.find(r"\end{document}"):
        issues.append(r"\begin{document} appears after \end{document}")
    if tex.count(r"\begin{thebibliography}") != tex.count(r"\end{thebibliography}"):
        issues.append("thebibliography environment is not balanced")
    return issues


def find_latex_engine() -> str | None:
    for engine in ("latexmk", "tectonic", "pdflatex"):
        if shutil.which(engine):
            return engine
    return None


def command_for_engine(engine: str, paper_path: Path, output_dir: Path) -> list[str]:
    if engine == "latexmk":
        return [
            engine,
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={output_dir}",
            str(paper_path),
        ]
    if engine == "tectonic":
        return [engine, "--outdir", str(output_dir), str(paper_path)]
    if engine == "pdflatex":
        return [
            engine,
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={output_dir}",
            str(paper_path),
        ]
    raise ValueError(f"Unsupported LaTeX engine: {engine}")


def build_manuscript(
    paper_path: Path = DEFAULT_PAPER,
    output_dir: Path = DEFAULT_OUTDIR,
    require_pdf: bool = False,
) -> dict:
    structure_issues = check_tex_structure(paper_path)
    result = {
        "paper": str(paper_path),
        "output_dir": str(output_dir),
        "structure_issues": structure_issues,
        "engine": None,
        "compiled": False,
        "pdf": None,
        "returncode": None,
    }
    if structure_issues:
        result["ok"] = False
        return result

    engine = find_latex_engine()
    result["engine"] = engine
    if engine is None:
        result["ok"] = not require_pdf
        result["skipped"] = "No LaTeX engine found; install latexmk, tectonic, or pdflatex for PDF output."
        return result

    output_dir.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        command_for_engine(engine, paper_path, output_dir),
        cwd=paper_path.parent,
        check=False,
        capture_output=True,
        text=True,
    )
    pdf_path = output_dir / f"{paper_path.stem}.pdf"
    result["returncode"] = completed.returncode
    result["stdout_tail"] = completed.stdout[-2000:]
    result["stderr_tail"] = completed.stderr[-2000:]
    result["compiled"] = completed.returncode == 0
    result["pdf"] = str(pdf_path)
    result["ok"] = completed.returncode == 0 and pdf_path.exists()
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check and optionally compile the UOGTO manuscript PDF.")
    parser.add_argument("--paper", default=str(DEFAULT_PAPER))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTDIR))
    parser.add_argument("--require-pdf", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_manuscript(Path(args.paper), Path(args.output_dir), args.require_pdf)
    if args.json:
        print(json.dumps(result, indent=2))
    elif result["structure_issues"]:
        print("Manuscript build check failed:")
        for issue in result["structure_issues"]:
            print(f"- {issue}")
    elif result["compiled"]:
        print(f"Manuscript PDF built with {result['engine']}: {result['pdf']}")
    elif result["ok"]:
        print(result["skipped"])
        print("Manuscript TeX structure check passed.")
    else:
        print("Manuscript PDF build failed.")
        if result.get("stdout_tail"):
            print(result["stdout_tail"])
        if result.get("stderr_tail"):
            print(result["stderr_tail"])
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
