# Conductor Status

Updated: `2026-07-02`

## Active Work

- `uogto_nature_presubmission_evaluation_20260625`: Active. arXiv upload-ready hardening is implemented and verified with deterministic packaging, privacy-audit enforcement, checksums, `00README.json` preview, strict CI arXiv-engine gating, 90-day artifact retention, checksum-bound GitHub artifact attestation, and a clean tracked-tree upload manifest.

## Current arXiv Submission State

- Pre-submission automation is in place.
- `make arxiv-upload-ready` is the current local gate for creating the upload candidate under `dist/arxiv/`.
- Local package/audit/upload-ready generation passed on 2026-07-02; the local upload tarball SHA-256 is `21d82a1da3f1b78d71433fd9ee316602e4962d18d4b5ab511d57cd84f34fa385`.
- GitHub Actions manual arXiv Preflight must pass on the current branch head before upload, including strict arXiv-engine preflight, upload-ready artifact generation, artifact upload, and provenance attestation.
- The CI upload artifact tarball SHA-256 must match the `SHA256SUMS` and `arxiv-submission-manifest.json` entries from the latest successful current-branch run.
- The CI upload manifest reports `dirty: false`, `dirty_file_count: 0`, `dirty_entries: []`, and `dirty_mode: tracked-files-only`.
- Local attestation verification against the downloaded CI tarball must exit successfully before upload.
- Pull request checks for PR #19 must pass on the current branch head: `arxiv-preflight`, `manuscript-pdf`, and `validate`.
- Full local `make arxiv-upload-ready` passed on 2026-07-02 using `.pixi/envs/default/python.exe`, bundled Tectonic, and locally installed SourceRight `0.1.20`.
- Strict local `make arxiv-preflight-strict` failed as designed because this workstation resolves bundled Tectonic, not `latexmk`/`pdflatex`; GitHub Actions is configured to run the strict arXiv-engine path.
- Live Codex subagents reviewed the manuscript/process: Hooke (`019f20ab-621a-70a3-9436-75b2744190bd`), Locke (`019f20ab-9dd4-7e02-8556-03e3665876b7`), and Franklin (`019f20ab-cbc4-7961-86f5-25c1753acaaf`).
- Corresponding arXiv red-team and devil's advocate agents are now explicit and archived:
  - Red team: Wegener (`019f20ca-bbe7-7e93-831b-b906d7c50f63`), archived at `docs/paper/reviews/arxiv-red-team-review-2026-07-02.md`.
  - Devil's advocate: Faraday (`019f20c7-9208-7702-af6b-36d441a50041`), archived at `docs/paper/reviews/arxiv-devils-advocate-review-2026-07-02.md`.
- Current devil's advocate recommendation: `pass-for-arxiv-upload`; clean strict-engine CI, remote attestation, and clean-tree manifest are complete. ArXiv-rendered PDF inspection remains a post-upload external submission step.
- `make validate` passed on 2026-07-02.
- `make test` passed on 2026-07-02: `207 passed, 21 warnings`.
- Preprint glossary and abbreviations were added at the end of `docs/paper/paper.tex`, with in-text hyperlinks to glossary/abbreviation anchors.
- Authentext-style prose cleanup has been applied to the manuscript/supplement, and `edithatogo/authentext` is installed globally at `C:\Users\60217257\.codex\skills\authentext` pending Codex restart.
- SourceRight is installed from `edithatogo/sourceright` at upstream commit `f0c2c7c5dc9c2a25724e11985eb2b906d34c7c17`; `make manuscript-sourcecheck` passes with matched manuscript citations and 0 citation reconciliation issues.
- Academic review workflows from `edithatogo/academic-research-skills` are installed globally (`academic-paper`, `academic-paper-reviewer`, `academic-pipeline`, `deep-research`) from inspected commit `734dd23e03e7261db9204702be9221119a30d7d2`; a Codex restart is required before future sessions list them automatically.
- Academic-research-skills agents reviewed the arXiv package: Bernoulli (`019f216a-c005-7dd0-b102-cb8663db4724`) as integrity verifier, Godel (`019f216a-f974-7720-9349-fdc3d97955e8`) as methods reviewer, Ampere (`019f2170-08bf-7641-9560-8a2900e66d1c`) as ontology/game-theory domain reviewer, and Raman (`019f2170-3dc4-79e2-a458-014e2949fdee`) as devil's advocate/perspective reviewer.
- Their review synthesis is archived at `docs/paper/reviews/academic-research-skills-arxiv-review-2026-07-02.md`; applied fixes include narrower universal/readiness claims, foundational game-theory and ontology-engineering references, an evidence-strength table, enriched first-price auction JSON-LD, concrete missing-element disposition labels, OpenSpiel DOI metadata correction, and exploratory graph/network wording.
- Current `make manuscript-sourcecheck` now passes with 19/19 manuscript citations matched and 0 citation reconciliation issues; SourceRight still reports 10 non-blocking missing-DOI warnings for web/spec/API/book/arXiv-style references.
- Figure 1 is now native TikZ rather than a PDF figure asset, with additional manuscript/appendix visual summaries for the economics-module roadmap, comparative mapping flow, and network analysis.
- Cosmograph graph/network visualisation now includes rendered source-similarity, term-alignment, and import/evidence-use images under `docs/ontology-comparison/cosmograph/`, PDF copies in the arXiv appendix as Figures A3 to A5, and a repository review surface at `docs/article-hardening/network-graph-visualisation-supplement.md`.
- LaTeX visual presentation scoring is tracked at `docs/paper/latex-visual-presentation-scorecard.md` and `.json`; current target state is all major sections at least 95/100 with a weighted total score of 96.5/100.
- Candidate decision audit is tracked at `docs/article-hardening/candidate-decision-ledger.md`, `.csv`, and `.json`; the current ledger covers 511 route, source, mapping, and ontology-inclusion candidate decisions with rationales and heuristics.
- Manual arXiv upload using the CI artifact, rendered-PDF inspection, and arXiv identifier recording remain external submission steps.
