# Plan — eight pending semantic-contract leaves

Each leaf implements one behavior in at most five files. New paths and tests
are marked **future** and must be created before use; a missing target or zero
collected tests is not a pass. `local` means a scoped diff review and focused
checks. `specialist` adds agent review of the coherent semantic/public contract,
not repeated human approval. Split additional behavior or files into a linked
leaf before expanding scope. Provider and numerical completion stay with their
existing owners.

## Phase A — explicit subset and identities

### [ ] SGC.01 — reject an unsupported executable contract version

- Behavior: an executable-profile validator rejects unknown versions and
  representations outside the declared subset instead of silently coercing them.
- Depends on: the existing interoperability inventory and game provider T17.01
  public contract; do not assume every ontology class is executable.
- Execution: specialist, semantic subset and public compatibility policy.
- Files (4, future): `docs/contracts/executable-game-subset-v1.md`,
  `validation/executable-game-subset-v1.json`,
  `uogto/interchange/game_contract.py`, `tests/test_executable_game_subset.py`.
- Check: `python -m pytest tests/test_executable_game_subset.py` (future target).
  Known supported fixtures pass; unknown versions and unsupported game classes
  produce named failures. Record exact `uogto-game-core`/`uogto-game-solve` versions.

### [ ] SGC.02 — preserve full semantic identifiers in Rust interchange

- Behavior: mapping a supported UOGTO identifier to a generic Rust identifier
  and back preserves the full IRI without label-based or local-name collisions.
- Depends on: SGC.01 and the provider's versioned identifier contract.
- Execution: specialist, public identifier mapping.
- Files (4, future): `uogto/interchange/game_contract.py`,
  `validation/game-identifier-mapping-v1.json`,
  `tests/test_game_identifier_mapping.py`, `docs/contracts/game-identifier-mapping.md`.
- Check: `python -m pytest tests/test_game_identifier_mapping.py` (future target).
  Distinct IRIs sharing a label or local name remain distinct; ambiguous or
  non-reversible encodings are rejected. No public namespace is renamed.

### [ ] SGC.03 — prevent specification/instance/session/trace conflation

- Behavior: the executable profile rejects identity assignments that collapse
  two separately declared instances, sessions, or traces into one run identity.
- Depends on: SGC.01–SGC.02; use existing `GameSpecification`, `GameInstance`,
  `PlaySession`, and `EventTrace` meanings.
- Execution: specialist, lifecycle identity semantics.
- Files (4): `shapes/executable-game-profile.shacl.ttl` (future),
  `examples/executable-game-identity.ttl` (future),
  `tests/test_game_execution_identity.py` (future), `docs/modelling-decisions.md`.
- Check: `python -m pytest tests/test_game_execution_identity.py` (future target),
  then `make validate`. Two sessions of one instance retain distinct traces;
  invalid identity/link assignments fail the scoped profile rather than adding
  unexplained global OWL restrictions.

## Phase B — distinguishing conformance checks

### [ ] SGC.04 — reject foreign action/payoff bindings in an executable game

- Behavior: the executable SHACL profile rejects an action or player-payoff
  binding that belongs to another game scope.
- Depends on: SGC.01–SGC.03.
- Execution: local against the reviewed profile.
- Files (3): `shapes/executable-game-profile.shacl.ttl` (future),
  `tests/fixtures/executable-game-scope-negatives.ttl` (future),
  `tests/test_executable_game_scope.py` (future).
- Check: `python -m pytest tests/test_executable_game_scope.py` (future target),
  plus existing `python -m pytest tests/test_game_runner.py
  tests/test_negative_shacl_fixtures.py`. Valid paired fixtures must pass so an
  always-rejecting shape cannot satisfy the negative controls.

### [ ] SGC.05 — round-trip a supported game without semantic loss

- Behavior: Turtle/JSON-LD/Rust-interchange round trips preserve the supported
  graph, scoped player/action identities, and payoff association.
- Depends on: SGC.02–SGC.04 and the provider's actual interchange implementation.
- Execution: specialist, cross-language public representation.
- Files (5, future): `uogto/interchange/game_contract.py`,
  `tests/test_game_contract_roundtrip.py`,
  `tests/fixtures/game-contract-roundtrip.ttl`,
  `tests/fixtures/game-contract-roundtrip.jsonld`,
  `validation/game-rust-roundtrip-receipt.json`.
- Check: `python -m pytest tests/test_game_contract_roundtrip.py` (future target).
  Compare graph isomorphism and explicit ordered-value rules; reject a mutated
  player/payoff association. A Rust provider must independently read and emit
  the fixture. Its exact Cargo target and output hashes belong in the future
  receipt; Python echoing its own output is not cross-language qualification.

### [ ] SGC.06 — attribute a trace to its declared execution origin

- Behavior: trace interchange retains session identity and distinguishes a
  reference-tool trace from one emitted by a qualified Rust runtime.
- Depends on: SGC.03, SGC.05 and the optional adapter's accepted trace contract.
- Execution: specialist, execution provenance and public trace mapping.
- Files (4, future): `docs/contracts/game-trace-provenance.md`,
  `validation/game-trace-provenance-v1.json`,
  `tests/fixtures/game-trace-provenance.json`, `tests/test_game_trace_provenance.py`.
- Check: `python -m pytest tests/test_game_trace_provenance.py` (future target).
  Reject conflicting session/provider identities and missing version evidence.
  A claimed native origin requires the provider's native-dispatch receipt;
  metadata or a reference fixture alone cannot prove Rust execution.

## Phase C — tooling interpretation and consumer acceptance

### [ ] SGC.07 — identify Python runner output as reference tooling

- Behavior: runner-facing output/help states its reference/experimental origin
  and never presents a Python run as production Rust simulation.
- Depends on: the known reference-tool origin and an agreed minimal origin-label
  vocabulary. Align those labels with SGC.01's profile when available; a completed
  Rust provider, native adapter, or SGC.06 is not a prerequisite for honest labels.
- Execution: local; no change to mathematical semantics or existing namespaces.
- Files (4): `uogto/runner/engine.py`, `docs/uogto-for-game-theorists.md`,
  `README.md`, `tests/test_runner_execution_origin.py` (future).
- Check: `python -m pytest tests/test_runner_execution_origin.py
  tests/test_game_runner.py` (first target future). Existing reference fixtures
  keep their documented role; a missing native path cannot silently fall back
  to Python while retaining a native/production label.

### [ ] SGC.08 — accept only a version-matched semantic consumer receipt

- Behavior: reject a consumer conformance receipt whose UOGTO profile, game
  package versions, or fixture hashes differ from the tested contract.
- Depends on: SGC.01–SGC.05 for a static semantic receipt. A receipt claiming
  dynamic execution additionally requires SGC.06 and the native provider's
  dispatch evidence. Downstream scientific-alignment owners retain provider/pin
  qualification. SGC.07's reference-tool labels do not gate static compatibility.
- Execution: specialist for the coherent public contract; reuse earlier reviews
  rather than adding a separate human approval chain.
- Files (4, future): `validation/semantic-game-consumer-receipt.json`,
  `scripts/validate_semantic_game_receipt.py`,
  `tests/test_semantic_game_receipt.py`, `docs/contracts/game-consumer-evidence.md`.
- Check: `python -m pytest tests/test_semantic_game_receipt.py` (future target),
  `python scripts/validate_semantic_game_receipt.py` (future helper), then
  `make validate` and `make test` at the phase gate. Require nonzero passing tests
  and real Rust interchange evidence; reject mismatched/absent evidence for the
  declared receipt scope. Test that a version-matched static receipt passes
  without a Kairos adapter or native-execution receipt, while promoting that same
  evidence to a dynamic-execution claim fails. A dynamic receipt must bind the
  SGC.06 trace contract and actual native dispatch before it can pass.
  Static acceptance establishes semantic compatibility only, not simulation,
  equilibrium correctness, numerical validity, model validity, or a provider
  release. Record static and dynamic outcomes separately within this leaf;
  passing one scope cannot mark the other accepted.

## Completion evidence

All leaves remain pending in this planning commit. Future completion records
exact revisions, commands, test counts, fixture hashes, failures, and specialist
findings. A qualified static semantic receipt can be consumed while SGC.06 and
the dynamic-execution receipt remain pending. Honest reference-tool labelling
can proceed independently. Neither partial acceptance closes the optional work
or the whole track. Preserve existing track ownership and external gates. No
ontology term, IRI, public schema, dependency pin, runtime, or scientific claim
changes as a side effect of creating this plan.
