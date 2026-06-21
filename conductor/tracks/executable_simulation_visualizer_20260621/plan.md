# Implementation Plan: Executable Simulation Runner and Interactive Playground

This plan outlines the deployment of runtimes, interactive playgrounds, and LLM player hooks.

## Phase 1: Executable Simulation Engine
- [x] Task: Develop RDF Game Runner
    - [x] Create `uogto/runner/engine.py` to parse game structures, payoffs, and strategies from RDF graphs
    - [x] Write execution loops outputting transition traces as event graphs
- [x] Task: Build execution unit tests
    - [x] Verify runner matches classical game outcomes (e.g., Prisoner's Dilemma payoffs)

## Phase 2: Interactive Web Visualizer
- [ ] Task: Create Streamlit Dashboard
    - [ ] Implement `uogto/playground/app.py` supporting Turtle file upload and SHACL validator checks
    - [ ] Integrate graph layout libraries (e.g., NetworkX, pyvis) to render states and node graphs

## Phase 3: LLM Player Benchmarking
- [ ] Task: Build LLM Agent Player Harness
    - [ ] Create API connectors querying LLM agents for choices in simulated UOGTO games
    - [ ] Record game traces and verify behavioral metrics
