# Plan — current semantic repairs

Each leaf has a concrete behavior and bounded ownership. Split a leaf if additional
behavior is discovered; preserve historical completion claims within their original
scope. A planning document is not execution evidence.

- [x] RCH.01 Correct solution/result/computation categories and causal definitions.
  Files: core ontology; cooperative, algorithmic, compositional and causal modules.
  Check: focused hierarchy and definition regressions.
- [x] RCH.02 Declare existing runner predicates and synchronize JSON-LD contexts.
  Files: core ontology, core context, focused semantic tests.
  Check: each exercised UOGTO predicate resolves to a declared term.
- [x] RCH.03 Reject literal player references and invalid probability values.
  Files: core SHACL shapes, focused positive/negative tests.
  Check: valid controls pass; named malformed examples fail; existing examples pass.
- [x] RCH.04 Separate game temporality from normal/extensive representation.
  Files: temporal ontology module, context, shapes, worked example, focused tests.
  Check: dynamic normal-form and simultaneous dynamic descriptions remain possible.
- [x] RCH.05 Register a temporality competency query and expected bindings.
  Files: query, expectation manifest, modelling documentation.
  Check: result identities, not just row count, satisfy the question.
- [x] RCH.06 Label reference inspection and deterministic baseline execution.
  Files: runner engine, baseline module, focused execution-origin tests.
  Check: no output implies a model request or native solver was executed.
- [x] RCH.07 Remove unsafe accepted mappings and prevent lexical auto-equivalence.
  Files: mapping builder, review ledger, focused mapping tests; generated TTL/SSSOM
  exports are regenerated as derivatives and recorded separately.
  Check: universal-class/device and mismatched observation mappings cannot be emitted.
- [x] RCH.08 Make the wheel smoke test exercise the installed distribution.
  Files: package smoke test and any directly required package metadata.
  Check: imports resolve inside installed wheel from outside the checkout.
- [x] RCH.09 Reconcile current evidence, Paignia ownership and project context.
  Files: current assessment/migration notes, README, product and technology context.
  Check: current vs historical facts and pending vs implemented capabilities agree.
- [x] RCH.10 Run integrated validation and record exact outcomes.
  Files: plan, metadata, canonical status/runlog and legacy status pointer.
  Check: `make validate`, `make test`, focused public-contract review. Hosted current-head CI remains the pull-request merge gate.

- [x] RCH.11 Preserve SVG when optional derivative renderers are unavailable.
  Files: visualisation helper and renderer regression test; current derivatives
  regenerated where the available renderer supports them.
- [x] RCH.12 Report canonical pending Conductor tracks alongside historical phases.
  Files: status reporter, legacy pointer and focused status-reporting tests.
- [x] RCH.13 Publish current quality evidence with reproducible inputs.
  Files: current quality metrics/report, input manifest and scope/readme notes.

## Completion evidence

Local validation passed: `make validate`; `make test` (310 passed, 1 skipped,
55 warnings); semantic audit; comparison artifact check; independent internal
code review (no blocking findings). The arXiv-artifact test is skipped locally
because its package is built by the dedicated gate. Current-head hosted checks
remain visible on the PR; no external solver or scientific result is claimed.

RCH.09 reconciles context/documentation in the linked migration note, programme,
source audit, README, product/technology context and canonical/legacy ledgers.
These coordinated document surfaces do not create additional runtime acceptance.
