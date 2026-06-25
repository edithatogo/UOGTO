# arXiv Toolchain Review

## Role

Evaluate libraries and command-line tools that can prepare, harden, and evaluate the arXiv submission package for UOGTO without weakening the repo-native source package policy.

## Required Checks

- Treat `scripts/maintenance/build_arxiv_source_package.py`, `scripts/maintenance/clean_arxiv_source_package.py`, `make arxiv-source-package`, `make arxiv-source-clean`, and `make arxiv-preflight` as the baseline.
- Benchmark `arxiv-latex-cleaner` only in an isolated output directory and compare its kept/removed files with the repo-native manifest.
- Use `latexmk` as the preferred arXiv-compatible build verifier when a TeX engine is available.
- Review `chktex`, `lacheck`, `checkcites`, `latexpand`, `texfot`, `texloganalyser`, and optional `tectonic` for practical value, false-positive risk, Windows viability, and CI viability.
- Confirm package contents, filenames, figure formats, bibliography files, TeX Live 2023/2025 compatibility, and generated-PDF review requirements.
- Audit source package privacy risks: comments, hidden files, private notes, referee material, unused figures, logs, aux files, embedded metadata, credentials, and private URLs.

## Findings

Pending.

## Required Output

- arXiv toolchain score out of 100.
- Completed `arxiv_toolchain_matrix.csv` dispositions with evidence.
- Completed `arxiv_acceptance_checklist.md`.
- Recommendation on whether any external tool should become required, optional, advisory, or rejected.
- Exact blockers for missing local tools or CI support.
