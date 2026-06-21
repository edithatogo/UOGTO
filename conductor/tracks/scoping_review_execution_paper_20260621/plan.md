# Implementation Plan: Scoping Review Execution and arXiv Manuscript

This plan outlines deduplication, classification, and drafting of the UOGTO scoping paper.

## Phase 1: Deduplication & Screening Setup
- [x] Task: Execute Deduplication Script
    - [x] Implement `scripts/review/deduplicate.py`
    - [x] Run deduplication over raw search downloads
- [x] Task: Implement Active Learning and Snowballing
    - [x] Create `scripts/review/active_screening.py` and run screening loop
    - [x] Build snowballing scraper `scripts/review/snowball.py` to fetch cited references

## Phase 2: Math Parsing & Graph Alignments
- [ ] Task: Build Multi-Format Math Parser & OCR
    - [ ] Create math extractor `scripts/review/parse_math.py` supporting LaTeX, MathML, Quarto, and Typst
    - [ ] Scaffold OCR matrix extractor `scripts/review/parse_table_ocr.py`
- [ ] Task: Create L2O Graph and Verify Gaps
    - [ ] Build literature graph compiler
    - [ ] Run RDF mapping check `scripts/review/verify_ontology_coverage.py` and output validation gaps

## Phase 3: Patches and Paper Writing
- [ ] Task: Scaffold RDF Patch Generator
    - [ ] Create patch builder `scripts/review/generate_rdf_patch.py` and update UOGTO classes
- [ ] Task: Write and Compile arXiv Paper
    - [ ] Draft LaTeX article source at `docs/paper/paper.tex` mapping review protocol, results, and ontology specification
    - [ ] Verify PDF compilation succeeds locally
