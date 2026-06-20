# CONDUCTOR.md

## Overview
This repository uses the Conductor system to drive development. It structures the process into sequential phases and automates checking project health.

## Development Phases
- `phase_00_bootstrap`: Repository layout, base scripts, tests, workflows.
- `phase_01_core_ontology`: Core game ontology properties and classes.
- `phase_02_classical_and_cooperative_games`: Core extensions for classical and cooperative games.
- `phase_03_information_and_epistemic_games`: Games with incomplete information and epistemic structures.
- `phase_04_dynamics_simulation_and_execution`: Event traces, transitions, and simulations.
- `phase_05_mechanism_design_social_choice_and_allocation`: Auctions, stable matchings, and social choice.
- `phase_06_learning_marl_and_evolution`: Policies, reinforcement learning, replicator dynamics.
- `phase_07_network_mean_field_and_continuous_games`: Large populations and spatial networks.
- `phase_08_norms_contracts_institutions_and_deontic_logic`: Contracts, sanctions, and institutional rules.
- `phase_09_llm_agents_digital_twins_and_protocols`: Interactive agents and cyber-physical twin integrations.
- `phase_10_validation_examples_docs_release`: Final build consolidation, full SHACL coverage, release artifacts.

## Operations
Run these commands from the repository root:
- Install dependencies: `make install`
- Build the final ontology assets: `make build` (Generates files in `dist/`)
- Run ontology/syntax validation: `make validate`
- Run test suites: `make test`
- Print ontology coverage: `make coverage`
- Check task status: `make conductor`

## Adding a New Module
1. Check `.conductor/module-template.md`.
2. Create the ontology file under `ontologies/`.
3. Create corresponding SHACL shapes under `shapes/`.
4. Create context mappings under `jsonld/`.
5. Add an example in `examples/`.
6. Document in `docs/` and add competency queries in `competency-questions/`.
7. Update task status in `.conductor/tasks.yaml`.
