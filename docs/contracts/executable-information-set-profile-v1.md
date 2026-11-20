# Executable information-set profile v1

UOGTO projects a finite extensive-form game's declared decision partition.
Paignia admits the partition against the paired native graph. This profile
binds `paignia-core` 0.1.0 at
[`d4047c0`](https://github.com/edithatogo/paignia/commit/d4047c0648a89f2aee4461ff70bbc9641e5320cd).
It emits schema `1.0.0` and semantic profile
`paignia/static-finite-information-set-perfect-recall/1.0.0`.
[Paignia's native contract](https://github.com/edithatogo/paignia/blob/d4047c0648a89f2aee4461ff70bbc9641e5320cd/docs/architecture/game-information-contract-v1.md)

## Source and projection

Pass one asserted RDFLib graph context and the absolute IRI of its game
specification to `uogto.interchange.information_sets.project_information_sets`.
Select a graph explicitly when working with a dataset. The packaged SHACL
shape targets that specification. The source supplies exactly one named
extensive representation, declared players, one initial state and a complete
`hasState` inventory. A specification may also link named, explicitly typed
normal-form representations. Every state has one decision, chance or terminal
kind. Each decision has one declared controller and one canonical
`belongsToInformationSet` assignment. A decision's `hasInformationSet`
assertion may name the same set. Each set's members share one controller and
belong to the selected game. Explicit profile roles are exclusive, and
compatible supertypes such as `GameNode` may also be asserted.

| Projected field | Source |
| --- | --- |
| `specification_iri` and `representation_iri` | The selected `GameSpecification` and its `ExtensiveFormRepresentation`. |
| `root_iri` and `state_types` | `hasInitialState` and the complete `hasState` inventory with explicit node kinds. |
| `declaration.sets[].id` and `members` | The `InformationSet` named by each decision's `belongsToInformationSet`. |
| `declaration.sets[].player` | The common `Player` linked to all members by `controlsNode`. |

Full IRIs survive verbatim, including Unicode and fragments. The projection
sorts set identities and member identities. Versions, malformed identifiers,
foreign members and foreign or conflicting controllers fail with named
errors. The native consumer binds the provider revision, specification, root
and node inventory before passing `declaration` to
`build_information_set_graph`. The builder checks full decision coverage,
ordered legal actions, and perfect recall against the actual topology.
[RDF 1.1 Concepts](https://www.w3.org/TR/rdf11-concepts/#section-IRIs)

## Verification

The retained Turtle fixture describes two distinct decisions with the same
local name. Their acting player cannot observe the preceding chance outcome.
The Rust fixture builds the topology independently, reads the Python
projection, and reports the admitted set, controller, membership and native
action order. Native negative controls exercise player ownership, omitted
coverage, reordered actions and loss of recall after replacing chance with an
earlier choice.
The required GitHub gate executes the cross-language check on Rust 1.75.0.

```bash
target/dev-python/bin/python -m pytest tests/test_information_set_profile.py tests/test_package_install_smoke.py
RUSTC="$(rustup which --toolchain 1.75.0 rustc)"
RUSTDOC="$(rustup which --toolchain 1.75.0 rustdoc)"
export RUSTC RUSTDOC
target/dev-python/bin/python -m scripts.verify_information_set_profile \
  --cargo "$(rustup which --toolchain 1.75.0 cargo)"
```

The handoff covers source declarations and native admission. Runtime
scheduling, solver policies, numerical convergence and the other SGC
interchange profiles have separate acceptance.
