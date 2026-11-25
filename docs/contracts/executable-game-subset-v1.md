# Executable game subset v1 — declaration gate

This bounded **SGC.01 source-side implementation** accepts a versioned JSON declaration of a finite perfect-information extensive game against the accepted Paignia T17.01 contract. It cannot certify graph topology, downstream static Rust interchange, native solver calls, numerical results, causal traces or empirical validity. SGC.02–08 and qualified consumer receipts remain separate.

The `jsonschema` draft-2020-12 validator accepts only the exact provider profile `paignia/static-finite-perfect-information-sparse-zero/1.0.0` and two exact source revisions, `bd880dd756d2ba56cc5f479bc078cea31b53c1d1` and the signed Paignia 0.1.0 source `a04a19da06cc50e310a172574ed66f62000b891a`, with `paignia-core`/`paignia-solve` package version `0.1.0`. The public schema lives at `validation/executable-game-subset-v1.json`; an exact tested copy is embedded in the `uogto.interchange` Python package to keep installed-wheel behavior independent of repo-relative files. It uses the existing `jsonschema` dependency, not a competing schema engine.

The admitted declaration requires a full GameSpecification IRI and exact `GameSpecification` class IRI; `ExtensiveFormRepresentation`, finite acyclic class, `PerfectInformation`, zero-allowed chance branch validation, intentional sparse-zero payoffs and ordered pairwise-tolerance/lexical selection. Selection tolerance must be explicit, finite and nonnegative, and `native_execution_claim` must be `false`. Unknown versions, profiles, classes, solver IDs and extra claims fail closed. No automatic term equivalence is inferred.

Optional `strategic_timing` may be `StaticGame` or `DynamicGame` because classification of strategic timing is independent of representation and the *static semantic* notion of offline qualification. A `DynamicGame` declaration does **not** establish a dynamic native execution; it may describe a finite sequential model for offline analysis.

The installed validator checks the specification identifier as an absolute
RFC 3986 URI using its required URI validator. Relative references, embedded
spaces, and trailing whitespace fail at `game.specification_iri`.

The signed release was replayed on the same bounded static wire and comparator fixtures. [T21 static results](https://github.com/edithatogo/paignia/blob/fa68aa91a093deadfb86398ac6a284238767c8ce/docs/validation/receipts/t21-core/README.md)

Source facts: [Paignia's accepted T17 review](https://github.com/edithatogo/paignia/blob/bd880dd756d2ba56cc5f479bc078cea31b53c1d1/docs/validation/t17-review-20261117.md) and [neutral conversion contract](https://github.com/edithatogo/paignia/blob/bd880dd756d2ba56cc5f479bc078cea31b53c1d1/docs/architecture/game-semantic-conversion-v1.md). Source-level declaration admission alone leaves SGC.01's provider graph/consumer qualification obligations open and is not a release claim.

API: `from uogto.interchange import validate_executable_subset`. It raises `UnsupportedExecutableSubset(code, path, detail)` for unsupported input and returns `status=profile_declaration_compatible` with `native_execution_qualified=False` on declaration success. This contract never converts, coerces, fills missing payoffs or calls Rust.
