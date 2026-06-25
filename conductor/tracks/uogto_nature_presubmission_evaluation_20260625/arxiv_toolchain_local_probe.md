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

## 2026-06-25 CI Verification Update
- Commit 018a2a4 installs SourceRight in CI with cargo install --git https://github.com/edithatogo/sourceright.git sourceright --locked.
- Local gates passed after the CI fixes: focused arXiv workflow/source-package tests, affected ontology-visual tests, affected article-hardening tests, make validate, and full pytest with 189 tests.
- Remote GitHub Actions passed on 018a2a4: Validate UOGTO run 28145232100, Build WIDOCO Pages run 28145232082, and arXiv Preflight run 28145232079.
- This remote pass supersedes the earlier local-only PDF blocker for the CI submission gate. The local workstation still lacks latexmk, pdflatex, and optional TeX audit tools, so local external-tool benchmarking remains advisory until those tools are installed or run in isolated CI jobs.

 
## 2026-06-25 Blocker Reclassification 
- Supersedes earlier local-tool blocker notes in this track. Remote arXiv Preflight run 28145232079 passed on commit 018a2a4, so missing local TeX and arxiv_latex_cleaner tools are optional advisory benchmarking gaps only. 
- Disposition: CI-proven arXiv gate is complete; local external-tool benchmarking remains useful but is not a submission blocker. 
- Next local hardening step: install TeX Live or MiKTeX plus arxiv-latex-cleaner in an isolated environment and compare manifests without replacing the repo-native cleaner.
