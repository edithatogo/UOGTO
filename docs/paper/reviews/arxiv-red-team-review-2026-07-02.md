# arXiv Red-Team Review

Date: `2026-07-02`

Runtime agent: `019f20ca-bbe7-7e93-831b-b906d7c50f63` (`Wegener`)

Recommendation: `submit-after-fixes-and-clean-ci`

## Summary

The red-team review focused on source-leak/privacy, dirty-tree provenance, strict arXiv engine gating, attestation, and false readiness claims. The review found in-scope fixes plus external blockers for clean-tree CI and remote attestation.

## Findings

| Classification | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| `fix_now` | high | Dirty-tree artifact was still listed as upload candidate evidence. | Contract remains local-provisional and blocks final readiness until a clean-tree manifest exists. |
| `fix_now` | high | Workflow path filters omitted `Makefile`, allowing arXiv gate changes to bypass CI. | Added `Makefile` to push and pull-request path filters. |
| `fix_now` | high | Privacy scanner did not catch common forward-slash local paths such as `C:/Users/...`, `/Users/...`, `/home/...`, or `/tmp/...`. | Extended private-path detection and added regression coverage. |
| `fix_now` | medium | Default `make arxiv-upload-ready` is local-development packaging, not strict-engine readiness. | Contract/status wording must keep final readiness tied to `arxiv-upload-ready-strict` or GitHub strict CI. |
| `defer` | medium | Manifest top-level compiler metadata can be read as actual engine proof. | Existing manifest source notes clarify intent; consider moving all compiler preview metadata under an intended-only object in a later cleanup. |
| `external_blocker` | high | Remote attestation remains pending. | Final publisher sign-off blocked until a clean GitHub run attests `dist/arxiv/SHA256SUMS`. |

## Required Gate Before Submission

- `make arxiv-upload-ready-strict` locally or equivalent GitHub arXiv Preflight success.
- Clean-tree upload manifest.
- GitHub artifact attestation over `dist/arxiv/SHA256SUMS`.
