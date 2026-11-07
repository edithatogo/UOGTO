# Specification — executable game subset and semantic identity

## Baseline and ownership

At `ac5b8e86c4a3547d008e83ba4cfcbb5f3ba95f25`, UOGTO already defines
`GameSpecification`, `GameInstance`, `PlaySession`, and `EventTrace`. Existing
runner tests distinguish actions and payoffs belonging to different games;
existing SHACL suites reject representative invalid graphs. These are reference
tooling and semantic checks, not proof of production Rust simulation or general
solver correctness.

UOGTO owns the versioned executable semantic subset and its mappings to the
existing `uogto-game-core` and `uogto-game-solve` packages incubated in
`new-drug-reimbursement-game`. Their provider T17 owns Rust package behavior and
numerical qualification. Static game solving has no Kairos dependency. A
separate optional adapter depends on game core and Rust Kairos for simulation
time, scheduling, state, RNG, and traces. UOGTO must not create another scheduler
or generic game library. Domain applications retain their games and payoffs.

Existing downstream `scientific_ecosystem_alignment_20261029` tracks retain
provider-contract acceptance, pins, installed-consumer qualification, and their
current deferrals. This UOGTO checkout contains no local track with that ID;
this plan does not invent, replace, or close one. Historical UOGTO ontology and
interoperability track completion remains bounded by its original evidence.

## Contract requirements

The first executable subset must be declared against exact game package
versions and supported representations. Finite perfect-information/chance and
normal-form examples are candidates, not blanket support for all UOGTO classes.
Unsupported representations and unknown contract versions must be rejected
explicitly. An ontology statement that a game exists does not mean the Rust
provider can execute or solve it.

| Identity | Meaning to preserve through mapping |
|---|---|
| Game specification | Versioned structural rules, players, actions, and utilities |
| Game instance | Parameterized realization of a particular specification |
| Play session | One run/play of that instance, with its own identity |
| Event trace | Recorded events attributed to that session and execution origin |

Repeated runs share a specification when appropriate but never overwrite each
other's session or trace identity. Mappings preserve full IRIs, scoped player
and action identifiers, payoff ownership, and provenance. SHACL applies the
chosen closed-world executable profile without silently tightening the entire
open-world ontology. A proposed new term or public schema change requires its
own explicit ontology change contract; none occurs in this planning change.

Round trips compare semantic graphs and declared value/order invariants across
Turtle, JSON-LD, and Rust interchange fixtures. Negative cases must detect
unsupported versions, foreign game/player references, lossy identifiers,
swapped payoff ownership, and session/trace conflation. A passing Python-only
round trip is not evidence of a passing Rust package interchange.

The Python runner, graph inspection, playground, and reference converters remain
reference/experimental tooling. Their output must identify that origin, and
documentation must distinguish it from production execution by the Rust game
packages and optional Rust Kairos adapter. Missing native execution cannot be
reported as success by silently running the Python reference tool instead.
Semantic conformance does not discharge inherited RK4, Nash, CE, or CFR numerical
obligations in the game-provider/Kairos scientific registers.

## Acceptance, review, and scope

The eight leaves define version rejection, identifier mapping, identity scopes,
SHACL negatives, cross-language round trips, trace provenance, tooling labels,
and a version-specific consumer receipt. Each has a file limit and a focused
test. Routine work uses diff review and focused checks; a coherent semantic or
public interchange boundary receives specialist agent review and relevant CI.
Agent review is an internal control, not external peer or domain-expert approval.
Repeated human approval is not an implementation gate in this solo-maintainer
workflow. Unresolved semantics remain explicit alternatives or unsupported.

Acceptance is scoped to the capability used. Static semantic compatibility needs
SGC.01–SGC.05 and a version-matched SGC.08 receipt with actual Rust interchange;
it does not require a Kairos adapter or native simulation evidence. A dynamic
execution receipt additionally requires SGC.06's trace contract and the native
provider's dispatch evidence. Record these outcomes separately, retaining the
optional execution work as pending until its own checks pass. SGC.07 can label
the known Python reference origin before a native adapter exists. Static
acceptance does not close the whole track or any numerical/provider obligation.

This change adds planning documents only. No IRI, ontology, SHACL shape,
JSON-LD context, runtime, dependency, pin, or generated artifact changes. All
execution and provider acceptance remain pending. Future implementation records
exact versions, fixture hashes, test counts, and review outcomes; rollback uses
the last qualified contract/profile and provider version while preserving old
identifiers and historical receipts.
