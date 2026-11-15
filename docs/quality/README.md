# Semantic evidence snapshot — 8 November 2026

## Interpretation after the 15 November integration

The files in this directory retain the evidence snapshot published at
`fa4e725d5f13830d3d44a2188c887fd546145ec3`. They are not a fingerprint or
validation receipt for the refreshed PR127 head. In particular, the snapshot's
CQ21 temporality query moved to CQ25 without changing its SPARQL bytes, and the
active expectation manifest changed its filename reference. Resolve historical
paths/hashes against that immutable source revision, not the new working tree.

See the [successor integration receipt](../../conductor/tracks/semantic_reconciliation_20261108/successor-integration-20261115.md)
for numbering ownership, checks and the unresolved predecessor handoff. The
historical snapshot is preserved rather than silently regenerated or backdated.
A new quality evaluation must produce its own dated inputs and actual receipts.

## Original snapshot and reproduction scope

Snapshot: **8 November 2026**. The
[input manifest](current-evidence-manifest.json) fingerprints the ontology,
shapes, examples, contexts, query expectations, quality generator and accepted
mapping artifacts. It identifies the audited and integrated upstream revisions
without pretending that a file can contain its own final commit hash.

Regenerate the quality report from a checkout of the stated snapshot with the
declared Python dependencies installed:

```sh
python scripts/maintenance/build_article_hardening_quality.py \
  --metrics docs/quality/current-semantic-quality.json \
  --report docs/quality/current-semantic-quality.md
make validate
make test
python scripts/maintenance/audit_semantics.py
make ontology-comparison-check
```

For a new evaluation, retain this snapshot and bind fresh input SHA-256 values to
its own report and actual run date. The formal profile and continuously enforced
evidence-manifest checks are future MAT.01/MAT.05 work; this snapshot is a
reproducible input record, not a new release qualification system.

The report's 54 ontology files, eight shape files, 30 examples and 21 queries
describe that snapshot. Its 307 classes and 211 properties follow the generator's
declared-term counting method. Full label/definition coverage is an annotation
measure. Class-target coverage and property-path coverage are only about 7.5%
and 15.6%, respectively; passing examples therefore cannot establish comprehensive
semantic constraint coverage. Scoped executable profiles remain necessary.

The snapshot's local OWL RL run passed, while the OWL profile result was a syntactic
screen. It is not external OWL DL certification, game-theoretic proof or numerical
solver validation. Its local full suite passed with 310 tests, one arXiv-artifact
skip and 55 dependency deprecation warnings. Dedicated hosted gates supply
artifact and supported-CI-environment evidence separately, tied to actual heads.

The comparison corpus retains its prior term inventory; corrected snapshot
decisions yield four accepted structural mappings and six pending domain reviews.
The new twenty-source discovery register has not been bulk-imported into that
corpus. June/July article snapshots, empty calibration scaffolds and two-row
robustness scaffolds must retain their stated scope; see the
[reconciliation notes](../semantic-reconciliation-20261108.md).

Live article-table compilations are regenerated from their sources: the SSSOM row
uses the corrected four mappings while older quality/calibration/robustness rows
keep their original source dates. The frozen manuscript is separate from these
live compilations; combining rows does not supply new independent validation.
