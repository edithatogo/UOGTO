# Reviewer calibration sample

## Snapshot status — 8 November 2026

The checked-in generated sample under `mapping-calibration/` is an earlier empty
scaffold (zero sampled/adjudicated rows). It is not independent calibration evidence
for the corrected current mapping set. Populate a real separately reviewed sample
before reporting agreement; see [current reconciliation](../semantic-reconciliation-20261108.md)
and MAT.05 in the repository-maturity track.

This report provides a balanced sample of accepted and rejected mappings for
manual calibration. It is intended to support agreement analysis and
adjudication logging in the article.

The generator writes:

- `mapping-review-calibration.json`
- `mapping-review-calibration.csv`
- `mapping-review-calibration.md`

Populate the reviewer B and adjudication columns when a second pass is
available. The generated summary will then report agreement rate and Cohen's
kappa.
