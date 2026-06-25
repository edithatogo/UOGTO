# arXiv Source-Leak and Privacy Audit

Generated: `2026-06-25T09:23:06+00:00`
Status: `pass`
Package: `C:/Users/60217257/OneDrive - Flinders/repos/legal-nz/UOGTO/.tmp/arxiv-source-package-08a3b864`
Cleaner manifest: `C:/Users/60217257/OneDrive - Flinders/repos/legal-nz/UOGTO/.tmp/arxiv-source-package-08a3b864.manifest.json`

## Summary

| Check | Status | Evidence |
| --- | --- | --- |
| Comments and disabled/draft blocks | pass | comment_lines=0, suspicious_comment_lines=0 |
| Hidden files and directories | pass | count=0 |
| Private notes, referee material, journal templates | pass | count=0 |
| Unused figures | pass | count=0 |
| Auxiliary, log, and output files | pass | count=0 |
| Embedded PDF/image metadata | pass | metadata_bearing_files=0, private_metadata_hits=0 |
| Credentials, private keys, and tokens | pass | count=0 |
| Private URLs, local paths, and UNC paths | pass | count=0 |

## Findings

No failing source-leak or privacy findings were detected.

## Embedded Metadata Review

No embedded metadata markers were detected in package figures/PDFs.

## Scope and Policy

This manifest audits the cleaned arXiv source package, not the full working tree. The repository-native cleaner remains the authoritative packaging gate. Benign PDF/image metadata keys are recorded for reviewer inspection; credential-like or private-location values are treated as failing source-leak findings.
