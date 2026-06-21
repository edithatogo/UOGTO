# Implementation Plan: Systematic Scoping Literature Review

This plan details the phases for building, executing, and documenting the literature review pipeline.

## Phase 1: Review Protocol & Database APIs
- [ ] Task: Create PRISMA scoping review protocol
    - [ ] Author `docs/review/protocol.md` defining eligibility, search terms, and screening criteria
- [ ] Task: Build API Search Client
    - [ ] Implement search scripts in `scripts/review/query_databases.py` targeting OpenAlex, PubMed, Europe PMC, arXiv, and Crossref
    - [ ] Save query responses to `data/raw/` with query metadata
- [ ] Task: Design Literature-to-Ontology (L2O) Schema
    - [ ] Define dynamic RDF schema mapping papers, metadata, and game variables to temporary graphs

## Phase 2: Deduplication & NLP Filtering
- [ ] Task: Implement deduplication scripts
    - [ ] Create `scripts/review/deduplicate.py` matching DOIs, titles, and authors
- [ ] Task: Implement NLP Game theory extraction
    - [ ] Create `scripts/review/extract_concepts.py` utilizing text classification/embeddings to identify game definitions, matrices, and variables
    - [ ] Implement semantic embedding clustering (sentence-transformers) to group abstracts
- [ ] Task: Build Active Learning and LaTeX parsing utilities
    - [ ] Implement active learning loop (`scripts/review/active_screening.py`) to rank abstracts based on eligibility choices
    - [ ] Implement `scripts/review/parse_math.py` to extract LaTeX equation strings from text

## Phase 3: Triangulation & UOGTO Mappings
- [ ] Task: Formulate formula triangulation script
    - [ ] Parse extracted math representations and verify properties
- [ ] Task: Generate UOGTO coverage reports
    - [ ] Compile L2O Graph representing extracted literature
    - [ ] Run SPARQL coverage query checks (`scripts/review/verify_ontology_coverage.py`) aligning L2O and UOGTO, outputting gaps
