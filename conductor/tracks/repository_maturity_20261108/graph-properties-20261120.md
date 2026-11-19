# Bounded graph metamorphic regression evidence

This MAT.04 increment tests the existing reference graph inspector without
changing ontology terms, SHACL shapes, solver interfaces or the costing/SGC lanes.
The input corpus is generated entirely from fictional IRIs and signed integer
payoffs. Two games share the same player/action pairs but have different payoffs,
so a cross-game lookup defect is observable rather than accidentally equivalent.

Three properties check IRI renaming, Turtle/inline JSON-LD equivalence, reversed
triple order, duplicate triple insertion, exact player/action identity and a
deliberate single-player payoff mutation. Oracles compare complete player-to-value
maps. This is stored-payoff inspection, not game execution or solver validation.

The optional `properties` extra keeps Hypothesis outside the ordinary runtime and
the unchanged Pixi environment. The new scoped workflow installs that extra,
executes `property_tests/` explicitly, and fails if the dependency or tests are
missing. PRs run up to 50 examples per property; weekly/manual campaigns use 500.
Graphs contain two games and two to four players. Address space is capped at
4 GiB, test time at ten minutes and total job time at fifteen minutes. These are
operational ceilings, not a measured scale-performance claim. Hypothesis seed,
minimal example, statistics and synthetic artifacts support reproduction.

## Executed evidence

Baseline: `147aee40fd682c0949244b5e34897ed952ed4b73`.
Python 3.10.22, RDFLib 7.6.0 and Hypothesis 6.168.5:

- Three properties passed at 50 examples and at 500 examples; the latter completed
  in 108.30 seconds with seed 20261122.
- Ruff check and formatting passed for the new property file.
- `make validate PYTHON=.venv/bin/python` passed all repository validation.
- The first `make test` run had 339 passed, one skipped and one failure because
  the isolated development environment lacked the declared setuptools build
  backend. After installing the declared build tools, the final `make test` run
  passed: 340 passed, one existing capability skip, 54 dependency warnings in
  64.02 seconds. No test was skipped or weakened to repair the environment.

MAT.04 remains incomplete: a measured time/memory scale corpus, justified regression
thresholds and qualified consumer interchange evidence are still required.
No scientific, semantic-release or external-solver qualification is implied.
