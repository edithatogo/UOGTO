# arXiv Devil's Advocate Review

Date: `2026-07-02`

Runtime agent: `019f20c7-9208-7702-af6b-36d441a50041` (`Faraday`)

Recommendation: `do-not-submit-yet`

## Summary

The package is close in process terms, but the evidence does not yet support final submission readiness. The minimum before submission is a clean commit, strict arXiv-engine CI pass, attested upload artifact, regenerated clean-tree manifest, and tightened manuscript/supplement wording around mapping calibration, network sensitivity, examples, and agent-review evidence.

## Findings

| Classification | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| `external_blocker` | high | Final publisher gate is not met because the upload manifest records a dirty tree and remote attestation is pending. | Retained as a blocker in the contract. |
| `fix_now` | high | Validation/test claims could be misread as clean submission evidence despite dirty/untracked state. | Contract and status must describe them as local evidence until clean CI proves the same gate. |
| `fix_now` | high | Mapping robustness and calibration claims were too strong where calibration rows have zero pairs and network-sensitivity rows expose empty metrics. | Manuscript wording narrowed to treat these as evidence gaps or claim-discipline artefacts. |
| `fix_now` | high | Example coverage wording read broader than module-level SHACL/CQ support. | Manuscript wording narrowed to illustrative representative coverage. |
| `fix_now` | medium | Agent-contract claims were process evidence, not independent review evidence, unless review notes are archived. | This archived note records the devil's advocate review; red-team notes are tracked separately. |
| `fix_now` | medium | Supplement readiness language conflicted with completion criteria. | Supplement wording changed to pre-submission package under final gate. |
| `defer` | medium | Missing-game-theory disposition table remains thin and should not support strong coverage-boundary claims. | Keep as future-work/domain-review evidence only. |

## Required Gate Before Submission

- Clean commit.
- Strict arXiv-engine CI pass.
- Remote GitHub artifact attestation.
- Clean-tree upload manifest.
- Updated arXiv post-submission provenance record after arXiv assigns an ID.
