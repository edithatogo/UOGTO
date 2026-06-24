---
name: article-hardening-research
description: Coordinates researcher agents for UOGTO article-hardening source discovery, standards review, evidence curation, gap analysis, and reproducibility.
---

# Article Hardening Research Skill

Use this skill when implementing research-heavy phases of `uogto_article_hardening_protocol_20260624`.

## Research Inputs
- Track plan: `conductor/tracks/uogto_article_hardening_protocol_20260624/plan.md`
- Research-agent registry: `conductor/agents/article-hardening-research-agents.json`
- Research workflow: `conductor/workflows/article-hardening-research-workflow.md`
- Review workflow: `conductor/workflows/article-hardening-phase-review.md`
- Protocol/search artifacts: `docs/article-hardening/`

## Required Research Roles
For every phase, assign:

1. `evidence_curation_researcher`
2. `reproducibility_curator`

For discovery and acquisition phases, also assign:

3. `registry_discovery_researcher`
4. `standards_landscape_researcher`

For competency, mapping, UOGTO-inclusion, and article-output phases, also assign:

5. `game_theory_gap_researcher`

## Research Procedure
1. Identify the phase and artifacts under development.
2. Assign the required research roles before review roles.
3. Record source searches, evidence decisions, reproducibility checks, and unresolved gaps in `docs/article-hardening/research/phase-research-log.jsonl`.
4. Produce role-specific research notes under `docs/article-hardening/research/`.
5. Pass the research handoff to the article-hardening review workflow.
6. Ensure every article-facing claim has an evidence level, source reference, and artifact path.

## Output Standard
Research notes should be concise, source-backed, and explicit about search limits, evidence level, source licence/provenance, and implications for article claims.
