# Current semantic evidence

Snapshot: **8 November 2026**. The
[input manifest](current-evidence-manifest.json) fingerprints the ontology,
shapes, examples, contexts, query expectations, quality generator and accepted
mapping artifacts. It identifies the audited and integrated upstream revisions
without pretending that a file can contain its own final commit hash.

Regenerate the current quality report from a repository checkout with the declared
Python dependencies installed:

```sh
python scripts/maintenance/build_article_hardening_quality.py \
  --metrics docs/quality/current-semantic-quality.json \
  --report docs/quality/current-semantic-quality.md
make validate
make test
python scripts/maintenance/audit_semantics.py
make ontology-comparison-check
```

If input files change, refresh the manifest's SHA-256 values alongside the report.
The formal profile and continuously enforced evidence-manifest checks are future
MAT.01/MAT.05 work; this snapshot is a reproducible input record, not a new release
qualification system.

The report's 54 ontology files, eight shape files, 30 examples and 21 queries are
current. Its 307 classes and 211 properties follow the generator's declared-term
counting method. Full label/definition coverage is an annotation measure.
Class-target coverage and property-path coverage are only about 7.5% and 15.6%,
respectively; passing examples therefore cannot establish comprehensive semantic
constraint coverage. Scoped executable profiles remain necessary.

The local OWL RL run passes, while the OWL profile result is a syntactic screen.
It is not external OWL DL certification, game-theoretic proof or numerical solver
validation. The local full suite passed with 310 tests, one arXiv-artifact skip and
55 dependency deprecation warnings. Dedicated hosted gates supply publication
artifact and supported-CI-environment evidence separately.

The comparison corpus retains its prior term inventory; corrected current
decisions yield four accepted structural mappings and six pending domain reviews.
The new twenty-source discovery register has not been bulk-imported into that
corpus. June/July article snapshots, empty calibration scaffolds and two-row
robustness scaffolds must retain their stated scope; see the
[reconciliation notes](../semantic-reconciliation-20261108.md).

Live article-table compilations are regenerated from their sources: the SSSOM row
uses the corrected four mappings while older quality/calibration/robustness rows
keep their original source dates. The frozen manuscript is separate from these
live compilations; combining rows does not supply new independent validation.
