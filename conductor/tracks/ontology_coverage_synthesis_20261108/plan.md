# Plan — source coverage and concept synthesis

Each leaf is one independently checkable outcome. Proposed paths are future targets,
not claims of existing code. Normal internal review and focused CI are sufficient;
a coherent public semantic change receives specialist internal review. Preserve
the existing SGC task owners. Dependencies identify the smallest required subset,
not a blanket gate on unrelated releases.

## [x] OCS.01 — Publish the bounded November source audit and gap register

- Depends on: none.
- Outputs: docs/research/game-semantics-source-audit-20261108.md; docs/research/game-semantics-source-register-20261108.json.
- Acceptance: Parse JSON; check primary URLs and baseline evidence classifications; explicitly state search limits.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] OCS.02 — Acquire and chart the direct GTO predecessor and forward/backward citations

- Depends on: OCS.01.
- Outputs: source acquisition manifest; predecessor concept chart; licence record (future).
- Acceptance: Retrieve a permitted artefact or record paper-only/inaccessible status; inspect concepts rather than asserting a merge.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] OCS.03 — Chart videogame vocabularies and formal game languages separately

- Depends on: OCS.01.
- Outputs: GOP/VGO/CGO and GDL/GDL-II/Ludii/VGDL concept charts; exclusion ledger (future).
- Acceptance: Identify reusable mechanics/information concepts and exclude title-specific assets or unrelated taxonomy.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] OCS.04 — Extract Gambit representation and solver-result requirements

- Depends on: OCS.01.
- Outputs: docs/research/gambit-concept-crosswalk.md; fixtures; focused crosswalk test (future).
- Acceptance: Cover histories, information sets, recall, chance, mixed/behaviour strategies, exact payoffs, solver residuals; mark implementation gaps.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] OCS.05 — Extract OpenSpiel and PettingZoo environment semantics

- Depends on: OCS.01.
- Outputs: docs/research/environment-concept-crosswalk.md; fixtures; focused test (future).
- Acceptance: Distinguish observation/history/information-state, joint/turn actions, reward/return, termination/truncation and legal-action masks.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] OCS.06 — Attach source lineage and competency questions to accepted concepts

- Depends on: OCS.02–OCS.05.
- Outputs: versioned concept-lineage table; validation schema; selected ontology annotations; tests (future).
- Acceptance: Every selected assertion links to source evidence and a meaningful question; conflicts and unmapped terms remain visible.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] OCS.07 — Evaluate coverage on independently specified strategic cases

- Depends on: OCS.06.
- Outputs: research protocol; held-out case register; adjudication outcomes (future).
- Acceptance: Measure supported questions, representation loss and inter-reviewer disagreement; agent review is labelled internal.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] OCS.08 — Publish an updated, reproducible coverage study

- Depends on: OCS.07.
- Outputs: dated report; machine-readable results; manuscript update (future).
- Acceptance: Report actual denominators, acquisition limits and unmet concepts; no exhaustive or frontier claim beyond results.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.
