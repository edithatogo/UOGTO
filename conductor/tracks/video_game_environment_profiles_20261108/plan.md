# Plan — video-game environments and strategic scenario profiles

Each leaf is one independently checkable outcome. Proposed paths are future targets,
not claims of existing code. Normal internal review and focused CI are sufficient;
a coherent public semantic change receives specialist internal review. Preserve
the existing SGC task owners. Dependencies identify the smallest required subset,
not a blanket gate on unrelated releases.

## [ ] VGP.01 — Specify one bounded game-environment scenario profile

- Depends on: OCS.03; OCS.05.
- Outputs: scenario contract; source/asset licence record; concept crosswalk (future).
- Acceptance: Identify strategic actors vs fixed dynamics, goals vs rewards vs utilities and selected observation model.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] VGP.02 — Implement an open reference environment mapping

- Depends on: VGP.01; relevant FRT adapter.
- Outputs: minimal environment adapter; semantic example; focused tests (future).
- Acceptance: Execute a small PettingZoo/OpenSpiel environment and compare supported actions/observations/transitions and trace identity.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] VGP.03 — Measure abstraction and transfer loss

- Depends on: VGP.02; FRT.04.
- Outputs: paired scenario fixtures; loss checker; report (future).
- Acceptance: Show which conclusions survive abstraction; fail information leakage, missing actors and unjustified payoff assumptions.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] VGP.04 — Assess one commercial-world research adapter only if useful

- Depends on: VGP.03.
- Outputs: GTA-like scenario proposal; access/licence assessment; experiment plan (future).
- Acceptance: Proceed only with a concrete strategic question and authorised environment access; no title-wide completeness claim.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.
