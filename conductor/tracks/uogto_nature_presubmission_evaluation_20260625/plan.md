# Nature-Ready Presubmission Evaluation and Improvement

## Objective

Create a professor-level, Nature-standard presubmission evaluation of UOGTO covering the repository, ontology, evaluation protocol, analyses, artefacts, manuscript, supplement, figures, and PowerPoint. The output must be decision-ready: it should identify whether UOGTO is submission-ready, what must change before submission, and how each improvement will be verified.

## Success Criteria

- Every major review surface has a scored finding in `review_matrix.csv` and `review_matrix.md`.
- Every manuscript, supplement, dashboard, and PowerPoint image has an entry in `image_scores.csv` and `image_scores.md`.
- Every image below 100/100 has a concrete improvement loop and re-score plan.
- Every recommendation has a priority, rationale, owner role, target artefact, and acceptance criterion.
- Reviewer findings exist for all specialist lanes.
- The final decision memo gives one of: `ready`, `ready after minor fixes`, `major revision before submission`, or `not yet submission-ready`.
- Repo validation gates are recorded before and after the review work.

## Phase 1: Track Setup and Evidence Inventory

1. Confirm current branch, clean/dirty status, and validation baseline.
2. Inventory repository surfaces:
   - GitHub documentation and setup.
   - Ontology modules, SHACL shapes, examples, competency queries, mappings, and governance metadata.
   - Evaluation protocol, analysis outputs, dashboards, source registers, RO-Crate, DuckDB, SSSOM, quality metrics, and review decisions.
   - Manuscript, supplement, bibliography, arXiv preflight artefacts, and release/citation material.
   - PowerPoint and all figure/image assets.
3. Populate initial rows in the review and image score matrices.
4. Record missing or inaccessible artefacts as blockers, not as silent omissions.

## Phase 2: Specialist Reviews

Run eight independent review lanes and write one report per lane under `reviewer_findings/`.

| Lane | Primary Question | Required Output |
| --- | --- | --- |
| `game-theory-professor` | Is the game-theoretic framing correct, novel, and defensible? | Must-fix conceptual issues, missing constructs, and overclaim risks. |
| `ontology-engineering-reviewer` | Does the ontology meet high-quality OWL/RDF/SHACL practice? | Modelling, annotation, reasoning, profile, governance, and mapping findings. |
| `simulation-methods-reviewer` | Are simulation, ABM, DES, SD, MARL, and executable trace claims methodologically sound? | Method coverage, executable semantics, trace/provenance gaps. |
| `FAIR-reproducibility-reviewer` | Can a reviewer reproduce, cite, reuse, and audit the work? | FAIR, RO-Crate, DuckDB, SSSOM, licence, provenance, and release findings. |
| `Nature-editorial-reviewer` | Is the manuscript framed for a Nature-level contribution? | Novelty, narrative, figure economy, abstract/title, methods, limitations, and claims discipline. |
| `statistics-and-network-analysis-reviewer` | Are quantitative analyses valid, sensitive, and interpretable? | Metrics, robustness checks, sensitivity analyses, uncertainty, and reporting findings. |
| `visual-communications-reviewer` | Are figures and slides publication-grade? | Per-image visual defects, redesign instructions, accessibility checks. |
| `red-team-devils-advocate-reviewer` | What would a hostile reviewer reject? | Likely objections, missing controls, inflated claims, and rebuttal requirements. |

## Phase 3: Scoring and Recommendation Synthesis

1. Score each review surface out of 100 using `protocol.md`.
2. Classify every finding as `must-fix`, `should-fix`, `stretch`, or `watch`.
3. Translate findings into `recommendations.md` with:
   - priority,
   - target artefact,
   - responsible reviewer lane,
   - rationale,
   - implementation guidance,
   - acceptance criterion.
4. Identify dependencies between recommendations so later implementation can be phased safely.

## Phase 4: Image Improvement Loop

For each image:

1. Locate source asset, generated output, caption, and manuscript/slide usage.
2. Score scientific accuracy, interpretability, visual design, reproducibility, accessibility, caption alignment, and Nature-readiness.
3. If score is below 100, create a concrete change list.
4. Re-render or regenerate during the implementation pass.
5. Re-score until the image reaches 100/100 or a blocker is recorded with the exact missing input or tooling problem.

## Phase 5: Decision Memo and Implementation Backlog

1. Write `presubmission_decision_memo.md`.
2. State the submission decision and top risks.
3. Separate must-fix issues from optional refinements.
4. Record whether the manuscript is Nature-ready, Nature-adjacent, or better suited to another venue.
5. Add the next implementation backlog with acceptance criteria.

## Verification

Run and record:

- `git status --short`
- `make validate`
- arXiv/source package preflight where available
- placeholder sweep for `TODO`, `FIXME`, `TBD`, `stub`, `placeholder`, and `NotImplementedError`

The track is complete only when every planned artefact exists, every matrix has been populated, and every blocker is explicit.
