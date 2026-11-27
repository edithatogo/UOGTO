# Plan — repository maturity

Each leaf has at most five authored outputs; split additional behaviors into linked leaves. Generated artifacts are recorded separately. Ordinary focused internal review applies; existing CI requirements remain unchanged.

## [ ] MAT.01 — Qualify the declared OWL profile and semantic constraint scope

- Depends on: Current semantic reconciliation.
- Outputs (future): Documented profile; pinned checker configuration; positive and contradictory fixtures; tests.
- Acceptance: A real profile/reasoner check runs and distinguishes valid from intentionally invalid input; uncovered semantics and open-world limits are stated.

## [ ] MAT.02 — Exercise core and optional adapter compatibility separately

- Depends on: SGC.01 for adapter contract jobs; core matrix can proceed independently.
- Outputs (future): CI matrix; compatibility policy; selected smoke fixtures; tests.
- Acceptance: Core supported Python versions pass; optional library jobs use supported pinned versions and report skipped/unavailable providers distinctly.

## [ ] MAT.03 — Record reproducible package and release inputs

- Depends on: MAT.02 for selected release targets.
- Outputs (future): Artifact manifest; reproducibility check; release documentation; tests.
- Acceptance: Installed-wheel origins, dependency versions and relevant input hashes are recorded; failed artifact or provenance verification fails the release check.

## [ ] MAT.04 — Measure scale and add semantic metamorphic regressions

- Depends on: Qualified profile for interchange cases; RDF validation baselines can proceed earlier.
- Outputs (future): Benchmark corpus; runner; measured baseline; regression checks.
- Acceptance: Measure time/memory at declared graph/game sizes, then set justified budgets; renaming/reordering properties expose deliberate payoff or identity mutations.

## [ ] MAT.05 — Bind current metrics to their actual evidence inputs

- Depends on: Current mapping corrections and source audit.
- Outputs (future): Evidence manifest; report-scope checks; current calibration design; tests.
- Acceptance: Current and historical results cannot be silently interchanged; no empty calibration sample or self-labelled mappings are presented as independent agreement evidence.

## [ ] MAT.06 — Publish a compatibility-tested semantic release

- Depends on: Completed release-relevant MAT leaves and corresponding SGC scope.
- Outputs (future): Migration notes; downstream fixture matrix; changelog; release evidence.
- Acceptance: Existing IRIs survive, changed entailments are explained, declared consumers are actually exercised; broader solver or scientific validity is not inferred.
