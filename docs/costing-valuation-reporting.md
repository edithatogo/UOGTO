# Costing, valuation and reporting reconciliation

Status: optional 0.1 semantic pack and sourced catalogue snapshot, prepared on
8 November 2026. This is an implementation of data semantics and consistency
checks. It is not a released costing engine, a consensus reporting guideline or
an empirical validation of a screening programme.

## Purpose and ownership

The [costing and valuation pack](../ontologies/applied/costing-valuation.ttl)
extends UOGTO's applied health-economics coverage without asserting that a cost,
resource, patient or study is a game. The separate
[HTA bridge](../ontologies/bridges/costing-hta.ttl) requires an explicit
transformation before a cost result is used in a decision payoff.

The proposed Dapane framework would implement resource measurement, valuation
and allocation contracts in Rust, initially exposed through Python. MCHS would
retain jurisdictional activity/funding rules; workforce and genomics packages
would retain their domain methods. UOGTO supplies vocabulary and conformance
semantics, not language bindings or financial calculation kernels. The shared
architecture and execution roadmap are maintained in
[MCHS](https://github.com/edithatogo/mchs/pull/411).

`standards_check` owns the source catalogue and original checklist pipelines.
UOGTO owns this semantic reconciliation and the study-to-evidence vocabulary.
The [import manifest](../validation/costing-reporting-import.json) pins the exact
source commit and SHA-256 digests used to generate the
[reporting snapshot](../ontologies/reporting/costing-profiles.ttl).
Digests identify the input catalogue files, not independently verified hashes
of publishers' articles.

## Economic objects and invariants

| Concern | Representation and boundary |
| --- | --- |
| Study scope | A bounded costing study, population, perspective, scenario and output denominator |
| Resource measurement | Resource-use observations have their own identity; activity/output measures remain distinct |
| Valuation | Quotes, immutable rate-release identities, effective periods and knowledge dates; valuation policy and basis are explicit |
| Numerical representation | Decimal and exact rational inputs are distinguishable; rounding/conversion policy must be explicit at a monetary boundary |
| Economic interpretation | Resource/opportunity cost, financial expenditure, accounting cost, tariff and payment remain separate bases |
| Allocation | Source ledger, shared cost pool and allocated recipient views are separate; allocation does not create another incurred cost |
| Processes | Model specification, activity and execution are separate; the ontology does not itself execute Petri nets or BPMN |
| Uncertainty | Parameter draw, uncertainty specification and actual population heterogeneity are distinct |
| Evidence | Source artefacts, review status and access status remain distinguishable from claims of validity |

The decimal ledger consistency profile checks declared pool totals, allocation
conservation and duplicate source valuations. Exact rational inputs avoid
forcing values such as one-third through a finite decimal approximation.
Arbitrary rational ledger arithmetic, automated pricing, empirical source
verification and clinical decision validity are future runtime concerns.

The 31 reporting domains cover more than the first executable shapes. Capital,
capacity, nonmarket valuation, equity and environmental inventory are
represented as reconciliation concepts; their complete calculation models are
not implemented by adding a domain label.

## Reconciliation model

The reconciliation preserves six distinct layers:

1. An instrument and its exact version, source URL, publication type and review scope.
2. Original item or principle identifiers, where those identifiers were verified.
3. Short original topic paraphrases, which do not replace official wording.
4. Qualified many-to-many mappings to common reporting domains.
5. Project-defined profiles selecting applicable instruments and requirements.
6. Study-specific assertions with applicability, reporting state and evidence.

`covers_topic` expresses an editorial association. It is neither `owl:sameAs`
nor a claim that requirements from different authorities are equivalent.
Domain-only coverage must not be promoted into invented numbered requirements.
`verificationScope` distinguishes `domain_mapping`, `item_mapping` and
`full_checklist`; this snapshot contains no full-checklist transcriptions.

Reporting completeness, methodological appropriateness, computational
verification and empirical validation are separate assessment dimensions.
Only a reporting assertion uses the reporting-completeness enumeration.
No combined checklist score is generated. A complete cost table can describe
an inappropriate valuation policy, and a structurally valid process graph can
contain unsubstantiated routing assumptions.

Reporting assertions distinguish `reported`, `partial`, `not-reported` and
`not-assessed`. Applicability is independently `applicable`, `not-applicable`
or `unresolved`. A reported claim needs an evidence reference; a not-applicable
claim needs a rationale. Presence of evidence does not establish its truth.

## Source coverage and maturity

The initial search identified 26 source records and 31 domains. Those records
include actual reporting instruments, methods/reference cases, appraisal
instruments, historical versions, protocols and evidence reviews. They are not
26 interchangeable checklists. The source catalogue records the search date,
URLs, source categories and limitations.

| Family | Role in the reconciliation | Initial item coverage |
| --- | --- | --- |
| CHEERS 2022 | General economic reporting, including cost-only work | All 28 original item identifiers mapped to topics |
| GHCC 2017 | Detailed costing principles and methods reporting | 17 principle identifiers; detailed checklist rows are not fully transcribed |
| TDABC Consortium 2020 | Process, time and capacity costing framework | Domain coverage; detailed 32-element extraction pending |
| AGREEDT 2018 | Diagnostic strategy reporting, relevant to genomics and screening | 44 original identifiers mapped |
| CHEERS-VOI 2023 | VOI reporting extension | Six supplemental identifiers; inherited elaborations remain source-dependent |
| CHEERS-AI 2024 | Economic evaluations of interventions using AI | Domain coverage; item extraction pending |
| iDSI 2016 | Contextual methodological and reporting principles | 11 principle identifiers mapped |
| ISPOR BIA and Second Panel | Budget-impact framework and impact-inventory/reference-case concepts | Domain coverage |
| AHPCS 4.2 and NHS ACG 2026 | Jurisdictional patient-costing conduct and reconciliation | Domain coverage; optional jurisdiction profiles |
| PECUNIA RUC | Multi-sector service/unit-cost measurement and valuation | Domain coverage; template reuse conditions preserved |
| Immunisation and UNAIDS programme costing | Sector-specific reporting concerns | Domain coverage |
| COI 2023, CHEC and Philips | Appraisal, distinct from reporting completeness | Domain coverage |
| AdViSHE | Reporting of model-validation evidence | Domain coverage |
| BMJ 1996 and CHEERS 2013 | Historical compatibility and supersession | Excluded from default active profiles |
| Microcosting and CHEERS ClimatE protocols; genomic reviews/protocol | Context and monitoring evidence | Evidence artefacts, not operational instruments |

The 106 verified item/principle identifiers have editorial topic mappings that
still require independent content review. Verified identifier does not mean
validated mapping or a fully implemented compliance checker.

CHEERS 2022 replaces CHEERS 2013. Budget-impact analysis needs its own profile.
CHEERS-AI is triggered by the nature of the intervention, not simply by an
analyst's use of an AI tool. A finalized successor to the 2016 microcosting
checklist-development protocol was not verified; CHEERS ClimatE was verified as
a 2025 development protocol. These are search findings, not proof that future
or unindexed instruments cannot exist.

This was a bounded primary-source review, not a registered exhaustive worldwide
systematic review. National HTA manuals, translations, specialty extensions and
study-design adjuncts remain ongoing curation work. Selection of an instrument
depends on the actual research design and jurisdiction. Restricted templates
and full copyrighted text are not redistributed in this snapshot.

## Common ontology domains

| Group | Reconciled domains |
| --- | --- |
| Decision definition | Study scope; comparators; perspective; cost concept; time basis |
| Measurement | Resource boundary; resource measurement; sampling; data collection; output denominator |
| Valuation and production | Price provenance; capital; price adjustment; nonmarket valuation; allocation; capacity/workflow |
| Variation and evaluation | Heterogeneity; equity; uncertainty; model validation; outcome measurement; VOI; budget impact |
| Communication and context | Results disaggregation; transferability; engagement; disclosure; diagnostic pathway; spillovers; environment; AI intervention |

Conflicting requirements remain visible. For example, complete allocation of
in-scope hospital accounts and a societal opportunity-cost analysis can both be
appropriate while yielding different totals. The reconciliation must retain
the valuation basis, perspective and policy instead of declaring one amount
universally correct.

## Newborn screening profile

The project-defined newborn profile composes CHEERS 2022, GHCC and AGREEDT.
TDABC, a jurisdictional patient-costing profile, budget impact or VOI can be
added when applicable. This composition is not an externally endorsed newborn
screening reporting standard.

Distinguish eligible births, infants, screening episodes, specimens/cards,
collection attempts, assays, batches, results, recalls, confirmations and
follow-up. A specimen may serve several tests; a batch may serve many infants;
an infant may need several specimens. These relationships must not collapse
into a single patient-row assumption.

Programme boundaries should explicitly include or exclude consent and
information, collection, transport, accession, quality control, first-tier and
reflex tests, repeat collection, reporting, recall, confirmatory diagnosis,
clinical handoff, programme administration, capital and unused capacity.
Long-term treatment and health outcomes belong to the linked evaluation when
in scope; assay cost alone does not establish programme cost-effectiveness.

Report distinct denominators such as eligible birth, screened infant, valid
screen, completed pathway and confirmed case. Specify whether the question is
average programme cost, marginal cost of an additional condition, expansion
at fixed capacity or the cost of a capacity step. Do not charge the existing
collection and transport process again for every extra analyte.

The [synthetic example](../examples/newborn-screening-costing.ttl) demonstrates
separate infant/specimen/batch/confirmation identities and allocation
conservation. All amounts and resource assumptions are fictional. It is a
semantic test fixture, not a clinical pathway, an Australian price release or
a programme estimate. The tests include deliberately inconsistent records to
show which declared invariants are rejected.

## Rebuild and verification

Check out the exact `standards_check` commit recorded in the manifest, then run:

```bash
python scripts/maintenance/import_costing_profiles.py \
  --registry ../standards_check/reconciliations/costing/costing-standards-registry.json \
  --mappings ../standards_check/reconciliations/costing/costing-item-mappings.json \
  --source-commit SOURCE_COMMIT_FROM_MANIFEST
make validate
make test
```

The importer checks the local input bytes against the exact Git commit before
writing provenance. It verifies reference integrity and refuses unverified item
identifiers and protocol/review records used as operational requirements.
SHACL tests cover semantic consistency and required evidence; they do not
verify publisher text or economic appropriateness. See the
[Conductor track](../conductor/tracks/costing_valuation_reporting_20261108/index.md)
for exact validation results and remaining research work.

## Primary reference entrypoints

- [CHEERS 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8749494/)
- [GHCC principles and methods reporting checklist](https://ghcosting.org/pages/standards/appendices/principles_and_methods_reporting_checklist.php)
- [TDABC Consortium consensus statement](https://doi.org/10.1186/s12913-020-05869-0)
- [AGREEDT](https://doi.org/10.1177/0272989X18797590)
- [CHEERS-VOI](https://doi.org/10.1016/j.jval.2023.06.014)
- [CHEERS-AI](https://doi.org/10.1016/j.jval.2024.05.006)
- [AHPCS 4.2](https://www.ihacpa.gov.au/resources/australian-hospital-patient-costing-standards-version-42)
- [NHS Approved Costing Guidance](https://www.england.nhs.uk/costing-in-the-nhs/approved-costing-guidance/)
- [PECUNIA RUC templates and use conditions](https://www.pecunia-project.eu/tools/ruc-templates)
- [CHEERS ClimatE protocol](https://doi.org/10.1136/bmjopen-2024-094617)

The exact versioned source catalogue is identified by the import manifest;
links above are navigational and can change independently of this snapshot.
