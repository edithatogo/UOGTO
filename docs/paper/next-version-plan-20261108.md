# Next version of the existing UOGTO resource paper

Planning date: **8 November 2026**. Planning baseline: repository revision
`f606ecc506130fdf88a435b3012b36c8760ad7a9` and the sources identified below.
**This plan is delivered; manuscript revision, new evaluation and publication are
pending.** The author requested a plan, so this change does not rewrite
`paper.tex`, its bibliography, or the historical supplement.

## 1. Publication object and stopping boundary

Revise the existing *Universal Open Game Theory Ontology (UOGTO): An extensible
semantic resource for strategic-interaction evidence*, retaining its resource-paper contribution and
specification/instance/session/trace design. The immediate contribution is a
source-attributed resource with corrected semantics, a reproducible evidence
snapshot, a defensible comparator account and clearly bounded validation. It does
not need the entire twelve-leaf interoperability/frontier programme to finish.

The repository's [arXiv state](arxiv-submission-state.md), last updated 5 July,
records `not_submitted`, with identifier and version unassigned. This is the next
repository manuscript version. Calling it public “arXiv v2”, a published
correction, an accepted paper, or an externally reviewed resource would require
new evidence. Recheck the state before submission; the local file is not an
independent current query of arXiv. Journal selection remains a submission choice,
not an implementation gate on this revision. The historical [decision memo](submission-revision-decision-memo.md)
and [revision backlog](submission-revision-backlog.csv) retain venue-specific
conditions without demonstrating acceptance or present-day venue policy.

Three publication scopes must remain distinct:

| Scope | Contribution and evidence | Dependency boundary |
| --- | --- | --- |
| Next resource-paper revision | Correct current claims, attribute predecessors and concepts, report bounded coverage and validation, publish reproducible artifacts | Semantic reconciliation plus the source/charting receipts needed for the claims actually retained; no blanket FRT dependency |
| Later interoperability methods paper | Demonstrate semantic preservation across actual independent representations and engines | Relevant SGC.01–05/static SGC.08, FRT.01–05 and real provider/library receipts |
| Later frontier/application study | Test semantic-loss detection, typed composition, strategic information, constrained game construction or modelling benefits against explicit baselines | The particular FRT research leaves and application evidence; not “all twelve completed” by default |

A resource revision may report descriptive examples and unsolved gaps while later
held-out, interoperability and empirical work remains pending. Any additional
claim of translation accuracy, solver correctness, model validity or useful
behavioural effects must bring its own evaluation. Narrow the claim if that
receipt is unavailable at the frozen submission cutoff; do not silently promote
planned work into Results.

## 2. Required corrections in the existing manuscript

The following map refers to current section headings, table labels and supplement
sections, avoiding brittle line numbers. Evidence comes from the retained
[manuscript](paper.tex), [supplement](supplement-package.md),
[semantic reconciliation](../semantic-reconciliation-20261108.md),
[current mapping report](../ontology-comparison/report.md) and
[current quality report](../quality/current-semantic-quality.md).

| Claim ID and location | Existing statement or implication | Revision and supporting evidence |
| --- | --- | --- |
| C01 — Abstract; Results “Source discovery”; `tab:mapping-summary`; mapping-flow appendix; supplement S2/S4 and Results | 460 candidates; 12 accepted; 448 rejected/non-asserted; zero domain review | Identify these as the historical June analysis. November reanalysis of the same 460 rows has **4 accepted structural narrow matches, 6 needing domain review, 450 rejected**. Four plus six plus 450 equals 460; rejected and unresolved are separate categories. Source: current `mapping-review.csv`, TTL/SSSOM exports and builder guard tests. |
| C02 — Results “Sparse mappings”; Discussion “restraint”; glossary accepted mapping | Twelve “careful”, “conservative”, “reviewed” alignments imply assessed semantic quality; low acceptance implies precision | Explain that eight earlier equivalences were deterministically prefilled by automation, and four narrow matches are supported by checked-in subclass assertions. Two equivalences are false for the compared scopes; six lack adequate evidence. Acceptance rate alone estimates neither precision nor semantic correctness. No fabricated expert adjudication or agreement statistic. |
| C03 — Results and Methods source discovery; supplement S1/S2 | Negative route found no additional includable game-theory ontology | Preserve the dated search event but withdraw any inference of absence. The November audit identifies Mejbri's GTO predecessor through a retrieved 2018 paper citing the original 2013 work. Describe original-source/artifact acquisition separately; absence from UOGTO's register differs from absence of prior work. |
| C04 — Introduction/related work; source families | A broad baseline inventory stands in for strategic-game coverage | Of 21 baseline comparator records, four are parsed external RDF artifacts and 17 are metadata-only. The 39-record extension register and twenty-source November audit are separate, overlapping discovery surfaces. Deduplicate the union; do not add their counts or call all records acquired ontologies. |
| C05 — Methods “Ontology representation and validation”; module audit; supplement S3 | Ten competency questions; module coverage presented without denominator | Current snapshot has 21 queries, 30 examples, 54 ontology files, eight shape files and scoped term counts below. Retain ten/17/49/five only in the identified historical snapshot. Separate file counts, named terms, linked examples, query execution and exact answer checks. |
| C06 — Semantic core and design explanation; new methods paragraph | Representation, strategic timing and runtime may be conflated | Explain static/dynamic strategic structure independently of normal/extensive representation, physical time and API scheduling. Use the new dynamic-normal-form example and CQ21 as descriptive evidence, not a complete tree/payoff tensor or an engine qualification. |
| C07 — Design/results; solution vocabulary | Equilibrium, allocation results and computational problems may appear interchangeable | Explain corrected `SolutionConcept`, `GameSolution`, `EquilibriumPredicate`, `ComputationalProblem` and `AllocationSolution`; use causal equations with parents/exogenous inputs determining the endogenous variable. Preserved IRIs have changed entailments, requiring migration notes. |
| C08 — Runtime/examples; reuse narrative; AI disclosure | LLM-labelled tool or external-library-labelled fixture can imply actual model/solver use | Reference runner inspects graphs and looks up stored payoffs; first-action baseline performs no LLM request or native solve. Existing OpenSpiel/PettingZoo-labelled RDF fixtures are fixtures. UOGTO owns semantics, Paignia runtime/adapters, Kairos optional simulation; inspect/pin actual provider versions before stronger claims. |
| C09 — Results network section; appendix graph summary and graph PDFs | 74 source/import nodes; 12 alignment edges; 11 module-coverage edges | Current retained-corpus reanalysis reports **75 source/import nodes, four alignment edges, ten coverage edges and 391 similarity edges**. Freeze each graph's node/edge definitions and inputs. Do not attribute every difference solely to mapping deletion or interpret graph centrality as semantic validity. |
| C10 — Robustness/calibration; supplement S5/S8 | Scaffold outputs or internal figure scores imply performance or reviewer confidence | Inspected calibration has zero sample rows; robustness sample has two. These cannot establish held-out performance, general precision or expert agreement. Internal 100/100 figure scores and 995/1000 submission scores concern local checks, not publication merit or independent review. |
| C11 — Resource snapshot/data availability; supplement S7/S9/S10 | v1.0.0 release metadata appears to identify November corrected contents | Distinguish the cited historical release/DOI from the next candidate revision. Record commit, ontology/profile version, input/output hashes, software environment, licenses and actual archive identifier if assigned. Do not reuse a release identifier as proof that new files were deposited. |
| C12 — Discussion limitations/future work; economics roadmap | Several modules remain vocabulary-only regardless of later examples | Re-evaluate against the frozen current per-module evidence: later examples and CQ11–21 exist, while support remains uneven. Replace obsolete blanket statements with module-specific gaps and keep empirical validation separate. |

The `owl:Thing` to device/asset `uogtox:Thing` equivalence and SOSA's
Sensor-to-ObservableProperty relation versus UOGTO's agent-to-observed-signal/state
relation supply concrete counterexamples to lexical equivalence. Six unresolved
rows remain a review queue. Four accepted structural mappings are evidence about
existing assertions, not a measured gold standard.

## 3. Research questions and study design

**RQ1: What does the resource represent, and where are its source boundaries?**
Chart each retained concept against a primary source, version, exact supporting
construct, UOGTO IRI, scope and disposition. Record conflicts and inaccessible
sources. Report the complete accounted-for discovery register and the explicitly
selected article-analysis corpus separately.

**RQ2: What can its implemented constraints and competency queries detect or
answer?** Report current annotation, scoped constraint, example and exact-answer
coverage, with paired valid/mutated controls. A constraint's failure to detect a
case is a result; it is not repaired silently and then reported as pre-existing
performance.

**RQ3: How much of an independently specified case/concept set is expressible,
queryable and validated?** OCS owns this evaluation. Freeze requirements and cases
before scoring a candidate version; keep development examples separate from
held-out cases. The next resource revision can retain descriptive scope if a
held-out receipt is unavailable, in which case this question remains explicitly
unanswered quantitatively.

**RQ4, conditional: Does a declared finite subset survive an external conversion
or execution?** Include only if qualified independent adapter receipts exist.
Otherwise report supported reference serialization/inspection and list RQ4 as
later work. The future interoperability paper addresses real preservation and
execution; a JSON-LD round trip cannot answer it.

### Source acquisition and comparator strata

Use the [comprehensive sourcing protocol](../research/comprehensive-game-semantics-sourcing-protocol.md)
and [discovery seeds](../research/game-semantics-discovery-seeds-20261108.json).
The [November audit](../research/game-semantics-source-audit-20261108.md) and
[twenty-source register](../research/game-semantics-source-register-20261108.json)
are starting evidence, not a closed universal source list. Integrate the
[bibliography](../research/game-semantics-bibliography-20261108.md), its
[CSL metadata](../research/game-semantics-bibliography-20261108.csl.json), and the
[attribution ledger](../research/game-semantics-attribution-20261108.json) when
those companion artifacts are available.

| Comparator stratum | Initial sources or leads | Permitted comparison |
| --- | --- | --- |
| Strategic-game ontologies | GTO and any verified citation-chain successors | Inspect original formal terms/axioms if acquired; distinguish paper descriptions from retrievable ontology artifacts |
| Videogame/design vocabularies | GOP, VGO, CGO; unresolved GBO remains unresolved | Compare game entities, goals, rules and interaction concepts; avoid equating product/play metadata with strategic semantics |
| Declarative game languages | GDL, separately verified variants, Ludii, VGDL and real-time languages when acquired | Compare representation, information, stochasticity, timing and supported transformations, with exact variants/version provenance |
| Executable game libraries and formalisms | Gambit, OpenSpiel, PettingZoo, PyCID, Open Game Engine; verified newer game-construction/checking work | Extract contracts and semantic distinctions; running them or claiming translation quality requires additional receipts |
| Supporting ontologies and exchange standards | PROV-O, OWL-Time, SSN/SOSA, schema.org, SSSOM and other scoped standards | Compare provenance/time/observation/metadata/exchange roles; never inflate direct strategic-ontology coverage using these counts |

OCS.09–12 own comprehensive discovery/retrieval, source completeness and lineage,
remaining approaches, and consolidated coverage. OCS.02–08 retain predecessor,
concept charting and case-evaluation ownership. Record every in-scope seed as
retrieved, screened, duplicate, excluded, inaccessible, unresolved or pending,
with reasons; follow the protocol's citation chains and search updates to its
explicit stopping rule. An inaccessible item stays in the denominator for source
acquisition, with its unavailable status, rather than disappearing. The analysis
corpus is frozen by eligibility and available evidence, not by ease of achieving a
high coverage score. Full retrieval may remain impossible; a complete accounting
of attempts is different from claiming all sources were obtained.

### Coverage denominators and the two kinds of missingness

A concept can be missing from the **source acquisition/charting evidence**, or it
can be missing from the **ontology's representation/constraints/examples** after a
source was examined. Keep separate fields for both. Unknown acquisition status
cannot be scored as a demonstrated ontology gap or as successful coverage.

Use a versioned matrix with one row per source requirement or case-question pair,
including applicable/not-applicable, evidence available/unavailable, expressible,
queryable, constrained, exemplified, unsupported, and intentionally out-of-scope.
Count unique constructs separately from source occurrences. Report:

- acquisition coverage = acquired eligible artifacts / all eligible artifacts,
  alongside paper-only and inaccessible counts;
- charting coverage = charted accessible constructs / the declared accessible
  construct set, plus uncharted and unknown cells;
- representation coverage = supported applicable requirements / all applicable
  requirements in the frozen evaluated set;
- query and constraint coverage using that same requirement set, rather than the
  number of examples that happen to exist;
- held-out answer accuracy, unsupported-feature detection, mutation sensitivity
  and valid-case false rejection with explicit numerators, denominators and case
  families; report exact descriptive counts for small samples.

Do not subtract the 3,485 historical external term rows from the 561 historical
UOGTO rows to estimate “missing concepts”. Those are corpus rows from different
source roles. Do not combine unknown, excluded, unsupported and pending review
into a single negative-evidence category.

### Current metrics to carry forward with qualifications

The [current quality JSON](../quality/current-semantic-quality.json) is paired with
[its input fingerprint](../quality/current-evidence-manifest.json). Its existing
`created` field still says `2026-06-24`; that builder constant is not the November
execution date. The next frozen manifest must record actual generation time and
revision separately, with a generator-provenance correction or an explicit
explanation. Do not silently overwrite the historical June metrics.

| Metric at the reconciled snapshot | Denominator and interpretation |
| --- | --- |
| 307 classes; 211 properties; 518 labelled and defined entities | Named core/extension terms counted by the builder; not every IRI namespace in every loaded file. Pack namespaces require a separately reported universe. |
| 54 ontology files; eight shape files; 32 explicitly typed node shapes | File and syntactic shape counts. Zero explicitly typed property shapes does not imply absence of property constraints encoded as blank nodes. |
| 27 target classes, of which 23 are within the counted class universe | Report **23/307 = 7.49%** target-class coverage; four pack targets sit outside that universe. Do not use 27/307 or describe those pack terms as absent from all loaded ontology files. |
| 33 property paths | **33/211 = 15.64%** of the counted properties occur as simple shape paths; occurrence is not complete semantic constraint coverage. |
| 30/30 example graphs share a term with shapes | Linked examples, not 100% class, property or module coverage; conformance tests remain distinct. |
| 17/17 module entries with shape links in the present report | The current denominator is already restricted to modules appearing in the link map. It cannot establish complete coverage of the 54 file/module entries. Report a declared full denominator separately. |
| 25 module entries have examples; 15 are mentioned by CQs | These identify uneven support. Pack-only and zero-term modules need scoped counting rather than an unexplained global percentage. |
| 21/21 CQs execute and return results; all have example links | Execution/nonempty results are weaker than correct answer identities. Bind the expectation manifest and exact-answer tests to any correctness claim; curated links are not independent query hits. |
| RDF parse, OWL RL and pySHACL RDFS checks pass in the stored report | Local syntactic profile screen and RL materialization are not formal external OWL DL certification or a proof of game-theoretic/numerical validity. |

### Controls, held-out cases and execution claims

The resource revision should expose the already implemented paired controls for
literal players, negative/above-one/nonfinite probabilities, and permitted numeric
values, plus known bad mapping equivalences and the dynamic-normal-form example.
Bind each claimed control to the actual test and result. An always-rejecting shape
must fail the valid control; a query that returns any row must not pass an
identity-specific expected-answer test.

OCS.07 owns independently specified held-out cases. Proposed strata include a
one-shot simultaneous game, two-stage contingent choice, imperfect-information
tree, chance/stochastic reward case, repeated simultaneous stages, and cooperative
allocation. Publish the case-selection and withholding rule before inspecting
candidate-version scores. Case designers and internal agent reviewers are labelled
accurately; external expert assessment is reported only if actually obtained.
Use paired information-partition/payoff-owner/chance mutations where a scoped
profile supports them, and record unsupported tests instead of expecting the
unrestricted core to reject every partial graph. Keep independently changed
rules separate from harmless IRI renaming or action reordering. Avoid a claim of
generalisation based on six hand-picked development fixtures.

SGC/FRT own player/payoff scope, complete interchange, information leakage,
chance-distribution normalisation and provider dispatch tests. No new adapter
acceptance system is introduced here. An execution claim requires a versioned
external reader/writer or actual library call, captured command/seed/output,
source and fixture hashes, information/payoff preservation checks and unsupported
feature errors. Paignia owns runtime implementation; Kairos is optional for native
simulation and is not a prerequisite for offline solving. The SGC phrase “static semantic acceptance” means offline interchange, not a
`StaticGame` classification. Solver tolerances and empirical payoffs remain
separate assumptions. Absence of a receipt leaves the
claim out of Results.

## 4. Manuscript, supplement and artifact integration

Keep the current narrative sequence, with targeted additions rather than a new
unrelated paper. Introduction gains source-attributed predecessor and comparator
positioning; Results distinguishes historical baseline, corrected reanalysis and
new source charting; Methods states RQs, strata, acquisition/stopping rules,
denominators, controls and actual reviewer roles. Discussion replaces low-count
precision inference with supported limitations and updates module maturity.
Declarations retain human responsibility and explicit AI/tool-use disclosure.

Use the following target display set, reusing existing labels where practical:

| Display | Evidence to freeze and citation relationship |
| --- | --- |
| Existing evidence-strength table, revised | Separate discovery, parsed comparison, constraints, internal review, actual adapters and empirical validation |
| Source/coverage table, new | Stratum; unique source; exact version; evidence/acquisition state; construct denominator; missing/unknown/excluded dispositions; primary citations |
| Existing mapping-summary table, revised | Historical 12/0/448 beside corrected 4/6/450, clearly labelled snapshots of the same retained candidate corpus |
| Existing module-audit summary, revised | Current scope and denominator table above, with per-module supplement and exact-query test receipt |
| Search/mapping flow figure, revised | Distinct source-discovery and mapping stages; six unresolved rows visibly separated from 450 rejected; comparator-union counts recomputed after deduplication |
| Semantic design figure, revised or new | Specification/instance/session/trace; criterion/result/computation; independent strategic timing and representation |
| Existing graph figures and appendices | Regenerate the accepted alignment graph and all dependent node/edge summaries from the same manifest; interpret similarity centrality as exploratory |
| Supplement control/case table, new if results exist | Requirement/case ID, source/version, valid/mutated pair, expected and actual output, unsupported status, reviewer role and result receipt |

Create a claim-evidence ledger joining each C01–C12 and any new claim to the actual
manuscript section, citation key, source locator, artifact/revision/hash, method,
result value/denominator and figure/table ID. A citation must support the adjacent
claim: a standards citation supports representation or validation semantics, not
UOGTO's measured coverage; the original Nash paper does not support an implemented
solver; a metadata landing page does not prove acquired OWL content.

The citation source-of-truth includes `CURATED_REFERENCES` and
`MANUSCRIPT_REFERENCE_IDS` in `build_manuscript_sources.py`, not only the generated
CSL file. The current builder also emits manually selected citation exports and
local verification candidates with a fixed retrieval date. New sources require
verified authorship/year/title/DOI or URL/version/license, real retrieval metadata,
updated source-builder inputs, LaTeX citations and bibliography entries. Recheck
existing entries as well, including reporting-guideline author lists. SourceRight
reconciliation checks citation metadata/keys; source-to-claim support and
attribution require the ledger and primary-source inspection. Re-run generation
in scratch before canonical replacement to detect omissions or silent overwrites.

## 5. Ordered delivery and verification

The [manuscript-integration track](../../conductor/tracks/manuscript_next_version_20261108/index.md)
contains bounded leaves MNV.00–12, each with at most five authored files and
explicit dependencies. Source research stays in OCS, semantic contracts in SGC,
and new library/frontier experiments in FRT. Manuscript integration consumes
receipts and reports unfinished outcomes; it does not claim their completion.
Normal internal review and the existing CI gates are sufficient for reversible
revision work. Scientific external review is evidence if obtained, not a repeated
permission gate for each paragraph.

The plan's completion establishes a reviewable path; it does not establish a new
paper, a new frozen benchmark, a new release or submission. Future implementation
runs the existing commands below at the indicated stage. These commands are
**not reported as executed by this planning document**:

```sh
python scripts/maintenance/build_article_hardening_quality.py --metrics docs/quality/current-semantic-quality.json --report docs/quality/current-semantic-quality.md --check-only
python scripts/maintenance/build_comparison_alignments.py --check-only
python scripts/maintenance/check_ontology_comparison_artifacts.py
python -m pytest tests/test_semantic_hardening.py tests/test_game_temporality.py tests/test_comparison_alignments.py tests/test_runner_execution_origin.py tests/test_competency_query_expectations.py
make manuscript-sources
make manuscript-check
make figure-caption-freeze
make manuscript-sourcecheck
make validate
make test
make manuscript-pdf
make arxiv-upload-ready ARXIV_PDF_FLAGS="--require-pdf --require-arxiv-engine"
python scripts/maintenance/score_arxiv_submission.py --threshold 995 --output .tmp/arxiv-strict-review-report.md --iterations .tmp/arxiv-strict-review-iterations.jsonl --rubric .tmp/arxiv-strict-review-rubric.md
```

Use the existing Required Gate and arXiv Preflight environment for tool-dependent
checks. A missing executable or future test target is pending/unavailable, never a
pass. Tests currently regenerate live article-facing tables; intentional derived
changes must be committed before recording final clean-tree upload provenance.
Keep dated source, calibration and original paper snapshots immutable. Freeze a
new candidate snapshot with a manifest covering inputs, outputs, commands, version
pins, licenses and hashes; use it consistently across prose, tables, figure
captions, supplement, CSL and source package. Record optional renderer failures
rather than claiming a PDF exists because an SVG was written.

The next revision is repository-complete when every retained factual claim has
source/result evidence, counts reconcile within their named snapshots, affected
checks and exact-head CI pass, and the current manuscript PDF/package has been
inspected. Author upload, identifier assignment, external rendered-PDF inspection,
journal decisions and publication remain separately recorded external actions.
