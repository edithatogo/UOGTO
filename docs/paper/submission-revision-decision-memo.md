# Submission Revision Decision Memo

Updated: `2026-07-05`

## Decision

The current manuscript path is:

1. Complete the arXiv preprint path first, using the current repository source
   package and strict arXiv-engine CI as the binding upload evidence.
2. After an arXiv identifier is assigned and the arXiv-rendered PDF is approved,
   prepare a journal-specific revision package.
3. Treat Nature Human Behaviour as the primary aspirational journal route only
   as a Resource-style submission. Do not pitch the current manuscript as a
   standard Article reporting a primary behavioural finding.
4. Keep Medical Decision Making / Medical Decision Making Policy & Practice as
   the strongest alternative if the paper is refitted into a tutorial,
   technical note, or methods explainer for decision-modelling readers.
5. Keep safety-systems venues as a later alternative only if the manuscript adds
   a concrete safety, resilience, or risk-governance case study.

## Source Checks Used

- arXiv official TeX guidance confirms that current arXiv processing offers
  TeX Live 2025 and 2023, with 2025 as the default:
  <https://info.arxiv.org/help/faq/texlive.html>
- arXiv official submission guidance remains the binding source for TeX upload
  constraints and rendered-PDF inspection:
  <https://info.arxiv.org/help/submit_tex.html>
- Nature Human Behaviour content types define a Resource as a large data set or
  tool of broad utility, interest, and significance:
  <https://www.nature.com/nathumbehav/content>
- Nature Human Behaviour submission guidance requires checking fit, content
  type, policies, publishing model, and presubmission-enquiry route before
  initial submission:
  <https://www.nature.com/nathumbehav/submission-guidelines>
- Medical Decision Making manuscript guidance lists tutorials and technical
  notes among accepted manuscript types:
  <https://www.journals.smdm.org/manuscript-types/>
- Medical Decision Making manuscript requirements emphasize clear, concise, and
  logically organized writing for a sophisticated general medical readership:
  <https://www.journals.smdm.org/manuscript-requirements/>

## Required Pre-Submission Fixes

| Priority | Area | Required action | Acceptance criterion |
| --- | --- | --- | --- |
| must-fix | arXiv external state | Upload the clean CI arXiv artifact, inspect the arXiv-rendered PDF, and record the assigned identifier. | `docs/paper/arxiv-submission-state.md` records identifier, version, rendered-PDF approval, CI run, manifest SHA-256, tarball SHA-256, and submitter/date. |
| must-fix | provenance | Use the latest successful clean-branch arXiv Preflight artifact as the upload source. | Manifest reports `dirty: false`, `dirty_file_count: 0`, and `dirty_entries: []`; GitHub artifact attestation verifies against `dist/arxiv/SHA256SUMS`. |
| must-fix | manuscript claims | Keep UOGTO framed as a reusable ontology/evidence resource, not a primary empirical behavioural finding or external peer-reviewed result. | `docs/paper/paper.tex` and supplement prose keep claim strength tied to validation, mapping, and repository evidence surfaces. |
| must-fix | journal route | Select article type before journal submission. | Decision memo and cover-letter outline choose Nature Human Behaviour Resource, MDM tutorial/technical note, or another named target with no mixed venue claims. |
| should-fix | supplement | Keep final supplement numbering, figure list, and claim map synchronized after any manuscript edit. | `make figure-caption-freeze`, `make manuscript-sourcecheck`, and citation checks pass after edits. |
| should-fix | cover package | Prepare a venue-specific cover letter and declarations packet after target selection. | Cover letter states audience fit, resource utility, limitations, data/code availability, ethics, conflicts, funding, author contribution, and AI/tool-use disclosure. |
| stretch | behavioural example | Add a fuller public-goods, collective-risk, bargaining, or AI-mediated-interaction example for Nature Human Behaviour revision. | Example separates game specification, instance, session/trace, incentives, outcomes, and evidence without claiming behavioural validation. |
| watch | domain validation | Do not treat internal agent review, mapping candidates, or metadata-only sources as independent peer review or domain-expert adjudication. | AI/tool-use disclosure remains explicit; mapping and source-evidence language stays conservative. |

## Backlog Binding

The machine-readable backlog is
`docs/paper/submission-revision-backlog.csv`. It is the current operating queue
for arXiv closeout and journal-revision work. Items marked `external_blocker`
cannot be closed by repository edits alone.

## Current State

- arXiv identifier: not assigned.
- arXiv version: not assigned.
- arXiv-rendered PDF: not inspected; requires external upload.
- Final upload manifest SHA-256: pending the successful clean CI arXiv
  Preflight artifact used for upload.
- Journal target: undecided until after arXiv closeout; primary recommended
  path is Nature Human Behaviour Resource, with MDM tutorial/technical note as
  the most coherent alternative.

## Non-Goals

- Do not submit to a journal on behalf of the author.
- Do not fabricate arXiv, publisher, reviewer, or acceptance evidence.
- Do not represent internal agent review as independent peer review.
