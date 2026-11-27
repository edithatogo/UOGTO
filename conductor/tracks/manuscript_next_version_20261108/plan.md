# Plan — manuscript integration, planning delivered and implementation pending

Task prefix: **MNV**. The complete planning package is delivered in MNV.00;
MNV.01–12 are future implementation. No canonical manuscript or reference edits
are completed by this plan. Each leaf has one independently reviewable outcome
and at most five authored files, including normal `plan.md`/`metadata.json`
bookkeeping where required. Listed generated derivatives do not expand the
source-edit budget; enumerate/review them before generation. Split a leaf before
adding an independent behavior or exceeding its file budget. Do not replace
OCS/SGC/FRT task IDs or create duplicate acceptance systems.

## [x] MNV.00 — Deliver the next-version plan and manuscript-integration track

- Depends on: inspected existing paper/supplement, submission state/backlog,
  semantic reconciliation, quality snapshot, source audit and current owner tracks.
- Authored files (five): `docs/paper/next-version-plan-20261108.md`; this track's
  `index.md`, `spec.md`, `plan.md`, `metadata.json`.
- Outcome: C01–C12 corrections, RQs, source strata, scoped denominators, paired
  controls, held-out proposal, traceability and publication boundaries are planned.
- Acceptance evidence: inspected baseline and plan/source consistency; local JSON
  and Markdown-link checks recorded when run. Root owns integrated repository
  validation, registry and status synchronization. Future work stays pending.

## Phase A — freeze the question and establish claim provenance

### [ ] MNV.01 — Freeze the paper's evidence universes

- Depends on: MNV.00; reconciled semantic inputs. No provider dependency.
- Authored outputs (future, three):
  `docs/paper/revisions/20261108/snapshot-manifest.json`,
  `docs/paper/revisions/20261108/snapshot-policy.md`,
  `tests/test_manuscript_revision_snapshot.py`.
- Generated derivatives: a dated candidate evidence directory containing hashed
  quality, mappings, source/case manifests and environment/command receipts. Bind
  the actual creation date and final revision; the directory label is a plan ID,
  not proof the evaluation was run on 8 November.
- Acceptance: distinguish historical June/July, retained-corpus November reanalysis
  and new source charting. Account for the quality builder's fixed `created` date;
  request an owner fix or record the limitation rather than backdating execution.
  Preserve old inputs as addressable snapshots. Missing/pending is a valid status.
- Check: `python -m pytest tests/test_manuscript_revision_snapshot.py` is a
  **future target**; test changed/missing hash and mixed-snapshot rejection.
  Existing quality/alignment `--check-only` commands verify current inputs before
  copying. No zero-collected or missing test can pass.

### [ ] MNV.02 — Bind every retained claim to evidence and attribution

- Depends on: MNV.01; OCS.09–10 sourcing/lineage receipts for source claims.
- Authored outputs (future, three):
  `docs/paper/revisions/20261108/claim-evidence.csv`,
  `docs/paper/revisions/20261108/claim-evidence-schema.json`,
  `tests/test_manuscript_claim_evidence.py`.
- Acceptance: C01–C12 and each additional assertion bind section/claim ID, source
  locator/citation key, revision/hash, reviewer/evidence role, result denominator
  and table/figure. Source unavailable, unknown support and intentional exclusion
  are distinct. Derived/adapted material retains creator/license attribution.
- Check: `python -m pytest tests/test_manuscript_claim_evidence.py` is a **future
  target**. Reject nonexistent artifacts, orphaned quantitative claims, fabricated
  external review and counts copied from the wrong snapshot. Internal expert-style
  agent checking is not evidence of independent external adjudication.

### [ ] MNV.03 — Integrate verified bibliography metadata into the source builder

- Depends on: MNV.02; OCS.10 plus the companion bibliography/attribution artifacts.
- Authored files (three): `scripts/maintenance/build_manuscript_sources.py`,
  `tests/test_manuscript_sources.py`,
  `docs/paper/revisions/20261108/citation-metadata-audit.md` (future).
- Generated derivatives: CSL/source inventories, verification inputs, citation
  export and review queues under `docs/paper/` and `.sourceright/`, enumerated
  explicitly in the receipt. Do not hand-edit only the generated CSL.
- Acceptance: reverify titles, complete author lists, year, DOI/URL, versions and
  retrieval/licensing provenance for existing and new citations; correct misleading
  fixed retrieval dates for newly retrieved evidence. Report unresolved records.
  The source builder reproduces the intended citation set without erasing additions.
- Checks: existing `python -m pytest tests/test_manuscript_sources.py`; generate
  first with the builder's existing `--paper-dir` and `--sourceright-dir` options
  pointing into scratch, inspect, then deliberately regenerate canonical outputs.
  Full LaTeX key reconciliation waits for manuscript citation integration.

Phase A checkpoint: MNV.01–03 close only after the chosen corpus/snapshot and
claim/citation surfaces reconcile. OCS.09–12 remain independently owned; a
bounded source receipt can be integrated without closing their entire programme.

## Phase B — integrate current evidence into the existing resource paper

### [ ] MNV.04 — Replace broad source-discovery implications with an accounted corpus

- Depends on: MNV.02–03; OCS.02/09–12 acquired/charted or explicitly unavailable
  dispositions needed for the claims retained. No blanket completion dependency
  on every OCS leaf.
- Authored files (two): `docs/paper/paper.tex`,
  `docs/paper/supplement-package.md`.
- Acceptance: update Introduction and source-discovery Methods/Results/S1–S2;
  cite GTO precedence with original-source availability qualified; stratify strategic
  ontologies, videogame vocabularies, languages, libraries and supporting standards.
  Deduplicate register unions and preserve acquisition/charting/execution states.
  The old negative search becomes a dated, limited observation.
- Checks: existing `make manuscript-check`; ledger review verifies primary-source
  support and candidate/source denominators. No “all ontologies found” claim.

### [ ] MNV.05 — Integrate quality measures with explicit denominator definitions

- Depends on: MNV.01–02; existing current quality receipt and any owner-delivered
  denominator/provenance improvements. Do not take over repository-maturity code.
- Authored files (three): `docs/paper/paper.tex`,
  `docs/paper/supplement-package.md`,
  `docs/paper/revisions/20261108/metric-definitions.md` (future).
- Generated derivatives: frozen per-module tables from the stated source universe.
- Acceptance: report 307/211 scoped term counts, 23/307 shape-target coverage,
  33/211 path coverage, pack namespaces, 30 linked examples and 21 CQs accurately;
  replace ten-CQ wording and restricted-denominator “all modules” inference.
  Query execution, curated example linkage and exact expected answers are distinct.
- Checks: existing quality `--check-only`; `python -m pytest
  tests/test_competency_query_expectations.py tests/test_competency_queries.py`;
  manual table/source denominator reconciliation recorded in the manifest.

### [ ] MNV.06 — Integrate bounded controls and case results without inventing evaluation

- Depends on: MNV.02/05; existing semantic controls. OCS.07/12 provide held-out
  requirements, case selection and results **only if those results are included**.
- Authored files (three): `docs/paper/paper.tex`,
  `docs/paper/supplement-package.md`,
  `docs/paper/revisions/20261108/evaluation-scope.md` (future).
- Generated derivatives: selected case/control table and result receipts, if real.
- Acceptance: bind valid/mutated pairs and exact CQ checks to actual outputs;
  distinguish missing source evidence from examined unsupported concepts. Freeze
  held-out cases before scoring; report sample counts/failures and reviewer roles.
  If unavailable at cutoff, state no held-out generalisation result and keep that
  study future work; resource corrections remain deliverable.
- Checks: existing `python -m pytest tests/test_semantic_hardening.py
  tests/test_game_temporality.py tests/test_negative_shacl_fixtures.py` plus the
  actual OCS case-evaluation command from its receipt when available. Do not name a
  nonexistent future evaluator as a passed test or duplicate FRT.04's experiment.

### [ ] MNV.07 — Integrate corrected mathematical and execution distinctions

- Depends on: MNV.02; semantic reconciliation. Provider receipts are conditional.
- Authored files (two): `docs/paper/paper.tex`,
  `docs/paper/supplement-package.md`.
- Acceptance: criterion/result/computation/allocation and causal direction agree
  with corrected terms; static/dynamic structure is independent of representation
  and scheduling. Runner/first-action labels state reference origin. UOGTO,
  Paignia and optional Kairos ownership is clear. Consumer receipt scopes remain
  SGC-owned; no Rust, LLM or native-execution inference from labels/fixtures.
- Checks: existing `python -m pytest tests/test_semantic_hardening.py
  tests/test_game_temporality.py tests/test_runner_execution_origin.py
  tests/test_game_runner.py`; source-to-claim review against C06–C08.
  Actual adapter claims additionally require the relevant SGC/FRT receipt;
  omitting those claims does not block this leaf.

### [ ] MNV.08 — Replace mapping and graph displays with one consistent reanalysis

- Depends on: MNV.01–02; corrected accepted exports and network receipts.
- Authored files (three): `docs/paper/paper.tex`,
  `docs/paper/supplement-package.md`,
  `docs/paper/revisions/20261108/figure-table-inputs.json` (future).
- Generated derivatives: new candidate mapping/graph figures, graph CSVs and
  corresponding paper PDFs, explicitly listed and hashed. Preserve old frozen
  versions; do not let default renderer synchronization overwrite them accidentally.
- Acceptance: show historical 12/0/448 and corrected 4/6/450 with the same retained
  460-row denominator, separate from new-source results. Show accepted structural
  evidence and unsupported automatic-equivalence history without claiming precision.
  Reconcile graph 75/4/391/10 with definitions; remove obsolete 74/12/391/11 claims.
  Empty/two-row calibration/robustness scaffolds cannot establish performance.
- Checks: existing comparison/alignment artifact checks and focused mapping tests;
  inspect actual SVG/PDF and counts; optional renderer absence is recorded as
  unavailable, not a completed PDF. `make figure-caption-freeze` after final placement.

Phase B checkpoint: every current Results statement and display has a matching
frozen input and claim-ledger row. Historical results remain visibly historical.
Do not introduce interoperability/frontier results by treating roadmap tasks as
completed, and do not gate this phase on FRT.01–12.

## Phase C — reconcile the whole article and package the candidate

### [ ] MNV.09 — Reconcile the abstract, Discussion and publication framing

- Depends on: MNV.04–08.
- Authored files (two): `docs/paper/paper.tex`,
  `docs/paper/supplement-package.md`.
- Acceptance: abstract and summary agree with final counts and scope; Discussion
  reports unknowns and module-specific support rather than low-count precision;
  Conclusion remains a resource contribution. Update future work, glossary,
  AI/tool-use disclosure and release-versus-candidate wording. No external arXiv
  version, acceptance or empirical validity is asserted from local gate scores.
- Checks: existing `make manuscript-check`; C01–C12 and all citations reconciled
  through the ledger. The candidate manuscript date reflects its real revision.

### [ ] MNV.10 — Synchronize supplement, captions and reusable artifact links

- Depends on: MNV.09 and the chosen frozen candidate.
- Authored files (three): `docs/paper/supplement-package.md`,
  `docs/paper/revisions/20261108/claim-evidence.csv`,
  `docs/paper/revisions/20261108/figure-table-inputs.json` (future).
- Generated derivatives: article-facing table compilations, supplementary display
  index, caption-freeze manifest and packaging metadata where actually used.
- Acceptance: S1–S10, existing supplementary table/figure numbering, Results,
  appendix, bibliography and download links agree. No mixed-date artifact is
  presented as one new evaluation; every reused figure has source/version/license.
- Checks: existing `make figure-caption-freeze`, `make manuscript-sourcecheck`;
  inspect actual generated files and review image/caption placement. Re-score
  changed visuals only for their actual layout/legibility, not scientific merit.

### [ ] MNV.11 — Record reproducibility and current-head validation

- Depends on: MNV.10.
- Authored outputs (future, two):
  `docs/paper/revisions/20261108/validation-receipt.json`,
  `docs/paper/revisions/20261108/reproducibility.md`.
- Generated derivatives: logs, environment/version capture, frozen candidate
  archive and hashes. Keep exact local versus hosted outcomes separate.
- Acceptance: `make validate`, `make test`, citation/source checks and applicable
  manuscript checks pass on the recorded head; every skip/optional failure is
  explained. Asserted test counts are from actual receipts, not copied from the
  reconciliation baseline. Regenerated live tracked tables are deliberately
  committed before final clean-tree provenance. Missing new tests remain pending.
- Checks: existing `make validate`, `make test`, `make manuscript-pdf` and the
  Required Gate workflow on the changed head; targeted future tests in Phase A
  must exist and collect nonzero cases before being treated as evidence.

### [ ] MNV.12 — Produce an inspected source/PDF candidate and record external boundaries

- Depends on: MNV.11; clean final candidate and required publication tooling.
- Authored files (up to three):
  `docs/paper/revisions/20261108/publication-handoff.md` (future),
  this track's `plan.md` and `metadata.json` completion records.
- Generated derivatives: current arXiv source/PDF bundle, manifest, SHA256SUMS,
  privacy audit and hosted attestation receipts. Historical outputs remain dated.
- Acceptance: source/package/PDF inspection passes; handoff binds exact revision,
  manifest/archive hashes and actual CI run. Report repository revision complete
  separately from author upload, identifier assignment, external rendered-PDF
  inspection and journal decisions. No submission is performed by this track.
- Checks: existing `make arxiv-upload-ready
  ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"`, then existing strict
  scorer with threshold 995 and `.tmp/` outputs as listed in the substantive plan.
  These are future checks, not evidence supplied by planning. Re-read the actual
  submission-state file before naming any public arXiv version.

## Completion and rollback

MNV.00 is planning-complete; twelve implementation leaves are pending. Phase gates
are normal reviews and recorded checks, not recurring requests for permission.
If a source or experiment stays unavailable, record the limiting disposition and
narrow the claim. A newly proposed execution/frontier claim consumes existing
SGC/FRT evidence rather than changing the baseline resource-paper exit criteria.

Freeze historical inputs before deliberate revision. Revert a coherent revision
through its normal version-controlled changeset and restore links to its source
snapshot if needed; do not delete historical tracks or claim that rollback changes
an external publication. Root owns registry/status integration and overall checks
for the present planning-only change.
