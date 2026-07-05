# Interoperability Benchmarks and Executable Examples

## Overview

Build the next roadmap layer for executable interoperability by adding benchmark
fixtures and mappings for practical game-theory tooling and simulation engines.

## Functional Requirements

- Identify priority interoperability targets such as OpenSpiel, Gambit, PettingZoo, Gymnasium, Mesa, and simulation trace formats.
- Add representative examples that map UOGTO terms to executable game/runtime structures.
- Extend the runner/playground smoke tests where local execution is feasible.
- Keep mappings evidence-backed and avoid claiming full tool compatibility before round-trip tests exist.

## Acceptance Criteria

- A benchmark inventory records target tool, license, integration status, fixture path, and verification command.
- At least two executable interoperability fixtures have passing parse/query tests.
- Documentation explains which targets are asserted mappings, illustrative examples, or future candidates.

## Out of Scope

- Shipping a full solver framework.
- Requiring heavyweight external engines in the default validation gate.
