# Implementation Plan: Manuscript Submission Revision and Venue Strategy

## Phase 1: External arXiv Closeout

- [x] Task: Record arXiv submission state
    - [x] Created `docs/paper/arxiv-submission-state.md` to record that the current external state is `not_submitted`.
    - [x] Kept the CI upload artifact as the binding submission candidate and documented that final hashes must come from the successful clean arXiv Preflight artifact.
    - [x] Recorded that arXiv-rendered PDF inspection is blocked until external registered-author upload.
    - [x] Recorded arXiv identifier, version, manifest SHA, and approval state as pending external fields rather than fabricated local evidence.

## Phase 2: Presubmission Review Backlog

- [x] Task: Synthesize manuscript findings
    - [x] Re-read presubmission decision memo, recommendations, review matrix, arXiv contract, arXiv process, and July 2 reviewer findings.
    - [x] Created `docs/paper/submission-revision-decision-memo.md` with the arXiv-first path, Nature Human Behaviour Resource route, MDM alternative route, and non-goals.
    - [x] Created `docs/paper/submission-revision-backlog.csv` with must-fix, should-fix, stretch, and watch classifications.
    - [x] Added acceptance criteria for arXiv external closeout, clean CI provenance, manuscript claims, journal-route selection, supplement alignment, cover package, behavioural example depth, and review-evidence discipline.

## Phase 3: Revision and Verification

- [x] Task: Implement accepted revision items
    - [x] Updated manuscript resource framing, journal-version caution, and arXiv state wording in `docs/paper/paper.tex`.
    - [x] Updated supplement, arXiv process, arXiv contract, and Nature must-fix status docs to distinguish repo-local readiness from external upload/rendered-PDF approval.
    - [x] Added regression tests for the submission decision memo, backlog, and arXiv state record.
    - [x] Rebuilt manuscript sources and PDF via `make manuscript-sourcecheck`.
    - [x] Regenerated figure/caption freeze manifest via `make figure-caption-freeze`.
    - [x] Verified local arXiv upload-ready packaging via `make arxiv-upload-ready`; local dirty-tree manifest remains non-final by design.
    - [x] Ran focused manuscript/arXiv tests: `19 passed`.
    - [x] Ran `make validate`: passed.
    - [x] Ran `make test`: `251 passed, 52 warnings`.

## Phase 4: Review Fixes

- [x] Task: Apply Conductor review fixes
    - [x] Reconciled arXiv contract CI/attestation status rows with the external-state file so the docs require clean CI evidence without claiming it already exists before PR/selected upload artifact verification.
    - [x] Updated regression tests for the stricter status wording.
