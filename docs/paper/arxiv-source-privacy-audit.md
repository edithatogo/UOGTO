# arXiv Source-Leak and Privacy Audit

Generated: `deterministic-local-preflight`
Status: `pass`
Package: `.tmp/arxiv-source-package`
Cleaner manifest: `.tmp/arxiv-source-package.manifest.json`

## Summary

| Check | Status | Evidence |
| --- | --- | --- |
| Comments and disabled/draft blocks | pass | comment_lines=0, suspicious_comment_lines=0 |
| Hidden files and directories | pass | count=0 |
| Private notes, referee material, journal templates | pass | count=0 |
| Unused figures | pass | count=0 |
| Auxiliary, log, and output files | pass | count=0 |
| Embedded PDF/image metadata | pass | metadata_files_reviewed=3, metadata_bearing_files=2, private_metadata_hits=0 |
| Credentials, private keys, and tokens | pass | count=0 |
| Private URLs, local paths, and UNC paths | pass | count=0 |

## Findings

No failing source-leak or privacy findings were detected.

## Embedded Metadata Review

- `figures/import-evidence-use-cosmograph.pdf`: Author, CreationDate, Creator, ModDate, Producer, Title; private hits=0
- `figures/term-alignment-cosmograph.pdf`: Author, CreationDate, Creator, ModDate, Producer, Title; private hits=0

## Scope and Policy

This manifest audits the cleaned arXiv source package, not the full working tree. The repository-native cleaner remains the authoritative packaging gate. Benign PDF/image metadata keys are recorded for reviewer inspection; credential-like or private-location values are treated as failing source-leak findings.
