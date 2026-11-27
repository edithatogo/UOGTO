# UOGTO PR #128: independent costing receiving review and close-out

**Review date:** 20 November 2026 (Australia/Brisbane). **Disposition:** independent review evidence complete; **PR #128 blocked/returned to the existing costing writer**, not accepted or merged. **Receiving acknowledgement requested, not yet established.** This file is evidence in a *separate review lane*, not a change to the writer's costing ontology, queries, tests, source-import pipeline, track status or shared Conductor registry.

## Review amendment — 28 November 2026 (Australia/Brisbane)

The sections below retain the 20 November evidence; this amendment records the
current review. Main has advanced to `b3f1de0119ee1c1e49913d9c1f9284e053e43433`.
PR128 remains at `7e9075b8fd77543fc8853fab20319415cb86597d`, conflicted, and the
writer/integrator acknowledgement is still absent. The [renewed receiving
request](https://github.com/edithatogo/UOGTO/pull/128#issuecomment-7229938074)
preserves the existing writer and integrator assignments. No costing fix,
combined-tree acceptance, source recovery or archive action is claimed.

### Ponytail and correctness review

The complexity review found no unnecessary abstraction or dependency in the
compact reproducer. A separate correctness review found that its infant-keyed
CQ23 dictionaries would overwrite separate scenario rows from a future corrected
query. That could give order-dependent false passes or failures. The smallest
sound correction is to remove the optional hash bypass and require the two
original Git blobs on every run. This is now a historical reproducer only.
Future acceptance belongs to the writer's chosen scenario contract and must
preserve scenario identity and row multiplicity. The original 20 November log
and its old command remain historical evidence, not instructions for the updated
script.

Fresh local checks on current main plus these review changes used CPython
3.15.2, RDFLib 7.6.0, PySHACL 0.40.2 and pytest 9.2.0:

| Executed check | Observed result | Scope |
| --- | --- | --- |
| `make all` (`build`, `validate`, `test`, `coverage`) | Pass; 453 passed, 1 skipped, 24,707 warnings, pytest 65.44 s | Current main plus review files; excludes unmerged CQ21–24 |
| `scripts/maintenance/audit_semantics.py` | Pass; 55 ontology files | Current review tree |
| Updated historical reproducer | 2 baseline passes, 3 failures, exit 1 | Unchanged original PR128 CQ21/CQ23 blobs |
| Changed-query rejection | Both CQ21 and CQ23 mutations rejected before semantic execution | Mandatory original-byte guard |
| `python -m py_compile` | Pass | Updated reproducer |
| `git diff --check` | Pass | Review changes |

The compact run and guard results are in `review-checks-20261128.txt`. The
intentional semantic failures remain writer-owned defects; they are not waived
by the passing main-based suite. No new SHACL claim is made for the compact
diagnostic fixture. Fresh hosted checks and any merge result are recorded in
PR138 against the resulting remote head; historical checks are not relabelled.

### Integration now also preserves CQ26

Current main has 22 expectations: CQ01–20, CQ25 and CQ26. PR128 has 24:
CQ01–24. The static union is **26 distinct queries**. Satisfying the requested
CQ01–25 combined verification must also retain and execute CQ26; a 25-entry
manifest would now drop current-main work. Main's manifest blob is
`7d4ebbfb2a37987cf430b00500c88a124d0d3e82`, CQ25 remains
`9b6ee8deed098919bcba437f097acb6cded059fb`, and CQ26 is
`58c6381e001200bf3cb14fc0897dc189156eada5`. This inventory is not a combined run.

### Other merge-review dependencies

A newer [scheduled privacy run](https://github.com/edithatogo/UOGTO/actions/runs/45811415789)
failed on current main after an earlier successful push run. A sanitized
[handoff under existing security issue #107](https://github.com/edithatogo/UOGTO/issues/107#issuecomment-7229938315)
routes diagnosis to the existing central privacy rollout and UOGTO security
owners. This lane does not waive the failure, change shared policy, or disclose
matched values. Current PR checks must be inspected separately.

The bounded maintenance review found #110 and #114 contain small dead-code
deletions, but their old August checks do not validate current-main integration.
PR109 must retain its deterministic sample ordering: an independently replayed
four-row, two-sample control selects `[a,b]` for both input orders on current
main, while PR109 `279bfef55954de17600100db317e15b0a10ae511` changes from `[a,b]`
to `[z,y]` when the same rows are reversed. No shared writer branch was changed.

### Next research steps within existing ownership

These are falsifiable proposals, not achieved frontier results or new tracks.

1. **Costing writer and integrator:** qualify zero/partial/full conservation,
   distinct recipient counts, direct and pooled scenario isolation, multi-line
   pools and malformed scenario provenance using shape-qualified fixtures and
   complete result rows; then execute CQ01–26 on the actual combined commit.
2. **Existing SGC/Paignia owners:** use the existing information-set and
   discounted-Markov profiles for a real version-matched read/write round trip.
   Preserve full identities, labelled axes, payoff ownership, timing,
   probabilities and provider revisions. A mutated payoff owner or information
   partition must fail beside a valid passing control. Reuse current native
   receipts and SGC.02–05/SGC.08; do not add another acceptance framework.
3. **Existing FRT.04/FRT.07 and MAT.04 owners:** test semantic-loss detection on
   independently specified held-out cases and seeded mutations, comparing direct
   conversion, identity-only checks and the semantic checker. Predeclare missed
   errors, false rejection, supported-case denominator, runtime and memory, then
   ablate individual checks. Implementation alone cannot establish superiority.

These follow the existing [frontier programme](../../../docs/roadmap/frontier-programme-20261108.md)
and [Markov contract](../../../docs/contracts/executable-discounted-markov-profile-v1.md).
Issue #134 remains held; none of these proposals recovers predecessor artifacts,
grants source rights or qualifies manuscript publication.

## Provenance and ownership

- Repository: [edithatogo/UOGTO](https://github.com/edithatogo/UOGTO).
- Current main as inspected: `147aee40fd682c0949244b5e34897ed952ed4b73`.
- Writer-owned [PR #128](https://github.com/edithatogo/UOGTO/pull/128): `7e9075b8fd77543fc8853fab20319415cb86597d` (`codex/costing-valuation-reporting-20261108`), three commits ahead and nine behind main; GitHub reports `mergeable=false`.
- Existing integration/admission owner: conversation `6af96da1-c088-83ec-85a8-ab19f5f4512c`. No integrator or writer authority is transferred by this review.
- PR128's branch-local Conductor metadata for `costing_valuation_reporting_20261108` says `status=in_progress`, `execution_status=semantic_implementation_verified_with_baseline_suite_limitations`. This is not completed/merged status on main.
- Previous full [independent receiving receipt](https://github.com/edithatogo/UOGTO/pull/128#issuecomment-7009348837) and [source inventory receipt](https://github.com/edithatogo/UOGTO/issues/134#issuecomment-7009365696) remain preserved.

## Exact source identities

| File | Git blob at pinned head |
| --- | --- |
| CQ21 conservation, PR128 | `4fbdeb27546d3e78e384b85571b1962825f57574` |
| CQ22 reporting, PR128 | `56cf264601c8ea7188a406318f3563d181c92bfe` |
| CQ23 infant attribution, PR128 | `1028141d5c3677eaeb5a94fff7b21771b16630f2` |
| CQ24 rate provenance, PR128 | `834110549313faffbc82c2816ef3453f967a3cb3` |
| CQ25 dynamic representation, main | `9b6ee8deed098919bcba437f097acb6cded059fb` |
| Main CQ expectation manifest | `4c36f87f68d07397eb02f7dc61a186ed6115c709` |
| PR128 CQ expectation manifest | `f26edca35b836cbe8fb1403a47b668a07cb84063` |
| Main CQ-ID reservation record | `c9ad1dd41ee76e641b18f963f84c075680d2077c` |

### Executed independent SPARQL verification

2026-11-19 pinned-query suite: Python 3.13.5, RDFLib 7.5.0, pytest 9.0.2, **8 passed / 3 failed (expected RED)**. Repeated on 2026-11-20: **8 passed / 3 failed**, 597 warnings, 0.45 s. The negative fixture outputs are unchanged:

1. CQ21 entirely unallocated 100-unit pool: pool row exists in RDFLib but `allocatedTotal` and `recipientCount` are **unbound**, rather than `0` / `0`. Other engines may omit the row; both outcomes violate the intended query contract.
2. CQ23 added alternative **direct** 7-unit valuation: infant A becomes **67**, incorrectly combining with baseline **60**.
3. CQ23 added alternative **pooled** 60+60 valuation: infants A/B become **120/150**, incorrectly combining with baseline **60/90**. The minimal alternative-pool RDF tests SPARQL aggregation only; complete SHACL conformance is not asserted.

CQ22 evidence and CQ24 rate-provenance baseline pass, as does a separate 4-row synthetic CQ25 main test. For an independently replayable *compact RED* reproduction, use adjacent `check_cq21_cq23.py` against an **actual checkout** of PR128 query files (not main). On the original head its three negative checks must fail:

```shell
python conductor/reviews/pr128-independent-costing-20261120/check_cq21_cq23.py \
  --query-root PATH_TO_PR128_CHECKOUT/competency-questions
# Exit 1: 2 baseline checks pass, 3 negative regression checks fail.
# Only the pinned historical bytes are accepted; changed queries are rejected.
```

The standalone script was executed locally on 2026-11-20 against the exact query bytes: 2 passes / 3 failures, expected exit 1; `python -m py_compile` passed. No real patients, funding figures or empirical observations are involved. Local PySHACL was not installed, so **no new local SHACL pass** is claimed. The optional diagnostic repair prototypes in the prior receiving artifact passed in isolation but are *not* a validated patch or instruction to replace owner code.

### Hosted baseline results — not combined-tree acceptance

PR128 unchanged-head GitHub Actions: [Validate UOGTO 42431227335](https://github.com/edithatogo/UOGTO/actions/runs/42431227335) and [Required Gate 42431227269](https://github.com/edithatogo/UOGTO/actions/runs/42431227269) both successful: **344 passed, 1 skipped**, semantic audit 56 ontology files, 31 SHACL-conforming examples, expected **CQ01–24** results. Those baseline cases did **not** detect the independent edge cases, and main-only CQ25 was not present in the PR128 validation tree.

## Writer: bounded requested fixes and regressions

1. CQ21: anchor all `CostPool` rows, optionally aggregate allocations, and use typed zero-safe totals/counts, including a completely unallocated pool. Prove 0%, partial and 100% allocations, amount/residual conservation, no duplicate recipients.
2. CQ23: separate alternative scenarios across **both direct valuation lines and allocations**. Either require a single selected scenario consistently or group by `scenarioKey` and infant. Define/enforce unambiguous pool/allocation scenario provenance; prevent join multiplication for multi-component pools. Prove alternate direct + pooled lines and failure on missing/mixed scenarios. Allocation is an attribution view, **not** a second source expense.
3. Submit exact-head RED→GREEN fixture receipts and full semantic/SHACL/CQ validation; leave source catalogue rights/editorial claims unchanged. Writer should acknowledge receipt and state intended correction head in [PR #128](https://github.com/edithatogo/UOGTO/pull/128).

## Integrator: CQ01–25 boundary

A *static comparison* of remote manifests finds **21** entries on current main (CQ01–20 and CQ25) and **24** on PR128 (CQ01–24); their unique union has exactly **25** distinct filenames/numbers. The CQ25 file on main retains original blob `9b6ee8...`. **This is not an executed combined-tree validation.**

After writer corrections, the existing integrator should non-forcibly reconcile both branches, preserving main's CQ25 query, reservation, temporality test and all PR128 CQ21–24 queries/fixtures/profiles, then run the **complete CQ01–25 manifest and SPARQL execution** together with all semantic/SHACL, security and protected CI checks on the exact integrated commit. Do not suppress checks or relabel historical results. Integrator should record receiving acknowledgement and actual combined-tree results before admission; no separate review lane may merge PR128.

## Source/recovery hold: issue #134

[Issue #134](https://github.com/edithatogo/UOGTO/issues/134) remains open. Main's independently accessible 60 source seeds, 74 bibliography entries, 64 attribution records, 4 checked-in RDF source artifacts plus 35 reference-only sources, and 24 current-manuscript CSL references are **not evidence of recovering** the predecessor's reported 114 references, 57 raw-byte receipts, 22 RDF parses or 26-page PDF. Preserve original worktree/archive, raw-byte SHA-256, copyright/licence disposition, original manuscript, graphs, figures, execution environment, logs and dirty/untracked inventory. No source promotion, rights inference, manuscript publication, artifact destruction or recovery closure.

## Close-out boundary

**Review evidence:** published for the independent reviewer lane. **Owner receipt:** pending express acknowledgement. **Costing acceptance, combined CQ integration, source recovery, scientific appraisal and release:** all remain with their existing owners and **not complete**. Under the user's 28 November review-and-merge instruction, this separate evidence PR may be merged after its current checks pass; that records the review without admitting costing or completing the handoff. Do not archive this lane. Shared `conductor/status.md`, `conductor/runlog.md`, track registry, root CI and owner-owned code are intentionally untouched.
