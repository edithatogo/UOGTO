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


## 2026-06-25 Executed Review
- Scores: arXiv toolchain hardening 86 source leak privacy audit 78; CI run 28145232079 passed but add an explicit privacy audit manifest for comments hidden files private notes unused figures logs aux files and metadata.


## Source-Leak/Privacy Audit Manifest

Status: implemented and locally passing as of `2026-06-25T07:36:31+00:00`.

Evidence:
- `docs/paper/arxiv-source-privacy-audit.json`
- `docs/paper/arxiv-source-privacy-audit.md`
- `scripts/maintenance/audit_arxiv_source_privacy.py`
- `tests/test_arxiv_privacy_audit.py`
- `Makefile` target `arxiv-privacy-audit`

The audit covers comments and disabled/draft blocks, hidden files, private notes/referee material, unused figures, aux/log/output files, embedded PDF/image metadata, credentials, and private URLs/local paths. Local missing optional tools remain advisory; this manifest is repo-native and can run in CI.
