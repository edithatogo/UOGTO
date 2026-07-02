import argparse
import json
import re
import shutil
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PAPER = ROOT / "docs" / "paper" / "paper.tex"
DEFAULT_OUTDIR = ROOT / ".tmp" / "manuscript-build"
ARXIV_COMPATIBLE_ENGINES = {"latexmk", "pdflatex"}

REQUIRED_TOKENS = (
    r"\documentclass",
    r"\begin{document}",
    r"\end{document}",
    r"\maketitle",
    r"\begin{thebibliography}",
    r"\end{thebibliography}",
)
BLOCKING_WARNING_PATTERNS = (
    re.compile(r"LaTeX Warning:.*Reference `[^`]+'.*undefined", re.IGNORECASE),
    re.compile(r"LaTeX Warning:.*Citation `[^`]+'.*undefined", re.IGNORECASE),
    re.compile(r"There were undefined references", re.IGNORECASE),
    re.compile(r"There were undefined citations", re.IGNORECASE),
)


def bundled_tectonic_candidates() -> Iterable[Path]:
    suffix = ".exe" if sys.platform == "win32" else ""
    yield ROOT / ".pixi" / "envs" / "default" / "Library" / "bin" / f"tectonic{suffix}"
    yield ROOT / ".pixi" / "envs" / "default" / "Scripts" / f"tectonic{suffix}"
    yield ROOT / ".pixi" / "envs" / "default" / "bin" / f"tectonic{suffix}"
    plugin_root = Path.home() / ".codex" / "plugins" / "cache" / "openai-bundled" / "latex"
    if plugin_root.exists():
        yield from sorted(plugin_root.glob(f"*/bin/tectonic{suffix}"))


def check_tex_structure(paper_path: Path) -> list[str]:
    tex = paper_path.read_text(encoding="utf-8")
    issues = [f"missing required token: {token}" for token in REQUIRED_TOKENS if token not in tex]
    if tex.find(r"\begin{document}") > tex.find(r"\end{document}"):
        issues.append(r"\begin{document} appears after \end{document}")
    if tex.count(r"\begin{thebibliography}") != tex.count(r"\end{thebibliography}"):
        issues.append("thebibliography environment is not balanced")
    return issues


def blocking_build_warnings(log_text: str) -> list[str]:
    warnings: list[str] = []
    for pattern in BLOCKING_WARNING_PATTERNS:
        warnings.extend(match.group(0) for match in pattern.finditer(log_text))
    return sorted(set(warnings))


def find_latex_engine() -> str | None:
    for engine in ("latexmk", "tectonic", "pdflatex"):
        found = shutil.which(engine)
        if found:
            return found
    for candidate in bundled_tectonic_candidates():
        if candidate.exists():
            return str(candidate)
    return None


def engine_basename(engine: str) -> str:
    name = re.split(r"[\\/]", engine)[-1].lower()
    return name[:-4] if name.endswith(".exe") else name


def is_arxiv_compatible_engine(engine: str) -> bool:
    return engine_basename(engine) in ARXIV_COMPATIBLE_ENGINES


def command_for_engine(engine: str, paper_path: Path, output_dir: Path) -> list[str]:
    executable = str(engine)
    engine_name = engine_basename(engine)
    if engine_name == "latexmk":
        return [
            executable,
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={output_dir}",
            str(paper_path),
        ]
    if engine_name == "tectonic":
        return [executable, "--outdir", str(output_dir), str(paper_path)]
    if engine_name == "pdflatex":
        return [
            executable,
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
    require_arxiv_engine: bool = False,
) -> dict:
    paper_path = paper_path.resolve()
    output_dir = output_dir.resolve()
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

    if require_arxiv_engine and not is_arxiv_compatible_engine(engine):
        result["ok"] = False
        result["skipped"] = (
            "arXiv-compatible PDF engine required; found "
            f"{engine_basename(engine)}. Install latexmk or pdflatex for strict arXiv preflight."
        )
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
    log_path = output_dir / f"{paper_path.stem}.log"
    warning_text = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else completed.stdout + "\n" + completed.stderr
    result["returncode"] = completed.returncode
    result["stdout_tail"] = completed.stdout[-2000:]
    result["stderr_tail"] = completed.stderr[-2000:]
    result["blocking_warnings"] = blocking_build_warnings(warning_text)
    result["compiled"] = completed.returncode == 0
    result["pdf"] = str(pdf_path)
    result["ok"] = completed.returncode == 0 and pdf_path.exists() and not result["blocking_warnings"]
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check and optionally compile the UOGTO manuscript PDF.")
    parser.add_argument("--paper", default=str(DEFAULT_PAPER))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTDIR))
    parser.add_argument("--require-pdf", action="store_true")
    parser.add_argument("--require-arxiv-engine", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = build_manuscript(
        Path(args.paper),
        Path(args.output_dir),
        require_pdf=args.require_pdf,
        require_arxiv_engine=args.require_arxiv_engine,
    )
    if args.json:
        print(json.dumps(result, indent=2))
    elif result["structure_issues"]:
        print("Manuscript build check failed:")
        for issue in result["structure_issues"]:
            print(f"- {issue}")
    elif result["compiled"]:
        print(f"Manuscript PDF built with {result['engine']}: {result['pdf']}")
        if result.get("blocking_warnings"):
            print("Blocking LaTeX warnings detected:")
            for warning in result["blocking_warnings"]:
                print(f"- {warning}")
    elif result["ok"]:
        print(result["skipped"])
        print("Manuscript TeX structure check passed.")
    else:
        if result.get("skipped"):
            print(result["skipped"])
        print("Manuscript PDF build failed.")
        if result.get("stdout_tail"):
            print(result["stdout_tail"])
        if result.get("stderr_tail"):
            print(result["stderr_tail"])
    if not result["ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
