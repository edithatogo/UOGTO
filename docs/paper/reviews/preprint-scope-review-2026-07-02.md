# Preprint Scope Review

Date: `2026-07-02`

Question: Which aspects of the current package do not belong in the preprint body?

## Findings

| Classification | Scope issue | Disposition |
| --- | --- | --- |
| `fix_now` | arXiv preflight, source-package cleaning, and submission gates were too prominent in the abstract/results contribution framing. | Removed from the abstract and results contribution framing; retained only as source-integrity methods/process evidence. |
| `fix_now` | SourceRight and arXiv checks could be misread as scientific evidence for UOGTO rather than manuscript/repository hygiene. | Reframed as source-integrity checks, not ontology evidence. |
| `fix_now` | “Publication hardening” read like a result rather than a reproducibility/release practice. | Renamed to reproducibility packaging and removed submission-gate wording from the result. |
| `defer` | Detailed CI, GitHub attestation, red-team/devil's-advocate, and arXiv upload mechanics do not belong in the preprint body. | Kept in contract/process/review artifacts under `docs/paper/`; not in the manuscript body. |

## Boundary

The preprint should focus on ontology design, validation examples, competency queries, mapping evidence, quality metrics, and reproducibility surfaces. Submission mechanics belong in repository process documentation unless a short source-integrity methods note is needed.
