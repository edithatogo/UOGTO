# Interoperability Benchmarks

This inventory records repo-local benchmark fixtures for external game and
simulation tooling. It separates asserted RDF mappings from illustrative examples
and future candidates so the repository does not imply full external engine
compatibility before optional adapter tests exist.

Machine-readable inventory: `docs/interoperability-benchmarks.json`.

## Current Fixtures

| Target | License | Status | Fixture | Verification |
| --- | --- | --- | --- | --- |
| OpenSpiel | Apache-2.0 | Asserted fixture | `examples/openspiel-matrix-game.jsonld` | JSON-LD parse, execution-binding SPARQL query, `RDFGameRunner` payoff smoke |
| PettingZoo | MIT | Illustrative fixture | `examples/pettingzoo-aec-gridworld.jsonld` | JSON-LD parse, Markov transition SPARQL query, runtime/simulation binding query |

## Future Candidates

| Target | License | Disposition |
| --- | --- | --- |
| Gambit | GPL-2.0 | Future file-format candidate; keep runtime linking out of the default package until adapter boundaries are reviewed. |
| Gymnasium | MIT | Future single-agent or reduction candidate, lower priority than PettingZoo for native multi-agent semantics. |
| Mesa | Apache-2.0 | Future network/agent-based simulation trace candidate. |

## Claim Levels

- `asserted_fixture`: the fixture uses current UOGTO terms and has local parse,
  query, and lightweight runtime smoke coverage.
- `illustrative_fixture`: the fixture demonstrates a plausible mapping pattern
  using current UOGTO terms but does not claim an implemented external adapter.
- `future_candidate`: the tool is in scope for roadmap planning, but this track
  adds no fixture or compatibility claim.

## Verification

Run the focused benchmark gate:

```powershell
.pixi/envs/default/python.exe -m pytest tests/test_interoperability_benchmarks.py
```

Run the repository validation gate:

```powershell
make validate
```

The default gate intentionally avoids installing OpenSpiel, PettingZoo, Gambit,
Gymnasium, or Mesa. Optional round-trip adapters should live behind extras or
isolated CI jobs once they exist.
