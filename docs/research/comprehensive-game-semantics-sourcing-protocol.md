# Comprehensive sourcing of game-theory ontologies and related approaches

Protocol date: **8 November 2026**. Status: **protocol and seed consolidation
implemented; comprehensive search, acquisition, charting and comparison pending**.
Owner: [source coverage and synthesis](../../conductor/tracks/ontology_coverage_synthesis_20261108/index.md),
with manuscript integration owned by [the next-paper track](../../conductor/tracks/manuscript_next_version_20261108/index.md).

## 1. Objective and meaning of completeness

Identify, attribute, acquire where permitted, and compare **all identifiable
in-scope game-theory ontologies**, together with the related languages, libraries,
modelling standards and research approaches relevant to UOGTO. Build on their
concepts and evidence, recording both agreements and differences. The twenty
sources in the [November audit](game-semantics-source-audit-20261108.md) are a
starting point, not a limit on the search. No source is excluded merely because
it lacks downloadable OWL, is old, uses a different formalism, or overlaps UOGTO.

“All” is the objective of a reproducible census. The defensible completed claim
will be “all identifiable eligible sources found through the reported searches
as of the stated cutoff, with these unresolved and inaccessible records”. An
unindexed, privately held or newly released ontology can escape any search.
Report that limit; do not turn an empty search result into evidence that prior
work does not exist. Maintain a living register after each publication freeze.

The [seed union](game-semantics-discovery-seeds-20261108.json) preserves all **90
input items in 60 records** from the 21-source comparison inventory, 39-source
extension inventory, twenty-source November audit, five interoperability targets
and five research baselines, plus unresolved GBO. Exact source IDs are merged;
ambiguous aliases and aggregate families remain separate. These are register
records, not 60 independent formal ontologies or 60 newly acquired artifacts.
Original records and their historical status remain inspectable.

Use the [bibliography](game-semantics-bibliography-20261108.md),
[CSL records](game-semantics-bibliography-20261108.csl.json) and
[attribution ledger](game-semantics-attribution-20261108.json) alongside the seeds.
A citation identifies a work; it does not demonstrate artifact acquisition,
concept integration, execution or claim support. The historical inventories and
June manuscript remain dated evidence until the next revision deliberately
reconciles them.

## 2. Scope and source strata

| Stratum | Include and discover | Comparison role |
| --- | --- | --- |
| Strategic-game ontologies | General and domain-specific strategic-interaction ontologies; auction, bargaining, negotiation, coalition, voting, mechanism, security, evolutionary and network-game models; Mejbri GTO and citation-chain predecessors/successors | Direct concepts, axioms, assumptions and solution vocabulary; original papers as well as formal artifacts |
| Videogame and game-design vocabularies | GOP, VGO, CGO and additional verified game/player/mechanic vocabularies; resolve GBO only from evidence | Rules, goals, entities, interaction, player roles and gameplay/product metadata; distinguish strategic semantics |
| Declarative game and planning languages | GDL and separately identified variants, Ludii, VGDL/GVGAI, real-time languages, PDDL and other discovered game descriptions | Expressivity, information, chance, timing, transitions, composition and semantics-preserving transformations |
| Executable game and environment libraries | Gambit, OpenSpiel, PettingZoo, PyCID, Open Game Engine, Gymnasium, Mesa and relevant successors; Paignia as the local implementation target | Representation/API contracts, solver assumptions, observations, rewards, lifecycle and execution evidence |
| Supporting modelling and exchange approaches | Existing simulation, systems, agent, process and upper-ontology inventories: DEVS, HLA/FOM, FMI, Modelica, ODD, BPMN, SysML, PNML, XMILE, CellML, SBML, SED-ML, SBGN, KiSAO, SBO, MIASE, EMMO/VIMMP/OSMO, BFO, DOLCE, OntoUML/UFO, KAOS, OWL-S, P-Plan, PROV-O, OWL-Time, SSN/SOSA and schema.org; SSSOM, OAEI and ROBOT as methods/tooling | Assess reusable provenance, temporal, observation, process, model and exchange concepts; retain relevant comparators without counting them as strategic-game ontologies |
| Research baselines and environments | Compositional games, MAID refinements, causal games, GameInterpreter and consistency checking; DeepGTAV and other scoped game environments | Compare actual claimed methods and bounded strategic abstractions; do not infer capability from a name or screen activity |

Paper-only conceptual models, theses, archived projects, non-English work and
historical versions are eligible evidence. Record the format and limits. A title
or acronym without an identifiable work remains an unresolved lead. Pure game
asset catalogues, unrelated uses of “game”, and generic ontology tooling without
a relevant comparison role receive explicit exclusion reasons, not silent removal.

Keep source family, individual publication, ontology release, software version and
retrieved file as different entities. For example, a combined GDL-II/III/GDLZ record
does not establish that each variant was studied; a paper describing GTO does not
prove that its formal release is available. Resolve GDL/Gamelan and VGDL/GVGAI
aliases with primary evidence before merging identities. Preserve supersession,
forks and version relationships rather than deduplicating them out of existence.

## 3. Search routes and reproducible records

The following are **planned search routes**, not a log of searches already run.
Use the available official interfaces and record access limits. A planned query
must not become an executed record without a result or an explicit failed attempt.

1. **Scholarly discovery:** Crossref, OpenAlex, Semantic Scholar, DBLP, arXiv,
   publisher proceedings and relevant ACM/IEEE/AAAI/DiGRA collections; Scopus or
   Web of Science only where access exists. Search title/abstract/keywords and
   full text where permitted. Preserve query syntax, filters, pagination and
   database/API version when available.
2. **Ontology and vocabulary registries:** LOV, OLS, Ontobee, BioPortal,
   Bioregistry, FAIRsharing, Wikidata and other relevant registries or archives.
   A registry hit is discovery evidence, not evidence of conceptual completeness
   or a recommendation to import its entire ontology.
3. **Primary artifact discovery:** author/institutional pages, GitHub, GitLab,
   Zenodo, Figshare and standards/project repositories, including W3C, OASIS,
   COMBINE, SISO and EMMC where relevant. Inspect releases, ontology IRIs,
   imports, citation files and documentation; pin revisions for acquired content.
4. **Citation and implementation chaining:** backward and forward citations from
   every included direct strategic ontology, systematic reviews and major language
   or library papers; follow referenced formalisms, imported ontologies, successor
   releases and implementation links. Record the referring source and edge type.
5. **Terminology expansion:** search verified names, acronyms, spelling variants,
   translations and author/project combinations. Record newly discovered terms
   and rerun the relevant routes. Treat ambiguous names as unresolved until the
   primary source establishes identity.

Starting query families, to adapt explicitly to each service:

- `("game theory" OR "game-theoretic" OR "strategic interaction") AND
  (ontology OR ontologies OR vocabulary OR "conceptual model" OR "knowledge graph")`.
- `(game OR games) AND (OWL OR RDF OR WSML OR OntoUML OR "formal ontology")`.
- `(auction OR bargaining OR negotiation OR coalition OR "social choice" OR
  "mechanism design" OR "security game" OR "stochastic game" OR "evolutionary game")
  AND (ontology OR vocabulary OR "conceptual model")`.
- `("game description language" OR "game semantics" OR "game representation")
  AND (information OR stochastic OR temporal OR composition OR interchange)`.
- Each known source name, its publication title and verified author names,
  followed by citation and implementation searches.

No default publication-year or language restriction applies. If a service requires
limits, export in documented partitions. Record translation and full-text access
limits. General search engines can supply leads, but technical attribution and
substantive concept claims must resolve to primary papers, specifications, author
artifacts or official code/documentation.

Each future search record must contain: stable search ID; exact query and service;
UTC execution time and cutoff; filters, pages/cursors and returned count; raw
export path/hash where permitted; deduplication rules; newly discovered IDs;
errors or unavailable routes; and the person/tool performing the search. Store
raw results and screened decisions separately. Never reconstruct a missing count
from memory or call an inaccessible database searched successfully.

## 4. Screening, acquisition and practical stopping rule

Screen each unique candidate for a stated stratum and relevance question. Record
included, excluded-with-reason, duplicate/alias, unresolved-identity or
awaiting-full-text outcomes. Preserve the original record and duplicate linkage.
Two names are not the same ontology merely because their abbreviations overlap.

For each included source attempt to locate the original scholarly description,
current or historically relevant formal artifact, official implementation and
license as applicable. Record successful acquisition separately for each item,
with URL, timestamp, version/commit, media type, SHA-256 and local permitted copy
or reproducible retrieval instruction. Record dead links, paywalls, author-only
availability and unknown redistribution terms without inventing an artifact.
Do not contact authors or maintainers without the user's separate authorization.

The comprehensive search closes a publication snapshot only when:

- Every declared seed has a screened disposition and citation or an explicit
  unresolved attribution exception; every planned route has an execution result
  or documented access limitation.
- Included direct strategic ontologies have completed backward/forward citation
  checks to the stated cutoff. New eligible records re-enter screening and
  chaining. Apply the same process to relevant related-approach families.
- Two consecutive documented citation/terminology expansion rounds yield no new
  eligible unique records within the declared routes. This is an operational
  stopping rule, not proof that the world's literature is exhausted.
- Every included record has an acquisition outcome and unresolved gaps are
  published, including aggregate families whose members remain unidentified.
- Search reruns immediately before the manuscript freeze record new additions or
  an unchanged result. The paper reports the actual cutoff and any inaccessible
  surfaces, rather than using the protocol date as the search date.

A bounded interim paper may be written before this full programme is complete,
but it must explicitly use the narrower searched corpus and retain the unanswered
coverage question. Completing this protocol or registering a task does not close
these conditions.

## 5. Attribution, citation and reuse contract

Every named source in the discovery register must resolve to one or more stable
bibliographic IDs or an explicit unresolved-identity record. Supply both the
original scholarly description and versioned software/specification citation
when they support different claims. A project homepage alone is an honest initial
citation, but not a substitute for locating its authors and original paper.
Include citation files requested by source maintainers where applicable.

Use only corroborated authors, titles, dates, DOI/arXiv identifiers, venue,
version, pages and URLs. Leave unknown fields absent and queue them for review.
Do not invent authors for standards, infer a release date from an access date,
copy a partial author list as complete, or conflate a preprint with its later
journal version. Preserve conflicting observations and their source locators.

For each reused concept or comparison claim record:

| Field group | Required evidence |
| --- | --- |
| Source identity | Source ID; bibliographic ID; specific artifact/revision; authoritative URL; acquisition state |
| Supporting content | Exact section/page/IRI/API symbol or code location; short permitted excerpt or faithful paraphrase; evidence hash when acquired |
| Attribution and rights | Creator/maintainer where verified; license and attribution requirement for each paper, ontology, code, documentation or dataset; unknown terms remain unknown |
| UOGTO disposition | Target IRI or module; adopted/adapted/mapped/compared/deferred/excluded; rationale; differences and conflicting definitions |
| Meaning and validation | Scope assumptions; mapping relation; competency question; positive example; relevant negative control or execution obligation |
| Claim linkage | Manuscript/roadmap claim ID and location; supporting references; support status and reviewer provenance |

Conceptual comparison with citation does not automatically authorize copying
code, redistributing an ontology or bundling commercial game assets. Verify
artifact-specific terms before import or reuse; keep attribution notices with
borrowed material. An unknown license is a recorded acquisition/reuse limitation,
not a reason to erase relevant prior work from the comparison.

Citation verification is progressive: extracted metadata, structural validity,
internal consistency, provider corroboration, source resolution, content checking,
and claim-support appraisal are distinct outcomes. Record the strongest level
actually achieved for each reference. SourceRight CSL validation checks structure;
it cannot certify that a paper supports a claim or that a homepage was read.
Run reference-ID and source-ID coverage checks in addition to the validator.
A green check on those structures must not relabel inherited metadata as verified
full text. Preserve the next-paper bibliography separately until a deliberate
manuscript citation migration updates the canonical generator and its tests.

## 6. Concept extraction and fair comparison

Chart constructs before creating new classes. At minimum compare:

- Agents, player roles, identity, specifications, instances, sessions and traces.
- Local actions, complete contingent strategies, mixed and behavioural strategies,
  policies, joint actions, legal actions and strategy domains.
- States, histories, information sets, observations, beliefs, perfect recall,
  chance support/probabilities and causal versus informational dependence.
- Static/dynamic strategic structure, normal/extensive representations, repeated
  and stochastic interaction, physical time and software scheduling separately.
- Payoffs, utility, immediate reward, accumulated return, discount, horizon,
  termination/truncation, outcomes, allocations and ownership.
- Solution concepts, candidate solutions, refinements, solver/computation records,
  assumptions, tolerance, regret and exploitability diagnostics.
- Coalition/cooperation, bargaining, mechanisms, voting and institutions;
  population/network/learning dynamics; composition and interventions.
- Provenance, versions, experiment configuration, reproducibility and execution
  bindings needed to interpret a claimed result.

Prioritise Gambit and OpenSpiel with small construct-level crosswalks, followed
by PettingZoo, PyCID and Open Game Engine. Extend to the remaining seed families
and newly discovered sources. Do not convert every API method into an ontology
class or add an upper ontology simply to increase term counts. Record a principled
“compared, no adoption needed” outcome when a concept is already adequately
represented or lies outside scope. Use SSSOM-style explicit mapping metadata
where appropriate; equivalence requires semantic justification, not lexical
similarity. The [SSSOM paper](https://doi.org/10.1093/database/baac035) is a methods
reference, not evidence that any proposed UOGTO mapping is correct.

Keep two missingness axes. **Evidence availability** records whether the source
was retrieved and examined. **Representational support** records whether the
examined source or UOGTO implements a feature. “Not examined” cannot become
“unsupported”, and an intended class label cannot become “validated”. Use
separate states for documented, represented, constrained, queried and executed.
Publish conflicts and irreducible translation loss.

For meaningful comparison use matched small cases: matrix games; finite sequential
games; chance and imperfect-information games; repeated simultaneous games;
cooperative allocation/bargaining or mechanism examples where supported. Include
player/action relabelling, asymmetric payoffs, illegal actions, information leakage,
probability and payoff-owner mutations. State source-specific supported subsets
and do not penalize a deliberately narrow vocabulary for unrelated features.

Report source, concept and case denominators separately: identified/screened/
eligible/acquired/charted sources; examined constructs with lineage; questions
expressible/queryable/validated; detected versus missed semantic mutations and
false rejection. Counts of names, triples or accepted mappings do not alone
measure quality. Freeze independently specified held-out requirements before
scoring; label coding-agent review as internal. Reviewer agreement requires
actual reviewer observations and a nonempty sample.

A claim about library interchange or solver execution requires a real run of the
pinned external implementation, with inputs, outputs, assumptions and failure
modes. Local RDF fixtures and structural round trips support their narrower
claims. UOGTO owns semantics; Paignia owns algorithms/runtime/adapters; Kairos
remains optional simulation. This source programme does not duplicate their work.

## 7. Deliverables, ownership and next paper

| Leaf | Outcome and concrete evidence |
| --- | --- |
| OCS.01 — completed historical audit | Preserve the twenty-source November register and bounded findings |
| OCS.02–05 — pending | Acquire/chart direct predecessors, videogame/language sources, Gambit and OpenSpiel/PettingZoo concepts |
| OCS.06–07 — pending | Source-to-concept lineage and independently specified case/coverage evaluation |
| OCS.08 — pending | Publish a reproducible coverage study with actual denominators; supply evidence to manuscript integration |
| OCS.09 — pending | Execute comprehensive discovery and retrieval; publish query logs, screened corpus, alias decisions and acquisition gaps |
| OCS.10 — pending | Complete per-source citations/rights and source-to-concept/claim support appraisal; all unresolved items visible |
| OCS.11 — pending | Chart remaining libraries, formalisms, modelling standards and research baselines; compare and justify adoption or exclusion |
| OCS.12 — pending | Consolidate the expanded comparison and coverage evidence; distinguish evidence gaps from semantic gaps |
| MNV.00 — completed planning | Deliver the [next-version manuscript plan](../paper/next-version-plan-20261108.md) |
| MNV.01–12 — pending | Integrate only supported findings into the existing paper, regenerate the chosen snapshot and check citation/claim consistency |

OCS.09 and OCS.10 can start immediately from the delivered seed and attribution
infrastructure. Existing OCS acquisition leaves need not wait for every database
to finish. The new MNV track consumes source and validation receipts rather than
repeating OCS/SGC/FRT implementation. Later interoperability and frontier studies
retain their separate hypotheses and evidence requirements.

The next paper must explain what changed from the historical manuscript: the
expanded and attributed comparator corpus, corrected mapping decisions and
semantics, explicit static/dynamic distinctions, current validation scope and
remaining gaps. Keep old and new denominators separate. Correct the historical
inference that no additional ontology was found, and avoid claiming the full
comprehensive programme complete if its execution is still pending.

## Methodological references and limits

Search reporting should use the applicable items from
[PRISMA-S](https://doi.org/10.5195/jmla.2021.962) and
[PRISMA-ScR](https://doi.org/10.7326/M18-0850), recording what was actually done.
Citing these reporting guidelines does not make an unexecuted protocol a completed
systematic review. Original source attribution is maintained in the linked
bibliography and ledger; historical manuscript references are reconciled during
MNV.03 rather than silently recertified here.
