# PR127 successor integration — 15 November 2026

This is a bounded integration receipt, not a new source study, provider
qualification, manuscript revision or publication decision. This record is part
of the existing semantic-reconciliation track; it creates no parallel owner.

## Ownership and pinned inputs

Dylan designated **UOGTO — Integration and source synthesis II** as successor to
**UOGTO — Source synthesis and implementation**. PR127 retains semantic/source
and manuscript integration. PR128 retains costing/valuation/reporting; PR130
retains its security provisioning hold. Maintenance, Paignia, Kairos and
application owners remain unchanged. No branch other than PR127 is updated.

- Published predecessor: `fa4e725d5f13830d3d44a2188c887fd546145ec3`.
- Inspected main: `0933b3100afa870ad4a92a10b0f13da159bd3b70`.
- Inspected PR128: `7e9075b8fd77543fc8853fab20319415cb86597d`.
- Common ancestor: `71139cca03f69256b9e88390dd21a3b8ad7f1dc1`.
- Two-parent refresh: `ea74389391247762d8df9c2ce691671a6a9af945`, tree
  `928ea4221735d7a05742fa8fa3c8b3411e7d3862`.
- Query migration: `da2553a5788175fc6573bccbf2ee1d9c7920723d`, tree
  `d491cbfe0d6494e6f027228bda93b2e349802a26`.

The receipt commit follows those code commits. Its own identity and actual hosted
results belong in the PR discussion; no file pretends to hash its own final commit.

## A — preserve both histories

The refresh has both the predecessor and inspected main as parents. It imports
main's exact `.github` tree and the exact `analyse_ontology_networks.py`,
`check_doi_status.py` and `score_arxiv_submission.py` blobs. Comparison with the
predecessor shows exactly 12 upstream file changes: eight issue forms, the
privacy/secrets workflow, and three maintenance files. Existing workflow gates,
thresholds and publication controls are unchanged.

The six overlapping generated JSON paths already have portable source paths on
PR127. Four are byte-identical to their main counterparts; the two mapping-table
copies remain byte-identical to each other at blob
`00b029b983895b1e6144ce2850942d3a966d59a4`. Their accepted-mapping value remains
four, not main's historical twelve. No table is regenerated or recertified by
this file-level reconciliation. The original source inventories remain unchanged.

## B — preserve the two CQ21 contributions without taking over PR128

PR128 keeps CQ21–24 for costing conservation, reporting evidence, infant
attribution and rate provenance. PR127 moves its temporality query to
`cq25-dynamic-game-representations.rq`. Its SPARQL bytes remain Git blob
`9b6ee8deed098919bcba437f097acb6cded059fb`; only the filename and active
expectation/test references change. All expectation thresholds, examples and
required bindings are preserved.

The machine-readable reservation record is
`validation/competency-query-id-reservations.json`. It does not insert unmerged
costing queries into the active manifest. Eventual integration must preserve the
union CQ01–20, costing CQ21–24 and temporality CQ25. This is a naming/manifest
contract, not acceptance of PR128, its numerical semantics or a combined branch.
Coordination is recorded in PR128 comment `6893343493` and PR127 comment
`6893346538`. No owner acknowledgement is inferred from silence.

`tests/test_pr127_pr128_query_numbering.py` covers actual manifest/file agreement,
unique numbers, reserved owner slots, identical query content, allowed absence of
pending costing slots, the declared five-query union, and six negative cases.
The existing temporality semantic test now loads CQ25.

## Verification scope and remaining gates

Standard sandbox Git access failed DNS. No DNS/proxy modification, network-policy
bypass, credential extraction or unofficial access route was used. The GitHub
connector provided exact Git objects and lease-checked, non-forced ref updates.
The isolated local directory is a recovered-file subset, not a full checkout.
Recovered baseline query, manifest and temporality-test bytes matched their
published Git blob IDs before edits.

Local numbering regression: **3 expected failures and 8 passes before migration;
11 passes after migration, with 1 full-directory check deliberately deselected**.
The missing checkout is not represented by placeholder source files. PySHACL was
not installed locally, so no local full ontology/SHACL suite is claimed. The
edited remote blobs were read back and matched the locally tested bytes.

Before any merge, the final head must pass current required checks and applicable
privacy/security checks, including the complete test suite and directory check.
Record actual commands, checkout revision/tree, results, skips and review findings
in the PR. Historical green results on `fa4e725` do not qualify this candidate.
No protected-branch bypass or release/paper submission is authorised by this receipt.

The [November quality snapshot](../../../docs/quality/README.md) remains historical
at the predecessor revision. Its old CQ21 locator and input hashes are not a
current-head fingerprint after the rename. Do not silently replace its dated
results or claim a newly rerun quality study.

## Residual predecessor handoff — unresolved, retain predecessor

Conversation-history retrieval found later reports dated 8 November 2026,
after the published predecessor commit: 114 cited references; 57 raw-byte
receipts; 22 parsed RDF artifacts; 50 manuscript citations; a 26-page PDF;
15 claims linked to 65 hashed artifacts; six classes and 21 properties; and
407 tests plus 100 reference subtests. **These are unverified predecessor reports,
not acquired artifacts or accepted results in this integration.**

No matching later push/archive receipt surfaced in that retrieval or the inspected
published branch state. The predecessor branch still pointed to `fa4e725` before
this refresh. No predecessor checkout was present in this sandbox; Desktop
Commander reported no connected device, and Browser access lacked the originating
context. This does not prove the work was never committed elsewhere or is lost.

Closure requires a durable commit or hashed archive/patch of the reported later
work, its base/head and dirty/untracked-file inventory, source-byte/rights manifests,
actual test/build logs and publication-state evidence. Reconcile those bytes against
this branch without overwriting them, rerun relevant checks, and record disposition
for every recovered change. Until then, retain the predecessor and any unverified
checkout. Published OCS/MNV/SGC leaf states are not promoted from conversation claims.
