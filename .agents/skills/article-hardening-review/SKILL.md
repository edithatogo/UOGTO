---
name: article-hardening-review
description: Coordinates peer, editorial, red-team, and devil's-advocate reviews for UOGTO article-hardening phases.
---

# Article Hardening Review Skill

Use this skill when implementing or reviewing `uogto_article_hardening_protocol_20260624`.

## Review Inputs
- Track plan: `conductor/tracks/uogto_article_hardening_protocol_20260624/plan.md`
- Agent registry: `conductor/agents/article-hardening-review-agents.json`
- Review workflow: `conductor/workflows/article-hardening-phase-review.md`
- Protocol artifacts: `docs/article-hardening/`

## Required Review Roles
For each phase, assign:

1. `ontology_peer_reviewer`
2. `methods_editor`
3. `evidence_red_team`
4. `devils_advocate_reviewer`

For phases 2 through 8, also assign:

5. `simulation_modelling_peer_reviewer`

## Review Procedure
1. Identify the phase and artifacts under review.
2. Read the acceptance criteria and the relevant generated artifacts.
3. Produce reviewer notes under `docs/article-hardening/reviews/`.
4. Record reviewer assignments and outcomes in `docs/article-hardening/reviews/phase-review-log.jsonl`.
5. Classify findings as `fix_now`, `defer`, `reject`, `needs_user_input`, or `external_blocker`.
6. Apply in-scope fixes before marking a phase complete.
7. Run `make article-hardening-protocol`, focused tests, and `make validate`.

## Output Standard
Reviewer notes should be concise, evidence-backed, and explicit about whether a finding affects article wording, source eligibility, UOGTO inclusion, mapping confidence, reproducibility, or validation.
