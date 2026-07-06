# arXiv Toolchain Matrix

This matrix records candidate tools for preparing, hardening, and evaluating arXiv submissions. The repo-native cleaner remains authoritative unless an external tool proves stricter without destructive side effects.

| Tool | Purpose | Disposition | Acceptance Criterion |
| --- | --- | --- | --- |
| repo-native-cleaner | Authoritative UOGTO source-package cleaner | Required | Manifest proves only required TeX, bibliography, style, and figure files are retained. |
| repo-native-upload-ready-bundler | Deterministic arXiv upload tarball, manifest, checksums, `00README.json` preview, and provenance handoff | Required | `make arxiv-upload-ready` emits `dist/arxiv/*`, records SHA-256 hashes, and CI retains the artifact set for 90 days plus attests `dist/arxiv/SHA256SUMS`. |
| arxiv-latex-cleaner | External cleaner for unused TeX/images, comments, and size reduction | Advisory benchmark | Run in isolated output and compare removed/kept manifest with repo-native cleaner. |
| latexmk / pdflatex | Automated LaTeX/BibTeX build verifier | Required for final publisher sign-off | `make arxiv-upload-ready-strict` or GitHub arXiv Preflight compiles with an arXiv-compatible processor; missing local engine is recorded as a local-toolchain blocker. |
| chktex | LaTeX linting | Optional with triage | Warnings are reviewed and fixed or marked false positive. |
| lacheck | Common LaTeX mistake checker | Optional with triage | Warnings are reviewed and fixed or marked false positive. |
| checkcites | Undefined and unused citation checker | Optional | Citation issues are fixed or explicitly justified. |
| latexpand | Flatten source for audit | Optional audit | Expanded source audit finds no hidden included material or records blocker. |
| texfot | Filter noisy TeX output | Optional | Build logs expose actionable warnings/errors without hiding failures. |
| texloganalyser | Extract TeX log warnings/errors | Optional | Log analysis report records unresolved warnings and errors. |
| tectonic | Secondary reproducible build check | Secondary only | Result is recorded separately and never substitutes for latexmk/arXiv-compatible build. |

## Required Review Outcome

The `arxiv-toolchain-reviewer` must classify every candidate as `required`, `required-when-available`, `optional`, `optional-with-triage`, `advisory-benchmark`, `secondary-only`, or `rejected`, with evidence from isolated runs or documented unavailability.
