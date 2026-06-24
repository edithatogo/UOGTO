# RO-Crate 1.1 Package Output

This artifact is the early RO-Crate surface for the article-hardening evidence package. It exists to make the crate structure part of the protocol, not just an end-stage export.

## Metadata

- Specification: RO-Crate 1.1
- Status: Recommendation
- Root metadata file: `docs/article-hardening/ro-crate-metadata.json`
- Package focus: UOGTO article-hardening evidence bundle

## Root Data Entity

The root data entity is the article-hardening package itself, represented as the dataset identified by `./` in the RO-Crate metadata.

## Data Entities

The crate includes the core protocol, checklist, evidence register, source inventory, quality benchmark, review and research logs, case-study outputs, screening samples, and analysis artefacts.

## Contextual Entities

The crate records contextual entities for standards, licences, source repositories, and related evidence references where they are available.

## Provenance

The package keeps provenance by preserving the search log, the source-extension inventory, the review log, the research log, and the generated analysis artefacts that derive from them.

## Workflows and Scripts

The crate also references the scripts and workflows used to build and validate the package, including the maintenance validators and the Conductor review workflows.

## Early Output Rule

RO-Crate output must be created alongside the protocol and search strategy, not deferred until the end of the article-hardening workflow.

## Included artifacts

- `docs/article-hardening/ro-crate-metadata.json`
- `docs/article-hardening/protocol.md`
- `docs/article-hardening/protocol-checklist.md`
- `docs/article-hardening/structured-summary.md`
- `docs/article-hardening/prisma-scr-artifact-map.md`
- `docs/article-hardening/search-strategy.md`
- `docs/article-hardening/search-log.jsonl`
- `docs/article-hardening/source-extension-inventory.json`
- `docs/article-hardening/quality-metrics.json`
- `docs/article-hardening/reasoner-report.md`
