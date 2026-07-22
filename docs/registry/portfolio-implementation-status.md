# Portfolio Registry Implementation Status

This ledger records repository-side implementation independently of GitHub API
availability. A repository marked `implemented` has a local readiness contract,
a focused validation test, and a Conductor track or equivalent registry plan.
No row claims external publication, DOI resolution, registry acceptance, or
provider response.

| Repository | Track / planning issue | Implementation evidence | Hosted integration | External gate |
| --- | --- | --- | --- | --- |
| UOGTO | #65; registry handoff track | BARTOC/RVA handoffs and packet tests | PR #101 | submission and provider response |
| corpus-cases-medilegal-nz | #19 | registry-readiness contract and test | PR #23 | dataset deposit and acceptance |
| fyi-archive | #226 | archive readiness contract and test | PR #230 | archive persistence |
| sm-govt-nz | #31 | archive readiness contract and test | PR #35 | archive publication |
| foi-process | #63 | event-log readiness contract and test | PR #68 merged | external deposit |
| reimbursement-atlas | #530 | database readiness contract and test | PR #550 | dataset publication |
| hathi-nz | #35 | rights-aware readiness contract and test | PR #39 | rights and registry response |
| dnz | #28 | DigitalNZ readiness contract and test | PR #32 | provider registration |
| nlp-policy-nz | #165 | artifact readiness checker, contract, and test | PR #174 | OCR, HF, and ontology gates |
| corpus-nz-hansard | #20 | Hansard readiness contract and test | PR #24 | archive publication |
| corpus-legislation-nz | #149 | Gazette readiness contract and test | PR #153 | source rights and registry |
| mchs | #356 | coding registry readiness contract and test | PR #360 | package and registry lanes |
| innovate | #398 | software readiness contract and test | PR #402 | external software registry |
| kairos | #90 | software readiness contract and test | PR #95 | package registry publication |
| ginsim | #17 | software readiness contract and test | PR #21 | package publication |
| nztaxmicrosim | #180 | software readiness contract and test | branch `codex/registry-readiness-submit-20260722` | PR creation pending API |
| sourceright | #72 | software readiness contract and test | PR #76 | package and MCP registries |
| voiage | #296 | software readiness contract and test | PR #302 | package registry publication |
| foi-o | #74 | ontology readiness contract and test | PR #94 | ontology registry response |

## State semantics

- `implemented` means local repository work is present and testable.
- `hosted integration` identifies the PR or branch carrying that work; it is
  not a merge claim.
- External gates stay open until authoritative provider evidence is recorded
  in the relevant issue and track.
