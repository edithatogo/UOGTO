# Article-Hardening Research Workflow

## Purpose
Research work for `uogto_article_hardening_protocol_20260624` must be explicit, assigned, and traceable before it becomes article evidence. This workflow complements the phase-review workflow by defining researcher roles before peer, editorial, red-team, and devil's-advocate review.

## Required Research Agents
The research-agent registry is `conductor/agents/article-hardening-research-agents.json`.

Minimum research set for every phase:

- `evidence_curation_researcher`
- `reproducibility_curator`

Additional phase-specific researchers:

- `registry_discovery_researcher` for source-discovery and acquisition phases.
- `standards_landscape_researcher` for standards, formal-language, and structured non-RDF phases.
- `game_theory_gap_researcher` for competency, mapping, UOGTO inclusion, and article-output phases.

## Research Steps
1. Identify phase scope, acceptance criteria, and output artifacts.
2. Assign minimum and phase-specific research roles.
3. Record source-search, evidence-curation, or reproducibility work in `docs/article-hardening/research/phase-research-log.jsonl`.
4. Produce role-specific notes under `docs/article-hardening/research/`.
5. Link each candidate claim to a source, evidence level, and artifact path.
6. Pass research outputs to the review workflow for peer, editorial, red-team, and devil's-advocate review.

## Researcher Outputs
Each researcher note must include:

- phase number and title
- researcher id
- research question or evidence task
- searched or inspected sources
- evidence level and limitations
- outputs updated
- unresolved gaps
- handoff notes for reviewers

## Reporting Rules
- Research notes must distinguish search failure from absence of evidence.
- Standards and structured non-RDF sources must not be described as OWL ontologies unless transformed or parsed as such.
- Metadata-only evidence can support discovery and context claims, but not term-level mapping claims.
- Reproducibility notes must record the validator, focused tests, and `make validate` evidence used for the phase.
