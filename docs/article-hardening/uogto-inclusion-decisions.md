# UOGTO Inclusion Decisions

This file records the explicit dispositions used when assessing missing or partial game-theory and simulation elements.

Disposition set:
- `add_to_uogto`
- `align_external_only`
- `defer_pending_evidence`
- `reject_as_duplicate`
- `reject_out_of_scope`
- `requires_domain_review`

Guidance:
- Use `add_to_uogto` only when the construct improves competency-question coverage, interoperability, conceptual clarity, or validation/example completeness.
- Use `align_external_only` when the construct is real and relevant but better kept as a cross-reference or mapping target.
- Use `defer_pending_evidence` when evidence is promising but insufficient for a firm decision.
- Use `reject_as_duplicate` when UOGTO already covers the construct adequately.
- Use `reject_out_of_scope` when the construct is outside the current ontology scope.
- Use `requires_domain_review` when subject-matter judgement is needed before an ontology change is recorded.

| Candidate | Disposition | Summary |
| --- | --- | --- |
| Game theory survey source | add_to_uogto | Contributes core vocabulary and mapping anchors. |
| Discrete-event simulation schema | align_external_only | Best handled as an external alignment point. |
| ABM execution ontology | add_to_uogto | Strengthens execution, trace, and session semantics. |
| System-dynamics vocab | requires_domain_review | Needs tighter scope and case-study corroboration. |
| Negative evidence search | reject_out_of_scope | Search preserved as evidence, not as an inclusion candidate. |