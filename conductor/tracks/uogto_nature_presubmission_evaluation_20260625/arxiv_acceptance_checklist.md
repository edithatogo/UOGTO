# arXiv Acceptance Checklist

This checklist is aligned to current arXiv TeX submission constraints and the repo-native source package cleaner.

## Package Contents

- [ ] No auxiliary, log, build, output, or cache files are included unless arXiv explicitly requires them.
- [ ] No referee letters, journal templates, private notes, hidden files, backup files, or unrelated source files are included.
- [ ] Every retained image or asset is referenced by the manuscript or explicitly justified.
- [ ] The source package manifest records kept and removed files with reasons.

## Filenames and References

- [ ] Filenames use only arXiv-safe characters: `a-z A-Z 0-9 _ + - . , =`.
- [ ] Case-sensitive TeX references match actual filenames exactly.
- [ ] Main TeX file and any included files are discoverable from the submission root.

## Figures

- [ ] PDFLaTeX submissions include only PDF, PNG, JPG/JPEG, or other accepted PDFLaTeX-compatible figure formats.
- [ ] No on-the-fly figure conversion is required during arXiv processing.
- [ ] Converted figures have been manually inspected for scientific correctness.
- [ ] No embedded JavaScript, animations, or active content is present in PDFs.

## Bibliography

- [ ] If BibTeX/Biber is used, every required `.bib` file is present or a matching `.bbl` is included.
- [ ] `.bbl` file name matches the main `.tex` file if `.bbl` is used.
- [ ] Citation extraction is tested with repo-native manuscript checks and optional `checkcites`.
- [ ] arXiv identifiers and DOI metadata are written in extraction-friendly form where relevant.

## Build Verification

- [ ] `make arxiv-source-package` succeeds.
- [ ] `make arxiv-source-clean` succeeds.
- [ ] `make arxiv-preflight` succeeds or records an exact missing-tool blocker.
- [ ] `latexmk` compiles the cleaned package with an arXiv-compatible processor where available.
- [ ] TeX Live 2023/2025 compatibility risks are recorded, including package-version risks.
- [ ] Generated PDF is visually checked before submission.

## Privacy and Source-Leak Audit

- [ ] LaTeX comments, disabled blocks, and draft macros do not disclose private notes or reviewer-facing concerns.
- [ ] No credentials, tokens, private URLs, local paths, account identifiers, or internal correspondence are present.
- [ ] PDF/image metadata is checked for private authoring or location data.
- [ ] External cleaner output is compared with the repo-native cleaner before changing policy.


## 2026-06-25 Tool Blocker Reclassification
- Remote arXiv Preflight run 28145232079 passed on commit 018a2a4, so missing local TeX and arxiv_latex_cleaner tools are no longer submission-gate blockers.
- Local latexmk and arxiv_latex_cleaner checks remain optional advisory benchmarks for developer convenience and additional assurance only.
- The authoritative gate remains the repo-native cleaner plus CI arXiv Preflight unless a future isolated benchmark proves stricter behavior without destructive side effects.


## Source-Leak/Privacy Audit Manifest

Status: complete as of `2026-06-25T07:36:31+00:00`.

Evidence surfaces:
- `docs/paper/arxiv-source-privacy-audit.json`: machine-readable manifest covering comments, hidden files, private notes/referee material, unused figures, aux/log/output files, embedded metadata, credentials, and private URLs/local paths.
- `docs/paper/arxiv-source-privacy-audit.md`: reviewer-readable summary of the same audit.

Policy: the repository-native arXiv source cleaner remains authoritative; external arXiv tooling is advisory unless benchmarked in an isolated output directory. The privacy audit is now part of the local `arxiv-privacy-audit` target and is invoked by `arxiv-preflight` after source package generation/cleaning.


### CI Evidence for Privacy Audit Manifest

Commit `a2ee99d` passed the relevant GitHub Actions on 2026-06-25 UTC: Validate UOGTO 28154901094; arXiv Preflight 28154901098; Build WIDOCO Pages 28154901113; Build Manuscript PDF 28154901116. The privacy audit manifest is therefore both locally generated and remotely preflighted.
