# Implementation Plan: Systematic Scoping Literature Review

This plan details the phases for building, executing, and documenting the literature review pipeline.

## Phase 1: Review Protocol & Database APIs
- [ ] Task: Create PRISMA scoping review protocol
    - [ ] Author `docs/review/protocol.md` defining eligibility, search terms, and screening criteria
- [ ] Task: Build API Search Client
    - [ ] Implement search scripts in `scripts/review/query_databases.py` targeting OpenAlex, PubMed, Europe PMC, arXiv, and Crossref
    - [ ] Save query responses to `data/raw/` with query metadata

## Phase 2: Deduplication & NLP Filtering
- [ ] Task: Implement deduplication scripts
    - [ ] Create `scripts/review/deduplicate.py` matching DOIs, titles, and authors
- [ ] Task: Implement NLP Game theory extraction
    - [ ] Create `scripts/review/extract_concepts.py` utilizing text classification/embeddings to identify game definitions, matrices, and variables

## Phase 3: Triangulation & UOGTO Mappings
- [ ] Task: Formulate formula triangulation script
    - [ ] Parse extracted math representations and verify properties
- [ ] Task: Generate UOGTO coverage reports
    - [ ] Create `scripts/review/verify_ontology_coverage.py` mapping literary game definitions to UOGTO classes and outputting gaps
