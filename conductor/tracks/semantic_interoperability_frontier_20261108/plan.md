# Plan — semantic interoperability and frontier research

Each leaf is one independently checkable outcome. Proposed paths are future targets,
not claims of existing code. Normal internal review and focused CI are sufficient;
a coherent public semantic change receives specialist internal review. Preserve
the existing SGC task owners. Dependencies identify the smallest required subset,
not a blanket gate on unrelated releases.

## [ ] FRT.01 — Consume the first qualified finite-game semantic profile

- Depends on: SGC.01–SGC.05 and static scope of SGC.08.
- Outputs: profile compatibility matrix; acceptance fixture manifest (future).
- Acceptance: Require actual Paignia reader/writer and full-IRI round trip; support only the declared normal-form/finite-tree subset.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.02 — Run a real Gambit interchange comparison

- Depends on: FRT.01; OCS.04.
- Outputs: optional adapter; external fixtures; focused integration tests; version record (future).
- Acceptance: Build/read a game in Gambit, compare players/actions/payoffs/information sets and returned strategy semantics; exact vs approximate results explicit.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.03 — Run a real OpenSpiel representation and trajectory comparison

- Depends on: FRT.01; OCS.05.
- Outputs: optional adapter; trajectory fixtures; integration tests; version record (future).
- Acceptance: Execute the external engine and preserve legal play, observations, rewards/returns and chance; no claim from an RDF-labelled fixture.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.04 — Build adversarial and metamorphic conformance cases

- Depends on: FRT.02–FRT.03.
- Outputs: mutation generators; held-out cases; evaluation runner; report (future).
- Acceptance: Detect swapped payoff ownership, IRI collisions, invalid probabilities and leaked information; renaming/reordering preserves intended invariants.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.05 — Qualify imperfect-information and simultaneous dynamic profiles

- Depends on: FRT.04; additional SGC profile version.
- Outputs: profile extension; Kuhn-poker and simultaneous-stage fixtures; tests (future).
- Acceptance: Preserve information partitions, perfect-recall assumptions and lawful observations; reject unsupported solver concepts.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.06 — Qualify optional native simulation trace interchange

- Depends on: SGC.06 and dynamic scope of SGC.08.
- Outputs: Paignia/Kairos adapter evidence; UOGTO trace validator; replay fixture (future).
- Acceptance: Distinguish offline solution analysis from play sessions and native execution; validate reproducible session and event identity.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.07 — Prototype explicit semantic-loss and equivalence checking

- Depends on: FRT.04–FRT.05.
- Outputs: transformation contract; checker; counterexamples; comparison report (future).
- Acceptance: Compare with existing verified game-description translation; state exactly which properties are preserved and produce a counterexample on failure.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.08 — Prototype typed composition and causal-game bridges

- Depends on: FRT.07; OCS.06.
- Outputs: one compositional profile; one causal profile; reference adapters; tests (future).
- Acceptance: Compare with Open Game Engine and PyCID; check port/information compatibility and intervention assumptions without claiming universal preservation.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.09 — Evaluate strategic uncertainty and information changes across applications

- Depends on: existing strategic-information note; qualified relevant profiles.
- Outputs: UOGTO field map; Paignia/Voiage paired-case fixtures; application study (future).
- Acceptance: Separate analyst uncertainty, player information, solver selection and empirical uncertainty; preserve signed outcomes and explicit failure states.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.10 — Evaluate constrained natural-language game construction

- Depends on: FRT.04 and FRT.07.
- Outputs: translation experiment; expert reference cases; deterministic/LLM baselines; report (future).
- Acceptance: Measure semantic errors, abstention, repair and generalisation against GameInterpreter/2026 consistency checkers; no first-of-kind claim.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.11 — Demonstrate benefits in two distinct applications

- Depends on: qualified static profile; FRT.04.
- Outputs: reimbursement pilot; distinct innovation or operational pilot; reproducibility record (future).
- Acceptance: Measure translation errors, modelling effort and reproducibility; clinical or causal validity remains separately evaluated.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.

## [ ] FRT.12 — Publish evaluated contributions with versioned benchmark artefacts

- Depends on: relevant completed research leaves.
- Outputs: benchmark release; methods paper; package/example docs (future).
- Acceptance: Choose publication by completed contribution; document negative results, unsupported features, versions and licence conditions.
- Execution: coding agent; split into a linked leaf if more than five authored files or a second independently testable behavior is needed. Generated derivatives are listed separately.
