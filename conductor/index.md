# UOGTO Conductor Context

This directory is the local source of truth for UOGTO planning, track history,
implementation evidence, and GitHub project synchronization.

## Core Context

- [Product Definition](./product.md)
- [Product Guidelines](./product-guidelines.md)
- [Tech Stack](./tech-stack.md)
- [Workflow](./workflow.md)
- [Tracks Registry](./tracks.md)
- [Conductor Status](./status.md)
- [Run Log](./runlog.md)
- [Remote Status](./remote_status.md)

## Track Ledgers

- [Active and historical tracks](./tracks.md)
- [Archived tracks index](./archive/index.md)
- [Active track directory](./tracks/)
- [Archived track directory](./archive/)

## Current semantic and research programme

- [Executable subset and semantic identity](./tracks/semantic_game_contracts_20261107/index.md)
- [Current semantic reconciliation](./tracks/semantic_reconciliation_20261108/index.md)
- [Source coverage and synthesis](./tracks/ontology_coverage_synthesis_20261108/index.md)
- [Repository maturity](./tracks/repository_maturity_20261108/index.md)
- [Interoperability and frontier research](./tracks/semantic_interoperability_frontier_20261108/index.md)
- [Video-game environment profiles](./tracks/video_game_environment_profiles_20261108/index.md)
- [Programme, baselines and acceptance evidence](../docs/roadmap/frontier-programme-20261108.md)

## Operating Notes

- `conductor/tracks.md` is the readable registry for all active, completed, and
  archived tracks.
- `conductor/archive/index.md` is the audit ledger for tracks that no longer
  require repo-local implementation work.
- GitHub Projects mirror the track ledger at issue level, but local Conductor
  files remain the detailed specification, plan, and evidence source of truth.
- `scripts/conductor.py` reads the active canonical registry and labels the older
  `.conductor/tasks.yaml` phases as historical. Completed bootstrap phases do not
  imply the newly registered programme is complete. Project-board synchronisation
  is a separate operation; no new remote board state is asserted by these files.
