# Gambit and OpenSpiel game catalogues

The [JSON-LD catalogue](../../data/processed/external-games/catalogues.jsonld)
records the game definitions shipped or exposed by the pinned upstream
releases. Each entry supplies its upstream loader key, label, format,
semantic mapping and source file SHA-256. The release resources supply the
upstream download and SHA-256. Keep the original source and the parameters
needed to load a particular game alongside a reference.

| Release source | Entries |
| --- | ---: |
| Gambit 16.7.0 package catalogue | 38 models, comprising 32 EFG and 6 NFG files |
| Gambit 16.7.0 contributed directory | 131 source files, comprising 86 EFG and 45 NFG files |
| GAMUT 1.0.1 registry exposed through Gambit | 35 base generators, 17 presets and 26 collections |
| OpenSpiel 2.0.2 source | 146 registrations, comprising 114 C++ games, 2 file loaders, 10 transforms and 20 Python games, plus two documented integrations |

The T21 OpenSpiel binary exposes 123 of the 126 C++ registrations. The
additional definitions are `hanabi`, `universal_poker` and `repeated_poker`,
which are available through optional build components. Python game modules register separately. A transform needs its input game
and configuration. Weighted voting and Atari use their linked Python
interfaces. The latter uses an external environment.

The contributed Gambit directory includes parser controls and files that
share a basename. Their keys retain the file suffix. A reference records the
source even when the file is a negative parser control. The GAMUT registry
uses `GuessTwoThirdsAve` and `ShapleysGame` as loader keys. The catalogue
preserves the Gambit-listed spellings as aliases. Collections group or select
generators. Presets provide parameters for a generator.

## Load and save

Gambit reads finite strategic games from NFG and finite extensive games from
EFG. The Gambit readers also support AGG action graph, BAGG Bayesian action
graph and GBT project files. Its model readers and writers preserve the
representation's choices, utilities and chance entries. A catalogue slug
loads the specific bundled EFG or NFG model. GAMUT classes generate a model
given parameters and a GAMUT installation. [Gambit formats](https://gambitproject.readthedocs.io/en/v16.7.0/formats.html) ·
[Gambit catalogue API](https://gambitproject.readthedocs.io/en/v16.7.0/catalog.html)

OpenSpiel loads a registered short name and a parameter map, sometimes after
importing a game module or enabling a build component. Its game-and-state
serializer records the game description with a state encoding. The default
state encoding records action history. Use the game's deserializer for
game-specific encodings and retain the matching runtime version. The
Gambit adapter can export admitted finite representations to EFG/NFG.
[OpenSpiel loader](https://openspiel.readthedocs.io/en/latest/api_reference/load_game.html) ·
[State serialization](https://openspiel.readthedocs.io/en/latest/api_reference/game_serialize_game_and_state.html)

## Semantic scope

The dataset links source references through PROV-O, groups them by release
through DCAT and uses `dct:subject` to point to existing UOGTO classes.
EFG maps to `ExtensiveFormRepresentation`. NFG and GAMUT map to
`NormalFormRepresentation`. OpenSpiel sequential, one-shot simultaneous
and mean-field declarations map to their corresponding representational
classes. General simultaneous and indirect metadata use the broad
`GameSpecification` subject. A subject is a classification of the
definition. Additional shapes and source checks govern any instantiated
game graph, including legal actions, information sets and utilities.

The catalogue includes bundled source definitions, including the optional
ones. Users can supply new games, use dynamically composed transforms or
select different parameter values. Those operations create new instances or
definitions to reference by their inputs. The catalogue keeps source assets
and game execution in the upstream libraries.

## Validate and reproduce

Download the release archives linked by `dcat:downloadURL` and the
[tagged PyGambit catalogue module](https://raw.githubusercontent.com/gambitproject/gambit/v16.7.0/src/pygambit/catalog.py).
The builder checks their hashes before parsing source files.
Use the repository's qualified Python and pass explicit paths:

```sh
target/dev-python/bin/python scripts/build_external_game_catalogues.py \
  --gambit /path/to/gambit-16.7.0.tar.gz \
  --gambit-catalog /path/to/v16.7.0/catalog.py \
  --gamut /path/to/gamut.src.tgz \
  --openspiel /path/to/open_spiel-2.0.2.tar.gz --check
target/dev-python/bin/python -m pytest -q tests/test_external_game_catalogues.py
```

The tests check the shape, unique loader identifiers, counts, classification
terms and representative source bindings through SPARQL. An executable
consumer also needs a graph and the appropriate runtime or solver profile.
