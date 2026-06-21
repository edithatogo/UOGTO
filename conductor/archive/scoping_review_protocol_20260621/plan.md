# Implementation Plan: Scoping Review Protocol Development

This plan outlines the steps for establishing protocols and search clients.

## Phase 1: Methodology & Checklists
- [x] Task: Formulate PRISMA-P Protocol
    - [x] Create `docs/review/protocol.md` defining scoping questions and inclusion/exclusion rules
- [x] Task: Formulate PRISMA-S Search Protocol
    - [x] Add search terms and database strings to the protocol file

## Phase 2: Scaffolding API Clients
- [x] Task: Build Multi-Database Search Client
    - [x] Implement query scripts in `scripts/review/query_databases.py` for PubMed, Europe PMC, Crossref, arXiv, and OpenAlex
    - [x] Verify query client connectivity and save format

## Phase 3: Validation and Baseline Runs
- [x] Task: Perform Dry-Run Queries
    - [x] Run test queries to estimate data size and log raw statistics
