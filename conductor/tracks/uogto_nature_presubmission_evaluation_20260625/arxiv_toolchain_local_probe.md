# arXiv Toolchain Local Probe

## 2026-06-25 Local Command Availability

| Tool | Probe | Result | Impact |
| --- | --- | --- | --- |
| latexmk | `where latexmk` | Not found | `make arxiv-preflight` cannot complete local PDF build. |
| pdflatex | `where pdflatex` | Not found | No local PDFLaTeX fallback for arXiv-compatible build. |
| tectonic | `where tectonic` | Not found | Secondary reproducible build check unavailable locally. |
| chktex | `where chktex` | Not found | Optional lint unavailable locally. |
| lacheck | `where lacheck` | Not found | Optional lint unavailable locally. |
| checkcites | `where checkcites` | Not found | Optional citation checker unavailable locally. |
| latexpand | `where latexpand` | Not found | Optional flattened-source audit unavailable locally. |
| texfot | `where texfot` | Not found | Optional TeX log filtering unavailable locally. |
| texloganalyser | `where texloganalyser` | Not found | Optional TeX log analyser unavailable locally. |
| arxiv_latex_cleaner | `where arxiv_latex_cleaner` | Not found | External cleaner benchmark not runnable locally until installed. |

## Gate Results

- `make arxiv-source-package`: passed; generated a cleaned UUID package with one retained file.
- `make arxiv-source-clean`: passed after the cleaner was hardened to resolve the latest generated UUID package from the default clean target.
- `make arxiv-preflight`: blocked after citation checks because no local LaTeX engine was found (`latexmk`, `tectonic`, or `pdflatex`).

## Required Follow-Up

Install a TeX Live/MiKTeX toolchain with `latexmk` or run the strict PDF/arXiv preflight in CI before marking arXiv PDF verification complete. External tools should be benchmarked only in isolated `.tmp` outputs.
