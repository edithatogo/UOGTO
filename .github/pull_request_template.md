## Summary

Describe the change and the reason for it.

## Change Type

- [ ] Ontology vocabulary or modelling change
- [ ] SHACL validation change
- [ ] Example or competency-query change
- [ ] Documentation, glossary, or release-note change
- [ ] Manuscript, figure, supplement, or arXiv-package change
- [ ] CI, packaging, registry, or automation change
- [ ] RI-HERO program or project-tracking change

## Ontology Contract

- [ ] New or changed classes/properties have `rdfs:label` and `skos:definition`.
- [ ] ObjectProperties and DatatypeProperties remain separated.
- [ ] SHACL shapes cover any changed validation invariants.
- [ ] Examples demonstrate changed modelling patterns.
- [ ] Competency queries cover changed retrieval behavior.
- [ ] Documentation and glossary entries are updated where public interpretation changes.
- [ ] Release, registry, manuscript, or RI-HERO impacts are noted below.
- [ ] Not applicable.

## Downstream Game Intake

For a new or changed game, complete the [intake contract](../docs/contracts/downstream-game-intake.md).

- Intake key and originating repository/source revision:
- UOGTO mapping/example update and disposition (`reuse_existing`, `extension_required`, `unsupported`, or `mapping_review_pending`):
- Linked Paignia reusable implementation and relevant upstream-provider decision:
- Exact semantic/profile versions, full-IRI mapping and bounded test evidence:
- [ ] No new or changed game is involved.

## Validation

- [ ] `make validate`
- [ ] `make test`
- [ ] `make publishing-metadata`
- [ ] `make registry-links`
- [ ] `make manuscript-pdf`
- [ ] `make arxiv-upload-ready`
- [ ] GitHub Actions `Required Gate`
- [ ] Not applicable, with rationale below.

## Impact Notes

- Related issue, project item, or external reference:
- Release or registry impact:
- Manuscript or arXiv impact:
- RI-HERO impact:
- Validation exceptions or warnings:
