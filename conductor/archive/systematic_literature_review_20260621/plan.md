# Implementation Plan: Systematic Scoping Literature Review

This plan details the phases for building, executing, and documenting the literature review pipeline.

## Phase 1: Review Protocol & Database APIs
- [x] Task: Create PRISMA scoping review protocol
    - [x] Author `docs/review/protocol.md` defining eligibility, search terms, and screening criteria
- [x] Task: Build API Search Client
    - [x] Implement search scripts in `scripts/review/query_databases.py` targeting OpenAlex, PubMed, Europe PMC, arXiv, and Crossref
    - [x] Save query responses to `data/raw/` with query metadata
- [x] Task: Design Literature-to-Ontology (L2O) Schema
    - [x] Define dynamic RDF schema mapping papers, metadata, and game variables to temporary graphs

## Phase 2: Deduplication & NLP Filtering
- [x] Task: Implement deduplication scripts
    - [x] Create `scripts/review/deduplicate.py` matching DOIs, titles, and authors
- [x] Task: Implement NLP Game theory extraction
    - [x] Implement semantic classification to group abstracts by game-theory categories
    - [x] Create temporal semantic drift calibrator to adjust historical era classifications
- [x] Task: Build Active Learning, Snowballing, and Equation Parsing Utilities
    - [x] Implement active learning loop (`scripts/review/active_screening.py`) to rank abstracts based on eligibility choices
    - [x] Implement `scripts/review/parse_math.py` to extract LaTeX, MathML, Quarto, and Typst equation strings from text
    - [x] Implement `scripts/review/snowball.py` to execute citation network snowballing via OpenAlex
    - [x] Implement table extraction and visual OCR (`scripts/review/parse_table_ocr.py`) to parse visual payoff grids from PDFs

## Phase 3: Triangulation & UOGTO Mappings
- [x] Task: Formulate formula triangulation script
    - [x] Parse extracted math representations (LaTeX, MathML, Typst, Quarto) and verify properties
    - [x] Map literature nodes to UOGTO ontology coverage checks
- [x] Task: Generate UOGTO coverage reports & RDF patches
    - [x] Compile L2O Graph representing extracted literature
    - [x] Run SPARQL coverage query checks (`scripts/review/verify_ontology_coverage.py`) aligning L2O and UOGTO, outputting gaps
    - [x] Implement RDF patch generator (`scripts/review/generate_rdf_patch.py`) to draft Turtle (.ttl) files for identified gaps
    - [x] Cover literature-review scripts in CI through the repository validation and pytest workflow
