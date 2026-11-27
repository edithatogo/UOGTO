# Specification — semantic interoperability and frontier research

## Purpose
Make UOGTO an interoperable semantic foundation with demonstrated preservation of
strategic meaning. Frontier and beyond-frontier are hypotheses tested against
existing tools, not status labels granted by completion of a plan.

## Ownership and dependencies
The existing semantic_game_contracts_20261107 track retains SGC.01–SGC.08. This
coordinating track consumes those outcomes and does not duplicate their implementation
or reopen historical tasks. Paignia owns Rust game representations, algorithms and
numerical diagnostics. UOGTO owns ontology, profiles and conformance fixtures. Kairos
owns optional dynamic time/state/RNG/replay. Applications own payoffs and empirical
assumptions. Voiage owns information-value estimands and arithmetic.

Static semantic acceptance does not require a Kairos adapter. Here static acceptance
means validation/interchange without a running simulator; it does not mean that the
represented strategic interaction must be a StaticGame. A DynamicGame can be analysed
offline. Dynamic-execution acceptance is an additional claim with trace evidence.

## Acceptance principles
Preserve full identities, information availability, player/action/payoff association,
chance structure and ordered values. Distinguish exact representation identity,
strategic equivalence under a named solution concept and approximate abstraction.
RDF graph isomorphism alone cannot certify strategic equivalence. Unknown/lossy
features fail explicitly or return a declared loss report. External engine execution
and numerical diagnostics must be real; self-echoing JSON is not a cross-engine test.

Use supported upstream C++/Python boundaries for OpenSpiel: its 2.0 Rust API is marked
unmaintained. Keep external engines optional and licence-separated; adopt exact
adapter versions only when qualified. No default Cargo dependency cycle between
Paignia, Kairos, Voiage or domain applications.

## Research boundaries
Novel composition, causal mapping, strategic information valuation and verified
translation each require baselines and falsifiable measures. Solver restart frequency
is not behavioural probability; equilibrium labels do not implement solvers; simulated
review is not independent evidence. Use regular internal code review and CI. Publication
and independent scientific assessment do not gate unrelated library releases.
