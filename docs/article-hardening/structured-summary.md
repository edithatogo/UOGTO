# PRISMA-ScR Structured Summary

## Title
UOGTO Article-Hardening Protocol and Evidence Package

## Background
This protocol packages the comparative ontology-mapping work on UOGTO as a scoping-review-style evidence set. The goal is to document what simulation and game-theory ontologies exist, how they relate to UOGTO, what evidence is strong enough to support inclusion or external alignment, and where the current repository still needs judgment, triangulation, or follow-up.

## Objectives
1. Discover and classify relevant ontologies, formalisms, standards, repositories, and source families.
2. Preserve the discovery trail as append-only evidence surfaces.
3. Map source overlap, coverage, quality, and missing-element triage outcomes.
4. Produce article-ready summary, table, figure, and review artifacts.

## Eligibility and Sources
The package includes parsed RDF/OWL sources, structured non-RDF sources, metadata-only records, literature-only evidence, registry entries, standards-body documents, and explicit negative-evidence searches. Inclusion and exclusion decisions are documented in the source inventory, search log, and inclusion-decision files.

## Search and Charting
Search routes and query families are defined in `docs/article-hardening/search-strategy.md`. Each search route is logged in `docs/article-hardening/search-log.jsonl` with result count, evidence level, inclusion rationale, licence, reviewer handoff, and screening decision. Charting fields are carried through the source inventory and quality-metric artifacts so the final article can separate discovery counts from validated mapping evidence.

## Synthesis
The package synthesises source discovery, evidence levels, mapping overlap, ontology-quality benchmarking, reviewer calibration, case studies, and missing-element triage. ROBOT-style outputs are retained as optional enrichment while RDFLib and pySHACL remain the portable baseline.

## Evidence Package Surfaces
- `docs/article-hardening/protocol.md`
- `docs/article-hardening/protocol-checklist.md`
- `docs/article-hardening/prisma-scr-artifact-map.md`
- `docs/article-hardening/search-strategy.md`
- `docs/article-hardening/search-log.jsonl`
- `docs/article-hardening/source-extension-inventory.json`
- `docs/article-hardening/source-extension-inventory.md`
- `docs/article-hardening/quality-metrics.json`
- `docs/article-hardening/reasoner-report.md`
- `docs/article-hardening/case-studies.md`
- `docs/article-hardening/ro-crate-metadata.json`

## Negative Evidence
Searches that return no relevant ontology or formalism are recorded as negative evidence rather than treated as proof of universal absence. This preserves transparency about what was searched and what was not found.