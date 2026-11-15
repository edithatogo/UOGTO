# Namespace Compatibility Contingency Decision

Track: `uogto_namespace_compatibility_contingency_20260721`
GitHub issue: <https://github.com/edithatogo/UOGTO/issues/95>
External feedback: <https://github.com/biopragmatics/bioregistry/issues/1999>

## Current contract

- `uogto:` maps to `https://w3id.org/uogto/core#` and is the primary stable core namespace.
- `uogtox:` maps to `https://w3id.org/uogto/extensions#` and identifies intentionally separate extension modules.
- Both namespaces are present in release assets, JSON-LD contexts, w3id redirects, and prefix.cc mappings.

## Compatibility options

| Option | RDF identity impact | Decision |
|---|---|---|
| Register only the core prefix in Bioregistry | None | Recommended current approach |
| Document `uogtox` as a separately maintained extension prefix | None | Recommended current approach |
| Add generated aliases or compatibility contexts | Low, but must be clearly non-canonical | Consider only for a concrete consumer need |
| Squash namespaces in place | Changes published identity and downstream mappings | Reject for v1.0.0 |
| Introduce a new major-version namespace | Requires migration, deprecation, and release governance | Future architecture track only |

## Trigger

If Bioregistry requires one squashed namespace before accepting `uogto`, open a separate migration track with an impact assessment, compatibility tests, deprecation policy, release plan, and explicit maintainer approval. Until then, no published IRI or registry metadata is changed.
