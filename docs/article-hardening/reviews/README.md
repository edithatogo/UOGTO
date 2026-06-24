# Article-Hardening Reviews

This directory stores phase-level review outputs for `uogto_article_hardening_protocol_20260624`.

Required review roles are declared in `conductor/agents/article-hardening-review-agents.json`.

Review workflow:

1. Assign required reviewers for the phase.
2. Write reviewer notes using the role-specific output paths.
3. Record review events in `phase-review-log.jsonl`.
4. Resolve or explicitly defer findings before phase completion.

The review log is append-only. Do not remove historical review entries; add superseding entries when a review outcome changes.
