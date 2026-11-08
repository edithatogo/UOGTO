# Costing ontology execution and curation plan

## Implemented in this change

- [x] Separate resource measurement, valuation bases, source ledgers and allocation views.
- [x] Add exact input representations and explicit process/evidence semantics.
- [x] Add a separate HTA payoff bridge rather than inheriting game semantics.
- [x] Model reporting, appraisal, computational and empirical assessments separately.
- [x] Add synthetic newborn batch identities and positive/negative conformance cases.
- [x] Reconcile sourced instruments into common domains with original identifiers and explicit scope.
- [x] Pin derivative catalogue provenance and exclude protocols/history from operational profiles.
- [x] Run repository validation and record exact evidence and baseline failures below.

## Curation and runtime roadmap

- [ ] Independent health-economic and diagnostic-domain review of editorial mappings.
- [ ] Complete source-permitted item extraction for TDABC, CHEERS-AI, BIA, COI,
  immunisation, UNAIDS and jurisdictional costing profiles.
- [ ] Extend national HTA, reimbursement-submission and relevant study-design profiles.
- [ ] Monitor CHEERS ClimatE and the microcosting-checklist development literature.
- [ ] Qualify versioned JSON/Arrow contracts against the future Rust valuation core.
- [ ] Expand capital, productive capacity and nonmarket valuation shapes with executable consumers.
- [ ] Qualify Petri-net/PNML and BPMN subset mappings with actual process traces.
- [ ] Connect evidence assertions to real programme data, source releases and review records.
- [ ] Publish an independently reviewed ontology/profile release and namespace documentation.

## Validation evidence

Integrated `make validate` passed: all 30 examples conform and all 24 competency
questions meet expected results. Focused reporting-profile checks also pass,
including a real Git-commit/input mismatch rejection.

Final `make test`: **307 passed, 1 skipped, 3 failed, 56 warnings**. All three
failures reproduce on the untouched base commit
`71139cca03f69256b9e88390dd21a3b8ad7f1dc1`: two visualisation tests lack
ImageMagick's `rsvg-convert` delegate; the wheel smoke test creates a nested
`--system-site-packages` environment that cannot see RDFLib installed only in
the parent QA environment. Wheel construction itself passes. No unrelated
source tests were weakened or skipped to obtain this result.

Validation used RDFLib 7.6.0, PySHACL 0.40.2 and pytest 9.2.0 in an isolated
QA environment. `git diff --check` passed. Generated article-table side effects
were restored; no article/manuscript artefacts are included in this change.
This is not a fully green whole-repository test run. It does establish the
reported semantic/conformance checks; it does not qualify a Rust costing
runtime, source truth, clinical pathways or an external consensus standard.

Source catalogue: [standards_check PR 65](https://github.com/edithatogo/standards_check/pull/65).
Coordinating architecture: [MCHS PR 411](https://github.com/edithatogo/mchs/pull/411).

### GitHub and follow-up evidence

On commit `33a0aac205fd4a281753c5e3f3bac7b7f411cae1`, GitHub's full suite
passed **310 tests with 1 skipped**. The Required Gate also passed, including
manuscript/arXiv checks. The separate coverage command then exposed the same
instance-catalogue assumption that the first test adjustment addressed.

The follow-up fixes the actual coverage CLI with populated-catalogue checks and
seven CLI regressions. It also adds explicit activity-kind quotation so weighted
funding activity does not become a resource by inference. The fictional funding
example has zero Resource and ResourceUse instances after RDFS inference.

Follow-up local results: **58 focused tests passed**, `make validate` passed
**31 examples and 24 competency questions**, `make coverage` passed, and
`git diff --check` passed. The whole-suite CI rerun for this follow-up is pending;
the earlier full-suite results are not relabelled as a test of a later commit.
