# UOGTO PR #128: independent costing receiving review and close-out

**Review date:** 20 November 2026 (Australia/Brisbane). **Disposition:** independent review evidence complete; **PR #128 blocked/returned to the existing costing writer**, not accepted or merged. **Receiving acknowledgement requested, not yet established.** This file is evidence in a *separate review lane*, not a change to the writer's costing ontology, queries, tests, source-import pipeline, track status or shared Conductor registry.

## Provenance and ownership

- Repository: [edithatogo/UOGTO](https://github.com/edithatogo/UOGTO).
- Current main as inspected: \`147aee40fd682c0949244b5e34897ed952ed4b73\`.
- Writer-owned [PR #128](https://github.com/edithatogo/UOGTO/pull/128): \`7e9075b8fd77543fc8853fab20319415cb86597d\` (\`codex/costing-valuation-reporting-20261108\`), three commits ahead and nine behind main; GitHub reports \`mergeable=false\`.
- Existing integration/admission owner: conversation \`6af96da1-c088-83ec-85a8-ab19f5f4512c\`. No integrator or writer authority is transferred by this review.
- PR128's branch-local Conductor metadata for \`costing_valuation_reporting_20261108\` says \`status=in_progress\`, \`execution_status=semantic_implementation_verified_with_baseline_suite_limitations\`. This is not completed/merged status on main.
- Previous full [independent receiving receipt](https://github.com/edithatogo/UOGTO/pull/128#issuecomment-7009348837) and [source inventory receipt](https://github.com/edithatogo/UOGTO/issues/134#issuecomment-7009365696) remain preserved.

## Exact source identities

| File | Git blob at pinned head |
| --- | --- |
| CQ21 conservation, PR128 | \`4fbdeb27546d3e78e384b85571b1962825f57574\` |
| CQ22 reporting, PR128 | \`56cf264601c8ea7188a406318f3563d181c92bfe\` |
| CQ23 infant attribution, PR128 | \`1028141d5c3677eaeb5a94fff7b21771b16630f2\` |
| CQ24 rate provenance, PR128 | \`834110549313faffbc82c2816ef3453f967a3cb3\` |
| CQ25 dynamic representation, main | \`9b6ee8deed098919bcba437f097acb6cded059fb\` |
| Main CQ expectation manifest | \`4c36f87f68d07397eb02f7dc61a186ed6115c709\` |
| PR128 CQ expectation manifest | \`f26edca35b836cbe8fb1403a47b668a07cb84063\` |
| Main CQ-ID reservation record | \`c9ad1dd41ee76e641b18f963f84c075680d2077c\` |

### Executed independent SPARQL verification

2026-11-19 pinned-query suite: Python 3.13.5, RDFLib 7.5.0, pytest 9.0.2, **8 passed / 3 failed (expected RED)**. Repeated on 2026-11-20: **8 passed / 3 failed**, 597 warnings, 0.45 s. The negative fixture outputs are unchanged:

1. CQ21 entirely unallocated 100-unit pool: pool row exists in RDFLib but \`allocatedTotal\` and \`recipientCount\` are **unbound**, rather than \`0\` / \`0\`. Other engines may omit the row; both outcomes violate the intended query contract.
2. CQ23 added alternative **direct** 7-unit valuation: infant A becomes **67**, incorrectly combining with baseline **60**.
3. CQ23 added alternative **pooled** 60+60 valuation: infants A/B become **120/150**, incorrectly combining with baseline **60/90**. The minimal alternative-pool RDF tests SPARQL aggregation only; complete SHACL conformance is not asserted.

CQ22 evidence and CQ24 rate-provenance baseline pass, as does a separate 4-row synthetic CQ25 main test. For an independently replayable *compact RED* reproduction, use adjacent \`check_cq21_cq23.py\` against an **actual checkout** of PR128 query files (not main). On the original head its three negative checks must fail:

\`\`\`shell
python conductor/reviews/pr128-independent-costing-20261120/check_cq21_cq23.py \
  --query-root PATH_TO_PR128_CHECKOUT/competency-questions --expect-original-head
# Exit 1: 2 baseline checks pass, 3 negative regression checks fail.
# Remove --expect-original-head only to test the costing writer's subsequent query edits.
\`\`\`

The standalone script was executed locally on 2026-11-20 against the exact query bytes: 2 passes / 3 failures, expected exit 1; \`python -m py_compile\` passed. No real patients, funding figures or empirical observations are involved. Local PySHACL was not installed, so **no new local SHACL pass** is claimed. The optional diagnostic repair prototypes in the prior receiving artifact passed in isolation but are *not* a validated patch or instruction to replace owner code.

### Hosted baseline results — not combined-tree acceptance

PR128 unchanged-head GitHub Actions: [Validate UOGTO 42431227335](https://github.com/edithatogo/UOGTO/actions/runs/42431227335) and [Required Gate 42431227269](https://github.com/edithatogo/UOGTO/actions/runs/42431227269) both successful: **344 passed, 1 skipped**, semantic audit 56 ontology files, 31 SHACL-conforming examples, expected **CQ01–24** results. Those baseline cases did **not** detect the independent edge cases, and main-only CQ25 was not present in the PR128 validation tree.

## Writer: bounded requested fixes and regressions

1. CQ21: anchor all \`CostPool\` rows, optionally aggregate allocations, and use typed zero-safe totals/counts, including a completely unallocated pool. Prove 0%, partial and 100% allocations, amount/residual conservation, no duplicate recipients.
2. CQ23: separate alternative scenarios across **both direct valuation lines and allocations**. Either require a single selected scenario consistently or group by \`scenarioKey\` and infant. Define/enforce unambiguous pool/allocation scenario provenance; prevent join multiplication for multi-component pools. Prove alternate direct + pooled lines and failure on missing/mixed scenarios. Allocation is an attribution view, **not** a second source expense.
3. Submit exact-head RED→GREEN fixture receipts and full semantic/SHACL/CQ validation; leave source catalogue rights/editorial claims unchanged. Writer should acknowledge receipt and state intended correction head in [PR #128](https://github.com/edithatogo/UOGTO/pull/128).

## Integrator: CQ01–25 boundary

A *static comparison* of remote manifests finds **21** entries on current main (CQ01–20 and CQ25) and **24** on PR128 (CQ01–24); their unique union has exactly **25** distinct filenames/numbers. The CQ25 file on main retains original blob \`9b6ee8...\`. **This is not an executed combined-tree validation.**

After writer corrections, the existing integrator should non-forcibly reconcile both branches, preserving main's CQ25 query, reservation, temporality test and all PR128 CQ21–24 queries/fixtures/profiles, then run the **complete CQ01–25 manifest and SPARQL execution** together with all semantic/SHACL, security and protected CI checks on the exact integrated commit. Do not suppress checks or relabel historical results. Integrator should record receiving acknowledgement and actual combined-tree results before admission; no separate review lane may merge PR128.

## Source/recovery hold: issue #134

[Issue #134](https://github.com/edithatogo/UOGTO/issues/134) remains open. Main's independently accessible 60 source seeds, 74 bibliography entries, 64 attribution records, 4 checked-in RDF source artifacts plus 35 reference-only sources, and 24 current-manuscript CSL references are **not evidence of recovering** the predecessor's reported 114 references, 57 raw-byte receipts, 22 RDF parses or 26-page PDF. Preserve original worktree/archive, raw-byte SHA-256, copyright/licence disposition, original manuscript, graphs, figures, execution environment, logs and dirty/untracked inventory. No source promotion, rights inference, manuscript publication, artifact destruction or recovery closure.

## Close-out boundary

**Review evidence:** complete and published for the independent reviewer lane. **Owner receipt:** pending express acknowledgement. **Costing acceptance, CQ01–25 integration, source recovery, scientific appraisal and release:** all remain with their existing owners and **not complete**. This evidence-only review PR must remain separate; do not merge or archive on an absent owner acknowledgement. Shared \`conductor/status.md\`, \`conductor/runlog.md\`, track registry, root CI and owner-owned code are intentionally untouched.
