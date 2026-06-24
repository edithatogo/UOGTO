# Term Deprecation Policy

This policy governs term-level changes in UOGTO and the article-hardening workflow.

## Event Types

- `new term`: a new class, property, individual, or controlled term is introduced.
- `changed definition`: the term IRI remains stable, but the meaning or scope text changes.
- `deprecated term`: the term remains readable for backward compatibility, but is no longer the preferred form.
- `replacement IRI`: a newer term IRI supersedes an older one.
- `migration note`: a short note explaining how downstream consumers should move from the old form to the new form.

## Required Rules

1. Every deprecated term must name a replacement IRI when a replacement exists.
2. Every changed definition must record the reason for the change and whether the semantic scope narrowed, widened, or was clarified.
3. Every new term must state whether it is canonical in UOGTO or align-only for external mapping.
4. Every migration note must be actionable for example data, SHACL validation, and downstream mappings.
5. Deprecated terms should remain resolvable long enough for migrations to complete, but new examples should use the replacement form.

## Minimal Record

Each changelog entry should include:

- term label
- term IRI
- event type
- old definition, if any
- new definition, if any
- replacement IRI, if any
- migration note
- rationale
- source or reviewer reference

## Review Standard

- Do not deprecate a term merely because a synonym exists.
- Prefer deprecation only when the current term is ambiguous, misleading, duplicated, or structurally inconsistent.
- If the correct replacement is not yet stable, mark the term as deferred rather than deprecated.
- If a term should not be retained in UOGTO at all, record the disposition separately from deprecation so scope decisions remain explicit.

