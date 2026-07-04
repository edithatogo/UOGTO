# Validation Contract and Release Metadata Coherence

## Overview

Close the current-version gaps found during repository review: competency-query
expected results must be a single complete contract, release metadata must agree
across ontology and package surfaces, and generated tabular artifacts must not
leave line-ending-only working tree churn after validation.

## Functional Requirements

- Maintain one active competency-query expectation manifest under `validation/`.
- Require every `competency-questions/*.rq` file to have expected-result coverage.
- Make required binding checks robust when queries return extra selected columns.
- Ensure mechanism-design examples exercise `cq06` with an incentive constraint.
- Align Python/Pixi package version metadata with the v1.0 ontology release.
- Normalize repository text line endings, especially generated CSV artifacts.

## Acceptance Criteria

- `make validate` passes and reports expected-result satisfaction for all ten competency queries.
- Focused competency-query tests pass and fail if any `.rq` lacks an expectation entry.
- `competency-questions/expected-results.json` is removed as a duplicate source of truth.
- `pyproject.toml`, `pixi.toml`, ontology headers, citation metadata, and Zenodo metadata no longer disagree on the released version.
- `git diff --check` passes.

## Out of Scope

- Changing ontology namespace IRIs.
- Publishing a new release tag.
- Reworking competency-query semantics beyond the current expected-result contract.
