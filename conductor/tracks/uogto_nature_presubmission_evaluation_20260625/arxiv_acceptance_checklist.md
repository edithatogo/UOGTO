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
